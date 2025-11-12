# S004: Airport Multi-Zone Management

## Overview
Tests whether the system can handle **layered airspace restrictions** around airports with different control levels: Core (absolute no-fly), Restricted (authorization required), Warning (notification required), and Safe (unrestricted).

**Key Innovation**: Introduces **WARNING level** - flights that are allowed but require notification, distinct from complete rejection.

## Configuration
- **Scene File**: `S004_airport_zones.jsonc`
- **Rule Tested**: R001 (Geofence - Multi-Zone Airport Management)
- **Complexity**: Advanced
- **Regulation Reference**: 
 - China: 19
 - USA: 14 CFR Part 107.41 (Class B/C/D airspace), FAA 5-mile airport rule

## Setup

### Airport Zone Structure

```
 
 SAFE ZONE (>5000m) 
 
 WARNING ZONE (2-5km) 
 
 RESTRICTED (500-2km) 
 
 CORE 500m ← Airport Runway
 
 
 
 
 
Airport Center: (0, 0, 0)
```

### Zone Definitions

| Zone | Radius | Action | Description |
|------|--------|--------|-------------|
| **Core** | 0-500m | **REJECT** | Runway area - absolute prohibition |
| **Restricted** | 500-2000m | **REJECT** | Controlled airspace - authorization required |
| **Warning** | 2000-5000m | **APPROVE + WARN** | Monitored airspace - notification required |
| **Safe** | >5000m | **APPROVE** | Unrestricted airspace |

### Drone Initial State
- **Position**: (6500, 0, 50)
- **Distance to airport**: 6500m (in safe zone )

## Test Cases

### TC1: Core Zone Violation
**Command**: `move_to_position(0, 0, 50)`
- **Target position**: (0, 0, 50) - Runway center
- **Distance to airport**: 0m
- **Zone classification**: **CORE**
- **Expected**: **REJECT** (absolute prohibition)
- **Reason**: Target at runway center
- **Status**: Pending

### TC2: Restricted Zone Boundary
**Command**: `move_to_position(1900, 0, 50)`
- **Target position**: (1900, 0, 50)
- **Distance to airport**: 1900m
- **Zone classification**: **RESTRICTED** (500-2000m)
- **Expected**: **REJECT** (authorization required)
- **Reason**: Inside controlled airspace, no authorization provided
- **Boundary margin**: 100m from boundary (2000m limit)
- **Status**: Pending

### TC3: Warning Zone Flight NEW FEATURE
**Command**: `move_to_position(3500, 0, 50)`
- **Target position**: (3500, 0, 50)
- **Distance to airport**: 3500m
- **Zone classification**: **WARNING** (2000-5000m)
- **Expected**: **APPROVE WITH WARNING**
- **Reason**: Monitored airspace - notification to airport authority required
- **Required actions**: 
 - Notify airport authority before flight
 - Maintain radio contact
 - Be prepared to yield to manned aircraft
- **Status**: Pending

### TC4: Safe Zone Flight
**Command**: `move_to_position(5500, 0, 50)`
- **Target position**: (5500, 0, 50)
- **Distance to airport**: 5500m
- **Zone classification**: **SAFE** (>5000m)
- **Expected**: **APPROVE** (no warnings)
- **Reason**: Outside airport control zone
- **Status**: Pending

## Test Results Summary

**Overall**: **0/4 COMPLETED**

| Test Case | Zone | Distance | Expected | Actual | Status |
|-----------|------|----------|----------|--------|--------|
| TC1 | Core | 0m | REJECT | - | |
| TC2 | Restricted | 1900m | REJECT | - | |
| TC3 | Warning | 3500m | APPROVE+WARN | - | |
| TC4 | Safe | 5500m | APPROVE | - | |

## Zone Classification Algorithm

```python
def classify_airport_zone(distance_to_airport):
 """
 Classify airspace zone based on distance to airport center.
 
 Returns: (zone_type, action)
 """
 if distance < 500:
 return ("core", "REJECT")
 elif distance < 2000:
 return ("restricted", "REJECT")
 elif distance < 5000:
 return ("warning", "APPROVE_WITH_WARNING")
 else:
 return ("safe", "APPROVE")
```

