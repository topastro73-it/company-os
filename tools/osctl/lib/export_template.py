"""export_template.py — deriva il template pubblico `company-os` da questa istanza.

È la meccanica di `/admin export-template` (os/agents/admin/commands/export-template.md):

  1. copia i file di sistema (`config/export.yaml → include`) meno quelli d'istanza (`exclude`)
  2. toglie le righe marcate `@instance` e i blocchi `@instance-begin` … `@instance-end`
  3. merge, non sovrascrittura: le varianti `.en.md` e i file `template_owned` del template
     restano; si cancellano solo i file base spariti da qui (con la loro variante orfana)
  4. leak-scan su tutto il template: un solo hit → export bloccato
  5. elenca le traduzioni da fare (base nuovo) e da rifare (base cambiato)

Dry-run di default: `--apply` scrive nel working tree del template. Non committa e non
pusha mai: il push al repo pubblico passa da PREPARE → APPROVE → EXECUTE.
"""

import fnmatch
import os
import re
import shutil

from lib.config import load_yaml

# Il marker vale solo dentro un commento (`<!--`, `#`, `//`): così il codice e la doc che ne
# parlano non vengono scambiati per righe d'istanza.
MARK_RE = re.compile(r"(?:<!--|#|//)\s*@instance(-begin|-end)?(?![\w-])")
TEXT_EXT = {".md", ".py", ".sh", ".js", ".yml", ".yaml", ".txt", ".html", ".css", ".json", ""}


