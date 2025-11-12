# S016 实时障碍物避让 - 服务器端测试指南

**场景**: S016_RealtimeObstacleAvoidance
**测试日期**: 2025-10-31
**预计时长**: 25分钟
**测试用例**: 6个

---

## 📋 测试概述

### 测试目标

验证无人机在**飞行过程中**实时检测障碍物并自动停止的能力。

### 关键特性

- ✅ **In-flight实时监控**: 飞行中每0.1秒检测一次与障碍物的距离
- ✅ **自动停止**: 当距离<80m时自动停止并悬停
- ✅ **持续飞行**: 无障碍物时正常完成飞行至目标点

### 与S015对比

| 特性     | S015                 | S016                |
| -------- | -------------------- | ------------------- |
| 检测时机 | Pre-flight（起飞前） | In-flight（飞行中） |
| 检测方法 | 路径几何分析         | 实时距离监控        |
| 触发条件 | 路径相交             | 接近<80m            |
| 响应行为 | 拒绝起飞             | 自动停止悬停        |

---

## 🔧 准备工作

### 1. 文件准备

需要上传的文件：

```bash
# 场景配置
scenarios/basic/S016_realtime_obstacle_avoidance.jsonc

# 执行脚本（与S015共用，使用不同detection-mode）
scripts/run_scenario_path.py  # 已扩展支持in-flight模式
```

### 2. 上传文件到服务器

```bash
# 场景配置
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S016_realtime_obstacle_avoidance.jsonc \       root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 执行脚本（与S015共用）
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_path.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 3. SSH连接服务器

```bash
ssh root@connect.westb.seetacloud.com
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts
source ../../airsim-venv/airsim-venv/bin/activate
```

---

## 🧪 测试执行

### 障碍物配置

```
Obstacle_Building (800, 0):   避让半径 80m
Obstacle_Tower (1500, 300):   避让半径 80m
Obstacle_Crane (500, 500):    避让半径 100m
```

### TC1: 直接接近障碍物 ⭐⭐⭐ 核心测试

**目标**: (1000, 0, 50)
**预期**: APPROVE_WITH_STOP（在720m处停止）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC1.json \
    --mode auto \
    --test-case TC1 \
    --detection-mode in-flight
```

**预期输出**:

```
✅ All pre-flight checks passed
✓ Executing movement...

🔍 In-flight monitoring: Obstacle detection active
   Monitoring frequency: 10Hz
   
Position: N=100.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (700m) ✓
   
Position: N=200.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (600m) ✓
   
...

Position: N=720.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (80m) ⚠️
   ⛔ OBSTACLE DETECTED WITHIN SAFETY DISTANCE!
   Obstacle: obstacle_building
   Distance: 80.0m
   Safety threshold: 80.0m
   
🛑 AUTOMATIC STOP TRIGGERED
   Reason: Obstacle within safety distance
   Hover position: N=720.0, E=0.0, Alt=50.0m
   Distance traveled: 720.0m
   
✓ Trajectory saved: trajectory_S016_TC1.json 
```

**验证点**:

- ✅ 停止位置 ≈ (720, 0, 50)
- ✅ 轨迹点数 >700
- ✅ 距离obstacle_building约80m时停止

---

### TC2: 无障碍路径完成 ⭐

**目标**: (400, 0, 50)
**预期**: APPROVE（完整飞行）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC2.json \
    --mode auto \
    --test-case TC2 \
    --detection-mode in-flight
```

**预期输出**:

```
✅ All pre-flight checks passed
✓ Executing movement...

🔍 In-flight monitoring: Obstacle detection active
   
Position: N=100.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (700m) ✓
   
Position: N=200.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (600m) ✓
   
Position: N=300.0, E=0.0, Alt=50.0m
   Closest obstacle: obstacle_building (500m) ✓
   
Position: N=400.0, E=0.0, Alt=50.0m
   ✓ Target reached
   Closest obstacle: obstacle_building (400m) ✓
   
✅ Flight completed successfully
   Final position: N=400.0, E=0.0, Alt=50.0m
   Distance traveled: 400.0m
   No obstacles encountered
   
✓ Trajectory saved: trajectory_S016_TC2.json (>400 points)
```

**验证点**:

- ✅ 完整飞行至(400, 0, 50)
- ✅ 轨迹点数 >400
- ✅ 无停止事件

---

### TC3: 偏移路径安全通过 ⭐⭐

**目标**: (800, 150, 50)
**预期**: APPROVE（完整飞行）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC3.json \
    --mode auto \
    --test-case TC3 \
    --detection-mode in-flight
```

