#!/usr/bin/env python3
"""Selftest di scripts/audit/ledger-check.py (unittest, solo stdlib).

Lo script si invoca SEMPRE via subprocess e non si importa mai: se manca, i test falliscono
a runtime e non al caricamento del modulo. Ogni test copia la fixture ermetica
`scripts/audit/fixtures/ledger/` in una tempdir e genera a runtime la variante da provare
(nessun importo, IBAN o P.IVA vive nei file committati).

Uso:  python3 -m unittest scripts/audit/tests/test_ledger_check.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
SCRIPT = os.path.join(AUDIT, "ledger-check.py")
FIXTURE = os.path.join(AUDIT, "fixtures", "ledger")
GOAL_DIR = os.path.join("ops", "goals", "G-900-esempio")

# Valori sensibili costruiti a runtime: mai letterali nei file committati.
FAKE_IBAN = "IT" + "00" + "X" + "1" * 12
FAKE_PIVA = "9" * 11
FAKE_AMOUNT_EURO = "€ " + "48" + ".500"
FAKE_AMOUNT_EUR = "12" + ".000 EUR"


class LedgerCheckTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ledger-check-test-")
        self.base = os.path.join(self.tmp, "ledger")
        shutil.copytree(FIXTURE, self.base)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- helper -------------------------------------------------------------

    def reset(self):
        """Ledger di fixture di nuovo pulito (per i subTest)."""
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.copytree(FIXTURE, self.base)

    def path(self, rel):
        return os.path.join(self.base, rel)

    def read(self, rel):
        with open(self.path(rel), encoding="utf-8") as fh:
            return fh.read()

    def write(self, rel, text):
        p = self.path(rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)

    def append(self, rel, text):
        self.write(rel, self.read(rel) + text)

    def set_field(self, rel, key, value):
        """Sostituisce (o aggiunge) `key: value` nel frontmatter."""
        text = self.read(rel)
        head, sep, body = text[4:].partition("\n---")
        lines = head.splitlines()
        out, done = [], False
        for line in lines:
            if re.match(r"^%s:" % re.escape(key), line):
                done = True
                if value is not None:
                    out.append("%s: %s" % (key, value))
            else:
                out.append(line)
        if not done and value is not None:
            out.append("%s: %s" % (key, value))
        self.write(rel, "---\n" + "\n".join(out) + sep + body)

    def run_check(self, ops="ops"):
        cmd = [sys.executable, SCRIPT, self.path(ops),
               "--config-dir", self.path("config"),
               "--org-dir", self.path("org")]
        return subprocess.run(cmd, capture_output=True, text=True)

    def assertFails(self, culprit):
        r = self.run_check()
        out = r.stdout + r.stderr
        self.assertNotEqual(r.returncode, 0, "atteso exit != 0, output:\n" + out)
        self.assertIn(culprit, out, "il file colpevole non è nominato:\n" + out)
        return out

    # -- fixture pulita ----------------------------------------------------

    def test_clean_fixture_passes(self):
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_ledger_is_ok(self):
        shutil.rmtree(self.path("ops"))
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ledger assente", r.stdout + r.stderr)

    # -- C1 (a): cifre e dati 🔴 nel contenuto --------------------------------

    def test_amount_in_goal_body(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"), "\nFabbisogno: %s\n" % FAKE_AMOUNT_EURO)
        self.assertFails("GOAL.md")

    def test_amount_in_wo_body(self):
        self.append("ops/wo/WO-901.md", "\nValore atteso %s\n" % FAKE_AMOUNT_EUR)
        self.assertFails("WO-901.md")

    def test_iban_in_wo(self):
        self.append("ops/wo/WO-902.md", "\nConto %s\n" % FAKE_IBAN)
        self.assertFails("WO-902.md")

    def test_piva_in_goal(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"), "\nFornitore %s\n" % FAKE_PIVA)
        self.assertFails("GOAL.md")

    # -- C1 (a'): ogni file di ops/ è letto, qualunque nome/estensione --------

    def test_amount_in_readme(self):
        self.write("ops/wo/README.md", "%s\n" % FAKE_AMOUNT_EURO)
        self.assertFails("README.md")

    def test_amount_in_index(self):
        self.write("ops/INDEX.md", "Indice\n\nSaldo %s\n" % FAKE_AMOUNT_EURO)
        self.assertFails("INDEX.md")

    def test_readme_without_frontmatter_is_ok(self):
        self.write("ops/wo/README.md", "# Work order\n\nUn file per WO, solo riferimenti.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_amount_in_csv(self):
        self.write("ops/scorecard.csv", "saldo,%s\n" % FAKE_AMOUNT_EURO)
        out = self.assertFails("scorecard.csv")
        self.assertIn("importo", out)

    def test_amount_in_uppercase_md(self):
        self.write("ops/WO-005.MD", "%s\n" % FAKE_AMOUNT_EURO)
        out = self.assertFails("WO-005.MD")
        self.assertIn("importo", out)

    def test_amount_in_txt(self):
        self.write("ops/wo/WO-909.txt", "%s\n" % FAKE_AMOUNT_EURO)
        out = self.assertFails("WO-909.txt")
        self.assertIn("importo", out)

    def test_amount_in_hidden_dir(self):
        self.write("ops/.bozze/nota.md", "%s\n" % FAKE_AMOUNT_EURO)
        self.assertFails("nota.md")

    # -- C1 (c'): file fuori formato, anche senza cifre ---------------------

    def test_clean_csv_is_out_of_format(self):
        self.write("ops/scorecard.csv", "settimana,stato\nW41,verde\n")
        out = self.assertFails("scorecard.csv")
        self.assertIn("fuori dal formato", out)

    def test_clean_uppercase_md_is_out_of_format(self):
        src = self.read("ops/wo/WO-904.md").replace("WO-904", "WO-905")
        self.write("ops/wo/WO-905.MD", src)
        out = self.assertFails("WO-905.MD")
        self.assertIn("fuori dal formato", out)

    def test_clean_txt_is_out_of_format(self):
        self.write("ops/wo/WO-909.txt", "nota senza cifre\n")
        out = self.assertFails("WO-909.txt")
        self.assertIn("fuori dal formato", out)

    # -- C1 (a''): importi in lettere / abbreviati ---------------------------

    def _amount_variant(self, text):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"), "\nFabbisogno: %s\n" % text)
        self.assertFails("GOAL.md")

    def test_amount_mila_euro(self):
        self._amount_variant("48" + " mila euro")

    def test_amount_k_eur(self):
        self._amount_variant("48" + "k EUR")

    def test_amount_milioni_di_euro(self):
        self._amount_variant("1,2" + " milioni di euro")

    def test_amount_mln_euro_symbol(self):
        self._amount_variant("1,2" + " mln €")

    def test_amount_M_euro_symbol(self):
        self._amount_variant("3" + "M€")

    def test_amount_euro_first_mila(self):
        self._amount_variant("euro " + "48" + " mila")

    def test_amount_eur_first_milioni(self):
        self._amount_variant("EUR " + "1,2" + " milioni")

    # valuta attaccata al numero, prima o dopo, e tra parentesi (remediation C1/C2)
    def test_amount_eur_glued_after(self):
        self._amount_variant("Nota: 12" + ".000EUR")

    def test_amount_eur_glued_after_decimals(self):
        self._amount_variant("Saldo: 48" + ".500,00EUR")

    def test_amount_eur_glued_before(self):
        self._amount_variant("EUR12" + ".000")

    def test_amount_eur_glued_plain(self):
        self._amount_variant("48500" + "EUR")

    def test_amount_eur_glued_plain_before(self):
        self._amount_variant("EUR" + "48500")

    def test_amount_euro_glued_word(self):
        self._amount_variant("48500" + "euro")

    def test_amount_euro_in_parentheses(self):
        self._amount_variant("saldo 48" + ".500 (euro)")

    def test_amount_glued_in_frontmatter(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "intent", '"Cassa 12' + '.000EUR"')
        self.assertFails("GOAL.md")

    # -- lista dei numeri ammessi (remediation C1/C2, terzo giro) -------------
    # Le forme sotto sono quelle che il verifier ha fatto passare con la sola lista nera.

    def test_allowlist_blocks_markdown_bold_amount(self):
        self._amount_variant("€ **48" + ".500**")

    def test_allowlist_blocks_code_amount(self):
        self._amount_variant("`48" + ".500` EUR")

    def test_allowlist_blocks_colon_currency(self):
        self._amount_variant("Importo (EUR): 12" + ".000")

    def test_allowlist_blocks_signed_amount(self):
        self._amount_variant("€ -12" + ".000")

    def test_allowlist_blocks_html_entity(self):
        self._amount_variant("&euro; 48" + ".500")

    def test_allowlist_blocks_other_currencies(self):
        for text in ("10" + ".000 USD", "£10" + ",000", "CHF 5" + ".000", "48" + ".500 euros"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)

    def test_allowlist_blocks_bare_amount(self):
        self._amount_variant("Saldo di cassa: 48" + ".500")

    def test_allowlist_blocks_table_cell(self):
        self._amount_variant("| Saldo (€) |\n|---|\n| 48" + ".500,00 |")

    def test_allowlist_blocks_spaced_iban(self):
        self._amount_variant("Conto IT60 X054 " + "2811 1010 0000 0123 456")

    def test_allowlist_blocks_foreign_iban(self):
        self._amount_variant("DE89" + "370400440532013000")

    def test_allowlist_blocks_prefixed_piva(self):
        for text in ("P.IVA IT" + "01234567890", "P.IVA: 012 " + "3456 7890"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)

    def test_allowlist_blocks_lowercase_cf(self):
        self._amount_variant("cf rssmra85t10" + "a562s")

    def test_allowlist_blocks_amount_in_words_and_abbrev(self):
        for text in ("quarantotto" + "mila euro", "saldo 48" + "k", "12000 tok" + "€", "£ " + "48"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)

    def test_allowlist_blocks_multiplier_without_currency(self):
        for text in ("fabbisogno stress 48" + " mila", "richiesta bando: 2" + " milioni",
                     "equity round da 1,5" + " milioni", "fabbisogno 1,2" + "M", "Fabbisogno: 1,5" + " M",
                     "cassa a fine anno 85" + " K", "burn 9" + " k al mese", "saldo: quarantotto" + "mila",
                     "un mili" + "one di cassa", "due mili" + "oni"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)

    def test_wo_output_tier_out_of_enum(self):
        for value in ("rosso", "🔴 restricted", "banana"):
            with self.subTest(value=value):
                self.reset()
                self.set_field("ops/wo/WO-901.md", "output-tier", value)
                self.assertFails("WO-901.md")

    def test_currency_indicator_with_small_numbers(self):
        # notazione dei report finance: €k / k€ con valori a 1-2 cifre, "migliaia"
        for text in ("- Ponte minimo: €k " + "90", "fabbisogno stress €k " + "85",
                     "saldo " + "48 migliaia €", "saldo 48,5 " + "migliaia di euro",
                     "- Scenario C, minimo di cassa in €k: −" + "79",
                     "- Cassa a fine mese (€k): ott 3, nov " + "33", "Cassa disponibile (k€): " + "43",
                     "saldo 48 " + "migliaia"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)

    def test_currency_word_with_ids_and_durations_is_ok(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"),
                    "\nStime in effort per P-901…P-905, mai in valuta; importi in euro solo in "
                    "`vault/finance/goals/G-900/basis.md`, orizzonte 12 mesi, copertura 120%.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_currency_unit_in_heading_or_table_header(self):
        cases = {
            "heading+table": "\n## Cassa di partenza riconciliata (€k)\n\n| Conto | Saldo |\n|---|---:|\n"
                             "| Conto A | 41 |\n| Totale | 53 |\n",
            "table header": "\n| Misurabile (€k) | W41 |\n|---|---|\n| Cassa fine mese | 37 |\n",
            "lead-in line": "\nValori in €k:\n- fabbisogno stress: 85\n",
            "heading+text": "\n### Proiezione (k€)\n\nScenario prudente: −42 a fine anno.\n",
        }
        for name, text in cases.items():
            with self.subTest(case=name):
                self.reset()
                self.append(os.path.join(GOAL_DIR, "GOAL.md"), text)
                self.assertFails("GOAL.md")

    def test_currency_scope_ends_at_next_heading_or_table(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"),
                    "\n## Importi (€k)\n\nSolo in `vault/finance/goals/G-900/basis.md`.\n\n"
                    "## Tempi\n\nRunway ≥ 6 mesi, 3 ondate, 4 WO su 15.\n\n"
                    "Valori in €k: vedi finance.\n\nPoi 2 checkpoint.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_currency_k_and_m_units(self):
        for text in ("fabbisogno stress 48 " + "kEUR", "fabbisogno stress 48 " + "KEUR",
                     "fabbisogno stress 48 " + "Keuro", "fabbisogno stress 1,2 " + "MEUR",
                     "fabbisogno stress 1,2 " + "Mio", "Valori in " + "KEuro:\n- stress: 48"):
            with self.subTest(text=text):
                self.reset()
                self._amount_variant(text)
        self.reset()
        self.append(os.path.join(GOAL_DIR, "GOAL.md"),
                    "\n| Scenario | Fabbisogno (" + "kEUR) |\n|---|---|\n| stress | 48 |\n")
        self.assertFails("GOAL.md")

    def test_allowlist_accepts_legit_shapes(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"),
                    "\nScadenza 31/12/2026 e 2026-12-31, settimana 2026-W41, `sync-2026-W41.md`; "
                    "G-900, WO-901, P-901…P-905, ADR-900, CHECKPOINT-01, C10, L2, M12; "
                    "copertura ≥ 120%, 0,5 mesi, 6/15 WO, 1/3 ondate; versione 2.7.2; "
                    "commit `c804ae9` e `302190e`; `40-Finance/cashflow/`; "
                    "tokens: 121000; costo ondata 18000 tok; PR FESR 2021-2027; ISO 27001, ISO/IEC 27001:2022.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_percent_and_months_are_not_amounts(self):
        self.append(os.path.join(GOAL_DIR, "CRITERIA.md"),
                    "\nRunway ≥ 12 mesi nello scenario stress; copertura ≥ 100% del fabbisogno "
                    "(soglia in `vault/finance/cashflow.md`, importi in euro solo lì); "
                    "scostamento ≤ 5% su 3 mesi; M1–M12.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # -- C6: goal chiuso solo con ACCEPT umano --------------------------------

    def test_goal_closed_without_accept(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "status", "closed")
        out = self.assertFails("GOAL.md")
        self.assertIn("ACCEPT", out)

    def test_goal_status_out_of_enum(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "status", "finito")
        self.assertFails("GOAL.md")

    def test_goal_status_closed_synonym(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "status", "chiuso")
        self.assertFails("GOAL.md")

    def test_goal_closed_with_agent_accept(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "status", "closed")
        self.write(os.path.join(GOAL_DIR, "ACCEPT.md"),
                   "---\nzone: direzione\ntier: 🟡\ntype: accept\naccepted-by: coo\n"
                   "accepted-at: 2026-10-10\n---\n\nAccettato.\n")
        self.assertFails("GOAL.md")

    def test_goal_closed_with_human_accept_is_ok(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "status", "closed")
        self.write(os.path.join(GOAL_DIR, "ACCEPT.md"),
                   "---\nzone: direzione\ntier: 🟡\ntype: accept\naccepted-by: human:persona-a\n"
                   "accepted-at: 2026-10-10\n---\n\nAccettato.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # -- C1 (b): instradamento 🔴 ------------------------------------------

    def test_red_wo_to_open_zone(self):
        rel = "ops/wo/WO-901.md"
        self.set_field(rel, "tier", "red")
        self.assertFails("WO-901.md")

    def test_red_wo_to_human_without_acl(self):
        rel = "ops/wo/WO-903.md"
        self.set_field(rel, "to", "human:persona-c")
        self.assertFails("WO-903.md")

    # -- instradamento: il catalogo prevale sull'etichetta del WO (remediation C1) --

    def test_red_service_relabelled_yellow_to_open_zone(self):
        for zone in ("commerciale", "direzione.ops"):
            with self.subTest(zone=zone):
                self.reset()
                self.set_field("ops/wo/WO-902.md", "output-zone", zone)
                self.set_field("ops/wo/WO-902.md", "output-tier", "🟡")
                self.assertFails("WO-902.md")

    def test_red_service_to_human_relabelled_yellow(self):
        self.set_field("ops/wo/WO-902.md", "to", "human:persona-b")
        self.set_field("ops/wo/WO-902.md", "output-zone", "commerciale")
        self.set_field("ops/wo/WO-902.md", "output-tier", "🟡")
        self.assertFails("WO-902.md")

    def test_yellow_wo_to_restricted_zone_for_human_without_acl(self):
        self.set_field("ops/wo/WO-903.md", "output-zone", "finance")
        self.set_field("ops/wo/WO-903.md", "output-tier", "🟡")
        self.assertFails("WO-903.md")

    def test_bare_year_shaped_amount(self):
        self._amount_variant("Incasso atteso: 20" + "35")

    def test_years_in_context_are_ok(self):
        self.append(os.path.join(GOAL_DIR, "GOAL.md"),
                    "\nScadenza nel 2026, Q4 2026, ottobre 2026, fine 2027, entro il 2026, FY 2027, "
                    "anno 2026, December 2026.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_output_zone_differs_from_catalog(self):
        self.set_field("ops/wo/WO-901.md", "output-zone", "finance")
        self.assertFails("WO-901.md")

    def test_output_subzone_of_catalog_is_ok(self):
        self.set_field("ops/wo/WO-902.md", "output-zone", "finance.bandi")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_role_without_write_on_output_zone(self):
        self.set_field("ops/wo/WO-901.md", "to", "finance")
        self.set_field("ops/wo/WO-901.md", "service", "riconciliazione-cassa")
        self.set_field("ops/wo/WO-901.md", "output-tier", "🟡")
        self.assertFails("WO-901.md")

    def test_red_wo_to_role_without_access(self):
        rel = "ops/wo/WO-902.md"
        self.set_field(rel, "to", "sales")
        self.set_field(rel, "service", "forecast-incassi")
        self.assertFails("WO-902.md")

    # -- C1 (c): formato --------------------------------------------------

    def test_wo_without_criteria(self):
        self.set_field("ops/wo/WO-901.md", "criteria", None)
        self.assertFails("WO-901.md")

    def test_wo_status_out_of_enum(self):
        self.set_field("ops/wo/WO-904.md", "status", "done")
        self.assertFails("WO-904.md")

    def test_blocked_without_reason(self):
        self.set_field("ops/wo/WO-903.md", "reason", None)
        self.assertFails("WO-903.md")

    def test_wrong_type(self):
        self.set_field(os.path.join(GOAL_DIR, "CONTEXT.md"), "type", "nota")
        self.assertFails("CONTEXT.md")

    def test_file_outside_format(self):
        self.write("ops/appunti.md", "---\nzone: direzione\ntier: 🟡\ntype: wo\n---\n")
        self.assertFails("appunti.md")

    # -- C6: firme umane ----------------------------------------------------

    def test_closed_without_accepted_by(self):
        self.set_field("ops/wo/WO-901.md", "accepted-by", None)
        self.assertFails("WO-901.md")

    def test_accepted_by_agent(self):
        self.set_field("ops/wo/WO-901.md", "accepted-by", "coo")
        self.assertFails("WO-901.md")

    def test_checkpoint_decided_by_agent(self):
        self.set_field(os.path.join(GOAL_DIR, "CHECKPOINT-01.md"), "decided-by", "coo")
        self.assertFails("CHECKPOINT-01.md")

    def test_goal_owner_not_human(self):
        self.set_field(os.path.join(GOAL_DIR, "GOAL.md"), "owner", "coo")
        self.assertFails("GOAL.md")

    # -- C7: budget anti-loop -------------------------------------------------

    def test_sixteen_wo(self):
        src = self.read("ops/wo/WO-904.md")
        for n in range(905, 917):
            self.write("ops/wo/WO-%d.md" % n, src.replace("WO-904", "WO-%d" % n))
        self.assertFails("WO-916.md")

    def test_four_waves_after_checkpoint(self):
        src = self.read("ops/wo/WO-904.md")
        for i, wave in enumerate((3, 4, 5)):
            n = 905 + i
            text = src.replace("WO-904", "WO-%d" % n).replace("wave: 2", "wave: %d" % wave)
            self.write("ops/wo/WO-%d.md" % n, text)
        self.assertFails("WO-907.md")

    def test_bounce_without_routed_by(self):
        rel = "ops/wo/WO-904.md"
        self.set_field(rel, "to", "coo")
        self.set_field(rel, "service", "dispatch")
        self.set_field(rel, "output-zone", "direzione.ops")
        self.set_field(rel, "output-tier", "🟡")
        self.assertFails("WO-904.md")

    def test_bounce_with_routed_by_is_ok(self):
        rel = "ops/wo/WO-904.md"
        self.set_field(rel, "from", "finance")
        self.set_field(rel, "to", "sales")
        self.set_field(rel, "service", "forecast-incassi")
        self.set_field(rel, "output-zone", "commerciale")
        self.set_field(rel, "output-tier", "🟡")
        self.set_field("ops/wo/WO-901.md", "from", "sales")
        self.set_field(rel, "routed-by", "coo")
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # -- C8: contratto risolvibile --------------------------------------------

    def test_service_not_offered_by_role(self):
        self.set_field("ops/wo/WO-901.md", "service", "piano-cassa")
        self.assertFails("WO-901.md")

    def test_unknown_criterion(self):
        self.set_field("ops/wo/WO-901.md", "criteria", "[C9]")
        self.assertFails("WO-901.md")

    def test_unknown_zone(self):
        self.set_field("ops/wo/WO-901.md", "output-zone", "zona-inesistente")
        self.assertFails("WO-901.md")

    def test_unknown_recipient(self):
        self.set_field("ops/wo/WO-901.md", "to", "ruolo-inesistente")
        self.assertFails("WO-901.md")

    def test_from_cos(self):
        self.set_field("ops/wo/WO-901.md", "from", "cos")
        self.assertFails("WO-901.md")

    def test_inputs_are_pasted_text(self):
        long_text = '"' + "la pipeline contiene molte opportunità aperte " * 6 + '"'
        self.set_field("ops/wo/WO-901.md", "inputs", "[%s]" % long_text)
        self.assertFails("WO-901.md")

    def test_charter_domain_mismatch(self):
        rel = "org/roles/sales.md"
        self.write(rel, self.read(rel).replace("write: [commerciale, direzione.ops]",
                                               "write: [commerciale, direzione.ops, finance]"))
        self.assertFails("sales.md")

    # -- C5: plan-blind -----------------------------------------------------

    def test_verify_cites_wo(self):
        self.append(os.path.join(GOAL_DIR, "VERIFY.md"), "\nC1 confermato da WO-902.\n")
        self.assertFails("VERIFY.md")

    def test_criteria_cites_wave(self):
        self.append(os.path.join(GOAL_DIR, "CRITERIA.md"), "\nSi osserva dopo la wave 1.\n")
        self.assertFails("CRITERIA.md")

    def test_plan_without_criteria_commit(self):
        self.set_field(os.path.join(GOAL_DIR, "PLAN.md"), "criteria-commit", None)
        self.assertFails("PLAN.md")


if __name__ == "__main__":
    unittest.main()
