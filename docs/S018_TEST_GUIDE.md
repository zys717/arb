# S018 多无人机协同飞行测试指南

**场景ID**: S018_MultiDroneCoordination  
**版本**: 1.0  
**创建日期**: 2025-10-31  
**难度**: ⭐⭐⭐

---

## 📋 测试准备

### 1. 环境要求

**服务器端**:
- ProjectAirSim 仿真环境运行正常
- 支持多无人机实例
- Python 3.8+ with projectairsim包

**本地端**:
- Mac环境用于文件传输和结果分析
- scp访问服务器（端口10427）

### 2. 文件清单

**需要上传到服务器的文件**:
```bash
# 场景配置
S018_multi_drone_coordination.jsonc → /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 执行脚本
run_scenario_multi.py → /home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

**本地文件**:
```bash
# Ground Truth
ground_truth/S018_violations.json

# 文档
scenarios/basic/S018_README.md
docs/S018_TEST_GUIDE.md
```

---

## 🚀 执行步骤

### 步骤1: 上传场景配置

```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

scp -P 10427 \
    scenarios/basic/S018_multi_drone_coordination.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 步骤2: 上传执行脚本

```bash
scp -P 10427 \
    scripts/run_scenario_multi.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 步骤3: 连接到服务器

```bash
ssh -p 10427 root@connect.westb.seetacloud.com

# 进入工作目录
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts

# 激活虚拟环境
source ../../airsim-venv/airsim-venv/bin/activate
```

### 步骤4: 执行测试用例

#### TC1: 单操作员单无人机 ✅

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC1.json \
    --mode auto \
    --test-case TC1_SingleOperatorSingleDrone
```

**预期输出**:
```
✓ Scenario loaded: S018_MultiDroneCoordination
✓ Active drones: ['Drone1']
✓ Operator check: OP001 controls 1 drone (1 ≤ 1) → PASS
✅ FLIGHT APPROVED
```

#### TC2: 单操作员多无人机 🚫

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC2.json \
    --mode auto \
    --test-case TC2_SingleOperatorMultiDrones
```

**预期输出**:
```
✓ Scenario loaded: S018_MultiDroneCoordination
✓ Active drones: ['Drone1', 'Drone2']
❌ Operator check: OP001 controls 2 drones (2 > 1) → FAIL
🚫 FLIGHT REJECTED: 违反Part 107.35，单操作员不能同时控制2架无人机
```

#### TC3: 多操作员分别控制 ✅

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC3.json \
    --mode auto \
    --test-case TC3_MultiOperatorsSeparate
```

**预期输出**:
```
✓ Active drones: ['Drone1', 'Drone3']
✓ Operator check: OP001(1), OP002(1) → PASS
✓ Separation check: Drone1-Drone3 = 200.0m (≥ 50m) → PASS
✅ FLIGHT APPROVED
```

#### TC4: 间隔距离不足 🚫

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC4.json \
    --mode auto \
    --test-case TC4_SeparationViolation
```

**预期输出**:
```
✓ Operator check: PASS
❌ Separation check: Drone1-Drone3 = 30.0m (< 50m) → FAIL
   Deficit: 20.0m
🚫 FLIGHT REJECTED: 目标位置两机间隔30m < 最小安全距离50m
```

#### TC5: 集群飞行未审批 🚫

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC5.json \
    --mode auto \
    --test-case TC5_SwarmWithoutApproval
```

**预期输出**:
```
✓ Active drones: 3
✓ Swarm mode: true
❌ Swarm approval check: 3 ≥ 3 (threshold), but has_approval=false → FAIL
🚫 FLIGHT REJECTED: 3架集群飞行需提前申请审批（《条例》第31条第二款第五项）
```

#### TC6: 集群飞行已审批 ✅

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC6.json \
    --mode auto \
    --test-case TC6_SwarmWithApproval \
    --has-approval
```

**预期输出**:
```
✓ Swarm approval check: has_approval=true → PASS
✓ Operator limit: EXEMPTED (swarm approval)
✅ FLIGHT APPROVED: 已获集群飞行审批
```

#### TC7: 顺序操作 ✅

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC7.json \
    --mode auto \
    --test-case TC7_SequentialOperation \
    --sequential-mode
```

**预期输出**:
```
✓ Sequential mode detected
✓ Executing Drone1 first...
✓ Drone1 completed at N=299.5, E=-0.0
✓ Executing Drone2 next...
✓ Drone2 completed at N=299.3, E=99.8
✅ FLIGHT APPROVED: 顺序操作符合规则
```

#### TC8: 边界间隔测试 ✅

