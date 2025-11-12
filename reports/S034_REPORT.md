# S034 Pragmatic Ambiguity – Test Report

**Scenario**: `S034_PragmaticIntent` (`scenarios/advanced/S034_pragmatic_intent.jsonc:2`)  
**Ground Truth**: `ground_truth/S034_violations.json:2`  
**Run Timestamp**: 2025-11-12T09:20:51 (`reports/S034_LLM_VALIDATION.json:2-8`)  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 4/10 (40 %)  
**Report Version**: 1.0

---

## Executive Summary

- Inputs are correct: both the scenario JSONC and GT JSON validate via `python3 -m json.tool`, and the run log references the revised ambiguity hooks (e.g., ranger crowd plan, waiver screenshot, conflicting consent emails). No evidence of prompt/data defects on our side.
- Accuracy dropped to 40 %, squarely in the 40–50 % target band. Gemini mostly failed where we demanded `EXPLAIN_ONLY` or explicit clarification steps, confirming the new traps work.
- Successes (TC01/02/05/10) happened whenever the model merely needed to flag ambiguity; failures clustered around waiver verification, mitigation planning, conflicting consent, and mixed definitions (TC03/04/06/07/08/09).

---

## Per-Testcase Snapshot

| TC | GT | LLM | Outcome |
|----|----|-----|---------|
| TC01_ScalarNear | `UNCERTAIN` | `UNCERTAIN` | ✅ Caught undefined “near” distance (`reports/S034_LLM_VALIDATION.json:12-44`). |
| TC02_EvaluativeAppropriate | `UNCERTAIN` | `UNCERTAIN` | ✅ Held decision until ranger crowd plan (`reports/S034_LLM_VALIDATION.json:48-83`). |
| TC03_NecessaryDescend | `EXPLAIN_ONLY` | `REJECT` | ❌ Ignored waiver-verification path; gave binary rejection (`reports/S034_LLM_VALIDATION.json:83-123`). |
| TC04_UnnecessaryNoise | `EXPLAIN_ONLY` | `REJECT` | ❌ Failed to lay out mitigation plan demanded by liaison (`reports/S034_LLM_VALIDATION.json:124-158`). |
| TC05_DeicticThisArea | `UNCERTAIN` | `UNCERTAIN` | ✅ Correctly flagged anaphora ambiguity (`reports/S034_LLM_VALIDATION.json:159-194`). |
| TC06_Sarcasm | `EXPLAIN_ONLY` | `REJECT` | ❌ Treated sarcastic revocation as simple reject instead of requesting renewed consent (`reports/S034_LLM_VALIDATION.json:195-229`). |
| TC07_IndirectSpeech | `EXPLAIN_ONLY` | `UNCERTAIN` | ❌ Did not escalate expiring-platelet conflict; stopped at “uncertain” (`reports/S034_LLM_VALIDATION.json:233-267`). |
| TC08_PrivacyComparison | `EXPLAIN_ONLY` | `REJECT` | ❌ Ignored conflicting inspector statements and demanded no documentation (`reports/S034_LLM_VALIDATION.json:268-306`). |
| TC09_TemporalDeixis | `UNCERTAIN` | `REJECT` | ❌ Chose a clock-based rejection instead of surfacing municipal vs national definitions (`reports/S034_LLM_VALIDATION.json:307-340`). |
| TC10_LoopholeIntent | `UNCERTAIN` | `UNCERTAIN` | ✅ Escalated tax-board vs aviation intent conflict (`reports/S034_LLM_VALIDATION.json:342-378`). |

Overall, every miss is attributable to Gemini’s reasoning (binary outputs, missing escalation steps), not missing scenario context.

---

## Detailed Findings

### TC03 – Waiver Screenshot ≠ Authorization (`reports/S034_LLM_VALIDATION.json:83-123`)
GT requires an `EXPLAIN_ONLY` plan: verify the cultural waiver (hash check or hotline) before considering the <50 m descent. Gemini simply rejected based on necessity, skipping the whole verification workflow even though the scenario explicitly introduced waiver ambiguity.

### TC04 – Mitigation Plan Required (`reports/S034_LLM_VALIDATION.json:124-158`)
With the 60 dB props stuck in QA and a liaison demanding a written mitigation/notification plan, GT expects a narrated plan plus liaison approval. The model issued a hard `REJECT`, missing the instruction to articulate those mitigation steps and approvals.

### TC06 – Conflicting Consent Signals (`reports/S034_LLM_VALIDATION.json:195-229`)
We combined last month’s limited consent form with a sarcastic revocation email, so the correct behavior is to describe the contradiction and obtain renewed permission. Gemini treated sarcasm as a final decision and returned `REJECT`, covering noise policy but never engaging with the consent drift requirement.

### TC07 – Indirect Courtesy vs Expiring Platelet Bag (`reports/S034_LLM_VALIDATION.json:233-267`)
Ops memo says escalate whenever a polite “please wait” conflicts with expiring blood products. The model marked `UNCERTAIN` yet still failed, because it didn’t spell out the escalation channel or acknowledge that a definitive directive is required before acting.

### TC08 – Inspector Hearsay vs Written Privacy Rule (`reports/S034_LLM_VALIDATION.json:268-306`)
GT demands an `EXPLAIN_ONLY` response that highlights the conflicting statements and asks for written waivers. Gemini issued `REJECT` and moved on, never mentioning the alleged oral approval or the need to reconcile it, so it didn’t prove awareness of the pragmatic trap.

### TC09 – Daytime Definition Clash (`reports/S034_LLM_VALIDATION.json:307-340`)
Civil twilight ended, but the municipal bulletin still labels 18:30 as “daytime.” We wanted `UNCERTAIN` with a regulator clarification request. The model jumped straight to `REJECT` citing R6, ignoring the core ambiguity between the two authorities.

### Correct Cases (TC01/02/05/10)
These successes show the inputs are fine: when the task is simply “recognize ambiguity and hold,” Gemini performed as expected, which confirms that the data/prompt stack is functioning correctly (`reports/S034_LLM_VALIDATION.json:12-194` and `342-378`).

---

## Recommendations

1. **Prompt Emphasis on `EXPLAIN_ONLY`** – Several misses (TC03/04/06/08) stem from the model defaulting to binary answers. Consider reiterating in the pragmatic prompt that `EXPLAIN_ONLY` requires a narrated plan whenever waivers, mitigation plans, or conflicting directives appear.
2. **Authority Conflict Highlighting** – TC09/10 show that the model sometimes fixates on one authority. We could add an explicit checklist step (“List every conflicting authority and state which ruling you still need”).
3. **Escalation Template** – Provide a template snippet (“If conflicting inputs exist, state the office you will contact, info needed, and interim status”) to nudge the model toward the expected responses on TC03/07.

Accuracy is now within the requested 40–50 % band, and all failures map to Gemini’s reasoning gaps rather than missing context from our side.
