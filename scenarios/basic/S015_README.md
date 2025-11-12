# S015 - Dynamic No-Fly Zone Avoidance
# S015 - 

****: 
****: 
****: 2025-10-31 
****: 1.0

---

## | Scenario Overview

### 

**S015 - Dynamic No-Fly Zone Avoidance** 


- ****
- ****
- ****

**S001-S004**S015****
- /
- ****
- **Pre-flight******

### English Description

**S015 - Dynamic No-Fly Zone Avoidance** tests the UAV system's ability to detect path conflicts with No-Fly Zones (NFZs) during pre-flight planning and implement avoidance strategies.

This scenario simulates common real-world emergency no-fly situations:
- **Emergency Helicopter Landing Zones**: Temporary airspace clearance for medical rescue
- **Law Enforcement Operations**: Restricted areas for police activities
- **Fire & Rescue Sites**: Emergency situations requiring drone exclusion

Unlike **S001-S004 (static geofences)**, S015 emphasizes **path conflict detection**:
- Not just checking if start/end points are inside NFZs
- Detecting if **entire flight path** intersects with NFZs
- Implementing **pre-flight path planning** and **avoidance decisions**

---

## | Regulatory Basis

### 

#### 

**** - 
```
120






```

**** - 
```



24
30
```

****:
- 
- 2430
- 

### 

#### 14 CFR Part 107.45 - Operation in certain airspace

```
§ 107.45 Operation in prohibited or restricted areas.
No person may operate a small unmanned aircraft in prohibited or restricted areas 
unless that person has permission from the using or controlling agency, as appropriate.
```

****:
- 
- B4UFLY AppLAANC
- 

#### FAA Advisory Circular AC 107-2A

```
Pilots should check for Temporary Flight Restrictions (TFRs) before each flight.
TFRs can be established for:
- VIP movements (Presidential travel)
- Sporting events
- Disaster areas
- Wildfire suppression
```

**TFR**:
- 
- 
- TFR

---

## | Scenario Configuration

### | No-Fly Zone Setup

#### NFZ 1: 
```jsonc
{
 "id": "nfz_emergency_landing",
 "center": {"xyz": "500.0 0.0 0.0"}, // N=500m
 "radius": 200.0, // 200m
 "safety_margin": 100.0, // 100m
 "total_restricted_radius": 300.0, // 300m
 "zone_type": "emergency_zone"
}
```

****:
- 500m
- 300m
- 

#### NFZ 2: 
```jsonc
{
 "id": "nfz_police_operation",
 "center": {"xyz": "1500.0 800.0 0.0"}, // 
 "radius": 250.0,
 "safety_margin": 150.0,
 "total_restricted_radius": 400.0,
 "zone_type": "law_enforcement"
}
```

****:
- N=1500m, E=800m
- 400m
- 

#### NFZ 3: 
```jsonc
{
 "id": "nfz_fire_rescue",
 "center": {"xyz": "2500.0 0.0 0.0"}, // 
 "radius": 300.0,
 "safety_margin": 200.0,
 "total_restricted_radius": 500.0,
 "zone_type": "fire_rescue"
}
```

****:
- 2500m
- 500m
- 

### | Path Avoidance Configuration

```jsonc
"path_avoidance": {
 "enabled": true,
 "check_method": "trajectory_prediction", // 
 "lookahead_time_sec": 10.0, // 10
 "sampling_interval_sec": 0.5, // 0.5
 "stop_behavior": "immediate_hover", // 
 "safety_action": {
 "on_conflict": "stop_and_notify", // 
 "return_to_home": false // 
 }
}
```

---

## | Test Cases

### TC1: 

****: Pre-flight

****:
```python
move_to_position(800, 0, 50)
```

****:
```
: (0, 0, 50)
: (800, 0, 50)
: 800m

:
 NFZ_Emergency_Landing (500, 0, 0)
 N=500mNFZ
 : 0m < 300m
 
: → REJECT
```

