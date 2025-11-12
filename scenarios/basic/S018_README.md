# S018: 多无人机协同飞行限制

## 📋 场景概述

**场景ID**: S018_MultiDroneCoordination  
**难度等级**: ⭐⭐⭐  
**场景类型**: 多机协同规则验证  
**版本**: 1.0  
**创建日期**: 2025-10-31

### 核心测试目标

验证无人机系统对**多机协同飞行规则**的合规性检查能力，包括：
1. **单操作员限制**：一名操作员同时只能控制一架无人机（美国Part 107.35）
2. **最小间隔距离**：不同无人机之间必须保持50米安全距离
3. **集群飞行审批**：3架及以上无人机编队飞行需提前申请审批（中国《条例》第31条第二款第五项）
4. **顺序操作豁免**：单操作员可顺序（非同时）操作多架无人机
5. **集群审批豁免**：已获集群审批可豁免单操作员限制

---

## 🎯 规则定义

### R018: 多无人机协同飞行规则

| 参数 | 值 | 说明 |
|-----|---|------|
| `max_drones_per_operator` | 1 | 单操作员最多同时控制的无人机数量 |
| `min_separation_distance` | 50.0m | 无人机之间的最小安全距离 |
| `swarm_threshold` | 3 | 达到此数量视为集群飞行 |
| `swarm_requires_approval` | true | 集群飞行需要提前审批 |

### 法规依据

1. **美国 Part 107.35** - 单操作员限制
   > "A person may not operate or act as a remote pilot in command or visual observer in the operation of more than one unmanned aircraft at the same time."

2. **中国《条例》第31条第二款第五项** - 集群飞行审批
   > "组织下列飞行活动，应当按照国家有关规定提出飞行活动申请：...（五）分布式操作或者集群飞行"

### 豁免条款

1. **顺序操作豁免**：单操作员可以先操作Drone1完成任务，再操作Drone2，不违反规则
2. **集群审批豁免**：已获得集群飞行审批后，可豁免单操作员限制

---

## 🧪 测试用例

### TC1: 单操作员单无人机 ✅

**测试目标**: 验证基础场景的合规性

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1 |
| 操作员 | OP001 |
| 目标位置 | (500, 0, 50) |
| 预期结果 | ✅ **APPROVE** |
| 预期原因 | 符合基本规则：单操作员单无人机 |

**验证点**:
- ✅ 操作员限制检查通过（1 ≤ 1）

---

### TC2: 单操作员多无人机 🚫

**测试目标**: 验证单操作员限制的强制执行

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone2 |
| 操作员 | OP001（同一人） |
| 目标位置 | Drone1→(500,0,50), Drone2→(500,100,50) |
| 预期结果 | 🚫 **REJECT** |
| 预期原因 | 违反美国Part 107.35：单操作员不能同时控制2架无人机 |

**验证点**:
- ❌ 操作员限制检查失败（2 > 1）
- 法规：Part 107.35

---

### TC3: 多操作员分别控制 ✅

**测试目标**: 验证多操作员场景的合规性

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone3 |
| 操作员 | OP001（Drone1）, OP002（Drone3） |
| 初始间隔 | 200m（East方向） |
| 目标位置 | Drone1→(500,0,50), Drone3→(500,200,50) |
| 预期结果 | ✅ **APPROVE** |
| 预期原因 | 不同操作员分别控制，初始间隔200m > 最小距离50m |

**验证点**:
- ✅ 操作员限制检查通过（每人控制1架）
- ✅ 间隔距离检查通过（200m > 50m）

---

### TC4: 间隔距离不足 🚫

**测试目标**: 验证最小安全距离的强制执行

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone3 |
| 操作员 | OP001, OP002 |
| 目标位置 | Drone1→(500,0,50), Drone3→(500,30,50) |
| 实际间隔 | 30m |
| 预期结果 | 🚫 **REJECT** |
| 预期原因 | 目标位置两机间隔30m < 最小安全距离50m，存在碰撞风险 |

