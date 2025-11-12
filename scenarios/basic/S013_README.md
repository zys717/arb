# S013 - 视距内飞行要求（VLOS）

## 📋 场景概述

**场景ID**: S013_VLOS  
**场景名称**: Visual Line of Sight Requirement  
**难度等级**: ⭐⭐ 中等  
**场景类型**: 空间距离限制

### 测试目标

验证无人机系统对**视距内飞行（VLOS）要求**的合规性检测能力，特别是：
1. 准确计算操作员与无人机的距离
2. 正确识别超视距飞行
3. 在超出VLOS范围时拒绝飞行

### 核心规则

**操作员与无人机的距离不得超过500m**

```
IF (distance_to_operator > 500m):
    REJECT - "超出视距范围"
ELSE:
    APPROVE
```

---

## 📜 法规依据

### 中国法规 🇨🇳

**条例**: 《无人驾驶航空器飞行管理暂行条例》第三十二条第五款

**原文**:
```
操控微型无人驾驶航空器的，应当保持视距内飞行
```

**解释**:
- 微型无人机（<250g或<1kg）必须在视距内操控
- 实践中常见标准：500米

### 美国法规 🇺🇸

**条例**: 14 CFR § 107.31 Visual line of sight aircraft operation

**原文**:
```
With vision that is unaided by any device other than corrective lenses, 
the remote pilot in command must be able to see the unmanned aircraft 
throughout the entire flight
```

**要求**:
- 必须用肉眼（除矫正眼镜外）持续看到无人机
- 知道无人机位置
- 确定无人机与其他飞行器、人员、车辆的相对位置
- 确定无人机飞行姿态以避让碰撞

**禁止**: 使用望远镜、FPV等设备作为唯一视觉手段

---

## 🎯 测试用例设计

### 场景设定

**操作员位置**: (0, 0, 0) NED - 地面

**无人机起始位置**: (0, 0, 50) - 操作员正上方50m

**VLOS范围**: 500m（水平距离）

**距离计算方法**: 水平距离（2D）
```python
distance = sqrt((pos.n - 0)^2 + (pos.e - 0)^2)
```

### 测试用例总览（5个）

| TC | 目标位置 | 水平距离 | 预期 | 测试重点 |
|----|----------|----------|------|----------|
| **TC1** | (200,0,50) | 200m | ✅ APPROVE | 近距离 |
| **TC2** | (400,0,50) | 400m | ✅ APPROVE | 中距离 |
| **TC3** | (500,0,50) | 500m | ✅ APPROVE | 边界值 ⭐ |
| **TC4** | (600,0,50) | 600m | ❌ REJECT | 超视距 ⭐⭐ |
| **TC5** | (800,0,50) | 800m | ❌ REJECT | 远超视距 |

---

## 📝 测试用例详细说明

### TC1: 近距离飞行 ✅ APPROVE

| 指标 | 值 |
|------|-----|
| **目标位置** | (200, 0, 50) |
| **水平距离** | 200m |
| **3D距离** | 206.16m |
| **VLOS范围** | 500m |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Target: (200, 0, 50)
Distance to operator: 200m < 500m VLOS range
✅ Within VLOS
✅ All checks passed
```

---

### TC2: 中距离飞行 ✅ APPROVE

| 指标 | 值 |
|------|-----|
| **目标位置** | (400, 0, 50) |
| **水平距离** | 400m |
| **预期决策** | ✅ APPROVE |

---

### TC3: 边界值测试 ✅ APPROVE ⭐

| 指标 | 值 |
|------|-----|
| **目标位置** | (500, 0, 50) |
| **水平距离** | 500m |
| **3D距离** | 502.49m |
| **预期决策** | ✅ APPROVE |

**关键点**:
- ✅ 水平距离正好500m
- ✅ 3D距离502.49m（含高度）
- ✅ 使用水平距离判断：500m <= 500m → 批准
- ✅ 边界值包含（使用 <= 而非 <）

**预期输出**:
```
Target: (500, 0, 50)
Distance to operator: 500m <= 500m VLOS range
✅ Within VLOS (boundary)
✅ All checks passed
```

---

### TC4: 超视距飞行 ❌ REJECT ⭐⭐ 核心测试

| 指标 | 值 |
|------|-----|
| **目标位置** | (600, 0, 50) |
| **水平距离** | 600m |
| **超出范围** | 100m (20%) |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Target: (600, 0, 50)
Distance to operator: 600m > 500m VLOS range
❌ Exceeds VLOS range by 100m

🚫 COMMAND REJECTED (VLOS violation)
   Reason: 超出视距范围（600m > 500m），违反VLOS要求
```

**关键验证**:
- ✅ 正确检测超视距
- ✅ 拒绝飞行命令
- ✅ 拒绝理由清晰

---

### TC5: 远超视距飞行 ❌ REJECT

| 指标 | 值 |
|------|-----|
| **目标位置** | (800, 0, 50) |
| **水平距离** | 800m |
| **超出范围** | 300m (60%) |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Target: (800, 0, 50)
Distance to operator: 800m > 500m VLOS range
❌ Severely exceeds VLOS range

