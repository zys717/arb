# S012 Test Guide: Time Window Restrictions

**Scenario ID**: S012_TimeWindowRestrictions  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Within allowed window (09:00-17:00)

```bash
python run_scenario.py S012_time_window.jsonc -o traj_S012_TC1.json --mode auto --command "move_to_position(500, 0, 50, time='09:00')"
```

**Expected**: ✅ APPROVE

---

### TC2: Before allowed window

```bash
python run_scenario.py S012_time_window.jsonc -o traj_S012_TC2.json --mode auto --command "move_to_position(500, 0, 50, time='08:30')"
```

**Expected**: ❌ REJECT

---

### TC3: After allowed window

```bash
python run_scenario.py S012_time_window.jsonc -o traj_S012_TC3.json --mode auto --command "move_to_position(500, 0, 50, time='17:30')"
```

**Expected**: ❌ REJECT

---

### TC4: Mid-day within window

```bash
python run_scenario.py S012_time_window.jsonc -o traj_S012_TC4.json --mode auto --command "move_to_position(500, 0, 50, time='12:00')"
```

**Expected**: ✅ APPROVE

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Within allowed window (09:00-17:00) |
| TC2 | REJECT | Before allowed window |
| TC3 | REJECT | After allowed window |
| TC4 | APPROVE | Mid-day within window |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S012_time_window.jsonc \
    --ground-truth ground_truth/S012_violations.json \
    --output reports/S012_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