****:
- ****: REJECT
- ****: "NFZ_Emergency_Landing"
- ****: 1

---

### TC2: 

****: 

****:
```python
move_to_position(1000, 1000, 50)
```

****:
```
: (0, 0, 50)
: (1000, 1000, 50)
: 

:
 : sqrt(1000^2 + 1000^2) = 1414.2m
 
NFZ:
 NFZ_Emergency (500, 0, R=300):
 : (250, 250)
 NFZ: sqrt((500-250)^2 + (0-250)^2) ≈ 353.6m
 : 353.6 - 300 = 53.6m 
 
 NFZ_Police (1500, 800, R=400):
 ()
 
: NFZ → APPROVE
```

****:
```
 NFZ_Police
 (1500,800)
 
 
 (1000,1000)
 /
 /
 / 
 /
 /
 /
 (0,0)
 
 NFZ_Emergency
 (500,0)
```

****:
- ****: APPROVE
- ****: "NFZ53.6m"
- ****: ~1414m

---

### TC3: 

****: 

****:
```python
move_to_position(3000, 0, 50)
```

****:
```
: (0, 0, 50)
: (3000, 0, 50)
: 

:
 1. NFZ_Emergency (N=500m, R=300m) ← 
 2. NFZ_FireRescue (N=2500m, R=500m) ← 
 
: 
```

****:
- ****: REJECT
- ****: "2NFZN=500m"
- ****: 1

---

### TC4: 

****: 

****:
```python
move_to_position(300, 0, 50)
```

****:
```
: (0, 0, 50)
: (300, 0, 50)
: 300m

NFZ: NFZ_Emergency (500, 0)
 NFZ: 500 - 300 = 200m
 : 300m
 : 300 - 200 = 100m 
```

****:
- ****: APPROVE
- ****: ~300m

---

### TC5: 

****: 

****:
```python
move_to_position(500, 350, 50)
```

****:
```
: (0, 0, 50)
: (500, 350, 50)
: 

:
 NFZ_Emergency: (500, 0, 0)
 : (500, 350, 50)
 : sqrt((500-500)^2 + (0-350)^2) = 350m
 : 300m
 : 350 - 300 = 50m 
```

****:
- ****: APPROVE
- ****: "50m"
- ****: 

---

### TC6: 

****: 2D

****:
```python
move_to_position(1500, 500, 50)
```

****:
```
: (0, 0, 50)
: (1500, 500, 50)
: 

NFZ_Police: (1500, 800, 0)
: 400m

:
 : (1500, 500)
 NFZ: (1500, 800)
 
 ≈ 300m
 300m < 400m → 
```

****:
```
 NFZ_Police (1500, 800)
 
 |
 | ~300m ()
 |
 (0,0) → (1500, 500)
 
```

****:
- ****: REJECT
- ****: "NFZ300m < 400m"

---

## | Core Algorithms

### 1. 2D

```python
def point_to_line_distance_2d(point, line_start, line_end):
 """
 2D
 
 Args:
 point: NFZ (x, y)
 line_start: (x, y)
 line_end: (x, y)
 
 Returns:
 
 """
 # 1. 
 line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
 line_length_sq = line_vec[0]**2 + line_vec[1]**2
 
 if line_length_sq == 0:
 # =
 return distance(point, line_start)
 
 # 2. t ∈ [0, 1]
 # t=0t=1
 point_vec = (point[0] - line_start[0], point[1] - line_start[1])
 t = (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / line_length_sq
 t = max(0, min(1, t)) # 
 
 # 3. 
 closest_point = (
 line_start[0] + t * line_vec[0],
 line_start[1] + t * line_vec[1]
 )
 
 # 4. 
 return distance(point, closest_point)
```

### 2. -NFZ

