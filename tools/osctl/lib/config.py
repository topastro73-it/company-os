"""config.py — parser di config/acl.yaml e config/people.yaml.

Usa PyYAML se disponibile; altrimenti un parser YAML minimale sufficiente per
i file di config del repo (mappe annidate per indentazione, liste inline
`[a, b]`, liste a blocco `- item`, stringhe quotate, commenti).

Risolve i ruoli speciali (`admin`, `all_internal`, `everyone`) in liste di
email a partire da people.yaml (campo `emails`). Persone senza email vengono
saltate con un warning.
"""

import os
import sys

try:
    import yaml as _pyyaml
except ImportError:
    _pyyaml = None


class ConfigError(Exception):
    pass


# ---------------------------------------------------------------------------
# Parser YAML minimale (fallback quando PyYAML non è installato)
# ---------------------------------------------------------------------------

def _strip_comment(line):
    """Rimuove i commenti `#` fuori dalle stringhe quotate."""
    out = []
    quote = None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _split_top(s):
    """Divide su virgole non annidate in quote/parentesi."""
    parts, buf, depth, quote = [], [], 0, None
    for ch in s:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
            buf.append(ch)
        elif ch in "[{":
            depth += 1
            buf.append(ch)
        elif ch in "]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf))
    return parts


def _scalar(tok):
    tok = tok.strip()
    if tok in ("", "~", "null", "Null", "NULL", "None"):
        return None
    if len(tok) >= 2 and tok[0] in ('"', "'") and tok.endswith(tok[0]):
        return tok[1:-1]
    if tok in ("true", "True"):
        return True
    if tok in ("false", "False"):
        return False
    try:
        return int(tok)
    except ValueError:
        return tok


def _inline(tok):
    tok = tok.strip()
    if tok.startswith("[") and tok.endswith("]"):
        inner = tok[1:-1].strip()
        return [_inline(t) for t in _split_top(inner)] if inner else []
    if tok.startswith("{") and tok.endswith("}"):
        d = {}
        for part in _split_top(tok[1:-1]):
            k, _, v = part.partition(":")
            d[_scalar(k)] = _inline(v)
        return d
    return _scalar(tok)


_BLOCK_SCALARS = (">", "|", ">-", "|-", ">+", "|+")


def _block_scalar(lines, i, ind, marker):
    """Scalari a blocco `>`/`|` (approssimati: basta per i file di config)."""
    parts = []
    while i < len(lines) and lines[i][0] > ind:
        parts.append(lines[i][1])
        i += 1
    joiner = "\n" if marker.startswith("|") else " "
    text = joiner.join(parts)
    if not marker.endswith("-") and text:
        text += "\n"
    return text, i


def _parse_block(lines, i, indent):
    """Parsa un blocco (dict o list) a partire da lines[i] con indentazione data."""
    if i >= len(lines):
        return None, i
    if lines[i][1].startswith("- "):
        items = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            items.append(_inline(lines[i][1][2:]))
            i += 1
        return items, i
    d = {}
    while i < len(lines):
        ind, content = lines[i]
        if ind != indent or content.startswith("- "):
            break
        key, sep, rest = content.partition(":")
        if not sep:
            raise ConfigError("riga YAML non riconosciuta: %r" % content)
        key, rest = key.strip(), rest.strip()
        i += 1
        if rest in _BLOCK_SCALARS:
            d[key], i = _block_scalar(lines, i, ind, rest)
        elif rest:
            d[key] = _inline(rest)
        elif i < len(lines) and (
            lines[i][0] > ind
            or (lines[i][0] == ind and lines[i][1].startswith("- "))
        ):
            d[key], i = _parse_block(lines, i, lines[i][0])
        else:
            d[key] = None
    return d, i


def _parse_yaml_min(text):
    lines = []
    for raw in text.splitlines():
        line = _strip_comment(raw.expandtabs(2))
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line.strip()))
    if not lines:
        return {}
    obj, _ = _parse_block(lines, 0, lines[0][0])
    return obj


