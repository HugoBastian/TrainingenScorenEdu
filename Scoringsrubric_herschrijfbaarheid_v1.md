# **Scoringsrubric — herschrijfbaarheid van trainingsbronnen**

**Versie 1 · bedoeld voor de scoring-agent die \~1000 oude trainingen scoort vóór het herschrijven**

---

## **1\. Wat deze rubric meet (en wat niet)**

Deze rubric beantwoordt één vraag per training:

**Hoeveel bruikbaar, correct-georiënteerd materiaal zit er in de bron om er automatisch een volwaardige training in de nieuwe stijl van te maken?**

Dat is nadrukkelijk *niet* hetzelfde als "hoe goed is deze pagina zoals hij nu is". Een pagina mag lelijk zijn, verkeerde toon hebben, in de "u"-vorm staan en vol marketing zitten — dat repareert de herschrijver sowieso. Wat telt is of er genoeg overdraagbare substantie in zit. Omgekeerd kan een pagina prettig lezen maar inhoudelijk hol zijn (veel "wat is tool X, opgericht in jaar Y"-achtergrond, geen echte leerinhoud). Die verdient een lage score, hoe vlot hij ook oogt.

Omdat álle trainingen herschreven worden (ook de dunne), is de score **geen auto-vs-handmatig-poort**. De score is:

1. een **kwaliteitsvoorspeller** van de auto-output (rijk → sterke training; dun → correct-maar-mager, kandidaat voor een latere tweede ronde);  
2. een **prioriteringssignaal** voor die tweede ronde;  
3. een **router** voor de enkele gevallen die vóór het herschrijven een menselijke beslissing nodig hebben (structurele veroudering; vrijwel lege bron).

### **Wel scoren, niet scoren**

De nieuwe stijl heeft negen kopjes. Ze hangen verschillend van de bron af:

| Kopje | Bron-afhankelijk? | Rol in de score |
| ----- | ----- | ----- |
| Korte omschrijving | via de kern | via dimensie *Kernhelderheid* |
| Algemene omschrijving | via de kern | via dimensie *Kernhelderheid* |
| **Programma** | **sterk** | zwaarst gewogen dimensie |
| Opzet | nee — boilerplate | **niet gescoord** |
| Doelgroep | zwak — afleidbaar | via *Ondersteunende secties* |
| Voorkennis | zwak — afleidbaar | via *Ondersteunende secties* |
| Doelen | via programma \+ omschrijving | via *Ondersteunende secties* |
| Vervolgtraining | nee — komt uit de catalogus (retrieval) | **niet gescoord** |
| Kortste omschrijving | via de kern | via dimensie *Kernhelderheid* |

Opzet, Vervolgtraining en Certificatie hangen niet van de bron af en tellen dus niet mee in de score.

---

## **2\. De schaal en de verdict-banden**

De ruwe schaal volgt de bestaande ankers: **0** \= geen bruikbare informatie; **50** \= redelijke herschrijving mogelijk; **100** \= staat feitelijk al in de nieuwe stijl.

| Band | Score | Betekenis |
| ----- | ----- | ----- |
| `al_nieuwe_stijl` | 85–100 | Bron is al (vrijwel) conform. Herschrijver valideert en poetst; nauwelijks constructie nodig. |
| `rijk` | 65–84 | Sterke grondstof. Auto-herschrijving levert een volwaardige training met weinig aanvulling. |
| `redelijk` | 45–64 | Bruikbare kern, maar de herschrijver moet substantieel aanvullen (modules opsplitsen/verdiepen, secties afleiden). Correcte maar mogelijk wat magere output; kandidaat voor de tweede ronde. |
| `dun` | 25–44 | Bron draagt het programma nauwelijks; de herschrijver moet veel zelf construeren. Risico op holle output. Menselijke input of tweede ronde aanbevolen. |
| `onbruikbaar` | 0–24 | Vrijwel geen bruikbare inhoud, **óf** een structurele actualiteitsbreuk die eerst een menselijke beslissing vereist. |

