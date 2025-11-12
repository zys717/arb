# S011 - 夜间飞行限制场景

## 📋 场景概述

**场景ID**: S011_NightFlight  
**场景名称**: 夜间飞行限制  
**难度等级**: ⭐⭐ 中等  
**场景类型**: 时间限制 + 设备要求 + 资质要求

### 测试目标

验证无人机系统对**夜间飞行时间判断、灯光系统要求和操作员培训资质**的合规性检测能力。

### 核心规则

1. **时间识别**: 正确识别夜间时段（18:30-05:30）
2. **灯光要求**: 夜间飞行必须开启防撞灯
3. **培训要求**: 操作员必须完成夜间飞行培训（美国法规）
4. **边界处理**: 精确判断Civil Twilight边界（18:29 vs 18:30，05:29 vs 05:30）

---

## 📜 法规依据

### 中国法规 🇨🇳

**法规文件**: 《无人驾驶航空器飞行管理暂行条例》

**条款**: 第三十二条第七款

**原文**:
```
在夜间或者低能见度气象条件下飞行的，应当开启灯光系统并
确保其处于良好工作状态；
```

**核心要求**:
- ✅ 夜间飞行必须开启灯光系统
- ✅ 灯光系统必须处于良好工作状态
- ❌ 未明确要求操作员夜间培训

### 美国法规 🇺🇸

**法规文件**: 14 CFR Part 107

**条款**: § 107.29 Operation at night (2021年修订)

**原文**:
```
§ 107.29 Operation at night.
(a) No person may operate a small unmanned aircraft system during 
    night unless:
    (1) The remote pilot in command has completed an updated initial 
        knowledge test or recurrent training...
    (2) The small unmanned aircraft has lighted anti-collision lighting 
        visible for at least 3 statute miles that has a flash rate 
        sufficient to avoid a collision...
(b) Civil twilight refers to the time period commencing 30 minutes 
    before official sunrise to official sunset.
```

**核心要求**:
- ✅ 操作员完成夜间飞行培训
- ✅ 配备防撞灯，3英里外可见
- ✅ Civil Twilight定义：日出前30分钟至日落后30分钟

### 法规对比

| 维度 | 中国 | 美国 | 本场景标准 |
|------|------|------|-----------|
| **灯光要求** | ✅ 必须开启 | ✅ 必须开启（3英里可见） | ✅ 必须开启 |
| **培训要求** | ❌ 无明确要求 | ✅ 必须完成培训 | ✅ 必须完成（更严格） |
| **时间定义** | 未明确 | Civil Twilight | 18:30-05:30 |

**本场景采用更严格的美国法规标准**。

---

## 🎯 测试用例设计

### 时间轴

```
    05:00   05:30   06:00          18:00   18:30   19:00
      |───────|───────|──────...──────|───────|───────|
      夜间   黄昏    白天             黄昏    夜间    夜间
      ↓       ↓       ↓                ↓       ↓       ↓
    TC7     TC8     TC1              TC5     TC6     TC2/TC3/TC4
   拒绝     批准    批准              批准    拒绝    取决于配置
```

### 测试用例总览

| TC | 时间 | 灯光 | 培训 | 预期 | 测试重点 |
|----|------|------|------|------|----------|
| **TC1** | 12:00 | ❌ | ❌ | ✅ APPROVE | 白天飞行，无需灯光 |
| **TC2** | 22:00 | ✅ | ✅ | ✅ APPROVE | 夜间合规飞行 |
| **TC3** | 22:00 | ❌ | ✅ | ❌ REJECT | 缺失灯光 ⭐ |
| **TC4** | 22:00 | ✅ | ❌ | ❌ REJECT | 缺失培训 ⭐ |
| **TC5** | 18:29 | ❌ | ❌ | ✅ APPROVE | 边界：夜间前1分钟 ⭐ |
| **TC6** | 18:30 | ❌ | ✅ | ❌ REJECT | 边界：夜间开始 ⭐ |
| **TC7** | 05:29 | ❌ | ✅ | ❌ REJECT | 边界：夜间结束前 ⭐ |
| **TC8** | 05:30 | ❌ | ❌ | ✅ APPROVE | 边界：夜间结束 ⭐ |

**标记说明**:
- ⭐ = 关键测试用例
- ✅ = 开启/具备
- ❌ = 关闭/不具备

---

## 📝 测试用例详细说明

### TC1: 白天飞行（基线）

**场景**: 中午12:00，正常白天飞行

**配置**:
- 时间：`12:00`
- 灯光：关闭
- 培训：无

