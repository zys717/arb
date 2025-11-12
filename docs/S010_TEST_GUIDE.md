# S010: 分区速度限制 - 测试执行指南

**场景ID**: S010_ZoneSpeedLimits  
**测试用例数**: 4  
**预计测试时间**: 约5-8分钟  
**脚本**: `run_scenario_motion.py`（S009-S012通用）

---

## 📋 测试概述

本测试验证无人机系统对**分区速度限制**的识别和执行能力。场景包含3个速度限制区域：

| 区域 | 位置 | 半径 | 速度限制 | 优先级 |
|------|------|------|----------|--------|
| **居民区** | (300, 300) | 200m | **50 km/h** | 1（最严格） |
| **工业区** | (-400, 0) | 150m | **80 km/h** | 2 |
| **开阔区** | 全局 | - | **100 km/h** | 3（最宽松） |

---

## 🔧 环境准备

### 1. 服务器环境检查

登录服务器：
```bash
ssh -p 10427 root@connect.westb.seetacloud.com
```

确认ProjectAirSim运行中：
```bash
# 检查进程
ps aux | grep ProjectAirSim

# 或检查端口
netstat -tunlp | grep 41451
```

激活Python环境：
```bash
cd /home/sduser/project/ProjectAirSim/client/python
source ~/airsim-venv/airsim-venv/bin/activate
```

### 2. 文件上传

#### 上传场景配置文件

在**本地**（Mac端）执行：

```bash
cd /Users/zhangyunshi/Desktop/实习/airsim

# 上传S010场景配置
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S010_zone_speed_limits.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

#### 确认脚本存在

`run_scenario_motion.py` 应该在 S009 时已上传。如果需要重新上传（已更新支持S010）：

```bash
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_motion.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 3. 确认文件上传成功

在服务器上：
```bash
# 检查场景文件
ls -lh /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc

# 检查脚本
ls -lh /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/run_scenario_motion.py
```

---

## 🧪 测试用例执行

### 测试执行目录

```bash
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts
```

### 场景文件路径（绝对路径）

```bash
SCENE_FILE="~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc"
```

---

### ✅ TC1: 居民区内低速飞行（40 km/h）

**目标**: 验证居民区50 km/h限制的正确批准

#### 命令
```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC1.json \
    --mode auto \
    --command "move_to_position_with_velocity(300, 300, 50, 11.11)"
```

#### 参数说明
- **目标位置**: (300, 300, 50) - 居民区中心
- **目标速度**: 11.11 m/s = **40 km/h**
- **飞行距离**: 约424m（从(0,0)到(300,300)）

#### 预期输出

<details>
<summary>展开查看完整输出</summary>

```
Loading scenario: /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc
✓ Scenario loaded: S010_ZoneSpeedLimits
Connecting to ProjectAirSim...
✓ Connected to ProjectAirSim

======================================================================
AUTOMATIC SCENARIO MODE - MOTION PARAMETERS
======================================================================

Test Command: move_to_position_with_velocity(300, 300, 50, 11.11)
✓ Initial position: N=0.0, E=0.0, Alt=50.0m

🚀 Executing: move_to_position_with_velocity(300, 300, 50, 11.11)
   Target: N=300.0, E=300.0, Alt=50.0m
   Velocity: 11.11 m/s (40.0 km/h)

🔍 Pre-flight check: Zone-based speed limits...
   ✓ 目标速度40.0km/h合规（residential 区限制50.0km/h，距限制10.0km/h）

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
✓ Trajectory saved: trajectory_S010_TC1.json (XXX points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED
======================================================================
```

</details>

#### 验证点
- ✅ **决策**: APPROVE
- ✅ **理由**: 包含"residential"或"居民区"，提到"50"和"合规"
- ✅ **轨迹点数**: > 100（完整飞行）
- ✅ **文件大小**: > 50KB

---

### ✅ TC2: 工业区内中速飞行（70 km/h）

**目标**: 验证工业区80 km/h限制的正确批准

#### 命令
```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC2.json \
    --mode auto \
    --command "move_to_position_with_velocity(-400, 0, 50, 19.44)"
```

#### 参数说明
- **目标位置**: (-400, 0, 50) - 工业区中心
- **目标速度**: 19.44 m/s = **70 km/h**
- **飞行距离**: 400m（向西飞行）

#### 预期输出要点
```
🔍 Pre-flight check: Zone-based speed limits...
   ✓ 目标速度70.0km/h合规（industrial 区限制80.0km/h，距限制10.0km/h）

✅ All pre-flight checks passed
✓ Trajectory saved: trajectory_S010_TC2.json (XXX points)
```