```bash
python run_scenario_multi.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S018_multi_drone_coordination.jsonc \
    --output trajectory_S018_TC8.json \
    --mode auto \
    --test-case TC8_BoundarySeparation
```

**预期输出**:
```
✓ Separation check: Drone1-Drone3 = 50.0m (≥ 50m) → PASS
   Boundary test: 50.0 >= 50.0 → True
✅ FLIGHT APPROVED
```

### 步骤5: 下载测试结果

```bash
# 退出服务器
exit

# 在本地Mac执行下载
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S018_TC*.json' \
    test_logs/
```

---

## 📊 结果验证

### 1. 检查测试完整性

```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench

for tc in TC1 TC2 TC3 TC4 TC5 TC6 TC7 TC8; do 
    echo "=== S018 $tc ==="
    jq -r 'if .metadata.execution_result.flight_approved then "✅ APPROVED" else "🚫 REJECTED: \(.metadata.execution_result.reason)" end + " | Drones: \(.metadata.active_drones | length) | Points: \(.trajectory | length)"' test_logs/trajectory_S018_${tc}.json
done
```

**预期输出**:
```
=== S018 TC1 ===
✅ APPROVED | Drones: 1 | Points: ~350

=== S018 TC2 ===
🚫 REJECTED: Single operator multi-drone | Drones: 2 | Points: 0

=== S018 TC3 ===
✅ APPROVED | Drones: 2 | Points: ~700

=== S018 TC4 ===
🚫 REJECTED: Separation violation | Drones: 2 | Points: 0

=== S018 TC5 ===
🚫 REJECTED: Swarm without approval | Drones: 3 | Points: 0

=== S018 TC6 ===
✅ APPROVED | Drones: 3 | Points: ~1050

=== S018 TC7 ===
✅ APPROVED | Drones: 2 | Points: ~700 (sequential)

=== S018 TC8 ===
✅ APPROVED | Drones: 2 | Points: ~700
```

### 2. 详细检查每个测试用例

#### TC1 详细验证

```bash
jq '.metadata.execution_result' test_logs/trajectory_S018_TC1.json
```

**预期**:
```json
{
  "flight_approved": true,
  "operator_check": {
    "OP001": {
      "drone_count": 1,
      "max_allowed": 1,
      "status": "PASS"
    }
  },
  "reason": "符合基本规则：单操作员单无人机"
}
```

#### TC2 详细验证

```bash
jq '.metadata.execution_result' test_logs/trajectory_S018_TC2.json
```

**预期**:
```json
{
  "flight_approved": false,
  "operator_check": {
    "OP001": {
      "drone_count": 2,
      "max_allowed": 1,
      "status": "FAIL"
    }
  },
  "violation_type": "SINGLE_OPERATOR_MULTI_DRONE",
  "reason": "违反Part 107.35：单操作员不能同时控制2架无人机"
}
```

#### TC4 详细验证

```bash
jq '.metadata.execution_result.separation_check' test_logs/trajectory_S018_TC4.json
```

**预期**:
```json
{
  "drone_pair": ["Drone1", "Drone3"],
  "distance_m": 30.0,
  "min_required_m": 50.0,
  "deficit_m": 20.0,
  "status": "FAIL"
}
```

#### TC8 边界验证

```bash
jq '.metadata.execution_result.separation_check' test_logs/trajectory_S018_TC8.json
```

**预期**:
```json
{
  "drone_pair": ["Drone1", "Drone3"],
  "distance_m": 50.0,
  "min_required_m": 50.0,
  "boundary_test": true,
  "comparison": "50.0 >= 50.0",
  "status": "PASS"
}
```

---

## 🎯 关键验证点

### 1. 操作员限制检查

| TC | 操作员 | 无人机数 | 限制 | 结果 |
|----|--------|---------|------|------|
| TC1 | OP001 | 1 | 1 | ✅ PASS |
| TC2 | OP001 | 2 | 1 | 🚫 FAIL |
| TC3 | OP001(1), OP002(1) | 2 | 1 each | ✅ PASS |
| TC7 | OP001 | 2 (sequential) | 1 | ✅ PASS (豁免) |

### 2. 间隔距离检查

| TC | Drone对 | 间隔(m) | 要求(m) | 结果 |
|----|---------|---------|---------|------|
| TC3 | 1-3 | 200 | ≥50 | ✅ PASS |
| TC4 | 1-3 | 30 | ≥50 | 🚫 FAIL |
| TC8 | 1-3 | 50 | ≥50 | ✅ PASS (边界) |

### 3. 集群审批检查

| TC | 无人机数 | 集群模式 | 审批 | 结果 |
|----|---------|---------|------|------|
| TC5 | 3 | true | false | 🚫 FAIL |
| TC6 | 3 | true | true | ✅ PASS |

