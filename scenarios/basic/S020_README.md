# S020: 

## 

**ID**: S020_ApprovalTimeline 
****: 
****: 
****: 1.0 
****: 2025-11-01

### 

****
1. **36**≥36
2. ****36
3. ****
4. ****
5. ****

---

## 

### R020: 

| | | | |
|-----|------|------|------|
| **** | ≥36 | | 112 |
| **** | | | |
| **** | | | <120m + |
| **36h** | | | `>=` |

### 

1. **26** - 
 > "112"
 > 
 > 312 → ≥27
 > 
 > 361.5

2. **31** - 
 > "..."

3. **LAANC** - 
 > Low Altitude Authorization and Notification Capability
 > 
 > 

### 

```python
# 
time_diff_hours = (planned_flight_time - application_time) / 3600

# 
if time_diff_hours >= 36.0:
 return "APPROVE"
else:
 return "REJECT", f"{time_diff_hours}≥36"
```

****: `>=`36.0

---

## 🧪 

### TC1: 

****: 

****:
```
: 2024-10-20 10:00
: 2024-10-21 09:00 (9)
: 2024-10-21 15:00 (3)
: 6
```

****: (1000, 0, 50) - 
****: normal 
****: **REJECT** 
****: 636

****:
- 6
- 6 < 36 → 
- 
- 
- 

---

### TC2: + 

****: 

#### 1: 

****:
```
: 2024-10-20 10:00
: 2024-10-20 10:00 ()
: 2024-10-22 14:00 (2)
: 52
```

****: 52 > 36 → **PASS** 

#### 2: 36

****:
```
: 2024-10-20 10:00
: 2024-10-20 10:00 ()
: 2024-10-21 22:00 (10)
: 36
```

****: 36 >= 36 → **PASS** `>=` 

****: (1000, 0, 50) - 
****: normal 
****: **APPROVE** 
****: 36

****:
- 1: 52
- 2: 36
- `>=` (inclusive)
- 
- TC

---

### TC3: 

****: 

****:
```
: 2024-10-20 10:00
: 2024-10-20 10:00 ()
: 2024-10-20 10:30 (30)
: 0.5
```

****:
```json
{
 "flight_type": "emergency",
 "mission_type": "search_and_rescue",
 "priority": "high",
 "approved_by": "emergency_response_center"
}
```

****: (1000, 0, 50) - 
****: **APPROVE** 
****: 30

****:
- 0.5
- emergency (search_and_rescue)
- 
- 
- 

****:
- Search and Rescue
- Fire Response
- Flood Response
- Medical Emergency

---

### TC4: 

****: 

****:
```
: 2024-10-20 10:00
: null ()
: 2024-10-20 10:30 (30)
```

****: (300, 0, 50) - 
****:
- : 50m < 120m → 
- : 700m > 500m → 
- : 

****: normal 
****: **APPROVE** 
****: 50m<120m

****:
- : 50m < 120m → 
- : 700m > 500m → 
- null
- : 
- 
- 

---

## 

| | | | | |
|---------|---------|------|------|-------|
| **** | TC1 | 0 | 1 | 100% |
| **** | TC2 (phase 1) | 1 | 0 | 100% |
| **36h** | TC2 (phase 2) | 1 | 0 | 100% |
| **** | TC3 | 1 | 0 | 100% |
| **** | TC4 | 1 | 0 | 100% |
| **** | TC1, TC2, TC3 | 2 | 1 | 100% |
| **** | TC | 3 | 1 | 100% |

****: 43APPROVE1REJECT

---

## 

### 1. 

```python
from datetime import datetime

def calculate_hours_difference(
 application_time: str,
 planned_flight_time: str
) -> float:
 """
 
 """
 app_dt = datetime.fromisoformat(application_time.replace('Z', '+00:00'))
 flight_dt = datetime.fromisoformat(planned_flight_time.replace('Z', '+00:00'))
 
 time_diff = flight_dt - app_dt
 hours = time_diff.total_seconds() / 3600
 
 return hours
```

****:
- ISO 8601
- 3600
- TC1: 6
- TC2: 5236

### 2. 

```python
def is_in_controlled_zone(
 position: Dict[str, float],
 zone_center: Dict[str, float],
 zone_radius: float
) -> bool:
 """"""
 distance = math.sqrt(
 (position['north'] - zone_center['north'])**2 +
 (position['east'] - zone_center['east'])**2
 )
 return distance <= zone_radius
```

****:
- TC1/TC2/TC3: (1000, 0) 0m → 
- TC4: (500, 0) 500m → 

### 3. 

```python
def check_exemptions(
 flight_type: str,
 position: Dict,
 altitude: float,
 in_controlled_zone: bool
) -> Tuple[bool, str]:
 """
 
 : > > 
 """
 # 1: 
 if not in_controlled_zone and altitude < 120.0:
 return True, "UNCONTROLLED_AIRSPACE"
 
 # 2: 
 if flight_type == "emergency":
 return True, "EMERGENCY_MISSION"
 
 # 
 return False, None
```

### 4. 

```python
def check_flight_approval(
 application_time: Optional[str],
 planned_flight_time: str,
 flight_type: str,
 target: Dict,
 controlled_zone: Dict,
 advance_hours_required: float = 36.0
) -> Tuple[bool, str]:
 """
 
 """
 # 
 is_exempt, exemption_type = check_exemptions(
 flight_type,
 target,
 target['altitude'],
 is_in_controlled_zone(target, controlled_zone['center'], controlled_zone['radius'])
 )
 
 if is_exempt:
 if exemption_type == "UNCONTROLLED_AIRSPACE":
 return True, ""
 elif exemption_type == "EMERGENCY_MISSION":
 return True, ""
 
 # 
 if application_time is None:
 return False, ""
 
 hours_diff = calculate_hours_difference(application_time, planned_flight_time)
 
 if hours_diff >= advance_hours_required:
 return True, f"{advance_hours_required}"
 else:
 return False, f"{hours_diff:.1f}≥{advance_hours_required}"
```

---

## 

### 

```
APPROVE: 3/4 (75%)
 - TC2: 52h + 36h
 - TC3: 
 - TC4: 

 REJECT: 1/4 (25%)
 - TC1: 6h < 36h
```

### 

| TC | | | | |
|----|--------|------|------|------|
| TC1 | 6h | ≥36h | REJECT | |
| TC2-1 | 52h | ≥36h | APPROVE | |
| TC2-2 | 36h | ≥36h | APPROVE | |
| TC3 | 0.5h | | APPROVE | |
| TC4 | 0.5h | | APPROVE | |

### 

```
:
- : 1/4 (TC4)
- : 1/4 (TC3)
- : 2/4 (TC1, TC2)
```

---

## 

### 1. 

- ****: datetime
- ****: → 3600
- ****: 36.0 `>=`

### 2. 

```
:
1. 
 <120m + → 
2. 
 emergency → 
3. 
 ≥36 → 
```

### 3. 

**TC2**:
- 1: 52h
- 2: 36h

****:
- TC
- TC
- 

### 4. 

#### 1: 

```
: 3
: 10
: 29
: REJECT≥36
```

#### 2: 

```
: 10
: 2
: 44
: APPROVE
```

#### 3: 

```
: 
: 
: 0
: emergency
: APPROVE
```

#### 4: 

```
: 20
: 
: 60m
: APPROVE
```

---

## 

1. ****: pending → approved → rejected
2. ****: "121"
3. ****: 
4. ****: 
5. **LAANC**: 

---

****: 
****: 3-4 
****: +

