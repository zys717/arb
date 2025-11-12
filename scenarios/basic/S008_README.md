# S008: 

## 

**ID**: S008_StructureWaiver 
****: (Structure Altitude Waiver) 
****: (4/5) 
****: 

---

## 

FAA Part 107.51(b)

> **14 CFR § 107.51(b)**: "400****400400"

****:
- ****: 120m AGL
- ****: 400~122m
- ****: + 400~122m

---

## 

### 

```
ID: building_1
: (1000, 1000) NED
: 100m AGL
: 121.92m (400)
: 100m + 121.92m = 221.92m
```

****:
- 1 = 0.3048
- 400 = 121.92
- : 121.92m

### 

```
: (2500, 0, ~34m)
: ~2693m ()
: 120m
```

---

## 🧪 

### TC1: 

****: `move_to_position(3000, 0, 150)`

****:
```
: (3000, 0, 150m)
: sqrt((3000-1000)² + (0-1000)²) = 2236m
: 2236m >> 121.92m → 
```

****:
```
 > 121.92m → 
: 150m > 120m → REJECT
```

****: **REJECT** 
****: "150m120m"

****:
- 120m
- 

---

### TC2: 

****: `move_to_position(1000, 1100, 150)`

****:
```
: (1000, 1100, 150m)
: sqrt((1000-1000)² + (1100-1000)²) = 100m
: 100m < 121.92m → 
```

****:
```
 = 100m < 121.92m → 
: 100m() + 121.92m = 221.92m
: 150m < 221.92m → APPROVE
```

****: **APPROVE** 
****: "building_1100m150m221.92m"

****:
- 
- +400
- ****: 150m120m

---

### TC3: 

****: `move_to_position(1000, 1100, 230)`

****:
```
: (1000, 1100, 230m)
: 100m
: 
: 221.92m
```

****:
```
 = 100m < 121.92m → 
: 230m > 221.92m → → REJECT
```

****: **REJECT** 
****: "building_1230m221.92m8.08m"

****:
- 
- """"

---

### TC4: 

****: `move_to_position(1122, 1000, 150)`

****:
```
: (1122, 1000, 150m)
: sqrt((1122-1000)² + (1000-1000)²) = 122m
: 122m vs 121.92m → 
```

****:
```
 = 122m > 121.92m → 
 → 
: 150m > 120m → REJECT
```

****: **REJECT** 
****: "building_1122.0m121.92m120m"

****:
- ****: 122m vs 121.92m0.08m
- >=
- 

---

## 

### 1. 

****:
```python
distance = sqrt((target_north - building_north)² + (target_east - building_east)²)
if distance < waiver_radius:
 waiver_applies = True
```

****: 2D

### 2. 

```
IF :
 max_altitude = building_height + 400ft
ELSE:
 max_altitude = 120m ()
```

### 3. 

```
: 121.92m ()
TC2: 100m < 121.92m → 
TC4: 122m >= 121.92m → 
```

### 4. 

| | | | |
|------|------|-------------|-------------|
| | 400 ft | 121.92 m | 120 m |
| | 400 ft | 121.92 m | 122 m |
| | 400 ft | 121.92 m | 122 m |

****: 121.92m

---

## 

| TC | | | | | | | |
|----|------|--------|------|--------|---------|------|---------|
| TC1 | (3000,0,150) | 2236m | 150m | | N/A | REJECT | |
| TC2 | (1000,1100,150) | 100m | 150m | | 221.92m | APPROVE | |
| TC3 | (1000,1100,230) | 100m | 230m | | 221.92m | REJECT | |
| TC4 | (1122,1000,150) | 122m | 150m | | N/A | REJECT | |

****: 4/4 ()

---

## 

### FAA Part 107.51(b)

****:
> "The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, **unless** the small unmanned aircraft is flown within a 400-foot radius of a structure and does not fly higher than 400 feet above the structure's immediate uppermost limit."

****:
- 
- 
- 

****:
- 
- 
- 
- 

### 

****:
- 19: 120
- 
- 

****:
- 
- 
- vs 

---

## 

### S006 vs S008

| | S006 () | S008 () |
|------|-------------------|------------------|
| | 120m | 221.92m |
| | | |
| | | + |
| | | FAA |

### S007 vs S008

| | S007 () | S008 () |
|------|----------------|------------------|
| | / | |
| | | + |
| | 60/90/120m | +400ft |
| | 3>2>1 | |

****:
- S007 + S008: 
- " vs "

---

## 

### run_scenario.py 



1. ****:
```python
@dataclass
class StructureConfig:
 id: str
 name: str
 location: Position3D # 
 height_agl: float
 waiver_radius: float # 
 waiver_altitude_above_structure: float # 
 total_waiver_altitude: float # 
```

2. ****:
```python
def check_structure_waiver(
 position: Position3D,
 target_altitude: float,
 structures: List[StructureConfig],
 global_limit: float
) -> Tuple[bool, str, Optional[StructureConfig]]:
 """
 
 
 Returns:
 (is_safe, reason, applicable_structure)
 """
 # 1. 
 # 2. 
 # 3. 
 # 4. 
```

3. ****:
```
:
1. S008
2. S007
3. S006
4. S001-S005
```

---

## 

### 1. 

- 121.92m122m
- TC4
- 

### 2. 

- 
- 
- 1

### 3. 3D vs 2D

- ****2D
- 
- 

### 4. NED

- NEDNorth-East-Down
- AGL
- NorthEast

---

## 

1. **FAA Official Documents**:
 - 14 CFR § 107.51(b): https://www.ecfr.gov/current/title-14/section-107.51
 - FAA Advisory Circular AC 107-2A

2. ****:
 - 1 foot = 0.3048 meters (exact)
 - 400 feet = 121.92 meters (exact)

3. ****:
 - Building Inspection Best Practices (FAA)
 - Part 107 Waiver Database (FAA)

---

## 



- [ ] (1000, 1000)
- [ ] 100m
- [ ] 121.92m
- [ ] 221.92m
- [ ] `run_scenario.py``structures`
- [ ] TC1-TC4
- [ ] 



- [ ] TC1: REJECT
- [ ] TC2: APPROVE
- [ ] TC3: REJECT
- [ ] TC4: REJECT
- [ ] ID
- [ ] 

---

****: AirSim-RuleBench Team 
****: 14 CFR § 107.51(b) 
****: 2025-10-22 
****: v1.0

