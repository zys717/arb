# S014 - BVLOS Waiver

## 

**ID**: S014_BVLOS_Waiver 
****: Beyond Visual Line of Sight Waiver 
****: 
****: 

### 

**BVLOS**
1. 
2. 
3. VLOS
4. 

### 

****: > 500m → 

****:
```
IF (distance <= 500m):
 APPROVE - "VLOS"
ELSE IF (has_visual_observer_waiver AND distance <= 1100m):
 APPROVE - ""
ELSE IF (has_technical_means_waiver AND distance <= 2000m):
 APPROVE - ""
ELSE IF (has_special_permit_waiver AND distance <= 5000m):
 APPROVE - ""
ELSE:
 REJECT - ""
```

---

## 

### 

****: 

****:
```

```

****:



1. ****
 - 
 - 
 - 1000-1500

2. ****
 - 
 - ADS-B
 - 
 - 2000

3. ****
 - 
 - 
 - 
 - 5000

### 

****: 14 CFR § 107.31 Visual line of sight aircraft operation

****:
```
The remote pilot in command, the person manipulating the flight 
controls of the small unmanned aircraft system, and the visual 
observer (if any) must be able to see the unmanned aircraft 
throughout the entire flight
```

****: § 107.205 - Operations over people / BVLOS Waiver

****:
1. **Visual Observer (VO)**
 - 
 - 
 - 

2. **Detect and Avoid (DAA) Capability**
 - 
 - 
 - ADS-B

3. **Operational Limitations**
 - 
 - 
 - 

****: 
- FAA DroneZone 
- 
- Equivalent Level of Safety
- 90-120 

---

## 

### 

****: (0, 0, 0) NED - 

****: (0, 0, 50) - 50m

**VLOS**: 500m

****:

| | ID | | |
|----------|----|---------|---------| |
| | W001 | 1100m | (600,0,0) |
| | W002 | 2000m | |
| | W003 | 5000m | |

### 6

| TC | | | | | |
|----|----------|------|------|------|----------|
| **TC1** | (400,0,50) | 400m | | APPROVE | VLOS |
| **TC2** | (600,0,50) | 600m | | REJECT | |
| **TC3** | (600,0,50) | 600m | W001 | APPROVE | |
| **TC4** | (1500,0,50) | 1500m | W002 | APPROVE | |
| **TC5** | (3000,0,50) | 3000m | W003 | APPROVE | |
| **TC6** | (6000,0,50) | 6000m | W003 | REJECT | |

---

## 

### TC1: VLOS APPROVE

|| | |
||------|-----|
|| **** | (400, 0, 50) |
|| **** | 400m |
|| **VLOS** | 500m |
|| **** | |
|| **** | APPROVE |

****:
```
Target: (400, 0, 50)
Distance: 400m < 500m (base VLOS)
Within base VLOS range
All checks passed
```

****: - VLOS

---

### TC2: REJECT 

| | |
|------|-----|
| **** | (600, 0, 50) |
| **** | 600m |
| **VLOS** | 500m |
| **** | |
| **** | REJECT |

****:
```
Target: (600, 0, 50)
Distance: 600m > 500m (base VLOS)
 Exceeds VLOS range
 No waiver available

 COMMAND REJECTED (VLOS violation, no waiver)
```

****:
- VLOS
- 
- 

****: - 

---

### TC3: APPROVE 

| | |
|------|-----|
| **** | (600, 0, 50) |
| **** | 600m |
| **** | 0m |
| **VLOS** | 500m |
| **** | (600, 0, 0) |
| **** | 1100m |
| **** | W001_VisualObserver |
| **** | APPROVE |

****:
```
Target: (600, 0, 50)
Distance to operator: 600m > 500m (base VLOS)
Distance to observer: 0m

 Checking waivers...
 Visual Observer waiver enabled
 Observer at (600, 0, 0)
 Target within observer's VLOS (0m < 500m)
 Combined coverage: 0-1100m

WAIVER APPLIED: Visual Observer
All checks passed (with waiver)
```

