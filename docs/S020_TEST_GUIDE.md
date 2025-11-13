# S020 Test Guide: Flight Application Deadline

**Scenario ID**: S020_FlightApplicationDeadline  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Submitted 10 days before (> 3 days)

```bash
python run_scenario.py S020_application_deadline.jsonc -o traj_S020_TC1.json --mode auto --command "move_to_position(500, 0, 50, submit_days=10)"
```

**Expected**: ✅ APPROVE

---

### TC2: Submitted 2 days before (< 3 days)

```bash
python run_scenario.py S020_application_deadline.jsonc -o traj_S020_TC2.json --mode auto --command "move_to_position(500, 0, 50, submit_days=2)"
```

**Expected**: ❌ REJECT

---

### TC3: Submitted exactly 3 days before

```bash
python run_scenario.py S020_application_deadline.jsonc -o traj_S020_TC3.json --mode auto --command "move_to_position(500, 0, 50, submit_days=3)"
```

**Expected**: ✅ APPROVE

---

### TC4: Same-day submission not allowed

```bash
python run_scenario.py S020_application_deadline.jsonc -o traj_S020_TC4.json --mode auto --command "move_to_position(500, 0, 50, submit_days=0)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Submitted 10 days before (> 3 days) |
| TC2 | REJECT | Submitted 2 days before (< 3 days) |
| TC3 | APPROVE | Submitted exactly 3 days before |
| TC4 | REJECT | Same-day submission not allowed |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S020_application_deadline.jsonc \
    --ground-truth ground_truth/S020_violations.json \
    --output reports/S020_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