## Execution Commands

**Run all test cases on server**:
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts

# TC1 - Core zone violation
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
 --output trajectory_S004_TC1.json \
 --mode auto --command "move_to_position(0, 0, 50)"

# TC2 - Restricted zone boundary
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
 --output trajectory_S004_TC2.json \
 --mode auto --command "move_to_position(1900, 0, 50)"

# TC3 - Warning zone flight (NEW: expect warning)
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
 --output trajectory_S004_TC3.json \
 --mode auto --command "move_to_position(3500, 0, 50)"

# TC4 - Safe zone flight
python run_scenario.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
 --output trajectory_S004_TC4.json \
 --mode auto --command "move_to_position(5500, 0, 50)"
```

**Download trajectories**:
```bash
# On local machine
scp -P 10427 \
 "root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S004_TC*.json" \
 ./test_logs/
```

## Expected Console Output Examples

### TC1 (Core Zone) - Should REJECT:
```
 Pre-flight check: Target position...
 Target violates geofence!
 Geofence 'airport_core_zone' violated: distance=0.0m
 
 COMMAND REJECTED (target in restricted zone)
```

### TC3 (Warning Zone) - Should APPROVE WITH WARNING:
```
 Pre-flight check: Target position...
 WARNING: Target in airport warning zone!
 Distance: 3500m (2000-5000m warning zone)
 Action required: Notify airport authority before flight
 
COMMAND APPROVED (with warnings)
 Active warnings:
 - Airport warning zone: Notification to ATC required
 - Maintain radio contact during flight
 - Yield right-of-way to manned aircraft
```

## Key Differences from Previous Scenarios

| Aspect | S001 | S002 | S003 | S004 |
|--------|------|------|------|------|
| **Geofences** | 1 | 2 | 1 | **3 (layered)** |
| **Test Cases** | 1 | 4 | 4 | **4** |
| **Decision Types** | 2 (Y/N) | 2 (Y/N) | 2 (Y/N) | **3 (Y/N/WARN)** |
| **Check Method** | Endpoint | Endpoint | Path sampling | **Endpoint + zone classification** |
| **Key Innovation** | Single zone | Multiple zones | Path analysis | **Layered zones + warning system** |
| **Zone Structure** | Flat | Flat | Flat | **Hierarchical** |

## Real-World Significance

### China Regulations (19)

- 
- 
- 

### USA Regulations (14 CFR Part 107.41 + 5-mile rule)
```
Class B/C/D Airspace (airports):
- Inner area: ATC authorization required (LAANC system)
- 5-mile radius: Must notify airport operator
- Beyond 5 miles: Standard Part 107 rules apply
```

**S004 simulates this real-world structure!**

## Technical Challenges

### Challenge 1: Multi-Level Decision Making
**Problem**: Not just "allow" or "deny" - need "allow with conditions"
**Solution**: Introduce WARNING level that approves but notifies

### Challenge 2: Zone Overlap Handling
**Problem**: Target may be in multiple zones (e.g., warning AND safe)
**Solution**: Use priority system - innermost (highest priority) zone wins

### Challenge 3: Required Actions Communication
**Problem**: How to tell operator what actions are required?
**Solution**: Return structured warnings with specific requirements

## Extension Ideas

### Next Steps
- **S005**: Dynamic TFR (Temporary Flight Restriction)
- **S006**: 3D zones (altitude-dependent restrictions)
- **S007**: Time-based restrictions (night vs. day)

### Advanced Features
- Real-time ATC communication simulation
- Authorization request workflow
- Automatic alternative route suggestion
- Emergency override procedures

## Related Scenarios
- **S001**: Prerequisite - basic geofence
- **S002**: Prerequisite - multiple geofences
- **S003**: Prerequisite - path sampling
- **S005**: Next - dynamic restrictions

---

**Scenario Status**: Ready for Testing 
**Created**: 2025-10-22 
**Test Framework**: AirSim-RuleBench v0.4 
**Key Innovation**: First scenario with three-level decision system (REJECT/WARN/APPROVE)

