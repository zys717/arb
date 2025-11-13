# S009 Test Guide: Global Speed Limit

**Scenario ID**: S009_GlobalSpeedLimit  
**Test Cases**: 3  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Below speed limit (10 m/s < 15 m/s)

```bash
python run_scenario_motion.py S009_global_speed.jsonc -o traj_S009_TC1.json --mode auto --command "move_to_position(500, 0, 50, velocity=10)"
```

**Expected**: ✅ APPROVE

---

### TC2: At speed limit (15 m/s)

```bash
python run_scenario_motion.py S009_global_speed.jsonc -o traj_S009_TC2.json --mode auto --command "move_to_position(500, 0, 50, velocity=15)"
```

**Expected**: ✅ APPROVE

---

### TC3: Exceeds speed limit (20 m/s > 15 m/s)

```bash
python run_scenario_motion.py S009_global_speed.jsonc -o traj_S009_TC3.json --mode auto --command "move_to_position(500, 0, 50, velocity=20)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Below speed limit (10 m/s < 15 m/s) |
| TC2 | APPROVE | At speed limit (15 m/s) |
| TC3 | REJECT | Exceeds speed limit (20 m/s > 15 m/s) |

**Expected Results**: 1 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S009_global_speed.jsonc \
    --ground-truth ground_truth/S009_violations.json \
    --output reports/S009_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