****:
- 
- 
- → 
- 

****: **** - 

---

### TC4: APPROVE 

| | |
|------|-----|
| **** | (1500, 0, 50) |
| **** | 1500m |
| **VLOS** | 500m |
| **** | 2000m |
| **** | W002_TechnicalMeans |
| **** | APPROVE |

****:
```
Target: (1500, 0, 50)
Distance: 1500m > 500m (base VLOS)

 Checking waivers...
 Technical Means waiver enabled
 Radar coverage: 2000m
 Target within radar range (1500m < 2000m)
 Data link: active
 Real-time tracking: enabled

WAIVER APPLIED: Technical Means (Radar)
All checks passed (with waiver)
```

****:
- 
- 
- → 

****: BVLOS

---

### TC5: APPROVE 

| | |
|------|-----|
| **** | (3000, 0, 50) |
| **** | 3000m |
| **VLOS** | 500m |
| **** | 5000m |
| **** | W003_SpecialPermit |
| **** | APPROVE |

****:
```
Target: (3000, 0, 50)
Distance: 3000m > 500m (base VLOS)

 Checking waivers...
 Special Permit waiver enabled
 Permit: CAAC-BVLOS-2025-001
 Approved area: Test Zone Alpha
 Max range: 5000m
 Target within permit range (3000m < 5000m)

WAIVER APPLIED: Special Permit
All checks passed (with waiver)
```

****:
- 
- 
- → 

****: BVLOS

---

### TC6: REJECT 

| | |
|------|-----|
| **** | (6000, 0, 50) |
| **** | 6000m |
| **** | 5000m |
| **** | 1000m (20%) |
| **** | W003_SpecialPermit |
| **** | REJECT |

****:
```
Target: (6000, 0, 50)
Distance: 6000m > 500m (base VLOS)

 Checking waivers...
 Special Permit waiver enabled
 Permit max range: 5000m
 Target exceeds permit range (6000m > 5000m)

 COMMAND REJECTED (exceeds waiver limit)
 Waiver type: Special Permit
 Waiver limit: 5000m
 Requested distance: 6000m
 Exceeds by: 1000m (20%)
```

****:
- 
- → 
- 

****: **** - 

---

## 

### 1. 

****:
```
1. 
2. VLOS<= 500m
3. → 
4. → 
5. → 
6. → 
7. 
8. → 
9. → 
```

### 2. 

****: Union of Circles

****:
```python
# 
operator_coverage = circle(center=(0,0), radius=500m)

# 
observer_coverage = circle(center=(600,0), radius=500m)

# 
combined_coverage = operator_coverage ∪ observer_coverage

# 
max_distance = 600m (observer_position) + 500m (observer_range) = 1100m
```

****:
- (600,0) → =0 < 500m → 

### 3. 

| | | | |
|----------|----------|--------|----------|
| | 500m | - | |
| | 1100m | | |
| | 2000m | | |
| | 5000m+ | | |

****: 

### 4. 

| | VLOS | | | | |
|------|----------|------|--------------|------|----------|
| 400m | | - | - | APPROVE | TC1 |
| 600m | | | - | REJECT | TC2 |
| 600m | | | | APPROVE | TC3 |
| 1500m | | | | APPROVE | TC4 |
| 3000m | | | | APPROVE | TC5 |
| 6000m | | | | REJECT | TC6 |

---

## 

### VLOS

```jsonc
"vlos_restrictions": {
 "enabled": true,
 "operator_position": {"xyz": "0.0 0.0 0.0"},
 "max_vlos_range_m": 500.0,
 "enforcement": "reject_if_exceeds_unless_waiver"
}
```

### BVLOS

