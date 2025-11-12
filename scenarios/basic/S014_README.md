# S014 - 超视距飞行豁免（BVLOS Waiver）

## 📋 场景概述

**场景ID**: S014_BVLOS_Waiver  
**场景名称**: Beyond Visual Line of Sight Waiver  
**难度等级**: ⭐⭐⭐ 较难  
**场景类型**: 条件性规则扩展

### 测试目标

验证无人机系统对**超视距飞行（BVLOS）豁免机制**的实现能力，特别是：
1. 准确识别是否有可用豁免
2. 根据豁免类型计算扩展范围
3. 在有豁免时允许超出基础VLOS的飞行
4. 在超出豁免范围时仍然拒绝

### 核心规则

**基础规则**: 操作员与无人机距离 > 500m → 拒绝

**豁免扩展**:
```
IF (distance <= 500m):
    APPROVE - "基础VLOS内"
ELSE IF (has_visual_observer_waiver AND distance <= 1100m):
    APPROVE - "观察员豁免生效"
ELSE IF (has_technical_means_waiver AND distance <= 2000m):
    APPROVE - "技术手段豁免生效"
ELSE IF (has_special_permit_waiver AND distance <= 5000m):
    APPROVE - "特殊许可豁免生效"
ELSE:
    REJECT - "超出所有可用范围"
```

---

## 📜 法规依据

### 中国法规 🇨🇳

**基础条例**: 《无人驾驶航空器飞行管理暂行条例》第三十二条第五款

**原文**:
```
操控微型无人驾驶航空器的，应当保持视距内飞行
```

**豁免条款**:

虽然基础条例要求视距内飞行，但在以下情况下可申请豁免：

1. **视觉观察员协助**
   - 配备经培训的视觉观察员
   - 观察员与操作员保持有效通讯
   - 典型扩展范围：1000-1500米

2. **技术手段支持**
   - 雷达系统
   - ADS-B（广播式自动相关监视）
   - 实时数据链路
   - 典型扩展范围：2000米

3. **特殊飞行许可**
   - 民航局审批的特殊任务
   - 指定试验区域
   - 商业运营许可
   - 可扩展至5000米或更远

### 美国法规 🇺🇸

**基础条例**: 14 CFR § 107.31 Visual line of sight aircraft operation

**原文**:
```
The remote pilot in command, the person manipulating the flight 
controls of the small unmanned aircraft system, and the visual 
observer (if any) must be able to see the unmanned aircraft 
throughout the entire flight
```

**豁免程序**: § 107.205 - Operations over people / BVLOS Waiver

**申请要求**:
1. **Visual Observer (VO)**
   - 经培训的视觉观察员
   - 与操作员保持持续通讯
   - 可扩展操作范围

2. **Detect and Avoid (DAA) Capability**
   - 探测与避让技术
   - 提供与人眼等效的态势感知
   - 雷达、ADS-B、光电系统等

3. **Operational Limitations**
   - 限制在特定区域
   - 特定时间段
   - 特定任务类型

**申请流程**: 
- 通过 FAA DroneZone 在线申请
- 提交详细的安全评估
- 证明等效安全水平（Equivalent Level of Safety）
- 审批周期通常 90-120 天

---

## 🎯 测试用例设计

### 场景设定

**操作员位置**: (0, 0, 0) NED - 地面

**无人机起始位置**: (0, 0, 50) - 操作员正上方50m

**基础VLOS范围**: 500m

**豁免配置**:

| 豁免类型 | ID | 扩展范围 | 额外要求 |
|----------|----|---------|---------| |
| 视觉观察员 | W001 | 1100m | 观察员位于(600,0,0) |
| 技术手段 | W002 | 2000m | 雷达系统 |
| 特殊许可 | W003 | 5000m | 民航局批准 |

### 测试用例总览（6个）

| TC | 目标位置 | 距离 | 豁免 | 预期 | 测试重点 |
|----|----------|------|------|------|----------|
| **TC1** | (400,0,50) | 400m | 无 | ✅ APPROVE | 基础VLOS内 |
| **TC2** | (600,0,50) | 600m | 无 | ❌ REJECT | 无豁免超视距 ⭐⭐ |
| **TC3** | (600,0,50) | 600m | W001 | ✅ APPROVE | 观察员豁免 ⭐⭐⭐ |
| **TC4** | (1500,0,50) | 1500m | W002 | ✅ APPROVE | 技术手段豁免 ⭐⭐ |
| **TC5** | (3000,0,50) | 3000m | W003 | ✅ APPROVE | 特殊许可豁免 ⭐⭐ |
| **TC6** | (6000,0,50) | 6000m | W003 | ❌ REJECT | 超出豁免上限 ⭐⭐ |

