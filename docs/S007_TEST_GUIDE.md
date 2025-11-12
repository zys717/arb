# S007 测试指南：分区高度限制场景

**场景ID**: S007_ZoneAltitudeLimits  
**测试日期**: 2025-10-22  
**法规依据**: 地方性规定（分级管理）

---

## 📋 测试准备

### 1. 前置条件

#### 文件准备
- ✅ `scenarios/basic/S007_zone_altitude_limits.jsonc` - 场景配置
- ✅ `ground_truth/S007_violations.json` - Ground truth
- ✅ `scripts/run_scenario.py` - 已增强支持分区高度检查

#### 服务器环境
- ProjectAirSim服务器运行正常
- 场景文件已上传到服务器 `sim_config/` 目录
- Python虚拟环境已激活

### 2. 脚本增强说明

本场景需要对`run_scenario.py`进行以下增强（新增约100行代码）：

#### 新增数据结构：区域配置

```python
@dataclass
class AltitudeZoneConfig:
    """高度限制区域配置"""
    id: str
    name: str
    center: Position3D
    radius: float  # 负数表示infinite
    altitude_limit_agl: float
    priority: int
    zone_type: str
```

#### 新增功能1：区域识别

```python
def identify_altitude_zone(
    position: Position3D,
    altitude_zones: List[AltitudeZoneConfig]
) -> Optional[AltitudeZoneConfig]:
    """
    根据位置识别所在高度限制区域
    
    策略：按优先级从高到低检查（处理嵌套区域）
    """
    sorted_zones = sorted(altitude_zones, key=lambda z: z.priority, reverse=True)
    
    for zone in sorted_zones:
        if zone.radius < 0:  # infinite zone
            return zone  # 默认区域
        
        # 计算水平距离（仅north和east）
        dx = position.north - zone.center.north
        dy = position.east - zone.center.east
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < zone.radius:
            return zone
    
    # 返回最低优先级区域作为默认
    return sorted_zones[-1] if sorted_zones else None
```

#### 新增功能2：分区高度检查

```python
def check_zone_altitude_limit(
    position: Position3D,
    target_altitude_agl: float,
    altitude_zones: List[AltitudeZoneConfig]
) -> Tuple[bool, str, Optional[AltitudeZoneConfig]]:
    """
    检查位置的分区高度限制
    
    Returns:
        (is_safe, reason, zone)
    """
    zone = identify_altitude_zone(position, altitude_zones)
    
    if not zone:
        return (True, "未识别到高度限制区域", None)
    
    if target_altitude_agl >= zone.altitude_limit_agl:
        excess = target_altitude_agl - zone.altitude_limit_agl
        return (
            False,
            f"目标位置在{zone.name}（限制{zone.altitude_limit_agl:.1f}m），"
            f"高度{target_altitude_agl:.1f}m超限（超出{excess:.1f}m）",
            zone
        )
    else:
        margin = zone.altitude_limit_agl - target_altitude_agl
        return (
            True,
            f"目标位置在{zone.name}（限制{zone.altitude_limit_agl:.1f}m），"
            f"高度{target_altitude_agl:.1f}m合规（距限制{margin:.1f}m）",
            zone
        )
```

---

## 🧪 测试执行

### 步骤1: 上传文件

```bash
# 本地 → 服务器
scp -P 10427 AirSim-RuleBench/scripts/run_scenario.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/

scp -P 10427 AirSim-RuleBench/scenarios/basic/S007_zone_altitude_limits.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 步骤2: 连接服务器

```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd ~/project/ProjectAirSim/client/python/example_user_scripts
source ~/project/airsim-venv/airsim-venv/bin/activate
```

### 步骤3: 执行测试用例

#### TC1: 核心区内低高度（50m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC1.json \
    --mode auto \
    --command "move_to_position(500, 0, 50)"
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (zone-based)...
   识别区域: 城市核心区 (距中心500.0m < 1000.0m)
   ✓ 目标位置在城市核心区（限制60.0m），高度50.0m合规（距限制10.0m）
```

---

#### TC2: 核心区边界值（60m）- 应拒绝 🚫 ⭐

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC2.json \
    --mode auto \
    --command "move_to_position(500, 0, 60)"
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (zone-based)...
   识别区域: 城市核心区 (距中心500.0m < 1000.0m)
   ❌ 目标位置在城市核心区（限制60.0m），高度60.0m超限（超出0.0m）

🚫 COMMAND REJECTED (zone altitude limit exceeded)
```

**关键检查点**:
- ✅ 60m被正确识别为超限（核心区）
- ✅ 区域识别正确（核心区）
- ✅ 拒绝原因包含区域名称和限制值

---

#### TC3: 核心区超限（70m）- 应拒绝 🚫

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC3.json \
    --mode auto \
    --command "move_to_position(500, 0, 70)"
```

**预期输出**:
```
   ❌ 目标位置在城市核心区（限制60.0m），高度70.0m超限（超出10.0m）
```

---

#### TC4: 边缘区合规（80m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC4.json \
    --mode auto \
    --command "move_to_position(1500, 0, 80)"
