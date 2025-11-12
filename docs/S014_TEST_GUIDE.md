# S014 超视距飞行豁免（BVLOS Waiver）- 测试执行指南

**场景ID**: S014_BVLOS_Waiver  
**测试日期**: 2025-10-31  
**测试人员**: Claude & 张耘实  
**预计时间**: ~12分钟（6个测试用例）

---

## 📋 测试前准备

### 1. 文件准备

需要上传的文件：
- ✅ `scenarios/basic/S014_bvlos_waiver.jsonc` - 场景配置
- ✅ `scripts/run_scenario_vlos.py` - 测试脚本（与S013共用）

### 2. 上传文件到服务器

```bash
# 在本地执行（当前目录：/Users/zhangyunshi/Desktop/实习/airsim/）

# 1. 上传场景配置文件
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S014_bvlos_waiver.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. 测试脚本已在S013时上传，无需重复上传
```

**预期输出**:
```
S014_bvlos_waiver.jsonc                100%   18KB   2.0MB/s   00:00
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

| TC | 目标位置 | 距离 | 豁免 | 预期 | 测试重点 |
|----|----------|------|------|------|----------|
| TC1 | (400,0,50) | 400m | 无 | ✅ APPROVE | 基础VLOS |
| TC2 | (600,0,50) | 600m | 无 | ❌ REJECT | 无豁免超视距 ⭐⭐ |
| TC3 | (600,0,50) | 600m | 观察员 | ✅ APPROVE | 观察员豁免 ⭐⭐⭐ |
| TC4 | (1500,0,50) | 1500m | 技术 | ✅ APPROVE | 技术手段 ⭐⭐ |
| TC5 | (3000,0,50) | 3000m | 许可 | ✅ APPROVE | 特殊许可 ⭐⭐ |
| TC6 | (6000,0,50) | 6000m | 许可 | ❌ REJECT | 超出豁免 ⭐⭐ |

**操作员位置**: (0, 0, 0) - 地面  
**观察员位置**: (600, 0, 0) - 地面  
**基础VLOS范围**: 500m

---

## 📝 详细测试步骤

### TC1: 基础VLOS内飞行 ✅ APPROVE

**测试目标**: 验证基础VLOS内无需豁免即可飞行（400m < 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC1.json \
    --mode auto \
    --test-case TC1
```

**预期输出**:
```
Target: N=400.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 在视距内（400.0m <= 500.0m）

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**验证要点**:
- ✅ 距离400m < 500m基础VLOS
- ✅ 无需豁免即可批准
- ✅ 完整飞行轨迹

---

### TC2: 无豁免超视距飞行 ❌ REJECT ⭐⭐ 关键测试

**测试目标**: 验证无豁免时超视距飞行被拒绝（600m > 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC2.json \
    --mode auto \
    --test-case TC2
```

**预期输出**:
```
Target: N=600.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ❌ 超出视距范围（600.0m > 500.0m）
   ❌ 无可用BVLOS豁免

🚫 COMMAND REJECTED (VLOS violation, no waiver)
✓ Trajectory saved: trajectory_S014_TC2.json (1 points)
```

**预期结果**: ❌ 拒绝，仅起点

**验证要点**:
- ✅ 正确检测超视距（600m > 500m）
- ✅ 正确识别无豁免
- ✅ 拒绝理由说明"无豁免"
- ✅ 仅记录起点（未起飞）

**这是关键对照测试**：证明无豁免时超视距会被拒绝

---

### TC3: 观察员豁免生效 ✅ APPROVE ⭐⭐⭐ 核心测试

**测试目标**: 验证启用观察员豁免后，可飞至观察员视距内（600m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC3.json \
    --mode auto \
    --test-case TC3
```

**预期输出**:
```
Target: N=600.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 超出操作员VLOS（600.0m > 500.0m）
   
🔍 Checking BVLOS waivers...
   ✓ Visual Observer waiver enabled
   ✓ Observer position: (600.0, 0.0, 0.0)
   ✓ Distance to observer: 0.0m
   ✓ Within observer VLOS: 0.0m <= 500.0m