def load_yaml(path):
    """Carica un file YAML (PyYAML se c'è, altrimenti parser minimale).

    Se il file non esiste ma c'è la variante `.example.yaml` (istanza template non
    ancora configurata), la usa come fallback con un avviso — così `osctl status` e i
    dry-run funzionano su un clone fresco. Le operazioni reali su Drive falliranno
    comunque perché i valori sono placeholder (root_id vuoto ecc.).
    """
    if not os.path.isfile(path):
        example = path.replace(".yaml", ".example.yaml")
        if example != path and os.path.isfile(example):
            print("  ⚠️  %s assente — uso %s (template non ancora configurato: "
                  "copia in %s e compila)" % (
                      os.path.basename(path), os.path.basename(example),
                      os.path.basename(path)), file=sys.stderr)
            path = example
        else:
            raise ConfigError("file di config mancante: %s" % path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if _pyyaml is not None:
        return _pyyaml.safe_load(text) or {}
    return _parse_yaml_min(text) or {}


# ---------------------------------------------------------------------------
# Config aziendale: acl.yaml + people.yaml
# ---------------------------------------------------------------------------

def find_repo_root(start=None):
    """Risale le directory fino a trovare la radice del repo (contiene .git)."""
    d = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    # fallback: posizione nota di questo file (tools/osctl/lib/config.py)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


SPECIAL_ROLES = ("admin", "all_internal", "everyone")


class Config:
    """Vista unificata su acl.yaml + people.yaml, con risoluzione ruoli → email."""

    def __init__(self, repo_root=None):
        self.root = repo_root or find_repo_root()
        self.acl = load_yaml(os.path.join(self.root, "config", "acl.yaml"))
        people_doc = load_yaml(os.path.join(self.root, "config", "people.yaml"))
        self.people = people_doc.get("people") or {}
        self.admins = people_doc.get("admin") or []
        self.warnings = []
        self._warned = set()
        self._warned_onboarding = set()

    # -- persone -----------------------------------------------------------

    def emails_for(self, person_key):
        person = self.people.get(person_key) or {}
        emails = person.get("emails") or []
        return [e for e in emails if e]

    def primary_email(self, person_key):
        emails = self.emails_for(person_key)
        if emails:
            return emails[0]
        if person_key not in self._warned:
            self._warned.add(person_key)
            msg = "persona %r senza campo `emails` in people.yaml — saltata" % person_key
            self.warnings.append(msg)
            print("  ⚠️  %s" % msg, file=sys.stderr)
        return None

    def _people_by_type(self, wanted):
        return [k for k, p in self.people.items() if (p or {}).get("type") == wanted]

    def resolve(self, names):
        """Risolve una lista di persone/ruoli speciali in una lista di email (dedup)."""
        keys = []
        for name in names or []:
            if name == "admin":
                keys.extend(self.admins)
            elif name == "all_internal":
                keys.extend(self._people_by_type("internal"))
            elif name == "everyone":
                keys.extend(self.people.keys())
            else:
                # accetta sia chiavi persona che sottozone tipo "finance.bandi"
                keys.append(name.split(".", 1)[0])
        out = []
        for k in keys:
            if k not in self.people:
                if k not in self._warned:
                    self._warned.add(k)
                    self.warnings.append("nome %r non presente in people.yaml" % k)
                    print("  ⚠️  nome %r non presente in people.yaml" % k, file=sys.stderr)
                continue
            if not self.is_onboarded(k):
                continue
            emails = self.emails_for(k)
            if not emails:
                self.primary_email(k)  # emette il warning "senza email"
                continue
            for email in emails:
                if email not in out:
                    out.append(email)
        return out

    def is_onboarded(self, person_key):
        """Ammesso alla matrice ACL: gli admin sempre; gli altri solo con
        `onboarded: true` esplicito in people.yaml (attivato via intervista
        di onboarding, os/protocols/onboarding-collaborator.md)."""
        if person_key in self.admins:
            return True
        person = self.people.get(person_key) or {}
        onboarded = person.get("onboarded")
        if onboarded is not True and person_key not in self._warned_onboarding:
            self._warned_onboarding.add(person_key)
            print("  ⏸  %r non ancora onboardato (onboarded: true mancante) — escluso dalla matrice"
                  % person_key, file=sys.stderr)
        return onboarded is True

    def all_emails(self):
        """Mappa email (lowercase) → chiave persona, per il matching in audit."""
        out = {}
        for k in self.people:
            for e in self.emails_for(k):
                out[e.lower()] = k
        return out

    # -- lingua ---------------------------------------------------------------

    @property
    def language(self):
        """Lingua operativa da config/company.yaml (default: it). Vedi os/protocols/language.md."""
        if not hasattr(self, "_language"):
            try:
                doc = load_yaml(os.path.join(self.root, "config", "company.yaml"))
            except ConfigError:
                doc = {}
            self._language = str((doc or {}).get("language") or "it").lower()
        return self._language

    # -- zone ----------------------------------------------------------------

    @property
    def zones(self):
        return self.acl.get("zones") or {}

    @property
    def drive(self):
        return self.acl.get("drive") or {}

    @property
    def publish(self):
        return self.acl.get("publish") or {}

    def zone_expected_acl(self, zone_name, node=None):
        """Matrice attesa {email: 'writer'|'reader'} per una zona (o sottocartella).

        I writer vincono sui reader. Le zone `git_to_drive` hanno writer solo
        via git: su Drive tutti sono reader.
        """
        zone = node if node is not None else self.zones.get(zone_name)
        if zone is None:
            raise ConfigError("zona sconosciuta: %s" % zone_name)
        expected = {}
        readers = self.resolve(zone.get("read") or [])
        writers = self.resolve(zone.get("write") or [])
        if zone.get("sync") == "git_to_drive":
            writers = []  # su Drive nessuno scrive: il master è git
        for e in readers:
            expected[e.lower()] = "reader"
        for e in writers:
            expected[e.lower()] = "writer"
        return expected
