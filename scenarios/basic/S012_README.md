# S012 - 

## 

**ID**: S012_TimeWindow 
****: 
****: 
****: + 

### 

****
1. 22:00-06:00
2. 
3. AND+

### 

****: **AND** → 

```
IF (is_in_hospital_zone AND is_in_time_window):
 REJECT
ELSE:
 APPROVE
```

---

## 

### 

****: 

****: 

****:
```
22:00-06:00
 
 
08:00-17:00
 
 
00:00-06:00
 
```

### 

****: 14 CFR Part 107 

**/**: State and Local Ordinances
```
Many states and local governments impose quiet hours or 
time-based restrictions near sensitive areas such as:
 - Hospitals
 - Schools
 - Residential areas
 - Parks
```

****: 

---

## 

### 

****:
- (200, 0, 50) NED - 200m0m50m
- 150m
- 0-120m

****:
- 22:0010
- 06:006
- 
- 

****:
```
REJECT = AND 


 time=false, zone=false → APPROVE
 time=false, zone=true → APPROVE 
 time=true, zone=false → APPROVE 
 time=true, zone=true → REJECT 
```

### 5

| TC | | | | | | |
|----|------|------|----------|--------|------|----------|
| **TC1** | 14:00 | (0,200) | | | APPROVE | |
| **TC2** | 14:00 | (200,0) | | | APPROVE | zone |
| **TC3** | 23:00 | (0,200) | | | APPROVE | time |
| **TC4** | 23:00 | (200,0) | | | REJECT | AND |
| **TC5** | 22:00 | (200,0) | | | REJECT | |

****: TC2/TC3+ TC4

---

## 

### TC1: 

****: 14:00

| | |
|------|-----|
| **** | 14:00 |
| **** | (0, 200, 50) |
| **** | (200, 0, 50) |
| **** | 282.84m > 150m |
| **** | |
| **** | |
| **** | APPROVE |

****:
```
Time: 14:00
Target: (0, 200, 50)
14:0022:00-06:00
282.84m > 150m
All checks passed
```

****: 

---

### TC2: 

****: 14:00

| | |
|------|-----|
| **** | 14:00 |
| **** | (200, 0, 50) |
| **** | (200, 0, 50) |
| **** | 0m < 150m |
| **** | **** |
| **** | |
| **** | APPROVE |

****:
```
Time: 14:00
Target: (200, 0, 50) - 
 0m
14:0022:00-06:00
All checks passed - 
```

****:
- ****
- 
- +
- AND

**S002**:
- S002: → 
- S012: + → 

---

### TC3: 

****: 23:00

| | |
|------|-----|
| **** | 23:00 |
| **** | (0, 200, 50) |
| **** | (200, 0, 50) |
| **** | 282.84m > 150m |
| **** | |
| **** | **** |
| **** | APPROVE |

****:
```
Time: 23:00
Target: (0, 200, 50)
 23:0022:00-06:00
282.84m > 150m
All checks passed - 
```

****:
- ****
- 
- +
- AND

**S011**:
- S011: → +
- S012: + → 

---

### TC4: AND 

****: 23:00

| | |
|------|-----|
| **** | 23:00 |
| **** | (200, 0, 50) |
| **** | (200, 0, 50) |
| **** | 0m < 150m |
| **** | **** |
| **** | **** |
| **** | REJECT |

****:
```
Time: 23:00
Target: (200, 0, 50) - 
 23:0022:00-06:00
 0m < 150m
 COMMAND REJECTED (time window restriction)
 22:00-06:00
```

****:
- ****
- +
- AND
- 

****:
```
time=true AND zone=true → REJECT 
```

---

### TC5: 22:00

****: 22:00

| | |
|------|-----|
| **** | **22:00** |
| **** | (200, 0, 50) |
| **** | (200, 0, 50) |
| **** | 0m |
| **** | |
| **** | 22:00 >= 22:00 |
| **** | REJECT |

****:
```
Time: 22:00
Target: (200, 0, 50)
 22:0022:00 >= 22:00
 
 COMMAND REJECTED (time window restriction)
```

****:
```
22:00 >= 22:00 → 
```

****:
- 22:00
- `>=` `>` 
- 

---

## 

### 1. AND

| | | | |
|----------|--------|------|----------|
| | | APPROVE | TC1 |
| | | APPROVE | TC2 |
| | | APPROVE | TC3 |
| | | REJECT | TC4 |

****: TC2TC3

### 2. S011

****: 22:00-06:00

****:
```python
is_in_time_window = (time >= "22:00") OR (time < "06:00")
```

****:
- 14:00: false
- 22:00: true
- 23:00: true
- 06:00: false

### 3. S002/S010

****: 
- (200, 0, -50)
- 150m
- 0-120m

****:
```python
distance_2d = sqrt((pos.n - 200)^2 + (pos.e - 0)^2)
is_in_hospital = distance_2d <= 150
```

****:
- (200, 0): 0m → 
- (0, 200): 282.84m → 

### 4. 

****:
```python
is_restricted = is_in_time_window AND is_in_hospital_zone

if is_restricted:
 return REJECT, "22:00-06:00"
else:
 return APPROVE
```

---

## 

### 

```jsonc
"restricted_zone": {
 "zone_id": "hospital_zone",
 "zone_type": "cylinder",
 "center": {"north": 200.0, "east": 0.0, "down": -50.0},
 "radius": 150.0,
 "height_min": -120.0,
 "height_max": 0.0
}
```

### 

```jsonc
"time_window": {
 "type": "night_quiet_hours",
 "start": "22:00",
 "end": "06:00",
 "description": ""
}
```

### 

- ****: (0, 0, 50) NED - 
- ****: (0, 0, 0)
- ****: 

### 

```
move_to_position(north, east, altitude)
```

****:
```
move_to_position(200, 0, 50) # 
move_to_position(0, 200, 50) # 
```

---

## 

### 

| | | |
|------|------|----------|
| **APPROVE** | 3 | TC1, TC2, TC3 |
| **REJECT** | 2 | TC4, TC5 |

### 

1. **TC2**: 
2. **TC3**: 
3. **TC4**: 
4. **TC5**: 22:00

### 

****: 5/5 (100%)

****: TC2/TC3/TC4AND

---

## 

### 1. S011

```python
def is_in_time_window(current_time: str, 
 start: str = "22:00", 
 end: str = "06:00") -> bool:
 """"""
 current_min = parse_time(current_time)
 start_min = parse_time(start) # 1320
 end_min = parse_time(end) # 360
 
 # 22:00-23:59 OR 00:00-06:00
 return current_min >= start_min or current_min < end_min
```

### 2. S002/S010

```python
def is_in_hospital_zone(position: Position3D,
 hospital_center: Position3D,
 radius: float = 150.0) -> bool:
 """"""
 distance_2d = math.sqrt(
 (position.north - hospital_center.north)**2 +
 (position.east - hospital_center.east)**2
 )
 return distance_2d <= radius
```

### 3. 

```python
def check_time_window_restriction(
 time_of_day: str,
 target_position: Position3D,
 time_window_config: TimeWindowConfig
) -> Tuple[bool, str]:
 """"""
 
 # 1. 
 is_in_window = is_in_time_window(
 time_of_day,
 time_window_config.start,
 time_window_config.end
 )
 
 # 2. 
 is_in_zone = is_in_hospital_zone(
 target_position,
 time_window_config.zone_center,
 time_window_config.zone_radius
 )
 
 # 3. AND
 if is_in_window and is_in_zone:
 return False, f"{time_window_config.start}-{time_window_config.end}"
 else:
 return True, ""
```

### 4. 

```python
def pre_flight_check_time_window(
 time_of_day: str,
 target_position: Position3D,
 config: ScenarioConfig
):
 """"""
 if not config.time_window:
 return True, ""
 
 print(f" Pre-flight check: Time window restrictions...")
 
 is_safe, reason = check_time_window_restriction(
 time_of_day,
 target_position,
 config.time_window
 )
 
 if not is_safe:
 print(f" {reason}")
 return False, reason
 else:
 print(f" {reason}")
 return True, reason
```

---

## 

### 
```
scenarios/basic/S012_time_window.jsonc
```

### Ground Truth
```
ground_truth/S012_violations.json
```

### 
```
scripts/run_scenario_motion.py # 
```

### 
```
docs/S012_TEST_GUIDE.md # 
```

---

## 

- **S011**: 
- **S002**: 
- **S005**: 
- **S010**: +

---

## 

### S011

| | S011 | S012 |
|------|------------------|------------------|
| **** | | + |
| **** | → + | AND → |
| **** | | |
| **** | | AND |
| **** | 8 | 5 |

### 

- ****: 
- ****: S011
- ****: AND
- ****: 

### 

1. **AND**
2. ****
3. ****S011S002/S010

---

## 

1. TC1
2. TC2
3. TC3
4. TC4+
5. TC522:00
6. 
7. 

---

****: 1.0 
****: 2025-10-31 
****: Claude & 
****: AirSim-RuleBench v1.0 
****: 5S0118AND

