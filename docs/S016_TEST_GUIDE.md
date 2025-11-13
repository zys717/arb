# S016 Test Guide: Detect and Avoid

**Scenario ID**: S016_DetectandAvoid  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: No obstacles detected

```bash
python run_scenario_detect.py S016_detect_avoid.jsonc -o traj_S016_TC1.json --mode auto --command "move_to_position(500, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC2: Obstacle on path without DAA

```bash
python run_scenario_detect.py S016_detect_avoid.jsonc -o traj_S016_TC2.json --mode auto --command "move_to_position(500, 0, 50, obstacle=True)"
```

**Expected**: ❌ REJECT

---

### TC3: Obstacle detected, avoidance active

```bash
python run_scenario_detect.py S016_detect_avoid.jsonc -o traj_S016_TC3.json --mode auto --command "move_to_position(500, 0, 50, obstacle=True, daa=True)"
```

**Expected**: ✅ APPROVE

---

### TC4: Long path with DAA system

```bash
python run_scenario_detect.py S016_detect_avoid.jsonc -o traj_S016_TC4.json --mode auto --command "move_to_position(1000, 0, 50, obstacle=True, daa=True)"
```

**Expected**: ✅ APPROVE

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | No obstacles detected |
| TC2 | REJECT | Obstacle on path without DAA |
| TC3 | APPROVE | Obstacle detected, avoidance active |
| TC4 | APPROVE | Long path with DAA system |

**Expected Results**: 1 REJECT, 3 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S016_detect_avoid.jsonc \
    --ground-truth ground_truth/S016_violations.json \
    --output reports/S016_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