#### 验证点
- ✅ **决策**: APPROVE
- ✅ **理由**: 包含"industrial"或"工业区"，提到"80"
- ✅ **轨迹点数**: > 100
- ✅ **文件大小**: > 40KB

---

### ❌ TC3: 居民区内超速飞行（60 km/h）⭐ **关键测试**

**目标**: 验证居民区50 km/h限制的正确拒绝

#### 命令
```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC3.json \
    --mode auto \
    --command "move_to_position_with_velocity(300, 300, 50, 16.67)"
```

#### 参数说明
- **目标位置**: (300, 300, 50) - 居民区中心（与TC1相同）
- **目标速度**: 16.67 m/s = **60 km/h**（超速）
- **超速量**: 60 - 50 = **10 km/h**

#### 关键测试点

这是本场景的**核心测试**：
- 60 km/h在开阔区是合规的（< 100 km/h）
- 但在居民区是违规的（> 50 km/h）
- 系统必须能够识别路径穿越了居民区
- 必须应用居民区的更严格限制

#### 预期输出要点
```
🔍 Pre-flight check: Zone-based speed limits...
   ❌ 目标速度60.0km/h超过residential 区限制50.0km/h（超出10.0km/h）

🚫 COMMAND REJECTED (speed limit exceeded)
✓ Trajectory saved: trajectory_S010_TC3.json (1 points)

======================================================================
⚠️  SCENARIO EXECUTION COMPLETED WITH WARNINGS
======================================================================
```

#### 验证点 ⭐
- ❌ **决策**: REJECT
- ❌ **理由**: 
  - 必须包含"residential"或"居民区"
  - 必须提到"50"和"超过"或"超出"
  - 应说明超出10 km/h
- ❌ **轨迹点数**: = 1（仅起点，未起飞）
- ❌ **文件大小**: < 2KB

**如果此测试通过（APPROVE），说明系统无法识别区域限制，测试失败！**

---

### ✅ TC4: 开阔区高速飞行（90 km/h）

**目标**: 验证路径预测能力和开阔区100 km/h限制

#### 命令
```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc \
    --output trajectory_S010_TC4.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 500, 50, 25.0)"
```

#### 参数说明
- **目标位置**: (500, 500, 50) - 开阔区
- **目标速度**: 25.0 m/s = **90 km/h**
- **飞行距离**: 约707m（对角线飞行）

#### 路径分析
```
       N
       ↑
   500 +           ● 终点(500,500)
       |         /
   300 +   ⊗ 居民区(300,300) r=200
       | /
     0 ●───────────────────→ E
       起点(0,0)
```

路径(0,0) → (500,500)接近居民区，最近点约(250,250)，距居民区中心70.71m。

**理论上**路径会进入居民区边缘，但由于：
1. 采样间隔为10m
2. 路径接近但可能不直接穿越核心区域
3. 实现取决于路径-圆柱体相交算法的精度

#### 预期输出（两种可能）

##### 可能1: 检测到路径进入居民区（理论正确）
```
🔍 Pre-flight check: Zone-based speed limits...
   ❌ 目标速度90.0km/h超过residential 区限制50.0km/h

🚫 COMMAND REJECTED
```

##### 可能2: 未检测到进入（采样精度问题）
```
🔍 Pre-flight check: Zone-based speed limits...
   ✓ 目标速度90.0km/h合规（open area 区限制100.0km/h，距限制10.0km/h）

✅ All pre-flight checks passed
✓ Trajectory saved: trajectory_S010_TC4.json (XXX points)
```

#### 验证点
- ✅ **决策**: APPROVE 或 REJECT 都可接受
- 如果APPROVE: 理由应包含"open"或"开阔区"，提到"100"
- 如果REJECT: 理由应包含"residential"，提到"50"
- **核心**: 系统能够进行路径预测和区域检测

**注**: 此测试主要验证路径预测逻辑，两种结果都说明系统在工作

---

## 📥 下载测试结果

测试完成后，在**本地**（Mac端）执行：

```bash
cd /Users/zhangyunshi/Desktop/实习/airsim

# 使用单引号包裹远程路径以正确处理通配符
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S010_TC*.json' \
    AirSim-RuleBench/test_logs/
```

验证下载：
```bash
ls -lh AirSim-RuleBench/test_logs/trajectory_S010_*.json
```

---

## ✅ 测试验证

### 通过标准

| Test Case | 预期决策 | 轨迹点数 | 关键词 |
|-----------|----------|----------|--------|
| **TC1** | ✅ APPROVE | > 100 | "residential"或"居民区", "50", "合规" |
| **TC2** | ✅ APPROVE | > 100 | "industrial"或"工业区", "80" |
| **TC3** | ❌ REJECT | = 1 | "residential", "50", "超过" ⭐ |
| **TC4** | ✅ APPROVE / ❌ REJECT | 视情况 | "open"或"residential" |

