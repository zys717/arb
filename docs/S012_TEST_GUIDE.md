# S012 时间窗口限制 - 测试执行指南

**场景ID**: S012_TimeWindow  
**测试日期**: 2025-10-31  
**测试人员**: Claude & 张耘实  
**预计时间**: ~8分钟（5个测试用例）

---

## 📋 测试前准备

### 1. 文件准备

需要上传的文件：
- ✅ `scenarios/basic/S012_time_window.jsonc` - 场景配置
- ✅ `scripts/run_scenario_motion.py` - 测试脚本（已更新支持时间窗口检查）

### 2. 上传文件到服务器

```bash
# 在本地执行（当前目录：/Users/zhangyunshi/Desktop/实习/airsim/）

# 1. 上传场景配置文件
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S012_time_window.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. 上传更新的测试脚本
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scripts/run_scenario_motion.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

**预期输出**:
```
S012_time_window.jsonc                 100%   12KB   1.2MB/s   00:00
run_scenario_motion.py                 100%   40KB   2.8MB/s   00:00
```

### 3. SSH连接到服务器

```bash
ssh -p 10427 root@connect.westb.seetacloud.com
```

### 4. 进入工作目录

```bash
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts
```

---

## 🧪 测试用例执行

### 测试概览

| TC | 时间 | 位置 | 时间窗口 | 医院内 | 预期 | 测试重点 |
|----|------|------|----------|--------|------|----------|
| TC1 | 14:00 | (0,200) | ❌ | ❌ | ✅ APPROVE | 基础合规 |
| TC2 | 14:00 | (200,0) | ❌ | ✅ | ✅ APPROVE | 单条件（zone）⭐ |
| TC3 | 23:00 | (0,200) | ✅ | ❌ | ✅ APPROVE | 单条件（time）⭐ |
| TC4 | 23:00 | (200,0) | ✅ | ✅ | ❌ REJECT | AND逻辑 ⭐⭐ |
| TC5 | 22:00 | (200,0) | ✅ | ✅ | ❌ REJECT | 边界值 ⭐ |

**关键测试**: TC2/TC3（单条件不拒绝）+ TC4（双条件拒绝）

---

## 📝 详细测试步骤

### TC1: 白天医院外✅ APPROVE

**测试目标**: 验证基础合规性（不满足任何限制条件）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S012_time_window.jsonc \
    --output trajectory_S012_TC1.json \
    --mode auto \
    --test-case TC1
```

**预期输出**:
```
Time of Day: 14:00
Target: N=0.0, E=200.0, Alt=50.0m

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

---

### TC2: 白天医院内✅ APPROVE ⭐ 关键测试

**测试目标**: 验证单条件不触发拒绝（仅在医院内，但不在禁飞时段）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S012_time_window.jsonc \
    --output trajectory_S012_TC2.json \
    --mode auto \
    --test-case TC2
```

**预期输出**:
```
Time of Day: 14:00
Target: N=200.0, E=0.0, Alt=50.0m - 医院中心

🔍 Pre-flight check: Time window restrictions...
   ✓ 通过时间窗口检查

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**关键验证**:
- ✅ 虽然在医院区域内（满足空间条件）
- ✅ 但不在禁飞时段（不满足时间条件）
- ✅ AND逻辑：必须两个条件同时满足才拒绝
- ✅ 单条件不触发拒绝 → 批准 ✅

---

### TC3: 夜间医院外✅ APPROVE ⭐ 关键测试

**测试目标**: 验证单条件不触发拒绝（仅在禁飞时段，但不在医院内）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S012_time_window.jsonc \
    --output trajectory_S012_TC3.json \
    --mode auto \
    --test-case TC3
```

**预期输出**:
```
Time of Day: 23:00
Target: N=0.0, E=200.0, Alt=50.0m

🔍 Pre-flight check: Time window restrictions...
   ✓ 通过时间窗口检查

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**关键验证**:
- ✅ 虽然在禁飞时段（满足时间条件）
- ✅ 但不在医院区域（不满足空间条件）
- ✅ AND逻辑：必须两个条件同时满足才拒绝
- ✅ 单条件不触发拒绝 → 批准 ✅

---

### TC4: 夜间医院内❌ REJECT ⭐⭐ 核心测试

**测试目标**: 验证AND逻辑（同时满足时间+空间条件才拒绝）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S012_time_window.jsonc \
    --output trajectory_S012_TC4.json \
    --mode auto \
    --test-case TC4
```

**预期输出**:
```
Time of Day: 23:00
Target: N=200.0, E=0.0, Alt=50.0m - 医院中心

🔍 Pre-flight check: Time window restrictions...
   ❌ 22:00-06:00禁飞时段，禁止在hospital zone内飞行（减少噪音干扰，保障患者休息）

🚫 COMMAND REJECTED (time window restriction)
✓ Trajectory saved: trajectory_S012_TC4.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ 在禁飞时段（满足时间条件）
- ✅ 在医院区域（满足空间条件）
- ✅ AND逻辑：两个条件同时满足 → 拒绝 ✅
- ✅ 拒绝理由清晰，说明时间窗口和区域
- ✅ 仅记录起点（未起飞）

**这是最核心的测试**：证明AND组合逻辑正确实现

---

### TC5: 边界值（22:00）医院内❌ REJECT ⭐

**测试目标**: 验证边界值处理（22:00禁飞开始时刻）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S012_time_window.jsonc \
    --output trajectory_S012_TC5.json \
    --mode auto \
    --test-case TC5
```