✅ WAIVER APPLIED: Visual Observer
✅ All pre-flight checks passed (with waiver)
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**验证要点**:
- ✅ 识别观察员豁免已启用
- ✅ 计算目标与观察员的距离
- ✅ 目标在观察员VLOS内（0m < 500m）
- ✅ 批准理由说明"观察员豁免"
- ✅ 完整飞行轨迹

**这是最核心的测试**：验证观察员豁免机制正确实现

**关键理解**:
- 操作员在(0,0,0)，目标在(600,0,50)，距离600m > 500m
- 观察员在(600,0,0)，目标在(600,0,50)，距离=0m < 500m
- 观察员可以直接看到目标 → 批准 ✅

---

### TC4: 技术手段豁免生效 ✅ APPROVE ⭐⭐

**测试目标**: 验证启用技术手段豁免后，可飞至雷达覆盖内（1500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC4.json \
    --mode auto \
    --test-case TC4
```

**预期输出**:
```
Target: N=1500.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 超出操作员VLOS（1500.0m > 500.0m）
   
🔍 Checking BVLOS waivers...
   ✓ Technical Means waiver enabled
   ✓ Radar coverage: 2000.0m
   ✓ Distance to operator: 1500.0m
   ✓ Within radar coverage: 1500.0m <= 2000.0m
   ✓ Data link: active
   ✓ Real-time tracking: enabled

✅ WAIVER APPLIED: Technical Means (Radar)
✅ All pre-flight checks passed (with waiver)
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**验证要点**:
- ✅ 识别技术手段豁免已启用
- ✅ 检查雷达覆盖范围（2000m）
- ✅ 目标在雷达覆盖内（1500m < 2000m）
- ✅ 批准理由说明"技术手段豁免"
- ✅ 完整飞行轨迹

**这是重要测试**：验证技术系统支持的远距离BVLOS

---

### TC5: 特殊许可豁免生效 ✅ APPROVE ⭐⭐

**测试目标**: 验证启用特殊许可后，可飞至最远距离（3000m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC5.json \
    --mode auto \
    --test-case TC5
```

**预期输出**:
```
Target: N=3000.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 超出操作员VLOS（3000.0m > 500.0m）
   
🔍 Checking BVLOS waivers...
   ✓ Special Permit waiver enabled
   ✓ Permit: CAAC-BVLOS-2025-001
   ✓ Approved area: Test Zone Alpha
   ✓ Max range: 5000.0m
   ✓ Distance to operator: 3000.0m
   ✓ Within permit range: 3000.0m <= 5000.0m

✅ WAIVER APPLIED: Special Permit
✅ All pre-flight checks passed (with waiver)
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**验证要点**:
- ✅ 识别特殊许可豁免已启用
- ✅ 检查许可范围（5000m）
- ✅ 目标在许可范围内（3000m < 5000m）
- ✅ 显示许可编号和批准区域
- ✅ 批准理由说明"特殊许可豁免"
- ✅ 完整飞行轨迹

**这是最远距离测试**：验证最高级别豁免的有效性

---

### TC6: 超出豁免上限 ❌ REJECT ⭐⭐ 边界测试

**测试目标**: 验证即使有豁免，超出其范围仍会被拒绝（6000m > 5000m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S014_bvlos_waiver.jsonc \
    --output trajectory_S014_TC6.json \
    --mode auto \
    --test-case TC6
```

**预期输出**:
```
Target: N=6000.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 超出操作员VLOS（6000.0m > 500.0m）
   
🔍 Checking BVLOS waivers...
   ✓ Special Permit waiver enabled
   ✓ Permit max range: 5000.0m
   ❌ Distance exceeds permit range（6000.0m > 5000.0m）

🚫 COMMAND REJECTED (exceeds waiver limit)
   Waiver type: Special Permit
   Waiver limit: 5000.0m
   Requested distance: 6000.0m
   Exceeds by: 1000.0m (20%)
   
