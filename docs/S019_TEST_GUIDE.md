# S019 适飞空域分类测试指南

**场景ID**: S019_AirspaceClassification  
**难度**: ⭐⭐  
**测试用例数**: 5个  
**预计执行时间**: 约10分钟

---

## 📦 文件上传

### 上传场景配置文件

```bash
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S019_airspace_classification.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 上传执行脚本

```bash
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_airspace.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

---

## 🧪 测试执行步骤

### TC1: 适飞空域飞行

**目标**: (500,0,50) + (800,200,119)  
**审批**: NO  
**预期**: APPROVE

```bash
python run_scenario_airspace.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S019_airspace_classification.jsonc \
    --output trajectory_S019_TC1.json \
    --test-case TC1_UncontrolledAirspace
```

**预期输出**:
```
Loading scenario: S019_AirspaceClassification
✓ Rules loaded: altitude_ceiling=120m
✓ Loaded 1 restricted zone(s)
✓ Loading test case: TC1_UncontrolledAirspace

======================================================================
S019 MODE - AIRSPACE CLASSIFICATION
======================================================================

Flight Plan:
  Target 1: (500, 0, 50m)
  Target 2: (800, 200, 119m)
  Approval: NO

🔍 Pre-flight check: Restricted area...
   Target 1: distance=500.0m > 300.0m → Outside restricted area
   Target 2: distance=838.1m > 300.0m → Outside restricted area
✅ No restricted area violations

🔍 Pre-flight check: Altitude boundary...
   Target 1: 50.0m < 120.0m → Uncontrolled airspace
   Target 2: 119.0m < 120.0m → Uncontrolled airspace (boundary)
✅ All targets within uncontrolled airspace

🔍 Pre-flight check: Approval requirement...
   Uncontrolled airspace + Light drone → No approval required
✅ Approval check passed

✅ All pre-flight checks passed, starting simulation...

🚁 Flying to Target 1: (500, 0, 50)
   [  50] N= 250.5 E=   0.0 Alt=  50.0m | To target:  249.5m
   [ 100] N= 450.2 E=   0.0 Alt=  50.0m | To target:   49.8m
   ✓ Target 1 reached at N=500.0, E=0.0, Alt=50.0m

🚁 Flying to Target 2: (800, 200, 119)
   [  50] N= 650.5 E= 100.0 Alt= 119.0m | To target:  223.6m
   [ 100] N= 750.2 E= 180.0 Alt= 119.0m | To target:   72.1m
   ✓ Target 2 reached at N=800.0, E=200.0, Alt=119.0m

✓ Flight completed, 512 trajectory points recorded

✓ Result saved: trajectory_S019_TC1.json (512 trajectory points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED
======================================================================
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S019_TC1.json
# 预期输出: true

# 检查目标数
jq '.metadata.targets | length' trajectory_S019_TC1.json
# 预期输出: 2

# 检查轨迹点数
jq '.trajectory | length' trajectory_S019_TC1.json
# 预期输出: 512 (约)
```

---

### TC2: 管制空域未审批

**目标**: (500,0,120) + (800,200,150)  
**审批**: NO  
**预期**: REJECT

```bash
python run_scenario_airspace.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S019_airspace_classification.jsonc \
    --output trajectory_S019_TC2.json \
    --test-case TC2_ControlledAirspace
```

**预期输出**:
```
Loading scenario: S019_AirspaceClassification
✓ Rules loaded: altitude_ceiling=120m
✓ Loading test case: TC2_ControlledAirspace

======================================================================
S019 MODE - AIRSPACE CLASSIFICATION
======================================================================

Flight Plan:
  Target 1: (500, 0, 120m)
  Target 2: (800, 200, 150m)
  Approval: NO

🔍 Pre-flight check: Restricted area...
   Target 1: distance=500.0m > 300.0m → Outside restricted area
   Target 2: distance=838.1m > 300.0m → Outside restricted area
✅ No restricted area violations

🔍 Pre-flight check: Altitude boundary...
   Target 1: 120.0m >= 120.0m → Controlled airspace
   Target 2: 150.0m >= 120.0m → Controlled airspace
❌ Targets enter controlled airspace

🔍 Pre-flight check: Approval requirement...
   Controlled airspace flight requires approval
   Current approval status: NO
❌ Missing required approval

🚫 FLIGHT REJECTED (Controlled airspace without approval)
Reason: 目标高度进入管制空域（≥120m），需要飞行审批

Rejection details:
  First violation: Target at 120.0m
  Altitude ceiling: 120.0m
  Excess: 0.0m (boundary)

✓ Result saved: trajectory_S019_TC2.json (0 trajectory points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED (Pre-flight rejection)
======================================================================
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S019_TC2.json
# 预期输出: false

# 检查拒绝原因
jq '.metadata.reason' trajectory_S019_TC2.json
# 预期输出: "目标高度进入管制空域（≥120m），需要飞行审批"

# 检查轨迹点数（应该为0）
jq '.trajectory | length' trajectory_S019_TC2.json
# 预期输出: 0
```

