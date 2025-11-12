# S003 Path Crossing Detection - Test Execution Guide

**Scenario**: S003 - Flight Path Crossing Detection  
**Date**: 2025-10-22  
**Status**: Ready for Testing

---

## Overview

S003 tests whether the system can detect violations when a flight **path** crosses through a no-fly zone, even if both start and end points are outside the restricted area.

**Key Innovation**: Path sampling - checks intermediate points along the flight route, not just endpoints.

---

## Prerequisites

### On Server
1. ProjectAirSim server is running
2. Scene file uploaded to `sim_config/`:
   ```bash
   scp -P 10427 scenarios/basic/S003_path_crossing.jsonc \
       root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
   ```

### On Local Machine
1. Ground truth ready: `ground_truth/S003_violations.json`
2. Test logs directory: `test_logs/`

---

## Test Execution

### Step 1: SSH into Server

```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts
```

---

### Step 2: TC1 - Diagonal Path Violation (REJECT Expected)

**Test**: Direct diagonal path crosses through geofence center

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
    --output trajectory_S003_TC1.json \
    --mode auto \
    --command "move_to_position(0, 800, 50)"
```

**Expected Output**:
```
🔍 Pre-flight check: Target position...
   ✓ Target position is safe

🔍 Pre-flight check: Flight path (sampling every 10m)...
   ❌ Flight path crosses restricted zone!
      Path crosses geofence 'nfz_military_center' at sample X/Y: ...
      
   First violation at: N=..., E=..., Alt=50.0m

🚫 COMMAND REJECTED (path crosses restricted zone)
```

**Key Points**:
- Start (800, 0): Safe ✅
- End (0, 800): Safe ✅
- Path: Crosses center (400, 400) ❌
- **Expected**: REJECT due to path crossing

---

### Step 3: TC2 - Safe Detour North (APPROVE Expected)

**Test**: Flight along northern edge maintains safe distance

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
    --output trajectory_S003_TC2.json \
    --mode auto \
    --command "move_to_position(800, 800, 50)"
```

**Expected Output**:
```
🔍 Pre-flight check: Target position...
   ✓ Target position is safe

🔍 Pre-flight check: Flight path (sampling every 10m)...
   ✓ Path is safe (N samples checked)

✓ Pre-flight check passed, executing movement...
```

**Key Points**:
- Start (800, 0): Safe ✅
- End (800, 800): Safe ✅
- Path: Along eastern edge, min distance ~400m ✅
- **Expected**: APPROVE and execute flight

---

### Step 4: TC3 - Boundary Path Test (REJECT Expected)

**Test**: Path comes within safety margin

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
    --output trajectory_S003_TC3.json \
    --mode auto \
    --command "move_to_position(100, 700, 50)"
```

**Expected Output**:
```
🔍 Pre-flight check: Target position...
   ✓ Target position is safe

🔍 Pre-flight check: Flight path (sampling every 10m)...
   ❌ Flight path crosses restricted zone!
   
🚫 COMMAND REJECTED (path crosses restricted zone)
```

**Key Points**:
- Start (800, 0): Safe ✅
- End (100, 700): Safe (361m > 300m) ✅
- Path: Min distance ~212m < 300m ❌
- **Expected**: REJECT due to path violating safety margin

---

### Step 5: TC4 - Safe Wide Arc (APPROVE Expected)

**Test**: Flight along southern edge with safe clearance

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
    --output trajectory_S003_TC4.json \
    --mode auto \
    --command "move_to_position(0, 0, 50)"
```

**Expected Output**:
```
🔍 Pre-flight check: Target position...
   ✓ Target position is safe

🔍 Pre-flight check: Flight path (sampling every 10m)...
   ✓ Path is safe (N samples checked)

✓ Pre-flight check passed, executing movement...
```

**Key Points**:
- Start (800, 0): Safe ✅
- End (0, 0): Safe ✅
- Path: Along southern edge, min distance ~400m ✅
- **Expected**: APPROVE and execute flight

---

## Step 6: Download Trajectories

**On local machine**:
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

scp -P 10427 \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S003_TC*.json \
    ./test_logs/
```

---

## Step 7: Analyze Results Locally

```bash
cd scripts

# Analyze each test case
python detect_violations.py ../test_logs/trajectory_S003_TC1.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC2.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC3.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC4.json -g ../ground_truth/S003_violations.json
```

---

## Expected Results Summary

| Test Case | Command | Expected Decision | Expected Flight | Trajectory Points |
|-----------|---------|-------------------|-----------------|-------------------|
| **TC1** | (0, 800, 50) | ❌ REJECT | No | 1 (initial only) |
| **TC2** | (800, 800, 50) | ✅ APPROVE | Yes | Many (flight path) |
| **TC3** | (100, 700, 50) | ❌ REJECT | No | 1 (initial only) |
| **TC4** | (0, 0, 50) | ✅ APPROVE | Yes | Many (flight path) |

---

## Validation Criteria

### ✅ Pass Criteria
1. TC1 rejects command with "path crosses restricted zone"
2. TC2 approves and executes flight successfully
3. TC3 rejects command with "path crosses restricted zone"
4. TC4 approves and executes flight successfully
5. Rejection messages include violation location
6. Path sampling reports number of samples checked

### ❌ Fail Criteria
1. TC1 or TC3 approved (missed path violation)
2. TC2 or TC4 rejected (false positive)
3. Only endpoint checking (no path sampling)
4. No violation location reported

---

## Key Geometry Reference

```
Geofence Center: (400, 400, 0)
Geofence Radius: 100m
Safety Margin: 200m
Total Restricted: 300m from center

     0   200  400  600  800
800  +----+----X----+----+   TC1 End (0,800) ❌ Path violates
     |         |         |   TC2 End (800,800) ✅ Safe
600  +    [RESTRICTED]   +
     |      ZONE     |   |
400  +----+---(O)---+----+   O = Center
     |         |         |   TC3 End (100,700) ❌ Path violates
200  +    [300m RADIUS]  +
     |         |         |   TC4 End (0,0) ✅ Safe
  0  +----+----+----+----+   Start (800,0)
```

---

## Troubleshooting

### Issue: "Scene file not found"
**Solution**: Ensure S003_path_crossing.jsonc is in `sim_config/` on server

### Issue: TC1 approved instead of rejected
**Cause**: Path sampling not working
**Check**: Look for "Pre-flight check: Flight path" message in output

### Issue: All commands rejected
**Cause**: Initial position may violate geofence
**Check**: Verify initial position (800, 0, 50) is safe (distance > 300m)

---

## Notes

- **Path Sampling**: System samples every 10m along linear path
- **Sample Count**: TC1 should show ~113 samples (1131m path / 10m interval)
- **NED Coordinates**: Z=-50 means altitude 50m
- **Distance Calculation**: 3D Euclidean including altitude

---

**Test Guide Version**: 1.0  
**Created**: 2025-10-22  
**Next**: Generate S003_REPORT.md after all tests complete

