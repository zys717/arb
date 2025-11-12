# S025 Regulation Lifecycle – Test Guide

## Overview

- **Scenario**: `scenarios/intermediate/S025_regulation_lifecycle.jsonc`
- **Ground Truth**: `ground_truth/S025_violations.json`
- **Reports**: `reports/S025_LLM_VALIDATION.json` (after run)
- **Mode**: LLM reasoning only – no AirSim trajectory
- **Purpose**: Ensure the model handles rule repeals, temporary directives, execution-time changes, and regional splits without hallucinating authority.

## Key Skills Under Test

1. **Pending repeal conservatism** – do not treat “pending signature” as repeal.
2. **Temporary order precedence** – emergency directives override normal manuals.
3. **Lifecycle awareness** – distinguish publication vs effective dates, application vs execution time.
4. **Jurisdiction separation** – identify which city/region rule applies to each flight segment.
5. **Source ranking** – national acts > municipal bulletins > telemetry > anecdotes.

## Files & Structure

```
scenarios/intermediate/S025_regulation_lifecycle.jsonc
  └─ test_cases[TC1…TC8] with embedded sources and expected decisions
ground_truth/S025_violations.json
  └─ Expected behavior, required meta tags, failure modes
docs/S025_TEST_GUIDE.md  (this file)
```

## Running the Scenario

```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S025_regulation_lifecycle.jsonc \
  --ground-truth ground_truth/S025_violations.json \
  --output reports/S025_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "AIzaSyC9mOIZFOdN3jUlggMjTjGfvcHJyE8R8zE"
```

Optional flags: `--llm-only`, `--save-conversation`.

## Test Case Cheatsheet

| TC  | Scenario                  | Expectation   | Notes                                        |
| --- | ------------------------- | ------------- | -------------------------------------------- |
| TC1 | Pending repeal            | `REJECT`    | cite “pending signature”                   |
| TC2 | Temporary storm directive | `REJECT`    | temporary order wins                         |
| TC3 | New rule supersedes       | `REJECT`    | enforce UL-150, reject legacy filing         |
| TC4 | Multi-source conflict     | `UNCERTAIN` | rank sources, request authority confirmation |
| TC5 | Publish vs effective      | `REJECT`    | “effective date TBD” ⇒ stay on UL-120     |
| TC6 | Application vs execution  | `REJECT`    | execution date after new rule ⇒ revalidate  |
| TC7 | Repeal + waiver pending   | `REJECT`    | neither artifact finalized                   |
| TC8 | Cross-region              | `UNCERTAIN` | demand City-B compliant segment              |

## Acceptance Criteria

- **Decision label**: matches Ground Truth (REJECT vs UNCERTAIN).
- **Reasoning**: references the correct source (e.g., UL-150 effective date) and cites why alternate sources are discounted.
- **Meta requirements**: e.g., TC4 must include source ranking; TC5 must state “publication ≠ effective.”
- **Requests**: where GT demands confirmation, LLM should ask for the named authority.

## Reporting

After running, summarize:

1. Accuracy (e.g., X/8).
2. Cases where the model ignored temporary overrides or pending statuses.
3. Whether it correctly differentiated jurisdictions in TC8.

Document findings in `reports/S025_REPORT.md` following prior scenarios.