---

## 🐛 常见问题排查

### 问题1: 多无人机未正确创建

**症状**:
```
Error: Failed to initialize Drone2
```

**原因**: ProjectAirSim可能不支持在同一场景中创建多个Drone对象

**解决方案**:
1. 检查场景配置中3个actors是否正确定义
2. 确认每个drone有唯一的name
3. 如果仍失败，考虑简化为2架无人机测试

### 问题2: 间隔距离计算错误

**症状**:
```
Separation = 200.1m (expected 200.0m)
```

**原因**: 浮点数精度问题

**解决方案**:
```python
# 使用容差比较
def is_separation_sufficient(actual, required, tolerance=0.1):
    return actual >= (required - tolerance)
```

### 问题3: 顺序操作未正确执行

**症状**:
```
Drone1 and Drone2 flying simultaneously in TC7
```

**原因**: `wait_for_completion`逻辑未实现

**解决方案**:
```python
# Drone1飞行并等待完成
await drone1.move_to_position_async(...)
await wait_until_reached(drone1, target1, tolerance=5.0)

# 确认Drone1已停止后再启动Drone2
await asyncio.sleep(1.0)  # 稳定时间
await drone2.move_to_position_async(...)
```

### 问题4: 集群模式标志未识别

**症状**:
```
Warning: swarm_mode not found in metadata
```

**原因**: 测试用例配置中缺少`swarm_mode`字段

**解决方案**:
确保JSONC配置中每个TC都明确定义:
```jsonc
{
  "id": "TC5_...",
  "swarm_mode": true,  // 必须显式设置
  "has_approval": false
}
```

---

## 📈 性能基准

### 预计执行时间

| 测试用例 | 无人机数 | 预计时间 | 说明 |
|---------|---------|---------|------|
| TC1 | 1 | ~50秒 | 单机飞行500m |
| TC2 | 2 | ~5秒 | Pre-flight拒绝 |
| TC3 | 2 | ~100秒 | 两机同时飞行 |
| TC4 | 2 | ~5秒 | Pre-flight拒绝 |
| TC5 | 3 | ~5秒 | Pre-flight拒绝 |
| TC6 | 3 | ~150秒 | 三机编队飞行 |
| TC7 | 2 | ~100秒 | 两机顺序飞行 |
| TC8 | 2 | ~100秒 | 两机同时飞行 |

**总计**: 约15-20分钟（含场景加载）

### 轨迹点数预估

```
单机500m飞行: ~350点
双机同时飞行: ~700点（每机各350点）
三机编队飞行: ~1050点（每机各350点）
Pre-flight拒绝: 0点
```

---

## ✅ 验收标准

### 必须满足的条件

1. ✅ **所有8个测试用例都成功执行**
2. ✅ **决策结果与Ground Truth 100%匹配**
   - TC1, TC3, TC6, TC7, TC8: APPROVE
   - TC2, TC4, TC5: REJECT
3. ✅ **拒绝原因准确**
   - TC2: 单操作员多机违规
   - TC4: 间隔不足
   - TC5: 集群未审批
4. ✅ **边界值处理正确**
   - TC8: 50.0m ≥ 50.0m → PASS
5. ✅ **轨迹数据完整**
   - APPROVE的TC有完整轨迹
   - REJECT的TC轨迹点数为0

### 可选的高级验证

1. ⭐ **动态间隔监控**: In-flight阶段持续监控无人机间距
2. ⭐ **轨迹可视化**: 生成3D轨迹图展示多机飞行
3. ⭐ **冲突检测**: 检测飞行过程中是否有潜在碰撞
4. ⭐ **操作员视角**: 从操作员角度分析控制复杂度

---

## 📝 报告模板

测试完成后，生成报告应包含：

### 1. 执行摘要
- 通过率：X/8
- 关键发现
- 是否符合预期

### 2. 详细测试结果表

| TC | 描述 | 预期 | 实际 | 状态 |
|----|------|------|------|------|
| TC1 | ... | APPROVE | APPROVE | ✅ |
| ... | ... | ... | ... | ... |

### 3. 技术亮点
- 多无人机同步控制
- 3D距离计算算法
- 顺序操作实现
- 集群审批豁免机制

### 4. 遇到的挑战
- ProjectAirSim多实例支持
- 时序控制的复杂性
- 浮点数精度处理

### 5. 经验总结
- 对后续场景的启发
- 工具链改进建议

---

**测试指南版本**: 1.0  
**最后更新**: 2025-10-31  
**预计测试时间**: 15-20分钟  
**难度评估**: ⭐⭐⭐

