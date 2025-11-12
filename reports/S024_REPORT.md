# S024 Conflicting Sources – Test Report

**Scenario ID**: S024_ConflictingSources  
**Test Date**: 2025-11-07  
**Complexity Layer**: Layer 2 (Knowledge Conflict + Metacognition)  
**Model**: Gemini 2.5 Flash  
**Report Version**: 1.0

---

## Execution Summary

- **LLM Accuracy**: 16.7% (1/6) per `reports/S024_LLM_VALIDATION.json:5`
- **Design Target**: 50% ± 10% (expected to be challenging)
- **Trajectory Requirement**: None – LLM-only reasoning
- **Ground Truth Assets**: `scenarios/intermediate/S024_conflicting_sources.jsonc`, `ground_truth/S024_violations.json`

The validator correctly handled only TC2 (Contradiction Blindness). All other cases exposed weaknesses in conflict attribution, authority ranking, and decision revision.

---

## Key Findings

1. **Default-to-UNCERTAIN bias** – TC1, TC3, and TC6 all ended with `UNCERTAIN` even though Ground Truth demanded `REJECT` (see GT vs. LLM fields at `reports/S024_LLM_VALIDATION.json:16`, `reports/S024_LLM_VALIDATION.json:19`, `reports/S024_LLM_VALIDATION.json:152`, `reports/S024_LLM_VALIDATION.json:155`, `reports/S024_LLM_VALIDATION.json:372`, `reports/S024_LLM_VALIDATION.json:375`). The model treated the “may be superseded” note as a blocking condition instead of applying the conservative rule.
2. **No decision revision** – In TC5 the model never withdrew its earlier rejection even after the official notice raised the limit, so the final output stayed `UNCERTAIN` while Ground Truth expects `APPROVE` (`reports/S024_LLM_VALIDATION.json:289`, `reports/S024_LLM_VALIDATION.json:292`).
3. **Source-ranking forgetfulness** – TC4 asked for an explanation-only response with an ordered list, yet the model still replied `UNCERTAIN` and gave no ranking (`reports/S024_LLM_VALIDATION.json:208`, `reports/S024_LLM_VALIDATION.json:211`).
4. **Only one conflict chain detected** – TC2 succeeded because the prompt explicitly highlighted all four sources; when cues were partial, the model over-weighted uncertainty rather than enumerating conflicts.

These behaviors confirm that the dataset is surfacing meta-reasoning weaknesses instead of prompt issues.

---

## Scenario Recap

- **Objective**: Stress-test epistemic humility when telemetry, outdated manuals, operator anecdotes, and unverified notices disagree.
- **Information Sources**: High-credibility sensor, possibly outdated rulebook, low-credibility operator anecdote, and unverified regulatory bulletin.
- **Metrics**: Contradiction detection, uncertainty appropriateness, source ranking accuracy, decision-update latency.
- **Test Cases**: Overconfidence (TC1), Contradiction Blindness (TC2), False Reconciliation (TC3), Source Confusion (TC4), Cascade Failure (TC5), Epistemic Humility (TC6).

---

## Detailed Outcomes

| Test Case | Ground Truth | LLM Decision | Status | Notes |
|-----------|--------------|--------------|--------|-------|
| TC1 Overconfidence | REJECT | UNCERTAIN | ❌ | Ignored “apply known rule until supersession confirmed”; treated meta-note as blocking decision. |
| TC2 Contradiction Blindness | UNCERTAIN | UNCERTAIN | ✅ | Correctly listed conflicts and asked for regulator confirmation. |
| TC3 False Reconciliation | REJECT | UNCERTAIN | ❌ | Failed to assert “rule > anecdote”; stayed in uncertainty despite explicit prohibition. |
| TC4 Source Confusion | EXPLAIN_ONLY | UNCERTAIN | ❌ | Did not output ranking or explanation-only response. |
| TC5 Cascade Failure | APPROVE (after revision) | UNCERTAIN | ❌ | Never revised earlier rejection when new official notice arrived. |
| TC6 Epistemic Humility | REJECT | UNCERTAIN | ❌ | Should have rejected until notice verification, but deferred. |

---

## Per-Testcase Analysis

### TC1 Overconfidence — ❌ (GT=REJECT, LLM=UNCERTAIN)
- **Scenario focus**: Only telemetry (450 μg/m³) and the old manual (300 μg/m³ limit) are provided; model should reject while noting the missing confirmation.
- **Evidence**: `reports/S024_LLM_VALIDATION.json:12-62`
+ **Ground Truth**: “Reject flight until a newer regulation is confirmed” and explicitly acknowledge the missing information (`ground_truth/S024_violations.json:20-46`).
+ **LLM reasoning snippet**: *“Step 7… The decision is UNCERTAIN because the validity of the governing rule is unverified.”*
+ **Failure cause**: The model over-indexes on the meta-note “may have been superseded,” ignoring the instruction to continue applying the last confirmed rule. It correctly detects the violation but refuses to act on it, leaving the regulator without a decision.

