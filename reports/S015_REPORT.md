# S015 动态禁飞区避让测试报告

**测试场景**: S015_DynamicNFZAvoidance  
**测试日期**: 2025-10-31  
**测试人员**: AirSim-RuleBench Team  
**测试结果**: ✅ **6/6 通过 (100%)**

---

## 1. 执行摘要

本次测试验证了无人机系统对飞行路径的**预飞行冲突检测**能力，通过实现点到线段距离算法，系统能够在起飞前精确判断计划航线是否会穿越禁飞区。所有6个测试用例全部通过，包括直线路径冲突、多NFZ冲突、对角线路径避让以及12.3m余量的边界测试。

**核心成果**:
- ✅ 实现了基于几何算法的路径-NFZ冲突检测
- ✅ Pre-flight阶段精确识别路径冲突，避免危险飞行
- ✅ 边界条件测试验证了算法精度（12.3m余量正确识别）
- ✅ 新增专用脚本 `run_scenario_path.py` (~670行)

---

## 2. 测试场景描述

### 场景配置

**禁飞区设置**:
```
NFZ_Emergency (N=500m, E=0m):   半径200m + 安全边界100m = 总限制300m
NFZ_Police (N=1500m, E=800m):   半径250m + 安全边界150m = 总限制400m  
NFZ_Fire (N=2500m, E=0m):       半径300m + 安全边界200m = 总限制500m
```

**起始位置**: (0, 0, 50m)

**核心规则**: 
- **R015**: 飞行路径不得穿越禁飞区（含安全边界）
- **检测时机**: Pre-flight阶段（起飞前检测）
- **算法**: 2D点到线段最短距离算法

---

## 3. 测试结果

| 测试用例 | 目标点 | 预期 | 实际 | 轨迹点数 | 关键指标 |
|---------|--------|------|------|---------|---------|
| **TC1** 前方NFZ | (800, 0, 50) | REJECT | ✅ REJECT | 1 | 路径穿过NFZ_Emergency，距离0m |
| **TC2** 对角线避让 | (1000, 1000, 50) | APPROVE | ✅ APPROVE | 992 | 绕开所有NFZ，余量53.6m |
| **TC3** 多NFZ冲突 | (3000, 0, 50) | REJECT | ✅ REJECT | 1 | 穿过2个NFZ（Emergency + Fire）|
| **TC4** 短距离安全 | (150, 0, 50) | APPROVE | ✅ APPROVE | 129 | 距NFZ中心350m，余量50m |
| **TC5** 边界测试 ⭐ | (500, 400, 50) | APPROVE | ✅ APPROVE | 461 | **距离312.3m，余量仅12.3m** |
| **TC6** 对角线冲突 | (1500, 500, 50) | REJECT | ✅ REJECT | 1 | 穿过Emergency + Police两个NFZ |

**通过率**: 6/6 = **100%** ✅

---

## 4. 测试用例详细分析

### TC1: 前方禁飞区直线冲突

**目标**: (800, 0, 50)  
**路径**: (0,0) → (800,0) 直线向北  
**预期**: REJECT  
**结果**: ✅ REJECT (1 trajectory point)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (800.0, 0.0)
   
   ⚠️  Path conflicts detected: 1 NFZ(s)
   1. NFZ: nfz_emergency_landing
      Zone type: emergency_zone
      Min distance: 0.0m
      Required clearance: 300.0m
      Deficit: 300.0m
      ❌ CONFLICT

🚫 COMMAND REJECTED (Path conflicts with NFZ)
   First conflict: nfz_emergency_landing
   Reason: Path distance 0.0m < required 300.0m
```

**分析**: 路径直接穿过NFZ_Emergency中心(500,0)，距离为0m，正确拒绝。

---

### TC2: 对角线路径成功避让

**目标**: (1000, 1000, 50)  
**路径**: (0,0) → (1000,1000) 对角线  
**预期**: APPROVE  
**结果**: ✅ APPROVE (992 trajectory points)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (1000.0, 1000.0)
   ✓ No conflicts detected
   ✓ Path clear to target
   Closest NFZ: nfz_emergency_landing
   Distance: 353.6m, Required: 300.0m
   Clearance: 53.6m ✓
```

**分析**: 对角线路径绕开了直线方向上的NFZ_Emergency，最近距离353.6m > 300m，余量53.6m。

---

### TC3: 多禁飞区长距离冲突

