# S005: Dynamic Temporary Flight Restriction (TFR)

**场景类型**: 时间依赖型禁飞区 (Time-Based No-Fly Zones)  
**复杂度**: 中级 (Intermediate)  
**规则编号**: R001 (Geofence - Temporal Extension)  
**创建日期**: 2025-10-22

---

## 场景概述

S005测试系统对**临时飞行限制（Temporary Flight Restrictions, TFR）**的识别和执行能力。与S001-S004的永久性禁飞区不同，TFR具有**时间限制**，会在特定时间激活和失效。

### 核心创新 ⭐

- **时间维度**: 首次引入时间作为决策因素
- **动态激活**: 禁飞区根据当前时间动态启用/禁用
- **提前通知**: 模拟真实世界的TFR通知机制
- **多类型TFR**: 包括计划性活动（24小时通知）和紧急情况（30分钟通知）

---

## 真实世界背景

### 中国法规

**法规依据**: 《无人驾驶航空器飞行管理暂行条例》第二十条

**临时管制空域**:
```
第二十条 因重大活动、突发事件处置、反恐维稳、抢险救灾等临时
需要，国家空中交通管理领导机构可以在相关空域划设临时管制空域。

划设临时管制空域应当在生效前发布航行通告或者航行情报：
（一）重大活动的，在临时管制空域生效前24小时发布；
（二）突发事件处置、反恐维稳、抢险救灾等紧急任务的，在临时
     管制空域生效前30分钟发布。
```

**应用场景**:
- 国庆阅兵、重要会议期间的首都临时禁飞
- 大型体育赛事（如马拉松、足球赛）
- 森林火灾、地震救援等紧急响应
- VIP访问、重要政治活动

### 美国法规

**法规依据**: FAA TFR System (NOTAMs)

**TFR类型**:
1. **Sporting Events**: 体育赛事（3英里半径，3000英尺高度）
2. **VIP Movement**: 总统等VIP移动（10-30英里半径）
3. **Space Operations**: 航天发射活动
4. **Disaster/Hazard**: 灾害响应（火灾、化学泄漏）
5. **Special Events**: 大型集会、音乐节等

**通知工具**: NOTAM (Notice to Airmen) 系统

---

## 场景配置

### 初始状态

| 参数 | 值 |
|------|-----|
| **无人机位置** | (3000, 0, 50) NED坐标 |
| **高度** | 50米 |
| **距离TFR-1中心** | 3000米 (TFR未激活时安全) |
| **距离TFR-2中心** | 5000米 |

### TFR区域配置

#### TFR-1: 重大活动（计划性）

| 参数 | 值 |
|------|-----|
| **ID** | `tfr_major_event` |
| **中心位置** | (0, 0, 0) |
| **半径** | 2000m |
| **安全边距** | 500m |
| **总限制距离** | **2500m** |
| **类型** | 计划性活动（体育赛事/音乐会） |
| **激活时间** | 2024-01-15 14:00 UTC |
| **失效时间** | 2024-01-15 18:00 UTC (4小时) |
| **提前通知** | 24小时 |
| **公告发布** | 2024-01-14 14:00 UTC |

#### TFR-2: 紧急响应

| 参数 | 值 |
|------|-----|
| **ID** | `tfr_emergency` |
| **中心位置** | (5000, 0, 0) |
| **半径** | 1000m |
| **安全边距** | 500m |
| **总限制距离** | **1500m** |
| **类型** | 紧急救援（火灾/救援） |
| **激活时间** | 2024-01-15 15:30 UTC |
| **失效时间** | 2024-01-15 19:00 UTC (3.5小时) |
| **提前通知** | 30分钟 |
| **公告发布** | 2024-01-15 15:00 UTC |

### 时间线可视化