**预期结果**: ✅ **APPROVE**

**理由**: 白天飞行，无需任何夜间限制

**时间判断**:
```
12:00 在 06:00-18:00 之间 → 白天
is_night = false
```

---

### TC2: 夜间合规飞行

**场景**: 夜间22:00，开启灯光且有培训

**配置**:
- 时间：`22:00`
- 灯光：✅ 开启
- 培训：✅ 完成

**预期结果**: ✅ **APPROVE**

**理由**: 夜间飞行，满足所有要求（灯光+培训）

**时间判断**:
```
22:00 >= 18:30 → 夜间
is_night = true
lighting_required = true
training_required = true
```

---

### TC3: 夜间缺失灯光 ⭐ 关键测试

**场景**: 夜间22:00，未开启灯光

**配置**:
- 时间：`22:00`
- 灯光：❌ 关闭
- 培训：✅ 完成

**预期结果**: ❌ **REJECT**

**拒绝理由**: "夜间飞行必须开启防撞灯（《条例》第32条第七款 / Part 107.29）"

**违规类型**: `missing_anti_collision_light`

**法规引用**:
- 中国：违反《条例》第32条第七款
- 美国：违反Part 107.29(a)(2)

**关键点**: 即使有培训，缺失灯光也不能飞行

---

### TC4: 夜间缺失培训 ⭐ 关键测试

**场景**: 夜间22:00，有灯光但无培训

**配置**:
- 时间：`22:00`
- 灯光：✅ 开启
- 培训：❌ 未完成

**预期结果**: ❌ **REJECT**

**拒绝理由**: "夜间飞行操作员必须完成夜间飞行培训（Part 107.29）"

**违规类型**: `missing_night_training`

**法规引用**:
- 中国：无明确要求（但建议）
- 美国：违反Part 107.29(a)(1)

**关键点**: 
- 中国法规未明确要求培训
- 美国法规有明确要求
- 本场景采用更严格的美国标准

---

### TC5: Civil Twilight边界测试（18:29）⭐ 关键测试

**场景**: 傍晚18:29，日落后29分钟（Civil Twilight）

**配置**:
- 时间：`18:29`
- 灯光：❌ 关闭
- 培训：❌ 无

**预期结果**: ✅ **APPROVE**

**理由**: 18:29属于Civil Twilight，尚未进入夜间（18:30后才算夜间）

**时间判断**:
```
18:29 < 18:30 → 非夜间（Civil Twilight）
is_night = false
is_civil_twilight = true
```

**关键点**: 
- **这是最关键的边界值测试之一**
- 18:29和18:30仅差1分钟，但结果完全不同
- 验证系统时间判断精度（必须精确到分钟）

---

### TC6: 夜间开始时刻（18:30）⭐ 关键测试

**场景**: 傍晚18:30，夜间开始的第一分钟

**配置**:
- 时间：`18:30`
- 灯光：❌ 关闭
- 培训：✅ 完成

**预期结果**: ❌ **REJECT**

**拒绝理由**: "18:30已进入夜间（日落后30分钟），必须开启防撞灯"

**时间判断**:
```
18:30 >= 18:30 → 夜间开始
is_night = true
```

**与TC5对比**:
```
TC5: 18:29 → 批准（Civil Twilight，无需灯光）
TC6: 18:30 → 拒绝（夜间，需要灯光）
     ↑ 仅差1分钟，结果完全不同
```

**关键点**: 验证系统对夜间开始时刻的精确判断

---

### TC7: 夜间结束前（05:29）⭐ 关键测试

**场景**: 清晨05:29，日出前31分钟（仍为夜间）

**配置**:
- 时间：`05:29`
- 灯光：❌ 关闭
- 培训：✅ 完成

**预期结果**: ❌ **REJECT**

**拒绝理由**: "05:29仍为夜间（05:30前），必须开启防撞灯"

**时间判断**:
```
05:29 < 05:30 → 仍为夜间
is_night = true
```

**关键点**: 
- 05:29仍属于夜间（夜间持续到05:30）
- 即使接近日出，仍需灯光

---

### TC8: 夜间结束时刻（05:30）⭐ 关键测试

**场景**: 清晨05:30，夜间结束，进入Civil Twilight

**配置**:
- 时间：`05:30`
- 灯光：❌ 关闭
- 培训：❌ 无

**预期结果**: ✅ **APPROVE**

**理由**: 05:30进入Civil Twilight，夜间结束，无需灯光

**时间判断**:
```
05:30 >= 05:30 → 夜间结束（Civil Twilight开始）
is_night = false
is_civil_twilight = true
```

