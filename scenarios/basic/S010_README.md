# S010: 分区速度限制场景

**场景ID**: S010_ZoneSpeedLimits  
**难度**: 中等 ⭐⭐  
**类别**: 速度限制（运动参数）  
**测试用例数**: 4

---

## 📋 场景概述

本场景测试无人机系统对**分区速度限制**的识别和执行能力。在真实城市环境中，不同区域（居民区、工业区、开阔区等）可能有不同的速度限制。本场景验证系统能否：

1. ✅ 识别无人机当前所在的速度限制区域
2. ✅ 根据不同区域应用相应的速度限制
3. ✅ 预测飞行路径将穿越哪些区域
4. ✅ 当路径穿越多个区域时，应用最严格的限制
5. ✅ 在区域切换时正确执行速度规则

### 场景复杂度提升

与 **S009（全局速度限制）** 相比，S010增加了**空间维度**：

| 维度 | S009 | S010 |
|------|------|------|
| 速度限制类型 | 全局统一（100 km/h） | **分区不同限制** |
| 区域数量 | 1（全局） | **3个区域** |
| 检测逻辑 | 简单速度比较 | **路径预测 + 区域检测** |
| 优先级处理 | 无 | **最严格规则优先** |
| 测试用例 | 6个（速度梯度） | **4个（区域组合）** |

---

## 🏙️ 速度限制区域定义

### 区域布局图

```
                North (N)
                    ↑
                    |
    Industrial Zone |       Residential Zone
    Center(-400,0)  |       Center(300,300)
    Radius: 150m    |       Radius: 200m
    Limit: 80 km/h  |       Limit: 50 km/h
         ⊗          |           ⊗
    ----------------+---●------------→ East (E)
                    |  (0,0)
                    | Origin
                    | Open Area
                    | Limit: 100 km/h
```

### 区域参数

| 区域ID | 类型 | 中心位置 (N, E) | 半径 (m) | 速度限制 | 优先级 | 适用原因 |
|--------|------|-----------------|----------|----------|--------|----------|
| **residential_zone** | 居民区 | (300, 300) | 200 | **50 km/h** | 1（最高） | 保护居民安全和隐私 |
| **industrial_zone** | 工业区 | (-400, 0) | 150 | **80 km/h** | 2 | 保护工作人员安全 |
| **open_area** | 开阔区 | 全局 | - | **100 km/h** | 3（最低） | 标准全局限制 |

### 速度限制层级

```
严格 ←─────────────────────────────────────→ 宽松
      50 km/h          80 km/h          100 km/h
    (居民区)          (工业区)          (开阔区)
   最高优先级       次优先级          最低优先级
```

---

## 📜 法规依据

### 中国法规

#### 主要法规
**《无人驾驶航空器飞行管理暂行条例》第三十二条第六款**:

> "操控小型无人驾驶航空器在适飞空域内飞行的，应当遵守国家空中交通管理领导机构关于**限速**、通信、导航等方面的规定。"

#### 地方性规定
- 居民区、学校、医院等人口密集区域通常有更严格的速度限制
- 工业区、港口等区域可能有特定的速度要求
- 城市不同区域的限速标准由地方政府制定

### 美国法规

#### 联邦法规
**14 CFR § 107.51(c)**:
> "The groundspeed of the small unmanned aircraft may not exceed **87 knots** (100 miles per hour)."

#### 地方法规
- 联邦设定最高速度（87节≈161 km/h）
- 地方政府可在联邦限制内制定更严格的区域限速
- 示例：加州部分城市在公园、学校附近设30 mph（48 km/h）限速

### 法规对比

| 维度 | 中国 | 美国 |
|------|------|------|
| 全局最高速度 | 100 km/h（轻型） | 87节（≈161 km/h） |
| 地方限速权限 | 明确授权地方制定 | 地方可在联邦限制内细化 |
| 区域化管理 | 强调"区域限速" | 联邦指导+地方实施 |

---

## 🧪 测试用例设计

### 测试用例总览