**预期输出**:

```
🔍 In-flight monitoring: Obstacle detection active

Position: N=750.0, E=140.0, Alt=50.0m
   Closest obstacle: obstacle_building (140m) ✓
   Safe clearance maintained
   
Position: N=800.0, E=150.0, Alt=50.0m
   ✓ Target reached
   Closest obstacle: obstacle_building (150m) ✓
   
✅ Flight completed successfully
   Path offset avoided obstacle
   
✓ Trajectory saved: trajectory_S016_TC3.json (>800 points)
```

**验证点**:

- ✅ 完整飞行至(800, 150, 50)
- ✅ 最小距离 >80m (约140m)
- ✅ 无停止事件

---

### TC4: 多障碍物第一个停止 ⭐⭐

**目标**: (2000, 0, 50)
**预期**: APPROVE_WITH_STOP（在720m处停止）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC4.json \
    --mode auto \
    --test-case TC4 \
    --detection-mode in-flight
```

**预期输出**:

```
Position: N=720.0, E=0.0, Alt=50.0m
   ⛔ OBSTACLE DETECTED!
   Obstacle: obstacle_building (first obstacle)
   
🛑 AUTOMATIC STOP TRIGGERED
   Stopped before first obstacle
   Target (2000m) not reached
   
✓ Trajectory saved: trajectory_S016_TC4.json (>700 points)
```

**验证点**:

- ✅ 停止于 ≈720m
- ✅ 未到达2000m目标
- ✅ 在第一个障碍物前停止

---

### TC5: 对角线路径检测塔 ⭐⭐⭐

**目标**: (1500, 300, 50)
**预期**: APPROVE_WITH_STOP（在≈1450m处停止）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC5.json \
    --mode auto \
    --test-case TC5 \
    --detection-mode in-flight
```

**预期输出**:

```
🔍 In-flight monitoring: Obstacle detection active
   Path: (0,0) → (1500,300) diagonal
   
Position: N=1200.0, E=240.0, Alt=50.0m
   Closest obstacle: obstacle_tower (300m) ✓
   
Position: N=1400.0, E=280.0, Alt=50.0m
   Closest obstacle: obstacle_tower (100m) ⚠️
   
Position: N=1465.0, E=293.0, Alt=50.0m
   ⛔ OBSTACLE DETECTED!
   Obstacle: obstacle_tower
   Distance: 80.0m
   
🛑 AUTOMATIC STOP TRIGGERED
   Stop position: N≈1465, E≈293, Alt=50m
   Distance traveled: ≈1450m
   
✓ Trajectory saved: trajectory_S016_TC5.json (>1400 points)
```

**验证点**:

- ✅ 停止距离 ≈1450m
- ✅ 停止位置 ≈(1465, 293, 50)
- ✅ 对角线路径检测精度

---

### TC6: 短距离无障碍 ⭐

**目标**: (200, 0, 50)
**预期**: APPROVE（完整飞行）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S016_realtime_obstacle_avoidance.jsonc \
    --output trajectory_S016_TC6.json \
    --mode auto \
    --test-case TC6 \
    --detection-mode in-flight
```

**预期输出**:

```
✅ All pre-flight checks passed
✓ Executing movement...

Position: N=200.0, E=0.0, Alt=50.0m
   ✓ Target reached
   All obstacles >500m away
   
✅ Flight completed successfully
   
✓ Trajectory saved: trajectory_S016_TC6.json (>200 points)
```

**验证点**:

- ✅ 完整飞行至(200, 0, 50)
- ✅ 短距离快速完成

---

## 📥 测试后工作

### 1. 下载轨迹文件

```bash
# 退出SSH（Ctrl+D）
# 在本地执行：
scp -P 10427 'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S016_TC*.json' test_logs/
```

### 2. 验证测试结果

检查轨迹文件：

```bash
# TC1: 停止于720m
ls -lh test_logs/trajectory_S016_TC1.json
# 预期: >100KB, >700个点

# TC2: 完整飞行400m
ls -lh test_logs/trajectory_S016_TC2.json
# 预期: >60KB, >400个点