def _match(path, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return True
        if pat.endswith("/**") and (path == pat[:-3] or path.startswith(pat[:-2])):
            return True
    return False


def _is_text(path):
    return os.path.splitext(path)[1].lower() in TEXT_EXT


def strip_instance(text):
    """Toglie righe `@instance` e blocchi `@instance-begin/end`. Errore se un blocco non chiude."""
    out, skip = [], False
    for n, line in enumerate(text.splitlines(keepends=True), 1):
        m = MARK_RE.search(line)
        kind = m.group(1) if m else None
        if kind == "-begin":
            if skip:
                raise ValueError("riga %d: @instance-begin annidato" % n)
            skip = True
            continue
        if kind == "-end":
            if not skip:
                raise ValueError("riga %d: @instance-end senza begin" % n)
            skip = False
            continue
        if skip or m:
            continue
        out.append(line)
    if skip:
        raise ValueError("@instance-begin senza @instance-end")
    return "".join(out)


def _walk(root, rels):
    for rel in rels:
        top = os.path.join(root, rel)
        if os.path.isfile(top):
            yield rel
            continue
        for dirpath, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                yield os.path.relpath(os.path.join(dirpath, f), root)


def _deny_terms(repo, ecfg):
    terms = set(ecfg.get("deny_terms") or [])
    company = (load_yaml(os.path.join(repo, "config/company.yaml")) or {}).get("company", {})
    for k in ("legal_name", "short_name"):
        if company.get(k):
            terms.add(str(company[k]))
    if company.get("website"):
        terms.add(str(company["website"]).split(".")[0])
    people = (load_yaml(os.path.join(repo, "config/people.yaml")) or {}).get("people", {}) or {}
    for p in people.values():
        if isinstance(p, dict):
            if p.get("name"):
                terms.add(str(p["name"]))
            for e in p.get("emails") or []:
                terms.add(str(e))
    clienti = os.path.join(repo, "company/clienti")
    if os.path.isdir(clienti):
        for d in os.listdir(clienti):
            if os.path.isdir(os.path.join(clienti, d)):
                terms.add(d)
    allow = {a.lower() for a in ecfg.get("allow_terms") or []}
    return sorted(t for t in terms if len(t) >= 3 and t.lower() not in allow)


def leak_scan(root, terms, skip=()):
    rx = re.compile(r"(?<![\w-])(%s)(?![\w])" % "|".join(re.escape(t) for t in terms), re.I)
    hits = []
    for rel in _walk(root, ["."]):
        rel = os.path.normpath(rel)
        if not _is_text(rel) or _match(rel, ["**/node_modules/**"] + list(skip)):
            continue
        try:
            text = open(os.path.join(root, rel), encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            m = rx.search(line)
            if m:
                hits.append((rel, n, m.group(1)))
    return hits


def plan_export(repo, ecfg, target):
    include = ecfg.get("include") or []
    exclude = ecfg.get("exclude") or []
    owned = ecfg.get("template_owned") or []

    src = {}
    for rel in _walk(repo, include):
        rel = os.path.normpath(rel)
        if rel.endswith(".en.md") or _match(rel, exclude) or _match(rel, owned):
            continue
        src[rel] = os.path.join(repo, rel)

    plan = {"add": [], "update": [], "delete": [], "orphan": [], "translate": [],
            "retranslate": [], "owned_changed": [], "errors": {}}
    rendered = {}
    for rel, path in sorted(src.items()):
        if _is_text(rel):
            try:
                data = strip_instance(open(path, encoding="utf-8").read()).encode("utf-8")
            except ValueError as e:
                plan["errors"][rel] = str(e)
                continue
            except UnicodeDecodeError:
                data = open(path, "rb").read()
        else:
            data = open(path, "rb").read()
        rendered[rel] = data
        dst = os.path.join(target, rel)
        if not os.path.exists(dst):
            plan["add"].append(rel)
        elif open(dst, "rb").read() != data:
            plan["update"].append(rel)
        else:
            continue
        if rel.endswith(".md"):
            variant = rel[:-3] + ".en.md"
            if os.path.exists(os.path.join(target, variant)):
                plan["retranslate"].append(variant)
            else:
                plan["translate"].append(rel)

    for rel in _walk(target, include):
        rel = os.path.normpath(rel)
        if rel in src or _match(rel, owned) or _match(rel, exclude):
            continue
        if rel.endswith(".en.md"):
            if rel[:-6] + ".md" not in src and not _match(rel[:-6] + ".md", owned):
                plan["orphan"].append(rel)
            continue
        plan["delete"].append(rel)

    for rel in owned:
        if "*" in rel:
            continue
        a, b = os.path.join(repo, rel), os.path.join(target, rel)
        if os.path.isfile(a) and os.path.isfile(b):
            # gemelli con contenuto proprio: segnala solo se qui è più recente
            if os.path.getmtime(a) > os.path.getmtime(b):
                plan["owned_changed"].append(rel)
    return plan, rendered


def run_export(cfg, apply=False, target=None):
    repo = cfg.root
    epath = os.path.join(repo, "config/export.yaml")
    if not os.path.isfile(epath):
        print("✗ config/export.yaml assente: copia config/export.example.yaml e compilalo")
        return 2
    ecfg = load_yaml(epath) or {}
    target = target or ecfg.get("target") or ""
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(repo, target))
    if not os.path.isdir(os.path.join(target, ".git")):
        print("✗ target %s non è un clone git del template" % target)
        return 2

    plan, rendered = plan_export(repo, ecfg, target)
    print("## Export template → %s %s" % (target, "(APPLY)" if apply else "(dry-run)"))
    for key, label in (("add", "nuovi"), ("update", "aggiornati"), ("delete", "da cancellare"),
                       ("orphan", "varianti .en.md orfane")):
        print("\n%s: %d" % (label, len(plan[key])))
        for rel in plan[key]:
            print("  %s" % rel)
    if plan["errors"]:
        print("\n✗ marker @instance malformati:")
        for rel, err in plan["errors"].items():
            print("  %s: %s" % (rel, err))
        return 1

    terms = _deny_terms(repo, ecfg)
    if apply:
        for rel in plan["add"] + plan["update"]:
            dst = os.path.join(target, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as f:
                f.write(rendered[rel])
            shutil.copymode(os.path.join(repo, rel), dst)
        for rel in plan["delete"] + plan["orphan"]:
            os.remove(os.path.join(target, rel))
        hits = leak_scan(target, terms, ecfg.get("scan_skip") or [])
    else:
        # dry-run: scansiona quello che uscirebbe, non il template su disco
        stage = {rel: data for rel, data in rendered.items() if _is_text(rel)}
        rx = re.compile(r"(?<![\w-])(%s)(?![\w])" % "|".join(re.escape(t) for t in terms), re.I)
        hits = []
        for rel, data in sorted(stage.items()):
            for n, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
                m = rx.search(line)
                if m:
                    hits.append((rel, n, m.group(1)))

    print("\nda tradurre (base nuovo, manca .en.md): %d" % len(plan["translate"]))
    for rel in plan["translate"]:
        print("  %s" % rel)
    print("da ritradurre (base cambiato): %d" % len(plan["retranslate"]))
    for rel in plan["retranslate"]:
        print("  %s" % rel)
    if plan["owned_changed"]:
        print("file template_owned cambiati qui (porting a mano): %s" % ", ".join(plan["owned_changed"]))

    print("\nLeak-scan (%d termini): %s" % (len(terms), "OK" if not hits else "KO — %d hit" % len(hits)))
    for rel, n, term in hits[:80]:
        print("  %s:%d  «%s»" % (rel, n, term))
    if hits:
        print("\n⛔ export bloccato: togli i dati d'istanza (o marca la riga @instance) e rilancia")
        return 1
    if apply:
        print("\nScritto nel working tree di %s. Prossimi passi nel template: traduzioni, "
              "link-lint --strict, convention-check --strict, i18n-parity --strict, CHANGELOG, "
              "poi PREPARE → APPROVE → EXECUTE per il push." % target)
    return 0
