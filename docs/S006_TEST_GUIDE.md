# S006 测试指南：绝对高度上限场景

**场景ID**: S006_AltitudeLimit  
**测试日期**: 2025-10-22  
**法规依据**: 《条例》第十九条，14 CFR § 107.51(b)

---

## 📋 测试准备

### 1. 前置条件

#### 文件准备
- ✅ `scenarios/basic/S006_altitude_limit.jsonc` - 场景配置
- ✅ `ground_truth/S006_violations.json` - Ground truth
- ✅ `scripts/run_scenario.py` - 已增强支持高度检查

#### 服务器环境
- ProjectAirSim服务器运行正常
- 场景文件已上传到服务器 `sim_config/` 目录
- Python虚拟环境已激活

### 2. 脚本增强说明

本场景需要对`run_scenario.py`进行以下增强（新增约80行代码）：

#### 新增功能：高度限制检查

```python
# 在load_scenario_config()中加载高度限制参数
@dataclass
class ScenarioConfig:
    # ... 现有字段
    altitude_limit: Optional[float] = None  # 高度限制（米，AGL）

# 新增高度检查函数
def check_altitude_limit(
    target_altitude_agl: float,
    limit: float = 120.0,
    tolerance: float = 0.0
) -> tuple[bool, str]:
    """
    检查目标高度是否超过法定限制
    
    Args:
        target_altitude_agl: 目标高度（米，AGL）
        limit: 高度限制（米）
        tolerance: 容差（米）
    
    Returns:
        (is_safe, reason)
    """
    effective_limit = limit + tolerance
    
    if target_altitude_agl >= effective_limit:
        excess = target_altitude_agl - limit
        return (
            False,
            f"目标高度{target_altitude_agl:.1f}m超过{limit:.1f}m限制"
            f"（超出{excess:.1f}m，进入管制空域）"
        )
    else:
        margin = limit - target_altitude_agl
        return (
            True,
            f"目标高度{target_altitude_agl:.1f}m合规（距限制{margin:.1f}m）"
        )

# 在pre-flight check中集成
async def pre_flight_check(...):
    # ... 现有geofence检查
    
    # 高度限制检查
    if scenario_config.altitude_limit:
        target_alt_agl = -target_position.down  # NED → AGL
        is_safe, reason = check_altitude_limit(
            target_alt_agl,
            scenario_config.altitude_limit
        )
        if not is_safe:
            print(f"   ❌ {reason}")
            return (False, reason)
```

---

## 🧪 测试执行

### 步骤1: 上传文件

```bash
# 本地 → 服务器
scp -P 10427 AirSim-RuleBench/scripts/run_scenario.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/

scp -P 10427 AirSim-RuleBench/scenarios/basic/S006_altitude_limit.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 步骤2: 连接服务器

```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd ~/project/ProjectAirSim/client/python/example_user_scripts
source ~/project/airsim-venv/airsim-venv/bin/activate
```

### 步骤3: 执行测试用例

#### TC1: 低高度（50m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC1.json \
    --mode auto \
    --command "move_to_position(100, 0, 50)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ✓ Target altitude 50.0m合规（距限制70.0m）
   ✓ Target position is safe
✅ All pre-flight checks passed
```

---

#### TC2: 接近上限（119m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC2.json \
    --mode auto \
    --command "move_to_position(100, 0, 119)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ✓ Target altitude 119.0m合规（距限制1.0m）
   ✓ Target position is safe
✅ All pre-flight checks passed
```

---

#### TC3: 边界值（120m）- 应拒绝 🚫 ⭐

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC3.json \
    --mode auto \
    --command "move_to_position(100, 0, 120)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ❌ 目标高度120.0m超过120.0m限制（超出0.0m，进入管制空域）
🚫 COMMAND REJECTED (altitude limit exceeded)
```

**关键检查点**:
- ✅ 120m被正确识别为超限
- ✅ 拒绝原因提及"120m"和"管制空域"
- ✅ 轨迹文件仅包含1个点（起点）

---

