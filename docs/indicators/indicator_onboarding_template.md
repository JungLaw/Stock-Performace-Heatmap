# Indicator Onboarding Template — Rolling Heatmap / Indicator Definitions
Date: 4/8/26

## 0) Request Summary
- **Indicator family:** 
- **Parameter(s):** 
- **Canonical row key(s):** 
- **Goal:** 
  - [ ] Add to rolling heatmap only
  - [ ] Add to Indicator Definitions only
  - [ ] Add full rule/scoring support
  - [ ] Add Learn More doc
- **In scope under current project locks?**
  - [ ] Yes
  - [ ] No
  - [ ] Need confirmation


---


## 1) Scope / Phase Check
### A. Scope status
- **Current phase / workstream:** 
- **Is this indicator family deferred or excluded?**
  - [ ] No
  - [ ] Yes → stop and reopen scope first

### B. Notes
- Relevant deferral / scope notes:
- If blocked, why:


---


## 2) Indicator Type
- [ ] Existing indicator already computed
- [ ] Existing indicator already scored
- [ ] New computed indicator
- [ ] New scored indicator
- [ ] Display-only indicator
- [ ] Educational-content-only addition

### Expected behavior
- **Should it have values in the heatmap?**
  - [ ] Yes
  - [ ] No
- **Should it have buy/sell/neutral scores?**
  - [ ] Yes
  - [ ] No
- **Should it appear in Indicator Definitions?**
  - [ ] Yes
  - [ ] No
- **Should it have Learn More markdown?**
  - [ ] Yes
  - [ ] No


---


## 3) Numeric Layer Check
**Primary file:** `indicator_preprocessor.py`

### A. Computation status
- **Does the numeric series already exist?**
  - [ ] Yes
  - [ ] No

### B. Canonical column names
- Primary value column:
- Related columns / extras:
- Notes on naming:

### C. If new computation is required
- Function / section to update:
- Dependencies:
- Risks:


---


## 4) Rule / Semantic Layer Check
**Primary file:** `master_rules_normalized.json`

### A. Scoring required?
- [ ] Yes
- [ ] No

### B. If yes
- Indicator family key in rulebook:
- Param key(s):
- Feature scope(s):
  - [ ] heatmap
  - [ ] overlay
  - [ ] alerts
  - [ ] custom

### C. Rule coverage
- [ ] strong_buy
- [ ] buy
- [ ] neutral
- [ ] sell
- [ ] strong_sell
- [ ] notes

### D. Naming alignment check
- Rule expressions match computed column names?
  - [ ] Yes
  - [ ] No

### E. Supporting files to inspect
- `signals_loader.py`
- `signal_classifier.py`
- `expression_engine.py`

Notes:
- 


---


## 5) Rolling Heatmap Row Identity
**Primary file:** `technical.py`
**Function:** `_get_optionc_meta()`

### A. Add / confirm row entry
- [ ] engine_indicator
- [ ] param_key
- [ ] display_key
- [ ] value_col
- [ ] extra_value_cols (if needed)

### B. Canonical row key(s)
- Row key 1:
- Row key 2:
- Row key 3:

### C. Questions
- Does the row key exactly match downstream UI metadata key?
  - [ ] Yes
  - [ ] No

Notes:
- 


---


## 6) UI Metadata Layer
**Primary file:** `rolling_heatmap_adapter.py`
**Variable:** `INDICATOR_DEFS`

### A. Add / confirm row-level metadata
- [ ] display_name
- [ ] definition
- [ ] how_to_read

### B. Exact key used in `INDICATOR_DEFS`
- 

### C. Notes
- Is this row-specific or family-level content?
- Any risk of duplicating family-level content here?


---


## 7) Family / Doc Mapping
**Primary file:** `rolling_heatmap_adapter.py`

### A. Family resolver
**Function:** `get_indicator_family(row_key: str)`

- [ ] Family mapping exists
- [ ] Family mapping is correct

### B. Doc slug resolver
**Function:** `get_indicator_doc_slug(row_key: str)`

- [ ] Doc slug matches family
- [ ] Doc slug intentionally differs from family

### C. Expected family/doc slug
- Family:
- Doc slug:


---


## 8) Learn More Documentation
**Primary location:** `docs/indicators/`

### A. Markdown file
- [ ] Exists
- [ ] Not needed
- [ ] To be added later

### B. Expected path
- `docs/indicators/<DOC_SLUG>.md`

### C. Content guidance
- [ ] Family-level only
- [ ] Educational only
- [ ] No rule-threshold semantics
- [ ] No date-specific commentary

### D. Suggested sections
- [ ] What it is
- [ ] Why traders use it
- [ ] Common interpretations
- [ ] Limitations
- [ ] Use with
- [ ] Common mistakes


---


## 9) Streamlit UI Integration
**Primary file:** `streamlit_app.py`

### A. Should it appear in Indicator Definitions?
- [ ] Yes
- [ ] No

### B. Learn More support
- [ ] Nested expander should appear if markdown exists
- [ ] No markdown needed

### C. Default selection
- [ ] Add to default selected indicators
- [ ] Leave available but not selected by default

### D. Related locations
- Rolling Signal Heatmap indicator selection
- Indicator Definitions expander
- Learn More nested expander


---


## 10) Verification Checklist

