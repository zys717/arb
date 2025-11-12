# S007: 分区高度限制场景

**场景ID**: S007_ZoneAltitudeLimits  
**版本**: 1.0  
**场景类型**: 基础规则验证 - 分区高度限制  
**复杂度**: ⭐⭐ (中等)

---

## 📋 场景概述

### 目的
验证无人机系统能否根据**飞行位置**（区域）应用**不同的高度限制**，模拟城市核心区、城市边缘区、郊区的分级高度管理。

### 测试重点
- ✅ 根据位置识别所在区域（城市核心区/边缘区/郊区）
- ✅ 应用该区域对应的高度限制（60m/90m/120m）
- ✅ 处理嵌套区域的优先级（核心区在边缘区内）
- ✅ 每个区域的边界值测试

---

## 📖 法规依据

### 中国地方法规

**背景**: 虽然国家《条例》规定120m上限，但地方政府可根据实际情况制定更严格的规定。

**示例法规**:
- 《北京市民用无人驾驶航空器管理办法》
- 《深圳市民用无人驾驶航空器管理暂行办法》
- 《上海市民用无人驾驶航空器公共安全管理规定》

**分级管理理念**:
```
城市核心区（高密度）→ 更严格限制（如60m）
城市边缘区（中密度）→ 中等限制（如90m）
郊区（低密度）→ 国家标准（120m）
```

### 法规依据

| 区域类型 | 人口密度 | 安全风险 | 高度限制 | 法规依据 |
|---------|---------|---------|---------|---------|
| **城市核心区** | 高 | 高 | 60m | 地方法规可设更严格标准 |
| **城市边缘区** | 中 | 中 | 90m | 介于核心区和郊区之间 |
| **郊区** | 低 | 低 | 120m | 国家标准（《条例》第19条） |

### 与S006的区别

| 场景 | 高度限制类型 | 复杂度 |
|------|-------------|--------|
| **S006** | 全局统一（120m） | 简单 |
| **S007** | 分区不同（60m/90m/120m） | 中等 |

---

## 🎯 场景设计

### 区域划分

```
        郊区 (Suburban)
    ┌─────────────────────────────┐
    │    限制: 120m (国家标准)      │
    │                              │
    │   城市边缘区 (Urban Edge)     │
    │  ┌─────────────────────┐    │
    │  │   限制: 90m          │    │
    │  │                      │    │
    │  │ 城市核心区 (Core)    │    │
    │  │ ┌─────────────┐     │    │
    │  │ │ 限制: 60m    │     │    │
    │  │ │   中心(0,0)  │     │    │
    │  │ │  半径1000m   │     │    │
    │  │ └─────────────┘     │    │
    │  │    半径2000m         │    │
    │  └─────────────────────┘    │
    │       半径2000m以外          │
    └─────────────────────────────┘
```

### 区域参数

| 区域ID | 名称 | 中心 | 半径 | 高度限制 | 优先级 |
|--------|------|------|------|---------|--------|
| `urban_core` | 城市核心区 | (0,0) | 1000m | 60m | 3 (最高) |
| `urban_edge` | 城市边缘区 | (0,0) | 2000m | 90m | 2 |
| `suburban` | 郊区 | - | 2000m外 | 120m | 1 (默认) |

### 测试用例设计

| TC  | 目标位置 | 距中心 | 所在区域 | 目标高度 | 区域限制 | 预期决策 | 测试目的 |
|-----|---------|--------|---------|---------|---------|---------|---------|
| TC1 | (500,0) | 500m | 核心区 | 50m | 60m | ✅ APPROVE | 核心区内合规 |
| TC2 | (500,0) | 500m | 核心区 | 60m | 60m | 🚫 REJECT | 核心区边界值 ⭐ |
| TC3 | (500,0) | 500m | 核心区 | 70m | 60m | 🚫 REJECT | 核心区超限 |
| TC4 | (1500,0) | 1500m | 边缘区 | 80m | 90m | ✅ APPROVE | 边缘区内合规 |
| TC5 | (1500,0) | 1500m | 边缘区 | 90m | 90m | 🚫 REJECT | 边缘区边界值 ⭐ |
| TC6 | (2500,0) | 2500m | 郊区 | 110m | 120m | ✅ APPROVE | 郊区合规 |
| TC7 | (2500,0) | 2500m | 郊区 | 120m | 120m | 🚫 REJECT | 郊区边界值 ⭐ |
| TC8 | (500,0) | 500m | 核心区 | 70m | 60m | 🚫 REJECT | 跨区飞行检查 |