---

## **3\. De vier inhoudsdimensies**

Elke dimensie krijgt een score 0–100 met behulp van de verankerde niveaubeschrijvingen hieronder. De basisscore is het gewogen gemiddelde:

basisscore \= 0.15·Kernhelderheid  
           \+ 0.45·Programma-substantie  
           \+ 0.20·Leeruitkomst-oriëntatie  
           \+ 0.20·Ondersteunende secties

Programma weegt het zwaarst omdat een auto-herschrijving staat of valt met een programma dat het aantal dagen vult; het is ook precies de as waarop dunne bronnen (kale opsommingen, tool-achtergrond) vallen.

### **3.1 Kernhelderheid — gewicht 15%**

*Is het onderwerp en de waarde van de training helder genoeg om Korte/Algemene/Kortste omschrijving op te bouwen?*

| Score | Beschrijving |
| ----- | ----- |
| 0–25 | Onderwerp onduidelijk of tegenstrijdig; geen grijpbare kern. |
| 26–50 | Onderwerp herkenbaar maar vaag; waarde/toepassing moet grotendeels geraden worden. |
| 51–75 | Kern helder, met enige indicatie van waarom het relevant is voor de praktijk. |
| 76–100 | Kern scherp en afgebakend; onderwerp én praktijkwaarde meteen duidelijk. |

### **3.2 Programma-substantie — gewicht 45%**

*Bevatten de modules echte, beschrijfbare, niet-overlappende inhoud die een compleet programma vormt voor het aantal dagen?* Beoordeel altijd **relatief aan de duur** uit de bron: 2 rijke modules kunnen een 2-daagse dragen (mits op te splitsen), maar niet een 5-daagse; 5 beschreven modules dekken een 1-daagse ruim.

| Score | Beschrijving |
| ----- | ----- |
| 0–25 | Kale opsomming zonder beschrijving, of vrijwel geen modules. De herschrijver moet structuur én inhoud volledig zelf verzinnen. |
| 26–50 | Modules aanwezig maar dun, overlappend of grotendeels zonder sub-inhoud; de herschrijver moet fors aanvullen om het aantal dagen te vullen. |
| 51–75 | Beschreven, grotendeels niet-overlappende modules met genoeg substantie; herordenen en verdiepen volstaat. Dekt het aantal dagen redelijk. |
| 76–100 | Rijk, afgebakend programma: beschreven modules, duidelijke deelonderwerpen, dekt het aantal dagen volledig. Klaar om te clusteren naar 4–6 modules. |

### **3.3 Leeruitkomst-oriëntatie — gewicht 20%**

*Verwoordt de bron wat de deelnemer met de kennis kan (uitkomsten), of is het vooral achtergrond over de tool ("wat is X, opgericht in jaar Y, hoe werkt het")?* De nieuwe stijl verschuift van technologie naar toepassing; achtergrond-ballast is grotendeels onbruikbaar.

| Score | Beschrijving |
| ----- | ----- |
| 0–25 | Vrijwel uitsluitend tool-/techniekbeschrijving; geen enkel spoor van wat de deelnemer ermee doet. |
| 26–50 | Overwegend achtergrond, met hier en daar een impliciete toepassing. |
| 51–75 | Mix: toepassing is aanwezig maar deels verpakt in uitleg over de tool. |
| 76–100 | Sterk toepassings-/uitkomstgericht ("je leert X zodat je Y sneller/beter doet"); levert rechtstreeks doelen en voordelen. |

### **3.4 Ondersteunende secties — gewicht 20%**

*Zijn Doelgroep, Voorkennis en Doelen aanwezig of schoon af te leiden?* Aanwezig-en-expliciet is het beste; schoon afleidbaar uit onderwerp \+ programma is prima; afwezig-én-niet-afleidbaar drukt de score. Geen enkele ontbrekende sectie zet de score op nul (er zijn geen harde poorten), maar afwezigheid weegt proportioneel mee.

