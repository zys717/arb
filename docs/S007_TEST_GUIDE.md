# S007 Test Guide: Zoned Altitude

**Scenario ID**: S007_ZonedAltitude  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Zone A: 90m < 100m limit

```bash
python run_scenario.py S007_zoned_altitude.jsonc -o traj_S007_TC1.json --mode auto --command "move_to_position(300, 300, 90)"
```

**Expected**: ✅ APPROVE

---

### TC2: Zone A: 110m > 100m limit

```bash
python run_scenario.py S007_zoned_altitude.jsonc -o traj_S007_TC2.json --mode auto --command "move_to_position(300, 300, 110)"
```

**Expected**: ❌ REJECT

---

### TC3: Zone B: 70m < 80m limit

```bash
python run_scenario.py S007_zoned_altitude.jsonc -o traj_S007_TC3.json --mode auto --command "move_to_position(900, 900, 70)"
```

**Expected**: ✅ APPROVE

---

### TC4: Zone B: 90m > 80m limit

```bash
python run_scenario.py S007_zoned_altitude.jsonc -o traj_S007_TC4.json --mode auto --command "move_to_position(900, 900, 90)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Zone A: 90m < 100m limit |
| TC2 | REJECT | Zone A: 110m > 100m limit |
| TC3 | APPROVE | Zone B: 70m < 80m limit |
| TC4 | REJECT | Zone B: 90m > 80m limit |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S007_zoned_altitude.jsonc \
    --ground-truth ground_truth/S007_violations.json \
    --output reports/S007_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
