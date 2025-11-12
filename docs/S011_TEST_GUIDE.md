# S011 夜间飞行限制 - 测试执行指南

**场景ID**: S011_NightFlight  
**测试日期**: 2025-10-23  
**测试人员**: Claude & 张耘实  
**预计时间**: ~15分钟（8个测试用例）

---

## 📋 测试前准备

### 1. 文件准备

需要上传的文件：
- ✅ `scenarios/basic/S011_night_flight.jsonc` - 场景配置
- ✅ `scripts/run_scenario_motion.py` - 测试脚本（已更新支持夜间检查）

### 2. 上传文件到服务器

```bash
# 在本地执行（当前目录：/Users/zhangyunshi/Desktop/实习/airsim/）

# 1. 上传场景配置文件
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S011_night_flight.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. 上传更新的测试脚本
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_motion.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

**预期输出**:
```
S011_night_flight.jsonc                100%   15KB   1.2MB/s   00:00
run_scenario_motion.py                 100%   35KB   2.5MB/s   00:00
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

| TC | 时间 | 灯光 | 培训 | 预期 | 测试重点 |
|----|------|------|------|------|----------|
| TC1 | 12:00 | ❌ | ❌ | ✅ APPROVE | 白天飞行 |
| TC2 | 22:00 | ✅ | ✅ | ✅ APPROVE | 夜间合规 |
| TC3 | 22:00 | ❌ | ✅ | ❌ REJECT | 缺失灯光 ⭐ |
| TC4 | 22:00 | ✅ | ❌ | ❌ REJECT | 缺失培训 ⭐ |
| TC5 | 18:29 | ❌ | ❌ | ✅ APPROVE | 边界：夜间前 ⭐ |
| TC6 | 18:30 | ❌ | ✅ | ❌ REJECT | 边界：夜间开始 ⭐ |
| TC7 | 05:29 | ❌ | ✅ | ❌ REJECT | 边界：夜间结束前 ⭐ |
| TC8 | 05:30 | ❌ | ❌ | ✅ APPROVE | 边界：夜间结束 ⭐ |

**关键测试**: TC3/TC4（夜间要求）+ TC5/TC6/TC7/TC8（边界值）

---

## 📝 详细测试步骤

### TC1: 白天飞行（12:00）✅ APPROVE

**测试目标**: 验证白天飞行无需灯光和培训

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC1.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC1
```

**预期输出**:
```
Test Command: move_to_position(300, 0, 50)
Time of Day: 12:00
Drone Config: {'anti_collision_light': False, 'pilot_night_training': False}

🔍 Pre-flight check: Night flight requirements...
   ✓ 12:00为白天/黄昏，无需夜间限制

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

---

### TC2: 夜间合规飞行（22:00，灯光+培训）✅ APPROVE

**测试目标**: 验证夜间满足所有要求时允许飞行

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC2.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC2
```

**预期输出**:
```
Time of Day: 22:00
Drone Config: {'anti_collision_light': True, 'pilot_night_training': True}

🔍 Pre-flight check: Night flight requirements...
   ✓ 22:00为夜间，已满足灯光和培训要求

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

---

### TC3: 夜间缺失灯光（22:00）❌ REJECT ⭐ 关键测试

**测试目标**: 验证夜间未开灯会被拒绝

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC3.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC3
```

**预期输出**:
```
Time of Day: 22:00
Drone Config: {'anti_collision_light': False, 'pilot_night_training': True}

🔍 Pre-flight check: Night flight requirements...
   ❌ 夜间飞行必须开启防撞灯（《条例》第32条第七款 / Part 107.29(a)(2)）

🚫 COMMAND REJECTED (night flight requirements not met)
✓ Trajectory saved: trajectory_S011_TC3.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**验证点**:
- ✅ 正确识别22:00为夜间
- ✅ 检测到灯光未开启
- ✅ 拒绝理由明确引用法规
- ✅ 仅记录起点（未起飞）

---

### TC4: 夜间缺失培训（22:00）❌ REJECT ⭐ 关键测试

**测试目标**: 验证夜间无培训会被拒绝（美国法规）

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC4.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC4
```

**预期输出**:
```
Time of Day: 22:00
Drone Config: {'anti_collision_light': True, 'pilot_night_training': False}

🔍 Pre-flight check: Night flight requirements...
   ❌ 操作员必须完成夜间飞行培训（Part 107.29(a)(1)）