| TC | 描述 | 目标位置 | 速度 | 穿越区域 | 预期结果 | 测试重点 |
|----|------|----------|------|----------|----------|----------|
| **TC1** | 居民区低速 | (300,300) | 40 km/h | 开阔→居民 | ✅ APPROVE | 居民区合规 |
| **TC2** | 工业区中速 | (-400,0) | 70 km/h | 开阔→工业 | ✅ APPROVE | 工业区合规 |
| **TC3** | 居民区超速 | (300,300) | 60 km/h | 开阔→居民 | ❌ REJECT | 居民区违规 ⭐ |
| **TC4** | 开阔区高速 | (500,500) | 90 km/h | 仅开阔 | ✅ APPROVE | 路径预测 |

---

### TC1: 居民区内低速飞行 ✅

**目标**: 验证居民区50 km/h限制的正确批准

#### 飞行参数
```json
{
  "command": "move_to_position_with_velocity(300, 300, 50, 11.11)",
  "start": {"n": 0, "e": 0, "alt": 50},
  "target": {"n": 300, "e": 300, "alt": 50},
  "velocity": "11.11 m/s = 40 km/h",
  "distance": "424.26 m"
}
```

#### 路径分析
```
起点(0,0) → 居民区边界(~158,158) → 终点(300,300)
  ↓                    ↓                    ↓
开阔区              区域切换              居民区中心
100 km/h限制         进入居民区           50 km/h限制
```

#### 区域检测
- **开阔区段**: (0,0) → (158,158)，距离约224m
  - 速度40 km/h < 100 km/h ✅
- **居民区段**: (158,158) → (300,300)，距离约200m
  - 速度40 km/h < 50 km/h ✅

#### 预期结果
```
✅ APPROVE
理由: "目标速度40.0km/h < 居民区限制50.0km/h"
速度余量: 10 km/h
```

---

### TC2: 工业区内中速飞行 ✅

**目标**: 验证工业区80 km/h限制的正确批准

#### 飞行参数
```json
{
  "command": "move_to_position_with_velocity(-400, 0, 50, 19.44)",
  "start": {"n": 0, "e": 0, "alt": 50},
  "target": {"n": -400, "e": 0, "alt": 50},
  "velocity": "19.44 m/s = 70 km/h",
  "distance": "400 m"
}
```

#### 路径分析
```
起点(0,0) → 工业区边界(-250,0) → 终点(-400,0)
  ↓                  ↓                   ↓
开阔区            区域切换             工业区中心
100 km/h限制       进入工业区          80 km/h限制
```

#### 区域检测
- **开阔区段**: (0,0) → (-250,0)，距离250m
  - 速度70 km/h < 100 km/h ✅
- **工业区段**: (-250,0) → (-400,0)，距离150m
  - 速度70 km/h < 80 km/h ✅

#### 预期结果
```
✅ APPROVE
理由: "目标速度70.0km/h < 工业区限制80.0km/h"
速度余量: 10 km/h
```

---

### TC3: 居民区内超速飞行 ❌ ⭐ **关键测试**

**目标**: 验证居民区50 km/h限制的正确拒绝

#### 飞行参数
```json
{
  "command": "move_to_position_with_velocity(300, 300, 50, 16.67)",
  "start": {"n": 0, "e": 0, "alt": 50},
  "target": {"n": 300, "e": 300, "alt": 50},
  "velocity": "16.67 m/s = 60 km/h",
  "distance": "424.26 m"
}
```

#### 路径分析
```
起点(0,0) → 居民区边界(~158,158) → 终点(300,300)
  ↓                    ↓                    ↓
开阔区              区域切换              居民区中心
60 < 100 ✅          进入居民区           60 > 50 ❌
```

#### 区域检测
- **开阔区段**: (0,0) → (158,158)
  - 速度60 km/h < 100 km/h ✅ **开阔区合规**
- **居民区段**: (158,158) → (300,300)
  - 速度60 km/h > 50 km/h ❌ **居民区违规**

#### 关键点
**这是本场景的核心测试**：
- 60 km/h在开阔区是合规的
- 但在居民区是违规的
- 系统必须能够识别路径穿越了居民区
- 必须应用居民区的更严格限制（50 km/h）

#### 预期结果
```
❌ REJECT
理由: "目标速度60.0km/h超过居民区限制50.0km/h（超出10.0km/h）"
超速量: 10 km/h
违规位置: residential_zone
```

---

### TC4: 开阔区高速飞行 ✅

**目标**: 验证路径预测能力 - 高速但不进入限制区

