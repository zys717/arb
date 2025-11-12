# S012 - 时间窗口限制场景

## 📋 场景概述

**场景ID**: S012_TimeWindow  
**场景名称**: 时间窗口限制  
**难度等级**: ⭐⭐ 中等  
**场景类型**: 时间限制 + 空间限制（组合规则）

### 测试目标

验证无人机系统对**特定区域特定时段禁飞规则**的合规性检测能力，特别是：
1. 准确识别时间窗口（如夜间22:00-06:00）
2. 准确检测敏感区域（如医院区域）
3. 正确执行AND组合规则（时间+空间同时满足才拒绝）

### 核心规则

**组合条件**: 在医院区域内 **AND** 在禁飞时段内 → 拒绝

```
IF (is_in_hospital_zone AND is_in_time_window):
    REJECT
ELSE:
    APPROVE
```

---

## 📜 法规依据

### 中国法规 🇨🇳

**法规基础**: 《无人驾驶航空器飞行管理暂行条例》第三十二条

**地方性规定**: 各地可根据实际情况制定具体限制

**典型案例**:
```
医院夜间禁飞（22:00-06:00）
  理由：减少噪音干扰，保障患者休息
  
学校上课时间限制（08:00-17:00）
  理由：保障教学秩序，确保学生安全
  
居民区深夜禁飞（00:00-06:00）
  理由：保证居民休息
```

### 美国法规 🇺🇸

**联邦层面**: 14 CFR Part 107 无明确时间窗口限制

**州/地方法规**: State and Local Ordinances
```
Many states and local governments impose quiet hours or 
time-based restrictions near sensitive areas such as:
  - Hospitals
  - Schools
  - Residential areas
  - Parks
```

**本场景标准**: 采用中国地方性规定标准（医院夜间禁飞）

---

## 🎯 测试用例设计

### 场景设定

**医院区域**:
- 中心位置：(200, 0, 50) NED - 北向200m，东向0m，高度50m
- 半径：150m
- 高度范围：0-120m

**禁飞时段**:
- 开始：22:00（晚上10点）
- 结束：06:00（早上6点）
- 描述：夜间安静时段
- 理由：减少噪音干扰，保障患者休息

**组合规则**:
```
REJECT条件 = 在医院区域内 AND 在禁飞时段内

真值表：
  time=false, zone=false → APPROVE
  time=false, zone=true  → APPROVE ✅ 关键
  time=true,  zone=false → APPROVE ✅ 关键
  time=true,  zone=true  → REJECT  ✅ 核心
```

### 测试用例总览（5个）

| TC | 时间 | 位置 | 时间窗口 | 医院内 | 预期 | 测试重点 |
|----|------|------|----------|--------|------|----------|
| **TC1** | 14:00 | (0,200) | ❌ | ❌ | ✅ APPROVE | 基础合规 |
| **TC2** | 14:00 | (200,0) | ❌ | ✅ | ✅ APPROVE | 单条件（仅zone） ⭐ |
| **TC3** | 23:00 | (0,200) | ✅ | ❌ | ✅ APPROVE | 单条件（仅time） ⭐ |
| **TC4** | 23:00 | (200,0) | ✅ | ✅ | ❌ REJECT | AND逻辑（双条件） ⭐⭐ |
| **TC5** | 22:00 | (200,0) | ✅ | ✅ | ❌ REJECT | 边界值 ⭐ |

**关键测试**: TC2/TC3（单条件不拒绝）+ TC4（双条件拒绝）

---

## 📝 测试用例详细说明

### TC1: 白天医院外（基线）

**场景**: 白天14:00，在医院区域外飞行

