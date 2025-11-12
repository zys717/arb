# S020 飞行申请时限测试指南

**场景ID**: S020_ApprovalTimeline  
**难度**: ⭐⭐  
**测试用例数**: 4个  
**预计执行时间**: 约5分钟（纯逻辑检查，无飞行模拟）

---

## 📦 文件上传

### 上传场景配置文件

```bash
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S020_approval_timeline.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

### 上传执行脚本

```bash
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_timeline.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

---

## 🧪 测试执行步骤

### TC1: 申请时间过晚

**时间差**: 6小时（不足36小时）  
**预期**: REJECT

```bash
python run_scenario_timeline.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S020_approval_timeline.jsonc \
    --output trajectory_S020_TC1.json \
    --test-case TC1_ApprovalTooLate
```

**预期输出**:
```
Loading scenario: S020_ApprovalTimeline
✓ Rules loaded: advance_notice=36h

Test Case: TC1_ApprovalTooLate
Current time: 2024-10-20 10:00
Application time: 2024-10-21 09:00
Planned flight time: 2024-10-21 15:00
Target: (1000, 0, 50m)

🔍 Pre-flight check: Controlled zone...
   Target position: (1000.0, 0.0)
   Distance to zone center: 0.0m <= 500.0m
   ✓ IN controlled zone → Requires approval

🔍 Pre-flight check: Exemptions...
   Flight type: normal
   Altitude: 50m (< 120m but in controlled zone)
   ❌ NO exemptions applicable

🔍 Pre-flight check: Time advance...
   Application time: 2024-10-21 09:00
   Flight time: 2024-10-21 15:00
   Time difference: 6.0 hours
   Required: 36.0 hours
   Shortage: 30.0 hours
   ❌ INSUFFICIENT ADVANCE NOTICE

🚫 FLIGHT REJECTED (Insufficient advance notice)
Reason: 申请时间距飞行仅6小时，未满足提前36小时申请要求

✓ Result saved: trajectory_S020_TC1.json (0 points)
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S020_TC1.json
# 预期输出: false

# 检查拒绝原因
jq '.metadata.reason' trajectory_S020_TC1.json
# 预期输出: "申请时间距飞行仅6小时，未满足提前36小时申请要求"

# 检查时间差
jq '.metadata.time_checks.time_difference_hours' trajectory_S020_TC1.json
# 预期输出: 6.0
```

---

### TC2: 按时提前申请（两阶段测试）

**阶段1**: 52小时提前量  
**阶段2**: 36小时边界测试  
**预期**: APPROVE

```bash
python run_scenario_timeline.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S020_approval_timeline.jsonc \
    --output trajectory_S020_TC2.json \
    --test-case TC2_ApprovalOnTime
```

**预期输出**:
```
Loading scenario: S020_ApprovalTimeline
✓ Rules loaded: advance_notice=36h

Test Case: TC2_ApprovalOnTime (Multi-phase test)

════════════════ Phase 1: Sufficient Advance ════════════════
Application time: 2024-10-20 10:00
Flight time: 2024-10-22 14:00

🔍 Pre-flight check: Time advance...
   Time difference: 52.0 hours
   Required: 36.0 hours
   Surplus: 16.0 hours
   ✅ SUFFICIENT ADVANCE NOTICE

✅ Phase 1 PASSED (52h advance)

════════════════ Phase 2: Boundary Test (36h) ═══════════════
Application time: 2024-10-20 10:00
Flight time: 2024-10-21 22:00

🔍 Pre-flight check: Time advance...
   Time difference: 36.0 hours
   Required: 36.0 hours
   Boundary test: 36.0 >= 36.0 → TRUE
   ✅ BOUNDARY SATISFIED

✅ Phase 2 PASSED (36h boundary)

✅ FLIGHT APPROVED (All phases passed)
Reason: 申请时间满足提前36小时要求，批准飞行

✓ Result saved: trajectory_S020_TC2.json (0 points)
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S020_TC2.json
# 预期输出: true

# 检查两个阶段
jq '.metadata.test_phases | length' trajectory_S020_TC2.json
# 预期输出: 2

# 检查阶段1时间差
jq '.metadata.test_phases[0].time_difference_hours' trajectory_S020_TC2.json
# 预期输出: 52.0

# 检查阶段2时间差（边界）
jq '.metadata.test_phases[1].time_difference_hours' trajectory_S020_TC2.json
# 预期输出: 36.0
```