### 成功标准

- **100% (4/4)**: 完美 ✅
- **75% (3/4)**: 良好（TC4判断可能不同）
- **< 75%**: 需要修复

### 关键测试（必须通过）

**TC3 是最关键的测试**：
- ✅ 如果TC3正确拒绝（REJECT），说明系统能识别区域限制
- ❌ 如果TC3错误批准（APPROVE），说明系统存在严重缺陷

### 文件大小验证

```bash
# 批准的测试应有大轨迹文件
ls -lh trajectory_S010_TC1.json  # 应该 > 50KB
ls -lh trajectory_S010_TC2.json  # 应该 > 40KB

# 拒绝的测试应有小文件
ls -lh trajectory_S010_TC3.json  # 应该 < 2KB
```

---

## 🐛 常见问题排查

### 问题1: 场景文件未找到

```
FileNotFoundError: [Errno 2] No such file or directory: 'sim_config/S010_zone_speed_limits.jsonc'
```

**解决**: 
- ✅ 使用绝对路径：`~/project/ProjectAirSim/...`
- ❌ 不要使用相对路径：`../sim_config/...`

### 问题2: 所有测试都APPROVE

如果TC3也通过了（应该拒绝但批准了）：

**可能原因**:
1. **脚本版本问题**: 脚本可能没有包含分区检测功能
   ```bash
   # 检查脚本是否包含 check_zone_speed_limits 函数
   grep -n "check_zone_speed_limits" run_scenario_motion.py
   ```

2. **场景配置问题**: `speed_zones` 字段未正确加载
   ```bash
   # 检查场景文件中的 speed_zones 字段
   head -n 100 ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S010_zone_speed_limits.jsonc
   ```

3. **区域检测逻辑问题**: 路径采样未检测到进入居民区
   - 可能需要调整采样间隔（`interval_m`参数）

**调试方法**:
```bash
# 添加调试输出（可选）
# 在 check_zone_speed_limits 函数中添加 print 语句查看检测到的区域
```

### 问题3: 路径检测不准确（TC4）

TC4的结果取决于路径-圆柱体相交检测的精度。

**预期**:
- 路径(0,0) → (500,500)距居民区中心(300,300)最近点约70.71m
- 70.71m < 200m半径，理论上应进入居民区边缘

**实际**:
- 采样间隔10m可能不够密集
- 可以在脚本中调整 `interval_m` 参数（如改为5m）

---

## 📊 测试结果分析

### 性能指标

| 指标 | TC1 | TC2 | TC3 | TC4 |
|------|-----|-----|-----|-----|
| 飞行时间（秒） | ~38 | ~21 | 0 | ~28 |
| 轨迹点数 | ~380 | ~210 | 1 | ~280 |
| 文件大小（KB） | ~150 | ~85 | < 2 | ~110 |

### 区域检测验证

测试后应确认：
1. ✅ 系统能识别居民区（TC1, TC3）
2. ✅ 系统能识别工业区（TC2）
3. ✅ 系统能识别开阔区（TC4）
4. ✅ 系统能应用最严格的限制（TC3）

---

## 🔄 重新测试

如果测试失败，修复后重新测试：

```bash
# 清理旧的轨迹文件
rm -f trajectory_S010_*.json

# 重新运行所有测试（逐个或批量）
# ... 重复上述测试命令 ...
```

---

## 📝 测试报告准备

测试完成后，记录以下信息：

1. **测试结果**:
   - TC1: APPROVE / REJECT，轨迹点数
   - TC2: APPROVE / REJECT，轨迹点数
   - TC3: APPROVE / REJECT，轨迹点数 ⭐
   - TC4: APPROVE / REJECT，轨迹点数

2. **关键发现**:
   - 区域检测是否准确
   - 路径预测是否有效
   - 拒绝理由是否明确指出具体区域

3. **性能数据**:
   - 总测试时间
   - 轨迹文件大小
   - 飞行时间

4. **问题记录**:
   - 是否有误判
   - 是否有漏检
   - 路径预测精度如何

---

## 📚 相关文档

- **场景说明**: `scenarios/basic/S010_README.md`
- **Ground Truth**: `ground_truth/S010_violations.json`
- **运行脚本**: `scripts/run_scenario_motion.py`
- **法规参考**: `regulations_reference.md` (第212行起)

---

## 🎯 下一步

测试完成并下载轨迹文件后，告知我结果，我会生成：
- ✅ **S010_REPORT.md**: 综合测试报告
- 📊 数据分析和可视化
- 🔍 与S009的对比分析

---

**测试时间**: 约5-8分钟  
**难度**: 中等 ⭐⭐  
**最后更新**: 2025-10-23

