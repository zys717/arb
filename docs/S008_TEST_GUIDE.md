# S008 建筑物附近高度豁免 - 测试指南

## 📋 测试概述

**场景ID**: S008_StructureWaiver  
**测试重点**: FAA Part 107.51(b) 建筑物400英尺半径高度豁免规则  
**测试用例数**: 4个  
**预期通过率**: 100%

---

## 🎯 测试目标

验证系统能够正确处理：
1. ✅ 全局高度限制（120m）
2. ✅ 建筑物豁免条件识别（水平距离判定）
3. ✅ 豁免高度上限计算（建筑高+400英尺）
4. ⭐ 边界值处理（半径边界精度）

---

## 🏗️ 场景配置

### 建筑物参数

```json
建筑物ID: building_1
名称: 高层建筑物
位置: (1000, 1000) NED
高度: 100m AGL
豁免半径: 121.92m (400英尺精确值)
豁免上限: 221.92m (100m + 121.92m)
```

### 坐标系说明

```
NED坐标系 (North-East-Down):
- North: 北向为正
- East: 东向为正
- Down: 向下为正（高度用负值表示，但本场景用AGL正值）

建筑物中心: (1000, 1000)
起点: (2500, 0)
```

---

## 🧪 测试用例

### TC1: 远离建筑物超全局限制

**目的**: 验证豁免区域外应用全局120m限制

**命令**:
```bash
python run_scenario.py \
    S008_structure_waiver.jsonc \
    --output trajectory_S008_TC1.json \
    --mode auto \
    --command "move_to_position(3000, 0, 150)"
```

**参数解析**:
```
目标: (3000, 0, 150m)
距建筑物: sqrt((3000-1000)² + (0-1000)²) = 2236m
豁免判定: 2236m >> 121.92m → 不在豁免区
高度检查: 150m > 120m全局限制 → REJECT
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (structure waiver check)...
   距building_1: 2236.0m (超出豁免半径121.92m)
   豁免不适用，应用全局限制120.0m
   ❌ 目标高度150.0m超过全局限制120.0m（超出30.0m）

🚫 COMMAND REJECTED (altitude limit exceeded)
```

**预期结果**: ❌ **REJECT**

---

### TC2: 建筑物豁免区内合规高度 ⭐

**目的**: 验证豁免条件成功应用，允许超过全局120m限制

**命令**:
```bash
python run_scenario.py \
    S008_structure_waiver.jsonc \
    --output trajectory_S008_TC2.json \
    --mode auto \
    --command "move_to_position(1000, 1100, 150)"
```

**参数解析**:
```
目标: (1000, 1100, 150m)
距建筑物: sqrt((1000-1000)² + (1100-1000)²) = 100m
豁免判定: 100m < 121.92m → 在豁免区内
豁免上限: 100m(建筑) + 121.92m = 221.92m
高度检查: 150m < 221.92m → APPROVE
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (structure waiver check)...
   距building_1: 100.0m (< 121.92m豁免半径)
   豁免适用: building_1 (高100.0m)
   豁免上限: 221.92m (建筑100.0m + 121.92m)
   ✓ 目标高度150.0m符合豁免上限（距上限71.92m）

🔍 Pre-flight check: Target position...
   ✓ Target position is safe

✅ All pre-flight checks passed
✓ Pre-flight check passed, executing movement...
```

**预期结果**: ✅ **APPROVE**（飞行并成功到达）

**关键验证**:
- ⭐ 虽然150m > 120m全局限制，但因为在豁免区内，所以合法
- ✓ 系统正确识别豁免条件并应用豁免上限

---

### TC3: 建筑物豁免区内超豁免上限

**目的**: 验证豁免区内仍有高度上限约束

**命令**:
```bash
python run_scenario.py \
    S008_structure_waiver.jsonc \
    --output trajectory_S008_TC3.json \
    --mode auto \
    --command "move_to_position(1000, 1100, 230)"
```

