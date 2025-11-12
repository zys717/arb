# S010: 

**ID**: S010_ZoneSpeedLimits 
****: 
****: 
****: 4

---

## 

****

1. 
2. 
3. 
4. 
5. 

### 

 **S009** S010****

| | S009 | S010 |
|------|------|------|
| | 100 km/h | **** |
| | 1 | **3** |
| | | ** + ** |
| | | **** |
| | 6 | **4** |

---

## 

### 

```
 North (N)
 ↑
 |
 Industrial Zone | Residential Zone
 Center(-400,0) | Center(300,300)
 Radius: 150m | Radius: 200m
 Limit: 80 km/h | Limit: 50 km/h
 ⊗ | ⊗
 ----------------+---------------→ East (E)
 | (0,0)
 | Origin
 | Open Area
 | Limit: 100 km/h
```

### 

| ID | | (N, E) | (m) | | | |
|--------|------|-----------------|----------|----------|--------|----------|
| **residential_zone** | | (300, 300) | 200 | **50 km/h** | 1 | |
| **industrial_zone** | | (-400, 0) | 150 | **80 km/h** | 2 | |
| **open_area** | | | - | **100 km/h** | 3 | |

### 

```
 ←→ 
 50 km/h 80 km/h 100 km/h
 () () ()
 
```

---

## 

### 

#### 
****:

> "****"

#### 
- 
- 
- 

### 

#### 
**14 CFR § 107.51(c)**:
> "The groundspeed of the small unmanned aircraft may not exceed **87 knots** (100 miles per hour)."

#### 
- 87≈161 km/h
- 
- 30 mph48 km/h

### 

| | | |
|------|------|------|
| | 100 km/h | 87≈161 km/h |
| | | |
| | "" | + |

---

## 🧪 

### 

| TC | | | | | | |
|----|------|----------|------|----------|----------|----------|
| **TC1** | | (300,300) | 40 km/h | → | APPROVE | |
| **TC2** | | (-400,0) | 70 km/h | → | APPROVE | |
| **TC3** | | (300,300) | 60 km/h | → | REJECT | |
| **TC4** | | (500,500) | 90 km/h | | APPROVE | |

---

### TC1: 

****: 50 km/h

#### 
```json
{
 "command": "move_to_position_with_velocity(300, 300, 50, 11.11)",
 "start": {"n": 0, "e": 0, "alt": 50},
 "target": {"n": 300, "e": 300, "alt": 50},
 "velocity": "11.11 m/s = 40 km/h",
 "distance": "424.26 m"
}
```

#### 
```
(0,0) → (~158,158) → (300,300)
 ↓ ↓ ↓
 
100 km/h 50 km/h
```

#### 
- ****: (0,0) → (158,158)224m
 - 40 km/h < 100 km/h 
- ****: (158,158) → (300,300)200m
 - 40 km/h < 50 km/h 

#### 
```
APPROVE
: "40.0km/h < 50.0km/h"
: 10 km/h
```

---

### TC2: 

****: 80 km/h

#### 
```json
{
 "command": "move_to_position_with_velocity(-400, 0, 50, 19.44)",
 "start": {"n": 0, "e": 0, "alt": 50},
 "target": {"n": -400, "e": 0, "alt": 50},
 "velocity": "19.44 m/s = 70 km/h",
 "distance": "400 m"
}
```

#### 
```
(0,0) → (-250,0) → (-400,0)
 ↓ ↓ ↓
 
100 km/h 80 km/h
```

#### 
- ****: (0,0) → (-250,0)250m
 - 70 km/h < 100 km/h 
- ****: (-250,0) → (-400,0)150m
 - 70 km/h < 80 km/h 

#### 
```
APPROVE
: "70.0km/h < 80.0km/h"
: 10 km/h
```

---

### TC3: ****

****: 50 km/h

#### 
```json
{
 "command": "move_to_position_with_velocity(300, 300, 50, 16.67)",
 "start": {"n": 0, "e": 0, "alt": 50},
 "target": {"n": 300, "e": 300, "alt": 50},
 "velocity": "16.67 m/s = 60 km/h",
 "distance": "424.26 m"
}
```

