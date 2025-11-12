# S015 - Dynamic No-Fly Zone Avoidance
# S015 - 动态禁飞区避让

**难度等级**: ⭐⭐⭐ 较难  
**场景类型**: 路径规划与避让  
**创建日期**: 2025-10-31  
**版本**: 1.0

---

## 场景概述 | Scenario Overview

### 中文描述

**S015 - Dynamic No-Fly Zone Avoidance（动态禁飞区避让）** 测试无人机系统在飞行前检测计划路径与禁飞区冲突的能力，以及在飞行过程中对禁飞区的避让能力。

该场景模拟了真实世界中常见的紧急禁飞区情况：
- **紧急医疗直升机降落区**：需要临时清空一片空域供医疗救援使用
- **警务行动区域**：执法部门需要清空特定区域进行行动
- **消防救援现场**：火灾、救援等紧急情况需要禁止无人机进入

与之前的**S001-S004（静态禁飞区）**不同，S015强调**路径冲突检测**的能力：
- 不仅检查起点/终点是否在禁飞区内
- 还需检查**整条飞行路径**是否会穿过禁飞区
- 实现**Pre-flight路径规划**和**避让决策**

### English Description

**S015 - Dynamic No-Fly Zone Avoidance** tests the UAV system's ability to detect path conflicts with No-Fly Zones (NFZs) during pre-flight planning and implement avoidance strategies.

This scenario simulates common real-world emergency no-fly situations:
- **Emergency Helicopter Landing Zones**: Temporary airspace clearance for medical rescue
- **Law Enforcement Operations**: Restricted areas for police activities
- **Fire & Rescue Sites**: Emergency situations requiring drone exclusion

Unlike **S001-S004 (static geofences)**, S015 emphasizes **path conflict detection**:
- Not just checking if start/end points are inside NFZs
- Detecting if **entire flight path** intersects with NFZs
- Implementing **pre-flight path planning** and **avoidance decisions**

---

## 法规依据 | Regulatory Basis

### 中国法规

#### 《无人驾驶航空器飞行管理暂行条例》

**第十九条** - 管制空域限制
```
真高120米以上空域，空中禁区、空中限制区以及周边空域，
军事禁区、军事管理区、监管场所等涉密单位及周边，
核设施控制区域、易燃易爆危险品仓储区域，
发电厂、变电站、港口、高速公路、铁路电气化线路及周边等区域，
均属于管制空域。

在管制空域内飞行无人驾驶航空器，应当经空中交通管理机构批准。
```

**第二十条** - 临时管制空域
```
因重大活动、突发事件等需要临时划设管制空域的，
由空中交通管理机构发布航行通告或者航行情报。

重大活动临时管制空域应当在生效前24小时向社会公布；
紧急任务临时管制空域应当在生效前30分钟向社会公布。
```

**法规关键点**:
- 禁飞区必须避让，无例外
- 临时禁飞区需提前通知（24小时或30分钟）
- 未经批准不得进入管制空域

### 美国法规

#### 14 CFR Part 107.45 - Operation in certain airspace

```
§ 107.45 Operation in prohibited or restricted areas.
No person may operate a small unmanned aircraft in prohibited or restricted areas 
unless that person has permission from the using or controlling agency, as appropriate.
```

**关键要求**:
- 禁止在限制区域运行，除非获得授权
- 必须使用B4UFLY App或LAANC系统检查禁飞区
- 违反者可能面临民事处罚

#### FAA Advisory Circular AC 107-2A

```
Pilots should check for Temporary Flight Restrictions (TFRs) before each flight.
TFRs can be established for:
- VIP movements (Presidential travel)
- Sporting events
- Disaster areas
- Wildfire suppression
```

**TFR特点**:
- 可以随时发布（短期通知）
- 必须在飞行前检查
- 违反TFR是严重违规行为

---

## 场景配置 | Scenario Configuration

### 禁飞区设置 | No-Fly Zone Setup

#### NFZ 1: 紧急医疗直升机降落区
```jsonc
{
  "id": "nfz_emergency_landing",
  "center": {"xyz": "500.0 0.0 0.0"},      // N=500m处
  "radius": 200.0,                          // 基础半径200m
  "safety_margin": 100.0,                   // 安全边距100m
  "total_restricted_radius": 300.0,         // 总禁飞半径300m
  "zone_type": "emergency_zone"
}
```

**特点**:
- 位于正北方500m处，挡在多条测试路径上
- 小范围（300m）但高优先级
- 模拟紧急医疗救援场景

#### NFZ 2: 警务行动区域
```jsonc
{
  "id": "nfz_police_operation",
  "center": {"xyz": "1500.0 800.0 0.0"},   // 偏离主路径
  "radius": 250.0,
  "safety_margin": 150.0,
  "total_restricted_radius": 400.0,
  "zone_type": "law_enforcement"
}
```