✓ Trajectory saved: trajectory_S014_TC6.json (1 points)
```

**预期结果**: ❌ 拒绝，仅起点

**验证要点**:
- ✅ 识别特殊许可豁免已启用
- ✅ 检查许可上限（5000m）
- ✅ 正确检测超出范围（6000m > 5000m）
- ✅ 拒绝理由详细说明豁免限制
- ✅ 显示超出的距离和百分比
- ✅ 仅记录起点（未起飞）

**这是关键边界测试**：验证豁免不能无限扩展

---

## 📦 下载测试结果

```bash
# 在本地执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S014_TC*.json' \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/
```

**注意**: 必须用单引号包裹远程路径。

---

## ✅ 验证清单

### 1. 文件检查

```bash
# 在本地执行
ls -lh /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S014_TC*.json
```

**预期结果**:
```
trajectory_S014_TC1.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S014_TC2.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S014_TC3.json    ~200KB   ✅ 批准，完整轨迹
trajectory_S014_TC4.json    ~400KB   ✅ 批准，完整轨迹
trajectory_S014_TC5.json    ~800KB   ✅ 批准，完整轨迹
trajectory_S014_TC6.json    ~1KB     ❌ 拒绝，仅起点
```

**批准/拒绝分布**:
- ✅ APPROVE: 4个 (TC1, TC3, TC4, TC5)
- ❌ REJECT: 2个 (TC2, TC6)

### 2. 快速验证命令

```bash
# 检查文件大小
wc -l /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S014_TC*.json
```

**预期**:
- TC1: ~700行（近距离）
- TC2: ~36行（拒绝）
- TC3: ~1200行（中距离）
- TC4: ~3000行（远距离）
- TC5: ~6000行（超远距离）
- TC6: ~36行（拒绝）

### 3. 关键测试验证

#### TC2 - 无豁免拒绝（对照测试）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S014_TC2.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"reason": "VLOS violation, no waiver"` 或类似
- `"trajectory_points": 1`

#### TC3 - 观察员豁免（核心测试）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S014_TC3.json | head -20
```
**必须包含**:
- `"success": true`
- `"waiver_applied": "Visual Observer"` 或在reason中说明
- `"trajectory_points": 大量点`

#### TC6 - 超出豁免上限（边界测试）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S014_TC6.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"reason": "exceeds waiver limit"` 或类似
- `"trajectory_points": 1`

---

## 🎯 成功标准

### 必须全部通过

1. ✅ **TC1**: 基础VLOS内（400m）批准
2. ✅ **TC2**: 无豁免超视距（600m）拒绝 ⭐⭐
3. ✅ **TC3**: 观察员豁免（600m）批准 ⭐⭐⭐
4. ✅ **TC4**: 技术手段豁免（1500m）批准 ⭐⭐
5. ✅ **TC5**: 特殊许可豁免（3000m）批准 ⭐⭐
6. ✅ **TC6**: 超出豁免上限（6000m）拒绝 ⭐⭐

### 豁免机制验证

| 测试 | 豁免 | 范围检查 | 预期 | 验证 |
|------|------|----------|------|------|
| TC2 | 无 | 600m > 500m | ❌ REJECT | 对照 |
| TC3 | 观察员 | 0m < 500m (observer) | ✅ APPROVE | 核心 ⭐⭐⭐ |
| TC4 | 技术 | 1500m < 2000m (radar) | ✅ APPROVE | 重要 ⭐⭐ |
| TC5 | 许可 | 3000m < 5000m (permit) | ✅ APPROVE | 重要 ⭐⭐ |
| TC6 | 许可 | 6000m > 5000m (limit) | ❌ REJECT | 边界 ⭐⭐ |

**关键验证**:
- TC2 vs TC3：同样600m，无豁免拒绝，有豁免批准
- TC5 vs TC6：同样有许可，3000m批准，6000m拒绝

---

## ⚠️ 常见问题

### 问题1: TC3被错误拒绝

**原因**: 
1. 观察员豁免未正确启用
2. 观察员位置计算错误
3. 距离判断逻辑错误

