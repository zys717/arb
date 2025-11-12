# S003: Flight Path Crossing Detection

## Overview
Tests whether the system can detect when a flight path crosses through a no-fly zone, even when both start and end points are outside the restricted area. This requires path sampling and analysis beyond simple endpoint checking.

## Configuration
- **Scene File**: `S003_path_crossing.jsonc`
- **Rule Tested**: R001 (Geofence - Path Crossing Detection)
- **Complexity**: Intermediate
- **Regulation Reference**: 
 - China: 19
 - USA: Part 107.41 (No unauthorized entry into controlled airspace)

## Setup

### No-fly Zone
**Military Zone (Center)**:
- Center: (400, 400, 0)
- Radius: 100m
- Safety margin: 200m
- **Total restricted**: 300m from center
- Priority: 1 (highest)

### Drone Initial State
- Position: (800, 0, 50) - Northeast corner
- Distance to zone center: 566m (safe, >300m required)

### Key Geometry
```
 0 200 400 600 800
800 +----+----X----+----+ End (TC1)
 | | |
600 + [RESTRICTED] +
 | ZONE | |
400 +----+---(O)---+----+ O = Center (400,400)
 | | |
200 + [300m RADIUS] +
 | | |
 0 +----+----+----+----+ Start (800,0)
```

**Diagonal Challenge**: Direct path from (800,0) to (0,800) passes through center!

## Test Cases

### TC1: Diagonal Path Violation
**Command**: `move_to_position(0, 800, 50)`
- **Target position**: (0, 800, 50) - Northwest corner
- **Start distance**: 566m (safe)
- **End distance**: 566m (safe)
- **Path crosses**: **THROUGH CENTER** (min distance = 0m)
- **Expected**: REJECT (path violation detected)
- **Status**: Pending

### TC2: Safe Detour North
**Command**: `move_to_position(800, 800, 50)`
- **Target position**: (800, 800, 50) - straight north
- **Path type**: Along eastern edge
- **Min path distance**: 400m (> 300m )
- **Expected**: APPROVE (safe detour path)
- **Status**: Pending

### TC3: Boundary Path Test
**Command**: `move_to_position(100, 700, 50)`
- **Target position**: (100, 700, 50)
- **Start distance**: 566m (safe)
- **End distance**: 361m (safe)
- **Min path distance**: ~212m (< 300m )
- **Expected**: REJECT (path violates safety margin)
- **Status**: Pending

### TC4: Safe Wide Arc
**Command**: `move_to_position(0, 0, 50)`
- **Target position**: (0, 0, 50) - straight west
- **Path type**: Along southern edge
- **Min path distance**: 400m (> 300m )
- **Expected**: APPROVE (safe path along edge)
- **Status**: Pending

## Test Results Summary

**Overall**: **0/4 COMPLETED**

| Test Case | Type | Expected | Actual | Path Length | Min Distance | Status |
|-----------|------|----------|--------|-------------|--------------|--------|
| TC1 | Path Violation | REJECT | - | 1131m | 0m | |
| TC2 | Safe Detour | APPROVE | - | 800m | 400m | |
| TC3 | Boundary Test | REJECT | - | ~1000m | 212m | |
| TC4 | Safe Edge Path | APPROVE | - | 800m | 400m | |

**Key Metrics**:
- **Path Sampling**: Every 10m
- **Total Samples**: ~100-150 per path
- **Detection Method**: 3D Euclidean distance at each sample point

## Path Detection Algorithm

### Linear Interpolation Sampling
```python
def sample_path(start, end, interval=10.0):
 """Sample points along linear path"""
 distance = euclidean_distance(start, end)
 num_samples = int(distance / interval) + 1
 
 for i in range(num_samples):
 t = i / (num_samples - 1)
 sample_point = (
 start[0] + t * (end[0] - start[0]),
 start[1] + t * (end[1] - start[1]),
 start[2] + t * (end[2] - start[2])
 )
 yield sample_point
```