```

**预期输出**:
```
   识别区域: 城市边缘区 (距中心1500.0m，在1000.0m-2000.0m间)
   ✓ 目标位置在城市边缘区（限制90.0m），高度80.0m合规（距限制10.0m）
```

**验证点**: 1500m不在核心区（>1000m），正确识别为边缘区

---

#### TC5: 边缘区边界值（90m）- 应拒绝 🚫 ⭐

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC5.json \
    --mode auto \
    --command "move_to_position(1500, 0, 90)"
```

**预期输出**:
```
   识别区域: 城市边缘区
   ❌ 目标位置在城市边缘区（限制90.0m），高度90.0m超限（超出0.0m）
```

---

#### TC6: 郊区合规（110m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC6.json \
    --mode auto \
    --command "move_to_position(2500, 0, 110)"
```

**预期输出**:
```
   识别区域: 郊区 (距中心2500.0m > 2000.0m)
   ✓ 目标位置在郊区（限制120.0m），高度110.0m合规（距限制10.0m）
```

---

#### TC7: 郊区边界值（120m）- 应拒绝 🚫 ⭐

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC7.json \
    --mode auto \
    --command "move_to_position(2500, 0, 120)"
```

**预期输出**:
```
   识别区域: 郊区
   ❌ 目标位置在郊区（限制120.0m），高度120.0m超限（超出0.0m）
```

---

#### TC8: 跨区飞行（郊区→核心区，70m）- 应拒绝 🚫

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc \
    --output trajectory_S007_TC8.json \
    --mode auto \
    --command "move_to_position(500, 0, 70)"
```

**预期输出**:
```
   初始位置: 郊区 (距中心2500.0m)
   目标位置: (500, 0)
   识别区域: 城市核心区 (距中心500.0m < 1000.0m)
   ❌ 目标位置在城市核心区（限制60.0m），高度70.0m超限（超出10.0m）
```

**验证点**: 检查目标位置(500,0)的区域，而非起点(2500,0)

---

## 📊 预期测试结果总结

| TC  | 命令                           | 距中心 | 区域 | 区域限制 | 目标高度 | 预期决策 | 轨迹点 |
|-----|-------------------------------|--------|------|---------|---------|---------|--------|
| TC1 | `move_to_position(500,0,50)`  | 500m   | 核心 | 60m     | 50m     | ✅ APPROVE | ~200 |
| TC2 | `move_to_position(500,0,60)`  | 500m   | 核心 | 60m     | 60m     | 🚫 REJECT  | 1 ⭐ |
| TC3 | `move_to_position(500,0,70)`  | 500m   | 核心 | 60m     | 70m     | 🚫 REJECT  | 1 |
| TC4 | `move_to_position(1500,0,80)` | 1500m  | 边缘 | 90m     | 80m     | ✅ APPROVE | ~200 |
| TC5 | `move_to_position(1500,0,90)` | 1500m  | 边缘 | 90m     | 90m     | 🚫 REJECT  | 1 ⭐ |
| TC6 | `move_to_position(2500,0,110)`| 2500m  | 郊区 | 120m    | 110m    | ✅ APPROVE | ~100 |
| TC7 | `move_to_position(2500,0,120)`| 2500m  | 郊区 | 120m    | 120m    | 🚫 REJECT  | 1 ⭐ |
| TC8 | `move_to_position(500,0,70)`  | 500m   | 核心 | 60m     | 70m     | 🚫 REJECT  | 1 |

**通过标准**: 8/8 (100%)

---

## 🔍 验证检查清单

### 自动检查（通过轨迹文件）

```bash
# 下载轨迹文件
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S007_TC*.json' \
    AirSim-RuleBench/test_logs/

# 检查轨迹点数
cd AirSim-RuleBench/test_logs
wc -l trajectory_S007_TC*.json
```

**预期输出**:
```
   ~1600 trajectory_S007_TC1.json  # 批准
      28 trajectory_S007_TC2.json  # 拒绝 ⭐
      28 trajectory_S007_TC3.json  # 拒绝
   ~1600 trajectory_S007_TC4.json  # 批准
      28 trajectory_S007_TC5.json  # 拒绝 ⭐
    ~800 trajectory_S007_TC6.json  # 批准（起点近）
      28 trajectory_S007_TC7.json  # 拒绝 ⭐
      28 trajectory_S007_TC8.json  # 拒绝
```

### 手动检查（通过日志输出）

#### ✅ 区域识别检查
- [ ] TC1-TC3: 显示"城市核心区"
- [ ] TC4-TC5: 显示"城市边缘区"
- [ ] TC6-TC7: 显示"郊区"
- [ ] 显示距中心距离

#### ✅ 批准决策（TC1/TC4/TC6）
- [ ] 输出包含区域名称和限制值
- [ ] 显示"合规（距限制Xm）"
- [ ] 无人机成功起飞并飞行

#### 🚫 拒绝决策（TC2/TC3/TC5/TC7/TC8）
- [ ] 输出包含"超限"字样
- [ ] 显示区域名称、限制值、超出距离
- [ ] 无人机未起飞（保持原位）
- [ ] 轨迹文件仅1个点

#### 边界值测试（TC2/TC5/TC7最关键）
- [ ] TC2（60m）被拒绝，TC1（50m）被批准
- [ ] TC5（90m）被拒绝，TC4（80m）被批准
- [ ] TC7（120m）被拒绝，TC6（110m）被批准

#### 跨区飞行（TC8）
- [ ] 日志显示目标位置在核心区
- [ ] 应用核心区60m限制（非郊区120m）
- [ ] 70m超过60m被拒绝

---

## 🐛 常见问题

### Q1: TC4被识别为核心区而非边缘区？

**原因**: 优先级顺序错误，或未按优先级排序

**检查代码**:
```python
# ✅ 正确：优先级降序
sorted_zones = sorted(zones, key=lambda z: z.priority, reverse=True)
# 核心区(3) → 边缘区(2) → 郊区(1)