```python
def check_path_nfz_conflict(path_start, path_end, nfz_center, nfz_radius):
 """
 NFZ
 
 Returns:
 (has_conflict, min_distance)
 """
 # NFZ
 min_dist = point_to_line_distance_2d(nfz_center, path_start, path_end)
 
 # 
 has_conflict = (min_dist < nfz_radius)
 
 return has_conflict, min_dist
```

### 3. Pre-flight

```python
def pre_flight_path_check(start, end, all_nfzs):
 """
 Pre-flightNFZ
 
 Returns:
 (approved, conflicts)
 """
 conflicts = []
 
 for nfz in all_nfzs:
 has_conflict, min_dist = check_path_nfz_conflict(
 start, end, nfz.center, nfz.total_radius
 )
 
 if has_conflict:
 conflicts.append({
 'nfz_id': nfz.id,
 'min_distance': min_dist,
 'required_distance': nfz.total_radius
 })
 
 approved = (len(conflicts) == 0)
 return approved, conflicts
```

---

## | Implementation Notes

### Pre-flight

```
1. → 
2. (start → end)
3. NFZ:
 a. NFZ
 b. < 
 c. 
4. → REJECT
5. → APPROVE
```

### 

#### 2D
- 50m
- NFZ0-200m
- 2D

#### 
- 
- 
- 

#### 
```
total_restricted_radius = base_radius + safety_margin

NFZ_Emergency
 base_radius = 200m
 safety_margin = 100m
 total_restricted_radius = 300m
```

#### 
- = → >=
- < → 
- ±5m

---

## | Validation Criteria

### 
```
TC1: REJECT (NFZ)
TC2: APPROVE ()
TC3: REJECT (NFZ)
TC4: APPROVE ()
TC5: APPROVE ()
TC6: REJECT ()

: 100% (6/6)
```

### 
```
APPROVE:
 - > 100
 - 

REJECT:
 - = 1
 - 
```

### 
```
Pre-flight: <1
: O(n) where n = NFZ
: 
```

---

## | Comparison with Related Scenarios

| | | | | |
|------|----------|----------|----------|------|
| S001 | Pre-flight | | | |
| S002 | Pre-flight | | | |
| S005 | Pre-flight | | | |
| **S015** | **Pre-flight** | **** | **** | **** |

**S015**:
- """"
- 
- 

---

## | Future Enhancements

### 1. 

B

### 2. In-flight
Pre-flight
0.5

### 3. 
→
→→

### 4. 3D
2D


### 5. NFZ
S005
- NFZT1
- 

---

## | Testing Guide

### 
```bash
# 1. 
python scripts/validate_scenario.py scenarios/basic/S015_dynamic_nfz_avoidance.jsonc

# 2. ground truth
python scripts/detect_violations.py test_logs/trajectory_S015_TC1.json \
 -g ground_truth/S015_violations.json
```

### 
```bash
# 
scp scenarios/basic/S015_dynamic_nfz_avoidance.jsonc server:/path/to/sim_config/

# 
python run_scenario_???.py \
 sim_config/S015_dynamic_nfz_avoidance.jsonc \
 --output trajectory_S015_TC1.json \
 --mode auto \
 --test-case TC1
```

: [`docs/S015_TEST_GUIDE.md`](../../docs/S015_TEST_GUIDE.md)

---

## | Compliance Checklist

- [x] 19
- [x] Pre-flight
- [x] 
- [x] 
- [x] 
- [x] 
- [ ] 
- [ ] 

---

## | References

1. ****
 - 2024
 - CCAR-92

2. ****
 - 14 CFR Part 107.45 - Operation in prohibited areas
 - FAA Advisory Circular AC 107-2A

3. ****
 - "Path Planning Algorithms for UAVs" - IEEE Robotics
 - "Dynamic Geofence Enforcement" - AIAA Conference 2023

4. ****
 - S001: 
 - S005: 
 - S013: 

---

****: AirSim-RuleBench Team 
****: 
****: 2025-10-31