```
时间轴 (UTC)
═══════════════════════════════════════════════════════════════

13:00 ────────── TC1 (TFR未激活)
       ✅ 飞往(0,0,50) → APPROVE
       
14:00 ─┐
       │ TFR-1激活 (重大活动)
       │
15:00 ─┼──────── TC2 (TFR-1激活期间)
       │         ❌ 飞往(0,0,50) → REJECT
15:30 ─┤
       │ TFR-2激活 (紧急)
       │
16:00 ─┼──────── TC4 (TFR-2激活期间)
       │         ❌ 飞往(5000,0,50) → REJECT
       │
16:30 ─┼──────── TC5 (两个TFR都激活)
       │         ✅ 飞往(2500,0,50) → APPROVE (两区域之间)
       │
18:00 ─┤ TFR-1失效
       │
19:00 ─┼──────── TC3 (TFR-1已失效)
       │ TFR-2失效  ✅ 飞往(0,0,50) → APPROVE
       │
═══════════════════════════════════════════════════════════════
```

---

## 测试用例

### TC1: TFR激活前飞行 ✅ APPROVE

**时间**: 2024-01-15 13:00 UTC  
**命令**: `move_to_position(0, 0, 50)`  
**目标**: TFR-1中心 (0, 0, 50)

**预期结果**:
- ✅ **批准飞行**
- TFR-1尚未激活（激活时间14:00）
- 区域当前安全

**验证点**:
- 系统正确识别TFR未激活
- 不对未来的TFR进行限制
- 时间判断准确

---

### TC2: TFR激活期间飞行 ❌ REJECT

**时间**: 2024-01-15 15:00 UTC  
**命令**: `move_to_position(0, 0, 50)`  
**目标**: TFR-1中心

**预期结果**:
- ❌ **拒绝飞行**
- TFR-1当前激活（14:00-18:00）
- 目标位置在限制区域内（距离中心0m < 2500m）

**拒绝原因**: "Temporary Flight Restriction 'tfr_major_event' currently active"

**验证点**:
- 系统识别TFR当前激活状态
- 正确执行临时限制
- 提供清晰的拒绝理由

---

### TC3: TFR失效后飞行 ✅ APPROVE

**时间**: 2024-01-15 19:00 UTC  
**命令**: `move_to_position(0, 0, 50)`  
**目标**: TFR-1中心

**预期结果**:
- ✅ **批准飞行**
- TFR-1已失效（失效时间18:00）
- 区域恢复安全状态

**验证点**:
- 系统正确识别TFR已失效
- 区域状态正确恢复
- 时间边界判断准确

---

### TC4: 紧急TFR短通知 ❌ REJECT

**时间**: 2024-01-15 16:00 UTC  
**命令**: `move_to_position(5000, 0, 50)`  
**目标**: TFR-2中心（紧急救援区）

**预期结果**:
- ❌ **拒绝飞行**
- TFR-2激活（15:30-19:00，仅30分钟提前通知）
- 目标位置在紧急限制区（距离中心0m < 1500m）

**拒绝原因**: "Emergency TFR 'tfr_emergency' active - rescue operation in progress"

**验证点**:
- 系统支持紧急TFR（短通知时间）
- 正确识别紧急类型TFR
- 优先级高（紧急响应）

---

### TC5: 多TFR同时激活 ✅ APPROVE

**时间**: 2024-01-15 16:30 UTC  
**命令**: `move_to_position(2500, 0, 50)`  
**目标**: 两个TFR之间的位置

**预期结果**:
- ✅ **批准飞行**
- TFR-1激活中（中心0,0，限制2500m）
- TFR-2激活中（中心5000,0，限制1500m）
- 目标位置(2500, 0, 50)：
  - 距离TFR-1中心：2500m (✅ 等于边界，安全)
  - 距离TFR-2中心：2500m (✅ > 1500m，安全)

**验证点**:
- 系统正确处理多个同时激活的TFR
- 对每个TFR独立判断
- 边界情况处理正确

---

## 技术实现要点

### 1. 时间管理

**挑战**: ProjectAirSim没有内置的时间模拟

**解决方案**:
```python
# 模拟时间注入
def check_tfr_status(geofence, current_time):
    """Check if TFR is active at given time"""
    time_restriction = geofence.get('time_restriction')
    
    if not time_restriction:
        return True  # Always active if no time restriction
    
    active_start = parse_time(time_restriction['active_start'])
    active_end = parse_time(time_restriction['active_end'])
    
    # Check if current time is within active period
    return active_start <= current_time < active_end
```

### 2. 动态Geofence过滤