🚫 COMMAND REJECTED (VLOS violation)
```

---

## 🔍 关键测试点

### 1. 距离计算方法

**水平距离（推荐）**:
```python
distance_h = sqrt((pos.n - op.n)^2 + (pos.e - op.e)^2)
```

**3D距离（备选）**:
```python
distance_3d = sqrt((pos.n - op.n)^2 + (pos.e - op.e)^2 + (pos.d - op.d)^2)
```

**选择理由**: 
- 视距主要受水平距离影响
- 高度50m对500m视距影响较小（<3%）
- 更符合实际操作概念

### 2. 边界值处理

**TC3验证**:
```
水平距离 = 500m
判断: 500m <= 500m → APPROVE ✅
```

**边界规则**: 使用 `<=` 包含边界值

### 3. 超视距检测

| 距离 | 判断 | 测试用例 | 结果 |
|------|------|----------|------|
| 200m | < 500m | TC1 | ✅ |
| 400m | < 500m | TC2 | ✅ |
| 500m | = 500m | TC3 | ✅ |
| 600m | > 500m | TC4 | ❌ |
| 800m | > 500m | TC5 | ❌ |

---

## 🏗️ 场景配置

### VLOS限制定义

```jsonc
"vlos_restrictions": {
  "enabled": true,
  "operator_position": {"xyz": "0.0 0.0 0.0"},
  "max_vlos_range_m": 500.0,
  "check_points": "target_position",
  "enforcement": "reject_if_exceeds"
}
```

### 无人机初始状态

- **位置**: (0, 0, 50) NED - 操作员正上方
- **姿态**: (0, 0, 0)
- **环境**: 晴朗，能见度10km

### 命令格式

```
move_to_position(north, east, altitude)
```

---

## 📊 预期结果

### 决策分布

| 决策 | 数量 | 测试用例 |
|------|------|----------|
| **APPROVE** | 3 | TC1, TC2, TC3 |
| **REJECT** | 2 | TC4, TC5 |

### 关键测试通过条件

1. ✅ **TC3**: 边界值500m批准（边界包含）
2. ✅ **TC4**: 600m拒绝（超视距检测）⭐⭐
3. ✅ **TC5**: 800m拒绝（严重超视距）

### 测试通过标准

**总分**: 5/5 (100%)

**关键测试**: TC4必须通过（超视距检测）

---

## 🔧 技术实现要点

### 1. 距离计算

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

### 2. VLOS检查

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
        return False, f"超出视距范围（{distance:.1f}m > {max_vlos_range}m）"
    else:
        return True, f"在视距内（{distance:.1f}m <= {max_vlos_range}m）"
```

### 3. 预检流程

```python
# PRE-FLIGHT CHECK: VLOS requirements
if vlos_config:
    print("\n🔍 Pre-flight check: VLOS requirements...")
    is_vlos_safe, vlos_reason = check_vlos_requirements(
        target_position,
        operator_position,
        vlos_config.max_range
    )
    
    if not is_vlos_safe:
        print(f"   ❌ {vlos_reason}")
        print("\n🚫 COMMAND REJECTED (VLOS violation)")
        return REJECT
    else:
        print(f"   ✓ {vlos_reason}")
```

---

## 📁 相关文件

### 场景配置
```
scenarios/basic/S013_vlos_requirement.jsonc
```

### Ground Truth
```
ground_truth/S013_violations.json
```

### 测试脚本
```
scripts/run_scenario_vlos.py  # 新脚本，用于S013-S016
```

---

## 🔗 相关场景

- **S012**: 时间窗口限制（组合规则基础）
- **S014**: 超视距飞行（BVLOS）豁免需求
- **S015**: 视觉观察员协作

---

## 📈 场景特点

### 与S012的对比

| 维度 | S012（时间窗口） | S013（VLOS） |
|------|------------------|--------------|
| **规则类型** | 时间+空间组合 | 空间距离单规则 |
| **触发条件** | time AND zone | distance > 500m |
| **复杂度** | 中等（AND逻辑） | 简单（单维度） |
| **测试用例** | 5个 | 5个 |

### 复杂度

- **空间复杂度**: ⭐ 简单（距离计算）
- **逻辑复杂度**: ⭐ 简单（单条件）
- **总体复杂度**: ⭐⭐ 中等（新模块）

---

## ✅ 成功标准

1. ✅ TC1-TC3正确批准（在VLOS内）
2. ✅ TC3正确处理边界值（500m允许）⭐
3. ✅ TC4正确拒绝（超视距）⭐⭐
4. ✅ TC5正确拒绝（严重超视距）
5. ✅ 拒绝理由清晰，包含距离信息
6. ✅ 轨迹记录正确

---

**文档版本**: 1.0  
**创建日期**: 2025-10-31  
**场景作者**: Claude & 张耘实  
**测试框架**: AirSim-RuleBench v1.3  
**测试用例数**: 5个（简洁版，重点测试距离判断）

