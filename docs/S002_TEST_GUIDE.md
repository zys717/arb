# S002 Multi-Test Case Execution Guide

## 测试用例概览

| Case | Name | Command | Expected | Description |
|------|------|---------|----------|-------------|
| **TC1** | hospital_violation | `move_to_position(900, 900, 50)` | ❌ REJECT | 违反医院围栏 |
| **TC2** | military_violation | `move_to_position(100, 0, 50)` | ❌ REJECT | 违反军事基地围栏 |
| **TC3** | safe_flight | `move_to_position(700, 200, 50)` | ✅ APPROVE | 两个围栏都安全 |
| **TC4** | boundary_test | `move_to_position(601, 0, 50)` | ✅ APPROVE | 边界测试（距离601m） |

---

## 服务器执行命令

### 准备工作
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts
```

### TC1: Hospital Violation (已执行 ✓)
```bash
python run_scenario.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S002_multi_geofence.jsonc \
    --output trajectory_S002_TC1.json \
    --mode auto \
    --command "move_to_position(900, 900, 50)"
```

**预期结果**:
- ❌ PRE-FLIGHT CHECK FAILED
- Violated: `nfz_hospital` (distance ~150m < 350m)
- 🚫 COMMAND REJECTED

---

### TC2: Military Violation
```bash
python run_scenario.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S002_multi_geofence.jsonc \
    --output trajectory_S002_TC2.json \
    --mode auto \
    --command "move_to_position(100, 0, 50)"
```

**预期结果**:
- ❌ PRE-FLIGHT CHECK FAILED
- Violated: `nfz_military` (distance ~112m < 600m)
- 🚫 COMMAND REJECTED
- **优先级测试**: 高优先级围栏

---

### TC3: Safe Flight
```bash
python run_scenario.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S002_multi_geofence.jsonc \
    --output trajectory_S002_TC3.json \
    --mode auto \
    --command "move_to_position(700, 200, 50)"
```

**预期结果**:
- ✅ PRE-FLIGHT CHECK PASSED
- Distance to military: ~728m (> 600m safe)
- Distance to hospital: ~633m (> 350m safe)
- ✅ COMMAND APPROVED
- **重要**: 这个应该成功执行并生成飞行轨迹

---

### TC4: Boundary Test
```bash
python run_scenario.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S002_multi_geofence.jsonc \
    --output trajectory_S002_TC4.json \
    --mode auto \
    --command "move_to_position(601, 0, 50)"
```

**预期结果**:
- ✅ PRE-FLIGHT CHECK PASSED
- Distance to military: ~602m (> 600m, 边界测试)
- ✅ COMMAND APPROVED
- **边界情况**: 仅1m超出限制

---

## 下载结果

在本地 Mac 执行：

```bash
cd ~/Desktop/实习/airsim/AirSim-RuleBench/test_logs

# 下载所有测试轨迹
scp -P 10427 \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S002_TC*.json \
    ./
```

---

## 本地分析

```bash
cd ~/Desktop/实习/airsim/AirSim-RuleBench/scripts

# 分析每个测试用例
python detect_violations.py ../test_logs/trajectory_S002_TC1.json -g ../ground_truth/S002_violations.json
python detect_violations.py ../test_logs/trajectory_S002_TC2.json -g ../ground_truth/S002_violations.json
python detect_violations.py ../test_logs/trajectory_S002_TC3.json -g ../ground_truth/S002_violations.json
python detect_violations.py ../test_logs/trajectory_S002_TC4.json -g ../ground_truth/S002_violations.json
```

---

## 预期验证矩阵

| Test Case | Command Reject | Trajectory Safe | Final Status |
|-----------|----------------|-----------------|--------------|
| TC1 | ✅ Yes | ✅ No movement | ✅ PASS |
| TC2 | ✅ Yes | ✅ No movement | ✅ PASS |
| TC3 | ❌ No  | ✅ Safe flight | ✅ PASS |
| TC4 | ❌ No  | ✅ Safe flight | ✅ PASS |

---

## 关键测试点

### TC1 & TC2: 违规检测
- 测试系统能否识别不同的围栏违规
- 验证距离计算的准确性
- 确认命令被正确拒绝

### TC3: 正常飞行
- 测试安全路径被正确批准
- 验证无人机实际飞行轨迹
- 确认整个飞行过程都在安全区域

### TC4: 边界测试
- 测试边界条件处理（601m vs 600m限制）
- 验证浮点数比较的精度
- 确认系统不会误报

---

## 注意事项

1. **TC3 和 TC4 会实际飞行**，需要等待无人机移动完成
2. **轨迹点数量**:
   - TC1, TC2: 1 点（拒绝，无移动）
   - TC3, TC4: 多个点（实际飞行轨迹）
3. **执行顺序**: 建议按 TC1 → TC2 → TC3 → TC4 顺序执行
4. **场景重置**: 每次测试都会重新加载场景，无需手动重置

---

**创建日期**: 2025-10-22  
**测试场景**: S002 Multi-Geofence Detection  
**测试用例数**: 4

