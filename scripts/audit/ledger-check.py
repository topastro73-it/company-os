#!/usr/bin/env python3
"""ledger-check.py — guardrail meccanico del ledger Org-OS (ADR-004/ADR-006).

Controlla il ledger dei goal (`ops/` della zona direzione) secondo
os/protocols/collaboration.md e os/protocols/autonomy.md:
  - contenuto: nessun importo con valuta (anche abbreviato o in lettere: `48 mila euro`,
    `48k EUR`, `1,2 milioni di euro`), IBAN, P.IVA o codice fiscale, su OGNI file sotto ops/
    qualunque nome o estensione (README/INDEX inclusi);
  - formato: `type` coerente col nome del file, campi obbligatori, stati ammessi,
    `reason`/`exit` per rejected/blocked, file fuori struttura (anche non `.md`: `.csv`,
    `.txt`, `.MD`); README.md/INDEX.md esenti solo da formato e frontmatter;
  - contratto dei WO: destinatario esistente, servizio offerto da quel ruolo, criteri esistenti
    nel CRITERIA del goal, zona esistente, input come riferimenti, `cos` non emette WO;
  - instradamento 🔴: output 🔴 solo verso zone ristrette e destinatari con accesso;
  - firme umane: owner/decided-by/accepted-by nella forma `human:<slug>`; GOAL `closed` solo
    con ACCEPT.md firmato `accepted-by: human:<slug>`;
  - budget anti-loop: ≤ 15 WO per goal, ≤ 3 ondate dopo l'ultimo CHECKPOINT, niente rimbalzi
    al mittente senza `routed-by: coo`;
  - plan-blind: VERIFY senza WO/PLAN, CRITERIA senza WO/ondate, PLAN con `criteria-commit`;
  - charter: `domain` di os/org/roles/*.md uguale a config/acl.yaml → roles.

Uso:  python3 scripts/audit/ledger-check.py [PATH] [--drive] [--staged]
                                            [--config-dir D] [--org-dir D]
        PATH          cartella ops/ (default: company/direzione/ops/, lo snapshot)
        --drive       ledger sul mount Drive: $OS_DRIVE_MOUNT/<drive_path direzione>/ops
                      (OS_DRIVE_MOUNT dall'ambiente o da .env)
        --staged      versione in stage di company/direzione/ops/ e delle regole (pre-commit)
Exit: 0 pulito (o ledger assente), 1 errori, 2 uso/config non validi.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ROOT dalla posizione dello script (scripts/audit/): affidabile anche dentro gli hook git,
# dove GIT_DIR/GIT_INDEX_FILE sono impostati e `rev-parse` può puntare altrove.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "osctl"))

from lib import config as _cfg  # noqa: E402
from lib.config import load_yaml, ConfigError  # noqa: E402

LEDGER_ZONE = "direzione"
DEFAULT_LEDGER = os.path.join("company", "direzione", "ops")
TYPES = {"goal", "context", "criteria", "plan", "verify", "checkpoint", "wave", "accept",
         "wo", "scorecard", "standup"}
STATUSES = ["proposed", "accepted", "in-progress", "delivered", "verified", "closed",
            "rejected", "blocked"]
VALID_TIERS = {"restricted", "internal", "public", "🔴", "🟡", "🟢", "red"}
RED_TIERS = {"red", "restricted", "🔴"}
WO_REQUIRED = ["id", "goal", "from", "to", "service", "intent", "inputs", "output-zone",
               "output-tier", "criteria", "due", "status", "wave"]
MAX_WO_PER_GOAL = 15
MAX_WAVES_PER_CHECKPOINT = 3
NON_EMITTERS = {"cos"}
# README/INDEX: esenti solo dal controllo di formato/frontmatter, MAI dal controllo contenuto.
SKIP_NAMES = {"README.md", "INDEX.md"}
# Metadati del sistema operativo/Drive: né contenuto né formato.
OS_JUNK = {".DS_Store", "Icon\r", "desktop.ini", "Thumbs.db"}

GOAL_STATUSES = ["active", "on-hold", "closed"]

# --- Lista dei numeri ammessi (ADR-004) ---------------------------------------------------
# Il ledger non contiene importi: invece di inseguire ogni grafia di un importo (lista nera),
# si ammettono solo i numeri con una forma nota. Ogni numero di 3+ cifre (o con separatori)
# che non ricade in una di queste forme blocca: va spostato nella zona finance.
NUM_TOKEN = re.compile(r"\d+(?:[.,']\d+)*")
ALLOWED_NUMBER_SHAPES = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                    # data ISO
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"),                # data gg/mm/aaaa
    re.compile(r"\b\d{4}-W\d{1,2}\b"),                       # settimana ISO
    # anno 2020–2039 solo con un contesto temporale davanti ("nel 2026", "Q4 2026", "ottobre
    # 2026"): un "2035" nudo può essere un importo
    re.compile(r"\b(?:Q[1-4]|H[12]|FY|anno|nel|del|dal|al|entro(?:\s+il)?|fine|inizio|metà|"
               r"gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|"
               r"novembre|dicembre|january|february|march|april|may|june|july|august|september|"
               r"october|november|december|jan|feb|apr|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s+"
               r"20[2-3][0-9](?![0-9]|[.,][0-9])", re.IGNORECASE),
    re.compile(r"\b20[2-3][0-9]\s?[-–/]\s?20[2-3][0-9]\b"),   # periodo: 2021-2027
    re.compile(r"\b(?:ISO|IEC|UNI|EN|NIST|SOC)(?:/IEC)?\s?\d{3,5}(?::\d{4})?\b"),  # standard
    re.compile(r"\b[A-Za-z]+-\d{1,4}(?![0-9]|[.,][0-9])"),           # id: G-NNN, WO-NNN, ADR-NNN, P-NNN
    re.compile(r"\b\d+(?:[.,]\d+)?\s?%"),                    # percentuale
    re.compile(r"\bv?\d{1,2}\.\d{1,2}\.\d{1,2}\b"),          # versione semver
    re.compile(r"(?<![0-9A-Za-z])(?=[0-9a-f]*[a-f])[0-9a-f]{6,40}(?![0-9A-Za-z])"),  # hash git
    re.compile(r"\btokens?:\s*\d+\b", re.IGNORECASE),        # tokens: <n>
    re.compile(r"\b\d+\s?tok\b(?!\s*[€$£])"),                            # <n> tok (tabelle WAVE)
]


# Indicatori di valuta (simbolo o nome dell'unità, non la parola "valuta"): una riga che ne
# contiene uno insieme a una cifra non ammessa è un importo, anche con valori a 1–2 cifre
# ("€k 90", "(k€): 43", "48 migliaia di euro").
CURRENCY_ANY = re.compile(r"€|&euro;|£|\b[kKmM]?\s?(?-i:EUR)[A-Za-z]*\b|\b[kKmM]?\s?eur\b|"
                          r"\b[kKmM]?\s?euros?\b|\bUSD\b|\bGBP\b|\bCHF\b|\bmigliaia\b|\b(?-i:Mio)\b",
                          re.IGNORECASE)
NON_AMOUNT_NUMBERS = [
    re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:mes[ei]|giorn[oi]|settiman[ae]|ann[oi]|or[ae]|giornate)\b",
               re.IGNORECASE),                              # durate
    re.compile(r"\b[A-Z]{1,2}\d{1,3}\b"),                  # codici brevi: M12, C10, W41, Q4
]


def currency_line_digits(line, in_scope=False):
    """Cifre fuori dalle forme ammesse su una riga che contiene un indicatore di valuta, o che
    sta sotto un titolo, un'intestazione di tabella o una riga introduttiva con l'unità (€k)."""
    if not in_scope and not CURRENCY_ANY.search(line):
        return []
    spans = []
    for rx in ALLOWED_NUMBER_SHAPES + NON_AMOUNT_NUMBERS:
        spans += [m.span() for m in rx.finditer(line)]
    out = []
    for m in re.finditer(r"\d+(?:[.,]\d+)*", line):
        if not any(a <= m.start() and m.end() <= b for a, b in spans):
            out.append(m.group())
    return out


def disallowed_numbers(line):
    """Numeri di 3+ cifre (o con separatori) che non ricadono in nessuna forma ammessa."""
    covered = []
    for rx in ALLOWED_NUMBER_SHAPES:
        covered += [m.span() for m in rx.finditer(line)]
    bad = []
    for m in NUM_TOKEN.finditer(line):
        tok = m.group()
        digits = re.sub(r"\D", "", tok)
        if len(digits) < 3 and tok == digits:
            continue                                         # 0–99: conteggi, mesi, liste
        if re.fullmatch(r"\d{1,2}[.,]\d{1,2}", tok):
            continue                                         # 0,5 mesi · 1.2 (valori piccoli)
        if any(a <= m.start() and m.end() <= b for a, b in covered):
            continue
        bad.append(tok)
    return bad

CURRENCY = r"(?:€|\$|k€|K€|EUR|euro|mln)"
NUM = r"[0-9][0-9.,']*"


def normalize_amounts(line):
    """Forma canonica per la ricerca di importi: niente parentesi, uno spazio tra cifre e
    lettere/simboli di valuta. Così `12.000EUR`, `EUR12.000`, `48500euro` e `48.500 (euro)`
    diventano `12.000 EUR`, `EUR 12.000`, … e cadono sotto le stesse regole: non si rincorre
    ogni grafia con una regex nuova."""
    s = re.sub(r"[()\[\]{}]", " ", line)
    s = re.sub(r"(?<=[0-9])(?=[€$£A-Za-z])|(?<=[€$£A-Za-z])(?=[0-9])", " ", s)
    return re.sub(r"\s+", " ", s)


CONTENT_RULES = [
    ("importo con valuta", re.compile(
        r"(?:€|\$|£|\bEUR\b|\beuros?\b|\bUSD\b|\bGBP\b|\bCHF\b)\s?" + NUM + r"|\b" + NUM
        + r"\s?(?:€|\$|£|k€|K€|\bEUR\b|\beuros?\b|\bUSD\b|\bGBP\b|\bCHF\b|\bmln\b|\bk€)",
        re.IGNORECASE)),
    # importi abbreviati o in lettere: "48 mila euro", "48k EUR", "1,2 milioni di euro", "3M€"
    # (l'ordine valuta → numero → moltiplicatore è già coperto dalla regola sopra)
    ("importo con valuta (abbreviato o in lettere)", re.compile(
        r"\b" + NUM + r"\s*(?:mila|milion[ei]|mln|mld|miliard[oi]|k|m)\s*(?:di\s+)?(?:€|\bEUR\b|\beuro\b)",
        re.IGNORECASE)),
    # importi tutti in lettere ("quarantottomila euro") e moltiplicatori attaccati ("48k")
    ("importo in lettere", re.compile(
        r"\w*(?:mila|milion[ei]|miliard[oi])\b\s*(?:di\s+)?(?:€|\bEUR\b|\beuros?\b)", re.IGNORECASE)),
    ("importo abbreviato", re.compile(r"\b\d+(?:[.,]\d+)?(?:k|K|mln|mld)\b")),
    # unità con moltiplicatore: "48 kEUR", "1,2 MEUR", "48 Keuro", "1,2 Mio"
    ("importo in kEUR/MEUR", re.compile(
        r"\b\d+(?:[.,]\d+)?\s*(?:[kKmM]\s?(?:EUR|[Ee]uro?s?)[A-Za-z]*|Mio)\b")),
    # un moltiplicatore dopo un numero è già un importo, con o senza valuta: "48 mila",
    # "1,5 milioni", "1,2M", "85 K"
    ("importo con moltiplicatore", re.compile(
        r"\b\d+(?:[.,]\d+)?\s*(?:mila|milion[ei]|miliard[oi]|mln|mld|[kKmM])\b")),
    # numeri in lettere con moltiplicatore: "quarantottomila", "un milione", "due milioni"
    ("importo in lettere", re.compile(
        r"\b(?:\w*(?:uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|undici|dodici|venti|"
        r"trenta|quaranta|cinquanta|sessanta|settanta|ottanta|novanta|cento|mille)mila|"
        r"(?:un|uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|mezzo)\s+milion[ei]|"
        r"\w+milion[ei]|\w+miliard[oi])\b", re.IGNORECASE)),
]
# Regole sugli identificativi: si applicano al testo originale (la normalizzazione li spezzerebbe).
ID_RULES = [
    ("IBAN", re.compile(r"IT[0-9]{2}[A-Z][0-9]{10,26}")),
    ("P.IVA (11 cifre)", re.compile(r"(?<![0-9A-Za-z-])[0-9]{11}(?![0-9A-Za-z])")),
    ("codice fiscale", re.compile(r"\b[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]\b")),
]
FM_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)
ID_REF_RE = re.compile(r"^[A-Z]+-[0-9]+[A-Za-z0-9-]*$")


def parse_yaml_text(text):
    if _cfg._pyyaml is not None:
        return _cfg._pyyaml.safe_load(text) or {}
    return _cfg._parse_yaml_min(text) or {}


def sval(v):
    return "" if v is None else str(v).strip()


def as_list(v):
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return v
    return [v]


class Ledger:
    def __init__(self, ops_dir, config_dir, org_dir, label=None):
        self.ops = ops_dir
        self.label = label or ops_dir
        self.config_dir = config_dir
        self.org_dir = org_dir
        self.errors = []
        self.warnings = []
        acl = load_yaml(os.path.join(config_dir, "acl.yaml"))
        people_doc = load_yaml(os.path.join(config_dir, "people.yaml"))
        self.zones = acl.get("zones") or {}
        self.roles = acl.get("roles") or {}
        self.people = people_doc.get("people") or {}
        self.admins = people_doc.get("admin") or []
        svc_path = os.path.join(org_dir, "services.yaml")
        self.services = (load_yaml(svc_path).get("services") or {}) if os.path.isfile(svc_path) else {}
        self.files = {}   # path → (fm, text, fm_lines, has_fm): .md del formato
        self.raw = {}     # path → text: README/INDEX e file fuori formato (solo contenuto)

    # -- output -------------------------------------------------------------

    def rel(self, path):
        return os.path.join(self.label, os.path.relpath(path, self.ops))

    def err(self, path, line, msg):
        self.errors.append("%s:%s: %s" % (path, line, msg))

    def warn(self, path, msg):
        self.warnings.append("%s: %s" % (path, msg))

    # -- zone e accessi ----------------------------------------------------

    def zone_node(self, name):
        name = sval(name)
        if not name:
            return None, None
        zone, _, sub = name.partition(".")
        z = self.zones.get(zone)
        if z is None:
            return None, None
        if not sub:
            return z, z
        node = (z.get("subfolders") or {}).get(sub)
        return node, z

    def zone_is_red(self, name):
        node, parent = self.zone_node(name)
        if node is None:
            return False
        for n in (node, parent):
            if sval(n.get("tier")).lower() in RED_TIERS or sval(n.get("snapshot_target")) == "vault":
                return True
        return False

    def expand(self, names):
        out = set()
        for n in names or []:
            n = sval(n)
            if n == "admin":
                out.update(self.admins)
            elif n == "all_internal":
                out.update(k for k, p in self.people.items() if (p or {}).get("type") == "internal")
            elif n == "everyone":
                out.update(self.people.keys())
            else:
                out.add(n.split(".", 1)[0])
        return out

    def human_has_access(self, person, zone_name):
        node, _ = self.zone_node(zone_name)
        if node is None:
            return False
        allowed = self.expand(node.get("write")) | self.expand(node.get("read"))
        return person in allowed

    def role_has_write(self, role, zone_name):
        r = self.roles.get(role) or {}
        zn = sval(zone_name)
        return any(zn == sval(z) or zn.startswith(sval(z) + ".") for z in (r.get("write") or []))

    def catalog_entry(self, role, service):
        """Voce del catalogo servizi per (ruolo, servizio), o None."""
        service = sval(service)
        for sid, s in self.services.items():
            if sval((s or {}).get("role")) == role and service in (sid, sid.split("/", 1)[-1]):
                return s or {}
        return None

    def role_exists(self, role):
        if os.path.isfile(os.path.join(self.org_dir, "roles", role + ".md")):
            return True
        return os.path.isfile(os.path.join(ROOT, "os", "agents", role, "AGENT.md"))

    def role_offers(self, role, service):
        service = sval(service)
        for sid, s in self.services.items():
            if sval((s or {}).get("role")) != role:
                continue
            if service == sid or service == sid.split("/", 1)[-1]:
                return True
        return False

    # -- lettura -----------------------------------------------------------

    def load(self):
        # Ogni file sotto ops/ viene letto, qualunque nome/estensione e anche nelle cartelle
        # nascoste: il controllo cifre/🔴 guarda il contenuto, non il nome del file.
        for root, dirs, files in os.walk(self.ops):
            dirs[:] = sorted(dirs)
            for fn in sorted(files):
                if fn in OS_JUNK:
                    continue
                p = os.path.join(root, fn)
                with open(p, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                if fn in SKIP_NAMES:
                    self.raw[p] = text
                    continue
                if not fn.endswith(".md"):
                    self.raw[p] = text
                    self.err(self.rel(p), 1, "file fuori dal formato del ledger: solo .md "
                             "riconosciuti (vedi os/protocols/collaboration.md)")
                    continue
                m = FM_RE.match(text)
                fm, fm_lines = {}, {}
                if m:
                    try:
                        fm = parse_yaml_text(m.group(1))
                        if not isinstance(fm, dict):
                            fm = {}
                    except Exception as e:  # frontmatter rotto
                        self.err(self.rel(p), 1, "frontmatter non parsabile (%s)" % e)
                    for i, line in enumerate(m.group(1).splitlines(), start=2):
                        k = line.split(":", 1)[0].strip()
                        if k and not line.startswith(" ") and k not in fm_lines:
                            fm_lines[k] = i
                else:
                    self.err(self.rel(p), 1, "manca il frontmatter YAML")
                self.files[p] = (fm, text, fm_lines, m is not None)

    def line_of(self, path, key):
        return self.files[path][2].get(key, 1)

    # -- controlli ---------------------------------------------------------

    def expected_type(self, path):
        rel = os.path.relpath(path, self.ops).replace(os.sep, "/")
        name = os.path.basename(rel)
        parts = rel.split("/")
        if rel == "scorecard.md":
            return "scorecard"
        if len(parts) == 2 and parts[0] == "standup" and re.match(r"^\d{4}-\d{2}-\d{2}\.md$", name):
            return "standup"
        if len(parts) == 2 and parts[0] == "wo" and re.match(r"^WO-\d{3,}\.md$", name):
            return "wo"
        if len(parts) == 3 and parts[0] == "goals" and re.match(r"^G-\d{3,}(-[a-z0-9-]+)?$", parts[1]):
            fixed = {"GOAL.md": "goal", "CONTEXT.md": "context", "CRITERIA.md": "criteria",
                     "PLAN.md": "plan", "VERIFY.md": "verify", "ACCEPT.md": "accept"}
            if name in fixed:
                return fixed[name]
            if re.match(r"^CHECKPOINT-\d{2}\.md$", name):
                return "checkpoint"
            if re.match(r"^WAVE-\d{2}\.md$", name):
                return "wave"
        return None

    def check_content(self, path, text):
        # Portata dell'unità: un indicatore di valuta in un titolo vale fino al titolo
        # successivo; nell'intestazione di una tabella, per tutta la tabella; in una riga che
        # termina con ":" ("Valori in €k:"), fino alla prima riga vuota.
        heading_scope = table_scope = lead_scope = in_table = False
        for i, line in enumerate(text.splitlines(), start=1):
            s = line.strip()
            has_cur = bool(CURRENCY_ANY.search(line))
            if s.startswith("#"):
                heading_scope, table_scope, lead_scope, in_table = has_cur, False, False, False
            elif s.startswith("|"):
                if not in_table:
                    in_table, table_scope = True, has_cur
            else:
                in_table = table_scope = False
                if not s:
                    lead_scope = False
                elif has_cur and s.endswith(":"):
                    lead_scope = True
            in_scope = heading_scope or table_scope or lead_scope
            norm = normalize_amounts(line)
            hits = [label for label, rx in CONTENT_RULES if rx.search(line) or rx.search(norm)]
            hits += [label for label, rx in ID_RULES if rx.search(line) or rx.search(line.upper())]
            for label in hits:
                self.err(self.rel(path), i, "🔴 %s nel ledger (ADR-004: solo riferimenti)" % label)
            if not hits:
                cur = currency_line_digits(line, in_scope)
                if cur:
                    self.err(self.rel(path), i,
                             "🔴 importo con valuta nel ledger %s (ADR-004: riga con indicatore di "
                             "valuta e cifre; gli importi stanno solo in finance)"
                             % ", ".join(repr(c) for c in cur[:3]))
                    continue
                bad = disallowed_numbers(line)
                if bad:
                    self.err(self.rel(path), i,
                             "🔴 numero non ammesso nel ledger %s (ADR-004: ammessi solo date, id, %%, "
                             "mesi, versioni, hash, `tokens:`/`tok`; importi e codici solo in finance)"
                             % ", ".join(repr(b) for b in bad[:3]))

    def check_human(self, path, fm, key, required=True):
        v = sval(fm.get(key))
        if not v:
            if required:
                self.err(self.rel(path), self.line_of(path, key), "manca `%s` (firma umana)" % key)
            return
        if not v.startswith("human:"):
            self.err(self.rel(path), self.line_of(path, key),
                     "`%s: %s` non è una firma umana (`human:<slug>`): l'AI non firma" % (key, v))
            return
        slug = v.split(":", 1)[1]
        if slug not in self.people:
            self.err(self.rel(path), self.line_of(path, key), "`%s`: persona %r non in people.yaml" % (key, slug))

    def check_common(self, path, fm):
        r = self.rel(path)
        exp = self.expected_type(path)
        if exp is None:
            self.err(r, 1, "file fuori dal formato del ledger (vedi os/protocols/collaboration.md)")
        if sval(fm.get("zone")) != LEDGER_ZONE:
            self.err(r, self.line_of(path, "zone"), "`zone:` deve essere %s" % LEDGER_ZONE)
        tier = sval(fm.get("tier"))
        if not tier or tier.lower() not in VALID_TIERS:
            self.err(r, self.line_of(path, "tier"), "`tier:` mancante o non valido")
        t = sval(fm.get("type"))
        if t not in TYPES:
            self.err(r, self.line_of(path, "type"), "`type:` mancante o non valido (%r)" % t)
        elif exp and t != exp:
            self.err(r, self.line_of(path, "type"), "`type: %s` non coerente col file (atteso %s)" % (t, exp))
        return exp

    def goal_dir(self, goal_id):
        goal_id = sval(goal_id)
        if not goal_id:
            return None
        for d in sorted(glob.glob(os.path.join(self.ops, "goals", goal_id + "*"))):
            base = os.path.basename(d)
            if base == goal_id or base.startswith(goal_id + "-"):
                return d
        return None

    def criteria_ids(self, goal_id):
        d = self.goal_dir(goal_id)
        if not d:
            return None
        p = os.path.join(d, "CRITERIA.md")
        if not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8", errors="replace") as fh:
            return set(re.findall(r"^###\s+(C[0-9]+)\b", fh.read(), re.MULTILINE))

    def check_wo(self, path, fm):
        r = self.rel(path)
        L = lambda k: self.line_of(path, k)  # noqa: E731
        for k in WO_REQUIRED:
            if k not in fm or fm.get(k) in (None, "", []):
                self.err(r, L(k), "WO: manca il campo obbligatorio `%s`" % k)
        stem = os.path.basename(path)[:-3]
        if sval(fm.get("id")) and sval(fm.get("id")) != stem:
            self.err(r, L("id"), "`id: %s` diverso dal nome del file" % sval(fm.get("id")))
        status = sval(fm.get("status"))
        if status and status not in STATUSES:
            self.err(r, L("status"), "stato %r fuori dagli ammessi (%s)" % (status, ", ".join(STATUSES)))
        if status in ("rejected", "blocked"):
            for k in ("reason", "exit"):
                if not sval(fm.get(k)):
                    self.err(r, L(k) if k in fm else L("status"), "stato %s senza `%s`" % (status, k))
        if status == "closed":
            self.check_human(path, fm, "accepted-by")
            if not sval(fm.get("accepted-at")):
                self.err(r, L("status"), "stato closed senza `accepted-at`")
        elif sval(fm.get("accepted-by")):
            self.check_human(path, fm, "accepted-by")

        frm, to = sval(fm.get("from")), sval(fm.get("to"))
        if frm in NON_EMITTERS:
            self.err(r, L("from"), "`from: %s`: questo ruolo non emette work order" % frm)
        elif frm and not frm.startswith("human:") and not self.role_exists(frm):
            self.err(r, L("from"), "`from: %s`: ruolo inesistente" % frm)
        human = None
        if to.startswith("human:"):
            human = to.split(":", 1)[1]
            if human not in self.people:
                self.err(r, L("to"), "`to: %s`: persona non presente in people.yaml" % to)
                human = None
            elif (self.people.get(human) or {}).get("onboarded") is not True and human not in self.admins:
                self.warn(r, "`to: %s`: persona non ancora onboardata" % to)
        elif to:
            if not self.role_exists(to):
                self.err(r, L("to"), "`to: %s`: ruolo senza charter né AGENT.md" % to)
            elif sval(fm.get("service")) and not self.role_offers(to, fm.get("service")):
                self.err(r, L("service"), "servizio %r non offerto da %r (os/org/services.yaml)"
                         % (sval(fm.get("service")), to))

        crit = as_list(fm.get("criteria"))
        known = self.criteria_ids(fm.get("goal"))
        if sval(fm.get("goal")) and self.goal_dir(fm.get("goal")) is None:
            self.err(r, L("goal"), "goal %r inesistente nel ledger" % sval(fm.get("goal")))
        elif crit and known is None:
            self.err(r, L("criteria"), "il goal %r non ha CRITERIA.md: criteri non risolvibili" % sval(fm.get("goal")))
        elif known is not None:
            for c in crit:
                if sval(c) not in known:
                    self.err(r, L("criteria"), "criterio %r inesistente nel CRITERIA del goal" % sval(c))

        oz = sval(fm.get("output-zone"))
        if oz and self.zone_node(oz)[0] is None:
            self.err(r, L("output-zone"), "zona %r inesistente in config/acl.yaml" % oz)

        inputs = fm.get("inputs")
        if inputs is not None and not isinstance(inputs, list):
            self.err(r, L("inputs"), "`inputs` deve essere una lista di riferimenti")
        for item in as_list(inputs):
            s = sval(item)
            ok = (s and len(s) <= 160 and "\n" not in s and len(s.split()) <= 3
                  and ("/" in s or ID_REF_RE.match(s) or s.endswith((".md", ".yaml"))))
            if not ok:
                self.err(r, L("inputs"), "input non è un riferimento (path o id): %r" % s[:60])

        # instradamento 🔴 — un output-tier fuori enum disattiverebbe in silenzio il controllo
        out_tier = sval(fm.get("output-tier")).lower()
        if out_tier and out_tier not in VALID_TIERS:
            self.err(r, L("output-tier"), "output-tier %r fuori dagli ammessi (%s)"
                     % (out_tier, ", ".join(sorted(VALID_TIERS))))
        red = out_tier in RED_TIERS or sval(fm.get("tier")).lower() in RED_TIERS
        # il catalogo prevale sull'etichetta del WO: un servizio 🔴 resta 🔴 anche se il WO
        # dichiara 🟡, e consegna solo nella zona del catalogo (o in una sua sottozona)
        role_to = to if to and not to.startswith("human:") else None
        cat = self.catalog_entry(role_to, fm.get("service")) if role_to else None
        if cat is None and not role_to and sval(fm.get("service")):
            # destinatario umano: il servizio citato porta comunque il suo tier di catalogo
            svc = sval(fm.get("service"))
            hits = [s or {} for sid, s in self.services.items() if svc in (sid, sid.split("/", 1)[-1])]
            cat = hits[0] if len(hits) == 1 else None
        if cat:
            if sval(cat.get("output-tier")).lower() in RED_TIERS:
                red = True
            cz = sval(cat.get("output-zone"))
            if oz and cz and not (oz == cz or oz.startswith(cz + ".")):
                self.err(r, L("output-zone"), "output-zone %r diversa da quella del catalogo %r per %s/%s"
                         % (oz, cz, role_to, sval(fm.get("service")).split("/")[-1]))
        if role_to and oz and self.zone_node(oz)[0] is not None and self.roles \
                and not self.role_has_write(role_to, oz):
            self.err(r, L("to"), "il ruolo %r non ha scrittura sulla zona %r (config/acl.yaml roles)"
                     % (role_to, oz))
        # una zona ristretta è 🔴 qualunque sia l'etichetta; e una persona riceve un output solo
        # se ha accesso alla zona, per ogni tier
        if oz and self.zone_node(oz)[0] is not None:
            if self.zone_is_red(oz):
                red = True
            if human is not None and not red and not self.human_has_access(human, oz):
                self.err(r, L("to"), "output verso %s, che non ha ACL sulla zona %r" % (to, oz))
        if red and oz and self.zone_node(oz)[0] is not None:
            if not self.zone_is_red(oz):
                self.err(r, L("output-zone"), "🔴 output 🔴 verso la zona %r che non è ristretta" % oz)
            if human is not None:
                if not self.human_has_access(human, oz):
                    self.err(r, L("to"), "🔴 output 🔴 verso %s, che non ha ACL sulla zona %r" % (to, oz))
            elif to and not to.startswith("human:") and not self.role_has_write(to, oz):
                self.err(r, L("to"), "🔴 output 🔴: il ruolo %r non ha accesso alla zona %r (roles)" % (to, oz))

    def check_typed(self, path, fm, text, exp):
        r = self.rel(path)
        body = text[FM_RE.match(text).end():] if FM_RE.match(text) else text
        if exp == "goal":
            for k in ("id", "due", "status"):
                if not sval(fm.get(k)):
                    self.err(r, self.line_of(path, k), "GOAL: manca `%s`" % k)
            self.check_human(path, fm, "owner")
            gstatus = sval(fm.get("status"))
            if gstatus and gstatus not in GOAL_STATUSES:
                self.err(r, self.line_of(path, "status"), "GOAL: stato %r fuori dagli ammessi (%s)"
                         % (gstatus, ", ".join(GOAL_STATUSES)))
            if gstatus == "closed":
                self.check_goal_accept(path)
        elif exp == "plan":
            if not sval(fm.get("criteria-commit")):
                self.err(r, 1, "PLAN senza `criteria-commit` (plan-blind: criteri prima del piano)")
        elif exp == "criteria":
            for i, line in enumerate(text.splitlines(), start=1):
                if re.search(r"\bWO-[0-9]|\bwave\b|\bondat[ae]\b", line, re.IGNORECASE):
                    self.err(r, i, "CRITERIA cita WO o ondate (plan-blind)")
            if not re.search(r"^###\s+C[0-9]+", body, re.MULTILINE):
                self.err(r, 1, "CRITERIA senza criteri `### C<n>`")
        elif exp == "verify":
            for i, line in enumerate(text.splitlines(), start=1):
                if re.search(r"\bWO-[0-9]|\bPLAN\b", line):
                    self.err(r, i, "VERIFY cita WO o PLAN (plan-blind: prove solo da fonti osservabili)")
        elif exp == "checkpoint":
            self.check_human(path, fm, "decided-by")
            for k in ("decided-at", "decision"):
                if not sval(fm.get(k)):
                    self.err(r, self.line_of(path, k), "CHECKPOINT: manca `%s`" % k)
        elif exp == "accept":
            self.check_human(path, fm, "accepted-by")
            if not sval(fm.get("accepted-at")):
                self.err(r, self.line_of(path, "accepted-at"), "ACCEPT: manca `accepted-at`")

    def check_goal_accept(self, path):
        """GOAL `closed` solo con ACCEPT.md firmato da un umano (l'AI non chiude i goal)."""
        r = self.rel(path)
        L = self.line_of(path, "status")
        acc = os.path.join(os.path.dirname(path), "ACCEPT.md")
        if not os.path.isfile(acc):
            self.err(r, L, "goal `status: closed` senza ACCEPT.md firmato (`accepted-by: human:<slug>`)")
            return
        fm = (self.files.get(acc) or ({},))[0]
        v = sval(fm.get("accepted-by"))
        slug = v.split(":", 1)[1] if v.startswith("human:") else None
        if not slug or slug not in self.people:
            self.err(r, L, "goal `status: closed` ma ACCEPT.md non ha `accepted-by: human:<slug>` "
                     "valido (trovato %r)" % v)

    def check_budget(self, wos):
        by_goal = {}
        for p, fm in wos:
            by_goal.setdefault(sval(fm.get("goal")), []).append((p, fm))
        by_id = {sval(fm.get("id")): fm for _, fm in wos}
        for goal, items in by_goal.items():
            items.sort(key=lambda x: os.path.basename(x[0]))
            if len(items) > MAX_WO_PER_GOAL:
                for p, _ in items[MAX_WO_PER_GOAL:]:
                    self.err(self.rel(p), 1, "budget: goal %s oltre %d WO (stop ed escalation al CEO)"
                             % (goal, MAX_WO_PER_GOAL))
            d = self.goal_dir(goal)
            last_cp = 0
            if d:
                for cp in glob.glob(os.path.join(d, "CHECKPOINT-*.md")):
                    fm = self.files.get(cp, ({},))[0]
                    m = re.search(r"CHECKPOINT-(\d+)", cp)
                    try:
                        w = int(sval(fm.get("wave")) or (m.group(1) if m else 0))
                    except ValueError:
                        w = 0
                    last_cp = max(last_cp, w)
            open_waves = {}
            for p, fm in items:
                try:
                    w = int(sval(fm.get("wave")))
                except ValueError:
                    continue
                if w > last_cp:
                    open_waves.setdefault(w, []).append(p)
            ordered = sorted(open_waves)
            for w in ordered[MAX_WAVES_PER_CHECKPOINT:]:
                for p in sorted(open_waves[w]):
                    self.err(self.rel(p), self.line_of(p, "wave"),
                             "budget: ondata %d è oltre la %da dopo l'ultimo CHECKPOINT umano"
                             % (w, MAX_WAVES_PER_CHECKPOINT))
        for p, fm in wos:
            parent = sval(fm.get("parent"))
            if not parent:
                continue
            pfm = by_id.get(parent)
            if pfm is None:
                self.err(self.rel(p), self.line_of(p, "parent"), "parent %r inesistente" % parent)
                continue
            if sval(fm.get("to")) == sval(pfm.get("from")) and sval(fm.get("routed-by")) != "coo":
                self.err(self.rel(p), self.line_of(p, "to"),
                         "rimbalzo al mittente di %s senza `routed-by: coo`" % parent)

    def check_charters(self):
        for p in sorted(glob.glob(os.path.join(self.org_dir, "roles", "*.md"))):
            if p.endswith(".en.md"):  # varianti di lingua (template): stessa charter, non un ruolo in più
                continue
            with open(p, encoding="utf-8", errors="replace") as fh:
                m = FM_RE.match(fh.read())
            fm = parse_yaml_text(m.group(1)) if m else {}
            role = sval(fm.get("role")) or os.path.basename(p)[:-3]
            exp = self.roles.get(role)
            if exp is None:
                self.err(p, 1, "charter %r senza `roles.%s` in config/acl.yaml" % (role, role))
                continue
            dom = fm.get("domain") or {}
            for k in ("read", "write"):
                a = sorted(sval(x) for x in (dom.get(k) or []))
                b = sorted(sval(x) for x in (exp.get(k) or []))
                if a != b:
                    self.err(p, 1, "domain.%s del charter diverso da config/acl.yaml → roles.%s" % (k, role))
            for sid in as_list(fm.get("services")):
                s = self.services.get(sval(sid))
                if s is None or sval(s.get("role")) != role:
                    self.err(p, 1, "servizio %r non nel catalogo per il ruolo %r" % (sval(sid), role))

    def run(self):
        self.load()
        wos = []
        for p, (fm, text, _, has_fm) in self.files.items():
            self.check_content(p, text)
            if not has_fm:
                continue
            exp = self.check_common(p, fm)
            if exp == "wo":
                self.check_wo(p, fm)
                wos.append((p, fm))
            elif exp:
                self.check_typed(p, fm, text, exp)
        for p, text in self.raw.items():
            self.check_content(p, text)
        self.check_budget(wos)
        self.check_charters()
        return len(self.files) + len(self.raw)


def read_env_mount():
    v = os.environ.get("OS_DRIVE_MOUNT")
    if v:
        return v
    env = os.path.join(ROOT, ".env")
    if os.path.isfile(env):
        for line in open(env, encoding="utf-8"):
            m = re.match(r'^\s*(?:export\s+)?OS_DRIVE_MOUNT\s*=\s*(.*)$', line)
            if m:
                return m.group(1).strip().strip('"\'')
    return None


STAGED_RULES = [("config", os.path.join("config", "acl.yaml")),
                ("config", os.path.join("config", "people.yaml")),
                ("org", os.path.join("os", "org"))]


def _materialize(prefix, dst_root, base):
    """Copia dall'indice git i file tracciati sotto `prefix` in `dst_root`, relativi a `base`."""
    out = subprocess.run(["git", "ls-files", "-z", "--", prefix], cwd=ROOT,
                         capture_output=True, text=True).stdout
    n = 0
    for rel in [x for x in out.split("\0") if x]:
        blob = subprocess.run(["git", "show", ":" + rel], cwd=ROOT, capture_output=True)
        if blob.returncode != 0:
            continue
        target = os.path.join(dst_root, os.path.relpath(rel, base))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(blob.stdout)
        n += 1
    return n


def staged_copy():
    """Ledger E regole (ACL, persone, catalogo, charter) nella versione IN STAGE: è ciò che entra
    nel commit. Validare il ledger in stage contro regole del working tree lascerebbe passare un
    commit incoerente."""
    tmp = tempfile.mkdtemp(prefix="ledger-staged-")
    dst = os.path.join(tmp, "ops")
    n = _materialize(DEFAULT_LEDGER, dst, DEFAULT_LEDGER)
    for kind, rel in STAGED_RULES:
        base = os.path.dirname(rel) if kind == "config" else rel
        _materialize(rel, os.path.join(tmp, kind), base)
    return tmp, dst, n


def main():
    ap = argparse.ArgumentParser(description="Guardrail del ledger Org-OS (ADR-004/006)")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--drive", action="store_true")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--config-dir", default=None)
    ap.add_argument("--org-dir", default=None)
    a = ap.parse_args()

    cleanup = None
    try:
        if a.staged:
            cleanup, ops, _ = staged_copy()
            label = DEFAULT_LEDGER  # versione in stage, regole comprese
            a.config_dir = a.config_dir or os.path.join(cleanup, "config")
            a.org_dir = a.org_dir or os.path.join(cleanup, "org")
        a.config_dir = a.config_dir or os.path.join(ROOT, "config")
        a.org_dir = a.org_dir or os.path.join(ROOT, "os", "org")
        if cleanup:
            pass                                          # ops e label già impostati da --staged
        elif a.drive:
            mount = read_env_mount()
            if not mount:
                print("⚠️  --drive: OS_DRIVE_MOUNT non impostata (ambiente o .env)")
                return 2
            try:
                zones = load_yaml(os.path.join(a.config_dir, "acl.yaml")).get("zones") or {}
            except ConfigError as e:
                print("🔴 config non valida: %s" % e)
                return 2
            dp = sval((zones.get(LEDGER_ZONE) or {}).get("drive_path")) or LEDGER_ZONE
            ops = os.path.join(mount, dp, "ops")
            label = ops
        else:
            ops = a.path or os.path.join(ROOT, DEFAULT_LEDGER)
            label = ops if a.path else DEFAULT_LEDGER

        if not os.path.isdir(ops):
            print("🟡 ledger assente (%s): niente da controllare" % label)
            return 0
        try:
            led = Ledger(ops, a.config_dir, a.org_dir, label=label)
            n = led.run()
        except ConfigError as e:
            print("🔴 config non valida: %s" % e)
            return 2
        for w in led.warnings:
            print("⚠️  %s" % w)
        if led.errors:
            for e in led.errors:
                print("🔴 %s" % e)
            print("\n🔴 ledger-check: %d errori su %d file (%s)" % (len(led.errors), n, label))
            return 1
        print("✅ ledger-check: %d file puliti (%s)" % (n, label))
        return 0
    finally:
        if cleanup:
            shutil.rmtree(cleanup, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
