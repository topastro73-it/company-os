"""drive.py — wrapper minimale su Google Drive API v3 per osctl.

Auth da service account: la chiave JSON è indicata dall'env `GDRIVE_SA_KEY_PATH`.
Supporta Shared Drive (supportsAllDrives su ogni chiamata).

Se google-api-python-client non è importabile, le funzioni falliscono con un
messaggio d'installazione chiaro — i comandi che non toccano Drive (status,
parser) non passano di qui.
"""

import io
import mimetypes
import os
import re
from datetime import datetime, timezone

FOLDER_MIME = "application/vnd.google-apps.folder"
GDOC_MIME = "application/vnd.google-apps.document"
SCOPES = ["https://www.googleapis.com/auth/drive"]

INSTALL_MSG = (
    "google-api-python-client non installato.\n"
    "Installa con:  pip install google-api-python-client google-auth pyyaml"
)


class DriveError(Exception):
    pass


def _load_google():
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
        from google.oauth2 import service_account
    except ImportError:
        raise DriveError(INSTALL_MSG)
    return build, MediaIoBaseUpload, MediaIoBaseDownload, service_account


def sa_client_email():
    """Email del service account (per escluderlo dall'acl-audit), se leggibile."""
    key_path = os.environ.get("GDRIVE_SA_KEY_PATH", "")
    if key_path and os.path.isfile(key_path):
        try:
            import json
            with open(key_path, encoding="utf-8") as fh:
                return (json.load(fh).get("client_email") or "").lower()
        except (OSError, ValueError):
            pass
    return ""


def parse_rfc3339(ts):
    """'2026-07-04T10:00:00.000Z' → epoch seconds (0 se non parsabile)."""
    if not ts:
        return 0.0
    try:
        return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").replace(
            tzinfo=timezone.utc).timestamp()
    except ValueError:
        return 0.0


# ---------------------------------------------------------------------------
# Conversione markdown → HTML semplice (per l'import come Google Doc)
# ---------------------------------------------------------------------------

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline_html(s):
    s = _esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md_text, title=""):
    """Conversione markdown → HTML volutamente semplice: heading, liste,
    tabelle, code block, blockquote, paragrafi. Basta per l'import Drive."""
    md_text = strip_frontmatter(md_text)
    out = ["<html><head><meta charset='utf-8'><title>%s</title></head><body>" % _esc(title)]
    lines = md_text.splitlines()
    i, in_code, in_list, in_quote = 0, False, False, False

    def close_blocks():
        nonlocal in_list, in_quote
        if in_list:
            out.append("</ul>")
            in_list = False
        if in_quote:
            out.append("</blockquote>")
            in_quote = False

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                out.append("</pre>")
            else:
                close_blocks()
                out.append("<pre>")
            in_code = not in_code
            i += 1
            continue
        if in_code:
            out.append(_esc(line))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_blocks()
            n = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (n, _inline_html(m.group(2)), n))
        elif re.match(r"^\s*([-*]|\d+\.)\s+", line):
            if not in_list:
                close_blocks()
                out.append("<ul>")
                in_list = True
            out.append("<li>%s</li>" % _inline_html(re.sub(r"^\s*([-*]|\d+\.)\s+", "", line)))
        elif line.strip().startswith(">"):
            if not in_quote:
                close_blocks()
                out.append("<blockquote>")
                in_quote = True
            out.append("<p>%s</p>" % _inline_html(line.strip().lstrip("> ")))
        elif line.strip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1] if i + 1 < len(lines) else ""):
            close_blocks()
            out.append("<table border='1' cellspacing='0' cellpadding='4'>")
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<tr>" + "".join("<th>%s</th>" % _inline_html(c) for c in cells) + "</tr>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join("<td>%s</td>" % _inline_html(c) for c in cells) + "</tr>")
                i += 1
            out.append("</table>")
            continue
        elif re.match(r"^\s*(---+|\*\*\*+)\s*$", line):
            close_blocks()
            out.append("<hr>")
        elif line.strip():
            close_blocks()
            out.append("<p>%s</p>" % _inline_html(line))
        else:
            close_blocks()
        i += 1
    close_blocks()
    if in_code:
        out.append("</pre>")
    out.append("</body></html>")
    return "\n".join(out)