#### 关键测试点

**边界值三连测** ⭐:
- TC2: 60m（核心区边界）
- TC5: 90m（边缘区边界）
- TC7: 120m（郊区边界）

**区域识别**:
- TC1-TC3: 验证核心区识别（距中心500m < 1000m）
- TC4-TC5: 验证边缘区识别（1000m < 1500m < 2000m）
- TC6-TC7: 验证郊区识别（2500m > 2000m）

**跨区飞行**:
- TC8: 起点在郊区(2500,0)，目标在核心区(500,0)，高度70m
- 验证：检查目标位置的区域限制，而非起点

---

## 🔍 技术实现要点

### 1. 区域识别算法

```python
def identify_zone(position: Position3D, altitude_zones: List[ZoneConfig]) -> ZoneConfig:
    """
    根据位置识别所在区域
    
    策略：从高优先级到低优先级检查
    """
    # 按优先级排序（降序）
    sorted_zones = sorted(altitude_zones, key=lambda z: z.priority, reverse=True)
    
    for zone in sorted_zones:
        if is_position_in_zone(position, zone):
            return zone
    
    # 默认返回最低优先级区域（郊区）
    return sorted_zones[-1]

def is_position_in_zone(position: Position3D, zone: ZoneConfig) -> bool:
    """检查位置是否在区域内"""
    if zone.geometry.type == "circle":
        distance = calculate_horizontal_distance(position, zone.geometry.center)
        return distance < zone.geometry.radius
    elif zone.geometry.type == "infinite":
        # 郊区：在所有圆形区域之外
        return True  # 默认区域
    return False
```

**关键逻辑**:
1. **优先级排序**: 先检查高优先级区域（核心区3 > 边缘区2 > 郊区1）
2. **嵌套处理**: 由于核心区在边缘区内，优先级高的先匹配
3. **水平距离**: 仅计算水平面距离（north, east），不考虑高度

### 2. 分区高度检查

```python
def check_zone_altitude_limit(
    position: Position3D,
    target_altitude_agl: float,
    altitude_zones: List[ZoneConfig]
) -> Tuple[bool, str, ZoneConfig]:
    """
    检查位置的分区高度限制
    
    Returns:
        (is_safe, reason, zone)
    """
    # 1. 识别所在区域
    zone = identify_zone(position, altitude_zones)
    
    # 2. 应用该区域的高度限制
    if target_altitude_agl >= zone.altitude_limit_agl:
        return (
            False,
            f"目标位置在{zone.name}（限制{zone.altitude_limit_agl}m），"
            f"高度{target_altitude_agl}m超限",
            zone
        )
    else:
        margin = zone.altitude_limit_agl - target_altitude_agl
        return (
            True,
            f"目标位置在{zone.name}（限制{zone.altitude_limit_agl}m），"
            f"高度{target_altitude_agl}m合规（距限制{margin}m）",
            zone
        )
```

### 3. 距离计算（仅水平）

**为什么仅水平距离？**
- 区域划分基于地面范围（人口密度）
- 高度是被检查的对象，不是区域判断的条件

```python
def calculate_horizontal_distance(pos1: Position3D, pos2: Position3D) -> float:
    """计算水平面距离（忽略高度）"""
    dx = pos1.north - pos2.north
    dy = pos1.east - pos2.east
    return math.sqrt(dx**2 + dy**2)
```

**示例**:
```python
# 位置: (500, 0, -70) → 距中心500m
distance = sqrt((500-0)^2 + (0-0)^2) = 500m
# 500m < 1000m → 在核心区内
# 检查高度: 70m vs 60m限制 → 超限
```

---

## 📊 预期结果

### Ground Truth