| 指标 | 值 |
|------|-----|
| **时间** | 14:00 |
| **目标位置** | (0, 200, 50) |
| **医院中心** | (200, 0, 50) |
| **距离** | 282.84m > 150m半径 |
| **在医院内** | ❌ 否 |
| **在禁飞时段** | ❌ 否 |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Time: 14:00
Target: (0, 200, 50)
✅ 不在禁飞时段（14:00不在22:00-06:00内）
✅ 不在医院区域（距离282.84m > 150m）
✅ All checks passed
```

**分析**: 两个条件都不满足，正常批准

---

### TC2: 白天医院内（单条件测试）⭐ 关键测试

**场景**: 白天14:00，在医院区域内飞行

| 指标 | 值 |
|------|-----|
| **时间** | 14:00 |
| **目标位置** | (200, 0, 50) |
| **医院中心** | (200, 0, 50) |
| **距离** | 0m < 150m半径 |
| **在医院内** | ✅ **是** |
| **在禁飞时段** | ❌ 否 |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Time: 14:00
Target: (200, 0, 50) - 医院中心
⚠ 目标位置在医院区域内（距离0m）
✅ 但不在禁飞时段（14:00不在22:00-06:00内）
✅ All checks passed - 白天允许在医院区域飞行
```

**关键点**:
- ✅ **这是最关键的测试之一**
- ✅ 证明仅满足空间条件不触发拒绝
- ✅ 必须同时满足时间+空间才拒绝
- ✅ AND逻辑的正确实现

**与S002对比**:
- S002: 在禁飞区 → 直接拒绝（单条件）
- S012: 在禁飞区 + 在禁飞时段 → 才拒绝（双条件）

---

### TC3: 夜间医院外（单条件测试）⭐ 关键测试

**场景**: 夜间23:00，在医院区域外飞行

| 指标 | 值 |
|------|-----|
| **时间** | 23:00 |
| **目标位置** | (0, 200, 50) |
| **医院中心** | (200, 0, 50) |
| **距离** | 282.84m > 150m半径 |
| **在医院内** | ❌ 否 |
| **在禁飞时段** | ✅ **是** |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Time: 23:00
Target: (0, 200, 50)
⚠ 在禁飞时段（23:00在22:00-06:00内）
✅ 但不在医院区域（距离282.84m > 150m）
✅ All checks passed - 医院外允许飞行
```

**关键点**:
- ✅ **这是最关键的测试之一**
- ✅ 证明仅满足时间条件不触发拒绝
- ✅ 必须同时满足时间+空间才拒绝
- ✅ AND逻辑的正确实现

**与S011对比**:
- S011: 夜间 → 需要灯光+培训（全局规则）
- S012: 夜间 + 在医院内 → 才禁飞（局部规则）

---

### TC4: 夜间医院内（AND逻辑测试）⭐⭐ 核心测试

**场景**: 夜间23:00，在医院区域内飞行

| 指标 | 值 |
|------|-----|
| **时间** | 23:00 |
| **目标位置** | (200, 0, 50) |
| **医院中心** | (200, 0, 50) |
| **距离** | 0m < 150m半径 |
| **在医院内** | ✅ **是** |
| **在禁飞时段** | ✅ **是** |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Time: 23:00
Target: (200, 0, 50) - 医院中心
❌ 在禁飞时段（23:00在22:00-06:00内）
❌ 在医院区域内（距离0m < 150m）
🚫 COMMAND REJECTED (time window restriction)
   理由：夜间22:00-06:00禁飞时段，禁止在医院区域内飞行
```

**关键点**:
- ✅ **这是最核心的测试**
- ✅ 同时满足时间+空间两个条件
- ✅ AND逻辑正确触发拒绝
- ✅ 拒绝理由清晰

**组合逻辑验证**:
```
time=true AND zone=true → REJECT ✅
```

---

### TC5: 边界值测试（22:00）⭐

**场景**: 禁飞开始时刻22:00，在医院内

