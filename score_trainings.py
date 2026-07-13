"""
score_trainings.py
==================
Scoort oude trainingsbeschrijvingen op HERSCHRIJFBAARHEID volgens
`Scoringsrubric_herschrijfbaarheid_v1.md`.

Ontwerpprincipes:
- De LLM levert alleen OORDELEN (4 dimensiescores, actualiteit-type/severity, vlaggen).
- Alle REKENKUNDE (basisscore, actualiteit-impact, cap, verdict) doet Python -> deterministisch
  en her-tunebaar zonder opnieuw te callen.
- Robuuste parser voor de (soms dubbel-ge-escapete) JSON-blob in kolom `content`.
- Rubric §1-§8 gaat als gecachete system-prefix mee; alleen de brontekst wisselt per call.

Gebruik (bestand-gebaseerd):
    python score_trainings.py --in trainingen.xlsx --out trainingen_scored.xlsx --rubric Scoringsrubric_herschrijfbaarheid_v1.md --limit 10

Voor de kalibratiefase importeer je de functies liever vanuit een notebook (zie calibratie.ipynb).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# 1. CONFIG  --  de TUNE-knoppen staan hier bewust bovenaan
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-5"          # kalibreren op Sonnet; later evt. Opus
MAX_TOKENS = 8000
USE_WEB_SEARCH = False              # actualiteitscheck; zet uit om sneller/goedkoper te testen
WEB_SEARCH_MAX_USES = 2            # zoekopdrachten per training
RUBRIC_CUT = 8                     # RUBRIC_CUT - 1 is hoeveel secties van de rubric meegestuurd worden

# Dimensiegewichten (rubric §3). Som = 1.0
WEIGHTS = {
    "kernhelderheid":         0.15,
    "programma_substantie":   0.45,
    "leeruitkomst_orientatie": 0.20,
    "ondersteunende_secties": 0.20,
}

# Actualiteit-impact op de basisscore (rubric §4.2), als (type, severity) -> punten.
# LET OP: dit is DE kalibratieknop. Deze defaults reproduceren je 5 ijklabels binnen ~3 punten.
# - additief: bescheiden (repareerbaar met refresh)
# - structureel: kleine aftrek PLUS de harde cap <=40 (cap doet het zware werk; niet dubbeltellen)
IMPACT = {
    ("none",        "none"):   0,
    ("additief",    "none"):   0,
    ("additief",    "low"):   -1,
    ("additief",    "medium"): -6,
    ("additief",    "high"):  -13,
    ("structureel", "low"):    -3,
    ("structureel", "medium"): -6,
    ("structureel", "high"):   -8,
}
STRUCTUREEL_CAP = 40  # structurele breuk -> eindscore altijd <= dit (dun/onbruikbaar)

# Verdict-banden (rubric §2): (ondergrens, label). Aflopend gecheckt.
VERDICT_BANDS = [
    (85, "al_nieuwe_stijl"),
    (65, "rijk"),
    (45, "redelijk"),
    (25, "dun"),
    (0,  "onbruikbaar"),
]

# ---------------------------------------------------------------------------
# 2. PARSER  --  content-cel -> dict, robuust tegen enkel- én dubbel-escaping
# ---------------------------------------------------------------------------

def parse_content(cell: str) -> dict:
    """De `content`-cel is een JSON-object, soms dubbel-ge-escaped (\\\\n i.p.v. \\n).
    Strategie: strikt proberen -> één laag backslashes de-dubbelen -> salvage."""
    if cell is None:
        return {}
    if isinstance(cell, dict):
        return cell
    cell = str(cell).strip()
    if not cell:
        return {}
    for attempt in (cell, cell.replace("\\\\", "\\")):
        try:
            obj = json.loads(attempt)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    # Salvage: geef de rauwe tekst terug onder één sleutel; clean_text maakt er leesbare tekst van.
    return {"_raw": cell}


_TAG_RE = re.compile(r"<[^>]+>")
_OPLNAAM_RE = re.compile(r"\{\{\s*oplnaam\s*\}\}")
_WS_RE = re.compile(r"[ \t\u00a0]+")
_MULTINL_RE = re.compile(r"\n\s*\n\s*\n+")


def clean_text(value: Any, training_naam: str = "") -> str:
    """HTML + escapes -> leesbare platte tekst. Behandelt zowel echte newlines als
    losse letterlijke \\n / \\t tokens, HTML-entities, tags en {{ oplnaam }}."""
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False)
    s = str(value)
    # letterlijke escape-tokens die soms overblijven
    s = s.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\n")
    s = html.unescape(s)
    s = _OPLNAAM_RE.sub(training_naam or "deze training", s)
    # blok-tags -> newline zodat structuur behouden blijft; overige tags weg
    s = re.sub(r"</?(p|h[1-6]|li|ul|ol|div|br|tr)[^>]*>", "\n", s, flags=re.I)
    s = _TAG_RE.sub("", s)
    s = _WS_RE.sub(" ", s)
    s = _MULTINL_RE.sub("\n\n", s)
    return s.strip()


# top-level velden die we bewust NIET als brontekst meesturen (boilerplate/retrieval, rubric §1)
_SKIP_KEYS = {"dagen", "certification", "summary_edudex", "follow_up", "setup"}


def build_source_text(content: dict, training_naam: str) -> str:
    """Zet het (variabele) content-object om in één leesbare brontekst voor de scorer.
    Neemt géén vaste sleutels aan: loopt door wat er is."""
    parts = []
    for key, val in content.items():
        if key.startswith("_"):
            parts.append(clean_text(val, training_naam))
            continue
        if key in _SKIP_KEYS:
            continue
        cleaned = clean_text(val, training_naam)
        if cleaned:
            parts.append(f"[{key}]\n{cleaned}")
    return "\n\n".join(parts).strip()


def extract_days(content: dict, row_days: Any = None) -> int | None:
    """Dagen uit de JSON-sleutel 'dagen' (gezaghebbend), anders uit een kolomwaarde, anders None."""
    for candidate in (content.get("dagen"), row_days):
        if candidate is None or candidate == "":
            continue
        try:
            return int(float(candidate))
        except (ValueError, TypeError):
            continue
    return None


# ---------------------------------------------------------------------------
# 3. DETERMINISTISCHE REKENKERN  (geen LLM, volledig testbaar)
# ---------------------------------------------------------------------------

def basisscore(dims: dict) -> float:
    return sum(WEIGHTS[k] * float(dims[k]["score"]) for k in WEIGHTS)


def actualiteit_impact(act_type: str, severity: str) -> int:
    return IMPACT.get((act_type or "none", severity or "none"), 0)


def verdict_for(score: float) -> str:
    for lo, label in VERDICT_BANDS:
        if score >= lo:
            return label
    return "onbruikbaar"


_DIM_KEYS = ("kernhelderheid", "programma_substantie",
             "leeruitkomst_orientatie", "ondersteunende_secties")

def tool_input_complete(inp: dict) -> tuple[bool, str]:
    """Controleert of een submit_score-tool_input compleet genoeg is om te scoren.
    Vangt truncatie op (bv. door max_tokens) vóór we in finalize_scores duiken."""
    if not isinstance(inp, dict):
        return False, "tool-input is geen object"
    dims = inp.get("dimensies")
    if not isinstance(dims, dict):
        return False, "'dimensies' ontbreekt (waarschijnlijk afgekapt door max_tokens)"
    for k in _DIM_KEYS:
        d = dims.get(k)
        if not isinstance(d, dict) or not isinstance(d.get("score"), (int, float)):
            return False, f"dimensie '{k}' ontbreekt of heeft geen score"
    return True, ""

def finalize_scores(model_out: dict) -> dict:
    """Neemt de LLM-oordelen en berekent basisscore, impact, eindscore, verdict, cap-vlag."""
    dims = model_out["dimensies"]
    act = model_out.get("actualiteit", {}) or {}
    act_type = act.get("type", "none")
    severity = act.get("severity", "none")

    base = basisscore(dims)
    impact = actualiteit_impact(act_type, severity)
    eind = base + impact
    eind = max(0.0, min(100.0, eind))

    menselijke_input = bool(model_out.get("menselijke_input_nodig", False))
    if act_type == "structureel":
        eind = min(eind, STRUCTUREEL_CAP)
        menselijke_input = True  # structurele breuk gaat altijd langs een mens

    eind_int = int(round(eind))
    return {
        "basisscore": round(base, 1),
        "actualiteit_impact": impact,
        "eindscore": eind_int,
        "verdict": verdict_for(eind_int),
        "menselijke_input_nodig": menselijke_input,
    }


# ---------------------------------------------------------------------------
# 4. HET SCORING-TOOL  (dwingt de JSON-structuur + toegestane waarden af)
# ---------------------------------------------------------------------------

_COVERAGE_ENUM = ["aanwezig", "gedeeltelijk", "afleidbaar", "afwezig"]

def _dim(desc: str) -> dict:
    return {
        "type": "object",
        "properties": {
            "score": {"type": "integer", "minimum": 0, "maximum": 100, "description": desc},
            "toelichting": {"type": "string"},
        },
        "required": ["score", "toelichting"],
    }

SUBMIT_TOOL = {
    "name": "submit_score",
    "description": "Lever het scoringsoordeel voor deze training. Geef GEEN basisscore of eindscore "
                   "-- die berekent de code. Vul alleen de dimensiescores, actualiteit en vlaggen in.",
    "input_schema": {
        "type": "object",
        "properties": {
            "kern": {"type": "string", "description": "1-2 zinnen: onderwerp + praktijkwaarde uit de bron."},
            "vermoedelijk_persona": {"type": "string", "enum": ["A", "B", "C"]},
            "aantal_dagen_bron": {"type": ["integer", "null"]},
            "dagen_bron_herkomst": {"type": "string", "enum": ["expliciet", "geschat"]},
            "dimensies": {
                "type": "object",
                "properties": {
                    "kernhelderheid": _dim("15% -- helderheid onderwerp/waarde"),
                    "programma_substantie": _dim("45% -- BEOORDEEL RELATIEF AAN AANTAL DAGEN"),
                    "leeruitkomst_orientatie": _dim("20% -- straf tool-achtergrond-ballast af"),
                    "ondersteunende_secties": _dim("20% -- doelgroep/voorkennis/doelen; aanwezig>afleidbaar>afwezig"),
                },
                "required": ["kernhelderheid", "programma_substantie",
                             "leeruitkomst_orientatie", "ondersteunende_secties"],
            },
            "actualiteit": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["none", "low", "medium", "high"]},
                    "type": {"type": "string", "enum": ["none", "additief", "structureel"]},
                    "samenvatting": {"type": "string"},
                    "specifiek": {"type": "array", "items": {"type": "string"}},
                    "actie_voor_rewriter": {"type": "string",
                                            "description": "additief -> 'refresh: ...'; structureel -> 'BESLISSING NODIG: ...'"},
                },
                "required": ["severity", "type", "samenvatting", "specifiek", "actie_voor_rewriter"],
            },
            "bruikbaar": {"type": "array", "items": {"type": "string"}},
            "strippen": {"type": "array", "items": {"type": "string"}},
            "gaten": {"type": "array", "items": {"type": "string"}},
            "rewrite_guidance": {"type": "string"},
            "menselijke_input_nodig": {"type": "boolean"},
            "menselijke_input_wat": {"type": "string"},
            "scorer_confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["kern", "vermoedelijk_persona", "aantal_dagen_bron", "dagen_bron_herkomst",
                     "dimensies", "actualiteit", "sectie_dekking", "bruikbaar", "strippen",
                     "gaten", "rewrite_guidance", "menselijke_input_nodig", "scorer_confidence"],
    },
}


# ---------------------------------------------------------------------------
# 5. PROMPT  --  gecachete rubric-prefix + korte werkinstructie
# ---------------------------------------------------------------------------

def load_rubric_prefix(rubric_path: str, cut_section: int = RUBRIC_CUT) -> str:
    """Leest de rubric-md en knipt alles vóór '## **{cut_section}' eruit."""
    with open(rubric_path, encoding="utf-8") as f:
        text = f.read()
    cut = re.search(rf"^##\s*\*\*{cut_section}", text, flags=re.M)
    return text[:cut.start()].strip() if cut else text.strip()


INSTRUCTIE = """\
Je scoort een OUDE trainingsbeschrijving op HERSCHRIJFBAARHEID: hoeveel bruikbaar,
correct-georiënteerd materiaal er in de bron zit om er automatisch een volwaardige
training in de nieuwe stijl van te maken. Je scoort NIET hoe goed de pagina nu is --
toon, format en marketing repareert de herschrijver sowieso.

