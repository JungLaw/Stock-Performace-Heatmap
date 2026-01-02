import json
import re
from pathlib import Path
from collections import defaultdict


RULEBOOK_PATH = Path("src/config/master_rules_normalized.json")
PREPROC_PATH = Path("src/calculations/indicator_preprocessor.py")
CLASSIFIER_PATH = Path("src/calculations/signal_classifier.py")

KEYWORDS = {"and", "or", "not", "True", "False"}

RAW_INPUTS = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}

def walk_json(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_json(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_json(v, path + (str(i),))
    elif isinstance(obj, str):
        yield (".".join(path), obj)

def extract_heatmap_expressions(rulebook: dict):
    exprs = []
    for p, s in walk_json(rulebook):
        if ".feature_scopes.heatmap." in p and not p.endswith(".notes") and s.strip():
            exprs.append((p, s.strip()))
    return exprs

def tokenize(expr: str):
    funcs = set()
    vars_ = set()
    for m in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expr):
        tok = m.group(0)
        if tok in KEYWORDS:
            continue
        if expr[m.end():m.end()+1] == "(":
            funcs.add(tok)
        else:
            vars_.add(tok)
    return vars_, funcs

def preprocessor_emission_patterns(preproc_text: str):
    # literal df["X"] = ...
    literal = set(re.findall(r"df\[(?:'|\")([^'\"]+)(?:'|\")\]\s*=", preproc_text))

    # f-strings: df[f"...{x}..."] = ...
    f_pats = set(re.findall(r"df\[\s*f(?:'|\")([^'\"]+)(?:'|\")\s*\]\s*=", preproc_text))

    def pat_to_regex(pat: str):
        # allow {prefix} to stand for MACD_12_26_9 etc.
        pat = re.sub(r"\{prefix\}", lambda _m: r"(?:[A-Za-z][A-Za-z0-9_]*)", pat)

        # other {x} slots → digits or digit tuples
        pat = re.sub(r"\{[^}]*\}", lambda _m: r"(?:\d+(?:_\d+)*)", pat)

        return re.compile("^" + pat + "$")


    regexes = [pat_to_regex(p) for p in f_pats]

    def is_emittable(token: str) -> bool:
        if token in literal:
            return True
        return any(r.match(token) for r in regexes)

    return is_emittable

def classifier_context_aliases(classifier_text: str):
    # currently we know it aliases close := Close (if present)
    aliases = {}
    if "context[\"close\"]" in classifier_text and "context[\"Close\"]" in classifier_text:
        aliases["close"] = "Close"
    return aliases

def main():
    rulebook = json.loads(RULEBOOK_PATH.read_text())
    preproc_text = PREPROC_PATH.read_text()
    classifier_text = CLASSIFIER_PATH.read_text()

    exprs = extract_heatmap_expressions(rulebook)

    token_paths = defaultdict(list)
    token_examples = defaultdict(list)

    all_vars = set()
    all_funcs = set()

    for p, e in exprs:
        vars_, funcs = tokenize(e)
        all_vars |= vars_
        all_funcs |= funcs
        for t in vars_:
            token_paths[t].append(p)
            if len(token_examples[t]) < 3:
                token_examples[t].append(e)

    is_emittable = preprocessor_emission_patterns(preproc_text)
    aliases = classifier_context_aliases(classifier_text)

    rows = []
    for t in sorted(all_vars):
        emitted = (t in RAW_INPUTS) or is_emittable(t)
        available = emitted or (t in aliases)

        # classify gap
        if available:
            gap = "OK"
            fix = ""
        else:
            # parameter-alias candidates (bare tokens used in normalized expressions)
            if t in {"CCI"} or re.match(r"MACD_\d+_\d+_\d+$", t):
                gap = "NEEDS_PARAM_ALIAS"
                fix = "context_alias"
            elif re.match(r"(EMA|SMA)_\d+_\\d+$", t):
                gap = "NEEDS_DF_ALIAS"
                fix = "df_alias"
            elif t.endswith("_slope") or t in {"VWMA_slope", "HMA_slope"}:
                gap = "MISSING_DERIVED_EMISSION"
                fix = "derived"
            elif re.match(r"(VWMA|HMA)_", t):
                gap = "MISSING_BASE_EMISSION"
                fix = "compute"
            else:
                gap = "NORMALIZER_FIX_CANDIDATE"
                fix = "normalizer_or_alias"

        rows.append({
            "token": t,
            "required_by_rulebook": True,
            "emitted_by_preprocessor": emitted,
            "available_in_context": available,
            "gap_type": gap,
            "recommended_fix": fix,
            "example_paths": " | ".join(token_paths[t][:3]),
            "example_expr": " | ".join(token_examples[t][:2]),
        })

    out = Path("contract_audit_report.csv")
    import csv
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {out} with {len(rows)} tokens.")
    print("Top gaps:", {g: sum(1 for r in rows if r["gap_type"] == g) for g in sorted({r['gap_type'] for r in rows})})

if __name__ == "__main__":
    main()
