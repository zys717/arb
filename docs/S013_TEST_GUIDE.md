# S013 视距内飞行要求（VLOS）- 测试执行指南

**场景ID**: S013_VLOS  
**测试日期**: 2025-10-31  
**测试人员**: Claude & 张耘实  
**预计时间**: ~8分钟（5个测试用例）

---

## 📋 测试前准备

### 1. 文件准备

需要上传的文件：
- ✅ `scenarios/basic/S013_vlos_requirement.jsonc` - 场景配置
- ✅ `scripts/run_scenario_vlos.py` - 新的测试脚本（用于S013-S016）

### 2. 上传文件到服务器

```bash
# 在本地执行（当前目录：/Users/zhangyunshi/Desktop/实习/airsim/）

# 1. 上传场景配置文件
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S013_vlos_requirement.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 2. 上传新的测试脚本
scp -P 10427 \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/scripts/run_scenario_vlos.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

**预期输出**:
```
S013_vlos_requirement.jsonc            100%   10KB   1.5MB/s   00:00
run_scenario_vlos.py                   100%   26KB   2.2MB/s   00:00
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

| TC | 目标位置 | 水平距离 | VLOS范围 | 预期 | 测试重点 |
|----|----------|----------|----------|------|----------|
| TC1 | (200,0,50) | 200m | 500m | ✅ APPROVE | 近距离 |
| TC2 | (400,0,50) | 400m | 500m | ✅ APPROVE | 中距离 |
| TC3 | (500,0,50) | 500m | 500m | ✅ APPROVE | 边界值 ⭐ |
| TC4 | (600,0,50) | 600m | 500m | ❌ REJECT | 超视距 ⭐⭐ |
| TC5 | (800,0,50) | 800m | 500m | ❌ REJECT | 远超视距 |

**操作员位置**: (0, 0, 0) - 地面  
**VLOS范围**: 500m（水平距离）

---

## 📝 详细测试步骤

### TC1: 近距离飞行 ✅ APPROVE

**测试目标**: 验证基础合规性（200m < 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S013_vlos_requirement.jsonc \
    --output trajectory_S013_TC1.json \
    --mode auto \
    --test-case TC1
```

**预期输出**:
```
Target: N=200.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 在视距内（200.0m <= 500.0m）

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

---

### TC2: 中距离飞行 ✅ APPROVE

**测试目标**: 验证中距离合规性（400m < 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S013_vlos_requirement.jsonc \
    --output trajectory_S013_TC2.json \
    --mode auto \
    --test-case TC2
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

---

### TC3: 边界值测试（500m）✅ APPROVE ⭐

**测试目标**: 验证边界值处理（500m = 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S013_vlos_requirement.jsonc \
    --output trajectory_S013_TC3.json \
    --mode auto \
    --test-case TC3
```

**预期输出**:
```
Target: N=500.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ✓ 在视距内（500.0m <= 500.0m）

✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
```

**预期结果**: ✅ 批准，完整轨迹

**关键验证**:
- ✅ 边界值500m使用 <= 判断，允许
- ✅ 水平距离正好500m
- ✅ 边界值包含（不拒绝）

---

### TC4: 超视距飞行（600m）❌ REJECT ⭐⭐ 核心测试

**测试目标**: 验证超视距检测（600m > 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S013_vlos_requirement.jsonc \
    --output trajectory_S013_TC4.json \
    --mode auto \
    --test-case TC4
```

**预期输出**:
```
Target: N=600.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ❌ 超出视距范围（600.0m > 500.0m），违反VLOS要求（§32(5) / Part 107.31）

🚫 COMMAND REJECTED (VLOS violation)
✓ Trajectory saved: trajectory_S013_TC4.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ 正确检测超视距（600m > 500m）
- ✅ 拒绝飞行命令
- ✅ 拒绝理由清晰，包含距离和法规依据
- ✅ 仅记录起点（未起飞）

**这是最核心的测试**：证明VLOS距离检测正确实现

---

### TC5: 远超视距飞行（800m）❌ REJECT

**测试目标**: 验证严重超视距检测（800m >> 500m）

**命令**:
```bash
python run_scenario_vlos.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S013_vlos_requirement.jsonc \
    --output trajectory_S013_TC5.json \
    --mode auto \
    --test-case TC5
```

**预期输出**:
```
Target: N=800.0, E=0.0, Alt=50.0m

🔍 Pre-flight check: VLOS requirements...
   ❌ 超出视距范围（800.0m > 500.0m），违反VLOS要求（§32(5) / Part 107.31）

🚫 COMMAND REJECTED (VLOS violation)
✓ Trajectory saved: trajectory_S013_TC5.json (1 points)
```

**预期结果**: ❌ 拒绝，仅有起点

**关键验证**:
- ✅ 正确检测严重超视距（800m是500m的1.6倍）
- ✅ 拒绝飞行命令

---

## 📦 下载测试结果

```bash
# 在本地执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S013_TC*.json' \
    /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/
