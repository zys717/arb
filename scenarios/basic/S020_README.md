# S020: 飞行申请时限规则

## 📋 场景概述

**场景ID**: S020_ApprovalTimeline  
**难度等级**: ⭐⭐  
**场景类型**: 申请时限验证  
**版本**: 1.0  
**创建日期**: 2025-11-01

### 核心测试目标

验证无人机系统对**飞行申请时限规则**的合规性检查能力，包括：
1. **36小时提前申请**：管制空域飞行需提前≥36小时申请
2. **边界值测试**：恰好36小时是否满足要求
3. **紧急任务豁免**：紧急救援可豁免时限要求
4. **适飞空域免申请**：适飞空域内飞行无需提前申请
5. **时间计算准确性**：正确计算申请时间与飞行时间差

---

## 🎯 规则定义

### R020: 飞行申请时限规则

| 条件 | 要求 | 豁免 | 说明 |
|-----|------|------|------|
| **管制空域飞行** | 提前≥36小时申请 | ❌ | 拟飞行前1日12时前提出申请 |
| **紧急任务** | 可在起飞前申请 | ✅ | 搜救、灾害应对等任务 |
| **适飞空域飞行** | 无需申请 | ✅ | 高度<120m + 非管制区域 |
| **边界值（36h）** | 满足要求 | ❌ | 使用 `>=` 判断 |

### 法规依据

1. **中国《条例》第26条** - 飞行申请时限
   > "拟飞行前1日12时前提出飞行活动申请"
   > 
   > 解读：若明天下午3点飞行，需在今天中午12点前申请 → 提前≥27小时
   > 
   > 实际操作：通常要求提前36小时（1.5天）

2. **中国《条例》第31条第一款** - 适飞空域豁免
   > "微型、轻型、小型无人驾驶航空器在适飞空域内的飞行活动...无需提出飞行活动申请"

3. **美国LAANC系统** - 实时授权
   > Low Altitude Authorization and Notification Capability
   > 
   > 支持实时或近实时（数分钟内）授权

### 时间计算

```python
# 计算申请时间到飞行时间的时间差
time_diff_hours = (planned_flight_time - application_time) / 3600

# 判断是否满足要求
if time_diff_hours >= 36.0:
    return "APPROVE"
else:
    return "REJECT", f"仅提前{time_diff_hours}小时，需≥36小时"
```

**边界判断**: 使用 `>=`，36.0小时恰好满足要求

---

## 🧪 测试用例

### TC1: 申请时间过晚 🚫

**测试目标**: 验证时限不足时的拒绝逻辑

**时间设置**:
```
当前时间: 2024-10-20 10:00
申请时间: 2024-10-21 09:00 (明天上午9点)
飞行时间: 2024-10-21 15:00 (明天下午3点)
时间差: 6小时
```

**目标**: (1000, 0, 50) - 在管制区域内  
**任务类型**: normal  
**预期结果**: 🚫 **REJECT**  
**预期原因**: 申请时间距飞行仅6小时，未满足提前36小时申请要求

**验证点**:
- ✅ 时间差计算准确：6小时
- ✅ 6 < 36 → 不满足要求
- ✅ 在管制区域内（需要申请）
- ✅ 非紧急任务（无豁免）
- ✅ 拒绝原因清晰

---

### TC2: 按时提前申请 + 边界测试 ✅

**测试目标**: 验证充足提前量和边界值（两阶段测试）

#### 阶段1: 充足提前量

**时间设置**:
```
当前时间: 2024-10-20 10:00
申请时间: 2024-10-20 10:00 (当前时间)
飞行时间: 2024-10-22 14:00 (后天下午2点)
时间差: 52小时
```

**验证**: 52 > 36 → **PASS** ✅

#### 阶段2: 边界值测试（36小时）

**时间设置**:
```
当前时间: 2024-10-20 10:00
申请时间: 2024-10-20 10:00 (当前时间)
飞行时间: 2024-10-21 22:00 (明天晚上10点)
时间差: 恰好36小时
```

**验证**: 36 >= 36 → **PASS** ✅ （使用 `>=` 判断）

**目标**: (1000, 0, 50) - 在管制区域内  
**任务类型**: normal  
**预期结果**: ✅ **APPROVE**  
**预期原因**: 申请时间满足提前36小时要求，批准飞行

**验证点**:
- ✅ 阶段1: 52小时提前量，远超要求
- ✅ 阶段2: 恰好36小时边界测试
- ✅ 边界判断使用 `>=` (inclusive)
- ✅ 在管制区域内但有足够提前量
- ✅ 两阶段测试提升TC质量

---

### TC3: 紧急任务豁免 ✅

**测试目标**: 验证紧急任务的时限豁免机制

