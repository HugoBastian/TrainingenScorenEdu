# Trainingen scoren op herschrijfbaarheid

Scoort oude trainingsbeschrijvingen volgens `Scoringsrubric_herschrijfbaarheid_v1.md`.
De **LLM oordeelt** (4 dimensiescores + actualiteit + vlaggen); **Python rekent** (basisscore,
impact, cap, verdict). Zo is de scoring deterministisch en her-tunebaar zonder opnieuw te callen.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # en vul je ANTHROPIC_API_KEY in
```

Zet in dezelfde map: `Scoringsrubric_herschrijfbaarheid_v1.md` en je sheet als **xlsx**
(Google Sheet → Bestand → Downloaden → Microsoft Excel).

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

## Dagen invullen

De programma-score (45%) wordt beoordeeld *relatief aan het aantal dagen*. Zet dat waar je het
weet als eerste sleutel in de `content`-cel: `{"dagen": 5, "intro": ...`. Ontbreekt het, dan schat
het model het en markeert `dagen_bron_herkomst = geschat`.

## Wat er nog te tunen valt (na ~30 labels)

Alle knoppen staan bovenaan `score_trainings.py`:
- **`IMPACT`** — hoe hard actualiteit meetelt. Dé kalibratieknop. Defaults reproduceren de 5 ijklabels
  binnen ~3 punten. Additief-hoog staat op −13 (Google Ads → ~65); lichter maken tikt 'm richting ~72.
- **`WEIGHTS`** — dimensiegewichten (nu 15/45/20/20).
- **`STRUCTUREEL_CAP`** — structurele breuk capt de eindscore (nu ≤40) en zet de mens-vlag.
- **`VERDICT_BANDS`** — grenzen van de verdict-banden.

## Later: rechtstreeks naar Google Sheets schrijven

Nu bestand-gebaseerd (xlsx in, xlsx uit). Wil je bij het opschalen rechtstreeks in de live sheet
schrijven, dan komt daar `gspread` + een service-account bij — pas doen als de rubric gekalibreerd is.
Voor de bulk-run van ~1000 loont ook de **Batch API** (~50% goedkoper); dat is een kleine aanpassing
op `score_one`.