**参数解析**:
```
目标: (1000, 1100, 230m)
距建筑物: 100m
豁免判定: 在豁免区内
豁免上限: 221.92m
高度检查: 230m > 221.92m → REJECT
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (structure waiver check)...
   距building_1: 100.0m (< 121.92m豁免半径)
   豁免适用: building_1 (高100.0m)
   豁免上限: 221.92m (建筑100.0m + 121.92m)
   ❌ 目标高度230.0m超过豁免上限221.92m（超出8.08m）

🚫 COMMAND REJECTED (structure waiver altitude limit exceeded)
```

**预期结果**: ❌ **REJECT**

**关键验证**:
- ✓ 豁免不是"无限制"，而是"有条件放宽"
- ✓ 正确计算超限幅度（8.08m）

---

### TC4: 豁免半径边界测试 ⭐

**目的**: 验证边界值处理精度（122m vs 121.92m）

**命令**:
```bash
python run_scenario.py \
    S008_structure_waiver.jsonc \
    --output trajectory_S008_TC4.json \
    --mode auto \
    --command "move_to_position(1122, 1000, 150)"
```

**参数解析**:
```
目标: (1122, 1000, 150m)
距建筑物: sqrt((1122-1000)² + (1000-1000)²) = 122m
豁免半径: 121.92m
豁免判定: 122m > 121.92m → 刚好超出 → 豁免不适用
高度检查: 应用全局120m限制 → 150m > 120m → REJECT
```

**预期输出**:
```
🔍 Pre-flight check: Altitude limit (structure waiver check)...
   距building_1: 122.0m (超出豁免半径121.92m，超出0.08m)
   豁免不适用，应用全局限制120.0m
   ❌ 目标高度150.0m超过全局限制120.0m（超出30.0m）

🚫 COMMAND REJECTED (altitude limit exceeded)
```

**预期结果**: ❌ **REJECT**

**关键验证**:
- ⭐ 边界精度：0.08m的差距决定豁免是否适用
- ✓ 边界值处理：`>=` 半径则豁免失效
- ✓ 豁免失效后正确回退到全局限制

---

## 🚀 执行步骤

### 1. 准备环境

**本地**:
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

# 验证场景文件
python scripts/validate_scenario.py scenarios/basic/S008_structure_waiver.jsonc
```

**服务器**:
```bash
# 复制场景文件到服务器
scp -P 10427 scenarios/basic/S008_structure_waiver.jsonc \
    root@connect.westb.seetacloud.com:~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 复制更新的run_scenario.py
scp -P 10427 AirSim-RuleBench/scripts/run_scenario.py \
    root@connect.westb.seetacloud.com:~/project/ProjectAirSim/client/python/example_user_scripts/
```

### 2. 启动ProjectAirSim

**服务器端（专用窗口）**:
```bash
cd ~/linux/
./Blocks.sh -RenderOffScreen -nullrhi
```

### 3. 运行测试

**服务器端（Python窗口）**:
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts
source ~/project/airsim-venv/airsim-venv/bin/activate

# TC1: 远离建筑物超限
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S008_structure_waiver.jsonc \
    --output /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S008_TC1.json \
    --mode auto \
    --command "move_to_position(3000, 0, 150)"

# TC2: 豁免区内合规 ⭐
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S008_structure_waiver.jsonc \
    --output /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S008_TC2.json \
    --mode auto \
    --command "move_to_position(1000, 1100, 150)"

# TC3: 豁免区内超限
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S008_structure_waiver.jsonc \
    --output /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S008_TC3.json \
    --mode auto \
    --command "move_to_position(1000, 1100, 230)"

# TC4: 边界测试 ⭐
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S008_structure_waiver.jsonc \
    --output /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S008_TC4.json \
    --mode auto \
    --command "move_to_position(1122, 1000, 150)"
```

### 4. 下载结果

**本地**:
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs

# 下载所有TC轨迹文件
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S008_TC*.json' \
    .
