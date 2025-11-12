# S029 Phased Conditional Approval – Test Report

**Scenario**: S029_PhasedConditionalApproval  
**Test Date**: 2025-11-08  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 5/8 (62.5%) – `reports/S029_LLM_VALIDATION.json:1-40`  
**Report Version**: 1.0

---

## Executive Summary
- Scenario tests multi-phase conditional approvals (Phase 1 → Phase 2 → Phase 3) with measurable gates.  
- Gemini handled the baseline instructions (TC1/TC2/TC5/TC7/TC8) but failed whenever the operator’s proposal conflicted with policy (TC3/TC4/TC6).  
- Inputs clearly include dependency rules, and GT explains how to react; failures are due to the model overriding requirements, not missing data.

---

## Per-Testcase Highlights

### TC1 Baseline Phases — ✅  
`CONDITIONAL_APPROVE` with three phases and clear metrics (`reports/S029_LLM_VALIDATION.json:41-57`).

### TC2 Binary Trap — ✅  
Model ignored the “approve or reject” framing and still issued a phased plan (`reports/S029_LLM_VALIDATION.json:58-75`).

### TC3 Skip Phase — ❌  
**GT**: `CONDITIONAL_APPROVE` while enforcing Phase 2.  
**LLM**: `REJECT`.  
Regulator policy (in the prompt) states all phases are mandatory; the model should have reissued the three-phase plan, not deny the application (`reports/S029_LLM_VALIDATION.json:41-75`).

### TC4 Vague Criteria — ❌  
**GT**: `UNCERTAIN` (request objective metrics).  
**LLM**: `CONDITIONAL_APPROVE` after inventing its own metrics.  
The prompt explicitly highlighted the operator’s subjective wording; we expected the model to hold the decision and ask for measurable thresholds (`reports/S029_LLM_VALIDATION.json:76-110`).

### TC5 Too Many Phases — ✅  
Model suggested consolidating into three phases, matching GT (`reports/S029_LLM_VALIDATION.json:111-135`).

### TC6 Reverse Order — ❌  
**GT**: `REJECT`.  
**LLM**: `CONDITIONAL_APPROVE` after silently correcting the plan.  
Even though it recognized the risk progression issue, GT requires rejecting the submission and requesting resubmission (`reports/S029_LLM_VALIDATION.json:146-180`).

### TC7 Nested Condition — ✅  
Handled “Phase 1 completion AND weather dataset” properly and returned a conditional approval (`reports/S029_LLM_VALIDATION.json:181-205`).

### TC8 Phase Failure — ✅  
Returned `UNCERTAIN`, escalated to certification board pending incident review (`reports/S029_LLM_VALIDATION.json:206-230`).

---

## Root Cause
- Scenario files and GT spell out every policy rule (no skipping phases, objective metrics, low-to-high risk order).  
- Gemini’s misses are all “overreaches”: rejecting when it should correct (TC3), approving vague info instead of holding (TC4), and approving a fixed-up plan instead of rejecting (TC6). Inputs are complete; the model simply chose the wrong actions.

---

## Recommendations
1. **Prompt reinforcement**: Emphasize “Do not reject or approve outright when GT expects you to restate the phased plan or request more data.”  
2. **Validator guard**: Auto-flag TCs where GT ≠ LLM decision for these structural cues (skip-phase, vague criteria, reverse order).  
3. **Model comparison**: Run S029 with another foundation model to see if the “over-correcting” bias persists.

S029 now demonstrates that Gemini handles standard phased approvals but struggles when the applicant’s plan violates policy, reinforcing the need for tight guardrails or human review in such cases.
