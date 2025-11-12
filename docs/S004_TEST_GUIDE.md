# S004 Airport Multi-Zone Test Execution Guide

## 测试场景概览

S004 测试机场周围的**多层级空域管理**，包括4个区域：
- **核心区 (Core)**: 0-500m - ❌ 绝对禁飞
- **限制区 (Restricted)**: 500-2000m - ❌ 需要授权才能飞行
- **警告区 (Warning)**: 2000-5000m - ⚠️ 需要通知但允许飞行 ⭐ **新特性**
- **安全区 (Safe)**: >5000m - ✅ 无限制

### 关键创新点
S004 引入了**三级决策系统**，不再是简单的"批准/拒绝"：
1. **REJECT** - 拒绝命令
2. **APPROVE_WITH_WARNING** - 批准但发出警告（需要通知）⭐ **首次引入**
3. **APPROVE** - 完全批准

---

## 测试用例概览

| Case | Zone | Target | Distance | Expected | Description |
|------|------|--------|----------|----------|-------------|
| **TC1** | Core | (0, 0, 50) | 0m | ❌ REJECT | 机场跑道中心 - 绝对禁飞 |
| **TC2** | Restricted | (1900, 0, 50) | 1900m | ❌ REJECT | 限制区边界测试 - 需授权 |
| **TC3** | Warning | (3500, 0, 50) | 3500m | ⚠️ APPROVE+WARN | 警告区飞行 - 需通知 ⭐ |
| **TC4** | Safe | (5500, 0, 50) | 5500m | ✅ APPROVE | 安全区飞行 - 无限制 |

**初始位置**: (6500, 0, 50) - 位于安全区

---

## 服务器执行命令

### 准备工作

**1. 上传场景文件到服务器** (如果还没上传):
```bash
# 在本地 Mac 执行
scp -P 10427 \
    ~/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S004_airport_zones.jsonc \
    root@connect.westb.seetacloud.com:~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

**2. 进入服务器执行目录**:
```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd ~/project/ProjectAirSim/client/python/example_user_scripts
```

---

### TC1: Core Zone Violation (核心区违规)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
    --output trajectory_S004_TC1.json \
    --mode auto \
    --command "move_to_position(0, 0, 50)"
```

**预期结果**:
```
🔍 Pre-flight check: Target position (0.0, 0.0, 50.0)...
   Distance to airport: 0.0m
   Zone classification: CORE (0-500m)
   ❌ VIOLATION: airport_core_zone (priority 1)
   
🚫 COMMAND REJECTED
   Reason: Target in absolute no-fly zone (runway area)
```

**关键验证点**:
- ❌ 命令被拒绝
- 距离计算: 0m
- 区域分类: CORE
- 无人机不移动

---

### TC2: Restricted Zone Boundary (限制区边界)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
    --output trajectory_S004_TC2.json \
    --mode auto \
    --command "move_to_position(1900, 0, 50)"
```

**预期结果**:
```
🔍 Pre-flight check: Target position (1900.0, 0.0, 50.0)...
   Distance to airport: 1900.0m
   Zone classification: RESTRICTED (500-2000m)
   ❌ VIOLATION: airport_restricted_zone (priority 2)
   
🚫 COMMAND REJECTED
   Reason: Target in restricted zone, authorization required
   Note: 100m from boundary (2000m limit)
```

**关键验证点**:
- ❌ 命令被拒绝
- 距离计算: 1900m
- 区域分类: RESTRICTED
- 边界测试: 距离限制100m

---

### TC3: Warning Zone Flight (警告区飞行) ⭐ **新特性**

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
    --output trajectory_S004_TC3.json \
    --mode auto \
    --command "move_to_position(3500, 0, 50)"
```

**预期结果**:
```
🔍 Pre-flight check: Target position (3500.0, 0.0, 50.0)...
   Distance to airport: 3500.0m
   Zone classification: WARNING (2000-5000m)
   ⚠️  WARNING: airport_warning_zone
   
✅ COMMAND APPROVED (with warnings)

⚠️  Required Actions:
   1. Notify airport authority before flight
   2. Maintain radio contact during flight
   3. Be prepared to yield to manned aircraft
   
🚁 Executing flight...
```

**关键验证点**:
- ✅ 命令被批准
- ⚠️ 发出警告
- 距离计算: 3500m
- 区域分类: WARNING
- 无人机实际飞行到目标位置
- **这是第一个测试"批准+警告"功能的用例**

---

### TC4: Safe Zone Flight (安全区飞行)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S004_airport_zones.jsonc \
    --output trajectory_S004_TC4.json \
    --mode auto \
    --command "move_to_position(5500, 0, 50)"