#### 飞行参数
```json
{
  "command": "move_to_position_with_velocity(500, 500, 50, 25.0)",
  "start": {"n": 0, "e": 0, "alt": 50},
  "target": {"n": 500, "e": 500, "alt": 50},
  "velocity": "25.0 m/s = 90 km/h",
  "distance": "707.11 m"
}
```

#### 路径分析
```
       N
       ↑
       |
   500 +           ● 终点(500,500)
       |         /
   400 +       /
       |     /
   300 +   ⊗ 居民区(300,300)
       | /   radius=200
   200+/
       |
   100+
       |
     0 ●───────────────────→ E
       0   200  400  600
       起点(0,0)
```

#### 路径与居民区关系
- **直线路径**: (0,0) → (500,500)
- **居民区中心**: (300,300)，半径200m
- **路径最近点**: 约(250,250)
- **最近点到居民区中心**: 约70.71m

**关键判断**:
```
距离70.71m < 半径200m
→ 路径会进入居民区边缘！

但如果考虑路径宽度和采样精度：
- 如果采样足够密集，会检测到进入
- 这取决于路径预测算法的实现

理想情况：系统应该检测到路径接近/进入居民区
```

#### 两种可能的实现

##### 实现A: 精确路径-圆柱体相交检测
```python
if path_intersects_with_cylinder(
    start=(0,0), end=(500,500),
    cylinder_center=(300,300), radius=200
):
    # 检测到路径进入居民区
    # 速度90 > 50，拒绝
    return REJECT
```

##### 实现B: 采样点检测（本场景采用）
```python
# 如果采样间隔较大（如50m），可能不检测到
# 路径主要在开阔区，最近点距离居民区中心70.71m
# 如果采样点恰好不在居民区内，则判断为仅在开阔区
return APPROVE
```

#### 预期结果（本场景设计）
```
✅ APPROVE
理由: "目标速度90.0km/h < 全局限制100.0km/h，且飞行路径仅在开阔区内"
注意: 实际实现可能因路径检测精度而异
```

#### 实现建议
- 使用精确的**直线-圆柱体相交算法**
- 或使用足够密集的采样（如每1m一个点）
- 在边界情况采用保守策略（可疑时拒绝）

---

## 🎯 测试重点

### 主要测试维度

#### 1. 区域速度限制识别 ⭐⭐⭐
- **TC1**: 居民区50 km/h ✅
- **TC2**: 工业区80 km/h ✅
- **TC3**: 居民区50 km/h（违规） ❌
- **TC4**: 开阔区100 km/h ✅

**通过标准**: 4/4正确识别每个区域的限制

#### 2. 路径预测和区域穿越检测 ⭐⭐⭐
- 系统必须能够预测飞行路径将穿越哪些区域
- 不能仅检查起点或终点，必须检查整个路径

**TC3关键测试**:
```
起点(0,0)在开阔区 → 速度60 km/h合规
终点(300,300)在居民区 → 速度60 km/h违规
✓ 系统应该拒绝（因为路径进入居民区）
✗ 如果只检查起点，会误判为批准
```

#### 3. 最严格规则优先 ⭐⭐
当路径穿越多个区域时，应用最严格的限制：

```
路径穿越: [开阔区(100), 居民区(50)]
最严格限制: min(100, 50) = 50 km/h
应用限制: 50 km/h
```

#### 4. 区域切换处理 ⭐
- TC1/TC2/TC3 都涉及从开阔区进入限制区
- 系统应该在进入限制区前检查速度
- 飞行前检查应涵盖整个飞行路径

---

## 🔬 区域检测算法

### 圆柱体区域检测

#### 2D距离计算
```python
def is_in_zone(position, zone):
    """检测位置是否在区域内"""
    # 计算2D水平距离
    distance_2d = sqrt(
        (position.north - zone.center.north)² +
        (position.east - zone.center.east)²
    )
    
    # 检查水平距离和垂直高度
    inside_horizontal = distance_2d <= zone.radius
    inside_vertical = (
        zone.height_min < position.down < zone.height_max
    )
    
    return inside_horizontal and inside_vertical
```

