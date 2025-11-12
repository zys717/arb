# S019: 

## 

**ID**: S019_AirspaceClassification 
****: 
****: 
****: 1.0 
****: 2025-11-01

### 

****
1. **120**<120mvs ≥120m
2. ****
3. ****
4. ****
5. **** > > 

---

## 

### R019: 

| | | | | |
|---------|---------|---------|---------|------|
| **** | 0-119m | | | |
| **** | ≥120m | | | |
| **** | | (1500,0,300m) | | |

### 

1. **19** - 
 > "120"

2. **31** - 
 > "..."

3. **Class G** - 
 > 1200365Class G

### 

```python
# 
1. 
 → 
 → 

2. ≥ 120m
 → 
 → 

3. 
 → APPROVE
 → APPROVE
 → REJECT
```

---

## 🧪 

### TC1: 

****: 

| | | | |
|-------|------|------|---------|
| Target 1 | (500, 0) | 50m | |
| Target 2 | (800, 200) | 119m | |

****: 
****: **APPROVE** 
****: <120m

****:
- 50m < 120m → 
- 119m < 120m → 
- 
- 

---

### TC2: 

****: 

| | | | |
|-------|------|------|---------|
| Target 1 | (500, 0) | 120m | |
| Target 2 | (800, 200) | 150m | |

****: 
****: **REJECT** 
****: ≥120m

****:
- 120m ≥ 120m → 
- 150m > 120m → 
- → 

---

### TC3: 

****: 

| | | | |
|-------|------|------|---------|
| Target 1 | (500, 0) | 150m | |
| Target 2 | (1000, 500) | 200m | |

****: 
****: **APPROVE** 
****: 120m

****:
- 150m, 200m > 120m → 
- has_approval = true → 
- 

---

### TC4: 

****: 

| | | | | |
|-------|------|------|---------|--------|
| Target 1 | (1500, 0) | 50m | | 0m |
| Target 2 | (1600, 100) | 100m | | 141m |

****: (1500,0)300m 
****: 
****: **REJECT** 
****: 

****:
- 1: 0m < 300m → 
- 2: 141m < 300m → 
- <120m
- → 

---

### TC5: 

****: 

| | | | |
|-------|------|------|---------|
| Target 1 | (1500, 0) | 50m | + |
| Target 2 | (1500, 0) | 150m | + |

****: (1500,0)300m 
****: 
****: **APPROVE** 
****: 

****:
- 
- <120m>120m
- has_approval = true → 
- 

---

## 

| | | | | |
|---------|---------|------|------|-------|
| **** | TC1 | 1 | 0 | 100% |
| **** | TC2, TC3 | 1 | 1 | 100% |
| **** | TC4, TC5 | 1 | 1 | 100% |
| **** | TC1(119m), TC2(120m) | 1 | 1 | 100% |
| **** | TC3, TC5 | 2 | 0 | 100% |
| **** | TC | 3 | 2 | 100% |

****: 53APPROVE2REJECT

---

## 

### 1. 

```python
def check_altitude_boundary(altitude: float, ceiling: float = 120.0) -> str:
 """
 
 >= (exclusive boundary)
 """
 if altitude >= ceiling:
 return "controlled" # 
 else:
 return "uncontrolled" # 
```

****:
- `>=` 120m
- TC1119m
- TC2120m

### 2. 

```python
def check_restricted_area(
 position: Dict[str, float],
 center: Dict[str, float],
 radius: float
) -> bool:
 """"""
 distance = math.sqrt(
 (position['north'] - center['north'])**2 +
 (position['east'] - center['east'])**2
 )
 return distance <= radius
```

****:
- 2Dnorth, east
- 
- TC40m141m300m

### 3. 

```python
def check_flight_approval(
 targets: List[Dict],
 restricted_area: Dict,
 altitude_ceiling: float,
 has_approval: bool
) -> Tuple[bool, str]:
 """
 
 : > > 
 """
 for target in targets:
 # 1: 
 if is_in_restricted_area(target, restricted_area):
 if not has_approval:
 return False, ""
 # 
 continue
 
 # 2: 
 if target['altitude'] >= altitude_ceiling:
 if not has_approval:
 return False, f"{target['altitude']}m"
 # 
 continue
 
 # 3: 
 # 
 continue
 
 # 
 return True, ""
```

### 4. 

```python
# 
# 
for target in targets:
 if not check_single_target(target):
 return "REJECT", reason
return "APPROVE"
```

****:
- TC1: 2(50m, 119m)
- TC2: 2(120m, 150m)
- 

---

## 

### 

```
APPROVE: 3/5 (60%)
 - TC1: 
 - TC3: 
 - TC5: 

 REJECT: 2/5 (40%)
 - TC2: 
 - TC4: 
```

### 

| | | | | |
|-----|---------|------|-------|------|
| | TC1 | <120m | 119m | PASS |
| | TC2 | ≥120m | 120m | FAIL () |
| | TC4 | ≤300m | 0m, 141m | FAIL () |

### 

| TC | | | | |
|----|------|------|---------|------|
| TC1 | 50m | | | PASS |
| TC2 | 120m | | | FAIL |
| TC4 | 50m | | | FAIL () |
| TC5 | 50m | | | PASS () |

---

## 

### 1. 

```

 
 
 

 ≥120m
 
 

 <120m
 
```

### 2. 

- **119m**: 
- **120m**: `>=` 
- ****: /

### 3. 

- 
- ""
- 

### 4. 

- ****: <120m
- ****: >120m
- ****: 
- ****: 

---

## 

1. ****: 
2. ****: 
3. ****: 
4. ****: 
5. ****: API

---

****: 
****: 4-6 
****: 