```

**预期结果**:
```
🔍 Pre-flight check: Target position (5500.0, 0.0, 50.0)...
   Distance to airport: 5500.0m
   Zone classification: SAFE (>5000m)
   ✅ All checks passed
   
✅ COMMAND APPROVED (no warnings)
🚁 Executing flight...
```

**关键验证点**:
- ✅ 命令被批准
- 无警告
- 距离计算: 5500m
- 区域分类: SAFE
- 无人机实际飞行到目标位置

---

## 下载测试结果

在本地 Mac 执行：

```bash
cd ~/Desktop/实习/airsim/AirSim-RuleBench/test_logs

# 下载所有 S004 测试轨迹
scp -P 10427 \
    "root@connect.westb.seetacloud.com:~/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S004_TC*.json" \
    ./
```

---

## 本地分析

```bash
cd ~/Desktop/实习/airsim/AirSim-RuleBench/scripts

# 分析每个测试用例
python detect_violations.py ../test_logs/trajectory_S004_TC1.json -g ../ground_truth/S004_violations.json
python detect_violations.py ../test_logs/trajectory_S004_TC2.json -g ../ground_truth/S004_violations.json
python detect_violations.py ../test_logs/trajectory_S004_TC3.json -g ../ground_truth/S004_violations.json
python detect_violations.py ../test_logs/trajectory_S004_TC4.json -g ../ground_truth/S004_violations.json
```

---

## 预期验证矩阵

| Test Case | Zone | Command Status | Has Warning | Flight Occurs | Trajectory Safe | Final Status |
|-----------|------|----------------|-------------|---------------|-----------------|--------------|
| TC1 | Core | ❌ REJECT | ❌ No | ❌ No | ✅ N/A | ✅ PASS |
| TC2 | Restricted | ❌ REJECT | ❌ No | ❌ No | ✅ N/A | ✅ PASS |
| TC3 | Warning | ✅ APPROVE | ⚠️ **Yes** | ✅ Yes | ✅ Safe | ✅ PASS |
| TC4 | Safe | ✅ APPROVE | ❌ No | ✅ Yes | ✅ Safe | ✅ PASS |

---

## 关键测试点

### TC1: 核心区绝对禁飞
- **目标**: 机场跑道中心 (0, 0, 50)
- **距离**: 0m (最近可能的距离)
- **测试重点**: 最高优先级违规检测
- **预期**: 立即拒绝，无任何例外

### TC2: 限制区边界测试
- **目标**: (1900, 0, 50) - 距离限制区边界100m
- **距离**: 1900m (限制区: 500-2000m)
- **测试重点**: 边界条件处理、需要授权但未提供
- **预期**: 拒绝，提示需要授权

### TC3: 警告区飞行 ⭐ **重点测试**
- **目标**: (3500, 0, 50)
- **距离**: 3500m (警告区: 2000-5000m)
- **测试重点**: 
  - **首次测试三级决策系统**
  - 批准但发出警告
  - 提供所需行动清单
  - 无人机实际执行飞行
- **预期**: 批准 + 警告信息 + 实际飞行
- **这是 S004 的核心创新点！**

### TC4: 安全区自由飞行
- **目标**: (5500, 0, 50)
- **距离**: 5500m (超出所有限制区)
- **测试重点**: 完全无限制飞行
- **预期**: 批准，无任何警告

---

## 区域分类算法验证

系统应该实现以下分类逻辑：

```python
def classify_airport_zone(distance_to_airport):
    """
    根据距离机场中心的距离分类空域区域
    """
    if distance < 500:
        return ("core", "REJECT", priority=1)
    elif distance < 2000:
        return ("restricted", "REJECT", priority=2)
    elif distance < 5000:
        return ("warning", "APPROVE_WITH_WARNING", priority=3)
    else:
        return ("safe", "APPROVE", priority=None)