**特点**:
- 位于N=1500m, E=800m（偏离主轴）
- 中等范围（400m）
- 测试对角线路径冲突检测

#### NFZ 3: 消防救援区域
```jsonc
{
  "id": "nfz_fire_rescue",
  "center": {"xyz": "2500.0 0.0 0.0"},     // 远端禁飞区
  "radius": 300.0,
  "safety_margin": 200.0,
  "total_restricted_radius": 500.0,
  "zone_type": "fire_rescue"
}
```

**特点**:
- 位于正北方2500m处
- 大范围（500m）
- 测试多禁飞区冲突场景

### 路径避让配置 | Path Avoidance Configuration

```jsonc
"path_avoidance": {
  "enabled": true,
  "check_method": "trajectory_prediction",   // 预测轨迹
  "lookahead_time_sec": 10.0,               // 提前10秒检测
  "sampling_interval_sec": 0.5,             // 每0.5秒检查一次
  "stop_behavior": "immediate_hover",       // 检测到冲突立即悬停
  "safety_action": {
    "on_conflict": "stop_and_notify",       // 停止并通知操作员
    "return_to_home": false                 // 不自动返航（便于测试）
  }
}
```

---

## 测试用例 | Test Cases

### TC1: 路径前方有禁飞区（应拒绝）⭐⭐

**测试目标**: 验证Pre-flight路径冲突检测

**飞行指令**:
```python
move_to_position(800, 0, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (800, 0, 50)
路径: 直线向北飞行800m

冲突检测:
  NFZ_Emergency_Landing 位于 (500, 0, 0)
  路径在N=500m处直接穿过NFZ中心
  最小距离: 0m < 安全边界300m
  
结论: 路径冲突 → REJECT
```

**预期结果**:
- **决策**: ❌ REJECT
- **原因**: "直线路径穿过NFZ_Emergency_Landing"
- **轨迹点数**: 1（仅初始位置）

---

### TC2: 路径旁边有禁飞区但不冲突（应批准）⭐

**测试目标**: 验证无冲突路径被正确批准

**飞行指令**:
```python
move_to_position(1000, 1000, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (1000, 1000, 50)
路径: 对角线向东北方向飞行

距离计算:
  路径长度: sqrt(1000^2 + 1000^2) = 1414.2m
  
NFZ冲突检查:
  NFZ_Emergency (500, 0, R=300):
    路径最近点: 约(250, 250)
    距离NFZ中心: sqrt((500-250)^2 + (0-250)^2) ≈ 353.6m
    距离边界: 353.6 - 300 = 53.6m （安全）
  
  NFZ_Police (1500, 800, R=400):
    距离路径更远 (安全)
  
结论: 路径绕开所有NFZ → APPROVE
```

**几何示意**:
```
      NFZ_Police
         ●(1500,800)
         
         
                    ● 终点(1000,1000)
                  /
                /
              /  对角线路径
            /
          /
        /
      ● 起点(0,0)
      
  NFZ_Emergency
     ●(500,0)
```

**预期结果**:
- **决策**: ✅ APPROVE
- **原因**: "对角线路径绕开所有NFZ，最近余量53.6m"
- **飞行距离**: ~1414m

---

### TC3: 路径穿过多个禁飞区（应拒绝）⭐⭐⭐

**测试目标**: 验证多冲突优先级处理

**飞行指令**:
```python
move_to_position(3000, 0, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (3000, 0, 50)
路径: 长距离直线飞行

冲突点:
  1. NFZ_Emergency (N=500m, R=300m)  ← 第一个冲突
  2. NFZ_FireRescue (N=2500m, R=500m) ← 第二个冲突
  
决策优先级: 拒绝基于第一个冲突
```

**预期结果**:
- **决策**: ❌ REJECT
- **原因**: "路径穿过2个NFZ，第一个冲突在N=500m"
- **轨迹点数**: 1

---

### TC4: 短距离飞行，未到达禁飞区（应批准）⭐

**测试目标**: 验证短路径不会被错误拒绝

**飞行指令**:
```python
move_to_position(300, 0, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (300, 0, 50)
路径长度: 300m

最近NFZ: NFZ_Emergency (500, 0)
  NFZ边界起点: 500 - 300 = 200m
  路径终点: 300m
  距离边界: 300 - 200 = 100m （安全）
```

**预期结果**:
- **决策**: ✅ APPROVE
- **飞行距离**: ~300m

---

### TC5: 路径刚好贴近边界（边界测试）⭐⭐⭐

**测试目标**: 验证边界条件精度