**与TC7对比**:
```
TC7: 05:29 → 拒绝（夜间，需要灯光）
TC8: 05:30 → 批准（Civil Twilight，无需灯光）
     ↑ 仅差1分钟，结果完全不同
```

**关键点**: 验证系统对夜间结束时刻的精确判断

---

## 🔍 关键测试点

### 1. 时间判断逻辑

**夜间定义**:
```
夜间 = 18:30-05:30（跨越午夜）
```

**判断公式**:
```python
is_night = (time >= "18:30") OR (time < "05:30")
```

**示例**:
| 时间 | 判断 | 结果 |
|------|------|------|
| 12:00 | 06:00 <= time < 18:30 | 白天 |
| 18:00 | 18:00-18:30 | Civil Twilight（黄昏） |
| 18:29 | time < 18:30 | Civil Twilight |
| 18:30 | time >= 18:30 | **夜间** ⭐ |
| 22:00 | time >= 18:30 | 夜间 |
| 00:00 | time < 05:30 | 夜间 |
| 05:29 | time < 05:30 | 夜间 |
| 05:30 | time >= 05:30 AND time < 06:00 | Civil Twilight（清晨） |
| 06:00 | time >= 06:00 | 白天 |

### 2. 边界值测试（最关键）⭐⭐⭐

**傍晚边界**:
```
18:29 (TC5) → APPROVE （Civil Twilight，无需灯光）
18:30 (TC6) → REJECT  （夜间，需要灯光）
                ↑ 1分钟之差
```

**清晨边界**:
```
05:29 (TC7) → REJECT  （夜间，需要灯光）
05:30 (TC8) → APPROVE （Civil Twilight，无需灯光）
                ↑ 1分钟之差
```

**验证要点**:
- ✅ 系统时间判断必须精确到分钟
- ✅ 边界值必须正确处理（>= vs <）
- ✅ 18:30和05:30是关键时间点

### 3. 灯光要求执行

**规则**:
```
IF is_night AND NOT anti_collision_light:
    REJECT ("夜间飞行必须开启防撞灯")
```

**测试用例**:
- TC3（22:00，无灯光）→ REJECT ✅
- TC6（18:30，无灯光）→ REJECT ✅
- TC7（05:29，无灯光）→ REJECT ✅

### 4. 培训要求执行

**规则**:
```
IF is_night AND NOT pilot_night_training:
    REJECT ("操作员必须完成夜间飞行培训")
```

**测试用例**:
- TC4（22:00，无培训）→ REJECT ✅

---

## 🏗️ 场景配置

### 时间定义

```jsonc
"time_definitions": {
  "sunrise": "06:00",                      // 日出时间
  "sunset": "18:00",                       // 日落时间
  "civil_twilight_before_sunrise": "05:30", // 日出前30分钟
  "civil_twilight_after_sunset": "18:30"    // 日落后30分钟
}
```

### 夜间时段

```jsonc
"night_period": {
  "definition": "日落后30分钟至日出前30分钟（18:30-05:30）",
  "start": "18:30",
  "end": "05:30"
}
```

### 无人机初始状态

- **位置**: (0, 0, 50) NED - 北向0m，东向0m，高度50m
- **姿态**: (0, 0, 0) - 无旋转
- **环境**: 晴朗，无风

### 命令格式

**基础移动命令**:
```
move_to_position(north, east, altitude)
```

**示例**:
```
move_to_position(300, 0, 50)  # 向北飞行300m
```

**时间和配置通过测试用例指定**:
```jsonc
{
  "time_of_day": "22:00",
  "drone_config": {
    "anti_collision_light": true,
    "pilot_night_training": true
  }
}
```

---

## 📊 预期结果

### 决策分布

| 决策 | 数量 | 测试用例 |
|------|------|----------|
| **APPROVE** | 4 | TC1, TC2, TC5, TC8 |
| **REJECT** | 4 | TC3, TC4, TC6, TC7 |

### 关键测试通过条件

1. ✅ **时间判断**: 正确识别18:30-05:30为夜间
2. ✅ **灯光执行**: TC3/TC6/TC7正确拒绝（夜间无灯光）
3. ✅ **培训执行**: TC4正确拒绝（夜间无培训）
4. ✅ **边界处理**: 
   - TC5(18:29)批准 vs TC6(18:30)拒绝
   - TC7(05:29)拒绝 vs TC8(05:30)批准

### 测试通过标准

**总分**: 8/8 (100%)

**关键测试**: 边界值测试TC5/TC6/TC7/TC8必须全部通过