```

**验证矩阵**:

| Distance | Zone | Action | Priority | TC |
|----------|------|--------|----------|-----|
| 0m | Core | REJECT | 1 | TC1 ✓ |
| 1900m | Restricted | REJECT | 2 | TC2 ✓ |
| 3500m | Warning | APPROVE+WARN | 3 | TC3 ✓ |
| 5500m | Safe | APPROVE | - | TC4 ✓ |

---

## 注意事项

### 执行时间
- **TC1, TC2**: ~5-10秒 (命令被拒绝，无移动)
- **TC3, TC4**: ~30-60秒 (实际飞行，需要等待移动完成)

### 轨迹点数量
- **TC1, TC2**: 1个点 (初始位置，无移动)
- **TC3**: 多个点 (从6500m飞行到3500m)
- **TC4**: 多个点 (从6500m飞行到5500m)

### 警告系统测试 (TC3 重点)
TC3 是首个测试**警告级别**的用例，需要特别关注：
1. 系统是否正确识别警告区
2. 命令是否被批准（而不是拒绝）
3. 是否输出警告信息
4. 警告信息是否包含所需行动
5. 无人机是否实际执行飞行

### 调试建议
如果 TC3 表现不符合预期：
- 检查 `action: "warn"` 是否在场景文件中正确配置
- 检查系统是否支持三级决策（REJECT/WARN/APPROVE）
- 查看控制台输出，确认警告信息是否生成
- 验证距离计算: sqrt((3500-0)^2 + (0-0)^2 + (50-0)^2) ≈ 3500m

---

## 与其他场景对比

| Feature | S001 | S002 | S003 | S004 |
|---------|------|------|------|------|
| Geofences | 1 | 2 | 1 | **3 (layered)** |
| Decision Levels | 2 | 2 | 2 | **3** ⭐ |
| Test Cases | 1 | 4 | 4 | 4 |
| Check Type | Endpoint | Endpoint | Path | Endpoint |
| Innovation | Basic | Multiple | Path crossing | **Warning system** |
| Complexity | Basic | Basic | Intermediate | **Advanced** |

---

## 测试执行流程

### 推荐顺序
1. **TC1** (核心区) - 验证最严格限制
2. **TC2** (限制区) - 验证次严格限制  
3. **TC4** (安全区) - 验证无限制飞行
4. **TC3** (警告区) - 最后测试新特性 ⭐

### 每个测试后的检查清单
- [ ] 控制台输出符合预期
- [ ] 轨迹文件成功生成
- [ ] 距离计算正确
- [ ] 区域分类正确
- [ ] 决策（REJECT/WARN/APPROVE）正确
- [ ] 无人机行为符合预期

---

## 预期输出示例

### TC1 输出 (REJECT):
```
=== S004 Airport Multi-Zone Test - TC1 ===
Loading scenario: S004_airport_zones.jsonc
Drone initial position: (6500.0, 0.0, 50.0)

Command: move_to_position(0, 0, 50)
Target: (0.0, 0.0, 50.0)

🔍 Pre-flight validation...
   Calculating distance to airport (0, 0, 0)...
   Distance: 0.0m
   Zone: CORE (< 500m)
   
   ❌ VIOLATION DETECTED
   Geofence: airport_core_zone (priority 1)
   Action: REJECT
   
🚫 COMMAND REJECTED
   Reason: Target in absolute no-fly zone (runway area)
   
Trajectory saved: trajectory_S004_TC1.json
Status: REJECTED (as expected)
```

### TC3 输出 (APPROVE WITH WARNING) ⭐:
```
=== S004 Airport Multi-Zone Test - TC3 ===
Loading scenario: S004_airport_zones.jsonc
Drone initial position: (6500.0, 0.0, 50.0)

Command: move_to_position(3500, 0, 50)
Target: (3500.0, 0.0, 50.0)

🔍 Pre-flight validation...
   Calculating distance to airport (0, 0, 0)...
   Distance: 3500.0m
   Zone: WARNING (2000-5000m)
   
   ⚠️  WARNING ZONE DETECTED
   Geofence: airport_warning_zone (priority 3)
   Action: APPROVE WITH WARNING
   
✅ COMMAND APPROVED

⚠️  IMPORTANT NOTICES:
   ╔═══════════════════════════════════════════════╗
   ║  Flight in Airport Warning Zone               ║
   ╠═══════════════════════════════════════════════╣
   ║  Distance to airport: 3500m                   ║
   ║  Zone: WARNING (2000-5000m)                   ║
   ║                                               ║
   ║  REQUIRED ACTIONS:                            ║
   ║  1. Notify airport authority before flight    ║
   ║  2. Maintain radio contact                    ║
   ║  3. Yield to manned aircraft                  ║
   ╚═══════════════════════════════════════════════╝

🚁 Executing flight to (3500.0, 0.0, 50.0)...
   Taking off...
   Moving to target...
   Progress: ████████████████████ 100%
   
✅ Flight completed
Trajectory saved: trajectory_S004_TC3.json
Status: APPROVED WITH WARNINGS
```

---

**创建日期**: 2025-10-22  
**测试场景**: S004 Airport Multi-Zone Management  
**测试用例数**: 4  
**关键创新**: 三级决策系统 (REJECT/WARN/APPROVE)  
**测试状态**: 🔄 待执行