| 指标 | 值 |
|------|-----|
| **时间** | **22:00** |
| **目标位置** | (200, 0, 50) |
| **医院中心** | (200, 0, 50) |
| **距离** | 0m |
| **在医院内** | ✅ 是 |
| **在禁飞时段** | ✅ 是（22:00 >= 22:00） |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Time: 22:00
Target: (200, 0, 50)
❌ 22:00禁飞时段开始（22:00 >= 22:00）
❌ 在医院区域内
🚫 COMMAND REJECTED (time window restriction)
```

**时间判断**:
```
22:00 >= 22:00 → 禁飞时段开始 ✅
```

**关键点**:
- ✅ 验证边界值处理（22:00是开始时刻）
- ✅ 使用 `>=` 而非 `>` 进行判断
- ✅ 时间判断精度到分钟

---

## 🔍 关键测试点

### 1. AND逻辑真值表验证

| 时间窗口 | 医院内 | 结果 | 测试用例 |
|----------|--------|------|----------|
| ❌ | ❌ | ✅ APPROVE | TC1 |
| ❌ | ✅ | ✅ APPROVE | TC2 ⭐ |
| ✅ | ❌ | ✅ APPROVE | TC3 ⭐ |
| ✅ | ✅ | ❌ REJECT | TC4 ⭐⭐ |

**关键验证**: TC2和TC3证明单条件不触发拒绝

### 2. 时间窗口判断（复用S011）

**时间窗口**: 22:00-06:00（跨越午夜）

**判断逻辑**:
```python
is_in_time_window = (time >= "22:00") OR (time < "06:00")
```

**示例**:
- 14:00: false（白天）
- 22:00: true（禁飞开始）
- 23:00: true（夜间）
- 06:00: false（禁飞结束）

### 3. 区域检测（复用S002/S010）

**医院区域**: 圆柱体
- 中心：(200, 0, -50)
- 半径：150m
- 高度：0-120m

**判断逻辑**:
```python
distance_2d = sqrt((pos.n - 200)^2 + (pos.e - 0)^2)
is_in_hospital = distance_2d <= 150
```

**示例**:
- (200, 0): 0m → 在医院内 ✅
- (0, 200): 282.84m → 在医院外 ❌

### 4. 组合规则执行

**实现**:
```python
is_restricted = is_in_time_window AND is_in_hospital_zone

if is_restricted:
    return REJECT, "夜间22:00-06:00禁飞时段，禁止在医院区域内飞行"
else:
    return APPROVE
```

---

## 🏗️ 场景配置

### 医院区域定义

```jsonc
"restricted_zone": {
  "zone_id": "hospital_zone",
  "zone_type": "cylinder",
  "center": {"north": 200.0, "east": 0.0, "down": -50.0},
  "radius": 150.0,
  "height_min": -120.0,
  "height_max": 0.0
}
```

### 时间窗口定义

```jsonc
"time_window": {
  "type": "night_quiet_hours",
  "start": "22:00",
  "end": "06:00",
  "description": "医院夜间安静时段"
}
```

### 无人机初始状态

- **位置**: (0, 0, 50) NED - 在医院区域外
- **姿态**: (0, 0, 0)
- **环境**: 晴朗，无风

### 命令格式

```
move_to_position(north, east, altitude)
```

**示例**:
```
move_to_position(200, 0, 50)  # 飞往医院中心
move_to_position(0, 200, 50)  # 飞往医院外
```

---

## 📊 预期结果

### 决策分布

| 决策 | 数量 | 测试用例 |
|------|------|----------|
| **APPROVE** | 3 | TC1, TC2, TC3 |
| **REJECT** | 2 | TC4, TC5 |

### 关键测试通过条件

1. ✅ **TC2**: 白天医院内批准（单条件不拒绝）
2. ✅ **TC3**: 夜间医院外批准（单条件不拒绝）
3. ✅ **TC4**: 夜间医院内拒绝（双条件拒绝）
4. ✅ **TC5**: 边界值22:00拒绝（时间精度）

### 测试通过标准

**总分**: 5/5 (100%)

**关键测试**: TC2/TC3/TC4必须全部通过（AND逻辑验证）

---

## 🔧 技术实现要点

### 1. 时间窗口检查（复用S011）

```python
def is_in_time_window(current_time: str, 
                       start: str = "22:00", 
                       end: str = "06:00") -> bool:
    """检查是否在禁飞时段"""
    current_min = parse_time(current_time)
    start_min = parse_time(start)  # 1320分钟
    end_min = parse_time(end)      # 360分钟
    
    # 跨午夜：22:00-23:59 OR 00:00-06:00
    return current_min >= start_min or current_min < end_min
