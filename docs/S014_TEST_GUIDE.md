# S014 Test Guide: BVLOS Waiver

**Scenario ID**: S014_BVLOSWaiver  
**Test Cases**: 6  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Within basic VLOS (400m < 500m)

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC1.json --mode auto --command "move_to_position(400, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC2: BVLOS without waiver (600m > 500m)

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC2.json --mode auto --command "move_to_position(600, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC3: BVLOS with observer waiver

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC3.json --mode auto --command "move_to_position(600, 0, 50, waiver='observer')"
```

**Expected**: ✅ APPROVE

---

### TC4: BVLOS with technical means waiver

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC4.json --mode auto --command "move_to_position(1500, 0, 50, waiver='technical')"
```

**Expected**: ✅ APPROVE

---

### TC5: BVLOS with special permit

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC5.json --mode auto --command "move_to_position(3000, 0, 50, waiver='permit')"
```

**Expected**: ✅ APPROVE

---

### TC6: Exceeds waiver limit (6000m > 5000m)

```bash
python run_scenario_vlos.py S014_bvlos_waiver.jsonc -o traj_S014_TC6.json --mode auto --command "move_to_position(6000, 0, 50, waiver='permit')"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | APPROVE | Within basic VLOS (400m < 500m) |
| TC2 | REJECT | BVLOS without waiver (600m > 500m) |
| TC3 | APPROVE | BVLOS with observer waiver |
| TC4 | APPROVE | BVLOS with technical means waiver |
| TC5 | APPROVE | BVLOS with special permit |
| TC6 | REJECT | Exceeds waiver limit (6000m > 5000m) |

**Expected Results**: 2 REJECT, 4 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S014_bvlos_waiver.jsonc \
    --ground-truth ground_truth/S014_violations.json \
    --output reports/S014_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