def strip_frontmatter(text):
    m = re.match(r"^---\s*\n.*?\n---\s*\n?", text, re.DOTALL)
    return text[m.end():] if m else text


# ---------------------------------------------------------------------------
# Client Drive
# ---------------------------------------------------------------------------

class Drive:
    def __init__(self, cfg):
        build, self._MediaUpload, self._MediaDownload, sa = _load_google()
        key_path = os.environ.get("GDRIVE_SA_KEY_PATH", "")
        if not key_path or not os.path.isfile(key_path):
            raise DriveError(
                "GDRIVE_SA_KEY_PATH non impostata o file inesistente.\n"
                "Esporta il path della chiave JSON del service account "
                "(vedi bootstrap/README.md).")
        creds = sa.Credentials.from_service_account_file(key_path, scopes=SCOPES)
        self.svc = build("drive", "v3", credentials=creds, cache_discovery=False)
        d = cfg.drive
        self.root_id = d.get("root_id") or ""
        self.shared_drive = bool(d.get("shared_drive"))
        if not self.root_id:
            raise DriveError(
                "config/acl.yaml: drive.root_id vuoto — crea lo Shared Drive, "
                "condividilo col service account e incolla l'ID (vedi bootstrap/README.md).")

    # -- helpers -------------------------------------------------------------

    def _list_kwargs(self):
        kw = {"supportsAllDrives": True, "includeItemsFromAllDrives": True}
        if self.shared_drive:
            kw.update({"corpora": "drive", "driveId": self.root_id})
        return kw

    def list_children(self, folder_id):
        """Tutti i figli diretti (non trashed) di una cartella."""
        items, page = [], None
        while True:
            resp = self.svc.files().list(
                q="'%s' in parents and trashed=false" % folder_id,
                fields="nextPageToken,files(id,name,mimeType,modifiedTime)",
                pageSize=200, pageToken=page, **self._list_kwargs()).execute()
            items.extend(resp.get("files", []))
            page = resp.get("nextPageToken")
            if not page:
                return items

    def find_child(self, parent_id, name, mime=None):
        for f in self.list_children(parent_id):
            if f["name"] == name and (mime is None or f["mimeType"] == mime):
                return f
        return None

    # -- folders ---------------------------------------------------------------

    def ensure_folder(self, path, parent_id=None):
        """Crea (se serve) la catena di cartelle `a/b/c` e ritorna l'ID finale."""
        parent = parent_id or self.root_id
        for part in [p for p in path.split("/") if p]:
            found = self.find_child(parent, part, FOLDER_MIME)
            if found:
                parent = found["id"]
            else:
                created = self.svc.files().create(
                    body={"name": part, "mimeType": FOLDER_MIME, "parents": [parent]},
                    fields="id", supportsAllDrives=True).execute()
                parent = created["id"]
        return parent

    # -- files ---------------------------------------------------------------

    def upload_or_update_file(self, local_path, parent_id, name=None, mime=None):
        """Carica un file, o lo aggiorna se un file con lo stesso nome esiste già."""
        name = name or os.path.basename(local_path)
        if mime is None:
            mime = ("text/markdown" if local_path.endswith(".md")
                    else mimetypes.guess_type(local_path)[0] or "application/octet-stream")
        with open(local_path, "rb") as fh:
            media = self._MediaUpload(io.BytesIO(fh.read()), mimetype=mime, resumable=False)
        existing = self.find_child(parent_id, name)
        if existing and existing["mimeType"] != FOLDER_MIME and existing["mimeType"] != GDOC_MIME:
            self.svc.files().update(
                fileId=existing["id"], media_body=media,
                supportsAllDrives=True).execute()
            return existing["id"], "aggiornato"
        created = self.svc.files().create(
            body={"name": name, "parents": [parent_id]},
            media_body=media, fields="id", supportsAllDrives=True).execute()
        return created["id"], "creato"

    def convert_md_to_gdoc(self, md_path, parent_id, name=None):
        """md → HTML semplice → import come Google Doc. Aggiorna il gdoc
        esistente con lo stesso nome, se c'è."""
        name = name or os.path.splitext(os.path.basename(md_path))[0]
        with open(md_path, encoding="utf-8", errors="ignore") as fh:
            html = md_to_html(fh.read(), title=name)
        media = self._MediaUpload(io.BytesIO(html.encode("utf-8")),
                                  mimetype="text/html", resumable=False)
        existing = self.find_child(parent_id, name, GDOC_MIME)
        if existing:
            self.svc.files().update(
                fileId=existing["id"], media_body=media,
                supportsAllDrives=True).execute()
            return existing["id"], "aggiornato"
        created = self.svc.files().create(
            body={"name": name, "mimeType": GDOC_MIME, "parents": [parent_id]},
            media_body=media, fields="id", supportsAllDrives=True).execute()
        return created["id"], "creato"

    # -- permissions -----------------------------------------------------------

    def list_permissions(self, file_id):
        perms, page = [], None
        while True:
            resp = self.svc.permissions().list(
                fileId=file_id, pageSize=100, pageToken=page,
                fields="nextPageToken,permissions(id,type,role,emailAddress,permissionDetails)",
                supportsAllDrives=True).execute()
            perms.extend(resp.get("permissions", []))
            page = resp.get("nextPageToken")
            if not page:
                return perms

    def set_permission(self, file_id, email, role):
        """role: 'reader' | 'writer'."""
        self.svc.permissions().create(
            fileId=file_id,
            body={"type": "user", "role": role, "emailAddress": email},
            sendNotificationEmail=False, supportsAllDrives=True).execute()

    def remove_permission(self, file_id, perm_id):
        self.svc.permissions().delete(
            fileId=file_id, permissionId=perm_id, supportsAllDrives=True).execute()

    # -- download -----------------------------------------------------------

    def _download(self, request, dest):
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        buf = io.BytesIO()
        downloader = self._MediaDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        with open(dest, "wb") as fh:
            fh.write(buf.getvalue())

    def download_folder_tree(self, folder_id, local_dir, stats=None):
        """Scarica ricorsivamente una cartella Drive in `local_dir`.

        Google Doc → export markdown (.md); Sheet → CSV; altri tipi
        google-apps vengono saltati con nota. Ritorna le statistiche.
        """
        stats = stats if stats is not None else {"files": 0, "skipped": 0}
        for f in self.list_children(folder_id):
            name, mime = f["name"], f["mimeType"]
            if mime == FOLDER_MIME:
                self.download_folder_tree(f["id"], os.path.join(local_dir, name), stats)
            elif mime == GDOC_MIME:
                try:
                    req = self.svc.files().export_media(fileId=f["id"], mimeType="text/markdown")
                    self._download(req, os.path.join(local_dir, name + ".md"))
                except Exception:
                    req = self.svc.files().export_media(fileId=f["id"], mimeType="text/plain")
                    self._download(req, os.path.join(local_dir, name + ".txt"))
                stats["files"] += 1
            elif mime == "application/vnd.google-apps.spreadsheet":
                req = self.svc.files().export_media(fileId=f["id"], mimeType="text/csv")
                self._download(req, os.path.join(local_dir, name + ".csv"))
                stats["files"] += 1
            elif mime.startswith("application/vnd.google-apps."):
                print("    · saltato (tipo Google non esportabile): %s" % name)
                stats["skipped"] += 1
            else:
                req = self.svc.files().get_media(fileId=f["id"])
                self._download(req, os.path.join(local_dir, name))
                stats["files"] += 1
        return stats
