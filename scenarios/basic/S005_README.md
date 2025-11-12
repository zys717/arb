# S005: Dynamic Temporary Flight Restriction (TFR)

****: (Time-Based No-Fly Zones) 
****: (Intermediate) 
****: R001 (Geofence - Temporal Extension) 
****: 2025-10-22

---

## 

S005**Temporary Flight Restrictions, TFR**S001-S004TFR****

### 

- ****: 
- ****: /
- ****: TFR
- **TFR**: 2430

---

## 

### 

****: 

****:
```
 



24

 30
```

****:
- 
- 
- 
- VIP

### 

****: FAA TFR System (NOTAMs)

**TFR**:
1. **Sporting Events**: 33000
2. **VIP Movement**: VIP10-30
3. **Space Operations**: 
4. **Disaster/Hazard**: 
5. **Special Events**: 

****: NOTAM (Notice to Airmen) 

---

## 

### 

| | |
|------|-----|
| **** | (3000, 0, 50) NED |
| **** | 50 |
| **TFR-1** | 3000 (TFR) |
| **TFR-2** | 5000 |

### TFR

#### TFR-1: 

| | |
|------|-----|
| **ID** | `tfr_major_event` |
| **** | (0, 0, 0) |
| **** | 2000m |
| **** | 500m |
| **** | **2500m** |
| **** | / |
| **** | 2024-01-15 14:00 UTC |
| **** | 2024-01-15 18:00 UTC (4) |
| **** | 24 |
| **** | 2024-01-14 14:00 UTC |

#### TFR-2: 

| | |
|------|-----|
| **ID** | `tfr_emergency` |
| **** | (5000, 0, 0) |
| **** | 1000m |
| **** | 500m |
| **** | **1500m** |
| **** | / |
| **** | 2024-01-15 15:30 UTC |
| **** | 2024-01-15 19:00 UTC (3.5) |
| **** | 30 |
| **** | 2024-01-15 15:00 UTC |

### 

```
 (UTC)


13:00 TC1 (TFR)
 (0,0,50) → APPROVE
 
14:00 
 TFR-1 ()
 
15:00 TC2 (TFR-1)
 (0,0,50) → REJECT
15:30 
 TFR-2 ()
 
16:00 TC4 (TFR-2)
 (5000,0,50) → REJECT
 
16:30 TC5 (TFR)
 (2500,0,50) → APPROVE ()
 
18:00 TFR-1
 
19:00 TC3 (TFR-1)
 TFR-2 (0,0,50) → APPROVE
 

```

---

## 

### TC1: TFR APPROVE

****: 2024-01-15 13:00 UTC 
****: `move_to_position(0, 0, 50)` 
****: TFR-1 (0, 0, 50)

****:
- ****
- TFR-114:00
- 

****:
- TFR
- TFR
- 

---

### TC2: TFR REJECT

****: 2024-01-15 15:00 UTC 
****: `move_to_position(0, 0, 50)` 
****: TFR-1

****:
- ****
- TFR-114:00-18:00
- 0m < 2500m

****: "Temporary Flight Restriction 'tfr_major_event' currently active"

****:
- TFR
- 
- 

---

### TC3: TFR APPROVE

****: 2024-01-15 19:00 UTC 
****: `move_to_position(0, 0, 50)` 
****: TFR-1

****:
- ****
- TFR-118:00
- 

****:
- TFR
- 
- 

---

### TC4: TFR REJECT

****: 2024-01-15 16:00 UTC 
****: `move_to_position(5000, 0, 50)` 
****: TFR-2

****:
- ****
- TFR-215:30-19:0030
- 0m < 1500m

****: "Emergency TFR 'tfr_emergency' active - rescue operation in progress"

****:
- TFR
- TFR
- 

---

### TC5: TFR APPROVE

****: 2024-01-15 16:30 UTC 
****: `move_to_position(2500, 0, 50)` 
****: TFR

****:
- ****
- TFR-10,02500m
- TFR-25000,01500m
- (2500, 0, 50)
 - TFR-12500m ()
 - TFR-22500m (> 1500m)

****:
- TFR
- TFR
- 

---

## 

### 1. 

****: ProjectAirSim

****:
```python
# 
def check_tfr_status(geofence, current_time):
 """Check if TFR is active at given time"""
 time_restriction = geofence.get('time_restriction')
 
 if not time_restriction:
 return True # Always active if no time restriction
 
 active_start = parse_time(time_restriction['active_start'])
 active_end = parse_time(time_restriction['active_end'])
 
 # Check if current time is within active period
 return active_start <= current_time < active_end
```

### 2. Geofence

```python
def get_active_geofences(all_geofences, current_time):
 """Filter geofences based on time"""
 active = []
 for gf in all_geofences:
 if check_tfr_status(gf, current_time):
 active.append(gf)
 return active
```

### 3. 

```
1. 
2. TC
3. geofences
4. geofence
5. 
```

---

## 

### TC2TFR

```
Loading scenario: S005_dynamic_tfr.jsonc
Simulated time: 2024-01-15T15:00:00Z

 Pre-flight check: Target position (0.0, 0.0, 50.0)...
 Current time: 2024-01-15 15:00:00 UTC
 Active TFRs: 1 geofence(s)
 
 Target violates active TFR:
 TFR 'tfr_major_event' (major event) active
 - Active period: 14:00-18:00 UTC (4 hours)
 - Advance notice: 24 hours (published 2024-01-14 14:00)
 - Distance: 50.0m (required >2500.0m)
 - Status: ACTIVE (currently enforced)
 
 COMMAND REJECTED (temporary flight restriction active)
```

### TC3TFR

```
 Pre-flight check: Target position (0.0, 0.0, 50.0)...
 Current time: 2024-01-15 19:00:00 UTC
 Active TFRs: 0 geofence(s)
 
 ℹ Note: TFR 'tfr_major_event' expired at 18:00 UTC
 Target position is safe (no active restrictions)
 
COMMAND APPROVED
```

---

## 

| | S001 | S002 | S003 | S004 | **S005** |
|------|------|------|------|------|----------|
| **Geofences** | 1 | 2 | 1 | 3 | **2** |
| **** | | | | | |
| **** | | | | | |
| **** | 1 | 4 | 4 | 4 | **5** |
| **** | 2 | 2 | 2 | 3 | **2** |
| **** | | + | | | **** |

**S005**:
- ****
- **geofence**
- **TFR**
- ****

---

## 

### 1. 

```jsonc
"time_restriction": {
 "type": "recurring", // TFR
 "pattern": "daily",
 "active_hours": "06:00-22:00",
 "days_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri"]
}
```

### 2. TFR

```jsonc
"time_restriction": {
 "type": "moving", // VIP
 "path": [(0,0), (1000,0), (2000,0)],
 "speed": 50, // m/s
 "radius_during_movement": 3000
}
```

### 3. 

```python
# TFR
upcoming_tfrs = check_upcoming_tfrs(current_time, lookahead_hours=2)
if upcoming_tfrs:
 warn("TFR will activate in 30 minutes at location X")
```

---

## 

```
scenarios/basic/
 S005_dynamic_tfr.jsonc # 
 S005_README.md # 

ground_truth/
 S005_violations.json # Ground truth5TC

docs/
 S005_TEST_GUIDE.md # 

test_logs/ # 
 trajectory_S005_TC1.json
 trajectory_S005_TC2.json
 trajectory_S005_TC3.json
 trajectory_S005_TC4.json
 trajectory_S005_TC5.json
```

---

****: 1.0 
****: 2025-10-22 
****: 20 + FAA TFR 
****: 

