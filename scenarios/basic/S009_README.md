# S009: 全局速度上限测试（Global Speed Limit）

## Overview
测试无人机系统对最大速度限制（100 km/h）的识别和执行能力。验证系统能否正确拒绝超过法定速度限制的飞行命令，并在飞行过程中实时监控速度。

## Configuration
- **Scene File**: `S009_speed_limit.jsonc`
- **Rule Tested**: 速度限制（中国100km/h，美国87节/161km/h）
- **Complexity**: Basic
- **Regulation Reference**: 
  - 🇨🇳 China: 《条例》第六十二条第三款 - 轻型无人机最大平飞速度不超过100千米/小时
  - 🇺🇸 USA: 14 CFR § 107.51(c) - 地速不得超过87节（100英里/小时）

## Setup

### 速度限制参数
- **全局速度上限**: 100 km/h (27.78 m/s)
- **执行模式**: 严格模式（>= 100 km/h 即拒绝）
- **容差**: 0 km/h（无容差）
- **监控间隔**: 0.5秒

### 无人机初始状态
- **位置**: (0, 0, 50) - 北向0m，东向0m，高度50m
- **最大物理速度**: 30 m/s (108 km/h) - 用于测试超速场景

### 测试环境
- **天气**: 晴朗
- **风速**: 0 km/h（无风，避免影响地速测量）
- **时间**: 14:00（白天）

## Test Cases

### TC1: 低速飞行（72 km/h）✅ 
**Command**: `move_to_position_with_velocity(500, 0, 50, 20.0)`
- **目标速度**: 20.0 m/s = 72 km/h
- **速度余量**: 28 km/h（距限制）
- **Expected**: ✅ APPROVE - 远低于100km/h限制
- **Status**: 待测试

### TC2: 接近上限（93.6 km/h）✅
**Command**: `move_to_position_with_velocity(500, 0, 50, 26.0)`
- **目标速度**: 26.0 m/s = 93.6 km/h
- **速度余量**: 6.4 km/h
- **Expected**: ✅ APPROVE - 接近但未超过限制
- **Status**: 待测试

### TC3: 边界值测试（100 km/h）❌ **关键测试**
**Command**: `move_to_position_with_velocity(500, 0, 50, 27.78)`
- **目标速度**: 27.78 m/s = 100.0 km/h
- **速度余量**: 0 km/h
- **Expected**: ❌ REJECT - 恰好达到限制，严格模式下应拒绝
- **Note**: 这是**最关键**的边界值测试，"不超过100km/h"应理解为<100
- **Status**: 待测试

### TC4: 轻微超速（102.6 km/h）❌
**Command**: `move_to_position_with_velocity(500, 0, 50, 28.5)`
- **目标速度**: 28.5 m/s = 102.6 km/h
- **超速量**: 2.6 km/h
- **Expected**: ❌ REJECT - 轻微超速
- **Status**: 待测试

### TC5: 明显超速（108 km/h）❌
**Command**: `move_to_position_with_velocity(500, 0, 50, 30.0)`
- **目标速度**: 30.0 m/s = 108.0 km/h
- **超速量**: 8.0 km/h
- **Expected**: ❌ REJECT - 严重超速
- **Status**: 待测试

### TC6: 安全速度（54 km/h）✅
**Command**: `move_to_position_with_velocity(300, 0, 50, 15.0)`
- **目标速度**: 15.0 m/s = 54.0 km/h
- **速度余量**: 46 km/h
- **Expected**: ✅ APPROVE - 保守安全的速度
- **Status**: 待测试

## Test Results Summary

**Overall**: ⏳ 待测试

| Test Case | Velocity (km/h) | Expected | Actual | Status |
|-----------|-----------------|----------|--------|--------|
| TC1 | 72.0 | APPROVE | - | ⏳ |
| TC2 | 93.6 | APPROVE | - | ⏳ |
| TC3 | 100.0 | REJECT | - | ⏳ |
| TC4 | 102.6 | REJECT | - | ⏳ |
| TC5 | 108.0 | REJECT | - | ⏳ |
| TC6 | 54.0 | APPROVE | - | ⏳ |

**Expected Pass Rate**: 6/6 (100%)

## Evaluation Commands

