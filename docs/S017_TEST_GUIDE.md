# S017 载重与投放物品限制 - 测试执行指南

**场景**: S017_PayloadAndDropRestrictions  
**脚本**: `run_scenario_payload.py` (待创建)  
**测试日期**: 2025-10-31  
**预计测试时间**: 40-50分钟（8个测试用例）

---

## 📋 测试前准备

### 1. 文件清单

确保以下文件已准备好：

```bash
# 场景配置
scenarios/basic/S017_payload_and_drop_restrictions.jsonc

# Ground Truth
ground_truth/S017_violations.json

# 执行脚本（需创建）
scripts/run_scenario_payload.py
```

### 2. 环境检查

```bash
# 连接服务器
ssh -p 10427 root@connect.westb.seetacloud.com

# 进入工作目录
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts

# 激活虚拟环境
source ../../airsim-venv/airsim-venv/bin/activate

# 验证Python版本
python --version  # 应该是 3.8.10
```

---

## 📤 文件上传

### 上传场景配置

```bash
# 在本地Mac执行
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S017_payload_and_drop_restrictions.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 上传执行脚本

```bash
# 在本地Mac执行
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_payload.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

---

## 🧪 测试执行步骤

### TC1: 超重起飞测试

**载重**: 8.0kg（超过5kg限制）  
**预期**: REJECT（起飞前拒绝）

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC1.json \
    --mode auto \
    --test-case TC1_ExceedPayloadLimit \
    --payload 8.0
```

**预期输出**:
```
Loading scenario: S017_PayloadAndDropRestrictions
✓ Payload restrictions loaded: max=5.0kg

Test Case: TC1_ExceedPayloadLimit
Payload: 8.0kg

🔍 Pre-flight check: Payload weight...
   Payload: 8.0kg
   Maximum: 5.0kg
   Excess: 3.0kg (60%)
   ❌ PAYLOAD EXCEEDED

🚫 FLIGHT REJECTED (Payload exceeds limit)
   Reason: 载重8kg超过最大限制5kg
   Recommended: 减少载重至5kg以内

✓ Trajectory saved: trajectory_S017_TC1.json (0 points)
```

**验证**:
```bash
# 检查轨迹点数（应该为0，未起飞）
jq '.trajectory | length' trajectory_S017_TC1.json
# 预期输出: 0

# 检查拒绝原因
jq '.metadata.execution_result.reason' trajectory_S017_TC1.json
# 预期输出: "Payload exceeded"
```

---

### TC2: 正常载重飞行

**载重**: 3.0kg  
**预期**: APPROVE

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC2.json \
    --mode auto \
    --test-case TC2_NormalPayload \
    --payload 3.0
```

**预期输出**:
```
Payload: 3.0kg
   Maximum: 5.0kg
   Margin: 2.0kg (40%)
   ✓ SAFE

✅ All pre-flight checks passed
✓ Executing movement...
   Target: N=500.0, E=0.0, Alt=50.0m
✓ Target reached

✓ Trajectory saved: trajectory_S017_TC2.json (>500 points)
```

**验证**:
```bash
jq '.trajectory | length' trajectory_S017_TC2.json
# 预期输出: >500

jq '.trajectory[-1].position.north' trajectory_S017_TC2.json
# 预期输出: ~500.0
```

---

### TC3: 城市区域投放物品

**载重**: 2.0kg  
**目标**: (1000, 0, 50) + drop  
**预期**: 飞行APPROVE，投放REJECT

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC3.json \
    --mode auto \
    --test-case TC3_DropInUrbanArea \
    --payload 2.0 \
    --include-drop
```

**预期输出**:
```
✅ Pre-flight checks passed
✓ Flying to (1000, 0, 50)...
✓ Target reached

🔍 Drop check: Verifying drop zone...
   Position: N=1000.0, E=0.0, Alt=50.0m
   Zone detected: urban_area (城市区域)
   Drop prohibited: Yes
   ❌ DROP IN PROHIBITED ZONE

🚫 DROP COMMAND REJECTED
   Reason: 城市区域严格禁止投放物品
   Regulation: 《条例》第31条

✓ Trajectory saved: trajectory_S017_TC3.json (>1000 points)
```

**验证**:
```bash
jq '.metadata.execution_result.drop_approved' trajectory_S017_TC3.json
# 预期输出: false

jq '.metadata.execution_result.drop_zone' trajectory_S017_TC3.json
# 预期输出: "urban_area"
```

---

### TC4: 安全区域投放（已审批）

**载重**: 2.5kg  
**目标**: (2000, 0, 50) + drop  
**审批**: YES  
**预期**: 完全APPROVE

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC4.json \
    --mode auto \
    --test-case TC4_DropInSafeZone \
    --payload 2.5 \
    --include-drop \
    --has-approval
```

