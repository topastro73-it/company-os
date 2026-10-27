# Collaborazione tra agenti — ledger, work order, ondate

Come i ruoli-agente lavorano in squadra su un goal aziendale. Il loop: intento → criteri
pre-registrati (plan-blind) → piano a ondate di work order (WO) → esecuzione per competenza →
verifica plan-blind del Controller → accept umano. Coordina l'agente **coo**, che risponde al
**CEO**. Ogni goal ha **un solo owner umano accountable**. Livelli di autonomia: `os/protocols/autonomy.md`.
Ruoli, servizi e decisioni: `os/org/services.yaml`, `os/org/decision-rights.yaml`, domain in
`config/acl.yaml → roles`.

## Ledger (zona `direzione`, sottozona `ops`, Drive-master)

```
ops/goals/G-NNN-slug/  GOAL.md · CONTEXT.md · CRITERIA.md · PLAN.md · VERIFY.md
                       WAVE-NN.md · CHECKPOINT-NN.md · ACCEPT.md
ops/wo/WO-NNN.md       un file per work order (numerazione globale)
ops/scorecard.md       righe datate settimanali (misurabile, owner, stato, ref)
ops/standup/YYYY-MM-DD.md
```

Si scrive sul Drive (in admin: mount locale `OS_DRIVE_MOUNT`), poi lo snapshot porta i file in
`company/direzione/ops/`. Mai two-way sullo stesso file.

**Frontmatter comune** a ogni file: `zone: direzione`, `tier: 🟡`, `type:` ∈ {goal, context,
criteria, plan, verify, checkpoint, wave, accept, wo, scorecard, standup}.

- GOAL: `id`, `owner: human:<slug>`, `due`, `status`.
- PLAN: `criteria-commit: <hash>` del commit che ha registrato i CRITERIA.
- CHECKPOINT: `decided-by: human:<slug>`, `decided-at`, `decision` (prosegui | correggi | ferma).
- ACCEPT: `accepted-by: human:<slug>`, `accepted-at`.

## Work order

```yaml
id: WO-NNN            # = nome file
goal: G-NNN           # goal di riferimento
from: coo             # ruolo-agente emittente
to: <ruolo> | human:<slug>
service: <servizio>   # offerto da `to` in os/org/services.yaml
intent: "una riga: perché serve"
inputs: [<path o id>] # solo riferimenti, mai dati incollati
output-zone: <zona o zona.sotto di config/acl.yaml>
output-tier: 🔴 | 🟡 | 🟢
criteria: [C1, C3]    # C-id esistenti nel CRITERIA del goal
due: YYYY-MM-DD
status: proposed
wave: 1
parent:               # WO da cui deriva (vuoto se nessuno)
routed-by:            # `coo` se `to` è il mittente del parent
accepted-by:          # human:<slug> — obbligatorio con status closed
accepted-at:
```

**Stati**: `proposed → accepted → in-progress → delivered → verified → closed`; uscite
`rejected` e `blocked`, che richiedono `reason` (motivo) ed `exit` (via d'uscita proposta).
La nota di consegna (`delivered`) contiene solo ref all'output e `tokens: <n>`.

**Chi emette WO**: il coo e i ruoli pilota, solo verso servizi a catalogo. Il `cos` **non
emette né assegna WO**: legge il ledger e fa briefing al servizio di coo e CEO.

## Modalità di interazione (Team Topologies)

| Modalità | Quando | Passa dal coo? |
|---|---|---|
| **X-as-a-Service** | servizio a catalogo, input/output noti | no: WO diretto tra ruoli, il coo lo vede nel ledger |
| **Collaboration** | lavoro nuovo, fuori catalogo, più ruoli insieme | sì: il coo apre i WO e decide l'ondata |
| **Facilitating** | un ruolo aiuta un altro a usare un servizio | sì, a tempo, con WO dedicato |

Il coo decide anche priorità tra goal e conflitti; sopra le soglie di
`os/org/decision-rights.yaml` decide il CEO.

## Escalation

Ruolo → **coo** → **CEO**. Un WO `blocked` va al coo entro la giornata; il coo sblocca
(`/coo unblock`) o porta la scelta al CEO con opzioni e raccomandazione.

## Anti-loop e budget

- **≤ 15 WO per goal** e **≤ 3 ondate** dopo l'ultimo CHECKPOINT umano.
- Al limite: stop, nessun nuovo WO, escalation al CEO con un CHECKPOINT da firmare.
- **Nessun rimbalzo al mittente**: un WO derivato non torna al ruolo che ha emesso il parent,
  salvo `routed-by: coo`.
- A fine ondata il coo scrive `WAVE-NN.md` con il costo **in token** per WO e totale (mai valuta),
  scritto `<n> tok`.

## Blackboard + dispatcher

I subagenti non lanciano subagenti. Quindi il coo gira **nella sessione principale**: legge il
ledger (blackboard), lancia i subagenti dell'ondata con un brief stretto (WO + path di output),
raccoglie i WO che emettono e li smista nell'ondata successiva.

## Dati sensibili (ADR-004)

- Nel ledger **solo riferimenti**: nessun importo, IBAN, CF/P.IVA, saldo o salario.
- Le soglie dei criteri stanno in mesi o percentuali; gli importi in un file della zona finance.
- Il VERIFY del ledger contiene solo l'**esito per criterio** e il ref; il dettaglio con i
  numeri sta nella zona finance.
- Un WO con output 🔴 va solo verso una zona 🔴 (`tier: restricted` o `snapshot_target: vault`) e
  verso un destinatario con accesso a quella zona.
- Il WAVE riporta i costi in token.
- **Numeri ammessi nel ledger** (`scripts/audit/ledger-check.py`, lista dei numeri ammessi):
  0–99, date, settimane ISO, anni, id (`G-NNN`, `WO-NNN`, `P-NNN`), percentuali, versioni,
  hash di commit, `tokens: <n>` e `<n> tok`. Ogni altro numero di 3+ cifre blocca il commit:
  si sposta nella zona finance e nel ledger resta il riferimento.

## Plan-blind

I CRITERIA del goal si **committano prima** del PLAN, scritti dal Controller leggendo solo GOAL,
CONTEXT e canone. Il PLAN cita `criteria-commit`. I CRITERIA non citano WO né ondate; il VERIFY
non cita WO né PLAN: la prova è sempre una fonte osservabile.

## Guardrail meccanico

`scripts/audit/` → ledger-check.py applica questo protocollo (formato, stati, contratti dei
WO, instradamento 🔴, firme umane, budget, plan-blind) in pre-commit, CI, snapshot e
`/admin health`. Rosso = si ferma e si sistema.