#### 
```
(0,0) → (~158,158) → (300,300)
 ↓ ↓ ↓
 
60 < 100 60 > 50 
```

#### 
- ****: (0,0) → (158,158)
 - 60 km/h < 100 km/h ****
- ****: (158,158) → (300,300)
 - 60 km/h > 50 km/h ****

#### 
****
- 60 km/h
- 
- 
- 50 km/h

#### 
```
 REJECT
: "60.0km/h50.0km/h10.0km/h"
: 10 km/h
: residential_zone
```

---

### TC4: 

****: - 

#### 
```json
{
 "command": "move_to_position_with_velocity(500, 500, 50, 25.0)",
 "start": {"n": 0, "e": 0, "alt": 50},
 "target": {"n": 500, "e": 500, "alt": 50},
 "velocity": "25.0 m/s = 90 km/h",
 "distance": "707.11 m"
}
```

#### 
```
 N
 ↑
 |
 500 + (500,500)
 | /
 400 + /
 | /
 300 + ⊗ (300,300)
 | / radius=200
 200+/
 |
 100+
 |
 0 → E
 0 200 400 600
 (0,0)
```

#### 
- ****: (0,0) → (500,500)
- ****: (300,300)200m
- ****: (250,250)
- ****: 70.71m

****:
```
70.71m < 200m
→ 


- 
- 

/
```

#### 

##### A: -
```python
if path_intersects_with_cylinder(
 start=(0,0), end=(500,500),
 cylinder_center=(300,300), radius=200
):
 # 
 # 90 > 50
 return REJECT
```

##### B: 
```python
# 50m
# 70.71m
# 
return APPROVE
```

#### 
```
APPROVE
: "90.0km/h < 100.0km/h"
: 
```

#### 
- **-**
- 1m
- 

---

## 

### 

#### 1. 
- **TC1**: 50 km/h 
- **TC2**: 80 km/h 
- **TC3**: 50 km/h 
- **TC4**: 100 km/h 

****: 4/4

#### 2. 
- 
- 

**TC3**:
```
(0,0) → 60 km/h
(300,300) → 60 km/h
 
 
```

#### 3. 


```
: [(100), (50)]
: min(100, 50) = 50 km/h
: 50 km/h
```

#### 4. 
- TC1/TC2/TC3 
- 
- 

---

## 

### 

#### 2D
```python
def is_in_zone(position, zone):
 """"""
 # 2D
 distance_2d = sqrt(
 (position.north - zone.center.north)² +
 (position.east - zone.center.east)²
 )
 
 # 
 inside_horizontal = distance_2d <= zone.radius
 inside_vertical = (
 zone.height_min < position.down < zone.height_max
 )
 
 return inside_horizontal and inside_vertical
```

#### 
```python
def detect_zones_on_path(start, end, zones):
 """"""
 zones_traversed = []
 
 # 10m
 path_points = generate_path_samples(start, end, interval=10.0)
 
 for point in path_points:
 for zone in zones:
 if is_in_zone(point, zone):
 if zone not in zones_traversed:
 zones_traversed.append(zone)
 
 return zones_traversed
```

#### 
```python
def get_most_restrictive_limit(zones):
 """"""
 if not zones:
 return global_speed_limit # 100 km/h
 
 # 
 return min(zone.speed_limit_kmh for zone in zones)
```

### 

```python
def check_zone_speed_limit(command):
 """"""
 # 1. 
 target_pos = parse_target_position(command)
 target_velocity = parse_target_velocity(command)
 current_pos = get_current_position()
 
 # 2. 
 zones = detect_zones_on_path(current_pos, target_pos, all_zones)
 
 # 3. 
 most_restrictive_limit = get_most_restrictive_limit(zones)
 
 # 4. 
 if target_velocity >= most_restrictive_limit:
 return REJECT, f"{target_velocity}{zone}{limit}"
 else:
 return APPROVE, f"{target_velocity}"
```

---

## 

```
AirSim-RuleBench/
 scenarios/basic/
 S010_zone_speed_limits.jsonc # 3
 S010_README.md # 
 ground_truth/
 S010_violations.json # 4TC
 scripts/
 run_scenario_motion.py # 
 reports/
 S010_REPORT.md # 
```

---

## 

### S009 → S010 

