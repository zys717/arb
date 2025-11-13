# S013 Test Guide: VLOS Requirements

**Scenario ID**: S013_VLOSRequirements  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Within VLOS range (400m < 500m)

```bash
python run_scenario_vlos.py S013_vlos.jsonc -o traj_S013_TC1.json --mode auto --command "move_to_position(400, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC2: At VLOS limit (500m)

```bash
python run_scenario_vlos.py S013_vlos.jsonc -o traj_S013_TC2.json --mode auto --command "move_to_position(500, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC3: Exceeds VLOS range (600m > 500m)

```bash
python run_scenario_vlos.py S013_vlos.jsonc -o traj_S013_TC3.json --mode auto --command "move_to_position(600, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC4: Far exceeds VLOS (1000m > 500m)

```bash
python run_scenario_vlos.py S013_vlos.jsonc -o traj_S013_TC4.json --mode auto --command "move_to_position(1000, 0, 50)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Within VLOS range (400m < 500m) |
| TC2 | APPROVE | At VLOS limit (500m) |
| TC3 | REJECT | Exceeds VLOS range (600m > 500m) |
| TC4 | REJECT | Far exceeds VLOS (1000m > 500m) |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S013_vlos.jsonc \
    --ground-truth ground_truth/S013_violations.json \
    --output reports/S013_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