Werkwijze:
1. Lees de brontekst. Bepaal de kern, het aantal dagen en de vermoedelijke persona (A/B/C).
   Is het aantal dagen als bekend meegegeven, gebruik dat en zet dagen_bron_herkomst=expliciet.
   Anders schat je het plausibel uit inhoud + titel en zet je dagen_bron_herkomst=geschat.
2. Scoor de vier dimensies 0-100 met de verankerde niveaubeschrijvingen uit de rubric.
   Programma-substantie beoordeel je RELATIEF aan het aantal dagen en het type training (bijv. foundations of beginner); straf tool-achtergrond-ballast af.
3. Beoordeel actualiteit. Zoek zo nodig het onderwerp op (web search) om deprecatie/versie-status
   vast te stellen. Bepaal severity (none/low/medium/high) en type (none/additief/structureel).
   Additief = repareerbaar met refresh; structureel = vraagt een menselijke inhoudelijke beslissing.
4. Schrijf VOORUITGERICHTE feedback voor de herschrijver (bruikbaar / strippen / gaten /
   rewrite_guidance) en de sectie-dekkingslabels.

BELANGRIJK: bereken ZELF GEEN basisscore of eindscore -- dat doet de code op basis van jouw
dimensiescores en actualiteitsoordeel. Roep tot slot het tool `submit_score` aan met je oordeel.