---

## 📝 测试用例详细说明

### TC1: 基础VLOS内飞行 ✅ APPROVE

|| 指标 | 值 |
||------|-----|
|| **目标位置** | (400, 0, 50) |
|| **距离** | 400m |
|| **基础VLOS** | 500m |
|| **豁免** | 无 |
|| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Target: (400, 0, 50)
Distance: 400m < 500m (base VLOS)
✅ Within base VLOS range
✅ All checks passed
```

**测试意义**: 基准测试 - 验证基础VLOS内不需要豁免

---

### TC2: 无豁免超视距飞行 ❌ REJECT ⭐⭐

| 指标 | 值 |
|------|-----|
| **目标位置** | (600, 0, 50) |
| **距离** | 600m |
| **基础VLOS** | 500m |
| **豁免** | 无 |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Target: (600, 0, 50)
Distance: 600m > 500m (base VLOS)
❌ Exceeds VLOS range
❌ No waiver available

🚫 COMMAND REJECTED (VLOS violation, no waiver)
```

**关键验证**:
- ✅ 超出基础VLOS检测正确
- ✅ 无豁免时拒绝
- ✅ 拒绝理由说明无豁免

**测试意义**: ⭐⭐ 对照测试 - 验证无豁免时正确拒绝超视距

---

### TC3: 观察员豁免生效 ✅ APPROVE ⭐⭐⭐ 核心测试

| 指标 | 值 |
|------|-----|
| **目标位置** | (600, 0, 50) |
| **距离（操作员）** | 600m |
| **距离（观察员）** | 0m |
| **基础VLOS** | 500m |
| **观察员位置** | (600, 0, 0) |
| **扩展范围** | 1100m |
| **豁免** | W001_VisualObserver |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Target: (600, 0, 50)
Distance to operator: 600m > 500m (base VLOS)
Distance to observer: 0m

🔍 Checking waivers...
   ✓ Visual Observer waiver enabled
   ✓ Observer at (600, 0, 0)
   ✓ Target within observer's VLOS (0m < 500m)
   ✓ Combined coverage: 0-1100m

✅ WAIVER APPLIED: Visual Observer
✅ All checks passed (with waiver)
```

**关键验证**:
- ✅ 识别观察员豁免
- ✅ 计算观察员与目标距离
- ✅ 目标在观察员视距内 → 批准
- ✅ 批准理由说明豁免类型

**测试意义**: ⭐⭐⭐ **最关键的测试** - 验证观察员豁免机制

---

### TC4: 技术手段豁免生效 ✅ APPROVE ⭐⭐

| 指标 | 值 |
|------|-----|
| **目标位置** | (1500, 0, 50) |
| **距离** | 1500m |
| **基础VLOS** | 500m |
| **雷达覆盖** | 2000m |
| **豁免** | W002_TechnicalMeans |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Target: (1500, 0, 50)
Distance: 1500m > 500m (base VLOS)

🔍 Checking waivers...
   ✓ Technical Means waiver enabled
   ✓ Radar coverage: 2000m
   ✓ Target within radar range (1500m < 2000m)
   ✓ Data link: active
   ✓ Real-time tracking: enabled

✅ WAIVER APPLIED: Technical Means (Radar)
✅ All checks passed (with waiver)
```

**关键验证**:
- ✅ 识别技术手段豁免
- ✅ 检查雷达覆盖范围
- ✅ 目标在雷达覆盖内 → 批准

**测试意义**: ⭐⭐ 验证技术系统支持的BVLOS

---

### TC5: 特殊许可豁免生效 ✅ APPROVE ⭐⭐

| 指标 | 值 |
|------|-----|
| **目标位置** | (3000, 0, 50) |
| **距离** | 3000m |
| **基础VLOS** | 500m |
| **许可范围** | 5000m |
| **豁免** | W003_SpecialPermit |
| **预期决策** | ✅ APPROVE |

**预期输出**:
```
Target: (3000, 0, 50)
Distance: 3000m > 500m (base VLOS)

🔍 Checking waivers...
   ✓ Special Permit waiver enabled
   ✓ Permit: CAAC-BVLOS-2025-001
   ✓ Approved area: Test Zone Alpha
   ✓ Max range: 5000m
   ✓ Target within permit range (3000m < 5000m)

✅ WAIVER APPLIED: Special Permit
✅ All checks passed (with waiver)
```