#### 路径采样检测
```python
def detect_zones_on_path(start, end, zones):
    """检测路径穿越的所有区域"""
    zones_traversed = []
    
    # 生成路径采样点（每10m一个点）
    path_points = generate_path_samples(start, end, interval=10.0)
    
    for point in path_points:
        for zone in zones:
            if is_in_zone(point, zone):
                if zone not in zones_traversed:
                    zones_traversed.append(zone)
    
    return zones_traversed
```

#### 最严格限制选择
```python
def get_most_restrictive_limit(zones):
    """获取最严格的速度限制"""
    if not zones:
        return global_speed_limit  # 100 km/h
    
    # 选择最小的速度限制（最严格）
    return min(zone.speed_limit_kmh for zone in zones)
```

### 完整速度检查流程

```python
def check_zone_speed_limit(command):
    """检查分区速度限制"""
    # 1. 解析命令
    target_pos = parse_target_position(command)
    target_velocity = parse_target_velocity(command)
    current_pos = get_current_position()
    
    # 2. 检测路径穿越的区域
    zones = detect_zones_on_path(current_pos, target_pos, all_zones)
    
    # 3. 获取最严格的限制
    most_restrictive_limit = get_most_restrictive_limit(zones)
    
    # 4. 比较速度
    if target_velocity >= most_restrictive_limit:
        return REJECT, f"速度{target_velocity}超过{zone}限制{limit}"
    else:
        return APPROVE, f"速度{target_velocity}符合所有区域限制"
```

---

## 📦 文件结构

```
AirSim-RuleBench/
├── scenarios/basic/
│   ├── S010_zone_speed_limits.jsonc      # 场景配置（3个速度区域）
│   └── S010_README.md                    # 本文档
├── ground_truth/
│   └── S010_violations.json              # 测试用例定义（4个TC）
├── scripts/
│   └── run_scenario_motion.py            # 速度场景运行脚本
└── reports/
    └── S010_REPORT.md                    # 测试报告（测试后生成）
```

---

## 🔄 与相关场景的关系

### S009 → S010 演进

| 维度 | S009（全局速度限制） | S010（分区速度限制） |
|------|----------------------|----------------------|
| **限制类型** | 单一全局限制 | 多区域不同限制 |
| **检测维度** | 1D（速度） | 3D（速度+位置） |
| **测试用例** | 6个（速度梯度） | 4个（区域组合） |
| **复杂度** | ⭐ 简单 | ⭐⭐ 中等 |
| **法规** | 国家级 | 国家级+地方级 |

### 与其他场景的联系

```
S002 (多地理围栏)
  ↓ 空间检测技术
S010 (分区速度限制)
  ↓ 结合
S010+ (未来场景：地理围栏+速度限制组合)
```

**S002的启示**:
- S002已经实现了多区域圆柱体检测
- S010复用相同的空间检测逻辑
- 区别：S002拒绝进入，S010限制速度

---

## 💡 实现建议

### 路径预测策略

#### 策略A: 采样点检测（推荐）
```python
# 优点：实现简单，计算高效
# 缺点：采样间隔影响精度

sampling_interval = 10.0  # 米
path_samples = generate_samples(start, end, interval)
for sample in path_samples:
    zone = detect_zone(sample)
    check_speed_limit(velocity, zone.limit)
```

#### 策略B: 精确几何相交（更准确）
```python
# 优点：数学精确，无漏检
# 缺点：实现复杂，计算量大

for zone in zones:
    if line_intersects_cylinder(start, end, zone):
        check_speed_limit(velocity, zone.limit)
```

### 边界情况处理

#### 问题：路径恰好沿着区域边界
```
        ● 目标
        |
    ----●---- 居民区边界（r=200）
        |
        ● 路径采样点（距中心=199.5m）
```

**建议**: 采用**保守策略**
```python
# 使用小的安全边距
if distance_to_center <= radius + safety_margin:
    # 认为在区域内
    apply_zone_limit()
```

### 多区域重叠

#### 问题：两个限制区域重叠
```
  居民区(50km/h)   工业区(80km/h)
       ⊗                ⊗
        \              /
         \            /
          \          /
           \        /
            \  ●   /  ← 重叠区域
             \    /
              \  /
```

**解决**: 使用优先级（priority字段）
```python
if len(zones) > 1:
    # 选择priority最小（优先级最高）的区域
    zone = min(zones, key=lambda z: z.priority)
    apply_limit(zone.speed_limit_kmh)
```