**预期输出**:
```
✓ Flying to (2000, 0, 50)...
✓ Target reached

🔍 Drop check: Verifying drop zone...
   Position: N=2000.0, E=0.0, Alt=50.0m
   Zone detected: safe_rural_zone (农村安全区)
   Drop allowed with approval: Yes
   Has approval: Yes
   ✓ ALL CONDITIONS MET

✅ DROP APPROVED
   Executing drop operation...
   ✓ Payload dropped successfully

✓ Trajectory saved: trajectory_S017_TC4.json (>2000 points)
```

---

### TC5: 未经审批投放

**载重**: 2.0kg  
**目标**: (500, 0, 50) + drop  
**审批**: NO  
**预期**: 飞行APPROVE，投放REJECT

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC5.json \
    --mode auto \
    --test-case TC5_DropWithoutApproval \
    --payload 2.0 \
    --include-drop
    # 注意：没有 --has-approval 标志
```

**预期输出**:
```
🔍 Drop check: Verifying authorization...
   Has approval: No
   Required approval: Yes
   ❌ DROP WITHOUT APPROVAL

🚫 DROP COMMAND REJECTED
   Reason: 投放操作需要提前申请审批
   Regulation: 《条例》第31条第二款第二项
```

---

### TC6: 载重边界测试

**载重**: 5.0kg（恰好最大值）  
**预期**: APPROVE

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC6.json \
    --mode auto \
    --test-case TC6_PayloadBoundary \
    --payload 5.0
```

**预期输出**:
```
Payload: 5.0kg
   Maximum: 5.0kg
   Margin: 0.0kg (0%)
   Judgment: 5.0 ≤ 5.0 → True
   ✓ AT BOUNDARY (SAFE)

✅ Pre-flight checks passed (boundary test)
```

**验证**:
```bash
# 确保边界值被正确处理
jq '.metadata.execution_result.flight_approved' trajectory_S017_TC6.json
# 预期输出: true

jq '.metadata.execution_result.boundary_test' trajectory_S017_TC6.json
# 预期输出: true
```

---

### TC7: 农用无人机豁免

**载重**: 3.0kg  
**无人机类型**: agricultural  
**目标**: (1500, -500, 50) + drop  
**审批**: NO（但豁免）  
**预期**: 完全APPROVE

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC7.json \
    --mode auto \
    --test-case TC7_AgriculturalExemption \
    --payload 3.0 \
    --include-drop \
    --drone-type agricultural
    # 注意：没有 --has-approval，但应该通过
```

**预期输出**:
```
Drone type: agricultural
✓ Flying to (1500, -500, 50)...
✓ Target reached

🔍 Drop check: Verifying zone and exemption...
   Position: N=1500.0, E=-500.0, Alt=50.0m
   Zone detected: agricultural_zone (农业作业区)
   Drone type: agricultural
   Exemption applicable: Yes
   ✓ AGRICULTURAL EXEMPTION

✅ DROP APPROVED (Agricultural exemption)
   Regulation: 《条例》第31条第二款第二项
   Clause: "（常规农用无人驾驶航空器作业飞行活动除外）"
   ✓ Payload dropped successfully

✓ Trajectory saved: trajectory_S017_TC7.json (>1500 points)
```

**关键验证**:
```bash
jq '.metadata.execution_result.exemption_applied' trajectory_S017_TC7.json
# 预期输出: true

jq '.metadata.execution_result.exemption_type' trajectory_S017_TC7.json
# 预期输出: "agricultural"
```

---

### TC8: 人群上方投放（绝对禁止）

**载重**: 1.5kg  
**目标**: (500, 500, 50) + drop  
**审批**: YES（但无效）  
**预期**: 飞行APPROVE，投放REJECT

```bash
python run_scenario_payload.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S017_payload_and_drop_restrictions.jsonc \
    --output trajectory_S017_TC8.json \
    --mode auto \
    --test-case TC8_DropInCrowdArea \
    --payload 1.5 \
    --include-drop \
    --has-approval  # 有审批但无效
```

**预期输出**:
```
✓ Flying to (500, 500, 50)...
✓ Target reached

🔍 Drop check: Verifying drop zone...
   Position: N=500.0, E=500.0, Alt=50.0m
   Zone detected: crowd_area (人群聚集区)
   Has approval: Yes
   ⚠️  APPROVAL OVERRIDDEN BY CROWD PROTECTION

🚫 DROP COMMAND REJECTED (ABSOLUTE PROHIBITION)
   Reason: 人群聚集区上方严格禁止投放物品
   Priority: 公共安全优先级最高
   Note: 即使有审批也不允许投放
   Regulation: 《条例》第31条第二款第三项