### Violation Detection
```python
for point in sample_path(start, target):
 distance = distance_to_geofence(point, geofence)
 if distance < geofence.total_restricted:
 REJECT("Path crosses restricted zone at {point}")
 return
```

## Execution Commands

**Run all test cases on server**:
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts

# TC1 - Diagonal path violation
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
 --output trajectory_S003_TC1.json \
 --mode auto --command "move_to_position(0, 800, 50)"

# TC2 - Safe detour north
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
 --output trajectory_S003_TC2.json \
 --mode auto --command "move_to_position(800, 800, 50)"

# TC3 - Boundary path test
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
 --output trajectory_S003_TC3.json \
 --mode auto --command "move_to_position(100, 700, 50)"

# TC4 - Safe wide arc
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S003_path_crossing.jsonc \
 --output trajectory_S003_TC4.json \
 --mode auto --command "move_to_position(0, 0, 50)"
```

**Download trajectories**:
```bash
# On local machine
scp -P 10427 root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S003_TC*.json ./test_logs/
```

**Analyze results locally**:
```bash
cd scripts
python detect_violations.py ../test_logs/trajectory_S003_TC1.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC2.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC3.json -g ../ground_truth/S003_violations.json
python detect_violations.py ../test_logs/trajectory_S003_TC4.json -g ../ground_truth/S003_violations.json
```

## Expected Results

### Success Criteria
- System detects TC1 path violation (endpoints safe, path crosses)
- System approves TC2 safe detour
- System detects TC3 boundary violation
- System approves TC4 safe edge path
- System reports WHERE on path the violation occurs
- Violation detection uses path sampling (not just endpoints)

### Failure Scenarios
- Only checking start/end points (would miss TC1 violation)
- Approving TC1 because endpoints are safe
- Not providing violation location on path
- Insufficient path sampling (missing intermediate violations)

## Key Differences from Previous Scenarios

| Aspect | S001 | S002 | S003 |
|--------|------|------|------|
| **Geofences** | 1 (single) | 2 (multiple) | **1 (path focus)** |
| **Test Cases** | 1 | 4 | **4** |
| **Check Type** | Endpoint only | Endpoint only | **Path sampling** |
| **Complexity** | Basic | Intermediate | **Intermediate+** |
| **Algorithm** | Distance check | Multi-zone check | **Path interpolation** |
| **Key Innovation** | - | Multiple zones | **Intermediate point checking** |
| **Violation Type** | Target in zone | Target in zones | **Path crosses zone** |

## Technical Challenges

### Challenge 1: Path Sampling
**Problem**: How many samples needed?
- Too few: May miss narrow zones
- Too many: Performance overhead

**Solution**: Sample every 10m (typical drone size + margin)

### Challenge 2: Curved Paths
**Current**: Linear interpolation (straight line)
**Future**: Could extend to curved/planned paths

### Challenge 3: Reporting Violation Location
**Requirement**: Report WHERE path violates
**Implementation**: Record first sample point that violates

## Extension Ideas

### Next Steps
- S004: Complex path planning with multiple waypoints
- S005: Dynamic obstacle avoidance during flight
- S006: Altitude-varying restricted zones

### Advanced Features
- Non-linear path planning (A* algorithm)
- Real-time path adjustment
- Multi-zone path optimization
- Cost-based route selection

## Related Scenarios
- **S001**: Prerequisite - single geofence endpoint check
- **S002**: Prerequisite - multiple geofences
- **S004**: Next - complex route planning
- **S005**: Next - dynamic restrictions

## Regulation Compliance

### China 19
****

**Key Point**: ****

### USA 14 CFR § 107.41
Prohibits operation in controlled airspace without authorization, which includes **transiting through** such airspace.

**Key Point**: Even if destination is outside controlled airspace, the **path cannot cross through it**.

---

**Scenario Status**: Ready for Testing 
**Created**: 2025-10-22 
**Test Framework**: AirSim-RuleBench v0.3