**时间设置**:
```
当前时间: 2024-10-20 10:00
申请时间: 2024-10-20 10:00 (当前时间)
飞行时间: 2024-10-20 10:30 (30分钟后)
时间差: 0.5小时
```

**任务详情**:
```json
{
  "flight_type": "emergency",
  "mission_type": "search_and_rescue",
  "priority": "high",
  "approved_by": "emergency_response_center"
}
```

**目标**: (1000, 0, 50) - 在管制区域内  
**预期结果**: ✅ **APPROVE**  
**预期原因**: 紧急救援任务豁免时限要求，批准在30分钟后起飞

**验证点**:
- ✅ 时间差仅0.5小时（正常情况会拒绝）
- ✅ 任务类型：emergency (search_and_rescue)
- ✅ 豁免条件满足
- ✅ 即使在管制空域也批准
- ✅ 紧急任务优先级高于时限要求

**应用场景**:
- 🚑 搜索救援（Search and Rescue）
- 🔥 火灾应对（Fire Response）
- 🌊 洪水救援（Flood Response）
- 🏥 医疗物资运输（Medical Emergency）

---

### TC4: 适飞空域免申请 ✅

**测试目标**: 验证适飞空域的免申请条件

**时间设置**:
```
当前时间: 2024-10-20 10:00
申请时间: null (未申请)
飞行时间: 2024-10-20 10:30 (30分钟后)
```

**目标**: (300, 0, 50) - 在适飞空域  
**空域检查**:
- 高度: 50m < 120m → 适飞空域 ✅
- 位置: 距管制区域中心700m > 半径500m → 外部 ✅
- 豁免: 轻型无人机在适飞空域 ✅

**任务类型**: normal  
**预期结果**: ✅ **APPROVE**  
**预期原因**: 适飞空域内飞行（高度50m<120m，非管制区域），无需提前申请

**验证点**:
- ✅ 高度: 50m < 120m → 适飞空域
- ✅ 位置: 距管制区域中心700m > 半径500m → 外部
- ✅ 无申请时间（null）
- ✅ 豁免条件: 适飞空域
- ✅ 即使当天起飞也批准
- ✅ 空域优先级高于时限检查

---

## 📊 测试覆盖矩阵

| 规则维度 | 测试用例 | 通过 | 拒绝 | 覆盖率 |
|---------|---------|------|------|-------|
| **时限不足** | TC1 | 0 | 1 | 100% |
| **时限充足** | TC2 (phase 1) | 1 | 0 | 100% |
| **边界值（36h）** | TC2 (phase 2) | 1 | 0 | 100% |
| **紧急豁免** | TC3 | 1 | 0 | 100% |
| **适飞空域豁免** | TC4 | 1 | 0 | 100% |
| **管制区域检测** | TC1, TC2, TC3 | 2 | 1 | 100% |
| **时间计算** | 全部TC | 3 | 1 | 100% |

**总计**: 4个测试用例，预期3个APPROVE，1个REJECT

---

## 🔧 技术实现要点

### 1. 时间差计算

```python
from datetime import datetime

def calculate_hours_difference(
    application_time: str,
    planned_flight_time: str
) -> float:
    """
    计算申请时间到飞行时间的小时差
    """
    app_dt = datetime.fromisoformat(application_time.replace('Z', '+00:00'))
    flight_dt = datetime.fromisoformat(planned_flight_time.replace('Z', '+00:00'))
    
    time_diff = flight_dt - app_dt
    hours = time_diff.total_seconds() / 3600
    
    return hours
```

**关键点**:
- 使用ISO 8601格式（带时区）
- 计算秒数后除以3600得到小时
- TC1验证: 6小时
- TC2验证: 52小时和36小时

### 2. 管制区域检测

```python
def is_in_controlled_zone(
    position: Dict[str, float],
    zone_center: Dict[str, float],
    zone_radius: float
) -> bool:
    """检查位置是否在管制区域内"""
    distance = math.sqrt(
        (position['north'] - zone_center['north'])**2 +
        (position['east'] - zone_center['east'])**2
    )
    return distance <= zone_radius
```

**验证**:
- TC1/TC2/TC3: (1000, 0) 距中心0m → 在区域内
- TC4: (500, 0) 距中心500m → 在区域外

### 3. 豁免条件检查

```python
def check_exemptions(
    flight_type: str,
    position: Dict,
    altitude: float,
    in_controlled_zone: bool
) -> Tuple[bool, str]:
    """
    检查豁免条件
    优先级: 适飞空域 > 紧急任务 > 时限检查
    """
    # 优先级1: 适飞空域豁免
    if not in_controlled_zone and altitude < 120.0:
        return True, "UNCONTROLLED_AIRSPACE"
    
    # 优先级2: 紧急任务豁免
    if flight_type == "emergency":
        return True, "EMERGENCY_MISSION"
    
    # 需要检查时限
    return False, None
```

