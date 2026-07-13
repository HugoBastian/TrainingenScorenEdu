# Trainingen scoren op herschrijfbaarheid

Scoort oude trainingsbeschrijvingen volgens `Scoringsrubric_herschrijfbaarheid_v1.md`.
De **LLM oordeelt** (4 dimensiescores + actualiteit + vlaggen); **Python rekent** (basisscore,
impact, cap, verdict). Zo is de scoring deterministisch en her-tunebaar zonder opnieuw te callen.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # ANTHROPIC_API_KEY
```

Zet in dezelfde map: `Scoringsrubric_herschrijfbaarheid_v1.md` en sheet met trainingen als **xlsx**.

## Gebruik

Kalibreren (aanrader): open `calibratie.ipynb`, draai op de eerste 10, leg naast je labels.

Of via de command line:
```bash
python score_trainings.py --in trainingen.xlsx --out trainingen_scored.xlsx --limit 10
python score_trainings.py --in trainingen.xlsx --out trainingen_scored.xlsx   # alles
python score_trainings.py --in trainingen.xlsx --out out.xlsx --no-web-search # sneller/goedkoper testen
```

Offline sanity check (geen API-key nodig):
```bash
python test_scoring.py
```

## Tuneable

Alle knoppen staan bovenaan `score_trainings.py`:
- **`IMPACT`** — hoe hard actualiteit meetelt. Dé kalibratieknop. De `basisscore` geeft het gewogen gemiddelde van de vier scoringsdomeinen onafhankelijk van van actualiteit. De eindscore geeft de basisscore een penalty.
- **`WEIGHTS`** — dimensiegewichten (nu 15/45/20/20).
- **`STRUCTUREEL_CAP`** — structurele breuk capt de eindscore (nu ≤40) en zet de mens-vlag.
- **`VERDICT_BANDS`** — grenzen van de verdict-banden.
- **`USE_WEB_SEARCH`** — Toggle Web Search
- **`RUBRIC_CUT`** — '**RUBRIC_CUT - 1**' is hoeveel secties van de rubric meegestuurd worden

## Definities scoringsdimensies

- **`Kernhelderheid`** — Is het onderwerp en de waarde van de training helder genoeg om Korte/Algemene/Kortste omschrijving op te bouwen?
- **`Programma-substantie`** — Bevatten de modules echte, beschrijfbare, niet-overlappende inhoud die een compleet programma vormt voor het aantal dagen, passend voor het niveau van de training?
- **`Leeruitkomst-oriëntatie`** — Verwoordt de bron wat de deelnemer met de kennis kan (uitkomsten), of is het vooral achtergrond over de tool ("wat is X, opgericht in jaar Y, hoe werkt het")?
- **`Ondersteunende secties`** — Zijn Doelgroep, Voorkennis en Doelen aanwezig of schoon af te leiden? 