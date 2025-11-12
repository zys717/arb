# S007: 

**ID**: S007_ZoneAltitudeLimits 
****: 1.0 
****: - 
****: ()

---

## 

### 
********

### 
- //
- 60m/90m/120m
- 
- 

---

## 

### 

****: 120m

****:
- 
- 
- 

****:
```
→ 60m
→ 90m
→ 120m
```

### 

| | | | | |
|---------|---------|---------|---------|---------|
| **** | | | 60m | |
| **** | | | 90m | |
| **** | | | 120m | 19 |

### S006

| | | |
|------|-------------|--------|
| **S006** | 120m | |
| **S007** | 60m/90m/120m | |

---

## 

### 

```
 (Suburban)
 
 : 120m () 
 
 (Urban Edge) 
 
 : 90m 
 
 (Core) 
 
 : 60m 
 (0,0) 
 1000m 
 
 2000m 
 
 2000m 
 
```

### 

| ID | | | | | |
|--------|------|------|------|---------|--------|
| `urban_core` | | (0,0) | 1000m | 60m | 3 () |
| `urban_edge` | | (0,0) | 2000m | 90m | 2 |
| `suburban` | | - | 2000m | 120m | 1 () |

### 

| TC | | | | | | | |
|-----|---------|--------|---------|---------|---------|---------|---------|
| TC1 | (500,0) | 500m | | 50m | 60m | APPROVE | |
| TC2 | (500,0) | 500m | | 60m | 60m | REJECT | |
| TC3 | (500,0) | 500m | | 70m | 60m | REJECT | |
| TC4 | (1500,0) | 1500m | | 80m | 90m | APPROVE | |
| TC5 | (1500,0) | 1500m | | 90m | 90m | REJECT | |
| TC6 | (2500,0) | 2500m | | 110m | 120m | APPROVE | |
| TC7 | (2500,0) | 2500m | | 120m | 120m | REJECT | |
| TC8 | (500,0) | 500m | | 70m | 60m | REJECT | |

#### 

**** :
- TC2: 60m
- TC5: 90m
- TC7: 120m

****:
- TC1-TC3: 500m < 1000m
- TC4-TC5: 1000m < 1500m < 2000m
- TC6-TC7: 2500m > 2000m

****:
- TC8: (2500,0)(500,0)70m
- 

---

## 

### 1. 

```python
def identify_zone(position: Position3D, altitude_zones: List[ZoneConfig]) -> ZoneConfig:
 """
 
 
 
 """
 # 
 sorted_zones = sorted(altitude_zones, key=lambda z: z.priority, reverse=True)
 
 for zone in sorted_zones:
 if is_position_in_zone(position, zone):
 return zone
 
 # 
 return sorted_zones[-1]

def is_position_in_zone(position: Position3D, zone: ZoneConfig) -> bool:
 """"""
 if zone.geometry.type == "circle":
 distance = calculate_horizontal_distance(position, zone.geometry.center)
 return distance < zone.geometry.radius
 elif zone.geometry.type == "infinite":
 # 
 return True # 
 return False
```

****:
1. ****: 3 > 2 > 1
2. ****: 
3. ****: north, east

### 2. 

```python
def check_zone_altitude_limit(
 position: Position3D,
 target_altitude_agl: float,
 altitude_zones: List[ZoneConfig]
) -> Tuple[bool, str, ZoneConfig]:
 """
 
 
 Returns:
 (is_safe, reason, zone)
 """
 # 1. 
 zone = identify_zone(position, altitude_zones)
 
 # 2. 
 if target_altitude_agl >= zone.altitude_limit_agl:
 return (
 False,
 f"{zone.name}{zone.altitude_limit_agl}m"
 f"{target_altitude_agl}m",
 zone
 )
 else:
 margin = zone.altitude_limit_agl - target_altitude_agl
 return (
 True,
 f"{zone.name}{zone.altitude_limit_agl}m"
 f"{target_altitude_agl}m{margin}m",
 zone
 )
```

### 3. 

****
- 
- 

```python
def calculate_horizontal_distance(pos1: Position3D, pos2: Position3D) -> float:
 """"""
 dx = pos1.north - pos2.north
 dy = pos1.east - pos2.east
 return math.sqrt(dx**2 + dy**2)
```

****:
```python
# : (500, 0, -70) → 500m
distance = sqrt((500-0)^2 + (0-0)^2) = 500m
# 500m < 1000m → 
# : 70m vs 60m → 
```

---

## 

### Ground Truth

```json
{
 "scenario_id": "S007_ZoneAltitudeLimits",
 "test_cases": [
 {
 "id": "TC1",
 "target_zone": "urban_core",
 "zone_limit": 60.0,
 "target_altitude": 50.0,
 "expected_decision": "APPROVE"
 },
 {
 "id": "TC2",
 "target_zone": "urban_core",
 "zone_limit": 60.0,
 "target_altitude": 60.0,
 "expected_decision": "REJECT"
 },
 // ... TC3-TC8
 ]
}
```

### 

```bash
# TC1: 
python run_scenario.py S007_zone_altitude_limits.jsonc \
 --output trajectory_S007_TC1.json \
 --mode auto \
 --command "move_to_position(500, 0, 50)"

# TC2: 
python run_scenario.py S007_zone_altitude_limits.jsonc \
 --output trajectory_S007_TC2.json \
 --mode auto \
 --command "move_to_position(500, 0, 60)"

# TC8: 
python run_scenario.py S007_zone_altitude_limits.jsonc \
 --output trajectory_S007_TC8.json \
 --mode auto \
 --command "move_to_position(500, 0, 70)"
```

---

## 

### 1. 
- **S006**: everywhere 120m
- **S007**: different limits in different places

### 2. 
- ****: 
- ****: → → 
- ****: 

### 3. 
- **3**: 60m, 90m, 120m
- ****: `>=`
- ****: 8TC+

---

## 

| | | |
|-----|------|------|
| **S006** | | 120m |
| **S008** | | +400ft |
| **S002** | | geofence |

---

## 

S007

- [ ] **TC1/TC4/TC6 (APPROVE)**: 
- [ ] **TC2/TC5/TC7 (REJECT)**: 3
- [ ] **TC3 (REJECT)**: 
- [ ] **TC8 (REJECT)**: 
- [ ] ****: 
- [ ] ****: 
- [ ] ****: REJECTTC1APPROVETC

---

## 

### 1. 
- ****: ""
- **3**: 

### 2. 
- ****: `sqrt(Δnorth² + Δeast²)`
- ****: 

### 3. 
- ****: 
- **TC8**: 

---

****: 1.0 
****: 2025-10-22 
****: AirSim-RuleBench Team

---

## 

```
: (north, east)
 ↓
: distance = sqrt(north² + east²)
 ↓
:
 < 1000m? → (60m) [3]
 < 2000m? → (90m) [2]
 ≥ 2000m? → (120m) [1]
 ↓
:
 altitude >= zone.limit? → REJECT
 altitude < zone.limit? → APPROVE
```

## 

| | | | | |
|------|---------|---------|---------|--------|
| | TC1 (50m) | TC2 (60m) | TC3 (70m) | 100% |
| | TC4 (80m) | TC5 (90m) | - | 100% |
| | TC6 (110m) | TC7 (120m) | - | 100% |
| | - | - | TC8 | |

****: 8TC3100%

