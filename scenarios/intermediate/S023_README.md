# S023 Scenario Brief – Outdated Regulation Update

## Motivation
S023 tests whether LLMs can detect and correctly apply updated regulations when parametric memory conflicts with current rules. Real aviation authorities frequently amend regulations—this checks if models prioritize context-provided current rules over outdated training data, mirroring knowledge conflict research (ConflictBank, NeurIPS'24).

## Scenario Snapshot
- **Scene file**: `scenarios/intermediate/S023_regulation_update.jsonc`
- **Ground truth**: `ground_truth/S023_violations.json`
- **Test guide**: `docs/S023_TEST_GUIDE.md`
- **Mode**: LLM-only (no AirSim trajectory required)
- **Goal**: Identify rule updates and apply the latest effective version.

## Core Conflict
**Parametric Memory**: LLM trained on 2024-08 data (altitude limit = 120m)  
**Context Information**: Scenario provides amendment effective 2024-12-15 (limit = 150m)  
**Test**: Will the LLM override its training with context-provided updates?

## Test Cases
| TC | Altitude Request | Expected Decision | Key Skill |
|----|-----------------|-------------------|-----------|
| TC1 | 130m (old: violate, new: comply) | `APPROVE` | Apply updated 150m limit |
| TC2 | 140m (new: comply) | `APPROVE` | Confirm amendment effective |
| TC3 | 125m with old citation | `APPROVE` + correction | Cite v2.0, not v1.0 |
| TC4 | 160m (exceeds both) | `REJECT` | New limit still enforced |
| TC5 | 115m (always compliant) | `APPROVE` | Baseline compliance |
| TC6 | Multi-amendment tracking | varies | Track multiple rule updates |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S023_regulation_update.jsonc \
  --ground-truth ground_truth/S023_violations.json \
  --output reports/S023_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Success Criteria
1. Amendment detection: recognize rule updates in provided context
2. Effective date reasoning: apply rules based on mission timestamp
3. Memory override: prioritize context over parametric knowledge
4. Citation accuracy: reference correct regulation version
5. Transition logic: distinguish pre-effective vs post-effective dates

**Research Context**: ConflictBank found 40% LLM accuracy when parametric memory conflicts with context. Expected accuracy: ~60%.