| Score | Beschrijving |
| ----- | ----- |
| 0–25 | Geen van de drie aanwezig en moeilijk af te leiden (onderwerp te vaag om doelgroep/niveau te bepalen). |
| 26–50 | Geen expliciet aanwezig, maar redelijk af te leiden uit onderwerp en programma. |
| 51–75 | Eén of twee expliciet aanwezig; de rest schoon afleidbaar. |
| 76–100 | Doelgroep én voorkennis expliciet in de bron, en het programma levert direct 4–5 doelen. |

---

## **4\. De actualiteitsmodifier (apart gevlagd)**

Actualiteit is géén vijfde gewogen dimensie, maar een **modifier** op de basisscore, plus een **losse vlag** voor de herschrijf-LLM. Reden: dezelfde "verouderde bron" betekent iets totaal anders afhankelijk van het *type*. Daarom scoort de impact op twee assen: **severity** (hoe verouderd) × **type** (repareerbaar of blokkerend).

### **4.1 De twee types**

* **Additief** — de veroudering is met een actualisatieslag te repareren zonder de opzet om te gooien: verouderde termen, gemiste features, samengesmolten vendors, ontbrekende recente ontwikkelingen. De bron blijft bruikbaar; de herschrijver werkt het bij (eventueel met web search). *Voorbeelden: Google Ads mist PMax/GA4/RSA; CRM multichannel→omnichannel; LDAP-vendors.*  
* **Structureel** — de veroudering ondergraaft de lesmethode, het paradigma of de productvraag, en vraagt een inhoudelijke beslissing die het model **niet uit de bron kan halen**. Auto-herschrijven levert dan een zelfverzekerd-foute of holle pagina. *Voorbeelden: React leert het pre-Hooks paradigma (heel curriculum moet om); XSL leunt op de browser-XSLT-processor die wordt uitgefaseerd (eerst een pivot-beslissing nodig).*

### **4.2 Score-impact (afgetrokken van de basisscore)**

| Severity | Additief | Structureel |
| ----- | ----- | ----- |
| none | 0 | — |
| low | −1 tot −3 | −8 tot −12 |
| medium | −5 tot −8 | −15 tot −25 |
| high | −10 tot −15 | −25 tot −40 |

**Structureel, elke severity → `menselijke_input_nodig = true`** en de **eindscore wordt gecapt op ≤ 40** (`dun`/`onbruikbaar`): een structurele breuk hoort altijd langs een mens voordat er automatisch wordt herschreven, ongeacht hoe sterk de inhoud verder is.

### **4.3 De vlag zelf**

Ongeacht de score-impact levert de scorer altijd een gestructureerde actualiteitsvlag op met: `severity`, `type`, een korte samenvatting, een lijst concrete verouderde punten, en een **actie voor de rewriter** — bij additief een "refresh: …"-instructie, bij structureel een "BESLISSING NODIG: …"-instructie. Zo weet de herschrijf-LLM (of de mens) precies welke actualisatieslag nodig is.

**Actualiteit vereist actuele wereldkennis.** De scorer kan niet uit de bron alleen bepalen of iets is uitgefaseerd. Draai de scoring-agent daarom mét web search aan, en laat 'm het onderwerp opzoeken op deprecatie/versie-status vóór hij de vlag zet (zie de "Actualiseren"-stap in de style guide).

---

## **5\. Eindscore berekenen**

basisscore  \= 0.15·K \+ 0.45·P \+ 0.20·L \+ 0.20·O        (0–100)  
eindscore   \= clamp(basisscore \+ actualiteits\_impact, 0, 100\)  
indien type \== structureel:  eindscore \= min(eindscore, 40\)

Daarna mapt de eindscore op de verdict-band uit §2.

---

## **6\. Sectie-dekkingskaart**

Naast de score levert de scorer per afleidbare doelsectie een dekkingslabel op — bruikbaar voor aggregatie ("hoeveel bronnen missen een doelgroep?") en om de herschrijf-prompt te voeden.