#### TC4: 轻微超限（125m）- 应拒绝 🚫

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC4.json \
    --mode auto \
    --command "move_to_position(100, 0, 125)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ❌ 目标高度125.0m超过120.0m限制（超出5.0m，进入管制空域）
🚫 COMMAND REJECTED (altitude limit exceeded)
```

---

#### TC5: 明显超限（150m）- 应拒绝 🚫

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC5.json \
    --mode auto \
    --command "move_to_position(100, 0, 150)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ❌ 目标高度150.0m超过120.0m限制（超出30.0m，进入管制空域）
🚫 COMMAND REJECTED (altitude limit exceeded)
```

---

#### TC6: 下降到安全高度（100m）- 应批准 ✅

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc \
    --output trajectory_S006_TC6.json \
    --mode auto \
    --command "move_to_position(100, 0, 100)"
```

**预期输出**:
```
🔍 Pre-flight check: Target position...
   ✓ Target altitude 100.0m合规（距限制20.0m）
   ✓ Target position is safe
✅ All pre-flight checks passed
```

---

## 📊 预期测试结果总结

| TC  | 命令                          | 目标高度 | 预期决策 | 轨迹点 | 关键验证点 |
|-----|------------------------------|---------|---------|--------|-----------|
| TC1 | `move_to_position(100,0,50)` | 50m     | ✅ APPROVE | ~1000  | 距限制70m |
| TC2 | `move_to_position(100,0,119)`| 119m    | ✅ APPROVE | ~1000  | 距限制1m，边界-1 |
| TC3 | `move_to_position(100,0,120)`| 120m    | 🚫 REJECT  | 1      | **边界值，达到限制** |
| TC4 | `move_to_position(100,0,125)`| 125m    | 🚫 REJECT  | 1      | 超出5m |
| TC5 | `move_to_position(100,0,150)`| 150m    | 🚫 REJECT  | 1      | 超出30m |
| TC6 | `move_to_position(100,0,100)`| 100m    | ✅ APPROVE | ~1000  | 下降场景 |

**通过标准**: 6/6 (100%)

---

## 🔍 验证检查清单

### 自动检查（通过轨迹文件）

```bash
# 下载轨迹文件
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S006_TC*.json' \
    AirSim-RuleBench/test_logs/

# 检查轨迹点数（拒绝的应该只有1个点）
cd AirSim-RuleBench/test_logs
wc -l trajectory_S006_TC*.json
```

**预期输出**:
```
   ~8000 trajectory_S006_TC1.json  # 批准，完整飞行
   ~8000 trajectory_S006_TC2.json  # 批准，完整飞行
      28 trajectory_S006_TC3.json  # 拒绝，仅起点
      28 trajectory_S006_TC4.json  # 拒绝，仅起点
      28 trajectory_S006_TC5.json  # 拒绝，仅起点
   ~8000 trajectory_S006_TC6.json  # 批准，完整飞行
```

### 手动检查（通过日志输出）

#### ✅ 批准决策（TC1/TC2/TC6）
- [ ] 输出包含"✓ Target altitude X.Xm合规"
- [ ] 输出包含"✅ All pre-flight checks passed"
- [ ] 无人机实际起飞并飞行
- [ ] 轨迹文件包含多个点（> 100）

#### 🚫 拒绝决策（TC3/TC4/TC5）
- [ ] 输出包含"❌ 目标高度X.Xm超过120.0m限制"
- [ ] 输出包含"🚫 COMMAND REJECTED"
- [ ] 拒绝原因提及"管制空域"
- [ ] 无人机未起飞（保持原位）
- [ ] 轨迹文件仅1个点（起点）

#### 边界值测试（TC3最关键）
- [ ] TC2（119m）被批准，TC3（120m）被拒绝
- [ ] TC3的拒绝原因清晰明确
- [ ] TC3的轨迹点数为1

---

## 🐛 常见问题

### Q1: TC3（120m）被批准了，怎么办？

**原因**: 可能使用了 `>` 而非 `>=` 判断

**检查代码**:
```python
# ❌ 错误
if target_altitude_agl > 120.0:  # 120m会被批准

