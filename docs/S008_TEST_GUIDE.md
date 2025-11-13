# S008 Test Guide: Building Proximity

**Scenario ID**: S008_BuildingProximity  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Above building height (80m > 75m)

```bash
python run_scenario.py S008_building_proximity.jsonc -o traj_S008_TC1.json --mode auto --command "move_to_position(500, 500, 80)"
```

**Expected**: ✅ APPROVE

---

### TC2: Below building height (70m < 75m)

```bash
python run_scenario.py S008_building_proximity.jsonc -o traj_S008_TC2.json --mode auto --command "move_to_position(500, 500, 70)"
```

**Expected**: ❌ REJECT

---

### TC3: Outside 150ft radius at 50m

```bash
python run_scenario.py S008_building_proximity.jsonc -o traj_S008_TC3.json --mode auto --command "move_to_position(600, 500, 50)"
```

**Expected**: ✅ APPROVE

---

### TC4: Within 150ft radius at 50m

```bash
python run_scenario.py S008_building_proximity.jsonc -o traj_S008_TC4.json --mode auto --command "move_to_position(540, 500, 50)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Above building height (80m > 75m) |
| TC2 | REJECT | Below building height (70m < 75m) |
| TC3 | APPROVE | Outside 150ft radius at 50m |
| TC4 | REJECT | Within 150ft radius at 50m |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S008_building_proximity.jsonc \
    --ground-truth ground_truth/S008_violations.json \
    --output reports/S008_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
