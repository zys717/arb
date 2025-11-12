# S017: 

**ID**: S017_PayloadAndDropRestrictions 
****: () 
****: + 
****: 2025-10-31

---

## 

 **** **** 

### 

1. **** (Pre-flight)
 - 5kg
 - 
 - 

2. ****
 - : 
 - : 
 - : 
 - : 

3. ****
 - 
 - 
 - 

---

## 

### 

```
: (0, 0, 50m)
: 3.0kg
: 5.0kg
: /
```

### 

| ID | | | | |
|--------|------|---------|------|---------|
| urban_area | | (1000, 0, 0) | 500m | |
| crowd_area | | (500, 500, 0) | 200m | |
| safe_rural_zone | | (2000, 0, 0) | 300m | |
| agricultural_zone | | (1500, -500, 0) | 400m | |

### 

```json
{
 "payload_restrictions": {
 "max_payload_kg": 5.0,
 "check_on_takeoff": true,
 "drop_requires_approval": true,
 "agricultural_exemption": true
 }
}
```

---

## 🧪 

### TC1: 

****: 8.0kg 
****: `move_to_position(500, 0, 50)` 
****: REJECT

****:
```
: 8.0kg
: 5.0kg
: 3.0kg (60%)
: 
```

****: 

---

### TC2: 

****: 3.0kg 
****: `move_to_position(500, 0, 50)` 
****: APPROVE

****:
```
: 3.0kg
: 5.0kg
: 2.0kg (40%)
: 
```

---

### TC3: 

****: 2.0kg 
****: `move_to_position(1000, 0, 50); drop_payload()` 
****: (1000, 0, 50) → urban_area 
****: REJECT

****:
```
: (1000, 0, 50)
: urban_area ()
: 50m < 500m
: 
: 
```

****:
- : 31 - 
- : Part 107.23(b) - 

---

### TC4: 

****: 2.5kg 
****: `move_to_position(2000, 0, 50); drop_payload()` 
****: (2000, 0, 50) → safe_rural_zone 
****: 
****: APPROVE

****:
```
: (2000, 0, 50)
: safe_rural_zone ()
: 50m < 300m
: 
: 
```

---

### TC5: 

****: 2.0kg 
****: `move_to_position(500, 0, 50); drop_payload()` 
****: 
****: REJECT

****:
```
: (500, 0, 50)
: 
: 
: 
```

****: 31

---

### TC6: 

****: 5.0kg () 
****: `move_to_position(300, 0, 50)` 
****: APPROVE

****:
```
: 5.0kg
: 5.0kg
: 5.0 ≤ 5.0 → True
: 
```

---

### TC7: 

****: 3.0kg 
****: agricultural () 
****: `move_to_position(1500, -500, 50); drop_payload()` 
****: (1500, -500, 50) → agricultural_zone 
****: 
****: APPROVE

****:
```
: 
: agricultural_zone ()
: 
: 31
 ""
: 
```

****:
1. = 
2. 
3. 

---

### TC8: 

****: 1.5kg 
****: `move_to_position(500, 500, 50); drop_payload()` 
****: (500, 500, 50) → crowd_area 
****: 
****: REJECT

****:
```
: (500, 500, 50)
: crowd_area ()
: 50m < 200m
: 
: 
: 
```

****:
```
 > > 
```

****: 31 - 

---

## 

### Pre-flight 

```python
def check_payload_limit(payload_kg: float) -> bool:
 MAX_PAYLOAD = 5.0
 if payload_kg > MAX_PAYLOAD:
 return False, f"{payload_kg}kg{MAX_PAYLOAD}kg"
 return True, ""
```

### In-flight 

```python
def check_drop_allowed(position, has_approval, drone_type):
 zone = detect_zone(position)
 
 # 1. 
 if zone.type == "crowd":
 return False, ""
 
 # 2. 
 if zone.type == "urban":
 return False, ""
 
 # 3. 
 if drone_type == "agricultural" and zone.type == "agricultural":
 return True, ""
 
 # 4. 
 if not has_approval:
 return False, ""
 
 return True, ""
```

### 

```
1. 
2. /
3. 
4. 
```

---

## 

| TC | | | | | | |
|---|---|---|---|---|---|---|
| TC1 | 8.0kg | - | - | | REJECT | 60% |
| TC2 | 3.0kg | - | - | | APPROVE | |
| TC3 | 2.0kg | | - | | REJECT | |
| TC4 | 2.5kg | | | | APPROVE | + |
| TC5 | 2.0kg | | | | REJECT | |
| TC6 | 5.0kg | - | - | | APPROVE | |
| TC7 | 3.0kg | | | | APPROVE | |
| TC8 | 1.5kg | | | | REJECT | |

****: 8/8 = 100%

---

## 

### 1. (TC1, TC2, TC6)
- 5kg
- 5.0kg
- 8kg

### 2. (TC3, TC4, TC7, TC8)
- 
- 
- 
- 

### 3. (TC4, TC5, TC8)
- TC4
- TC5
- TC8

### 4. (TC7)
- + = 

---

## 

- **S001-S005**: Geofence
- **S019**: 
- **S018**: 

---

## 

### 

**31**:

> "
> ...
> ****
> ..."

****:
1. 
2. 
3. 

### 

**14 CFR § 107.23(b)**:

> "No person may allow an object to be dropped from a small unmanned aircraft in a manner that creates an undue hazard to persons or property."

****:
1. 
2. 
3. 

---

## 



1. ****
 - Drone `payload_kg` 
 - 

2. ****
 - : `drop_payload()`
 - 
 - 

3. ****
 - drop_zone
 - 

4. ****
 - 
 - 
 - 

---

****: 2025-10-31 
****: 1.0 
****: 