### 4. 综合决策逻辑

```python
def check_flight_approval(
    application_time: Optional[str],
    planned_flight_time: str,
    flight_type: str,
    target: Dict,
    controlled_zone: Dict,
    advance_hours_required: float = 36.0
) -> Tuple[bool, str]:
    """
    综合决策逻辑
    """
    # 检查豁免条件
    is_exempt, exemption_type = check_exemptions(
        flight_type,
        target,
        target['altitude'],
        is_in_controlled_zone(target, controlled_zone['center'], controlled_zone['radius'])
    )
    
    if is_exempt:
        if exemption_type == "UNCONTROLLED_AIRSPACE":
            return True, "适飞空域内飞行，无需提前申请"
        elif exemption_type == "EMERGENCY_MISSION":
            return True, "紧急任务豁免时限要求"
    
    # 需要检查时限
    if application_time is None:
        return False, "管制空域飞行需要提前申请"
    
    hours_diff = calculate_hours_difference(application_time, planned_flight_time)
    
    if hours_diff >= advance_hours_required:
        return True, f"申请时间满足提前{advance_hours_required}小时要求"
    else:
        return False, f"申请时间距飞行仅{hours_diff:.1f}小时，需≥{advance_hours_required}小时"
```

---

## 📈 预期结果分析

### 决策分布

```
✅ APPROVE: 3/4 (75%)
  - TC2: 按时提前申请（52h + 36h边界）
  - TC3: 紧急任务豁免
  - TC4: 适飞空域免申请

🚫 REJECT: 1/4 (25%)
  - TC1: 申请时间过晚（6h < 36h）
```

### 时间差分布

| TC | 时间差 | 要求 | 结果 | 原因 |
|----|--------|------|------|------|
| TC1 | 6h | ≥36h | REJECT | 时限不足 |
| TC2-1 | 52h | ≥36h | APPROVE | 充足 |
| TC2-2 | 36h | ≥36h | APPROVE | 边界 |
| TC3 | 0.5h | 豁免 | APPROVE | 紧急任务 |
| TC4 | 0.5h | 豁免 | APPROVE | 适飞空域 |

### 豁免机制验证

```
豁免条件使用:
- 适飞空域豁免: 1/4 (TC4)
- 紧急任务豁免: 1/4 (TC3)
- 无豁免: 2/4 (TC1, TC2)
```

---

## 🎓 学习要点

### 1. 时间计算的重要性

- **精确计算**: 使用datetime库，考虑时区
- **单位转换**: 秒 → 小时（除以3600）
- **边界处理**: 36.0小时恰好满足（使用 `>=`）

### 2. 豁免条件的优先级

```
优先级顺序:
1. 适飞空域豁免（最高）
   └─ 高度<120m + 非管制区域 → 无需申请
2. 紧急任务豁免
   └─ emergency类型 → 可立即起飞
3. 时限检查
   └─ ≥36小时 → 批准
```

### 3. 多阶段测试的价值

**TC2包含两个阶段**:
- 阶段1: 验证充足提前量（52h）
- 阶段2: 验证边界值（36h）

**优势**:
- 提升单个TC的覆盖率
- 减少TC总数但保持质量
- 更接近实际应用场景

### 4. 实际应用场景

#### 场景1: 商业配送

```
计划: 明天下午3点配送
申请: 今天上午10点申请
时间差: 29小时
结果: REJECT（需≥36小时）
```

#### 场景2: 航拍任务

```
计划: 后天上午10点航拍
申请: 今天下午2点申请
时间差: 44小时
结果: APPROVE（满足要求）
```

#### 场景3: 应急救援

```
计划: 现在立即起飞救援
申请: 现在申请
时间差: 0小时
任务类型: emergency
结果: APPROVE（豁免时限）
```

#### 场景4: 农田巡检

```
计划: 20分钟后巡检农田
申请: 无
位置: 农村，高度60m
结果: APPROVE（适飞空域免申请）
```

---

## 🚀 后续扩展方向

1. **动态审批流程**: 模拟审批状态变化（pending → approved → rejected）
2. **批复时限**: 验证"飞行前1日21时前批复"的要求
3. **多日申请**: 测试跨多天的申请场景
4. **取消与变更**: 飞行计划的取消和时间变更
5. **LAANC集成**: 美国实时授权系统的模拟

---

**场景状态**: ✅ 设计完成，待实现  
**预计开发时间**: 3-4小时  
**难度评估**: ⭐⭐（时间计算+豁免逻辑）

