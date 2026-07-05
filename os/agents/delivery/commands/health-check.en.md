# /delivery health-check — Partner health score

## Purpose
Compute a partner's health score (0-100) (or everyone's), with trend and recommendations.

## Input
- Partner slug (optional — if omitted: all, in board mode)

## Steps
1. Load the partner card and the available data (platform/ERP if MCP is active,
   otherwise the latest recorded data — declare its freshness).
2. Compute the **5 weighted indicators**:
   SMBs Onboarded 25% · SMBs Active 30d 25% · SMB churn per quarter 20% ·
   Salespeople engagement 15% · NPS 15%.
   `Health = Σ(indicator × weight)`. Indicator with no data → ⚫ and flag it, don't make it up.
3. Assign the **band**: Healthy 80-100 · Stable 60-79 · At-Risk 40-59 · Critical 0-39.
4. **Trend**: compare with the previous score recorded in the card; drop >15 points
   in 30d → WARNING even if the band holds.
5. **Recommendations by band**: Healthy → expansion play; Stable → engagement boost
   (training, co-marketing); At-Risk → proactive call ≤14d; Critical → CEO escalation,
   rescue plan ≤7d.
6. Update `health-score` and the history in the partner card; in board mode also update
   the cross-partner picture.

## Output format
```markdown
## Partner Health — {name} ({YYYY-MM-DD})
| Indicator | Score | Detail |
|---|---|---|
| SMBs Onboarded | 85 | 34/40 target |
| … | | |

**Health Score: {N}/100 — {Band}** · Trend: {↑/↓ from N}
### Recommendations (max 3, with owner and deadline)
```

## Destination
Single partner: `clienti/{slug}` zone → health section of the `scheda-partner.md`.
Cross-partner board: `commerciale` zone → `delivery/health-board.md`.
Commit (admin): `[delivery] health: {slug} {score}`.