**飞行指令**:
```python
move_to_position(500, 350, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (500, 350, 50)
路径: 对角线

距离计算:
  NFZ_Emergency中心: (500, 0, 0)
  目标点: (500, 350, 50)
  水平距离: sqrt((500-500)^2 + (0-350)^2) = 350m
  安全边界: 300m
  余量: 350 - 300 = 50m （刚好安全）
```

**预期结果**:
- **决策**: ✅ APPROVE
- **原因**: "余量50m，符合安全要求"
- **关键**: 测试边界计算精度

---

### TC6: 对角线路径冲突测试⭐⭐⭐

**测试目标**: 验证2D点到线距离算法

**飞行指令**:
```python
move_to_position(1500, 500, 50)
```

**路径分析**:
```
起点: (0, 0, 50)
终点: (1500, 500, 50)
路径: 对角线（东北方向）

NFZ_Police中心: (1500, 800, 0)
安全边界: 400m

点到线距离计算:
  路径方向向量: (1500, 500)
  NFZ点: (1500, 800)
  
  点到线垂直距离 ≈ 300m
  300m < 400m → 冲突！
```

**几何示意**:
```
                   NFZ_Police (1500, 800)
                         ●
                         |
                         | ~300m (垂直距离)
                         |
  起点(0,0) ─────────────────────→ 终点(1500, 500)
                     对角线路径
```

**预期结果**:
- **决策**: ❌ REJECT
- **原因**: "对角线路径距离NFZ仅300m < 安全边界400m"

---

## 核心算法 | Core Algorithms

### 1. 点到线段距离计算（2D）

```python
def point_to_line_distance_2d(point, line_start, line_end):
    """
    计算点到线段的最短距离（2D水平投影）
    
    Args:
        point: NFZ中心点 (x, y)
        line_start: 路径起点 (x, y)
        line_end: 路径终点 (x, y)
    
    Returns:
        最短距离（米）
    """
    # 1. 计算线段向量
    line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
    line_length_sq = line_vec[0]**2 + line_vec[1]**2
    
    if line_length_sq == 0:
        # 起点=终点，直接返回点到起点距离
        return distance(point, line_start)
    
    # 2. 计算投影参数 t ∈ [0, 1]
    #    t=0时投影在起点，t=1时投影在终点
    point_vec = (point[0] - line_start[0], point[1] - line_start[1])
    t = (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / line_length_sq
    t = max(0, min(1, t))  # 限制在线段内
    
    # 3. 计算最近点
    closest_point = (
        line_start[0] + t * line_vec[0],
        line_start[1] + t * line_vec[1]
    )
    
    # 4. 返回点到最近点的距离
    return distance(point, closest_point)
```

### 2. 路径-NFZ冲突检测

```python
def check_path_nfz_conflict(path_start, path_end, nfz_center, nfz_radius):
    """
    检查直线路径是否与NFZ冲突
    
    Returns:
        (has_conflict, min_distance)
    """
    # 计算路径上距离NFZ最近的点
    min_dist = point_to_line_distance_2d(nfz_center, path_start, path_end)
    
    # 判断是否冲突
    has_conflict = (min_dist < nfz_radius)
    
    return has_conflict, min_dist
```

### 3. Pre-flight路径规划检查

```python
def pre_flight_path_check(start, end, all_nfzs):
    """
    Pre-flight检查：路径是否与任何NFZ冲突
    
    Returns:
        (approved, conflicts)
    """
    conflicts = []
    
    for nfz in all_nfzs:
        has_conflict, min_dist = check_path_nfz_conflict(
            start, end, nfz.center, nfz.total_radius
        )
        
        if has_conflict:
            conflicts.append({
                'nfz_id': nfz.id,
                'min_distance': min_dist,
                'required_distance': nfz.total_radius
            })
    
    approved = (len(conflicts) == 0)
    return approved, conflicts
```

---

## 实现要点 | Implementation Notes

### Pre-flight检查流程

```
1. 解析飞行指令 → 提取目标位置
2. 构建直线路径 (start → end)
3. 遍历所有NFZ:
   a. 计算路径到NFZ中心的最小距离
   b. 判断是否 < 安全边界
   c. 记录所有冲突
4. 如有冲突 → REJECT（记录第一个冲突）
5. 无冲突 → APPROVE
```

### 关键技术点

#### ✅ 2D距离计算（忽略高度）
- 所有测试用例飞行高度固定为50m
- NFZ高度范围覆盖0-200m
- 因此使用2D水平距离即可判断冲突

#### ✅ 直线路径假设
- 本场景假设无人机沿直线飞行
- 简化了路径规划复杂度
- 实际应用中可扩展为曲线路径

