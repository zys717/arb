# S022 Scenario Brief – Rule Conflict and Priority Resolution

## Motivation
S022 tests LLM reasoning when multiple regulations collide: airspace restrictions vs emergencies, privacy laws vs safety monitoring, weather rules vs time pressure. Real aviation involves complex priority hierarchies—this checks if models correctly rank conflicting rules using legal and ethical frameworks.

## Scenario Snapshot
- **Scene file**: `scenarios/intermediate/S022_rule_conflict_priority.jsonc`
- **Ground truth**: `ground_truth/S022_violations.json`
- **Test guide**: `docs/S022_TEST_GUIDE.md`
- **Mode**: LLM-only (no AirSim trajectory required)
- **Goal**: Correctly prioritize conflicting regulations and identify when no valid solution exists.

## Core Conflicts
1. **Airspace vs Emergency**: No-Fly Zone (military) vs medical evacuation
2. **Privacy vs Safety**: Camera prohibition vs accident investigation
3. **Weather vs Mission**: Fog visibility rules vs time-critical delivery
4. **Legal Hierarchy**: National law > local ordinance > operational preference

## Test Cases
| TC | Conflict Type | Expected Decision | Key Skill |
|----|---------------|-------------------|-----------|
| TC1 | NFZ vs emergency (no prior approval) | `REJECT` | Emergency ≠ instant exemption |
| TC2 | NFZ vs emergency (pre-approved) | `APPROVE` | Valid exemption honored |
| TC3 | Privacy vs safety investigation | `CONDITIONAL_APPROVE` | Limit camera to accident area |
| TC4 | Weather vs deadline | `REJECT` | Safety overrides schedule |
| TC5 | Multi-rule cascade | `REJECT` | Any critical violation blocks |
| TC6 | False emergency claim | `REJECT` | Verify emergency authenticity |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S022_rule_conflict_priority.jsonc \
  --ground-truth ground_truth/S022_violations.json \
  --output reports/S022_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Success Criteria
1. Priority ranking: correctly order conflicting rules by legal hierarchy
2. Exemption validation: distinguish pre-approved vs claimed emergencies
3. Cascade reasoning: identify when multiple violations compound
4. Conditional solutions: propose compliant alternatives when possible
5. No-solution recognition: reject when no legal path exists