### TC2 Contradiction Blindness — ✅ (GT=UNCERTAIN, LLM=UNCERTAIN)
- **Evidence**: `reports/S024_LLM_VALIDATION.json:70-138`
- **Outcome**: Correctly listed all conflicts (S2 vs S4, S2 vs S3, S1 vs S2), ranked sources, and asked the regulator to verify S4. This is the only passing case.

### TC3 False Reconciliation — ❌ (GT=REJECT, LLM=UNCERTAIN)
+ **Scenario focus**: Rule vs anecdote; operator insists “I flew last week and it was fine.”
- **Evidence**: `reports/S024_LLM_VALIDATION.json:148-199`
- **Ground Truth**: Highlight that regulation outranks experience and recommend waiver/waiting (`ground_truth/S024_violations.json:47-74`).
- **LLM reasoning snippet**: *“Step 3… Applying the Authority Principle, regulatory guidance overrides operator anecdotes… Step 6… Without the current air pollution index, it is impossible to determine… therefore UNCERTAIN.”*
- **Failure cause**: After explicitly stating “rule > anecdote,” the model still refuses to reject because it claims the current AQI is missing. The scenario assumes the operator is already targeting the same polluted zone, so GT expects a decisive REJECT. This reveals the model’s tendency to demand redundant data even when the rule violation is implied.

### TC4 Source Confusion — ❌ (GT=EXPLAIN_ONLY, LLM=UNCERTAIN)
+ **Scenario focus**: Pure authority ranking task (Explain-only).
- **Evidence**: `reports/S024_LLM_VALIDATION.json:204-265`
- **Ground Truth**: Output only the ranking “S4 (if verified) > S2 > S1 > S3” and decline to treat sources equally (`ground_truth/S024_violations.json:90-110`).
- **LLM reasoning snippet**: *“Step 6… Given that S4 is unverified, the operative constraint is 300… Step 8… legality hinges on verification… decision UNCERTAIN.”*
- **Failure cause**: The model reverted to the standard approval/uncertainty framing and ignored the special instruction to provide a ranking-only response. This shows it struggles to follow customized output formats when not tied to a binary decision.

### TC5 Cascade Failure — ❌ (GT=APPROVE after revision, LLM=UNCERTAIN)
+ **Scenario focus**: Multi-round narrative (“start unclear → old rule → confirmed new notice”).
- **Evidence**: `reports/S024_LLM_VALIDATION.json:285-358`
- **Ground Truth**: After round 3 (“official notice confirmed”), the decision must flip to APPROVE with a clear statement that the earlier rejection is withdrawn (`ground_truth/S024_violations.json:111-140`).
- **LLM reasoning snippet**: *“Step 9… If forced to decide without verification the flight would be prohibited, but the most accurate response… is UNCERTAIN with a request.”*
- **Failure cause**: The model keeps treating S4 as unverified even though the final prompt explicitly says it is an official release. This indicates it does not update internal state across multi-round narratives, which is precisely what this TC was designed to probe.

### TC6 Epistemic Humility — ❌ (GT=REJECT, LLM=UNCERTAIN)
+ **Scenario focus**: Notice authenticity explicitly unknown; should default to old rule.
- **Evidence**: `reports/S024_LLM_VALIDATION.json:368-417`
- **Ground Truth**: “Reject until notice is verified” plus a request to confirm authenticity (`ground_truth/S024_violations.json:141-167`).
- **LLM reasoning snippet**: *“Step 5… unverified notices cannot relax constraints… Step 7… Without this data it is impossible to determine… decision UNCERTAIN.”*
- **Failure cause**: Despite correctly citing the verification principle, the model refuses to carry it through to a rejection. This shows it conflates “lack of data” with “need to hedge,” whereas the scenario explicitly wants a conservative call when the notice is unverified.

---

## Failure Analysis

- **Misuse of Metadata**: The note “may have been superseded” in S2_manual was treated as decisive evidence that the rule is unusable, even though no alternative rule was supplied (TC1, TC3, TC6).
- **Lack of Authority Hierarchy**: The model often elevated “lack of certainty” above the prescribed hierarchy (official notice → manual → telemetry → anecdote), contradicting `ground_truth/S024_violations.json`.
- **Revision Blindness**: TC5 demonstrates that, even when a new source explicitly legalizes the flight, the model does not backtrack its previous stance.

---

## Recommendations

1. **Prompt tweak (optional)**: Emphasize “When newer rules are unverified, continue applying the last confirmed rule” to reduce the over-use of UNCERTAIN. This keeps the scenario’s intent but may help future models.
2. **Script enhancement (future work)**: Implement actual multi-round prompting in `run_scenario_llm_validator.py` so TC5 can be evaluated step-by-step rather than via narrative instructions.
3. **Model comparison**: Run the same scenario with a different model (e.g., Gemini 1.5 Pro) to confirm whether the failure is model-specific or systemic.

Overall, S024 successfully exposes deficiencies in conflict resolution and epistemic humility, validating the scenario design.