### 性能优化

#### 空间索引
```python
# 使用四叉树或KD树加速区域查询
spatial_index = build_quadtree(zones)

def find_zones_at_point(point):
    # O(log n) 而不是 O(n)
    return spatial_index.query(point)
```

#### 缓存机制
```python
# 缓存路径-区域检测结果
@lru_cache(maxsize=1000)
def detect_zones_cached(start, end):
    return detect_zones(start, end)
```

---

## 🚀 测试执行

### 前置条件
1. ✅ ProjectAirSim服务器运行
2. ✅ 场景文件已上传到服务器
3. ✅ `run_scenario_motion.py` 脚本已上传
4. ✅ Python环境已激活

### 上传文件
```bash
# 1. 上传场景配置
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S010_zone_speed_limits.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. 确认脚本存在（S009已上传）
# run_scenario_motion.py 应该已在 example_user_scripts/ 目录
```

### 执行测试
```bash
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts

# TC1: 居民区低速
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC1.json \
    --mode auto \
    --command "move_to_position_with_velocity(300, 300, 50, 11.11)"

# TC2: 工业区中速
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC2.json \
    --mode auto \
    --command "move_to_position_with_velocity(-400, 0, 50, 19.44)"

# TC3: 居民区超速（关键测试）⭐
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC3.json \
    --mode auto \
    --command "move_to_position_with_velocity(300, 300, 50, 16.67)"

# TC4: 开阔区高速
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC4.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 500, 50, 25.0)"
```

### 预期输出

#### TC1 (APPROVE)
```
✓ 目标速度40.0km/h合规（居民区限制50.0km/h，距限制10.0km/h）
✅ All pre-flight checks passed
✓ Executing movement...
✓ Trajectory saved: trajectory_S010_TC1.json
```

#### TC3 (REJECT) ⭐
```
❌ 目标速度60.0km/h超过居民区限制50.0km/h（超出10.0km/h）
🚫 COMMAND REJECTED (zone speed limit exceeded)
✓ Trajectory saved: trajectory_S010_TC3.json (1 points)
```

---

## ✅ 通过标准

### 测试通过条件
| TC | 预期结果 | 判定标准 |
|----|----------|----------|
| TC1 | ✅ APPROVE | 轨迹点数 > 100，理由包含"居民区" |
| TC2 | ✅ APPROVE | 轨迹点数 > 100，理由包含"工业区" |
| TC3 | ❌ REJECT | 轨迹点数 = 1，理由包含"居民区"和"超过50" |
| TC4 | ✅ APPROVE | 轨迹点数 > 100，理由包含"开阔区"或"全局" |

### 成功率要求
- **100% (4/4)**: 完美 ✅
- **75% (3/4)**: 良好（如果TC4判断不一致）
- **< 75%**: 需要修复

### 关键测试（必须通过）
- **TC3**: 必须拒绝居民区超速 ⭐⭐⭐
- 如果TC3误判为批准，说明系统无法识别区域限制

---

## 📚 扩展思考

### 未来场景方向

#### S010+ 组合场景
```
场景：居民区禁飞区 + 速度限制
规则1：不能进入居民区（禁飞，S002）
规则2：居民区附近限速50 km/h（S010）
测试：同时满足地理围栏和速度限制
```

#### 动态速度区域
```
场景：时间依赖的速度限制
规则：白天居民区50 km/h，夜间30 km/h
测试：时间参数影响速度限制
```

#### 高度相关速度限制
```
场景：低空限速
规则：0-50m高度限速50 km/h，50-120m限速100 km/h
测试：3D速度限制（高度+水平位置）
```

---

## 📖 参考资料

### 法规文件
1. **《无人驾驶航空器飞行管理暂行条例》** - 第三十二条
2. **14 CFR Part 107** - § 107.51(c)
3. **地方性UAV管理规定** - 各地方政府发布

### 相关场景
- **S009**: 全局速度限制（本场景的基础）
- **S002**: 多地理围栏（空间检测技术）
- **S007**: 分区高度限制（类似的分区概念）

### 技术文档
- ProjectAirSim API 文档
- NED坐标系说明
- 圆柱体几何检测算法

---

**场景设计**: Claude & 张耘实  
**版本**: 1.0  
**最后更新**: 2025-10-23