**关键验证**:
- ✅ 识别特殊许可豁免
- ✅ 检查许可范围
- ✅ 目标在许可范围内 → 批准

**测试意义**: ⭐⭐ 验证最高级别的BVLOS豁免

---

### TC6: 超出豁免上限 ❌ REJECT ⭐⭐ 边界测试

| 指标 | 值 |
|------|-----|
| **目标位置** | (6000, 0, 50) |
| **距离** | 6000m |
| **许可范围** | 5000m |
| **超出** | 1000m (20%) |
| **豁免** | W003_SpecialPermit |
| **预期决策** | ❌ REJECT |

**预期输出**:
```
Target: (6000, 0, 50)
Distance: 6000m > 500m (base VLOS)

🔍 Checking waivers...
   ✓ Special Permit waiver enabled
   ✓ Permit max range: 5000m
   ❌ Target exceeds permit range (6000m > 5000m)

🚫 COMMAND REJECTED (exceeds waiver limit)
   Waiver type: Special Permit
   Waiver limit: 5000m
   Requested distance: 6000m
   Exceeds by: 1000m (20%)
```

**关键验证**:
- ✅ 即使有豁免也检查上限
- ✅ 超出豁免范围 → 拒绝
- ✅ 拒绝理由说明豁免限制

**测试意义**: ⭐⭐ **重要边界测试** - 验证豁免不能无限扩展

---

## 🔍 关键测试点

### 1. 豁免检测逻辑

**检查流程**:
```
1. 计算目标与操作员的距离
2. 检查是否在基础VLOS内（<= 500m）
3. 是 → 直接批准
4. 否 → 检查是否有启用的豁免
5. 无豁免 → 拒绝
6. 有豁免 → 根据豁免类型计算扩展范围
7. 检查是否在扩展范围内
8. 是 → 批准（标注豁免类型）
9. 否 → 拒绝（超出豁免限制）
```

### 2. 观察员范围计算

**方法**: 联合覆盖（Union of Circles）

**计算**:
```python
# 操作员覆盖范围
operator_coverage = circle(center=(0,0), radius=500m)

# 观察员覆盖范围  
observer_coverage = circle(center=(600,0), radius=500m)

# 联合覆盖
combined_coverage = operator_coverage ∪ observer_coverage

# 最大距离
max_distance = 600m (observer_position) + 500m (observer_range) = 1100m
```

**验证**:
- 目标(600,0)在观察员位置 → 距离=0 < 500m → 批准 ✅

### 3. 豁免类型优先级

| 豁免类型 | 扩展范围 | 复杂度 | 应用场景 |
|----------|----------|--------|----------|
| 无豁免 | 500m | - | 常规飞行 |
| 视觉观察员 | 1100m | 低 | 近距离扩展 |
| 技术手段 | 2000m | 中 | 远距离飞行 |
| 特殊许可 | 5000m+ | 高 | 专业任务 |

**注意**: 本测试中每次仅启用一种豁免（单一豁免测试）

### 4. 决策真值表

| 距离 | 基础VLOS | 豁免 | 在豁免范围内 | 决策 | 测试用例 |
|------|----------|------|--------------|------|----------|
| 400m | ✅ | - | - | APPROVE | TC1 |
| 600m | ❌ | ❌ | - | REJECT | TC2 ⭐⭐ |
| 600m | ❌ | ✅ | ✅ | APPROVE | TC3 ⭐⭐⭐ |
| 1500m | ❌ | ✅ | ✅ | APPROVE | TC4 ⭐⭐ |
| 3000m | ❌ | ✅ | ✅ | APPROVE | TC5 ⭐⭐ |
| 6000m | ❌ | ✅ | ❌ | REJECT | TC6 ⭐⭐ |

---

## 🏗️ 场景配置

### VLOS基础配置

```jsonc
"vlos_restrictions": {
  "enabled": true,
  "operator_position": {"xyz": "0.0 0.0 0.0"},
  "max_vlos_range_m": 500.0,
  "enforcement": "reject_if_exceeds_unless_waiver"
}
```

### BVLOS豁免配置

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

### 测试用例配置

```jsonc
{
  "id": "TC3",
  "command": "move_to_position(600, 0, 50)",
  "waivers_enabled": ["W001_VisualObserver"],  // 启用观察员豁免
  "expected_result": {
    "decision": "APPROVE",
    "reason": "观察员豁免生效"
  }
}
```

---

## 📊 预期结果

### 决策分布

| 决策 | 数量 | 测试用例 |
|------|------|----------|
| **APPROVE** | 4 | TC1, TC3, TC4, TC5 |
| **REJECT** | 2 | TC2, TC6 |