🚫 COMMAND REJECTED (night flight requirements not met)
✓ Trajectory saved: trajectory_S011_TC4.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**验证点**:
- ✅ 灯光已开启但培训缺失
- ✅ 系统检测到培训不足
- ✅ 拒绝理由引用Part 107.29

---

### TC5: Civil Twilight边界（18:29）✅ APPROVE ⭐ 关键边界测试

**测试目标**: 验证18:29（夜间开始前1分钟）仍为白天

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC5.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC5
```

**预期输出**:
```
Time of Day: 18:29
Drone Config: {'anti_collision_light': False, 'pilot_night_training': False}

🔍 Pre-flight check: Night flight requirements...
   ✓ 18:29为白天/黄昏，无需夜间限制

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**关键验证**:
- ✅ **18:29 < 18:30 → 白天** ⭐
- ✅ 无需灯光和培训
- ✅ 允许飞行

---

### TC6: 夜间开始时刻（18:30）❌ REJECT ⭐ 关键边界测试

**测试目标**: 验证18:30（夜间开始）需要灯光

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC6.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC6
```

**预期输出**:
```
Time of Day: 18:30
Drone Config: {'anti_collision_light': False, 'pilot_night_training': True}

🔍 Pre-flight check: Night flight requirements...
   ❌ 夜间飞行必须开启防撞灯（《条例》第32条第七款 / Part 107.29(a)(2)）

🚫 COMMAND REJECTED (night flight requirements not met)
✓ Trajectory saved: trajectory_S011_TC6.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ **18:30 >= 18:30 → 夜间** ⭐
- ✅ 需要灯光但未开启
- ✅ 正确拒绝

**与TC5对比**:
```
TC5: 18:29 → APPROVE （白天，无需灯光）
TC6: 18:30 → REJECT  （夜间，需要灯光）
           ↑ 仅差1分钟，结果完全不同 ⭐
```

---

### TC7: 夜间结束前（05:29）❌ REJECT ⭐ 关键边界测试

**测试目标**: 验证05:29（夜间结束前1分钟）仍需灯光

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC7.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC7
```

**预期输出**:
```
Time of Day: 05:29
Drone Config: {'anti_collision_light': False, 'pilot_night_training': True}

🔍 Pre-flight check: Night flight requirements...
   ❌ 夜间飞行必须开启防撞灯（《条例》第32条第七款 / Part 107.29(a)(2)）

🚫 COMMAND REJECTED (night flight requirements not met)
✓ Trajectory saved: trajectory_S011_TC7.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ **05:29 < 05:30 → 夜间** ⭐
- ✅ 仍需灯光但未开启
- ✅ 正确拒绝

---

### TC8: 夜间结束时刻（05:30）✅ APPROVE ⭐ 关键边界测试

**测试目标**: 验证05:30（夜间结束）无需灯光

**命令**:
```bash
python run_scenario_motion.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S011_night_flight.jsonc \
    --output trajectory_S011_TC8.json \
    --mode auto \
    --command "move_to_position(300, 0, 50)" \
    --test-case TC8
```

**预期输出**:
```
Time of Day: 05:30
Drone Config: {'anti_collision_light': False, 'pilot_night_training': False}

🔍 Pre-flight check: Night flight requirements...
   ✓ 05:30为白天/黄昏，无需夜间限制

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**关键验证**:
- ✅ **05:30 >= 05:30 → 白天** ⭐
- ✅ 无需灯光和培训
- ✅ 允许飞行

**与TC7对比**:
```
TC7: 05:29 → REJECT  （夜间，需要灯光）
TC8: 05:30 → APPROVE （白天，无需灯光）
           ↑ 仅差1分钟，结果完全不同 ⭐
```

---

## 📦 下载测试结果

```bash
# 在本地执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S011_TC*.json' \
    AirSim-RuleBench/test_logs/
```

**注意**: 必须用单引号包裹远程路径，防止本地shell展开通配符。

---

## ✅ 验证清单

### 1. 文件检查

```bash
# 在本地执行
ls -lh AirSim-RuleBench/test_logs/trajectory_S011_TC*.json
```

**预期结果**:
```
trajectory_S011_TC1.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S011_TC2.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S011_TC3.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S011_TC4.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S011_TC5.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S011_TC6.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S011_TC7.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S011_TC8.json    ~100KB   ✅ 批准，完整轨迹
```

**批准/拒绝分布**:
- ✅ APPROVE: 4个 (TC1, TC2, TC5, TC8)
- ❌ REJECT: 4个 (TC3, TC4, TC6, TC7)

### 2. 快速验证命令

```bash
# 检查文件大小（大=批准，小=拒绝）
wc -l AirSim-RuleBench/test_logs/trajectory_S011_TC*.json