### A. Numeric verification
- [ ] Column exists in computed dataframe
- [ ] Values look correct
- [ ] No naming mismatch

### B. Heatmap verification
- [ ] Row appears in heatmap
- [ ] Row key is correct
- [ ] Value formatting is correct
- [ ] Hover works correctly

### C. Scoring verification (if applicable)
- [ ] Scores populate
- [ ] Colors change as expected
- [ ] Hover rule text / notes are correct

### D. Indicator Definitions verification
- [ ] display_name renders correctly
- [ ] definition renders correctly
- [ ] how_to_read renders correctly

### E. Learn More verification
- [ ] Nested expander appears
- [ ] Correct markdown file loads
- [ ] Markdown renders cleanly
- [ ] Missing-doc behavior is graceful

### F. Regression checks
- [ ] No impact on unrelated indicators
- [ ] No persistence behavior changed
- [ ] No UI layout breakage


---


## 11) Common Failure Checks
- [ ] Missing from `_get_optionc_meta()`
- [ ] Missing from `INDICATOR_DEFS`
- [ ] Missing family mapping in `get_indicator_family()`
- [ ] Missing markdown file
- [ ] Row key / value column mismatch
- [ ] Rule expressions reference wrong variable names
- [ ] Indicator is actually out of scope


---


## 12) Final Decision
- [ ] Ready to implement
- [ ] Partially ready
- [ ] Blocked

### Blocking reason(s)
- 

### Next action
- [ ] Add compute support
- [ ] Add rule support
- [ ] Add row identity
- [ ] Add UI metadata
- [ ] Add Learn More markdown
- [ ] Reopen scope first


---

# Indicator Onboarding Template — Rolling Heatmap / Indicator Definitions

## 0) Request Summary
- **Indicator family:** ATR
- **Parameter(s):** 14
- **Canonical row key(s):** ATR_14
- **Goal:** 
  - [x] Add to rolling heatmap only
  - [x] Add to Indicator Definitions only
  - [ ] Add full rule/scoring support
  - [x] Add Learn More doc
- **In scope under current project locks?**
  - [x] Yes
  - [ ] No
  - [ ] Need confirmation


---


## 1) Scope / Phase Check
### A. Scope status
- **Current phase / workstream:** Phase III UX / educational refinement
- **Is this indicator family deferred or excluded?**
  - [x] No
  - [ ] Yes → stop and reopen scope first

### B. Notes
- ATR itself is not the same as derived ATR-based semantics.
- Adding ATR as an educational/display row is different from adding new ATR-based rule logic.


---


## 2) Indicator Type
- [x] Existing indicator already computed
- [ ] Existing indicator already scored
- [ ] New computed indicator
- [ ] New scored indicator
- [x] Display-only indicator
- [x] Educational-content-only addition

### Expected behavior
- **Should it have values in the heatmap?**
  - [x] Yes
  - [ ] No
- **Should it have buy/sell/neutral scores?**
  - [ ] Yes
  - [x] No
- **Should it appear in Indicator Definitions?**
  - [x] Yes
  - [ ] No
- **Should it have Learn More markdown?**
  - [x] Yes
  - [ ] No


---


## 3) Numeric Layer Check
**Primary file:** `indicator_preprocessor.py`

### A. Computation status
- **Does the numeric series already exist?**
  - [x] Yes
  - [ ] No

### B. Canonical column names
- Primary value column: `ATR_14`
- Related columns / extras: `ATRP_14`
- Notes on naming:
  - `ATR_14` = absolute volatility
  - `ATRP_14` = ATR normalized as a percent of price

### C. If new computation is required
- Not required for this example


---


## 4) Rule / Semantic Layer Check
**Primary file:** `master_rules_normalized.json`

### A. Scoring required?
- [ ] Yes
- [x] No

### B. If yes
- Not applicable for this example

### C. Rule coverage
- Not applicable for this example

### D. Naming alignment check
- Not applicable for this example

### E. Supporting files to inspect
- `signals_loader.py`
- `signal_classifier.py`
- `expression_engine.py`

Notes:
- ATR may exist as a dependency for other rules without needing its own scored heatmap row.


---


## 5) Rolling Heatmap Row Identity
**Primary file:** `technical.py`
**Function:** `_get_optionc_meta()`

### A. Add / confirm row entry
- [x] engine_indicator
- [x] param_key
- [x] display_key
- [x] value_col
- [ ] extra_value_cols (if needed)

### B. Canonical row key(s)
- Row key 1: `ATR_14`

### C. Questions
- Does the row key exactly match downstream UI metadata key?
  - [x] Yes
  - [ ] No

Notes:
- This is the key UI gate.
- If `ATR_14` is not added here, it will never appear in the heatmap or definitions panel.


---


## 6) UI Metadata Layer
**Primary file:** `rolling_heatmap_adapter.py`
**Variable:** `INDICATOR_DEFS`

### A. Add / confirm row-level metadata
- [x] display_name
- [x] definition
- [x] how_to_read

### B. Exact key used in `INDICATOR_DEFS`
- `ATR_14`

### C. Notes
- Keep content row-level and concise.
- Do not put long-form family education here.

Example entry:

```python
"ATR_14": {
    "display_name": "ATR (14)",
    "definition": "Average True Range measures recent absolute price volatility.",
    "how_to_read": "Higher ATR means larger recent price movement; lower ATR means quieter price action.",
}