---

### TC3: 紧急任务豁免

**时间差**: 0.5小时（30分钟）  
**任务类型**: emergency  
**预期**: APPROVE

```bash
python run_scenario_timeline.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S020_approval_timeline.jsonc \
    --output trajectory_S020_TC3.json \
    --test-case TC3_EmergencyExemption
```

**预期输出**:
```
Loading scenario: S020_ApprovalTimeline
✓ Rules loaded: advance_notice=36h

Test Case: TC3_EmergencyExemption
Current time: 2024-10-20 10:00
Application time: 2024-10-20 10:00
Planned flight time: 2024-10-20 10:30 (30 minutes later)
Flight type: EMERGENCY
Mission: search_and_rescue

🔍 Pre-flight check: Controlled zone...
   Target position: (1000.0, 0.0)
   ✓ IN controlled zone

🔍 Pre-flight check: Exemptions...
   Flight type: emergency
   Mission type: search_and_rescue
   Priority: high
   ✅ EMERGENCY EXEMPTION GRANTED

⚠️  Time advance check BYPASSED (emergency exemption)

✅ FLIGHT APPROVED (Emergency exemption)
Reason: 紧急救援任务豁免时限要求，批准在30分钟后起飞

Emergency details:
  Mission: Search and Rescue
  Priority: High
  Approved by: emergency_response_center
  Regulation: 紧急任务豁免条款

✓ Result saved: trajectory_S020_TC3.json (0 points)
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S020_TC3.json
# 预期输出: true

# 检查豁免类型
jq '.metadata.exemption_applied' trajectory_S020_TC3.json
# 预期输出: "EMERGENCY_MISSION"

# 检查任务类型
jq '.metadata.flight_type' trajectory_S020_TC3.json
# 预期输出: "emergency"
```

---

### TC4: 适飞空域免申请

**申请时间**: null（未申请）  
**空域**: 适飞空域（50m, 非管制区）  
**预期**: APPROVE

```bash
python run_scenario_timeline.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S020_approval_timeline.jsonc \
    --output trajectory_S020_TC4.json \
    --test-case TC4_UncontrolledAirspaceExempt
```

**预期输出**:
```
Loading scenario: S020_ApprovalTimeline
✓ Rules loaded: advance_notice=36h

Test Case: TC4_UncontrolledAirspaceExempt
Current time: 2024-10-20 10:00
Application time: null (NO APPLICATION)
Planned flight time: 2024-10-20 10:30
Target: (300, 0, 50m)

🔍 Pre-flight check: Controlled zone...
   Target position: (300.0, 0.0)
   Distance to zone center: 700.0m > 500.0m
   ✓ OUTSIDE controlled zone

🔍 Pre-flight check: Airspace classification...
   Altitude: 50m < 120m
   Zone: Outside controlled
   ✓ UNCONTROLLED AIRSPACE

🔍 Pre-flight check: Exemptions...
   Airspace: Uncontrolled (< 120m + outside controlled zone)
   Drone type: Light
   ✅ UNCONTROLLED AIRSPACE EXEMPTION

⚠️  Application check BYPASSED (uncontrolled airspace)

✅ FLIGHT APPROVED (Uncontrolled airspace exemption)
Reason: 适飞空域内飞行（高度50m<120m，非管制区域），无需提前申请

Regulation: 中国《条例》第31条第一款
Exemption: 轻型无人机在适飞空域内飞行无需申请

✓ Result saved: trajectory_S020_TC4.json (0 points)
```

