"""Offline tests voor de deterministische rekenkern en de parser (geen API nodig).
Draai:  python test_scoring.py
"""
from score_trainings import (
    finalize_scores, parse_content, clean_text, build_source_text, extract_days,
)

def _dims(k, p, l, o):
    return {
        "kernhelderheid": {"score": k, "toelichting": ""},
        "programma_substantie": {"score": p, "toelichting": ""},
        "leeruitkomst_orientatie": {"score": l, "toelichting": ""},
        "ondersteunende_secties": {"score": o, "toelichting": ""},
    }

# (naam, dims, actualiteit_type, severity, verwachte eindscore uit rubric §9)
ANKERS = [
    ("React",      _dims(75, 20, 35, 60), "structureel", "high", 30),
    ("XSL",        _dims(75, 40, 35, 50), "structureel", "high", 40),
    ("Google Ads", _dims(85, 75, 80, 80), "additief",    "high", 65),
    ("CRM",        _dims(85, 72, 65, 55), "additief",    "low",  69),
    ("LDAP",       _dims(85, 68, 60, 55), "additief",    "low",  68),
]

def test_ankers(tolerantie=6):
    print("=== IJklabels reproduceren (tolerantie ±%d) ===" % tolerantie)
    ok = True
    for naam, dims, atype, sev, target in ANKERS:
        out = finalize_scores({
            "dimensies": dims,
            "actualiteit": {"type": atype, "severity": sev},
            "menselijke_input_nodig": False,
        })
        delta = abs(out["eindscore"] - target)
        flag = "OK " if delta <= tolerantie else "!! "
        struct = " [mens-vlag]" if out["menselijke_input_nodig"] else ""
        print(f"  {flag}{naam:11} basis={out['basisscore']:5} impact={out['actualiteit_impact']:>4} "
              f"-> eind={out['eindscore']:3} ({out['verdict']}) | label {target} (Δ{delta}){struct}")
        ok = ok and delta <= tolerantie
    print("  RESULTAAT:", "GESLAAGD" if ok else "GEZAKT")
    return ok

def test_parser():
    print("\n=== Parser: dubbel-ge-escapete cel ===")
    cell = '{"dagen": 5, "intro": "<p>\\\\n\\\\tPHP commando\u2019s\\\\n<a href=\\\\"/course/x\\\\">x</a></p>", "objectives": ""}'
    obj = parse_content(cell)
    assert obj.get("dagen") == 5, "dagen niet gelezen"
    assert extract_days(obj) == 5
    txt = build_source_text(obj, "Cursus PHP")
    print("  keys:", list(obj))
    print("  brontekst:", repr(txt[:80]))
    assert "commando\u2019s" in txt, "curly quote verloren"
    assert "<" not in txt and "{{" not in txt, "tags/placeholder niet geschoond"
    print("  OK: dagen gelezen, tekst geschoond, curly quote intact")
    return True

if __name__ == "__main__":
    a = test_ankers()
    b = test_parser()
    raise SystemExit(0 if (a and b) else 1)