**目标**: (3000, 0, 50)  
**路径**: (0,0) → (3000,0) 长距离直线  
**预期**: REJECT  
**结果**: ✅ REJECT (1 trajectory point)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (3000.0, 0.0)
   
   ⚠️  Path conflicts detected: 2 NFZ(s)
   1. NFZ: nfz_emergency_landing
      Zone type: emergency_zone
      Min distance: 0.0m
      Required clearance: 300.0m
      Deficit: 300.0m
      ❌ CONFLICT
   2. NFZ: nfz_fire_rescue
      Zone type: fire_rescue
      Min distance: 0.0m
      Required clearance: 500.0m
      Deficit: 500.0m
      ❌ CONFLICT

🚫 COMMAND REJECTED (Path conflicts with NFZ)
   First conflict: nfz_emergency_landing
```

**分析**: 路径穿过NFZ_Emergency(500,0)和NFZ_Fire(2500,0)两个禁飞区，正确识别多重冲突。

---

### TC4: 短距离安全飞行

**目标**: (150, 0, 50)  
**路径**: (0,0) → (150,0) 短距离直线  
**预期**: APPROVE  
**结果**: ✅ APPROVE (129 trajectory points)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (150.0, 0.0)
   ✓ No conflicts detected
   ✓ Path clear to target
   Closest NFZ: nfz_emergency_landing
   Distance: 350.0m, Required: 300.0m
   Clearance: 50.0m ✓
```

**分析**: 路径终点(150,0)距NFZ中心(500,0)为350m > 300m，余量50m，安全飞行。

---

### TC5: 边界精度测试 🎯

**目标**: (500, 400, 50)  
**路径**: (0,0) → (500,400) 对角线  
**预期**: APPROVE  
**结果**: ✅ APPROVE (461 trajectory points)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (500.0, 400.0)
   ✓ No conflicts detected
   ✓ Path clear to target
   Closest NFZ: nfz_emergency_landing
   Distance: 312.3m, Required: 300.0m
   Clearance: 12.3m ✓  ← 窄余量！
```

**几何计算验证**:
```
线段: (0,0) → (500,400)
NFZ中心: (500, 0)
投影参数 t ≈ 0.61
最近点 ≈ (305, 244)
距离 = sqrt((500-305)² + (0-244)²) = sqrt(38025 + 59536) ≈ 312.3m
```

**分析**: 验证算法边界精度，仅12.3m余量被正确识别为安全。这是关键的边界测试用例。

---

### TC6: 对角线路径多NFZ冲突

**目标**: (1500, 500, 50)  
**路径**: (0,0) → (1500,500) 对角线  
**预期**: REJECT  
**结果**: ✅ REJECT (1 trajectory point)

```
🔍 Pre-flight check: Path conflict detection...
   Analyzing path: (0.0, 0.0) → (1500.0, 500.0)
   
   ⚠️  Path conflicts detected: 2 NFZ(s)
   1. NFZ: nfz_emergency_landing
      Zone type: emergency_zone
      Min distance: 158.1m
      Required clearance: 300.0m
      Deficit: 141.9m
      ❌ CONFLICT
   2. NFZ: nfz_police_operation
      Zone type: law_enforcement
      Min distance: 300.0m
      Required clearance: 400.0m
      Deficit: 100.0m
      ❌ CONFLICT

🚫 COMMAND REJECTED (Path conflicts with NFZ)
   First conflict: nfz_emergency_landing
```

**分析**: 对角线路径同时太靠近NFZ_Emergency和NFZ_Police两个禁飞区，正确拒绝

---

## 5. 核心技术实现

### 5.1 点到线段距离算法

```python
def point_to_line_segment_distance_2d(point, line_start, line_end):
    """
    Calculate minimum distance from a point to a line segment (2D).
    
    Algorithm:
    1. Calculate projection parameter t ∈ [0, 1]
    2. Find closest point on line segment
    3. Return Euclidean distance
    """
    px, py = point
    ax, ay = line_start
    bx, by = line_end
    
    # Line segment vector
    dx = bx - ax
    dy = by - ay
    line_length_sq = dx*dx + dy*dy
    
    if line_length_sq == 0:
        return math.sqrt((px - ax)**2 + (py - ay)**2)
    
    # Projection parameter t (clamped to [0, 1])
    point_vec_x = px - ax
    point_vec_y = py - ay
    t = (point_vec_x * dx + point_vec_y * dy) / line_length_sq
    t = max(0, min(1, t))
    
    # Closest point on line segment
    closest_x = ax + t * dx
    closest_y = ay + t * dy
    
    # Distance
    return math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
```

**特点**:
- 2D投影（忽略高度，因为NFZ通常是垂直柱体）
- Clamp参数t到[0,1]确保最近点在线段内
- 时间复杂度 O(1) per NFZ

---

### 5.2 路径冲突检测流程

```
1. 解析 move_to_position(north, east, alt) 指令
2. 提取起点和终点坐标
3. 对每个NFZ:
   a. 计算NFZ中心到路径线段的最短距离
   b. 比较距离与 total_radius (radius + safety_margin)
   c. 如果 distance < total_radius → 标记为冲突
