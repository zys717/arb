# S011 - 

## 

**ID**: S011_NightFlight 
****: 
****: 
****: + + 

### 

****

### 

1. ****: 18:30-05:30
2. ****: 
3. ****: 
4. ****: Civil Twilight18:29 vs 18:3005:29 vs 05:30

---

## 

### 

****: 

****: 

****:
```


```

****:
- 
- 
- 

### 

****: 14 CFR Part 107

****: § 107.29 Operation at night (2021)

****:
```
§ 107.29 Operation at night.
(a) No person may operate a small unmanned aircraft system during 
 night unless:
 (1) The remote pilot in command has completed an updated initial 
 knowledge test or recurrent training...
 (2) The small unmanned aircraft has lighted anti-collision lighting 
 visible for at least 3 statute miles that has a flash rate 
 sufficient to avoid a collision...
(b) Civil twilight refers to the time period commencing 30 minutes 
 before official sunrise to official sunset.
```

****:
- 
- 3
- Civil Twilight3030

### 

| | | | |
|------|------|------|-----------|
| **** | | 3 | |
| **** | | | |
| **** | | Civil Twilight | 18:30-05:30 |

****

---

## 

### 

```
 05:00 05:30 06:00 18:00 18:30 19:00
 |||...|||
 
 ↓ ↓ ↓ ↓ ↓ ↓
 TC7 TC8 TC1 TC5 TC6 TC2/TC3/TC4
 
```

### 

| TC | | | | | |
|----|------|------|------|------|----------|
| **TC1** | 12:00 | | | APPROVE | |
| **TC2** | 22:00 | | | APPROVE | |
| **TC3** | 22:00 | | | REJECT | |
| **TC4** | 22:00 | | | REJECT | |
| **TC5** | 18:29 | | | APPROVE | 1 |
| **TC6** | 18:30 | | | REJECT | |
| **TC7** | 05:29 | | | REJECT | |
| **TC8** | 05:30 | | | APPROVE | |

****:
- = 
- = /
- = /

---

## 

### TC1: 

****: 12:00

****:
- `12:00`
- 
- 

****: **APPROVE**

****: 

****:
```
12:00 06:00-18:00 → 
is_night = false
```

---

### TC2: 

****: 22:00

****:
- `22:00`
- 
- 

****: **APPROVE**

****: +

****:
```
22:00 >= 18:30 → 
is_night = true
lighting_required = true
training_required = true
```

---

### TC3: 

****: 22:00

****:
- `22:00`
- 
- 

****: **REJECT**

****: "32 / Part 107.29"

****: `missing_anti_collision_light`

****:
- 32
- Part 107.29(a)(2)

****: 

---

### TC4: 

****: 22:00

****:
- `22:00`
- 
- 

****: **REJECT**

****: "Part 107.29"

****: `missing_night_training`

****:
- 
- Part 107.29(a)(1)

****: 
- 
- 
- 

---

### TC5: Civil Twilight18:29 

****: 18:2929Civil Twilight

****:
- `18:29`
- 
- 

****: **APPROVE**

****: 18:29Civil Twilight18:30

****:
```
18:29 < 18:30 → Civil Twilight
is_night = false
is_civil_twilight = true
```

****: 
- ****
- 18:2918:301
- 

---

### TC6: 18:30 

****: 18:30

****:
- `18:30`
- 
- 

****: **REJECT**

****: "18:3030"

****:
```
18:30 >= 18:30 → 
is_night = true
```

**TC5**:
```
TC5: 18:29 → Civil Twilight
TC6: 18:30 → 
 ↑ 1
```

****: 

---

### TC7: 05:29 

****: 05:2931

****:
- `05:29`
- 
- 

****: **REJECT**

****: "05:2905:30"

****:
```
05:29 < 05:30 → 
is_night = true
```

****: 
- 05:2905:30
- 

---

### TC8: 05:30 

****: 05:30Civil Twilight

****:
- `05:30`
- 
- 

****: **APPROVE**

****: 05:30Civil Twilight

****:
```
05:30 >= 05:30 → Civil Twilight
is_night = false
is_civil_twilight = true
```

**TC7**:
```
TC7: 05:29 → 
TC8: 05:30 → Civil Twilight
 ↑ 1
```

****: 

---

## 

### 1. 

****:
```
 = 18:30-05:30
```

****:
```python
is_night = (time >= "18:30") OR (time < "05:30")
```

****:
| | | |
|------|------|------|
| 12:00 | 06:00 <= time < 18:30 | |
| 18:00 | 18:00-18:30 | Civil Twilight |
| 18:29 | time < 18:30 | Civil Twilight |
| 18:30 | time >= 18:30 | **** |
| 22:00 | time >= 18:30 | |
| 00:00 | time < 05:30 | |
| 05:29 | time < 05:30 | |
| 05:30 | time >= 05:30 AND time < 06:00 | Civil Twilight |
| 06:00 | time >= 06:00 | |