```

### 2. 区域检测（复用S002/S010）

```python
def is_in_hospital_zone(position: Position3D,
                        hospital_center: Position3D,
                        radius: float = 150.0) -> bool:
    """检查是否在医院区域内"""
    distance_2d = math.sqrt(
        (position.north - hospital_center.north)**2 +
        (position.east - hospital_center.east)**2
    )
    return distance_2d <= radius
```

### 3. 组合规则检查（新增）

```python
def check_time_window_restriction(
    time_of_day: str,
    target_position: Position3D,
    time_window_config: TimeWindowConfig
) -> Tuple[bool, str]:
    """检查时间窗口限制"""
    
    # 1. 检查时间窗口
    is_in_window = is_in_time_window(
        time_of_day,
        time_window_config.start,
        time_window_config.end
    )
    
    # 2. 检查区域
    is_in_zone = is_in_hospital_zone(
        target_position,
        time_window_config.zone_center,
        time_window_config.zone_radius
    )
    
    # 3. AND逻辑
    if is_in_window and is_in_zone:
        return False, f"夜间{time_window_config.start}-{time_window_config.end}禁飞时段，禁止在医院区域内飞行"
    else:
        return True, "通过时间窗口检查"
```

### 4. 综合检查流程

```python
def pre_flight_check_time_window(
    time_of_day: str,
    target_position: Position3D,
    config: ScenarioConfig
):
    """时间窗口预检"""
    if not config.time_window:
        return True, "无时间窗口限制"
    
    print(f"🔍 Pre-flight check: Time window restrictions...")
    
    is_safe, reason = check_time_window_restriction(
        time_of_day,
        target_position,
        config.time_window
    )
    
    if not is_safe:
        print(f"   ❌ {reason}")
        return False, reason
    else:
        print(f"   ✓ {reason}")
        return True, reason
```

---

## 📁 相关文件

### 场景配置
```
scenarios/basic/S012_time_window.jsonc
```

### Ground Truth
```
ground_truth/S012_violations.json
```

### 测试脚本
```
scripts/run_scenario_motion.py  # 需要更新以支持时间窗口检查
```

### 测试指南
```
docs/S012_TEST_GUIDE.md  # 将在下一步创建
```

---

## 🔗 相关场景

- **S011**: 夜间飞行规则（时间判断基础）
- **S002**: 多地理围栏（区域检测基础）
- **S005**: 临时禁飞区（动态限制）
- **S010**: 分区速度限制（空间+规则组合）

---

## 📈 场景特点

### 与S011的对比

| 维度 | S011（夜间飞行） | S012（时间窗口） |
|------|------------------|------------------|
| **规则类型** | 全局时间规则 | 时间+空间组合规则 |
| **触发条件** | 夜间 → 需要灯光+培训 | 夜间 AND 医院内 → 禁飞 |
| **空间依赖** | 无（全局适用） | 有（仅医院区域） |
| **逻辑类型** | 单条件 | AND组合条件 |
| **测试用例** | 8个 | 5个 |

### 复杂度

- **空间复杂度**: ⭐⭐ 中等（圆柱体检测）
- **时间复杂度**: ⭐ 简单（复用S011逻辑）
- **逻辑复杂度**: ⭐⭐ 中等（AND组合）
- **总体复杂度**: ⭐⭐ 中等

### 关键挑战

1. ⚡ **AND逻辑实现**：两个条件同时满足才拒绝
2. 🎯 **单条件处理**：单条件满足不应拒绝
3. 🔄 **代码复用**：时间判断复用S011，区域检测复用S002/S010

---

## ✅ 成功标准

1. ✅ TC1正确批准（基线）
2. ✅ TC2正确批准（仅在医院内，但白天）⭐
3. ✅ TC3正确批准（仅在夜间，但医院外）⭐
4. ✅ TC4正确拒绝（夜间+医院内）⭐⭐
5. ✅ TC5正确拒绝（边界值22:00）
6. ✅ 拒绝理由清晰，说明时间窗口和区域
7. ✅ 批准的轨迹完整，拒绝的仅有起点

---

**文档版本**: 1.0  
**创建日期**: 2025-10-31  
**场景作者**: Claude & 张耘实  
**测试框架**: AirSim-RuleBench v1.0  
**测试用例数**: 5个（比S011的8个少，重点测试AND逻辑）