Labels: `aanwezig` (staat expliciet in de bron) · `gedeeltelijk` (deels aanwezig/dun) · `afleidbaar` (niet aanwezig maar schoon af te leiden) · `afwezig` (niet aanwezig en niet schoon af te leiden).

Te labelen: `korte_omschrijving`, `algemene_omschrijving`, `programma`, `doelgroep`, `voorkennis`, `doelen`. (Opzet, Vervolgtraining, Certificatie worden overgeslagen — boilerplate/retrieval.)

---

## **7\. Output-schema (JSON)**

De scoring-agent geeft per training exact dit terug. De velden `score`/`feedback` uit de sheet vul je uit `eindscore` en een korte samenvatting van `bruikbaar` \+ `gaten` \+ de actualiteitsvlag.

{  
  "training\_id": 0,  
  "titel": "",  
  "url": "",  
  "kern": "1–2 zinnen: het onderwerp en de praktijkwaarde zoals uit de bron gelezen",  
  "vermoedelijk\_persona": "A | B | C",  
  "aantal\_dagen\_bron": null,

  "dimensies": {  
    "kernhelderheid":        { "score": 0, "toelichting": "" },  
    "programma\_substantie":  { "score": 0, "toelichting": "" },  
    "leeruitkomst\_orientatie":{ "score": 0, "toelichting": "" },  
    "ondersteunende\_secties":{ "score": 0, "toelichting": "" }  
  },  
  "basisscore": 0,

  "actualiteit": {  
    "severity": "none | low | medium | high",  
    "type": "none | additief | structureel",  
    "score\_impact": 0,  
    "samenvatting": "",  
    "specifiek": \[\],  
    "actie\_voor\_rewriter": "refresh: … | BESLISSING NODIG: …"  
  },

  "eindscore": 0,  
  "verdict": "al\_nieuwe\_stijl | rijk | redelijk | dun | onbruikbaar",

  "sectie\_dekking": {  
    "korte\_omschrijving":  "aanwezig | gedeeltelijk | afleidbaar | afwezig",  
    "algemene\_omschrijving":"aanwezig | gedeeltelijk | afleidbaar | afwezig",  
    "programma":           "aanwezig | gedeeltelijk | afleidbaar | afwezig",  
    "doelgroep":           "aanwezig | gedeeltelijk | afleidbaar | afwezig",  
    "voorkennis":          "aanwezig | gedeeltelijk | afleidbaar | afwezig",  
    "doelen":              "aanwezig | gedeeltelijk | afleidbaar | afwezig"  
  },

  "bruikbaar": \[\],  
  "strippen": \[\],  
  "gaten": \[\],  
  "rewrite\_guidance": "",  
  "menselijke\_input\_nodig": false,  
  "menselijke\_input\_wat": "",  
  "scorer\_confidence": "low | medium | high"  
}

---

## **8\. Persona-referentie (voor het `vermoedelijk_persona`\-veld)**

De scorer classificeert de vermoedelijke doelgroep-persona op basis van onderstaande definities (uit de style guide). Dit is een **hulp-hint voor de herschrijver met lage inzet** — de definitieve persona-keuze ligt bij de mens op het moment van herschrijven. Zet `scorer_confidence` navenant.

* **Persona A — Diepgaande IT-professional.** Ervaren IT'er (developers, data, cloud, security). Verwacht technische diepgang, best practices, realistische use cases. Kies A wanneer het onderwerp technisch en hands-on is en gericht op mensen die de techniek zelf bouwen/beheren.  
* **Persona B — Praktische IT-gebruiker (niet-technisch).** Professional die IT als middel gebruikt (marketing, HR, finance, beleid). Wil begrijpen en direct toepassen. Kies B wanneer een tool centraal staat maar de doelgroep 'm gebruikt in plaats van bouwt.  
* **Persona C — Business professional / veranderaar.** Manager, consultant, beleidsmaker. Denkt in impact, keuzes en organisatiecontext. Kies C wanneer het onderwerp strategie, proces of besluitvorming is (bijv. een CRM-strategie- of governance-training).

