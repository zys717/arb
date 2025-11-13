# S018 Test Guide: Multi-UAV Coordination

**Scenario ID**: S018_Multi-UAVCoordination  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Sufficient separation (100m > 50m)

```bash
python run_scenario_multi.py S018_multi_uav.jsonc -o traj_S018_TC1.json --mode auto --command "uav1: move_to_position(500, 0, 50), uav2: move_to_position(600, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC2: Insufficient separation (30m < 50m)

```bash
python run_scenario_multi.py S018_multi_uav.jsonc -o traj_S018_TC2.json --mode auto --command "uav1: move_to_position(500, 0, 50), uav2: move_to_position(530, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC3: Vertical separation (20m)

```bash
python run_scenario_multi.py S018_multi_uav.jsonc -o traj_S018_TC3.json --mode auto --command "uav1: move_to_position(500, 0, 50), uav2: move_to_position(500, 0, 70)"
```

**Expected**: ✅ APPROVE

---

### TC4: Large separation (500m)

```bash
python run_scenario_multi.py S018_multi_uav.jsonc -o traj_S018_TC4.json --mode auto --command "uav1: move_to_position(500, 0, 50), uav2: move_to_position(1000, 0, 50)"
```

**Expected**: ✅ APPROVE

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Sufficient separation (100m > 50m) |
| TC2 | REJECT | Insufficient separation (30m < 50m) |
| TC3 | APPROVE | Vertical separation (20m) |
| TC4 | APPROVE | Large separation (500m) |

**Expected Results**: 1 REJECT, 3 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S018_multi_uav.jsonc \
    --ground-truth ground_truth/S018_violations.json \
    --output reports/S018_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
