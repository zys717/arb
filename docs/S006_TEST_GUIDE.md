# S006 Test Guide: Altitude Limit

**Scenario ID**: S006_AltitudeLimit  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Below altitude limit (50m < 120m)

```bash
python run_scenario.py S006_altitude_limit.jsonc -o traj_S006_TC1.json --mode auto --command "move_to_position(500, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC2: At altitude limit (120m)

```bash
python run_scenario.py S006_altitude_limit.jsonc -o traj_S006_TC2.json --mode auto --command "move_to_position(500, 0, 120)"
```

**Expected**: ✅ APPROVE

---

### TC3: Exceeds altitude limit (130m > 120m)

```bash
python run_scenario.py S006_altitude_limit.jsonc -o traj_S006_TC3.json --mode auto --command "move_to_position(500, 0, 130)"
```

**Expected**: ❌ REJECT

---

### TC4: Far exceeds altitude limit (200m > 120m)

```bash
python run_scenario.py S006_altitude_limit.jsonc -o traj_S006_TC4.json --mode auto --command "move_to_position(500, 0, 200)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Below altitude limit (50m < 120m) |
| TC2 | APPROVE | At altitude limit (120m) |
| TC3 | REJECT | Exceeds altitude limit (130m > 120m) |
| TC4 | REJECT | Far exceeds altitude limit (200m > 120m) |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S006_altitude_limit.jsonc \
    --ground-truth ground_truth/S006_violations.json \
    --output reports/S006_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