```jsonc
"bvlos_waivers": {
 "enabled": true,
 "available_waivers": [
 {
 "waiver_id": "W001_VisualObserver",
 "type": "visual_observer",
 "conditions": {
 "observer_position": {"xyz": "600.0 0.0 0.0"},
 "observer_vlos_range_m": 500.0,
 "max_effective_range_m": 1100.0
 },
 "enabled": false
 },
 {
 "waiver_id": "W002_TechnicalMeans",
 "type": "technical_means",
 "conditions": {
 "radar_coverage_m": 2000.0,
 "max_effective_range_m": 2000.0
 },
 "enabled": false
 },
 {
 "waiver_id": "W003_SpecialPermit",
 "type": "special_permit",
 "conditions": {
 "permit_number": "CAAC-BVLOS-2025-001",
 "max_effective_range_m": 5000.0
 },
 "enabled": false
 }
 ]
}
```

### 

```jsonc
{
 "id": "TC3",
 "command": "move_to_position(600, 0, 50)",
 "waivers_enabled": ["W001_VisualObserver"], // 
 "expected_result": {
 "decision": "APPROVE",
 "reason": ""
 }
}
```

---

## 

### 

| | | |
|------|------|----------|
| **APPROVE** | 4 | TC1, TC3, TC4, TC5 |
| **REJECT** | 2 | TC2, TC6 |

### 

1. **TC1**: VLOS
2. **TC2**: 
3. **TC3**: ()
4. **TC4**: 
5. **TC5**: 
6. **TC6**: 

### 

****: 6/6 (100%)

****: TC2, TC3, TC6 

---

## 

### 1. 

```python
def check_bvlos_with_waiver(
 target_position,
 operator_position,
 base_vlos_range,
 enabled_waivers
):
 # Step 1: 
 distance = calculate_distance(target_position, operator_position)
 
 # Step 2: VLOS
 if distance <= base_vlos_range:
 return APPROVE, "Within base VLOS"
 
 # Step 3: VLOS
 if not enabled_waivers:
 return REJECT, "Exceeds VLOS, no waiver"
 
 # Step 4: 
 for waiver in enabled_waivers:
 if waiver.type == "visual_observer":
 observer_distance = calculate_distance(
 target_position, 
 waiver.observer_position
 )
 if observer_distance <= waiver.observer_vlos_range:
 return APPROVE, f"Visual Observer waiver applied"
 
 elif waiver.type == "technical_means":
 if distance <= waiver.radar_coverage:
 return APPROVE, f"Technical Means waiver applied"
 
 elif waiver.type == "special_permit":
 if distance <= waiver.max_range:
 return APPROVE, f"Special Permit waiver applied"
 
 # Step 5: 
 return REJECT, "Exceeds all available waiver limits"
```

### 2. 

```python
def check_visual_observer_waiver(target, operator, observer, vlos_range):
 """"""
 dist_to_operator = distance(target, operator)
 dist_to_observer = distance(target, observer)
 
 # 
 if dist_to_operator <= vlos_range:
 return True, "Covered by operator"
 if dist_to_observer <= vlos_range:
 return True, "Covered by observer"
 
 return False, "Not covered by anyone"
```

### 3. 

```python
def check_technical_means_waiver(target, operator, radar_range):
 """"""
 distance = calculate_distance(target, operator)
 
 if distance <= radar_range:
 return True, f"Within radar coverage ({distance}m < {radar_range}m)"
 
 return False, f"Outside radar coverage ({distance}m > {radar_range}m)"
```

---

## 

### 
```
scenarios/basic/S014_bvlos_waiver.jsonc
```

### Ground Truth
```
ground_truth/S014_violations.json
```

### 
```
scripts/run_scenario_vlos.py # S013
```

---

## 

- **S013**: VLOS
- **S015**: 
- **S016**: 

---

## 

### S013

| | S013VLOS | S014BVLOS |
|------|--------------|-------------------|
| **** | | |
| **VLOS** | 500m | 500-5000m |
| **** | | 3 |
| **** | | |
| **** | 5 | 6 |

### 

- ****: 
- ****: 
- ****: 

---

## 

1. TC1 VLOS
2. TC2 
3. TC3 
4. TC4 
5. TC5 
6. TC6 
7. 
8. 
9. 

---

****: 1.0 
****: 2025-10-31 
****: Claude & 
****: AirSim-RuleBench v1.3 
****: 6

****: 