# TC5: 停止于1450m
ls -lh test_logs/trajectory_S016_TC5.json
# 预期: >240KB, >1400个点
```

快速验证：

```bash
# 检查TC1是否在720m左右停止
jq '.trajectory[-1].position.north' test_logs/trajectory_S016_TC1.json
# 预期输出: 720左右

# 检查TC2是否完整到达400m
jq '.trajectory[-1].position.north' test_logs/trajectory_S016_TC2.json
# 预期输出: 400左右

# 检查TC5停止距离
jq '.trajectory[-1]' test_logs/trajectory_S016_TC5.json | jq '{north: .position.north, east: .position.east}'
# 预期输出: north≈1465, east≈293
```

---

## ✅ 验证清单

### 核心功能验证

- [ ] **TC1**: 直接接近障碍物，自动停止@720m ⭐⭐⭐
- [ ] **TC2**: 无障碍路径，完整飞行至400m ⭐
- [ ] **TC3**: 偏移路径，安全绕过障碍物 ⭐⭐
- [ ] **TC4**: 多障碍物，第一个障碍物前停止 ⭐⭐
- [ ] **TC5**: 对角线路径，检测塔并停止@1450m ⭐⭐⭐
- [ ] **TC6**: 短距离，无障碍完成 ⭐

### 技术指标验证

- [ ] In-flight实时监控工作正常（10Hz频率）
- [ ] 距离计算准确（80m阈值）
- [ ] 自动停止响应及时
- [ ] 悬停位置稳定
- [ ] 轨迹记录完整

### 文件完整性

- [ ] 6个轨迹文件全部生成
- [ ] 文件大小合理
- [ ] JSON格式正确

---

## 🔍 常见问题

### Q1: 如果TC1没有停止而是继续飞行？

**可能原因**:

1. In-flight监控未启用
2. 障碍物距离计算错误
3. 安全阈值设置不正确

**调试**:

```bash
# 检查脚本中的监控逻辑
# 确认每个飞行循环都在检测障碍物距离
```

### Q2: TC3意外停止了？

**可能原因**:

- 路径距离计算错误，误判为接近障碍物

**调试**:

```bash
# 检查路径几何计算
# TC3应该保持>140m距离，远大于80m阈值
```

### Q3: TC5停止位置不准确？

**可能原因**:

- 对角线路径的距离计算不准确
- 监控频率不够（应为10Hz）

**调试**:

```bash
# 增加监控日志输出
# 检查停止时的实际距离
```

---

## 📊 预期成功标准

| 测试用例 | 通过标准                            |
| -------- | ----------------------------------- |
| TC1      | 停止位置720±20m，轨迹>700点        |
| TC2      | 完整到达400m，轨迹>400点            |
| TC3      | 完整到达(800,150)，轨迹>800点       |
| TC4      | 停止位置720±20m（与TC1相同）       |
| TC5      | 停止距离1450±50m，位置≈(1465,293) |
| TC6      | 完整到达200m，轨迹>200点            |

**总体目标**: 6/6 = 100% 通过率

---

## 🛠️ 脚本实现建议

### 核心逻辑伪代码

```python
async def run_scenario_auto(scenario_config, test_command):
    # 1. 起飞
    await drone.takeoff_async()
  
    # 2. 解析目标
    target = parse_command(test_command)
  
    # 3. 开始飞行
    asyncio.create_task(drone.move_to_position_async(target))
  
    # 4. In-flight监控循环
    while not reached_target:
        current_pos = get_drone_position(drone)
      
        # 检测所有障碍物
        for obstacle in obstacles:
            distance = calculate_distance(current_pos, obstacle.center)
          
            if distance < obstacle.safety_threshold:
                # 触发自动停止
                await drone.hover()
                print(f"🛑 OBSTACLE DETECTED: {obstacle.id}")
                print(f"   Distance: {distance:.1f}m")
                return {"stopped": True, "reason": "obstacle"}
      
        # 记录轨迹
        recorder.record_point(current_pos)
      
        # 检查是否到达
        if distance_to_target < 1.0:
            break
      
        await asyncio.sleep(0.1)  # 10Hz监控
  
    return {"success": True, "completed": True}
```

---

**测试指南版本**: 1.0
**创建日期**: 2025-10-31
**作者**: AirSim-RuleBench Team

---

**提示**: S016是In-flight实时检测场景，重点验证飞行中的自动停止功能。确保监控频率足够高（10Hz）以及时检测障碍物接近！🚁
