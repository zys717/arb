```

```

# S001 Test Guide: Geofence Basic

**Scenario ID**: S001_GeofenceBasic
**Rule Tested**: R001 - Geofence Violation Prevention
**Test Type**: Basic single NFZ distance checking and boundary handling
**Total Test Cases**: 8

---

## Overview

S001 tests the most fundamental geofence functionality:

- Distance calculation from NFZ center
- Boundary violation detection (300m restricted radius)
- Target position checking
- Simple straight-line paths (no complex crossing)

**NFZ Configuration**:

- Center: (0, 0, 0) NED coordinates
- Physical radius: 100m
- Safety margin: 200m
- **Total restricted distance: 300m**

**Initial Position**: (800, 0, 50) - safe distance from NFZ

---

## Prerequisites

### 1. File Upload

```bash
# Upload scenario file
scp -P 10427 AirSim-RuleBench/scenarios/basic/S001_geofence_basic.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# Upload run script
scp -P 10427 AirSim-RuleBench/scripts/run_scenario.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 2. Server Setup

```bash
# SSH to server
ssh -p 10427 root@connect.westb.seetacloud.com

# Switch to sduser
su - sduser

# Navigate to test directory
cd ~/project/ProjectAirSim/client/python/example_user_scripts

# Activate environment
source ~/airsim-venv/bin/activate
```

---

## Test Cases

### TC1: Deep Violation - Center

**Description**: Direct flight to NFZ center (0m from center)
**Expected**: REJECT - deep violation
**Target Distance**: 0m < 300m ❌

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC1.json \
  --mode auto \
  --command "move_to_position(0, 0, 50)"
```

**Expected Output**:

```
❌ PRE-FLIGHT CHECK FAILED: Target violates geofence!
   Geofence 'nfz_military_base' violated: 
   distance=0.0m (required >300.0m), depth=300.0m

🚫 COMMAND REJECTED (target in restricted zone)
```

**Verification**:

- ✓ Command rejected before flight
- ✓ No trajectory recorded (stays at start)
- ✓ Violation depth: 300.0m

---

### TC2: Shallow Violation - Inside Margin

**Description**: Flight to 250m from center (inside safety margin)
**Expected**: REJECT - shallow violation
**Target Distance**: 250m < 300m ❌

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC2.json \
  --mode auto \
  --command "move_to_position(250, 0, 50)"
```

**Expected Output**:

```
❌ PRE-FLIGHT CHECK FAILED: Target violates geofence!
   Geofence 'nfz_military_base' violated: 
   distance=250.0m (required >300.0m), depth=50.0m

🚫 COMMAND REJECTED (target in restricted zone)
```

**Verification**:

- ✓ Command rejected
- ✓ Violation depth: 50.0m (shallow)
- ✓ Target inside safety margin

---

### TC3: Boundary Violation

**Description**: Flight near boundary - 3D distance ~299m (295m horizontal at 50m altitude)
**Expected**: REJECT - inside restricted zone (3D distance < 300m)
**Target Distance**: 3D distance ~299m < 300m ❌
**Note**: Rule engine uses 3D distance calculation including altitude

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC3.json \
  --mode auto \
  --command "move_to_position(295, 0, 50)"
```

**Expected Output**:

```
❌ PRE-FLIGHT CHECK FAILED: Target violates geofence!
   Geofence 'nfz_military_base' violated: 
   distance≈299.2m (required >300.0m), depth≈0.8m

🚫 COMMAND REJECTED (boundary violation)
```

**Verification**:

- ✓ Command rejected near boundary
- ✓ 3D distance calculation: √(295² + 50²) ≈ 299.2m
- ✓ Violation depth: ~0.8m (boundary case)

---

### TC4: Boundary Safe

**Description**: Flight just outside boundary - 3D distance ~302m (297m horizontal at 50m altitude)
**Expected**: APPROVE - outside restricted zone
**Target Distance**: 3D distance ~302m > 300m ✅

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC4.json \
  --mode auto \
  --command "move_to_position(297, 0, 50)"
```

**Expected Output**:

```
✓ Target position is safe
✓ Path is safe (XX samples checked)