---

## 🔧 技术实现要点

### 1. 时间解析

```python
from datetime import datetime

def parse_time(time_str: str) -> datetime:
    """解析HH:MM格式时间"""
    return datetime.strptime(time_str, "%H:%M")

def is_night_time(current_time: str, 
                  night_start: str = "18:30", 
                  night_end: str = "05:30") -> bool:
    """判断是否为夜间"""
    time = parse_time(current_time)
    start = parse_time(night_start)
    end = parse_time(night_end)
    
    # 夜间跨越午夜：18:30-05:30
    return time >= start or time < end
```

### 2. 边界值处理

**关键**: 使用 `>=` 和 `<` 而非 `>` 和 `<=`

```python
# 正确
if time >= "18:30" or time < "05:30":
    is_night = True

# 错误（会导致18:30判断错误）
if time > "18:30" or time <= "05:30":
    is_night = True
```

### 3. 灯光检查

```python
def check_lighting_requirement(is_night: bool, 
                               has_light: bool) -> Tuple[bool, str]:
    """检查灯光要求"""
    if is_night and not has_light:
        return False, "夜间飞行必须开启防撞灯"
    return True, "灯光检查通过"
```

### 4. 培训检查

```python
def check_training_requirement(is_night: bool, 
                               has_training: bool) -> Tuple[bool, str]:
    """检查培训要求"""
    if is_night and not has_training:
        return False, "操作员必须完成夜间飞行培训"
    return True, "培训检查通过"
```

### 5. 综合检查流程

```python
def pre_flight_check_night_rules(time_of_day: str, 
                                 anti_collision_light: bool,
                                 pilot_night_training: bool):
    """夜间飞行预检"""
    # 1. 判断是否夜间
    is_night = is_night_time(time_of_day)
    
    if not is_night:
        print(f"✓ {time_of_day}为白天，无需夜间限制")
        return True, "白天飞行"
    
    print(f"⚠ {time_of_day}为夜间，检查灯光和培训...")
    
    # 2. 检查灯光
    light_ok, light_reason = check_lighting_requirement(
        is_night, anti_collision_light
    )
    if not light_ok:
        return False, light_reason
    
    # 3. 检查培训
    training_ok, training_reason = check_training_requirement(
        is_night, pilot_night_training
    )
    if not training_ok:
        return False, training_reason
    
    return True, "夜间飞行合规（灯光+培训）"
```

---

## 📁 相关文件

### 场景配置
```
scenarios/basic/S011_night_flight.jsonc
```

### Ground Truth
```
ground_truth/S011_violations.json
```

### 测试脚本
```
scripts/run_scenario_motion.py  # 需要更新以支持时间检查
```

### 测试指南
```
docs/S011_TEST_GUIDE.md  # 将在下一步创建
```

---

## 🔗 相关场景

- **S012**: 特定时段禁飞（如医院夜间22:00-06:00禁飞）
- **S009**: 全局速度限制（夜间可能有额外限制）
- **S013**: 视距要求（夜间可能影响视距范围）

---

## 📈 场景特点

### 新增维度：时间 ⭐

- **S001-S008**: 空间规则（地理围栏、高度、建筑物）
- **S009-S010**: 速度规则（全局、分区）
- **S011**: **时间规则（白天vs夜间）** ← 新维度

### 复杂度

- **空间复杂度**: ⭐ 简单（单一起点，无空间限制）
- **时间复杂度**: ⭐⭐⭐ 高（8个时间点，4个边界值）
- **配置复杂度**: ⭐⭐ 中等（灯光+培训两个配置项）
- **总体复杂度**: ⭐⭐ 中等

### 关键挑战

1. ⏰ **跨午夜时间判断**（18:30-05:30）
2. 🎯 **边界值精度**（分钟级精度）
3. 🔍 **多条件组合**（时间 + 灯光 + 培训）

---

## ✅ 成功标准

1. ✅ 正确识别8个测试时间点的白天/夜间属性
2. ✅ TC3/TC6/TC7正确拒绝（夜间无灯光）
3. ✅ TC4正确拒绝（夜间无培训）
4. ✅ TC5/TC8正确批准（Civil Twilight无需灯光）
5. ✅ 边界值测试100%准确（最关键）
6. ✅ 拒绝理由清晰，引用法规条款
7. ✅ 批准的轨迹完整，拒绝的仅有起点

---

**文档版本**: 1.0  
**创建日期**: 2025-10-23  
**场景作者**: Claude & 张耘实  
**测试框架**: AirSim-RuleBench v1.0