**验证点**:
- ❌ 间隔距离检查失败（30m < 50m）
- 赤字：20m

---

### TC5: 集群飞行未审批 🚫

**测试目标**: 验证集群飞行审批要求

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone2, Drone3（3架） |
| 集群模式 | true |
| 审批状态 | false（未审批） |
| 目标位置 | 编队飞行（间隔10-20m） |
| 预期结果 | 🚫 **REJECT** |
| 预期原因 | 3架无人机编队飞行（集群），需提前申请审批（《条例》第31条第二款第五项） |

**验证点**:
- ❌ 集群审批检查失败（3架 ≥ 阈值3，但无审批）
- 法规：中国《条例》第31条第二款第五项

---

### TC6: 集群飞行已审批 ✅

**测试目标**: 验证集群审批的豁免机制

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone2, Drone3（3架） |
| 集群模式 | true |
| 审批状态 | true（已审批） |
| 目标位置 | 编队飞行（间隔10-20m） |
| 预期结果 | ✅ **APPROVE** |
| 预期原因 | 已获得集群飞行审批，3机协同编队飞行合规 |

**验证点**:
- ✅ 集群审批检查通过
- ✅ 单操作员限制被豁免（因为有集群审批）

---

### TC7: 顺序操作 ✅

**测试目标**: 验证顺序操作的豁免机制

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone2 |
| 操作员 | OP001（同一人） |
| 操作模式 | 顺序：Drone1完成后再启动Drone2 |
| 目标位置 | Drone1→(300,0,50), Drone2→(300,100,50) |
| 预期结果 | ✅ **APPROVE** |
| 预期原因 | 顺序操作：Drone1完成后再启动Drone2，符合单操作员规则 |

**验证点**:
- ✅ 操作员限制检查通过（任何时刻只有1架在飞）
- 豁免原因：sequential_operation

---

### TC8: 边界间隔测试 ✅

**测试目标**: 验证50米边界值的精确处理

| 属性 | 值 |
|-----|---|
| 活跃无人机 | Drone1, Drone3 |
| 操作员 | OP001, OP002 |
| 目标位置 | Drone1→(500,0,50), Drone3→(500,50,50) |
| 实际间隔 | 恰好50.0m |
| 预期结果 | ✅ **APPROVE** |
| 预期原因 | 目标位置间隔恰好50m，满足最小安全距离要求（50 ≥ 50） |

**验证点**:
- ✅ 边界值检查通过（50.0 ≥ 50.0）
- 使用闭区间判断（`>=`）

---

## 📊 测试覆盖矩阵

| 规则维度 | 测试用例 | 通过 | 拒绝 | 覆盖率 |
|---------|---------|------|------|-------|
| **操作员限制** | TC1, TC2, TC7 | 2 | 1 | 100% |
| **间隔距离** | TC3, TC4, TC8 | 2 | 1 | 100% |
| **集群审批** | TC5, TC6 | 1 | 1 | 100% |
| **豁免机制** | TC6, TC7 | 2 | 0 | 100% |

**总计**: 8个测试用例，预期5个APPROVE，3个REJECT

---

## 🔧 技术实现要点

### 1. 多无人机场景配置

```jsonc
"actors": [
  {
    "name": "Drone1",
    "origin": {"xyz": "0.0 0.0 -50.0"},
    "metadata": {
      "operator_id": "OP001"
    }
  },
  {
    "name": "Drone2",
    "origin": {"xyz": "0.0 100.0 -50.0"},
    "metadata": {
      "operator_id": "OP001"  // 同操作员
    }
  },
  {
    "name": "Drone3",
    "origin": {"xyz": "0.0 200.0 -50.0"},
    "metadata": {
      "operator_id": "OP002"  // 不同操作员
    }
  }
]
```

### 2. 操作员检测逻辑

