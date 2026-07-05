# company/ — snapshot delle zone operative Drive

Questa cartella è lo **snapshot versionato** delle zone Drive-master (`osctl snapshot`).
Il **master è Google Drive**: qui il repo tiene versioning e backup. In sessione admin puoi
editare un file di `company/` SOLO se poi lo ripubblichi (`osctl publish`), altrimenti il
prossimo snapshot lo sovrascrive.

Nel template è vuota: si popola quando colleghi il Drive e lavori. Struttura attesa (una
sottocartella per zona): `direzione/ commerciale/ clienti/ prodotto/ compliance/ marketing/`.
La zona `finance` e i `contratti` finiscono in `vault/` (vedi `config/acl.yaml → snapshot_target`).