```

**注意**: 必须用单引号包裹远程路径。

---

## ✅ 验证清单

### 1. 文件检查

```bash
# 在本地执行
ls -lh /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S013_TC*.json
```

**预期结果**:
```
trajectory_S013_TC1.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S013_TC2.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S013_TC3.json    ~100KB   ✅ 批准，完整轨迹
trajectory_S013_TC4.json    ~1KB     ❌ 拒绝，仅起点
trajectory_S013_TC5.json    ~1KB     ❌ 拒绝，仅起点
```

**批准/拒绝分布**:
- ✅ APPROVE: 3个 (TC1, TC2, TC3)
- ❌ REJECT: 2个 (TC4, TC5)

### 2. 快速验证命令

```bash
# 检查文件大小
wc -l /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S013_TC*.json
```

**预期**:
- TC1/TC2/TC3: 大文件（~600-700行）
- TC4/TC5: 小文件（~36行）

### 3. 关键测试验证

#### TC3 - 边界值测试
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S013_TC3.json | head -20
```
**必须**:
- ✅ `"success": true`
- ✅ 完整轨迹（~600点）

#### TC4 - 超视距检测（核心）
```bash
cat /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench/test_logs/trajectory_S013_TC4.json | head -20
```
**必须包含**:
- `"command_rejected": true`
- `"reason": "VLOS violation"`
- `"violations": ["超出视距范围"]`
- `"trajectory_points": 1`

---

## 🎯 成功标准

### 必须全部通过

1. ✅ **TC1**: 近距离200m批准
2. ✅ **TC2**: 中距离400m批准
3. ✅ **TC3**: 边界值500m批准 ⭐
4. ✅ **TC4**: 超视距600m拒绝 ⭐⭐
5. ✅ **TC5**: 远超视距800m拒绝

### 距离检测验证

| 距离 | 判断 | 预期 | 验证 |
|------|------|------|------|
| 200m | < 500m | ✅ APPROVE | TC1 |
| 400m | < 500m | ✅ APPROVE | TC2 |
| 500m | = 500m | ✅ APPROVE | TC3 ⭐ |
| 600m | > 500m | ❌ REJECT | TC4 ⭐⭐ |
| 800m | > 500m | ❌ REJECT | TC5 |

**关键**: TC3边界值必须批准（使用 <=），TC4必须拒绝（正确检测超视距）

---

## ⚠️ 常见问题

### 问题1: TC3被错误拒绝

**原因**: 边界值判断使用了 `<` 而非 `<=`

**排查**:
```python
# 错误实现
if distance > max_vlos_range:  # 应该用 > 而非 >=

# 正确实现
if distance > max_vlos_range:
    REJECT
```

### 问题2: TC4被错误批准

**原因**: 
1. 距离计算错误
2. VLOS检查未触发
3. 判断逻辑错误

**排查**:
- 检查600m > 500m判断是否正确
- 检查操作员位置是否正确（0, 0, 0）
- 检查距离计算方法（水平距离）

### 问题3: 找不到vlos_restrictions配置

**原因**: 场景文件未包含`vlos_restrictions`字段

**解决**: 确保场景文件上传成功且包含完整配置

---

## 📊 预期测试时长

- 每个测试用例: ~1-2分钟
- 总计5个用例: ~5-10分钟
- 文件上传/下载: ~2分钟
- 结果验证: ~2分钟

**总时长**: ~10-15分钟

---

## 📝 测试注意事项

1. ⚡ **距离计算**: 使用水平距离（2D），不含高度
2. 🎯 **边界值**: 500m使用 <= 判断，允许
3. 📏 **操作员位置**: (0, 0, 0) 地面固定
4. 🚁 **起始位置**: (0, 0, 50) 操作员正上方
5. 🔄 **新脚本**: 使用`run_scenario_vlos.py`（720行，比motion精简48%）

---

## 🔗 相关场景

- **S012**: 时间窗口限制（组合规则基础）
- **S014**: 超视距飞行（BVLOS）豁免
- **S015**: 视觉观察员协作

---

## 🚀 新脚本特点

**run_scenario_vlos.py**:
- ✅ 专注于VLOS和避让场景（S013-S016）
- ✅ 720行（vs motion的1385行，精简48%）
- ✅ 移除速度检查、时间窗口检查
- ✅ 仅保留VLOS距离检查
- ✅ 代码更简洁，易于维护

---

**测试指南版本**: 1.0  
**最后更新**: 2025-10-31  
**适用脚本**: run_scenario_vlos.py v1.0（新脚本）  
**测试用例数**: 5个（重点测试距离判断和边界值）