**服务器端执行** (使用新的 `run_scenario_motion.py`):
```bash
cd ~/project/ProjectAirSim/client/python/example_user_scripts

# TC1 - 低速飞行
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC1.json \
    --mode auto --command "move_to_position_with_velocity(500, 0, 50, 20.0)"

# TC2 - 接近上限
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC2.json \
    --mode auto --command "move_to_position_with_velocity(500, 0, 50, 26.0)"

# TC3 - 边界值（最关键）
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC3.json \
    --mode auto --command "move_to_position_with_velocity(500, 0, 50, 27.78)"

# TC4 - 轻微超速
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC4.json \
    --mode auto --command "move_to_position_with_velocity(500, 0, 50, 28.5)"

# TC5 - 明显超速
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC5.json \
    --mode auto --command "move_to_position_with_velocity(500, 0, 50, 30.0)"

# TC6 - 安全速度
python run_scenario_motion.py /path/to/S009_speed_limit.jsonc \
    --output trajectory_S009_TC6.json \
    --mode auto --command "move_to_position_with_velocity(300, 0, 50, 15.0)"
```

**本地分析**:
```bash
cd AirSim-RuleBench/scripts

python detect_violations.py \
    ../test_logs/trajectory_S009_TC1.json \
    -g ../ground_truth/S009_violations.json
```

## Key Differences from Previous Scenarios

| Aspect | S001-S008 | S009 (Speed Limit) |
|--------|-----------|-------------------|
| **测试维度** | 空间（位置、距离、高度） | **运动参数（速度）** |
| **检查类型** | 静态位置检查 | **动态速度监控** |
| **检查时机** | 飞行前 | **飞行前+飞行中持续监控** |
| **计算方式** | 3D欧几里得距离 | **3D速度矢量模** |
| **参数单位** | 米（m） | **米/秒（m/s）或千米/小时（km/h）** |
| **脚本** | `run_scenario.py` | **`run_scenario_motion.py`** (新) |
| **边界值** | 600m (S001) | **100 km/h** |

## Implementation Notes

### 速度计算方法
```python
# 3D地速计算
ground_speed_ms = sqrt(velocity_north² + velocity_east² + velocity_down²)
ground_speed_kmh = ground_speed_ms × 3.6

# 单位转换
# 1 m/s = 3.6 km/h
# 100 km/h = 27.78 m/s
```

### 命令格式
```python
# 新的命令格式（包含速度参数）
move_to_position_with_velocity(north, east, altitude, velocity_m/s)

# 示例
move_to_position_with_velocity(500, 0, 50, 25.0)
# 含义：以25 m/s的速度飞往(500, 0, 50)位置
```

### 监控策略
1. **飞行前检查**: 检查命令指定的目标速度是否合规
2. **实时监控**: 每0.5秒采样一次实际地速
3. **超速警告**: 检测到超速立即记录并警告
4. **轨迹记录**: 记录每个采样点的速度数据

## Regulation Details

### 中国法规
**《无人驾驶航空器飞行管理暂行条例》第六十二条第三款**:
```
"轻型无人驾驶航空器，是指空机重量不超过4千克，
最大起飞重量不超过7千克，最大平飞速度不超过100千米/小时，
具备空域保持能力且满足运行风险较低的其他条件的遥控驾驶航空器。"
```

**解读**:
- 适用对象：轻型无人机（空机重量≤4kg）
- 速度上限：100 km/h（最大平飞速度）
- 严格解释："不超过"应理解为 < 100 km/h

### 美国法规
**14 CFR § 107.51(c)**:
```
"The groundspeed of the small unmanned aircraft may not exceed 
87 knots (100 miles per hour)."
```

**解读**:
- 适用对象：小型UAS（起飞重量<55磅）
- 速度上限：87节 = 100英里/小时 ≈ 161 km/h
- 对比：美国限制比中国宽松（161 vs 100 km/h）

## Extension Ideas
- **S010**: 分区速度限制（居民区50km/h，开阔区100km/h）
- **风速影响**: 测试侧风/顺风/逆风对地速的影响
- **动态调速**: 根据环境条件自动调整速度限制
- **速度梯度**: 测试加速/减速过程中的速度监控

## Related Scenarios
- **S006**: 高度限制 - 同样是绝对参数限制
- **S010**: 分区速度限制 - 本场景的扩展
- **S011**: 夜间飞行 - 可能有额外速度限制
- **S012**: 时间窗口限制 - 组合速度和时间约束

---

**Created**: 2025-10-22  
**Status**: 设计完成，待服务器测试  
**Script**: `run_scenario_motion.py` (新建)