**预期输出**:
```
Time of Day: 22:00
Target: N=200.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: Time window restrictions...
   ❌ 22:00-06:00禁飞时段，禁止在hospital zone内飞行（减少噪音干扰，保障患者休息）

🚫 COMMAND REJECTED (time window restriction)
✓ Trajectory saved: trajectory_S012_TC5.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ 22:00 >= 22:00 → 禁飞开始
- ✅ 在医院内
- ✅ 两个条件同时满足 → 拒绝
- ✅ 边界值处理正确

---

## 📦 下载测试结果

```bash
# 在本地执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S012_TC*.json' \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/
```

**注意**: 必须用单引号包裹远程路径。

---

## ✅ 验证清单

### 1. 文件检查

```bash
# 在本地执行
ls -lh /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S012_TC*.json
```

**预期结果**:
```
trajectory_S012_TC1.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S012_TC2.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S012_TC3.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S012_TC4.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S012_TC5.json    ~1KB     ❌ 拒绝，仅起点
```

**批准/拒绝分布**:
- ✅ APPROVE: 3个 (TC1, TC2, TC3)
- ❌ REJECT: 2个 (TC4, TC5)

### 2. 快速验证命令

```bash
# 检查文件大小
wc -l /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S012_TC*.json
```

**预期**:
- TC1/TC2/TC3: 大文件（~600-700行）
- TC4/TC5: 小文件（~36行）

### 3. 关键测试验证

#### TC2 - 单条件测试（仅zone）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S012_TC2.json | head -20
```
**必须**:
- ✅ `"success": true`
- ✅ 完整轨迹（~600点）

#### TC3 - 单条件测试（仅time）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S012_TC3.json | head -20
```
**必须**:
- ✅ `"success": true`
- ✅ 完整轨迹（~600点）

#### TC4 - AND逻辑测试（核心）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S012_TC4.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"reason": "Time window restriction"`
- `"violations": ["22:00-06:00禁飞时段"]`
- `"trajectory_points": 1`

---

## 🎯 成功标准

### 必须全部通过

1. ✅ **TC1**: 白天医院外批准
2. ✅ **TC2**: 白天医院内批准（单条件不拒绝）⭐
3. ✅ **TC3**: 夜间医院外批准（单条件不拒绝）⭐
4. ✅ **TC4**: 夜间医院内拒绝（AND逻辑）⭐⭐
5. ✅ **TC5**: 边界值22:00拒绝

### AND逻辑真值表验证

| 时间窗口 | 医院内 | 预期 | 测试用例 |
|----------|--------|------|----------|
| ❌ | ❌ | ✅ APPROVE | TC1 |
| ❌ | ✅ | ✅ APPROVE | TC2 ⭐ |
| ✅ | ❌ | ✅ APPROVE | TC3 ⭐ |
| ✅ | ✅ | ❌ REJECT | TC4 ⭐⭐ |

**如果TC2或TC3被拒绝**，说明AND逻辑实现错误！

---

## ⚠️ 常见问题

### 问题1: TC2或TC3被错误拒绝

**原因**: AND逻辑实现错误，可能使用了OR逻辑

**排查**:
```python
# 错误实现（OR逻辑）
if is_in_time_window or is_in_zone:
    REJECT

# 正确实现（AND逻辑）
if is_in_time_window and is_in_zone:
    REJECT
```

### 问题2: TC4被错误批准

**原因**: 
1. 时间窗口判断错误
2. 区域检测错误
3. AND逻辑未触发

**排查**:
- 检查23:00是否在22:00-06:00时间窗口内
- 检查(200,0)是否在医院区域内（半径150m）
- 检查AND条件是否同时满足

### 问题3: 找不到time_window_zones配置

**原因**: 场景文件未包含`time_restricted_zones`字段

**解决**: 确保场景文件上传成功且包含完整配置

---

## 📊 预期测试时长

- 每个测试用例: ~1-2分钟
- 总计5个用例: ~5-10分钟
- 文件上传/下载: ~2分钟
- 结果验证: ~2分钟

**总时长**: ~10-15分钟

---

## 📝 测试注意事项

1. ⚡ **AND逻辑关键**: 必须同时满足时间+空间才拒绝
2. 🎯 **单条件处理**: TC2和TC3最关键，单条件不应拒绝
3. 🏥 **医院区域**: 中心(200,0)，半径150m
4. ⏰ **禁飞时段**: 22:00-06:00（跨越午夜）
5. 🔄 **代码复用**: 时间判断复用S011，区域检测复用S002/S010

---

## 🔗 相关场景

- **S011**: 夜间飞行规则（时间判断基础）
- **S002**: 多地理围栏（区域检测基础）
- **S010**: 分区速度限制（空间+规则组合）

---

**测试指南版本**: 1.0  
**最后更新**: 2025-10-31  
**适用脚本**: run_scenario_motion.py v1.3（新增时间窗口检查）  
**测试用例数**: 5个（比S011的8个少，重点测试AND逻辑）

