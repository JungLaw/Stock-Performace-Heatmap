# TA Rule Engine Project — Canonical End-to-End Outline
- Version: 3.0 
- Created: 1/12/26
- Last update: 1/12/26 @ 435P

**(Authoritative, Corrected, Chronological, Single Source)**

---

## MAJOR PHASE I — Core Data & Indicator Foundation (Numbers)

**Goal:** Produce stable, correct, and reproducible indicator time series with canonical naming, predictable dtypes, and known numerical semantics.

### 1. Data acquisition & normalization

* OHLCV retrieval (daily semantics)
* Trading-calendar correctness (“last completed trading day” logic)
* DB caching with deterministic fallback (e.g., yfinance)
* Canonical index alignment and dtype normalization

### 2. Option A — Baseline indicators (price-driven)

* RSI, ROC, Williams %R, Stochastic
* Canonical column naming
* No rule semantics yet; numeric correctness only

### 3. Option B — Volume-aware indicators

* MFI, CMF, OBV
* Explicit daily-volume assumptions
* Guardrails for intraday usage
* Local implementations where third-party libraries prove unstable

### 4. Option C — Expanded indicator inventory

* EMA, HMA, ADX, CCI, Ultimate Oscillator (multi-parameter families)
* Parameter-instance normalization (e.g., `UO_7_14_28`)
* `indicator_preprocessor.py` as the canonical computation wrapper


**Deferred but canonically named Bollinger-derived outputs**

The following Bollinger-derived numeric outputs are canonically named now,
but computation and rule usage are deferred:

- Bollinger %B → `BB_PCT_B`
- Bollinger Bandwidth → `BB_BW`

**Status:**
- Naming is locked to prevent future churn.
- Computation, semantics, and UI exposure are deferred until:
  - Option E (numeric derivation) and
  - Option F (band-position semantics) are explicitly activated.


### 5. Required detour — pandas dtype & stability fixes

**Why it mattered:** pandas-ta and legacy dtype assumptions caused silent corruption and FutureWarnings that became runtime failures.

* Stable float64 enforcement for volume series
* Removal / replacement of fragile third-party paths
* Elimination of dtype mutation warnings that break Streamlit runs

**Status:**
✅ Phase I is **complete**.
Known non-blocking issues: pandas fragmentation/performance warnings.

---

## MAJOR PHASE II — Signal & Rule Infrastructure (Meaning / Scoring)

**Goal:** Convert numeric indicator outputs into consistent, rule-evaluable signals and rolling scores.

### 6. Rulebook ingestion & normalization

* `master_rules_normalized.json`
* Deterministic rule loading & validation
* Scope-aware rule segmentation (heatmap / overlay / alerts)

### 7. Option D — Rule inventory & scope locking

* Indicator families enumerated
* Explicit scope definitions
* Deferred semantics documented (no silent expansion)

**Status:** ✅ Completed earlier

### 8. Rule execution engine

* Expression engine (DSL)
* Signal classifier (`-2 .. +2`)
* Rolling-window score packaging
* Instance binding for multi-parameter indicators (e.g., UO)


**Rule-evaluation correctness checkpoint — ROC unit normalization**
- Validate that ROC_* numeric series units match the thresholds defined in
  `master_rules_normalized.json`.
- Current risk: ROC series are emitted in **percent-point units**
  (e.g., `ROC_20 = 6.34` meaning +6.34%), while rule thresholds are written
  in **fractional units** (e.g., `0.03` meaning +3%).
- This mismatch causes ROC rules to over-score as `buy` / `strong_buy`
  across most positive values.

**Resolution rule (authoritative):**
- Either:
  1) Normalize ROC series to fractional units (`ROC = ROC / 100`), **or**
  2) Rewrite ROC rule thresholds to percent-point units.

Decision to be made once and applied globally; mixed-unit handling is prohibited.

**Acceptance criteria:**
- ROC_12 / ROC_20 signals must transition correctly across
  neutral / buy / sell boundaries when replayed against historical data.

### 9. Option E — Derived numeric primitives (**NOT semantics**)

**Purpose:** Provide reusable numeric transforms that other layers depend on.

Examples:

* Slopes (EMA/HMA/ADX)
* Deltas / ROC-of-indicators
* Volatility normalization
* Distance-to-band (numeric only)

> ⚠️ Important boundary:
> Option E produces **numbers**, not interpretations.


#### Option E Task Class — Numeric Deviation & Normalization (Explicit)

**Definition (Option E):** Numeric deviation work defines or corrects **pure numeric transforms** such as units, scaling, normalization, and derived series. It must not introduce buy/sell meaning or thresholds beyond unit alignment.