---

## **9\. IJkvoorbeelden (reproduceren jouw handmatige labels)**

Deze vijf zijn met de rubric doorgerekend en landen binnen enkele punten van jouw eigen scores. Gebruik ze óók als few-shot-ankers in de scoring-prompt.

### **React — jouw label 30 → rubric 30**

* Kern 75 · Programma **20** (kale opsomming, geen beschrijvingen) · Leeruitkomst 35 · Ondersteunend 60 (voorkennis expliciet, rest afleidbaar)  
* basisscore ≈ 39  
* Actualiteit: **structureel, high** (pre-Hooks paradigma, heel curriculum moet om naar function components/Hooks/Vite/React 19/TS) → cap ≤ 40, impact tot 30  
* **eindscore 30**, verdict `dun`, `menselijke_input_nodig = true` (curriculumkeuze)

### **XSL — jouw label 40 → rubric 40**

* Kern 75 · Programma **40** (dun, overlappend voor 2-daagse) · Leeruitkomst 35 (veel "wat is X"-achtergrond) · Ondersteunend 50 (afleidbaar)  
* basisscore ≈ 46  
* Actualiteit: **structureel, high** (browser-XSLT-processor wordt uitgefaseerd; pivot naar server-side/XSLT 3.0 nodig) → cap ≤ 40  
* **eindscore 40**, verdict `dun`, `menselijke_input_nodig = true` (pivot-beslissing)

### **Google Ads Basis — jouw label 65 → rubric \~65**

* Kern 85 · Programma **75** (5 beschreven modules \+ case, dekt 1-daagse) · Leeruitkomst 80 (sterk uitkomstgericht) · Ondersteunend 80 (doelgroep \+ voorkennis expliciet)  
* basisscore ≈ 79  
* Actualiteit: **additief, high** (mist PMax/Smart Bidding/GA4/RSA/AI Max; verouderde claims) → impact ≈ −13  
* **eindscore \~66**, verdict `rijk`, vlag hoog maar repareerbaar. *Dit is de casus die "actualiteit valt buiten het cijfer" verzoent met "moet meetellen": additief-hoog drukt de score wél, maar bescheiden.*

### **CRM — jouw label 70 → rubric \~69**

* Kern 85 · Programma **72** (6 beschreven, niet-overlappende modules \+ case) · Leeruitkomst 65 · Ondersteunend 55 (afleidbaar)  
* basisscore ≈ 69  
* Actualiteit: **additief, low** (evergreen strategie; lichte verfrissing: omnichannel, cloud/AI, AVG) → impact ≈ 0  
* **eindscore \~69**, verdict `rijk`

### **LDAP — jouw label 70 → rubric \~68**

* Kern 85 · Programma **68** (2 rijke modules voor 2-daagse; opsplitsen nodig, maar substantie aanwezig) · Leeruitkomst 60 · Ondersteunend 55 (afleidbaar)  
* basisscore ≈ 68  
* Actualiteit: **additief, low** (stabiele infrastructuur; vendors samengevoegd, cloud-IdP-context toe te voegen) → impact ≈ 0  
* **eindscore \~68**, verdict `rijk`

---

## **10\. Kant-en-klare scoring-prompt**

**Wat geef je mee per call.** De vaste prefix (identiek voor alle \~1000 trainingen, dus cachebaar) is de rubric §1–§8, inclusief het persona-blok. De variabele input per call is alleen de brontekst van die ene training (titel, duur, prijs, body). Je hoeft de style guide **niet** apart mee te geven: alles wat de scorer nodig heeft is in de rubric gedistilleerd. Draai de agent mét web search aan (voor de actualiteitscheck).

system  \= \[ rubric §1–§8 \+ persona-blok \]        ← vast, gecached  
user    \= \[ brontekst van deze training \]         ← wisselt per call

Plak onderstaande instructie boven de vaste prefix.

