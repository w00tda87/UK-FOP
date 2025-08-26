# FOP Generator


Byg og kør UK FOP (Foreign Carrier Permit) generator uden lokal Python ved hjælp af GitHub Actions.


## Hurtigt i gang
1. Læg din officielle `assets/CPG3200.pdf` i repoet (eller kopier den manuelt senere ved kørsel).
2. Gå til **Actions** → kør **Build EXE**.
3. Hent `FOP-Generator.zip` fra artifacts, pak ud, kør `FOP-Generator.exe`.


## Kørsel
- Standard udfylder PDF og genererer `CPG3200_filled.pdf`.
- CLI:
- `--mode pdf|mock`
- `--send` (kræver SMTP_HOST/PORT/USER/PASS som miljøvariabler)
- `--attach-template` (vedlægger skabelonen som ekstra vedhæftning)