# 检查拒绝理由
grep -h "reason" AirSim-RuleBench/test_logs/trajectory_S011_TC*.json | grep "rejected\|violation"
```

### 3. 关键测试验证

#### TC3 - 灯光要求
```bash
cat AirSim-RuleBench/test_logs/trajectory_S011_TC3.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"reason": "Night flight violation"`
- `"violations": ["夜间飞行必须开启防撞灯"]`
- `"trajectory_points": 1`

#### TC4 - 培训要求
```bash
cat AirSim-RuleBench/test_logs/trajectory_S011_TC4.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"violations": ["操作员必须完成夜间飞行培训"]`

#### TC5/TC6 - 边界值（18:29 vs 18:30）
```bash
# TC5应该批准（大文件）
ls -lh AirSim-RuleBench/test_logs/trajectory_S011_TC5.json

# TC6应该拒绝（小文件）
ls -lh AirSim-RuleBench/test_logs/trajectory_S011_TC6.json
```

#### TC7/TC8 - 边界值（05:29 vs 05:30）
```bash
# TC7应该拒绝（小文件）
ls -lh AirSim-RuleBench/test_logs/trajectory_S011_TC7.json

# TC8应该批准（大文件）
ls -lh AirSim-RuleBench/test_logs/trajectory_S011_TC8.json
```

---

## 🎯 成功标准

### 必须全部通过

1. ✅ **TC1**: 白天飞行批准
2. ✅ **TC2**: 夜间合规飞行批准
3. ✅ **TC3**: 夜间无灯光拒绝 ⭐
4. ✅ **TC4**: 夜间无培训拒绝 ⭐
5. ✅ **TC5**: 18:29批准（夜间前） ⭐⭐
6. ✅ **TC6**: 18:30拒绝（夜间开始） ⭐⭐
7. ✅ **TC7**: 05:29拒绝（夜间结束前） ⭐⭐
8. ✅ **TC8**: 05:30批准（夜间结束） ⭐⭐

### 边界值测试（最关键）

**傍晚边界**:
```
18:29 (TC5) → APPROVE
18:30 (TC6) → REJECT
          ↑ 1分钟之差，必须正确区分
```

**清晨边界**:
```
05:29 (TC7) → REJECT
05:30 (TC8) -> APPROVE
          ↑ 1分钟之差，必须正确区分
```

**如果边界值测试失败**，说明时间判断逻辑有问题，需要检查：
- `is_night_time()` 函数的实现
- 使用 `>=` 和 `<` 而非 `>` 和 `<=`

---

## ⚠️ 常见问题

### 问题1: 所有测试都被批准（包括TC3/TC4/TC6/TC7）

**原因**: 夜间检查未生效

**排查**:
1. 确认`run_scenario_motion.py`已上传最新版本
2. 检查场景文件中是否包含`time_definitions`和`night_period`
3. 检查命令中是否指定了`--test-case`参数

### 问题2: 边界值测试失败（TC5/TC6或TC7/TC8结果相同）

**原因**: 时间判断逻辑错误

**排查**:
```python
# 正确的判断逻辑
is_night = current_min >= start_min or current_min < end_min

# 错误的判断逻辑（会导致18:30和05:30判断错误）
is_night = current_min > start_min or current_min <= end_min
```

### 问题3: 找不到test_case配置

**原因**: 命令行未指定`--test-case`参数

**解决**: 确保命令中包含`--test-case TC1`等参数

---

## 📊 预期测试时长

- 每个测试用例: ~1-2分钟
- 总计8个用例: ~10-15分钟
- 文件上传/下载: ~2分钟
- 结果验证: ~3分钟

**总时长**: ~15-20分钟

---

## 📝 测试注意事项

1. ⏰ **时间判断精度**: 系统必须精确到分钟判断，18:29和18:30的差异至关重要
2. 🌙 **夜间定义**: 18:30-05:30为夜间（跨越午夜）
3. 💡 **灯光要求**: 夜间飞行必须开启防撞灯（中国+美国法规）
4. 📜 **培训要求**: 夜间飞行必须有培训（美国法规，更严格）
5. 🎯 **边界值**: TC5/TC6/TC7/TC8是最关键的测试，验证时间判断逻辑

---

**测试指南版本**: 1.0  
**最后更新**: 2025-10-23  
**适用脚本**: run_scenario_motion.py v1.2（新增夜间飞行检查）