---

### TC3: 管制空域已审批

**目标**: (500,0,150) + (1000,500,200)  
**审批**: YES  
**预期**: APPROVE

```bash
python run_scenario_airspace.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S019_airspace_classification.jsonc \
    --output trajectory_S019_TC3.json \
    --test-case TC3_ControlledAirspaceWithApproval \
    --has-approval
```

**预期输出**:
```
Loading scenario: S019_AirspaceClassification
✓ Rules loaded: altitude_ceiling=120m
✓ Loading test case: TC3_ControlledAirspaceWithApproval

======================================================================
S019 MODE - AIRSPACE CLASSIFICATION
======================================================================

Flight Plan:
  Target 1: (500, 0, 150m)
  Target 2: (1000, 500, 200m)
  Approval: YES

🔍 Pre-flight check: Restricted area...
   Target 1: distance=500.0m > 300.0m → Outside restricted area
   Target 2: distance=1118.0m > 300.0m → Outside restricted area
✅ No restricted area violations

🔍 Pre-flight check: Altitude boundary...
   Target 1: 150.0m >= 120.0m → Controlled airspace
   Target 2: 200.0m >= 120.0m → Controlled airspace
⚠️  Targets enter controlled airspace, but approval granted

🔍 Pre-flight check: Approval requirement...
   Controlled airspace flight → Approval required
   Current approval status: YES
✅ Approval check passed

✅ All pre-flight checks passed, starting simulation...

🚁 Flying to Target 1: (500, 0, 150)
   [  50] N= 250.5 E=   0.0 Alt= 150.0m | To target:  249.5m
   [ 100] N= 450.2 E=   0.0 Alt= 150.0m | To target:   49.8m
   ✓ Target 1 reached at N=500.0, E=0.0, Alt=150.0m

🚁 Flying to Target 2: (1000, 500, 200)
   [  50] N= 750.5 E= 250.0 Alt= 200.0m | To target:  559.0m
   [ 100] N= 900.2 E= 450.0 Alt= 200.0m | To target:  111.8m
   ✓ Target 2 reached at N=1000.0, E=500.0, Alt=200.0m

✓ Flight completed, 498 trajectory points recorded

✓ Result saved: trajectory_S019_TC3.json (498 trajectory points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED
======================================================================
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S019_TC3.json
# 预期输出: true

# 检查审批状态
jq '.metadata.has_approval' trajectory_S019_TC3.json
# 预期输出: true

# 检查轨迹点数
jq '.trajectory | length' trajectory_S019_TC3.json
# 预期输出: 498 (约)
```

---

### TC4: 限制区域未审批

**目标**: (1500,0,50) + (1600,100,100)  
**审批**: NO  
**预期**: REJECT

```bash
python run_scenario_airspace.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S019_airspace_classification.jsonc \
    --output trajectory_S019_TC4.json \
    --test-case TC4_RestrictedArea
```

**预期输出**:
```
Loading scenario: S019_AirspaceClassification
✓ Rules loaded: altitude_ceiling=120m
✓ Loaded 1 restricted zone(s)
   - 军事限制区: center=(1500,0), radius=300m
✓ Loading test case: TC4_RestrictedArea

======================================================================
S019 MODE - AIRSPACE CLASSIFICATION
======================================================================

Flight Plan:
  Target 1: (1500, 0, 50m)
  Target 2: (1600, 100, 100m)
  Approval: NO

🔍 Pre-flight check: Restricted area...
   Restricted area center: (1500.0, 0.0), radius: 300.0m
   Target 1: distance=0.0m <= 300.0m → INSIDE restricted area
   Target 2: distance=141.4m <= 300.0m → INSIDE restricted area
❌ Targets enter restricted area

🔍 Pre-flight check: Approval requirement...
   Restricted area flight requires special approval
   Current approval status: NO
❌ Missing required approval

🚫 FLIGHT REJECTED (Restricted area without approval)
Reason: 目标位置在军事限制区内，无论高度均需审批

Rejection details:
  Zone: restricted_area_military
  Center: (1500.0, 0.0)
  Radius: 300.0m
  Targets in zone: 2/2

Note: 虽然高度50m和100m均<120m，但限制区域检查优先级更高

✓ Result saved: trajectory_S019_TC4.json (0 trajectory points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED (Pre-flight rejection)
======================================================================
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S019_TC4.json
# 预期输出: false

# 检查拒绝原因
jq '.metadata.reason' trajectory_S019_TC4.json
# 预期输出: "目标位置在军事限制区内，无论高度均需审批"

# 检查限制区域信息
jq '.metadata.pre_flight_checks.restricted_area_checks[0].in_restricted' trajectory_S019_TC4.json
# 预期输出: true
```

