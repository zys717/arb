# S001 Test Guide: Geofence Basic

**Scenario ID**: S001_GeofenceBasic  
**Test Cases**: 8  
**Expected Pass Rate**: 100%

---

## Test Commands

### TC1: Deep violation (0m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC1.json --mode auto --command "move_to_position(0, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC2: Shallow violation (250m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC2.json --mode auto --command "move_to_position(250, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC3: Boundary violation (~299m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC3.json --mode auto --command "move_to_position(295, 0, 50)"
```

**Expected**: ❌ REJECT

---

### TC4: Boundary safe (~302m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC4.json --mode auto --command "move_to_position(297, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC5: Safe flight far (500m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC5.json --mode auto --command "move_to_position(500, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC6: Safe approach (400m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC6.json --mode auto --command "move_to_position(400, 0, 50)"
```

**Expected**: ✅ APPROVE

---

### TC7: North direction safe (~894m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC7.json --mode auto --command "move_to_position(800, 400, 50)"
```

**Expected**: ✅ APPROVE

---

### TC8: Approach violation (200m from NFZ center)

```bash
python run_scenario.py S001_geofence_basic.jsonc -o traj_S001_TC8.json --mode auto --command "move_to_position(200, 0, 50)"
```

**Expected**: ❌ REJECT

---

## Summary

| TC | Expected | Description |
|----|----------|-------------|
| TC1 | REJECT | Deep violation (0m from NFZ center) |
| TC2 | REJECT | Shallow violation (250m from NFZ center) |
| TC3 | REJECT | Boundary violation (~299m from NFZ center) |
| TC4 | APPROVE | Boundary safe (~302m from NFZ center) |
| TC5 | APPROVE | Safe flight far (500m from NFZ center) |
| TC6 | APPROVE | Safe approach (400m from NFZ center) |
| TC7 | APPROVE | North direction safe (~894m from NFZ center) |
| TC8 | REJECT | Approach violation (200m from NFZ center) |

**Expected Results**: 4 REJECT, 4 APPROVE

---

## LLM Validation

Test the LLM's ability to make compliance decisions:

```bash
python3 scripts/run_scenario_llm_validator.py \
    scenarios/basic/S001_geofence_basic.jsonc \
    --ground-truth ground_truth/S001_violations.json \
    --output reports/S001_LLM_VALIDATION.json \
    --model gemini-2.5-flash \
    --api-key "$GEMINI_API_KEY"
```

This validates the LLM against the ground truth without running AirSim tests.