# ❌ 错误：优先级升序或未排序
# 可能导致边缘区先匹配，"吞掉"核心区
```

---

### Q2: 所有位置都被识别为同一区域？

**原因**: 距离计算错误，可能包含了高度

**检查**:
```python
# ✅ 正确：仅水平距离
dx = position.north - zone.center.north
dy = position.east - zone.center.east
distance = sqrt(dx^2 + dy^2)  # 不含down

# ❌ 错误：包含高度
# 会导致高空飞行被识别为远距离（郊区）
```

---

### Q3: TC8检查起点而非目标位置？

**原因**: 位置参数传递错误

**检查**:
```python
# ✅ 正确：传入目标位置
check_zone_altitude_limit(target_pos, target_alt, zones)

# ❌ 错误：传入当前位置
check_zone_altitude_limit(current_pos, target_alt, zones)
```

---

## 📝 测试报告要点

执行完成后，报告应包含：

1. **区域识别准确性**
   - 8个TC的区域识别结果
   - 距中心距离计算验证

2. **分区限制执行**
   - 核心区60m、边缘区90m、郊区120m的独立验证
   - 每个区域的边界值测试结果

3. **嵌套区域处理**
   - TC4验证优先级逻辑（1500m识别为边缘区，非核心区）

4. **跨区飞行**
   - TC8验证目标位置检查逻辑

5. **与S006对比**
   - S006: 全局120m
   - S007: 分区60m/90m/120m
   - 郊区行为应与S006一致

---

## ⏱️ 预计执行时间

- **文件上传**: 1分钟
- **TC1执行**: ~1分钟（500m飞行）
- **TC2执行**: ~10秒（拒绝）
- **TC3执行**: ~10秒（拒绝）
- **TC4执行**: ~2分钟（1000m飞行）
- **TC5执行**: ~10秒（拒绝）
- **TC6执行**: ~30秒（起点近）
- **TC7执行**: ~10秒（拒绝）
- **TC8执行**: ~10秒（拒绝）

**总计**: 约5分钟

---

## 🎯 成功标准

测试成功的标志：

1. ✅ **8/8通过率**: 所有TC的实际决策与预期一致
2. ✅ **区域识别**: 8个TC的区域全部正确识别
3. ✅ **边界值**: TC2/TC5/TC7三个边界值全部拒绝
4. ✅ **限制应用**: 核心60m/边缘90m/郊区120m正确应用
5. ✅ **跨区检查**: TC8检查目标位置而非起点
6. ✅ **原因清晰**: 包含区域名称、限制值、高度值
7. ✅ **轨迹正确**: 拒绝5个TC仅1点，批准3个TC有完整轨迹

---

**文档版本**: 1.0  
**创建日期**: 2025-10-22  
**预计测试时间**: 2025-10-22  

---

## 附录：完整测试脚本

```bash
#!/bin/bash
# S007 自动化测试脚本

cd ~/project/ProjectAirSim/client/python/example_user_scripts
SCENE_PATH=~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S007_zone_altitude_limits.jsonc

echo "=== S007 分区高度限制测试 ==="
echo ""

echo "[1/8] TC1: 核心区内低高度（50m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC1.json --mode auto --command "move_to_position(500, 0, 50)"

echo "[2/8] TC2: 核心区边界值（60m）⭐..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC2.json --mode auto --command "move_to_position(500, 0, 60)"

echo "[3/8] TC3: 核心区超限（70m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC3.json --mode auto --command "move_to_position(500, 0, 70)"

echo "[4/8] TC4: 边缘区合规（80m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC4.json --mode auto --command "move_to_position(1500, 0, 80)"

echo "[5/8] TC5: 边缘区边界值（90m）⭐..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC5.json --mode auto --command "move_to_position(1500, 0, 90)"

echo "[6/8] TC6: 郊区合规（110m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC6.json --mode auto --command "move_to_position(2500, 0, 110)"

echo "[7/8] TC7: 郊区边界值（120m）⭐..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC7.json --mode auto --command "move_to_position(2500, 0, 120)"

echo "[8/8] TC8: 跨区飞行（郊区→核心区）..."
python run_scenario.py $SCENE_PATH --output trajectory_S007_TC8.json --mode auto --command "move_to_position(500, 0, 70)"

echo ""
echo "=== 测试完成！==="
echo "轨迹文件已保存，请下载分析。"
```

