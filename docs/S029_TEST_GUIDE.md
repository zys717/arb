# S029 Phased Conditional Approval – Test Guide

## Overview
- Scenario: `scenarios/intermediate/S029_phased_conditional.jsonc`
- Ground truth: `ground_truth/S029_violations.json`
- Goal: Verify LLM can generate multi-phase conditional approvals with measurable gates and proper escalation.

## Key Expectations
- Phase structure: low-risk → medium-risk → full operations.
- Each phase must specify scope, hours, success criteria, and next-phase trigger.
- Dependencies cannot be skipped; nested conditions must be evaluated in order.

## Test Cases
| Case | Theme | GT Decision |
|------|-------|-------------|
| TC1 | Baseline phased approval | `CONDITIONAL_APPROVE` |
| TC2 | Binary framing trap | `CONDITIONAL_APPROVE` |
| TC3 | Skip Phase 2 request | `CONDITIONAL_APPROVE` (phase mandatory) |
| TC4 | Vague completion criteria | `UNCERTAIN` |
| TC5 | Seven micro phases | `CONDITIONAL_APPROVE` (consolidate) |
| TC6 | Reverse order plan | `REJECT` |
| TC7 | Nested condition gate | `CONDITIONAL_APPROVE` |
| TC8 | Incident mid Phase 2 | `UNCERTAIN` |

## Run Command
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S029_phased_conditional.jsonc \
  --ground-truth ground_truth/S029_violations.json \
  --output reports/S029_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Acceptance Checklist
1. Decision labels match GT (see table above).
2. Each `CONDITIONAL_APPROVE` includes at least three phases or consolidated phases with measurable criteria.
3. Phase dependencies explicitly reference prior phase completion.
4. `UNCERTAIN` responses explain why human review is needed (missing metrics or incident analysis).
5. `REJECT` explains the violation (reverse order) and instructs resubmission.

## Reporting
After running, summarize:
1. Accuracy and which cases defaulted to binary decisions or skipped phases.
2. Any vague criteria accepted by mistake.
3. Whether nested conditions and incident escalations were handled correctly.