**排查**:
```python
# 检查观察员位置
observer_position = (600, 0, 0)
target_position = (600, 0, 50)
distance = sqrt((600-600)^2 + (0-0)^2 + (50-0)^2) = 50m

# 应该批准
50m < 500m (observer_vlos_range) → APPROVE ✅
```

### 问题2: TC2被错误批准

**原因**: 
1. 基础VLOS检查未执行
2. 豁免检查逻辑错误
3. 错误启用了豁免

**排查**:
- 确认TC2配置中 `waivers_enabled = []`（空数组）
- 确认600m > 500m判断正确
- 确认无豁免时应该拒绝

### 问题3: TC6被错误批准

**原因**: 
1. 豁免上限检查缺失
2. 距离比较错误
3. 特殊许可判断逻辑错误

**排查**:
```python
# 应该拒绝
permit_max_range = 5000m
target_distance = 6000m
6000m > 5000m → REJECT ✅
```

### 问题4: 豁免类型识别错误

**原因**: 
1. waivers_enabled 配置未正确解析
2. 豁免ID匹配错误
3. 豁免类型判断错误

**排查**:
- 检查场景文件中的豁免配置
- 检查test_case中的waivers_enabled字段
- 确认豁免ID匹配（W001, W002, W003）

---

## 📊 预期测试时长

- 每个测试用例: ~2-3分钟
- 总计6个用例: ~12-18分钟
- 文件上传/下载: ~3分钟
- 结果验证: ~3分钟

**总时长**: ~20-25分钟

---

## 📝 测试注意事项

1. ⚡ **豁免配置**: 每个TC的waivers_enabled字段不同
2. 🎯 **观察员位置**: (600, 0, 0) 地面固定
3. 📏 **距离计算**: 水平距离（2D），不含高度
4. 🔄 **豁免类型**: 观察员、技术手段、特殊许可
5. 📊 **范围扩展**: 500m → 1100m → 2000m → 5000m
6. 🚫 **上限检查**: 即使有豁免也有最大范围

---

## 🔗 相关场景

- **S013**: VLOS要求（基础场景）
- **S015**: 视觉观察员协作（观察员豁免扩展）
- **S016**: 探测与避让（技术手段豁免扩展）

---

## 🚀 实现要点

### 豁免检查逻辑流程

```
1. 计算目标与操作员距离
2. 距离 <= 500m？
   ├─ 是 → 直接批准（无需豁免）
   └─ 否 → 继续检查
3. 检查waivers_enabled是否为空？
   ├─ 是（空）→ 拒绝（无豁免）→ TC2
   └─ 否（有豁免）→ 继续检查
4. 遍历启用的豁免：
   ├─ 观察员豁免 (W001)：
   │   └─ 计算目标与观察员距离
   │   └─ 距离 <= 500m？→ 批准 → TC3
   ├─ 技术手段豁免 (W002)：
   │   └─ 距离 <= 2000m（雷达覆盖）？→ 批准 → TC4
   └─ 特殊许可豁免 (W003)：
       └─ 距离 <= 5000m（许可范围）？→ 批准 → TC5
5. 所有豁免都不满足？
   └─ 拒绝（超出豁免限制）→ TC6
```

### 观察员覆盖计算

```python
# TC3 场景
operator_pos = (0, 0, 0)
observer_pos = (600, 0, 0)
target_pos = (600, 0, 50)

# 距离计算（2D水平距离）
dist_to_operator = sqrt((600-0)^2 + (0-0)^2) = 600m
dist_to_observer = sqrt((600-600)^2 + (0-0)^2) = 0m

# 判断
dist_to_operator = 600m > 500m → 超出操作员VLOS
dist_to_observer = 0m <= 500m → 在观察员VLOS内 ✅
→ 批准（观察员豁免生效）
```

---

**测试指南版本**: 1.0  
**最后更新**: 2025-10-31  
**适用脚本**: run_scenario_vlos.py v1.0  
**测试用例数**: 6个（全面测试豁免机制）

**核心测试**: TC2（无豁免拒绝）、TC3（观察员豁免）、TC6（超出豁免上限）