✓ Trajectory saved: trajectory_S017_TC8.json (>700 points)
```

**关键验证**:
```bash
jq '.metadata.execution_result.drop_approved' trajectory_S017_TC8.json
# 预期输出: false

jq '.metadata.execution_result.absolute_prohibition' trajectory_S017_TC8.json
# 预期输出: true

jq '.metadata.execution_result.protection_priority' trajectory_S017_TC8.json
# 预期输出: "crowd_safety"
```

---

## 📥 下载轨迹文件

测试完成后，下载所有轨迹：

```bash
# 在本地Mac执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S017_TC*.json' \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/
```

---

## ✅ 验证检查清单

### 1. 载重检查（TC1, TC2, TC6）

```bash
# TC1: 超重拒绝
jq '.metadata.execution_result.flight_approved' test_logs/trajectory_S017_TC1.json
# 预期: false

# TC2: 正常载重
jq '.trajectory | length' test_logs/trajectory_S017_TC2.json
# 预期: >500

# TC6: 边界值
jq '.metadata.execution_result.boundary_test' test_logs/trajectory_S017_TC6.json
# 预期: true
```

### 2. 投放区域检查（TC3, TC4, TC8）

```bash
# TC3: 城市禁止
jq '.metadata.execution_result.drop_zone' test_logs/trajectory_S017_TC3.json
# 预期: "urban_area"

# TC4: 安全区批准
jq '.metadata.execution_result.drop_approved' test_logs/trajectory_S017_TC4.json
# 预期: true

# TC8: 人群绝对禁止
jq '.metadata.execution_result.absolute_prohibition' test_logs/trajectory_S017_TC8.json
# 预期: true
```

### 3. 审批验证（TC4, TC5）

```bash
# TC4: 有审批通过
jq '.metadata.execution_result.has_approval' test_logs/trajectory_S017_TC4.json
# 预期: true

# TC5: 无审批拒绝
jq '.metadata.execution_result.approval_missing' test_logs/trajectory_S017_TC5.json
# 预期: true
```

### 4. 豁免逻辑（TC7）

```bash
jq '.metadata.execution_result.exemption_applied' test_logs/trajectory_S017_TC7.json
# 预期: true

jq '.metadata.execution_result.exemption_type' test_logs/trajectory_S017_TC7.json
# 预期: "agricultural"
```

---

## 📊 预期结果汇总

| TC | 载重 | 目标 | 审批 | 类型 | 飞行 | 投放 | 轨迹点 |
|---|---|---|---|---|---|---|---|
| TC1 | 8.0kg | 500,0 | - | 通用 | ❌ | - | 0 |
| TC2 | 3.0kg | 500,0 | - | 通用 | ✅ | - | >500 |
| TC3 | 2.0kg | 1000,0 | - | 通用 | ✅ | ❌ | >1000 |
| TC4 | 2.5kg | 2000,0 | ✅ | 通用 | ✅ | ✅ | >2000 |
| TC5 | 2.0kg | 500,0 | ❌ | 通用 | ✅ | ❌ | >500 |
| TC6 | 5.0kg | 300,0 | - | 通用 | ✅ | - | >300 |
| TC7 | 3.0kg | 1500,-500 | ❌ | 农用 | ✅ | ✅ | >1500 |
| TC8 | 1.5kg | 500,500 | ✅ | 通用 | ✅ | ❌ | >700 |

**预期通过率**: 8/8 = 100%

---

## ⚠️ 常见问题

### 问题1: payload参数不生效

**症状**: 无论设置什么载重都能起飞

**原因**: 脚本未正确解析 `--payload` 参数

**解决**: 检查脚本的参数解析部分

### 问题2: drop命令未执行

**症状**: 没有投放检查输出

**原因**: 缺少 `--include-drop` 标志

**解决**: 确保包含该标志

### 问题3: 豁免逻辑不工作

**症状**: TC7农用机投放被拒绝

**原因**: 
- drone-type未设置为 `agricultural`
- 或位置不在agricultural_zone内

**解决**: 验证位置和类型参数

---

## 📝 测试报告模板

完成测试后，创建 `S017_REPORT.md`:

```markdown
# S017 载重与投放物品限制 - 测试报告

**测试日期**: 2025-10-31
**测试结果**: X/8 通过

## 执行摘要
[简要描述测试结果]

## 测试结果汇总
[表格展示8个TC的结果]

## 关键发现
- 载重限制执行情况
- 区域分类准确性
- 审批验证完整性
- 豁免逻辑正确性

## 技术亮点
[描述实现要点]
```

---

**文档版本**: 1.0  
**最后更新**: 2025-10-31  
**下次测试**: 脚本创建后