```

---

## ✅ 验证检查清单

### 预飞行检查输出

每个TC应包含：
- [x] 建筑物距离计算
- [x] 豁免半径判定
- [x] 豁免适用性判断
- [x] 高度上限确定（豁免上限 or 全局上限）
- [x] 明确的APPROVE/REJECT决策

### TC1验证

- [ ] **REJECT**决策
- [ ] 距离正确：~2236m
- [ ] 豁免不适用（超出半径）
- [ ] 应用全局120m限制
- [ ] 拒绝原因包含"超出豁免半径"

### TC2验证 ⭐

- [ ] **APPROVE**决策
- [ ] 距离正确：100m
- [ ] 豁免适用（100m < 121.92m）
- [ ] 应用豁免上限221.92m
- [ ] 成功飞行并到达目标
- [ ] 轨迹文件包含飞行数据

**关键**: 150m > 120m但仍APPROVE！

### TC3验证

- [ ] **REJECT**决策
- [ ] 距离正确：100m
- [ ] 豁免适用判定
- [ ] 超过豁免上限221.92m
- [ ] 超限幅度计算：8.08m

### TC4验证 ⭐

- [ ] **REJECT**决策
- [ ] 距离正确：122m
- [ ] 豁免不适用（122m > 121.92m）
- [ ] 超出半径0.08m被识别
- [ ] 回退到全局120m限制

---

## 📊 预期结果汇总

| TC | 命令 | 距建筑 | 豁免区 | 高度 | 上限 | 预期 | 轨迹点 |
|----|------|--------|--------|------|------|------|--------|
| TC1 | (3000,0,150) | 2236m | ❌ | 150m | 120m | REJECT | 1 |
| TC2 | (1000,1100,150) | 100m | ✅ | 150m | 221.92m | APPROVE | >100 |
| TC3 | (1000,1100,230) | 100m | ✅ | 230m | 221.92m | REJECT | 1 |
| TC4 | (1122,1000,150) | 122m | ❌ | 150m | 120m | REJECT | 1 |

**通过率**: 4/4 (100%)

---

## 🔧 故障排查

### 问题1: 豁免未被识别

**症状**: TC2被REJECT（应为APPROVE）

**排查**:
```bash
# 检查run_scenario.py是否支持structures字段
grep "structures" run_scenario.py

# 检查场景文件是否正确加载
python -c "import json; print(json.load(open('S008_structure_waiver.jsonc'))['structures'])"
```

**解决**: 确保`run_scenario.py`已更新，包含`check_structure_waiver`函数

### 问题2: 距离计算不准确

**症状**: TC4结果与预期不符

**排查**:
```python
# 验证距离计算
import math
dx = 1122 - 1000  # 122
dy = 1000 - 1000  # 0
dist = math.sqrt(dx**2 + dy**2)
print(f"距离: {dist}m")  # 应为122.0

print(f"豁免半径: 121.92m")
print(f"超出: {dist - 121.92}m")  # 应为0.08
```

**解决**: 使用精确的121.92m而非四舍五入的122m

### 问题3: 边界值处理错误

**症状**: TC4被APPROVE（应为REJECT）

**原因**: 可能使用`<`而非`<=`，或浮点数比较误差

**解决**:
```python
# 正确的边界判定
if distance < waiver_radius:  # 严格小于
    waiver_applies = True
else:
    waiver_applies = False
```

---

## 📖 法规参考

### 14 CFR § 107.51(b)

**原文**:
> "The altitude of the small unmanned aircraft cannot be higher than 400 feet above ground level, unless the small unmanned aircraft is flown within a 400-foot radius of a structure and does not fly higher than 400 feet above the structure's immediate uppermost limit."

**关键点**:
1. **条件**: 在建筑物400英尺半径内
2. **豁免**: 可飞至建筑物顶部+400英尺
3. **计算**: 半径为**水平距离**（2D，不含高度）

### 单位转换

```
1 foot = 0.3048 meters (exact)
400 feet = 400 × 0.3048 = 121.92 meters
```

---

## 🎯 成功标准

测试成功的标志：

1. ✅ **TC1**: 正确应用全局限制（豁免区外）
2. ✅ **TC2**: 豁免成功生效（150m合法）⭐
3. ✅ **TC3**: 豁免区内上限约束有效
4. ✅ **TC4**: 边界精度处理正确（0.08m差距）⭐
5. ✅ 所有决策包含明确的建筑物ID和距离信息
6. ✅ 100%测试用例通过

---

**文档版本**: v1.0  
**最后更新**: 2025-10-22  
**作者**: AirSim-RuleBench Team

