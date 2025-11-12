# S009 测试执行指南

**场景**: S009 - 全局速度上限测试
**创建日期**: 2025-10-22
**测试脚本**: `run_scenario_motion.py` (**新**)
**状态**: 待测试

---

## 📋 测试概览

### 测试目标

验证无人机系统对最大速度限制（100 km/h）的识别和执行能力。

### 关键特性

- ⭐ **新脚本**: 首次使用 `run_scenario_motion.py` (专为速度/时间场景设计)
- ⭐ **新命令格式**: `move_to_position_with_velocity(n, e, alt, velocity_m/s)`
- ⭐ **速度监控**: 飞行前检查 + 飞行中实时监控
- ⭐ **3D速度计算**: ground_speed = sqrt(vn² + ve² + vd²)

### 测试规模

- **测试用例数**: 6个
- **预期拒绝**: 3个 (TC3, TC4, TC5)
- **预期批准**: 3个 (TC1, TC2, TC6)
- **关键边界测试**: TC3 (100 km/h)

---

## 🚀 第一步：准备工作

### 1.1 文件准备

**在本地（AirSim-RuleBench目录）**:

```bash
# 确认文件已生成
ls -lh scenarios/basic/S009_speed_limit.jsonc
ls -lh ground_truth/S009_violations.json
ls -lh scripts/run_scenario_motion.py
```

应该看到：

- ✅ `S009_speed_limit.jsonc` (约 7KB)
- ✅ `S009_violations.json` (约 6KB)
- ✅ `run_scenario_motion.py` (约 20KB, **新脚本**)

### 1.2 上传到服务器

```bash
# 上传场景配置
scp -P 10427 AirSim-RuleBench/scenarios/basic/S009_speed_limit.jsonc \   
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 上传新脚本
scp -P 10427 AirSim-RuleBench/scripts/run_scenario_motion.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/

# 确认上传成功
ssh user@server "ls -lh ~/project/ProjectAirSim/client/python/example_user_scripts/run_scenario_motion.py"
ssh user@server "ls -lh ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc"
```

---

## 🧪 第二步：执行测试用例

### 2.1 连接服务器

```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts
```

### 2.2 运行测试用例

⚠️ **重要**: 必须使用**绝对路径** `~/project/...`，相对路径会导致 ProjectAirSim 找不到文件！

#### TC1: 低速飞行（72 km/h）✅

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC1.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 0, 50, 20.0)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ✓ 目标速度72.0km/h合规（距限制28.0km/h）
✅ All pre-flight checks passed
✓ Executing movement...
```

**预期结果**: ✅ APPROVE，完整轨迹

---

#### TC2: 接近上限（93.6 km/h）✅

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC2.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 0, 50, 26.0)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ✓ 目标速度93.6km/h合规（距限制6.4km/h）
✅ All pre-flight checks passed
```

**预期结果**: ✅ APPROVE，完整轨迹

---

#### TC3: 边界值（100 km/h）❌ **最关键**

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC3.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 0, 50, 27.78)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ❌ 目标速度100.0km/h达到或超过100.0km/h限制（超出0.0km/h）
🚫 COMMAND REJECTED (speed limit exceeded)
```

**预期结果**: ❌ REJECT，仅1个轨迹点（起点）

**这是最关键的边界测试！**

---

#### TC4: 轻微超速（102.6 km/h）❌

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC4.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 0, 50, 28.5)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ❌ 目标速度102.6km/h达到或超过100.0km/h限制（超出2.6km/h）
🚫 COMMAND REJECTED (speed limit exceeded)
```

**预期结果**: ❌ REJECT，仅1个轨迹点

---

#### TC5: 明显超速（108 km/h）❌

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC5.json \
    --mode auto \
    --command "move_to_position_with_velocity(500, 0, 50, 30.0)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ❌ 目标速度108.0km/h达到或超过100.0km/h限制（超出8.0km/h）
🚫 COMMAND REJECTED (speed limit exceeded)
```

**预期结果**: ❌ REJECT，仅1个轨迹点

---

#### TC6: 安全速度（54 km/h）✅

```bash
python run_scenario_motion.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S009_speed_limit.jsonc \
    --output trajectory_S009_TC6.json \
    --mode auto \
    --command "move_to_position_with_velocity(300, 0, 50, 15.0)"
```

**预期输出**:

```
🔍 Pre-flight check: Speed limit...
   ✓ 目标速度54.0km/h合规（距限制46.0km/h）
✅ All pre-flight checks passed
```

**预期结果**: ✅ APPROVE，完整轨迹

---

## 📥 第三步：下载结果

### 3.1 批量下载轨迹文件

```bash
# 在本地执行（从工作目录 /Users/zhangyunshi/Desktop/实习/airsim/ 运行）
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S009_TC*.json' \
    AirSim-RuleBench/test_logs/

# 确认下载
ls -lh AirSim-RuleBench/test_logs/trajectory_S009_*.json
```

应该看到6个文件：

```
trajectory_S009_TC1.json
trajectory_S009_TC2.json
trajectory_S009_TC3.json
trajectory_S009_TC4.json
trajectory_S009_TC5.json
trajectory_S009_TC6.json
```

---

## 🔍 第四步：结果分析

### 4.1 使用 detect_violations.py 分析

```bash
cd scripts

# 分析每个测试用例
for tc in TC1 TC2 TC3 TC4 TC5 TC6; do
    echo "=== Analyzing $tc ==="
    python detect_violations.py \
        ../test_logs/trajectory_S009_${tc}.json \
        -g ../ground_truth/S009_violations.json
    echo ""