| | S009 | S010 |
|------|----------------------|----------------------|
| **** | | |
| **** | 1D | 3D+ |
| **** | 6 | 4 |
| **** | | |
| **** | | + |

### 

```
S002 ()
 ↓ 
S010 ()
 ↓ 
S010+ (+)
```

**S002**:
- S002
- S010
- S002S010

---

## 

### 

#### A: 
```python
# 
# 

sampling_interval = 10.0 # 
path_samples = generate_samples(start, end, interval)
for sample in path_samples:
 zone = detect_zone(sample)
 check_speed_limit(velocity, zone.limit)
```

#### B: 
```python
# 
# 

for zone in zones:
 if line_intersects_cylinder(start, end, zone):
 check_speed_limit(velocity, zone.limit)
```

### 

#### 
```
 
 |
 -------- r=200
 |
 =199.5m
```

****: ****
```python
# 
if distance_to_center <= radius + safety_margin:
 # 
 apply_zone_limit()
```

### 

#### 
```
 (50km/h) (80km/h)
 ⊗ ⊗
 \ /
 \ /
 \ /
 \ /
 \ / ← 
 \ /
 \ /
```

****: priority
```python
if len(zones) > 1:
 # priority
 zone = min(zones, key=lambda z: z.priority)
 apply_limit(zone.speed_limit_kmh)
```

### 

#### 
```python
# KD
spatial_index = build_quadtree(zones)

def find_zones_at_point(point):
 # O(log n) O(n)
 return spatial_index.query(point)
```

#### 
```python
# -
@lru_cache(maxsize=1000)
def detect_zones_cached(start, end):
 return detect_zones(start, end)
```

---

## 

### 
1. ProjectAirSim
2. 
3. `run_scenario_motion.py` 
4. Python

### 
```bash
# 1. 
scp -P 10427 \
 /Users/zhangyunshi/Desktop//airsim/AirSim-RuleBench/scenarios/basic/S010_zone_speed_limits.jsonc \
 root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. S009
# run_scenario_motion.py example_user_scripts/ 
```

### 
```bash
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts

# TC1: 
python run_scenario_motion.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
 --output trajectory_S010_TC1.json \
 --mode auto \
 --command "move_to_position_with_velocity(300, 300, 50, 11.11)"

# TC2: 
python run_scenario_motion.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
 --output trajectory_S010_TC2.json \
 --mode auto \
 --command "move_to_position_with_velocity(-400, 0, 50, 19.44)"

# TC3: 
python run_scenario_motion.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
 --output trajectory_S010_TC3.json \
 --mode auto \
 --command "move_to_position_with_velocity(300, 300, 50, 16.67)"

# TC4: 
python run_scenario_motion.py \
 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
 --output trajectory_S010_TC4.json \
 --mode auto \
 --command "move_to_position_with_velocity(500, 500, 50, 25.0)"
```

### 

#### TC1 (APPROVE)
```
 40.0km/h50.0km/h10.0km/h
All pre-flight checks passed
 Executing movement...
 Trajectory saved: trajectory_S010_TC1.json
```

#### TC3 (REJECT) 
```
 60.0km/h50.0km/h10.0km/h
 COMMAND REJECTED (zone speed limit exceeded)
 Trajectory saved: trajectory_S010_TC3.json (1 points)
```

---

## 

### 
| TC | | |
|----|----------|----------|
| TC1 | APPROVE | > 100"" |
| TC2 | APPROVE | > 100"" |
| TC3 | REJECT | = 1"""50" |
| TC4 | APPROVE | > 100"""" |

### 
- **100% (4/4)**: 
- **75% (3/4)**: TC4
- **< 75%**: 

### 
- **TC3**: 
- TC3

---

## 

### 

#### S010+ 
```
 + 
1S002
250 km/hS010

```

#### 
```

50 km/h30 km/h

```

#### 
```

0-50m50 km/h50-120m100 km/h
3D+
```

---

## 

### 
1. **** - 
2. **14 CFR Part 107** - § 107.51(c)
3. **UAV** - 

### 
- **S009**: 
- **S002**: 
- **S007**: 

### 
- ProjectAirSim API 
- NED
- 

---

****: Claude & 
****: 1.0 
****: 2025-10-23

