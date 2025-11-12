# S030 UTM Dynamic Scheduling – Test Guide

## Overview
- Scenario: `scenarios/intermediate/S030_dynamic_utm.jsonc`
- Ground truth: `ground_truth/S030_violations.json`
- Goal: Evaluate LLM’s ability to coordinate multiple drones with changing wind/NFZ/charging constraints while enforcing priority rules.

## Test Cases
| Case | Theme | GT Decision |
|------|-------|-------------|
| TC1 | Baseline priority | `CONDITIONAL_APPROVE` (A immediate, B/C delayed) |
| TC2 | Wind forecast | `CONDITIONAL_APPROVE` with “finish before 15 min or abort B” |
| TC3 | Temporary NFZ | `CONDITIONAL_APPROVE` with A reroute, B first |
| TC4 | Charging station delay | `REJECT` |
| TC5 | OR logic (wind vs waiver) | `APPROVE` |
| TC6 | Priority inversion | `CONDITIONAL_APPROVE` (ignore commercial pressure) |
| TC7 | Grey-zone safety margins | `CONDITIONAL_APPROVE` + monitoring condition |
| TC8 | Nested conditional chain | `CONDITIONAL_APPROVE` (dispatch backup) |

## Run Command
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S030_dynamic_utm.jsonc \
  --ground-truth ground_truth/S030_violations.json \
  --output reports/S030_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Acceptance Checklist
1. Decisions match GT labels and include per-drone conditions.
2. `CONDITIONAL_APPROVE` outputs list all follow-ups (monitor wind, reroute, dispatch backup).
3. `REJECT` includes time/battery math justifying failure (TC4).
4. OR/AND logic honored: B approved if wind <12 m/s OR waiver.
5. Escalation documented when alternative assets are needed (TC8).

## Reporting
After running, note accuracy and highlight any cases where the model ignored priority order or misread the conditional chain (TC5/TC8).  