Numeric deviation tasks may be initiated by UI discrepancies or rule-evaluation mismatches but must be resolved entirely within Option E before any semantic interpretation occurs.

**In-scope examples (Option E):**
- Unit normalization (percent vs fractional, basis points vs percent points)
- Derived numeric series (slopes, deltas, ratios, z-scores)
- Band-derived numeric series (e.g., Bollinger %B and bandwidth)
- Numeric distance-to-band series (raw and normalized)
- Volatility normalization primitives (numeric only)

**Out of scope (Option E):**
- Any semantic interpretation of numeric values (belongs to Option F)
- Any UI formatting or display-only transforms (belongs to Phase III)


### 10. Option F — Semantic & relational logic

**Purpose:** Interpret numbers.

Examples:

* Band position meaning
* Cross-confirmation logic
* Regime classification
* Composite signals

**Status (Phase II overall):**

* Rule infrastructure exists and is operational
* Option D closed
* Option E & F are **intentionally incomplete**, pending UI-driven confirmation

---

## MAJOR PHASE III — Visualization & Interaction Layer (UI)

**Goal:** Make engine outputs visible, explorable, and trustworthy **without redefining the math**.

### 11. Rolling signal heatmap (primary UI driver)

* Rule-engine rolling scores
* Indicator-instance rows
* Time-indexed columns
* Stable adapter contract
* Group selection (custom tickers, ETFs, etc.)


**Rolling Heatmap UX Milestone — Layout & Semantics (UI-only)**

**Must-haves (Phase III, blocking for usability):**
- Dates rendered at the **top** of the heatmap.
- Date format normalized to `M/D` (e.g., `12/24 … 1/7`).
- Add a **Price row** directly under dates:
  - Row label = ticker symbol (fallback: `Price`)
  - Cell format = `$X,XXX.XX`
  - Price source must be the same canonical close series used by indicators.
- Enforce consistent column widths across all dates.
- Persist indicator row order across reruns
  (no forced re-selection to preserve ordering).

**Nice-to-haves (Phase III, explicitly optional):**
- Hover enrichment for Price row:
  - absolute change vs prior day
  - % change vs prior day
  - raw volume
  - volume vs trailing average
- Optional date-range selector:
  - user chooses start date
  - heatmap renders next *N* completed trading days
  - must not introduce new rule semantics.


### 12. Technical Analysis dashboard (tiles)

* Secondary view
* Feature-flag controlled
* Must not mutate rule semantics

### **Formal Feedback Loop (Governed)**

UI is allowed to:

* Reveal missing numeric primitives
* Expose naming or binding gaps
* Surface usability constraints

UI is **not** allowed to:

* Invent semantics
* Patch numeric logic locally
* Diverge from engine outputs

Any gap discovered becomes:

* Option E task (numeric)
* or Option F task (semantic)

**Status:**
🟡 Phase III is **in progress**.
Rolling heatmap core is functional and validated.

---

## MAJOR PHASE IV — Semantic Presentation & Decision Support

**Goal:** Explain *why* signals exist, not just show them.

* Natural-language explanations
* Rule rationale panels
* Composite signal narratives
* User-facing decision support

**Depends on:**
Stable completion of Option E + Option F.

---

## Design-Level Decisions (Explicit, Non-Negotiable)

### SMA Exclusion — Rationale (Authoritative)

SMA is **intentionally excluded** at this stage because:

1. **Numerically redundant** with EMA/HMA for current goals
2. **Lag-heavy**, adds little signal value in rolling heatmap context
3. Increases cognitive and UI clutter
4. Slopes/deltas (Option E) are better applied to EMA/HMA
5. SMA inclusion is a **Phase IV or later** decision, justified only if:

   * a semantic use case emerges
   * or SMA is required for external compatibility

This is a **design choice**, not a missing feature.

---

## Canonical Path Selection (Resolved)

### ❌ Path B — Phase II-first (Option E first)

* Deferred
* To be revisited only when UI requirements stabilize

### ✅ Path A — Phase III-first (**Canonical**)

* Rolling heatmap UX refinement
* Tight feedback loop into Option E
* No speculative numeric expansion

This is now the **official project path**.

---

## Current Project State (Snapshot)

* Phase I: ✅ Complete
* Phase II:

  * Core engine: ✅
  * Option D: ✅
  * Option E/F: ⏸️ gated
* Phase III:

  * Rolling heatmap: 🟡 active
  * Layout & semantics: next
* Phase IV: 🔒 future

---

## What Comes Next (Immediately)

**Next active workstream:**

> **Redesign the rolling heatmap layout and semantics**

Only after that:

* Option E backlog formalization
* Phase II continuation