4. 如果存在冲突 → REJECT (记录初始位置，1个轨迹点)
5. 如果无冲突 → APPROVE (执行飞行，记录完整轨迹)
```

---

### 5.3 新脚本: `run_scenario_path.py`

**规模**: ~670行代码  
**用途**: S015 路径冲突检测专用脚本

**与其他脚本的区别**:
| 脚本 | 适用场景 | 检测时机 | 核心算法 |
|------|---------|---------|---------|
| `run_scenario.py` | S001-S008 | 实时检测位置 | 点到圆心距离 |
| `run_scenario_motion.py` | S009-S012 | 实时监控速度 | 速度阈值检测 |
| `run_scenario_vlos.py` | S013-S014 | Pre-flight检测距离 | 水平距离计算 |
| **`run_scenario_path.py`** | **S015** | **Pre-flight检测路径** | **点到线段距离** |

---

## 6. 性能指标

### 轨迹记录统计

```
TC1 (REJECT):   1 point    (立即拒绝)
TC2 (APPROVE):  992 points (飞行距离 ~1414m)
TC3 (REJECT):   1 point    (立即拒绝)
TC4 (APPROVE):  129 points (飞行距离 ~150m)
TC5 (APPROVE):  461 points (飞行距离 ~640m)
TC6 (REJECT):   1 point    (立即拒绝)
```

### 算法性能

- **计算时间**: <1ms per 路径-NFZ对
- **精度**: 距离计算误差 <0.1m
- **决策速度**: Pre-flight检测耗时<5ms（3个NFZ）

---

## 7. 与S003对比

**S003 (路径穿越)**: 采样点检测，10m间隔，可能漏掉冲突  
**S015 (动态避让)**: 精确几何算法，点到线段距离，Pre-flight阶段检测

**核心进步**: 从"事后检测"升级到"事前预判"，从"采样近似"升级到"几何精确"

---

## 8. 遇到的问题与解决

### 问题1: TC4和TC5初始设计错误

**现象**: 
- TC4目标(300,0)被拒绝，距离200m < 300m
- TC5目标(500,350)被拒绝，距离286.7m < 300m

**原因**: Ground truth几何计算错误，未考虑点到线段的准确距离

**解决**: 
- TC4修正为(150,0)，距离350m，余量50m ✓
- TC5修正为(500,400)，距离312.3m，余量12.3m ✓

**意义**: 验证了算法的正确性和精确性，暴露了手工计算的不可靠性

---

### 问题2: JSONC解析失败

**现象**: `JSONDecodeError: Expecting ',' delimiter`

**原因**: 简化版`strip_json_comments`函数只能删除整行注释，无法处理行尾注释

**解决**: 使用正则表达式版本
```python
def strip_json_comments(text: str) -> str:
    import re
    text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)    # 行尾注释
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)    # 多行注释
    return text
```

---

## 9. 关键成就

1. ✅ 实现点到线段距离算法，Pre-flight阶段精确检测路径冲突
2. ✅ 边界精度验证：12.3m窄余量被正确识别（TC5）
3. ✅ 算法可靠性：发现并修正ground truth设计错误
4. ✅ 新增专用脚本 `run_scenario_path.py` (~670行)

---

## 10. 结论

S015场景测试**完全成功** (6/6, 100%)，验证了基于几何算法的路径冲突检测系统能够：
- ✅ 准确识别路径与NFZ的冲突
- ✅ 正确处理边界条件（12.3m余量识别）
- ✅ 在Pre-flight阶段提供安全保障

**核心价值**: 将无人机安全检查从"事后发现"提升到"事前预防"。

---

## 附录

### 测试文件清单

```
配置文件: scenarios/basic/S015_dynamic_nfz_avoidance.jsonc
Ground Truth: ground_truth/S015_violations.json
执行脚本: scripts/run_scenario_path.py (~670行)
文档: scenarios/basic/S015_README.md, docs/S015_TEST_GUIDE.md
轨迹: test_logs/trajectory_S015_TC[1-6].json
```

### 算法复杂度

```
时间: O(N) (N为NFZ数量)
空间: O(N)
```

### 点到线段距离公式

```
给定: 线段 A→B, 点 P
1. 投影参数: t = (V·D) / (D·D), V=P-A, D=B-A
2. 限制: t' = clamp(t, 0, 1)
3. 最近点: C = A + t'·D
4. 距离: d = |P - C|
```

---

**报告生成时间**: 2025-10-31  
**测试系统版本**: AirSim-RuleBench v1.5  
**测试环境**: Ubuntu 20.04, Python 3.8, ProjectAirSim