✅ All pre-flight checks passed
✓ Pre-flight check passed, executing movement...
✓ Target reached
```

**Verification**:

- ✓ Command approved and executed
- ✓ 3D distance calculation: √(297² + 50²) ≈ 302m
- ✓ Minimal clearance: ~2m beyond boundary
- ✓ Trajectory recorded successfully

---

### TC5: Safe Flight - Far

**Description**: Safe flight well outside NFZ (500m from center)
**Expected**: APPROVE - clearly safe
**Target Distance**: 500m > 300m ✅

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC5.json \
  --mode auto \
  --command "move_to_position(500, 0, 50)"
```

**Expected Output**:

```
✓ Target position is safe
✓ Path is safe

✅ All pre-flight checks passed
✓ Target reached
```

**Verification**:

- ✓ Command approved
- ✓ Clearance margin: 200m (comfortable)
- ✓ Flight completed successfully

---

### TC6: Perpendicular Approach

**Description**: Approach toward NFZ but stop at 400m
**Expected**: APPROVE - safe approach
**Target Distance**: 400m > 300m ✅

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC6.json \
  --mode auto \
  --command "move_to_position(400, 0, 50)"
```

**Expected Output**:

```
✓ Target position is safe
✓ Path is safe

✅ All pre-flight checks passed
✓ Target reached
```

**Verification**:

- ✓ Approaching NFZ but stops safely
- ✓ Clearance margin: 100m
- ✓ Path: (800, 0) → (400, 0) perpendicular approach

---

### TC7: North Direction Safe

**Description**: Safe flight in different direction (north)
**Expected**: APPROVE - different direction test
**Target Distance**: ~894m > 300m ✅

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC7.json \
  --mode auto \
  --command "move_to_position(800, 400, 50)"
```

**Expected Output**:

```
✓ Target position is safe
✓ Path is safe

✅ All pre-flight checks passed
✓ Target reached
```

**Verification**:

- ✓ Flight in north direction
- ✓ Distance from NFZ: sqrt(800² + 400²) ≈ 894m
- ✓ Large clearance margin: ~594m

---

### TC8: South Approach Violation

**Description**: Approach from start toward NFZ center at 200m
**Expected**: REJECT - violates restricted zone
**Target Distance**: 200m < 300m ❌

```bash
python run_scenario.py \
  /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
  -o traj_S001_TC8.json \
  --mode auto \
  --command "move_to_position(200, 0, 50)"
```

**Expected Output**:

```
❌ PRE-FLIGHT CHECK FAILED: Target violates geofence!
   Geofence 'nfz_military_base' violated: 
   distance=200.0m (required >300.0m), depth=100.0m

🚫 COMMAND REJECTED (target in restricted zone)
```

**Verification**:

- ✓ Command rejected
- ✓ Violation depth: 100.0m
- ✓ Approaching center but intercepted

---

## Summary Table

| TC  | Target Distance | Expected | Type               | Status |
| --- | --------------- | -------- | ------------------ | ------ |
| TC1 | 0m              | REJECT   | Deep violation     | ⬜     |
| TC2 | 250m            | REJECT   | Shallow violation  | ⬜     |
| TC3 | 300m            | REJECT   | Boundary violation | ⬜     |
| TC4 | 350m            | APPROVE  | Safe boundary      | ⬜     |
| TC5 | 500m            | APPROVE  | Safe far           | ⬜     |
| TC6 | 400m            | APPROVE  | Safe approach      | ⬜     |
| TC7 | 894m            | APPROVE  | North direction    | ⬜     |
| TC8 | 200m            | REJECT   | Approach violation | ⬜     |

**Expected Accuracy**: 8/8 = 100%

---

## Validation

After running all tests, check results:

```bash
# Count rejections (should be 4: TC1, TC2, TC3, TC8)
grep -l "COMMAND REJECTED" traj_S001_TC*.json | wc -l

# Count approvals (should be 4: TC4, TC5, TC6, TC7)
grep -l "success.*true" traj_S001_TC*.json | wc -l
```

```bash
# On local machine
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/traj_S001_*.json' .
```

---

## Notes

- S001 is the **most basic** geofence test
- All test cases use simple straight-line paths
- Focus on distance calculation and boundary handling
- No complex path crossing (that's S003's job)
- Rule engine should achieve 100% accuracy

**Next Steps**:

- S002: Multiple NFZ recognition
- S003: Path crossing detection
- S004: Tiered NFZ systems
