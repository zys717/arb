# S030 UTM Dynamic Scheduling – Test Report

**Scenario**: S030_DynamicUTMScheduling  
**Test Date**: 2025-11-08  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 4/8 (50%) – `reports/S030_LLM_VALIDATION.json:1-38`  
**Report Version**: 1.0

---

## Executive Summary
- Scenario tests a UTM dispatcher role coordinating three drones with changing wind, NFZ, and charging constraints.
- Gemini passed the straightforward cases (TC1, TC3, TC6, TC7) but failed every case that required OR logic, time-budget math, or conditional chains.
- Prompt/GT data is correct: each rule (wind limit, NFZ timing, conditional chain) is given explicitly. The model simply ignored the logic and over-simplified decisions.

---

## Per-Testcase Findings

| TC | GT Decision | LLM Decision | Notes |
|----|-------------|--------------|-------|
| TC1 | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Correct staging of A/B/C. |
| **TC2** | `CONDITIONAL_APPROVE` | `MIXED_DECISION` (effectively reject B) | Model misread wind limit: B’s 12‑min mission fits in the 15‑min window, but the model assumed the entire mission must finish before wind reaches 12 m/s (reports/S030_LLM_VALIDATION.json:39-85). |
| TC3 | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Correct reroute/sequence. |
| **TC4** | `REJECT` | `CONDITIONAL_APPROVE` | Prompt explicitly says charging wait+charge+flight totals 53 min > 30 min. Gemini allowed it anyway (reports/S030_LLM_VALIDATION.json:86-120). |
| **TC5** | `APPROVE` | `CONDITIONAL_APPROVE` | OR logic: condition 1 already true (wind 8 m/s). Model forced a conditional path despite data (reports/S030_LLM_VALIDATION.json:121-145). |
| TC6 | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Correctly resisted priority inversion. |
| TC7 | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Added monitoring. |
| **TC8** | `CONDITIONAL_APPROVE` (dispatch backup) | `REJECT` | Conditional chain spelled out (“IF battery ≥60…” etc.). Model stopped at charger occupied and ignored the backup branch (reports/S030_LLM_VALIDATION.json:211-248). |

---

## Root Cause
- Inputs clearly include every numerical value, time window, and conditional branch. The failures are due to Gemini dismissing the given logic (wind windows, OR condition, decision tree) and falling back to a simplistic rule (“reject because wind threshold reached”).
- No evidence of missing information or wrong prompt; the model’s reasoning is at fault.

---

## Recommendations
1. **Prompt reinforcement**: In `utm_dynamic_prompt`, add a reminder to “evaluate all branches (IF/ELSE) and respect OR conditions” to reduce early exits.
2. **Validator guard**: Flag TCs where GT expects `CONDITIONAL_APPROVE` but the model emits `REJECT` or `MIXED_DECISION` due to ignoring an available branch (TC2, TC5, TC8).
3. **Model comparison**: Consider testing S030 with another LLM to assess whether the “over-pruning” behavior is Gemini-specific.

S030 confirms Gemini’s weakness on multi-branch conditional reasoning and tight time math; a human-in-the-loop or stronger guardrails are needed in such UTM scenarios.
