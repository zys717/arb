# S009: Global Speed Limit

## Overview
100 km/h

## Configuration
- **Scene File**: `S009_speed_limit.jsonc`
- **Rule Tested**: 100km/h87/161km/h
- **Complexity**: Basic
- **Regulation Reference**: 
 - China: - 100/
 - USA: 14 CFR § 107.51(c) - 87100/

## Setup

### 
- ****: 100 km/h (27.78 m/s)
- ****: >= 100 km/h 
- ****: 0 km/h
- ****: 0.5

### 
- ****: (0, 0, 50) - 0m0m50m
- ****: 30 m/s (108 km/h) - 

### 
- ****: 
- ****: 0 km/h
- ****: 14:00

## Test Cases

### TC1: 72 km/h
**Command**: `move_to_position_with_velocity(500, 0, 50, 20.0)`
- ****: 20.0 m/s = 72 km/h
- ****: 28 km/h
- **Expected**: APPROVE - 100km/h
- **Status**: 

### TC2: 93.6 km/h
**Command**: `move_to_position_with_velocity(500, 0, 50, 26.0)`
- ****: 26.0 m/s = 93.6 km/h
- ****: 6.4 km/h
- **Expected**: APPROVE - 
- **Status**: 

### TC3: 100 km/h ****
**Command**: `move_to_position_with_velocity(500, 0, 50, 27.78)`
- ****: 27.78 m/s = 100.0 km/h
- ****: 0 km/h
- **Expected**: REJECT - 
- **Note**: ****"100km/h"<100
- **Status**: 

### TC4: 102.6 km/h
**Command**: `move_to_position_with_velocity(500, 0, 50, 28.5)`
- ****: 28.5 m/s = 102.6 km/h
- ****: 2.6 km/h
- **Expected**: REJECT - 
- **Status**: 

### TC5: 108 km/h
**Command**: `move_to_position_with_velocity(500, 0, 50, 30.0)`
- ****: 30.0 m/s = 108.0 km/h
- ****: 8.0 km/h
- **Expected**: REJECT - 
- **Status**: 

### TC6: 54 km/h
**Command**: `move_to_position_with_velocity(300, 0, 50, 15.0)`
- ****: 15.0 m/s = 54.0 km/h
- ****: 46 km/h
- **Expected**: APPROVE - 
- **Status**: 

## Test Results Summary

**Overall**: ⏳ 

| Test Case | Velocity (km/h) | Expected | Actual | Status |
|-----------|-----------------|----------|--------|--------|
| TC1 | 72.0 | APPROVE | - | ⏳ |
| TC2 | 93.6 | APPROVE | - | ⏳ |
| TC3 | 100.0 | REJECT | - | ⏳ |
| TC4 | 102.6 | REJECT | - | ⏳ |
| TC5 | 108.0 | REJECT | - | ⏳ |
| TC6 | 54.0 | APPROVE | - | ⏳ |

**Expected Pass Rate**: 6/6 (100%)

## Evaluation Commands

**** ( `run_scenario_motion.py`):
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts

# TC1 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC1.json \
 --mode auto --command "move_to_position_with_velocity(500, 0, 50, 20.0)"

# TC2 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC2.json \
 --mode auto --command "move_to_position_with_velocity(500, 0, 50, 26.0)"

# TC3 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC3.json \
 --mode auto --command "move_to_position_with_velocity(500, 0, 50, 27.78)"

# TC4 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC4.json \
 --mode auto --command "move_to_position_with_velocity(500, 0, 50, 28.5)"

# TC5 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC5.json \
 --mode auto --command "move_to_position_with_velocity(500, 0, 50, 30.0)"

# TC6 - 
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
 --output trajectory_S009_TC6.json \
 --mode auto --command "move_to_position_with_velocity(300, 0, 50, 15.0)"
```

****:
```bash
cd AirSim-RuleBench/scripts

python detect_violations.py \
 ../test_logs/trajectory_S009_TC1.json \
 -g ../ground_truth/S009_violations.json
```

## Key Differences from Previous Scenarios

| Aspect | S001-S008 | S009 (Speed Limit) |
|--------|-----------|-------------------|
| **** | | **** |
| **** | | **** |
| **** | | **+** |
| **** | 3D | **3D** |
| **** | m | **/m/s/km/h** |
| **** | `run_scenario.py` | **`run_scenario_motion.py`** () |
| **** | 600m (S001) | **100 km/h** |

## Implementation Notes

### 
```python
# 3D
ground_speed_ms = sqrt(velocity_north² + velocity_east² + velocity_down²)
ground_speed_kmh = ground_speed_ms × 3.6

# 
# 1 m/s = 3.6 km/h
# 100 km/h = 27.78 m/s
```

### 
```python
# 
move_to_position_with_velocity(north, east, altitude, velocity_m/s)

# 
move_to_position_with_velocity(500, 0, 50, 25.0)
# 25 m/s(500, 0, 50)
```

### 
1. ****: 
2. ****: 0.5
3. ****: 
4. ****: 

## Regulation Details

### 
****:
```
"4
7100/
"
```

****:
- ≤4kg
- 100 km/h
- "" < 100 km/h

### 
**14 CFR § 107.51(c)**:
```
"The groundspeed of the small unmanned aircraft may not exceed 
87 knots (100 miles per hour)."
```

****:
- UAS<55
- 87 = 100/ ≈ 161 km/h
- 161 vs 100 km/h

## Extension Ideas
- **S010**: 50km/h100km/h
- ****: //
- ****: 
- ****: /

## Related Scenarios
- **S006**: - 
- **S010**: - 
- **S011**: - 
- **S012**: - 

---

**Created**: 2025-10-22 
**Status**: 
**Script**: `run_scenario_motion.py` ()

