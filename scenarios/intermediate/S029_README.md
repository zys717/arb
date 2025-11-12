# 🎯 S029 Scenario – Phased Conditional Approval

## Motivation
Some UAV programs can’t be flat approved or rejected: regulators require progressive phases (similar to FAA progressive inspections). Literature shows LLMs struggle with multi-step conditional logic, so S029 checks whether the model can design and enforce Phase1→Phase2→Phase3 approvals with measurable criteria.

## Files
- Scene: `scenarios/intermediate/S029_phased_conditional.jsonc`
- Ground truth: `ground_truth/S029_violations.json`
- Test guide: `docs/S029_TEST_GUIDE.md`
- Output: `reports/S029_LLM_VALIDATION.json`

## Scenario Snapshot
- Aircraft: DX-450 Hybrid, newly type-certified but little field data.
- Regulator: Civil Aviation Authority requiring progressive validation.
- Expected pattern: Phase 1 (low risk) → Phase 2 (expanded) → Phase 3 (full approval).

## Test Cases
| Case | Theme | Expected Decision |
|------|-------|-------------------|
| TC1 | Baseline phased approval | `CONDITIONAL_APPROVE` |
| TC2 | Binary framing trap | `CONDITIONAL_APPROVE` |
| TC3 | Attempt to skip a phase | `CONDITIONAL_APPROVE` (Phase2 mandatory) |
| TC4 | Vague criteria submission | `UNCERTAIN` (ask for measurable metrics) |
| TC5 | Over-segmentation (7 phases) | `CONDITIONAL_APPROVE` (consolidate) |
| TC6 | Reverse phase order | `REJECT` |
| TC7 | Nested conditional gates | `CONDITIONAL_APPROVE` |
| TC8 | Incident during Phase2 | `UNCERTAIN` |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S029_phased_conditional.jsonc \
  --ground-truth ground_truth/S029_violations.json \
  --output reports/S029_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Success Criteria
1. Recognize when a phased decision is required even if the prompt looks binary.
2. Provide objective metrics (flight hours, incident counts) for each phase.
3. Preserve phase order & dependencies; refuse to skip steps.
4. Detect vague criteria, over-segmentation, or reverse risk progression.
5. Escalate to human review when incident investigations or undefined metrics are pending.