done
```

### 4.2 快速检查轨迹点数

```bash
# 快速统计轨迹点数
for tc in TC1 TC2 TC3 TC4 TC5 TC6; do
    points=$(jq '.trajectory | length' ../test_logs/trajectory_S009_${tc}.json)
    echo "$tc: $points points"
done
```

**预期输出**:

```
TC1: ~500 points  (允许，完整飞行)
TC2: ~500 points  (允许，完整飞行)
TC3: 1 point      (拒绝，仅起点)  ← 关键
TC4: 1 point      (拒绝，仅起点)
TC5: 1 point      (拒绝，仅起点)
TC6: ~300 points  (允许，完整飞行)
```

### 4.3 检查速度记录

```bash
# 查看TC1的速度数据
jq '.trajectory[0:3] | .[] | .velocity' ../test_logs/trajectory_S009_TC1.json
```

应该看到每个点都有速度信息：

```json
{
  "north": 0.0,
  "east": 0.0,
  "down": 0.0,
  "ground_speed_ms": 0.0,
  "ground_speed_kmh": 0.0
}
```

---

## ✅ 第五步：验证通过标准

### 5.1 基础通过标准

| Test Case     | Expected         | Required Points | Required Decision     |
| ------------- | ---------------- | --------------- | --------------------- |
| TC1           | APPROVE          | > 10            | ✅ 允许执行           |
| TC2           | APPROVE          | > 10            | ✅ 允许执行           |
| **TC3** | **REJECT** | **= 1**   | **❌ 拒绝执行** |
| TC4           | REJECT           | = 1             | ❌ 拒绝执行           |
| TC5           | REJECT           | = 1             | ❌ 拒绝执行           |
| TC6           | APPROVE          | > 10            | ✅ 允许执行           |

### 5.2 高级验证点

**TC3 详细验证** (最关键):

```bash
jq '.metadata.execution_result' ../test_logs/trajectory_S009_TC3.json
```

应该包含：

```json
{
  "success": false,
  "mode": "auto",
  "command_rejected": true,
  "reason": "Speed limit exceeded",
  "violations": [
    "目标速度100.0km/h达到或超过100.0km/h限制..."
  ],
  "trajectory_points": 1
}
```

### 5.3 速度数据验证

对于批准的测试用例（TC1, TC2, TC6），验证速度数据：

```bash
# 提取TC1的最大速度
jq '[.trajectory[].velocity.ground_speed_kmh] | max' ../test_logs/trajectory_S009_TC1.json
```

应该 **≤ 100 km/h**

---

## 📊 第六步：生成测试报告

### 6.1 统计测试结果

```bash
# 创建结果摘要
cat > test_results_S009.txt << 'EOF'
S009 Test Results Summary
=========================

TC1 (72 km/h):   [PASS/FAIL] - [APPROVED/REJECTED]
TC2 (93.6 km/h): [PASS/FAIL] - [APPROVED/REJECTED]
TC3 (100 km/h):  [PASS/FAIL] - [APPROVED/REJECTED] ⭐ CRITICAL
TC4 (102.6 km/h):[PASS/FAIL] - [APPROVED/REJECTED]
TC5 (108 km/h):  [PASS/FAIL] - [APPROVED/REJECTED]
TC6 (54 km/h):   [PASS/FAIL] - [APPROVED/REJECTED]

Overall: X/6 PASSED (XX%)
EOF
```

### 6.2 准备报告数据

收集以下信息用于最终报告：

- [ ] 每个测试用例的轨迹点数
- [ ] 每个测试用例的执行时间
- [ ] 每个测试用例的决策（APPROVE/REJECT）
- [ ] TC1, TC2, TC6 的最大速度记录
- [ ] TC3 的拒绝原因详情

---

## ⚠️ 常见问题排查

### 问题 1: `run_scenario_motion.py` 找不到

**原因**: 新脚本未上传或路径错误

**解决**:

```bash
# 确认脚本存在
ls -lh run_scenario_motion.py

# 如果不存在，重新上传
scp ../scripts/run_scenario_motion.py ./
```

### 问题 2: 命令格式错误

**错误信息**: "Unknown command format"

**原因**: 命令格式不正确

**正确格式**:

```bash
--command "move_to_position_with_velocity(500, 0, 50, 20.0)"
#         命令名                       N   E  Alt Vel(m/s)
```

### 问题 3: 速度数据缺失

**症状**: 轨迹中没有 `velocity` 字段

**可能原因**: ProjectAirSim API 返回的速度数据格式不同

**调试步骤**:

1. 检查 `get_drone_velocity()` 函数的实现
2. 打印 `drone.get_state()` 的原始输出
3. 根据实际API调整速度提取逻辑

### 问题 4: 所有测试都被拒绝

**检查**: 速度限制配置是否正确加载

```bash
# 查看场景配置
cat sim_config/S009_speed_limit.jsonc | grep -A 5 "scenario_parameters"
```

应该看到 `speed_limit_kmh: 100.0`

---

## 📝 测试完成检查清单

完成测试后，确认：

- [ ] 6个测试用例全部执行
- [ ] 6个轨迹文件已下载
- [ ] TC3 (边界值) 正确被拒绝
- [ ] TC1, TC2, TC6 (允许) 有完整轨迹
- [ ] TC4, TC5 (超速) 正确被拒绝
- [ ] 速度数据记录完整
- [ ] 准备好数据生成最终报告

---

## 🎯 下一步

测试完成后：

1. 将测试结果发送给我
2. 我会生成 `S009_REPORT.md` 综合报告
3. 根据测试发现更新 `run_scenario_motion.py`（如有需要）
4. 继续 S010（分区速度限制）的开发

---

**文档创建**: 2025-10-22
**预计测试时间**: 30-45分钟
**难度**: ⭐⭐⭐ (中等，新脚本首次使用)
