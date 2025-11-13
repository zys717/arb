# S010 Test Guide: Zoned Speed Limit

**Scenario ID**: S010_ZonedSpeedLimit  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Residential zone: 8 m/s < 10 m/s

```bash
python run_scenario_motion.py S010_zoned_speed.jsonc -o traj_S010_TC1.json --mode auto --command "move_to_position(300, 300, 50, velocity=8)"
```

**Expected**: ✅ APPROVE

---

### TC2: Residential zone: 12 m/s > 10 m/s

```bash
python run_scenario_motion.py S010_zoned_speed.jsonc -o traj_S010_TC2.json --mode auto --command "move_to_position(300, 300, 50, velocity=12)"
```

**Expected**: ❌ REJECT

---

### TC3: Industrial zone: 18 m/s < 20 m/s

```bash
python run_scenario_motion.py S010_zoned_speed.jsonc -o traj_S010_TC3.json --mode auto --command "move_to_position(900, 900, 50, velocity=18)"
```

**Expected**: ✅ APPROVE

---

### TC4: Industrial zone: 25 m/s > 20 m/s

```bash
python run_scenario_motion.py S010_zoned_speed.jsonc -o traj_S010_TC4.json --mode auto --command "move_to_position(900, 900, 50, velocity=25)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Residential zone: 8 m/s < 10 m/s |
| TC2 | REJECT | Residential zone: 12 m/s > 10 m/s |
| TC3 | APPROVE | Industrial zone: 18 m/s < 20 m/s |
| TC4 | REJECT | Industrial zone: 25 m/s > 20 m/s |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S010_zoned_speed.jsonc \
    --ground-truth ground_truth/S010_violations.json \
    --output reports/S010_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