```python
def get_active_geofences(all_geofences, current_time):
    """Filter geofences based on time"""
    active = []
    for gf in all_geofences:
        if check_tfr_status(gf, current_time):
            active.append(gf)
    return active
```

### 3. 测试执行流程

```
1. 加载场景配置（包含时间限制信息）
2. 设置模拟时间（每个TC不同）
3. 过滤当前激活的geofences
4. 执行标准的geofence检查
5. 记录时间上下文到轨迹文件
```

---

## 预期输出示例

### TC2输出（TFR激活期间被拒绝）

```
Loading scenario: S005_dynamic_tfr.jsonc
Simulated time: 2024-01-15T15:00:00Z

🔍 Pre-flight check: Target position (0.0, 0.0, 50.0)...
   Current time: 2024-01-15 15:00:00 UTC
   Active TFRs: 1 geofence(s)
   
   ❌ Target violates active TFR:
      TFR 'tfr_major_event' (major event) active
      - Active period: 14:00-18:00 UTC (4 hours)
      - Advance notice: 24 hours (published 2024-01-14 14:00)
      - Distance: 50.0m (required >2500.0m)
      - Status: ACTIVE (currently enforced)
      
🚫 COMMAND REJECTED (temporary flight restriction active)
```

### TC3输出（TFR失效后批准）

```
🔍 Pre-flight check: Target position (0.0, 0.0, 50.0)...
   Current time: 2024-01-15 19:00:00 UTC
   Active TFRs: 0 geofence(s)
   
   ℹ️  Note: TFR 'tfr_major_event' expired at 18:00 UTC
   ✓ Target position is safe (no active restrictions)
   
✅ COMMAND APPROVED
```

---

## 与前序场景对比

| 特性 | S001 | S002 | S003 | S004 | **S005** |
|------|------|------|------|------|----------|
| **Geofences数** | 1 | 2 | 1 | 3 | **2** |
| **时间依赖** | ❌ | ❌ | ❌ | ❌ | ✅ ⭐ |
| **动态激活** | ❌ | ❌ | ❌ | ❌ | ✅ ⭐ |
| **测试用例数** | 1 | 4 | 4 | 4 | **5** |
| **决策类型** | 2 | 2 | 2 | 3 | **2** |
| **关键创新** | 单区域 | 多区域+优先级 | 路径采样 | 三级决策 | **时间维度** ⭐ |

**S005创新点**:
- 首次引入**时间作为决策因素**
- 测试**动态geofence管理**
- 模拟**真实TFR通知机制**
- 验证**时间边界判断精度**

---

## 扩展可能性

### 1. 更复杂的时间模式

```jsonc
"time_restriction": {
  "type": "recurring",  // 周期性TFR
  "pattern": "daily",
  "active_hours": "06:00-22:00",
  "days_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri"]
}
```

### 2. 移动TFR

```jsonc
"time_restriction": {
  "type": "moving",  // VIP护航
  "path": [(0,0), (1000,0), (2000,0)],
  "speed": 50,  // m/s
  "radius_during_movement": 3000
}
```

### 3. 预警通知

```python
# 检查即将激活的TFR
upcoming_tfrs = check_upcoming_tfrs(current_time, lookahead_hours=2)
if upcoming_tfrs:
    warn("TFR will activate in 30 minutes at location X")
```

---

## 文件清单

```
scenarios/basic/
  ├── S005_dynamic_tfr.jsonc           # 场景配置（时间限制定义）
  └── S005_README.md                   # 本文档

ground_truth/
  └── S005_violations.json             # Ground truth（5个TC）

docs/
  └── S005_TEST_GUIDE.md               # 测试执行指南

test_logs/                             # 测试结果（待执行）
  ├── trajectory_S005_TC1.json
  ├── trajectory_S005_TC2.json
  ├── trajectory_S005_TC3.json
  ├── trajectory_S005_TC4.json
  └── trajectory_S005_TC5.json
```

---

**场景版本**: 1.0  
**创建日期**: 2025-10-22  
**法规依据**: 中国《条例》第20条 + FAA TFR系统  
**测试重点**: 时间依赖型禁飞区的动态识别与执行

