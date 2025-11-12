# S006: 

**ID**: S006_AltitudeLimit 
****: 1.0 
****: - 
****: ()

---

## 

### 
****120AGL

### 
- 120
- 119m vs 120m vs 121m
- 

---

## 

### 

****: 
****: 

```
120
...
```

****:
- **120**
- **120**
- **120**//

### 

****: 14 CFR Part 107 
****: § 107.51(b)

```
The altitude of the small unmanned aircraft cannot be higher than 
400 feet above ground level, unless the small unmanned aircraft 
is flown within a 400-foot radius of a structure and does not fly 
higher than 400 feet above the structure's immediate uppermost limit.
```

****:
- **400AGL**122
- 400+400S008

### 

| | | | |
|------|------|------|--------|
| **** | 120 | 400AGL (≈122m) | |
| **** | AGL | AGL | |
| **** | 120m | 400ft | |
| **** | | | |

****: 120

---

## 

### 

```jsonc
{
 "altitude_limit_agl": 120.0, // 
 "enforcement_mode": "strict", // 
 "tolerance_margin": 0.0 // 
}
```

### 

- ****: N=0, E=0, **Alt=50m**
- ****: 0m MSLMean Sea Level
- ****: 14:00

### 

| TC | | | | |
|-----|---------|--------|---------|---------|
| TC1 | 50m | -70m | APPROVE | |
| TC2 | 119m | -1m | APPROVE | |
| TC3 | 120m | 0m | REJECT | **** |
| TC4 | 125m | +5m | REJECT | |
| TC5 | 150m | +30m | REJECT | |
| TC6 | 100m | -20m | APPROVE | |

#### 

**TC3**
- "120****" → 120m
- 120m ≥ → REJECT
- 

****
```python
if target_altitude_agl >= 120.0:
 decision = "REJECT"
 reason = "120m"
else:
 decision = "APPROVE"
```

---

## 

### 1. AGL vs MSL

**AGLAbove Ground Level**: 
- ""AGL
- `AGL = MSL - ground_elevation`

**NED**:
- ProjectAirSimNEDNorth-East-Down
- **Down**`down = -AGL`
- `down = -120.0` 120m

****
```python
# 120m
target_down = -120.0 # NED
target_agl = -target_down # AGL120m

# 
ALTITUDE_LIMIT = 120.0
if target_agl >= ALTITUDE_LIMIT:
 decision = "REJECT"
```

### 2. Pre-flight Check

`run_scenario.py`pre-flight check

```python
def check_altitude_limit(target_altitude_agl: float, limit: float = 120.0) -> tuple:
 """
 
 
 Args:
 target_altitude_agl: AGL
 limit: 120m
 
 Returns:
 (is_safe: bool, reason: str)
 """
 if target_altitude_agl >= limit:
 return (
 False,
 f"{target_altitude_agl:.1f}m{limit:.1f}m"
 )
 else:
 margin = limit - target_altitude_agl
 return (
 True,
 f"{target_altitude_agl:.1f}m{margin:.1f}m"
 )
```

### 3. S002

| | | |
|-----|---------|-------------|
| **S002** | 3D geofence | Euclidean distance |
| **S006** | | |

**S002**:
```python
distance = sqrt((Δnorth)² + (Δeast)² + (Δdown)²) # 3D
if distance < geofence_radius:
 violation = True
```

**S006**:
```python
if altitude_agl >= 120.0: # 
 violation = True
```

---

## 

### Ground Truth

```json
{
 "scenario_id": "S006_AltitudeLimit",
 "test_cases": [
 {
 "id": "TC1",
 "expected_violation": false,
 "decision": "APPROVE",
 "reason": "50m < 120m"
 },
 {
 "id": "TC2",
 "expected_violation": false,
 "decision": "APPROVE",
 "reason": "119m < 120m"
 },
 {
 "id": "TC3",
 "expected_violation": true,
 "decision": "REJECT",
 "reason": "120m"
 },
 {
 "id": "TC4",
 "expected_violation": true,
 "decision": "REJECT",
 "reason": "125m > 120m"
 },
 {
 "id": "TC5",
 "expected_violation": true,
 "decision": "REJECT",
 "reason": "150m >> 120m"
 },
 {
 "id": "TC6",
 "expected_violation": false,
 "decision": "APPROVE",
 "reason": "100m < 120m"
 }
 ]
}
```

### 

```bash
# TC1: 50m
python run_scenario.py S006_altitude_limit.jsonc \
 --output trajectory_S006_TC1.json \
 --mode auto \
 --command "move_to_position(100, 0, 50)"

# TC3: 120m
python run_scenario.py S006_altitude_limit.jsonc \
 --output trajectory_S006_TC3.json \
 --mode auto \
 --command "move_to_position(100, 0, 120)"

# TC5: 150m
python run_scenario.py S006_altitude_limit.jsonc \
 --output trajectory_S006_TC5.json \
 --mode auto \
 --command "move_to_position(100, 0, 150)"
```

---

## 

### 1. 
- ****"120"120m
- ****120m vs 400ft
- **AGL vs MSL**

### 2. 
- ****119m vs 120m vs 121m
- ****`>=` vs `>` 
- ****NED → AGL

### 3. 
- ****geofence
- ****tolerance_margin0
- ****S007S008

---

## 

| | | |
|-----|------|------|
| **S007** | | 60m vs 120m |
| **S008** | | 400ft+400ft |
| **S002** | | 3D |

---

## 

S006

- [ ] **TC1-TC2 (APPROVE)**: 120m
- [ ] **TC3 (REJECT)**: 120m
- [ ] **TC4-TC5 (REJECT)**: 120m
- [ ] ****: "120m"""
- [ ] ****: Part 107.51
- [ ] ****: NEDAGL
- [ ] ****: REJECT1

---

## 

### 1. 
- ****`altitude >= 120.0` → REJECT
- 120""120
- 

### 2. NED
- **ProjectAirSimNED**Down
- ****`down=-120.0`120m
- ****`AGL = -down`

### 3. geofence
- **Geofence**: +3D
- **Altitude limit**: 
- ****: geofence

---

****: 1.0 
****: 2025-10-22 
****: AirSim-RuleBench Team

---

## 

### 

```
 



120


...
```

### 14 CFR § 107.51(b)

```
§ 107.51 Operating limitations for small unmanned aircraft.

(b) The altitude of the small unmanned aircraft cannot be higher than 
400 feet above ground level, unless the small unmanned aircraft is 
flown within a 400-foot radius of a structure and does not fly higher 
than 400 feet above the structure's immediate uppermost limit.
```