### 2. 

****:
```
18:29 (TC5) → APPROVE Civil Twilight
18:30 (TC6) → REJECT 
 ↑ 1
```

****:
```
05:29 (TC7) → REJECT 
05:30 (TC8) → APPROVE Civil Twilight
 ↑ 1
```

****:
- 
- >= vs <
- 18:3005:30

### 3. 

****:
```
IF is_night AND NOT anti_collision_light:
 REJECT ("")
```

****:
- TC322:00→ REJECT 
- TC618:30→ REJECT 
- TC705:29→ REJECT 

### 4. 

****:
```
IF is_night AND NOT pilot_night_training:
 REJECT ("")
```

****:
- TC422:00→ REJECT 

---

## 

### 

```jsonc
"time_definitions": {
 "sunrise": "06:00", // 
 "sunset": "18:00", // 
 "civil_twilight_before_sunrise": "05:30", // 30
 "civil_twilight_after_sunset": "18:30" // 30
}
```

### 

```jsonc
"night_period": {
 "definition": "303018:30-05:30",
 "start": "18:30",
 "end": "05:30"
}
```

### 

- ****: (0, 0, 50) NED - 0m0m50m
- ****: (0, 0, 0) - 
- ****: 

### 

****:
```
move_to_position(north, east, altitude)
```

****:
```
move_to_position(300, 0, 50) # 300m
```

****:
```jsonc
{
 "time_of_day": "22:00",
 "drone_config": {
 "anti_collision_light": true,
 "pilot_night_training": true
 }
}
```

---

## 

### 

| | | |
|------|------|----------|
| **APPROVE** | 4 | TC1, TC2, TC5, TC8 |
| **REJECT** | 4 | TC3, TC4, TC6, TC7 |

### 

1. ****: 18:30-05:30
2. ****: TC3/TC6/TC7
3. ****: TC4
4. ****: 
 - TC5(18:29) vs TC6(18:30)
 - TC7(05:29) vs TC8(05:30)

### 

****: 8/8 (100%)

****: TC5/TC6/TC7/TC8

---

## 

### 1. 

```python
from datetime import datetime

def parse_time(time_str: str) -> datetime:
 """HH:MM"""
 return datetime.strptime(time_str, "%H:%M")

def is_night_time(current_time: str, 
 night_start: str = "18:30", 
 night_end: str = "05:30") -> bool:
 """"""
 time = parse_time(current_time)
 start = parse_time(night_start)
 end = parse_time(night_end)
 
 # 18:30-05:30
 return time >= start or time < end
```

### 2. 

****: `>=` `<` `>` `<=`

```python
# 
if time >= "18:30" or time < "05:30":
 is_night = True

# 18:30
if time > "18:30" or time <= "05:30":
 is_night = True
```

### 3. 

```python
def check_lighting_requirement(is_night: bool, 
 has_light: bool) -> Tuple[bool, str]:
 """"""
 if is_night and not has_light:
 return False, ""
 return True, ""
```

### 4. 

```python
def check_training_requirement(is_night: bool, 
 has_training: bool) -> Tuple[bool, str]:
 """"""
 if is_night and not has_training:
 return False, ""
 return True, ""
```

### 5. 

```python
def pre_flight_check_night_rules(time_of_day: str, 
 anti_collision_light: bool,
 pilot_night_training: bool):
 """"""
 # 1. 
 is_night = is_night_time(time_of_day)
 
 if not is_night:
 print(f" {time_of_day}")
 return True, ""
 
 print(f" {time_of_day}...")
 
 # 2. 
 light_ok, light_reason = check_lighting_requirement(
 is_night, anti_collision_light
 )
 if not light_ok:
 return False, light_reason
 
 # 3. 
 training_ok, training_reason = check_training_requirement(
 is_night, pilot_night_training
 )
 if not training_ok:
 return False, training_reason
 
 return True, "+"
```

---

## 

### 
```
scenarios/basic/S011_night_flight.jsonc
```

### Ground Truth
```
ground_truth/S011_violations.json
```

### 
```
scripts/run_scenario_motion.py # 
```

### 
```
docs/S011_TEST_GUIDE.md # 
```

---

## 

- **S012**: 22:00-06:00
- **S009**: 
- **S013**: 

---

## 

### 

- **S001-S008**: 
- **S009-S010**: 
- **S011**: **vs** ← 

### 

- ****: 
- ****: 84
- ****: +
- ****: 

### 

1. ****18:30-05:30
2. ****
3. **** + + 

---

## 

1. 8/
2. TC3/TC6/TC7
3. TC4
4. TC5/TC8Civil Twilight
5. 100%
6. 
7. 

---

****: 1.0 
****: 2025-10-23 
****: Claude & 
****: AirSim-RuleBench v1.0