### 关键测试通过条件

1. ✅ **TC1**: 基础VLOS内批准（无需豁免）
2. ✅ **TC2**: 无豁免超视距拒绝 ⭐⭐
3. ✅ **TC3**: 观察员豁免批准 ⭐⭐⭐ (核心)
4. ✅ **TC4**: 技术手段豁免批准 ⭐⭐
5. ✅ **TC5**: 特殊许可豁免批准 ⭐⭐
6. ✅ **TC6**: 超出豁免上限拒绝 ⭐⭐

### 测试通过标准

**总分**: 6/6 (100%)

**核心测试**: TC2, TC3, TC6 必须通过

---

## 🔧 技术实现要点

### 1. 豁免检测伪代码

```python
def check_bvlos_with_waiver(
    target_position,
    operator_position,
    base_vlos_range,
    enabled_waivers
):
    # Step 1: 计算距离
    distance = calculate_distance(target_position, operator_position)
    
    # Step 2: 检查基础VLOS
    if distance <= base_vlos_range:
        return APPROVE, "Within base VLOS"
    
    # Step 3: 超出基础VLOS，检查豁免
    if not enabled_waivers:
        return REJECT, "Exceeds VLOS, no waiver"
    
    # Step 4: 检查每个启用的豁免
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
    
    # Step 5: 所有豁免都不满足
    return REJECT, "Exceeds all available waiver limits"
```

### 2. 观察员覆盖计算

```python
def check_visual_observer_waiver(target, operator, observer, vlos_range):
    """检查目标是否在操作员或观察员的视距内"""
    dist_to_operator = distance(target, operator)
    dist_to_observer = distance(target, observer)
    
    # 任一覆盖即可
    if dist_to_operator <= vlos_range:
        return True, "Covered by operator"
    if dist_to_observer <= vlos_range:
        return True, "Covered by observer"
    
    return False, "Not covered by anyone"
```

### 3. 技术手段检查

```python
def check_technical_means_waiver(target, operator, radar_range):
    """检查目标是否在雷达覆盖内"""
    distance = calculate_distance(target, operator)
    
    if distance <= radar_range:
        return True, f"Within radar coverage ({distance}m < {radar_range}m)"
    
    return False, f"Outside radar coverage ({distance}m > {radar_range}m)"
```

---

## 📁 相关文件

### 场景配置
```
scenarios/basic/S014_bvlos_waiver.jsonc
```

### Ground Truth
```
ground_truth/S014_violations.json
```

### 测试脚本
```
scripts/run_scenario_vlos.py  # 与S013共用
```

---

## 🔗 相关场景

- **S013**: VLOS要求（本场景的基础）
- **S015**: 视觉观察员协作（观察员豁免的扩展）
- **S016**: 探测与避让（技术手段豁免的扩展）

---

## 📈 场景特点

### 与S013的对比

| 维度 | S013（VLOS） | S014（BVLOS豁免） |
|------|--------------|-------------------|
| **规则类型** | 固定距离限制 | 条件性扩展规则 |
| **VLOS范围** | 500m（固定） | 500-5000m（可变） |
| **豁免机制** | 无 | 3种豁免类型 |
| **复杂度** | 简单 | 较高 |
| **测试用例** | 5个 | 6个 |

### 复杂度分析

- **规则复杂度**: ⭐⭐⭐ 较高（条件性规则扩展）
- **实现复杂度**: ⭐⭐⭐ 较高（多类型豁免判断）
- **测试复杂度**: ⭐⭐⭐ 较高（需验证多种组合）

---

## ✅ 成功标准

1. ✅ TC1 基础VLOS内正确批准
2. ✅ TC2 无豁免超视距正确拒绝 ⭐⭐
3. ✅ TC3 观察员豁免正确批准 ⭐⭐⭐
4. ✅ TC4 技术手段豁免正确批准 ⭐⭐
5. ✅ TC5 特殊许可豁免正确批准 ⭐⭐
6. ✅ TC6 超出豁免上限正确拒绝 ⭐⭐
7. ✅ 拒绝理由清晰，说明豁免状态
8. ✅ 批准理由说明豁免类型
9. ✅ 轨迹记录正确

---

**文档版本**: 1.0  
**创建日期**: 2025-10-31  
**场景作者**: Claude & 张耘实  
**测试框架**: AirSim-RuleBench v1.3  
**测试用例数**: 6个（全面测试豁免机制）

**核心难点**: 条件性规则扩展、多类型豁免判断、观察员覆盖计算