Je scoort een oude trainingsbeschrijving op HERSCHRIJFBAARHEID: hoeveel bruikbaar,  
correct-georiënteerd materiaal er in de bron zit om er automatisch een volwaardige  
training in de nieuwe stijl van te maken. Je scoort NIET hoe goed de pagina nu is —  
toon, format en marketing repareert de herschrijver sowieso.

Werkwijze:  
1\. Lees de brontekst. Bepaal de kern (onderwerp \+ praktijkwaarde), het aantal dagen,  
   en de vermoedelijke persona (A/B/C, zie persona-blok) — dit laatste is een hint met  
   lage inzet, zet scorer\_confidence navenant.  
2\. Scoor de vier dimensies 0–100 met de verankerde niveaubeschrijvingen:  
   \- Kernhelderheid (15%)  
   \- Programma-substantie (45%) — beoordeel RELATIEF aan het aantal dagen  
   \- Leeruitkomst-oriëntatie (20%) — straf tool-achtergrond-ballast af  
   \- Ondersteunende secties (20%) — aanwezig \> afleidbaar \> afwezig  
3\. Bereken de basisscore als gewogen gemiddelde.  
4\. Beoordeel actualiteit. Zoek het onderwerp op (web search) om deprecatie/versie-status  
   vast te stellen. Bepaal severity (none/low/medium/high) en type:  
   \- additief  \= repareerbaar met een refresh → bescheiden score-impact  
   \- structureel \= vraagt een inhoudelijke/pedagogische beslissing die niet uit de bron  
     te halen is → forse impact, cap eindscore ≤ 40, menselijke\_input\_nodig \= true  
   Trek de impact af van de basisscore (zie impacttabel), clamp 0–100, pas de cap toe.  
5\. Map de eindscore op de verdict-band.  
6\. Label de sectie-dekking per afleidbare doelsectie.  
7\. Schrijf VOORUITGERICHTE feedback voor de herschrijf-LLM: wat is bruikbaar, wat moet  
   gestript, welke gaten zijn er (en zijn die afleidbaar of vragen ze menselijke input),  
   en een korte rewrite\_guidance. Geen kritiek op de huidige staat — alleen wat de  
   herschrijver moet weten.

Geef UITSLUITEND geldige JSON terug volgens het meegeleverde schema. Geen tekst eromheen.

Kalibratie-ankers (voorbeeldscores): React 30 (structureel), XSL 40 (structureel),  
Google Ads 65 (additief-hoog), CRM 70 (additief-laag), LDAP 68 (additief-laag).

---

## **11\. Kalibratie en gebruik**

1. **Valideer voor je opschaalt.** Scoor \~30 diverse trainingen handmatig (label \+ één zin waarom), draai de agent erover, en leg naast elkaar. Kijk of de scores correleren en of de verdict-grenzen landen waar je ze wil. Stel dan de gewichten en de actualiteits-impacttabel bij — die getallen zijn expliciet bedoeld om te tunen.  
2. **De één ontwerpkeuze om te bevestigen.** Hoe hard mag additief-hoog bijten? Ik heb 'm nu op ≈ −13 gezet zodat Google Ads op \~65 landt (jouw label). Wil je additieve veroudering nóg lichter laten meetellen (dichter bij "buiten het cijfer"), verlaag dan de additieve rij in de impacttabel; dat tikt Google Ads richting \~72.  
3. **Twijfelgevallen langs een mens.** Scores dicht bij een bandgrens en alles met `scorer_confidence: low` verdienen een steekproef-blik, want verkeerd routeren is asymmetrisch duur.  
4. **De vlaggen voeden de vervolgstap.** `actualiteit.actie_voor_rewriter` en `rewrite_guidance` gaan rechtstreeks de herschrijf-prompt in; `menselijke_input_nodig` en `menselijke_input_wat` vullen de kleine mens-wachtrij; `sectie_dekking` aggregeer je om te zien hoe scheef je populatie is.