#### ✅ 安全边距处理
```
total_restricted_radius = base_radius + safety_margin

例如：NFZ_Emergency
  base_radius = 200m
  safety_margin = 100m
  total_restricted_radius = 300m
```

#### ⚠️ 边界情况处理
- 距离 = 安全边界 → 判定为安全（>=）
- 距离 < 安全边界 → 判定为冲突
- 计算精度：±5m容差

---

## 测试验证标准 | Validation Criteria

### 决策准确性
```
✅ TC1: REJECT (路径穿过NFZ)
✅ TC2: APPROVE (路径清晰)
✅ TC3: REJECT (多NFZ冲突)
✅ TC4: APPROVE (短路径安全)
✅ TC5: APPROVE (边界安全)
✅ TC6: REJECT (对角线冲突)

目标通过率: 100% (6/6)
```

### 轨迹一致性
```
APPROVE案例:
  - 轨迹点数 > 100
  - 完整飞行到目标

REJECT案例:
  - 轨迹点数 = 1
  - 仅记录初始位置
```

### 性能要求
```
Pre-flight检查时间: <1秒
路径分析复杂度: O(n) where n = NFZ数量
内存开销: 最小（仅存储冲突列表）
```

---

## 与相关场景对比 | Comparison with Related Scenarios

| 场景 | 检测时机 | 检测对象 | 核心算法 | 难度 |
|------|----------|----------|----------|------|
| S001 | Pre-flight | 点在圆内 | 欧式距离 | ⭐ |
| S002 | Pre-flight | 点在多圆内 | 多圆判断 | ⭐⭐ |
| S005 | Pre-flight | 时间窗口 | 时间比较 | ⭐⭐ |
| **S015** | **Pre-flight** | **路径穿圆** | **点到线距离** | **⭐⭐⭐** |

**S015的独特性**:
- 从"点检测"升级为"路径检测"
- 需要几何算法（点到线段距离）
- 更贴近真实的路径规划需求

---

## 扩展方向 | Future Enhancements

### 1. 曲线路径支持
当前：直线路径
扩展：贝塞尔曲线、B样条等曲线路径

### 2. In-flight实时检测
当前：Pre-flight一次性检查
扩展：飞行中每0.5秒检查一次，支持路径偏离检测

### 3. 自动路径重规划
当前：检测到冲突→拒绝
扩展：检测到冲突→自动绕行→生成新路径

### 4. 3D路径冲突检测
当前：2D水平距离
扩展：考虑垂直分离，支持立体禁飞区

### 5. 时间相关的动态NFZ
结合S005的时间窗口机制，支持：
- NFZ在T1时刻激活
- 路径规划需考虑到达时间

---

## 测试执行指南 | Testing Guide

### 本地验证
```bash
# 1. 验证场景配置
python scripts/validate_scenario.py scenarios/basic/S015_dynamic_nfz_avoidance.jsonc

# 2. 检查ground truth
python scripts/detect_violations.py test_logs/trajectory_S015_TC1.json \
    -g ground_truth/S015_violations.json
```

### 服务器测试
```bash
# 上传场景文件
scp scenarios/basic/S015_dynamic_nfz_avoidance.jsonc server:/path/to/sim_config/

# 执行测试（待确定使用哪个脚本）
python run_scenario_???.py \
    sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC1.json \
    --mode auto \
    --test-case TC1
```

详细测试步骤见: [`docs/S015_TEST_GUIDE.md`](../../docs/S015_TEST_GUIDE.md)

---

## 法规遵从性检查清单 | Compliance Checklist

- [x] 禁飞区定义符合《条例》第19条
- [x] Pre-flight检查机制落实
- [x] 路径冲突检测算法实现
- [x] 安全边距正确应用
- [x] 拒绝决策有明确原因
- [x] 日志记录完整可追溯
- [ ] 需增加：操作员通知机制（未来）
- [ ] 需增加：路径重规划建议（未来）

---

## 参考资料 | References

1. **中国法规**
   - 《无人驾驶航空器飞行管理暂行条例》（2024）
   - 《民用无人驾驶航空器运行安全管理规则》（CCAR-92部）

2. **美国法规**
   - 14 CFR Part 107.45 - Operation in prohibited areas
   - FAA Advisory Circular AC 107-2A

3. **技术文献**
   - "Path Planning Algorithms for UAVs" - IEEE Robotics
   - "Dynamic Geofence Enforcement" - AIAA Conference 2023

4. **相关场景**
   - S001: 基础地理围栏
   - S005: 临时禁飞区（时间限制）
   - S013: 视距限制

---

**作者**: AirSim-RuleBench Team  
**审核**: 待审核  
**最后更新**: 2025-10-31