---

### TC5: 限制区域已审批

**目标**: (1500,0,50) + (1500,0,150)  
**审批**: YES  
**预期**: APPROVE

```bash
python run_scenario_airspace.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S019_airspace_classification.jsonc \
    --output trajectory_S019_TC5.json \
    --test-case TC5_RestrictedAreaWithApproval \
    --has-approval
```

**预期输出**:
```
Loading scenario: S019_AirspaceClassification
✓ Rules loaded: altitude_ceiling=120m
✓ Loaded 1 restricted zone(s)
✓ Loading test case: TC5_RestrictedAreaWithApproval

======================================================================
S019 MODE - AIRSPACE CLASSIFICATION
======================================================================

Flight Plan:
  Target 1: (1500, 0, 50m)
  Target 2: (1500, 0, 150m)
  Approval: YES

🔍 Pre-flight check: Restricted area...
   Restricted area center: (1500.0, 0.0), radius: 300.0m
   Target 1: distance=0.0m <= 300.0m → INSIDE restricted area
   Target 2: distance=0.0m <= 300.0m → INSIDE restricted area
⚠️  Targets enter restricted area, but approval granted

🔍 Pre-flight check: Altitude boundary...
   Target 1: 50.0m < 120.0m → Uncontrolled airspace
   Target 2: 150.0m >= 120.0m → Controlled airspace

🔍 Pre-flight check: Approval requirement...
   Restricted area flight → Approval required
   Current approval status: YES
✅ Approval check passed

✅ All pre-flight checks passed, starting simulation...

🚁 Flying to Target 1: (1500, 0, 50)
   [  50] N= 750.5 E=   0.0 Alt=  50.0m | To target:  749.5m
   [ 100] N=1350.2 E=   0.0 Alt=  50.0m | To target:  149.8m
   ✓ Target 1 reached at N=1500.0, E=0.0, Alt=50.0m

🚁 Flying to Target 2: (1500, 0, 150)
   [  50] N=1500.0 E=   0.0 Alt= 100.0m | To target:   50.0m
   [ 100] N=1500.0 E=   0.0 Alt= 150.0m | To target:    0.0m
   ✓ Target 2 reached at N=1500.0, E=0.0, Alt=150.0m

✓ Flight completed, 256 trajectory points recorded

✓ Result saved: trajectory_S019_TC5.json (256 trajectory points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED
======================================================================
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S019_TC5.json
# 预期输出: true

# 检查审批状态
jq '.metadata.has_approval' trajectory_S019_TC5.json
# 预期输出: true

# 检查轨迹点数
jq '.trajectory | length' trajectory_S019_TC5.json
# 预期输出: 256 (约)
```

---

## 📥 下载结果

```bash
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S019_TC*.json' \
    AirSim-RuleBench/test_logs/
```

---

## ✅ 结果汇总

```bash
# 快速查看所有测试结果
cd AirSim-RuleBench
for tc in TC1 TC2 TC3 TC4 TC5; do
    echo "===== $tc ====="
    jq -r '.metadata | "\(.test_case_id): \(if .flight_approved then "✅ APPROVED" else "🚫 REJECTED" end) - \(.reason)"' \
        test_logs/trajectory_S019_${tc}.json
    echo ""
done
```

**预期结果对照表**:

| TC  | 预期决策 | 预期原因                                 | 轨迹点数 |
| --- | -------- | ---------------------------------------- | -------- |
| TC1 | APPROVE  | 所有目标高度均在适飞空域内（<120m）     | ~500     |
| TC2 | REJECT   | 目标高度进入管制空域（≥120m），需要审批 | 0        |
| TC3 | APPROVE  | 已获得管制空域飞行审批                   | ~500     |
| TC4 | REJECT   | 目标位置在军事限制区内，无论高度均需审批 | 0        |
| TC5 | APPROVE  | 已获得限制区域飞行审批                   | ~250     |

**通过率**: 3/5 APPROVE, 2/5 REJECT

---

## 🎯 关键验证点

### 1. 高度边界测试

- TC1: 119m应该通过（适飞空域边界内）
- TC2: 120m应该拒绝（管制空域边界）
- **边界判断使用 `>=`**

### 2. 限制区域优先级

- TC4: 即使高度<120m，限制区域仍需审批
- **检查顺序**: 限制区域 → 高度边界 → 审批状态

### 3. 审批逻辑

- TC3: 有审批可以在管制空域飞行
- TC5: 有审批可以在限制区域飞行

---

**文档版本**: 1.0  
**最后更新**: 2025-11-01  
**维护人**: Claude