```python
def check_operator_limit(active_drones: List[Dict]) -> bool:
    """检查单操作员限制"""
    operator_drone_count = {}
    for drone in active_drones:
        op_id = drone['operator_id']
        operator_drone_count[op_id] = operator_drone_count.get(op_id, 0) + 1
    
    for op_id, count in operator_drone_count.items():
        if count > max_drones_per_operator:
            return False  # 违规
    return True  # 合规
```

### 3. 间隔距离计算

```python
def calculate_separation(pos1: Dict, pos2: Dict) -> float:
    """计算两架无人机之间的3D欧氏距离"""
    return math.sqrt(
        (pos1['north'] - pos2['north'])**2 +
        (pos1['east'] - pos2['east'])**2 +
        (pos1['altitude'] - pos2['altitude'])**2
    )

def check_minimum_separation(drones: List[Dict], min_sep: float) -> bool:
    """检查所有无人机对之间的距离"""
    for i in range(len(drones)):
        for j in range(i+1, len(drones)):
            distance = calculate_separation(drones[i]['position'], drones[j]['position'])
            if distance < min_sep:
                return False  # 间隔不足
    return True  # 所有间隔都足够
```

### 4. 集群飞行检测

```python
def check_swarm_approval(active_count: int, swarm_mode: bool, has_approval: bool) -> bool:
    """检查集群飞行审批"""
    if active_count >= swarm_threshold and swarm_mode:
        if not has_approval:
            return False  # 需要审批但未获得
    return True  # 通过
```

### 5. 顺序操作模拟

```python
async def execute_sequential(drone1: Drone, drone2: Drone):
    """顺序操作：先执行drone1，完成后再执行drone2"""
    # 阶段1: 只有drone1飞行
    await drone1.move_to_position_async(...)
    await wait_until_reached(drone1, target1)
    
    # 阶段2: drone1完成，drone2开始
    await drone2.move_to_position_async(...)
    await wait_until_reached(drone2, target2)
```

---

## 📈 预期结果分析

### 决策分布

```
✅ APPROVE: 5/8 (62.5%)
  - TC1: 单操作员单机
  - TC3: 多操作员合规间隔
  - TC6: 集群已审批
  - TC7: 顺序操作
  - TC8: 边界间隔

🚫 REJECT: 3/8 (37.5%)
  - TC2: 单操作员多机
  - TC4: 间隔不足
  - TC5: 集群未审批
```

### 关键边界值

| 边界 | 测试用例 | 阈值 | 测试值 | 结果 |
|-----|---------|------|-------|------|
| 操作员限制 | TC1, TC2 | 1架 | 1架, 2架 | PASS, FAIL |
| 间隔距离 | TC8 | 50m | 50.0m | PASS (≥) |
| 集群阈值 | TC5, TC6 | 3架 | 3架 | 触发检查 |

---

## 🎓 学习要点

### 1. 多机协同的复杂性

多无人机场景远比单机复杂：
- **O(n²)** 复杂度的间隔检查
- 操作员与无人机的多对多映射
- 同时/顺序操作的时序逻辑

### 2. 法规的层次性

```
优先级: 安全距离 > 操作员限制 > 审批要求

豁免机制:
- 集群审批可豁免操作员限制
- 顺序操作可豁免操作员限制
```

### 3. 边界值的重要性

- TC8验证了`50.0 >= 50.0 → PASS`
- 必须使用`>=`而非`>`，符合工程实践

### 4. 实际应用场景

- **物流配送**：多无人机需要协同但保持间隔
- **编队表演**：需要集群审批和专业控制
- **农业作业**：单操作员顺序操作多架
- **应急救援**：多团队协同需要严格管制

---

## 🚀 后续扩展方向

1. **动态间隔监控**：In-flight阶段持续监控无人机间距
2. **编队保持算法**：测试集群飞行的队形维持
3. **操作员切换**：测试无人机控制权交接
4. **通信链路**：模拟无人机间通信延迟
5. **4D航迹冲突**：时空四维的轨迹碰撞检测

---

**场景状态**: ✅ 设计完成，待实现  
**预计开发时间**: 8-10小时  
**难度评估**: ⭐⭐⭐（需要多无人机同步控制）

