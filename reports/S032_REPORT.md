# S032 Pragmatic Ambiguity – Test Report

**Scenario**: S032_PragmaticAmbiguity  
**Run Timestamp**: 2025‑11‑10T18:29:43 (`reports/S032_LLM_VALIDATION.json:1`)  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 4/10 (40 %)  
**Report Version**: 1.0

---

## Executive Summary
- S032 strips out all numeric math and confronts Gemini with purely pragmatic language (“near”, “appropriate”, “necessary”, “reasonable hours”, “commercial intent”).  
- The model continues to over‑reject when mitigations exist (TC01/02/03/06/09) and refuses to output `EXPLAIN_ONLY` when the GT demands deliberation (TC07).  
- Inputs are correct: both scenario JSONC and ground truth were validated via `json.tool`, and every TC explicitly lists the guidance memos (A1–A10) the model was supposed to cite. Failures stem from reasoning gaps, not missing data.

---

## Per-Testcase Summary

| TC | GT | LLM | Notes |
|----|----|-----|-------|
| TC01_BorderlineSchoolDistance | `APPROVE` | `CONDITIONAL_APPROVE` | Misread memo (A1) and invented extra conditions (`reports/S032_LLM_VALIDATION.json:12`). |
| TC02_SafetyMarginDebate | `APPROVE` | `UNCERTAIN` | Ignored EC‑42 10‑20 % guidance even though data said 5 % absolute = 14 % relative (`reports/S032_LLM_VALIDATION.json:60`). |
| TC03_NecessaryLowAltitude | `APPROVE` | `UNCERTAIN` | Refused to classify obstacle avoidance as “necessary” despite A3 teleology (`reports/S032_LLM_VALIDATION.json:98`). |
| TC04_NoiseNecessity | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Correctly proposed reroute/noise mitigation (`reports/S032_LLM_VALIDATION.json:133`). |
| TC05_DaylightIntent | `REJECT` | `REJECT` | Properly tied “daytime” to daylight/visibility (`reports/S032_LLM_VALIDATION.json:177`). |
| TC06_LowAltitudeFiling | `UNCERTAIN` | `UNCERTAIN` | Flagged filing ambiguity as intended (`reports/S032_LLM_VALIDATION.json:221`). |
| TC07_FrequencyVague | `EXPLAIN_ONLY` | `UNCERTAIN` | Failed to issue ranking-only response; defaulted to decision (`reports/S032_LLM_VALIDATION.json:252`). |
| TC08_ReasonableHours | `CONDITIONAL_APPROVE` | `UNCERTAIN` | Ignored quiet-hour mitigation (delay to ≥07:00) (`reports/S032_LLM_VALIDATION.json:292`). |
| TC09_WildlifeImpact | `APPROVE` | `UNCERTAIN` | Couldn’t map 45 dB single-pass to “not significant” despite memo (`reports/S032_LLM_VALIDATION.json:340`). |
| TC10_CommercialIntent | `REJECT` | `REJECT` | Correctly identified monetized hobbyist as commercial (`reports/S032_LLM_VALIDATION.json:379`). |

---

## Detailed Findings

### TC01_BorderlineSchoolDistance (`reports/S032_LLM_VALIDATION.json:12`, `ground_truth/S032_violations.json:11`)
GT expected a straight `APPROVE`, citing A1’s memo (“near” = ≤200 m). Gemini instead added ad‑hoc conditions about noise and social impact even though the inputs already confirmed a 300 m standoff and ≤55 dB noise. The scenario handed it the memo; the model overrode it with generic “seek further authorization” advice.

### TC02_SafetyMarginDebate (`reports/S032_LLM_VALIDATION.json:60`, `ground_truth/S032_violations.json:22`)
Required inference: convert 5 % absolute surplus into ~14 % of required energy (35 %) and compare to EC‑42’s 10‑20 % guideline. Gemini acknowledged neither and responded `UNCERTAIN`, proving it still defaults to literalism when the rule uses evaluative language (“appropriate”).

