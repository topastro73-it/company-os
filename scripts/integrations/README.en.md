# Integrations — example scripts

**Working** scripts, taken from real company-os deployments and stripped of the
originating company's data. They are not skeletons to fill in: if you use the same
provider they work as they are, and if you use a different one they serve as a model.

Three rules that hold for everything in here:

- **Read-only** — none of these scripts write to the external system. The worst case
  is a read that fails.
- **Zero dependencies** — bash and the Python 3 standard library. No `pip install`.
- **Credentials outside the repo** — they are read from the macOS Keychain (or from
  environment variables), never from versioned files.

## What is here today

| File | What it does |
|------|--------------|
| `bank-qonto.sh` | The command you run: it pulls the Qonto credentials from the Keychain and starts the Python script. |
| `bank_qonto_sync.py` | Reads account balances and a month's transactions from Qonto (API v2), as readable text or `--json`. |

Setup instructions — which two values you need, where to put them, what the Keychain
entry is called — are in the comment block at the top of each script (in Italian, the
base language of this repo).

## How people get here

The `/admin setup` interview asks whether the company has a business bank account: if
the provider is one of those covered here, it points to this directory instead of
having the integration written from scratch.