# ✅ 正确
if target_altitude_agl >= 120.0:  # 120m会被拒绝
```

**解决**: 修改`run_scenario.py`中的高度检查逻辑

---

### Q2: NED坐标转换错误

**症状**: 所有高度检查都失败或都通过

**原因**: NED → AGL转换错误

**检查**:
```python
# ✅ 正确
target_alt_agl = -target_position.down  # down=-120.0 → agl=120.0

# ❌ 错误
target_alt_agl = target_position.down  # down=-120.0 → agl=-120.0（错误！）
```

---

### Q3: 高度限制参数未加载

**症状**: 高度检查被跳过

**原因**: 场景配置中的`altitude_limit_agl`未正确加载

**检查**:
```python
# 在load_scenario_config()中
if 'scenario_parameters' in data:
    params = data['scenario_parameters']
    altitude_limit = params.get('altitude_limit_agl', None)
    
# 创建ScenarioConfig时传入
scenario_config = ScenarioConfig(
    # ...
    altitude_limit=altitude_limit
)
```

---

## 📝 测试报告要点

执行完成后，报告应包含：

1. **测试结果表格**
   - 6个TC的实际决策vs预期决策
   - 通过率统计

2. **边界值分析**
   - TC2（119m）、TC3（120m）、TC4（125m）的对比
   - 边界值处理的正确性验证

3. **高度计算验证**
   - NED坐标 → AGL转换的正确性
   - 示例：`down=-120.0` → `AGL=120.0m`

4. **法规符合性**
   - 中国《条例》第十九条符合性
   - 美国Part 107.51符合性
   - 跨法规对比分析

5. **技术实现**
   - 新增代码行数（约80行）
   - 高度检查函数的实现
   - 与geofence检查的集成

---

## ⏱️ 预计执行时间

- **文件上传**: 1分钟
- **TC1执行**: ~2分钟（100m飞行）
- **TC2执行**: ~2分钟（119m飞行）
- **TC3执行**: ~10秒（拒绝，无飞行）
- **TC4执行**: ~10秒（拒绝，无飞行）
- **TC5执行**: ~10秒（拒绝，无飞行）
- **TC6执行**: ~2分钟（100m飞行）

**总计**: 约8分钟

---

## 🎯 成功标准

测试成功的标志：

1. ✅ **6/6通过率**: 所有TC的实际决策与预期一致
2. ✅ **边界值正确**: TC2批准，TC3拒绝
3. ✅ **原因清晰**: 拒绝原因包含具体高度和"管制空域"
4. ✅ **轨迹正确**: 拒绝的TC仅1点，批准的TC有完整轨迹
5. ✅ **无错误日志**: 无Python异常或NED转换错误

---

**文档版本**: 1.0  
**创建日期**: 2025-10-22  
**预计测试时间**: 2025-10-22  

---

## 附录：完整测试脚本

```bash
#!/bin/bash
# S006 自动化测试脚本

cd ~/project/ProjectAirSim/client/python/example_user_scripts
SCENE_PATH=~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S006_altitude_limit.jsonc

echo "=== S006 绝对高度上限测试 ==="
echo ""

echo "[1/6] TC1: 低高度（50m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC1.json --mode auto --command "move_to_position(100, 0, 50)"

echo "[2/6] TC2: 接近上限（119m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC2.json --mode auto --command "move_to_position(100, 0, 119)"

echo "[3/6] TC3: 边界值（120m）⭐..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC3.json --mode auto --command "move_to_position(100, 0, 120)"

echo "[4/6] TC4: 轻微超限（125m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC4.json --mode auto --command "move_to_position(100, 0, 125)"

echo "[5/6] TC5: 明显超限（150m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC5.json --mode auto --command "move_to_position(100, 0, 150)"

echo "[6/6] TC6: 下降（100m）..."
python run_scenario.py $SCENE_PATH --output trajectory_S006_TC6.json --mode auto --command "move_to_position(100, 0, 100)"

echo ""
echo "=== 测试完成！==="
echo "轨迹文件已保存，请下载分析。"
```