**验证**:
```bash
# 检查决策
jq '.metadata.flight_approved' trajectory_S020_TC4.json
# 预期输出: true

# 检查豁免类型
jq '.metadata.exemption_applied' trajectory_S020_TC4.json
# 预期输出: "UNCONTROLLED_AIRSPACE"

# 检查申请时间（应为null）
jq '.metadata.application_time' trajectory_S020_TC4.json
# 预期输出: null
```

---

## 📥 下载结果

```bash
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S020_TC*.json' \
    AirSim-RuleBench/test_logs/
```

---

## ✅ 结果汇总

```bash
# 快速查看所有测试结果
cd AirSim-RuleBench
for tc in TC1 TC2 TC3 TC4; do
    echo "===== $tc ====="
    jq -r '.metadata | "\(.test_case_id): \(if .flight_approved then "✅ APPROVED" else "🚫 REJECTED" end) - \(.reason)"' \
        test_logs/trajectory_S020_${tc}.json
    echo ""
done
```

**预期结果对照表**:

| TC  | 预期决策 | 预期原因                                           | 关键验证             |
| --- | -------- | -------------------------------------------------- | -------------------- |
| TC1 | REJECT   | 申请时间距飞行仅6小时，未满足提前36小时申请要求   | 6h < 36h             |
| TC2 | APPROVE  | 申请时间满足提前36小时要求，批准飞行               | 52h ≥ 36h, 36h ≥ 36h |
| TC3 | APPROVE  | 紧急救援任务豁免时限要求，批准在30分钟后起飞       | emergency豁免        |
| TC4 | APPROVE  | 适飞空域内飞行（高度50m<120m，非管制区域），无需申请 | 适飞空域豁免         |

**通过率**: 3/4 APPROVE, 1/4 REJECT

---

## 🎯 关键验证点

### 1. 时间计算准确性

- TC1: 6小时 → 正确计算
- TC2-1: 52小时 → 正确计算
- TC2-2: 36小时 → 边界测试
- TC3: 0.5小时 → 但豁免
- TC4: 0.5小时 → 但豁免

### 2. 边界值判断

```bash
# TC2阶段2: 恰好36小时
jq '.metadata.test_phases[1] | {
    time_diff: .time_difference_hours,
    required: 36,
    judgment: ">=",
    result: .meets_requirement
}' test_logs/trajectory_S020_TC2.json
```

**预期输出**:
```json
{
  "time_diff": 36.0,
  "required": 36,
  "judgment": ">=",
  "result": true
}
```

### 3. 豁免机制

```bash
# 查看TC3和TC4的豁免类型
jq '.metadata.exemption_applied' test_logs/trajectory_S020_TC3.json
jq '.metadata.exemption_applied' test_logs/trajectory_S020_TC4.json
```

**预期输出**:
```
"EMERGENCY_MISSION"
"UNCONTROLLED_AIRSPACE"
```

---

## 🐛 常见问题

### 1. 时区问题

**现象**: 时间差计算不准确

**原因**: ISO 8601时间字符串未正确处理时区

**解决**:
```python
# 正确处理
from datetime import datetime
dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
```

### 2. 边界判断错误

**现象**: 36小时被拒绝

**原因**: 使用了 `>` 而非 `>=`

**解决**:
```python
# 正确判断
if time_diff >= 36.0:  # 使用 >=
    return "APPROVE"
```

### 3. 豁免优先级错误

**现象**: TC4在适飞空域但还检查时限

**原因**: 检查顺序不对

**解决**:
```python
# 正确顺序
1. 适飞空域检查（优先）
2. 紧急任务检查
3. 时限检查
```

---

## 📝 注意事项

1. **S020不需要飞行模拟**: 纯Pre-flight逻辑检查，轨迹点数为0
2. **TC2是多阶段测试**: 两个阶段在一个TC中，提升质量
3. **时间格式统一**: 使用ISO 8601格式（YYYY-MM-DDTHH:MM:SSZ）
4. **豁免优先级**: 先检查豁免条件，再检查时限
5. **边界判断**: 使用 `>=` 确保36.0小时满足要求

---

**文档版本**: 1.0  
**最后更新**: 2025-11-01  
**维护人**: Claude

