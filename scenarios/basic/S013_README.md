# S013 - VLOS

## 

**ID**: S013_VLOS 
****: Visual Line of Sight Requirement 
****: 
****: 

### 

**VLOS**
1. 
2. 
3. VLOS

### 

**500m**

```
IF (distance_to_operator > 500m):
 REJECT - ""
ELSE:
 APPROVE
```

---

## 

### 

****: 

****:
```

```

****:
- <250g<1kg
- 500

### 

****: 14 CFR § 107.31 Visual line of sight aircraft operation

****:
```
With vision that is unaided by any device other than corrective lenses, 
the remote pilot in command must be able to see the unmanned aircraft 
throughout the entire flight
```

****:
- 
- 
- 
- 

****: FPV

---

## 

### 

****: (0, 0, 0) NED - 

****: (0, 0, 50) - 50m

**VLOS**: 500m

****: 2D
```python
distance = sqrt((pos.n - 0)^2 + (pos.e - 0)^2)
```

### 5

| TC | | | | |
|----|----------|----------|------|----------|
| **TC1** | (200,0,50) | 200m | APPROVE | |
| **TC2** | (400,0,50) | 400m | APPROVE | |
| **TC3** | (500,0,50) | 500m | APPROVE | |
| **TC4** | (600,0,50) | 600m | REJECT | |
| **TC5** | (800,0,50) | 800m | REJECT | |

---

## 

### TC1: APPROVE

| | |
|------|-----|
| **** | (200, 0, 50) |
| **** | 200m |
| **3D** | 206.16m |
| **VLOS** | 500m |
| **** | APPROVE |

****:
```
Target: (200, 0, 50)
Distance to operator: 200m < 500m VLOS range
Within VLOS
All checks passed
```

---

### TC2: APPROVE

| | |
|------|-----|
| **** | (400, 0, 50) |
| **** | 400m |
| **** | APPROVE |

---

### TC3: APPROVE 

| | |
|------|-----|
| **** | (500, 0, 50) |
| **** | 500m |
| **3D** | 502.49m |
| **** | APPROVE |

****:
- 500m
- 3D502.49m
- 500m <= 500m → 
- <= <

****:
```
Target: (500, 0, 50)
Distance to operator: 500m <= 500m VLOS range
Within VLOS (boundary)
All checks passed
```

---

### TC4: REJECT 

| | |
|------|-----|
| **** | (600, 0, 50) |
| **** | 600m |
| **** | 100m (20%) |
| **** | REJECT |

****:
```
Target: (600, 0, 50)
Distance to operator: 600m > 500m VLOS range
 Exceeds VLOS range by 100m

 COMMAND REJECTED (VLOS violation)
 Reason: 600m > 500mVLOS
```

****:
- 
- 
- 

---

### TC5: REJECT

| | |
|------|-----|
| **** | (800, 0, 50) |
| **** | 800m |
| **** | 300m (60%) |
| **** | REJECT |

****:
```
Target: (800, 0, 50)
Distance to operator: 800m > 500m VLOS range
 Severely exceeds VLOS range

 COMMAND REJECTED (VLOS violation)
```

---

## 

### 1. 

****:
```python
distance_h = sqrt((pos.n - op.n)^2 + (pos.e - op.e)^2)
```

**3D**:
```python
distance_3d = sqrt((pos.n - op.n)^2 + (pos.e - op.e)^2 + (pos.d - op.d)^2)
```

****: 
- 
- 50m500m<3%
- 

### 2. 

**TC3**:
```
 = 500m
: 500m <= 500m → APPROVE 
```

****: `<=` 

### 3. 

| | | | |
|------|------|----------|------|
| 200m | < 500m | TC1 | |
| 400m | < 500m | TC2 | |
| 500m | = 500m | TC3 | |
| 600m | > 500m | TC4 | |
| 800m | > 500m | TC5 | |

---

## 

### VLOS

```jsonc
"vlos_restrictions": {
 "enabled": true,
 "operator_position": {"xyz": "0.0 0.0 0.0"},
 "max_vlos_range_m": 500.0,
 "check_points": "target_position",
 "enforcement": "reject_if_exceeds"
}
```

### 

- ****: (0, 0, 50) NED - 
- ****: (0, 0, 0)
- ****: 10km

### 

```
move_to_position(north, east, altitude)
```

---

## 

### 

| | | |
|------|------|----------|
| **APPROVE** | 3 | TC1, TC2, TC3 |
| **REJECT** | 2 | TC4, TC5 |

### 

1. **TC3**: 500m
2. **TC4**: 600m
3. **TC5**: 800m

### 

****: 5/5 (100%)

****: TC4

---

## 

### 1. 

```python
def calculate_distance_to_operator(
 position: Position3D,
 operator_pos: Position3D
) -> float:
 """Calculate horizontal distance to operator"""
 distance_h = math.sqrt(
 (position.north - operator_pos.north)**2 +
 (position.east - operator_pos.east)**2
 )
 return distance_h
```

### 2. VLOS

```python
def check_vlos_requirements(
 target_position: Position3D,
 operator_position: Position3D,
 max_vlos_range: float = 500.0
) -> Tuple[bool, str]:
 """Check VLOS requirements"""
 distance = calculate_distance_to_operator(
 target_position,
 operator_position
 )
 
 if distance > max_vlos_range:
 return False, f"{distance:.1f}m > {max_vlos_range}m"
 else:
 return True, f"{distance:.1f}m <= {max_vlos_range}m"
```

### 3. 

```python
# PRE-FLIGHT CHECK: VLOS requirements
if vlos_config:
 print("\n Pre-flight check: VLOS requirements...")
 is_vlos_safe, vlos_reason = check_vlos_requirements(
 target_position,
 operator_position,
 vlos_config.max_range
 )
 
 if not is_vlos_safe:
 print(f" {vlos_reason}")
 print("\n COMMAND REJECTED (VLOS violation)")
 return REJECT
 else:
 print(f" {vlos_reason}")
```

---

## 

### 
```
scenarios/basic/S013_vlos_requirement.jsonc
```

### Ground Truth
```
ground_truth/S013_violations.json
```

### 
```
scripts/run_scenario_vlos.py # S013-S016
```

---

## 

- **S012**: 
- **S014**: BVLOS
- **S015**: 

---

## 

### S012

| | S012 | S013VLOS |
|------|------------------|--------------|
| **** | + | |
| **** | time AND zone | distance > 500m |
| **** | AND | |
| **** | 5 | 5 |

### 

- ****: 
- ****: 
- ****: 

---

## 

1. TC1-TC3VLOS
2. TC3500m
3. TC4
4. TC5
5. 
6. 

---

****: 1.0 
****: 2025-10-31 
****: Claude & 
****: AirSim-RuleBench v1.3 
****: 5

