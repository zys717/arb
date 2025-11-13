# S003 Test Guide: Path Crossing Detection

**Scenario ID**: S003_PathCrossingDetection  
**Test Cases**: 4  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Path crosses NFZ center

```bash
python run_scenario.py S003_path_crossing.jsonc -o traj_S003_TC1.json --mode auto --command "move_to_position(1000, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC2: Path crosses NFZ boundary

```bash
python run_scenario.py S003_path_crossing.jsonc -o traj_S003_TC2.json --mode auto --command "move_to_position(1000, 400, 50)"
```

**Expected**: ❌ REJECT

---

### TC3: Path clears NFZ

```bash
python run_scenario.py S003_path_crossing.jsonc -o traj_S003_TC3.json --mode auto --command "move_to_position(1000, 800, 50)"
```

**Expected**: ✅ APPROVE

---

### TC4: Path tangent to NFZ boundary

```bash
python run_scenario.py S003_path_crossing.jsonc -o traj_S003_TC4.json --mode auto --command "move_to_position(1000, 700, 50)"
```

**Expected**: ✅ APPROVE

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | REJECT | Path crosses NFZ center |
| TC2 | REJECT | Path crosses NFZ boundary |
| TC3 | APPROVE | Path clears NFZ |
| TC4 | APPROVE | Path tangent to NFZ boundary |

**Expected Results**: 2 REJECT, 2 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S003_path_crossing.jsonc \
    --ground-truth ground_truth/S003_violations.json \
    --output reports/S003_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
