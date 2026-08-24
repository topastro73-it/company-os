#!/usr/bin/env python3
"""Letture dal conto Qonto (API v2): saldi dei conti e movimenti del mese.

=============================================================================
COSA FA E COSA NON FA
=============================================================================
Interroga l'API di Qonto e stampa i saldi dei conti oppure i movimenti di un
mese, in formato leggibile o come JSON (`--json`).

È SOLA LETTURA: chiama solo endpoint di lettura (GET). Non dispone bonifici,
non modifica nulla sul conto, non manda dati a terzi. Il caso peggiore è una
lettura che fallisce.

=============================================================================
È UN ESEMPIO, NON UNO SCHELETRO DA RIEMPIRE
=============================================================================
Questo file arriva insieme al template: è codice vero, in uso in
un'installazione reale, ripulito dai dati dell'azienda d'origine. Se usi Qonto
funziona così com'è. Se usi un'altra banca, prendilo come modello: la struttura
(autenticazione, paginazione, gestione errori, output `--json`) vale per
qualunque provider, cambia solo la parte di chiamata all'API.

=============================================================================
COME SI LANCIA E COME SI DANNO LE CREDENZIALI
=============================================================================
Non lanciarlo direttamente. Usa il wrapper `bank-qonto.sh`, che sta nella
stessa cartella: legge le credenziali dal Keychain di macOS e le passa qui
come variabili d'ambiente, senza mai stamparle.

    bash scripts/integrations/bank-qonto.sh balance
    bash scripts/integrations/bank-qonto.sh balance --json
    bash scripts/integrations/bank-qonto.sh transactions --month 2026-08

Setup una volta sola per macchina — i due valori si trovano in
Qonto → Integrazioni → API key:

    security add-generic-password -a "qonto" -s "QONTO_LOGIN"  -w "acme-1234"      -U
    security add-generic-password -a "qonto" -s "QONTO_SECRET" -w "la-tua-secret"  -U

Il `-a "qonto"` è il nome dell'account nel Keychain. Se da te quelle voci si
chiamano in un altro modo, non serve modificare niente: dichiaralo con

    export QONTO_KEYCHAIN_ACCOUNT="qonto-acme"

Se non sei su macOS, o preferisci non usare il Keychain, esporta a mano le due
variabili che questo script legge — in quel caso il wrapper non tocca il
Keychain:

    QONTO_LOGIN     login dell'organizzazione (una stringa tipo `acme-1234`)
    QONTO_SECRET    secret key generata da Qonto

=============================================================================
DIPENDENZE
=============================================================================
Nessuna libreria di terze parti: solo la standard library di Python 3
(`urllib`, `json`, `argparse`). Niente `pip install`.

Uso diretto (se le variabili d'ambiente sono già impostate):
  bank_qonto_sync.py balance [--json]
  bank_qonto_sync.py transactions [--month YYYY-MM] [--json]
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

API = "https://thirdparty.qonto.com/v2"
# Cloudflare, davanti a Qonto, rifiuta lo User-Agent di default di urllib
# ("Python-urllib/3.x") con un errore 1010: serve un UA esplicito.
UA = "company-os/1.0 (bank_qonto_sync.py)"


def _auth() -> str:
    login, secret = os.environ.get("QONTO_LOGIN"), os.environ.get("QONTO_SECRET")
    if not login or not secret:
        sys.exit("QONTO_LOGIN/QONTO_SECRET assenti — lancia lo script via "
                 "scripts/integrations/bank-qonto.sh")
    return f"{login}:{secret}"  # Qonto vuole la coppia in chiaro, non Basic base64


def _get(path: str, params: dict | None = None) -> dict:
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": _auth(),
        "Accept": "application/json",
        "User-Agent": UA,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        if "error_code\":1010" in detail or "Error 1010" in detail:
            sys.exit("Cloudflare ha bloccato la richiesta (1010): User-Agent rifiutato.\n"
                     "Non e' un problema di credenziali — aggiorna UA in bank_qonto_sync.py.")
        if e.code in (401, 403):
            sys.exit(f"Qonto ha rifiutato le credenziali (HTTP {e.code}). "
                     f"Rigenera la API key e riscrivila nel Keychain.\n{detail}")
        sys.exit(f"Qonto HTTP {e.code} su {path}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Qonto irraggiungibile: {e.reason}")


def _eur(cents: int | None, fallback: float | None) -> float:
    """Preferisce i centesimi interi: il float di Qonto arrotonda."""
    if cents is not None:
        return round(cents / 100, 2)
    return round(fallback or 0.0, 2)


def _fmt(v: float) -> str:
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return f"€{s}"


def accounts() -> list[dict]:
    # Nota: prendiamo solo i campi che servono a saldi e movimenti. Le coordinate
    # bancarie complete non vengono lette ne' stampate: a un saldo non servono, e
    # tenerle fuori dall'output evita di ritrovarsele in un log o in un file.
    org = _get("/organization").get("organization", {})
    out = []
    for a in org.get("bank_accounts", []):
        out.append({
            "name": a.get("name") or a.get("slug") or "(senza nome)",
            "slug": a.get("slug"),
            "currency": a.get("currency", "EUR"),
            "balance": _eur(a.get("balance_cents"), a.get("balance")),
            "authorized_balance": _eur(a.get("authorized_balance_cents"),
                                       a.get("authorized_balance")),
            "updated_at": a.get("updated_at"),
            "status": a.get("status"),
        })
    return out


def cmd_balance(args) -> None:
    accs = accounts()
    total = round(sum(a["balance"] for a in accs), 2)
    total_auth = round(sum(a["authorized_balance"] for a in accs), 2)
    if args.json:
        print(json.dumps({"accounts": accs, "total": total,
                          "total_authorized": total_auth,
                          "read_at": datetime.now().isoformat(timespec="seconds")},
                         ensure_ascii=False, indent=2))
        return
    print(f"Saldi Qonto — letti il {date.today().isoformat()}\n")
    width = max((len(a["name"]) for a in accs), default=10)
    for a in accs:
        flag = "" if a["balance"] == a["authorized_balance"] else \
               f"   (autorizzato {_fmt(a['authorized_balance'])})"
        print(f"  {a['name']:<{width}}  {_fmt(a['balance']):>14}{flag}")
    print(f"\n  {'TOTALE QONTO':<{width}}  {_fmt(total):>14}")
    if total != total_auth:
        print(f"  {'di cui autorizzato':<{width}}  {_fmt(total_auth):>14}")
    print("\n⚠️  Solo conti Qonto. L'endpoint /organization NON restituisce i conti")
    print("   esterni collegati via Open Banking: gli eventuali conti presso altre")
    print("   banche vanno letti a parte. Questo NON e' il totale della cassa")
    print("   aziendale, ma solo la quota che sta su Qonto.")


def _month_bounds(month: str | None) -> tuple[str, str, str]:
    if month:
        try:
            y, m = (int(x) for x in month.split("-"))
            first = date(y, m, 1)
        except (ValueError, TypeError):
            sys.exit(f"--month non valido: '{month}' (atteso YYYY-MM)")
    else:
        today = date.today()
        first = date(today.year, today.month, 1)
    last = date(first.year, first.month, calendar.monthrange(first.year, first.month)[1])
    return (f"{first.isoformat()}T00:00:00.000Z",
            f"{last.isoformat()}T23:59:59.999Z",
            first.strftime("%Y-%m"))


def transactions(month: str | None) -> tuple[list[dict], str]:
    since, until, label = _month_bounds(month)
    rows: list[dict] = []
    for acc in accounts():
        if not acc["slug"]:
            continue
        page: int | None = 1
        while page:
            d = _get("/transactions", {
                "slug": acc["slug"], "settled_at_from": since, "settled_at_to": until,
                "current_page": page, "per_page": 100,
            })
            for t in d.get("transactions", []):
                rows.append({
                    "account": acc["name"],
                    "settled_at": (t.get("settled_at") or "")[:10],
                    "emitted_at": (t.get("emitted_at") or "")[:10],
                    "side": t.get("side"),
                    "amount": _eur(t.get("amount_cents"), t.get("amount")),
                    "currency": t.get("currency", "EUR"),
                    "label": t.get("label"),
                    "counterparty": t.get("counterparty_name"),
                    "reference": t.get("reference"),
                    "category": t.get("category"),
                    "status": t.get("status"),
                })
            page = (d.get("meta") or {}).get("next_page")
    rows.sort(key=lambda r: (r["settled_at"] or "", -r["amount"]))
    return rows, label


def cmd_transactions(args) -> None:
    rows, label = transactions(args.month)
    settled = [r for r in rows if r["status"] != "declined"]
    ent = [r for r in settled if r["side"] == "credit"]
    usc = [r for r in settled if r["side"] == "debit"]
    tot_e = round(sum(r["amount"] for r in ent), 2)
    tot_u = round(sum(r["amount"] for r in usc), 2)
    if args.json:
        print(json.dumps({"month": label, "transactions": rows,
                          "entrate": tot_e, "uscite": tot_u,
                          "netto": round(tot_e - tot_u, 2)},
                         ensure_ascii=False, indent=2))
        return
    print(f"Movimenti Qonto — {label}  ({len(settled)} movimenti)\n")
    print(f"  Entrate:  {_fmt(tot_e):>14}  ({len(ent)})")
    print(f"  Uscite:   {_fmt(tot_u):>14}  ({len(usc)})")
    print(f"  Netto:    {_fmt(round(tot_e - tot_u, 2)):>14}")
    for titolo, gruppo in (("Top 5 entrate", ent), ("Top 5 uscite", usc)):
        if not gruppo:
            continue
        print(f"\n  {titolo}")
        for r in sorted(gruppo, key=lambda x: -x["amount"])[:5]:
            who = r["counterparty"] or r["label"] or "—"
            print(f"    {r['settled_at']}  {_fmt(r['amount']):>12}  {who[:44]}")
    scartati = len(rows) - len(settled)
    if scartati:
        print(f"\n  ({scartati} movimenti 'declined' esclusi dai totali)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Letture Qonto v2 (sola lettura)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("balance", help="saldi dei conti")
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_balance)

    t = sub.add_parser("transactions", help="movimenti di un mese")
    t.add_argument("--month", help="YYYY-MM (default: mese corrente)")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_transactions)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
