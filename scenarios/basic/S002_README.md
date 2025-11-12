# S002: Multiple Geofence Recognition Test

## Overview
Tests whether the system can simultaneously detect and prevent violations of multiple no-fly zones with different parameters and priorities.

## Configuration
- **Scene File**: `S002_multi_geofence.jsonc`
- **Rule Tested**: R001 (Geofence - Multi-zone)
- **Complexity**: Intermediate
- **Regulation Reference**: 
 - China: 19
 - USA: Multiple TFR/Airport zones

## Setup

### No-fly Zones
**Zone 1 - Military Base**:
- Center: (0, 0, 0)
- Radius: 100m
- Safety margin: 500m
- **Total restricted**: 600m from center
- Priority: 1 (highest)

**Zone 2 - Hospital**:
- Center: (800, 800, 0)
- Radius: 50m
- Safety margin: 300m
- **Total restricted**: 350m from center
- Priority: 2

### Drone Initial State
- Position: (650, 0, 50)
- Distance to military zone: 650m (safe, >600m required)
- Distance to hospital zone: ~1131m (safe, >350m required)

## Test Cases

### TC1: Hospital Violation
**Command**: `move_to_position(900, 900, 50)`
- **Target position**: (900, 900, 50)
- **Distance to hospital**: ~150m
- **Expected**: REJECT (violates hospital zone, 150m < 350m required)
- **Status**: PASSED

### TC2: Military Violation
**Command**: `move_to_position(100, 0, 50)`
- **Target position**: (100, 0, 50)
- **Distance to military**: ~112m
- **Expected**: REJECT (violates military zone, 112m < 600m required)
- **Status**: PASSED

### TC3: Safe Flight
**Command**: `move_to_position(700, 200, 50)`
- **Target position**: (700, 200, 50)
- **Distance to military**: ~728m (> 600m )
- **Distance to hospital**: ~633m (> 350m )
- **Expected**: APPROVE (safe from both zones)
- **Status**: PASSED (440 trajectory points, 44.7s flight)

### TC4: Boundary Test
**Command**: `move_to_position(601, 0, 50)`
- **Target position**: (601, 0, 50)
- **Distance to military**: ~602m (just above 600m threshold)
- **Expected**: APPROVE (edge case, boundary condition)
- **Status**: PASSED (135 trajectory points, 13.5s flight)

## Test Results Summary

**Overall**: **4/4 PASSED (100%)**

| Test Case | Type | Expected | Actual | Points | Status |
|-----------|------|----------|--------|--------|--------|
| TC1 | Hospital Violation | REJECT | REJECT | 1 pt | |
| TC2 | Military Violation | REJECT | REJECT | 1 pt | |
| TC3 | Safe Flight | APPROVE | APPROVE | 440 pts | |
| TC4 | Boundary Test | APPROVE | APPROVE | 135 pts | |

**Total Trajectory Points**: 577 
**Total Flight Time**: 58.2 seconds 
**Test Coverage**: 100% (violations + approvals + boundaries)

## Evaluation Commands

**Run all test cases on server**:
```bash
# TC1 - Hospital violation
python run_scenario.py S002_multi_geofence.jsonc \
 --output trajectory_S002_TC1.json \
 --mode auto --command "move_to_position(900, 900, 50)"

# TC2 - Military violation
python run_scenario.py S002_multi_geofence.jsonc \
 --output trajectory_S002_TC2.json \
 --mode auto --command "move_to_position(100, 0, 50)"

# TC3 - Safe flight
python run_scenario.py S002_multi_geofence.jsonc \
 --output trajectory_S002_TC3.json \
 --mode auto --command "move_to_position(700, 200, 50)"

# TC4 - Boundary test
python run_scenario.py S002_multi_geofence.jsonc \
 --output trajectory_S002_TC4.json \
 --mode auto --command "move_to_position(601, 0, 50)"
```

**Analyze results locally**:
```bash
cd scripts
python detect_violations.py ../test_logs/trajectory_S002_TC1.json \
 -g ../ground_truth/S002_violations.json
```

## Key Differences from S001

| Aspect | S001 | S002 |
|--------|------|------|
| **Geofences** | 1 (single) | **2 (multiple)** |
| **Test Cases** | 1 | **4** |
| **Complexity** | Basic | **Intermediate** |
| **Check Logic** | Distance to one center | **Distance to ALL centers** |
| **Priority** | N/A | **Zone priority levels** |
| **Violations Tested** | 1 type | **2 types** |
| **Safe Flights** | 0 | **2 (TC3, TC4)** |
| **Boundary Tests** | 0 | **1 (TC4)** |
| **Trajectory Points** | 1 | **577** |
| **Flight Time** | 0s | **58.2s** |

## Extension Ideas
- Add 3rd no-fly zone (create triangular safe corridor)
- Dynamic priority (time-based hospital restrictions)
- Overlapping geofences
- Rectangular/polygonal zones
- Flight path optimization through safe corridors

## Related Scenarios
- **S001**: Prerequisite - single geofence
- **S003**: Next - priority-based conflict resolution
- **S004**: Airport-specific geofence rules