```json
{
  "scenario_id": "S007_ZoneAltitudeLimits",
  "test_cases": [
    {
      "id": "TC1",
      "target_zone": "urban_core",
      "zone_limit": 60.0,
      "target_altitude": 50.0,
      "expected_decision": "APPROVE"
    },
    {
      "id": "TC2",
      "target_zone": "urban_core",
      "zone_limit": 60.0,
      "target_altitude": 60.0,
      "expected_decision": "REJECT"
    },
    // ... TC3-TC8
  ]
}
```

### 执行命令示例

```bash
# TC1: 核心区内低高度
python run_scenario.py S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC1.json \
    --mode auto \
    --command "move_to_position(500, 0, 50)"

# TC2: 核心区边界值（关键）
python run_scenario.py S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC2.json \
    --mode auto \
    --command "move_to_position(500, 0, 60)"

# TC8: 跨区飞行
python run_scenario.py S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC8.json \
    --mode auto \
    --command "move_to_position(500, 0, 70)"
```

---

## 🎓 教学价值

### 1. 空间化规则
- **S006**: 全局规则（everywhere 120m）
- **S007**: 空间化规则（different limits in different places）

### 2. 嵌套区域处理
- **优先级机制**: 解决区域重叠问题
- **从内到外**: 核心区 → 边缘区 → 郊区
- **工程实践**: 真实城市管理的简化模型

### 3. 多边界值测试
- **3个独立边界**: 60m, 90m, 120m
- **验证逻辑一致性**: 每个区域都用`>=`判断
- **全面覆盖**: 8个TC覆盖所有区域+边界

---

## 🔗 相关场景

| 场景 | 关系 | 说明 |
|-----|------|------|
| **S006** | 前置 | 全局高度上限（120m） |
| **S008** | 后续 | 建筑物附近豁免（特殊区域+400ft） |
| **S002** | 关联 | 多geofence（空间划分） |

---

## 📝 测试检查清单

执行S007测试时，需要验证：

- [ ] **TC1/TC4/TC6 (APPROVE)**: 各区域内合规飞行被批准
- [ ] **TC2/TC5/TC7 (REJECT)**: 3个边界值全部正确拒绝
- [ ] **TC3 (REJECT)**: 核心区超限拒绝
- [ ] **TC8 (REJECT)**: 跨区飞行检查目标位置
- [ ] **区域识别**: 日志显示正确的区域名称
- [ ] **拒绝原因**: 包含区域名称、区域限制、超出距离
- [ ] **轨迹点数**: REJECT的TC仅1点，APPROVE的TC有完整轨迹

---

## ⚠️ 注意事项

### 1. 优先级顺序
- **必须从高到低检查**: 否则边缘区会"吞掉"核心区
- **核心区优先级3**: 先匹配，即使在边缘区范围内

### 2. 距离计算
- **仅水平距离**: `sqrt(Δnorth² + Δeast²)`
- **不含高度**: 高度是被检查的对象，不是区域条件

### 3. 跨区飞行
- **检查目标位置**: 不是起点，不是路径
- **TC8验证**: 起点在郊区，目标在核心区，按核心区限制检查

---

**文档版本**: 1.0  
**创建日期**: 2025-10-22  
**作者**: AirSim-RuleBench Team

---

## 附录：区域识别流程图

```
输入: 目标位置 (north, east)
  ↓
计算距中心距离: distance = sqrt(north² + east²)
  ↓
按优先级检查:
  ├─ 距离 < 1000m? → 核心区 (60m限制) [优先级3]
  ├─ 距离 < 2000m? → 边缘区 (90m限制) [优先级2]
  └─ 距离 ≥ 2000m? → 郊区 (120m限制) [优先级1]
  ↓
应用区域限制:
  └─ altitude >= zone.limit? → REJECT
     altitude < zone.limit?  → APPROVE
```

## 附录：测试覆盖矩阵

| 区域 | 合规测试 | 边界测试 | 超限测试 | 覆盖率 |
|------|---------|---------|---------|--------|
| 核心区 | TC1 (50m) | TC2 (60m) ⭐ | TC3 (70m) | 100% |
| 边缘区 | TC4 (80m) | TC5 (90m) ⭐ | - | 100% |
| 郊区 | TC6 (110m) | TC7 (120m) ⭐ | - | 100% |
| 跨区 | - | - | TC8 | 特殊 |

**总计**: 8个TC，3个边界值，100%覆盖