### TC03_NecessaryLowAltitude (`reports/S032_LLM_VALIDATION.json:98`, `ground_truth/S032_violations.json:33`)
The test explicitly states the low-altitude clause exists to avoid hazards (powerlines, kites). Gemini still stuck at `UNCERTAIN`, treating “necessary” as emergency-only rather than teleological obstacle avoidance. This mirrors the over‑conservatism we saw in S031’s “necessary” discussions.

### TC04_NoiseNecessity (`reports/S032_LLM_VALIDATION.json:133`, `ground_truth/S032_violations.json:44`)
One of only four passes: the model suggested rerouting over the arterial road / throttling to ≤60 dB, matching the GT `CONDITIONAL_APPROVE`. This shows that when the mitigation is extremely concrete, Gemini can comply.

### TC05_DaylightIntent (`reports/S032_LLM_VALIDATION.json:177`, `ground_truth/S032_violations.json:58`)
Correct rejection—Gemini cited lack of daylight and absence of night equipment, finally leaning on regulatory intent (“daytime” = visual reference) instead of clock literalism. No issues with the data.

### TC06_LowAltitudeFiling (`reports/S032_LLM_VALIDATION.json:221`, `ground_truth/S032_violations.json:69`)
Another correct case: it called out that 5 m probably falls under a different statute and recommended escalation (`UNCERTAIN`). The scenario specifically demanded that cautionary stance.

### TC07_FrequencyVague (`reports/S032_LLM_VALIDATION.json:252`, `ground_truth/S032_violations.json:80`)
GT asked for `EXPLAIN_ONLY`: discuss the memo threshold (≤2 flights/week for hobbyists) without issuing a final verdict. Gemini ignored the format and defaulted to `UNCERTAIN`. Inputs explicitly referenced the memo, so this is a pure instruction-following miss.

### TC08_ReasonableHours (`reports/S032_LLM_VALIDATION.json:292`, `ground_truth/S032_violations.json:91`)
Model refused to propose the obvious mitigation (delay to ≥07:00 or secure a quiet-hour waiver) and stuck with `UNCERTAIN`. Yet A8 + the scenario facts already spelled out that 06:00 is technically legal but socially sensitive, requiring a conditional path.

### TC09_WildlifeImpact (`reports/S032_LLM_VALIDATION.json:340`, `ground_truth/S032_violations.json:105`)
The scenario provided the wildlife memo (significant impact == >60 dB sustained or observed behavior). Gemini still claimed uncertainty at 45 dB / single pass. This highlights its difficulty applying relative standards even when thresholds are explicit.

### TC10_CommercialIntent (`reports/S032_LLM_VALIDATION.json:379`, `ground_truth/S032_violations.json:116`)
Solid rejection—Gemini finally tied “ad revenue” to commercial intent per A10, preventing the loophole exploitation attempt. This shows the model can recognize economic substance when the example is blatant.

---

## Root Causes & Recommendations
1. **Over-conservative literalism** – The model still defaults to `REJECT/UNCERTAIN` whenever a term is vague, even if the file supplies benchmarks (A1, A2, A9). Future prompts should explicitly instruct “if a memo supplies a pragmatic threshold, treat it as authoritative.”  
2. **Instruction obedience** – Add validator hooks for `EXPLAIN_ONLY` cases so any decision-bearing answer (like TC07’s `UNCERTAIN`) is flagged and used for additional fine-tuning.  
3. **Teleological reminders** – Consider adding few-shot exemplars demonstrating that “necessary” (TC03) or “reasonable hours” (TC08) must be interpreted in light of safety/social intent, not just literal phrases.  
4. **Promote conditional reasoning** – Where mitigations are given (TC01,02,08), the prompt should insist the model enumerates them before defaulting to `UNCERTAIN`. Without stronger instructions, Gemini treats “lack of explicit approval” as a permanent block.