Kalibratie-ankers: React 30 (structureel), XSL 40 (structureel),
Google Ads 65 (additief-hoog), CRM 69 (additief-laag), LDAP 68 (additief-laag).
"""


def build_system(rubric_prefix: str) -> list[dict]:
    """System-blok met cache_control op de vaste prefix (identiek voor alle ~1000 trainingen)."""
    return [{
        "type": "text",
        "text": INSTRUCTIE + "\n\n---\n\n" + rubric_prefix,
        "cache_control": {"type": "ephemeral"},
    }]


def build_user(training_naam: str, source_text: str, known_days: int | None) -> str:
    dagen = str(known_days) if known_days is not None else "ONBEKEND (schat zelf, herkomst=geschat)"
    return (f"Titel: {training_naam}\n"
            f"Bekend aantal dagen: {dagen}\n\n"
            f"Brontekst:\n{source_text}")


# ---------------------------------------------------------------------------
# 6. API-CALL  (web search server-side; submit_score client-side)
# ---------------------------------------------------------------------------

@dataclass
class ScoreResult:
    training_id: Any
    titel: str
    ok: bool
    model_out: dict = field(default_factory=dict)
    computed: dict = field(default_factory=dict)
    source_chars: int = 0
    error: str = ""

    @property
    def record(self) -> dict:
        """Platgeslagen dict, klaar voor één rij in de output-sheet."""
        m, c = self.model_out, self.computed
        dims = m.get("dimensies", {})
        act = m.get("actualiteit", {})
        dek = m.get("sectie_dekking", {})

        def g(d, *ks):
            for k in ks:
                d = (d or {}).get(k, {}) if isinstance(d, dict) else {}
            return d

        rec = {
            "training_id": self.training_id,
            "titel": self.titel,
            "ok": self.ok,
            "error": self.error,
            "kern": m.get("kern", ""),
            "vermoedelijk_persona": m.get("vermoedelijk_persona", ""),
            "aantal_dagen_bron": m.get("aantal_dagen_bron"),
            "dagen_bron_herkomst": m.get("dagen_bron_herkomst", ""),
            "kernhelderheid_score": (dims.get("kernhelderheid") or {}).get("score"),
            "programma_score": (dims.get("programma_substantie") or {}).get("score"),
            "leeruitkomst_score": (dims.get("leeruitkomst_orientatie") or {}).get("score"),
            "ondersteunend_score": (dims.get("ondersteunende_secties") or {}).get("score"),
            "basisscore": c.get("basisscore"),
            "actualiteit_severity": act.get("severity", ""),
            "actualiteit_type": act.get("type", ""),
            "actualiteit_impact": c.get("actualiteit_impact"),
            "actualiteit_samenvatting": act.get("samenvatting", ""),
            "actualiteit_specifiek": " | ".join(act.get("specifiek", []) or []),
            "actualiteit_actie": act.get("actie_voor_rewriter", ""),
            "eindscore": c.get("eindscore"),
            "verdict": c.get("verdict", ""),
        }
        rec.update({
            "bruikbaar": " | ".join(m.get("bruikbaar", []) or []),
            "strippen": " | ".join(m.get("strippen", []) or []),
            "gaten": " | ".join(m.get("gaten", []) or []),
            "rewrite_guidance": m.get("rewrite_guidance", ""),
            "menselijke_input_nodig": c.get("menselijke_input_nodig", m.get("menselijke_input_nodig")),
            "menselijke_input_wat": m.get("menselijke_input_wat", ""),
            "scorer_confidence": m.get("scorer_confidence", ""),
        })
        return rec

def _extract_tool_input(response) -> dict | None:
    for block in response.content:
        if getattr(block, "type", None) == "tool_use" and block.name == "submit_score":
            return block.input
    return None

def _attempt(client, model, system, messages, tools, max_tokens):
    """Eén poging: geef (tool_input, stop_reason, resp) terug. tool_input kan None zijn."""
    for _ in range(4):  # marge voor eventuele extra tool-ronden
        resp = client.messages.create(
            model=model, max_tokens=max_tokens,
            system=system, messages=messages, tools=tools,
        )
        tool_input = _extract_tool_input(resp)
        if tool_input is not None:
            return tool_input, resp.stop_reason, resp
        if resp.stop_reason != "tool_use":
            return None, resp.stop_reason, resp
        # tool gebruikt zonder submit_score (onwaarschijnlijk) -> resultaat terugvoeren en doorgaan
        messages = messages + [{"role": "assistant", "content": resp.content}]
    return None, resp.stop_reason, resp

def score_one(client, training_id, training_naam: str, source_text: str,
              known_days: int | None, rubric_prefix: str,
              model: str = MODEL, use_web_search: bool = USE_WEB_SEARCH,
              max_tokens: int = MAX_TOKENS) -> ScoreResult:
    tools: list[dict] = [SUBMIT_TOOL]
    if use_web_search:
        tools.append({
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": WEB_SEARCH_MAX_USES,
        })
 
    system = build_system(rubric_prefix)
    messages = [{"role": "user", "content": build_user(training_naam, source_text, known_days)}]
 
    try:
        budget = max_tokens
        last_reason = None
        for attempt_nr in range(2):  # 2e poging met dubbel budget bij afkapping/onvolledigheid
            tool_input, stop_reason, _ = _attempt(client, model, system, messages, tools, budget)
            last_reason = stop_reason
            if tool_input is None:
                if stop_reason == "max_tokens":       # afgekapt vóór de tool -> meer budget
                    budget *= 2
                    continue
                break                                  # andere reden: niet zinvol te herproberen
            complete, why = tool_input_complete(tool_input)
            if complete:
                computed = finalize_scores(tool_input)
                return ScoreResult(training_id, training_naam, True,
                                   model_out=tool_input, computed=computed,
                                   source_chars=len(source_text))
            # tool wél aangeroepen maar onvolledig (bv. dimensies afgekapt) -> retry met meer budget
            budget *= 2
            last_reason = f"onvolledige tool-output: {why} (stop_reason={stop_reason})"
        return ScoreResult(training_id, training_naam, False,
                           error=f"Geen bruikbare submit_score na 2 pogingen ({last_reason}).")
    except Exception as e:  # noqa: BLE001
        return ScoreResult(training_id, training_naam, False, error=f"{type(e).__name__}: {e}")
 

def make_client():
    """Lazy import zodat de rekenkern zonder anthropic/API-key te testen is."""
    import anthropic
    return anthropic.Anthropic()  # leest ANTHROPIC_API_KEY uit de omgeving


# ---------------------------------------------------------------------------
# 7. I/O  --  xlsx in, xlsx uit (bestand-gebaseerd; geen Google-toegang nodig)
# ---------------------------------------------------------------------------

ID_CANDIDATES = ["id", "training_id", "trainingid"]
NAME_CANDIDATES = ["name", "naam", "titel", "title"]
CONTENT_CANDIDATES = ["content", "inhoud"]
DAYS_CANDIDATES = ["dagen", "days", "aantal_dagen", "duur"]


def _find_col(df, candidates):
    lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand in lower:
            return lower[cand]
    return None


def read_input(path: str):
    import pandas as pd
    df = pd.read_excel(path) if path.lower().endswith((".xlsx", ".xls")) else pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    name_col = _find_col(df, NAME_CANDIDATES)
    content_col = _find_col(df, CONTENT_CANDIDATES)
    if name_col is None or content_col is None:
        raise ValueError(f"Kon 'name'/'content'-kolommen niet vinden. Gevonden: {list(df.columns)}")
    id_col = _find_col(df, ID_CANDIDATES)
    if id_col is None:
        first = df.columns[0]  # eerste kolom is vaak het id zonder header
        id_col = first if first not in (name_col, content_col) else None
    days_col = _find_col(df, DAYS_CANDIDATES)
    return df, {"id": id_col, "name": name_col, "content": content_col, "days": days_col}


def run_file(in_path: str, out_path: str, rubric_path: str,
             limit: int | None = None, use_web_search: bool = USE_WEB_SEARCH,
             model: str = MODEL, verbose: bool = True):
    import pandas as pd
    df, cols = read_input(in_path)
    if limit:
        df = df.head(limit)
    rubric_prefix = load_rubric_prefix(rubric_path)
    client = make_client()

    records = []
    for i, row in df.iterrows():
        tid = row[cols["id"]] if cols["id"] else i
        naam = str(row[cols["name"]])
        content = parse_content(row[cols["content"]])
        known_days = extract_days(content, row[cols["days"]] if cols["days"] else None)
        source_text = build_source_text(content, naam)
        res = score_one(client, tid, naam, source_text, known_days,
                        rubric_prefix, model=model, use_web_search=use_web_search)
        if verbose:
            status = f"{res.computed.get('eindscore')} {res.computed.get('verdict')}" if res.ok else f"FOUT: {res.error}"
            print(f"[{i+1}/{len(df)}] {naam[:45]:45} -> {status}")
        records.append(res.record)

    out = pd.DataFrame.from_records(records)
    out.to_excel(out_path, index=False)
    if verbose:
        print(f"\nGeschreven: {out_path}  ({len(out)} rijen)")
    return out


def main():
    from dotenv import load_dotenv
    load_dotenv()
    p = argparse.ArgumentParser(description="Scoor trainingen op herschrijfbaarheid.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--rubric", dest="rubric_path", default="Scoringsrubric_herschrijfbaarheid_v1.md")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--no-web-search", action="store_true")
    p.add_argument("--model", default=MODEL)
    a = p.parse_args()
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit("Zet ANTHROPIC_API_KEY (in een .env-bestand of je omgeving).")
    run_file(a.in_path, a.out_path, a.rubric_path,
             limit=a.limit, use_web_search=not a.no_web_search, model=a.model)


if __name__ == "__main__":
    main()
