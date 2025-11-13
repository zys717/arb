# S015 Test Guide: Dynamic NFZ Avoidance

**Scenario ID**: S015_DynamicNFZAvoidance  
**Test Cases**: 6  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Path crosses emergency NFZ

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC1.json --mode auto --command "move_to_position(800, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC2: Path clears emergency NFZ

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC2.json --mode auto --command "move_to_position(1500, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC3: Path crosses multiple NFZs

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC3.json --mode auto --command "move_to_position(3000, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC4: Short path before NFZ

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC4.json --mode auto --command "move_to_position(300, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC5: Path tangent to NFZ (50m clearance)

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC5.json --mode auto --command "move_to_position(500, 350, 50)"
```

**Expected**: ✅ APPROVE

---

### TC6: Diagonal path too close to NFZ

```bash
python run_scenario_path.py S015_dynamic_nfz_avoidance.jsonc -o traj_S015_TC6.json --mode auto --command "move_to_position(1500, 500, 50)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | REJECT | Path crosses emergency NFZ |
| TC2 | APPROVE | Path clears emergency NFZ |
| TC3 | REJECT | Path crosses multiple NFZs |
| TC4 | APPROVE | Short path before NFZ |
| TC5 | APPROVE | Path tangent to NFZ (50m clearance) |
| TC6 | REJECT | Diagonal path too close to NFZ |

**Expected Results**: 3 REJECT, 3 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S015_dynamic_nfz_avoidance.jsonc \
    --ground-truth ground_truth/S015_violations.json \
    --output reports/S015_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
