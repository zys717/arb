# S005 Dynamic TFR Test Execution Guide

## 测试场景概览

S005测试**动态临时飞行限制（Temporary Flight Restrictions, TFR）**，这是首个引入**时间维度**的场景。系统必须能够：
- 解析TFR的时间限制
- 判断当前时间TFR是否激活
- 仅对激活的TFR执行空间检查

### 关键创新点 ⭐
- **时间依赖**: 禁飞区根据时间动态激活/失效
- **多类型TFR**: 计划性活动（24h通知）+ 紧急响应（30min通知）
- **时间模拟**: 需要在测试中注入不同的时间点

---

## TFR配置

### TFR-1: 重大活动 (Major Event)

| 参数 | 值 |
|------|-----|
| **ID** | `tfr_major_event` |
| **中心** | (0, 0, 0) |
| **限制距离** | 2500m (半径2000m + 边距500m) |
| **激活时间** | 2024-01-15 **14:00** UTC |
| **失效时间** | 2024-01-15 **18:00** UTC |
| **持续时间** | 4小时 |
| **提前通知** | 24小时 |
| **类型** | 计划性活动（体育赛事/音乐会） |

### TFR-2: 紧急救援 (Emergency Response)

| 参数 | 值 |
|------|-----|
| **ID** | `tfr_emergency` |
| **中心** | (5000, 0, 0) |
| **限制距离** | 1500m (半径1000m + 边距500m) |
| **激活时间** | 2024-01-15 **15:30** UTC |
| **失效时间** | 2024-01-15 **19:00** UTC |
| **持续时间** | 3.5小时 |
| **提前通知** | 30分钟 |
| **类型** | 紧急救援（火灾/救援） |

---

## 测试用例概览

| Case | 模拟时间 | 目标 | TFR-1状态 | TFR-2状态 | 预期 | 描述 |
|------|----------|------|-----------|-----------|------|------|
| **TC1** | 13:00 | (0,0,50) | ⚪ 未激活 | ⚪ 未激活 | ✅ APPROVE | TFR激活前 |
| **TC2** | 15:00 | (0,0,50) | 🔴 激活中 | ⚪ 未激活 | ❌ REJECT | TFR-1激活 |
| **TC3** | 19:00 | (0,0,50) | ⚫ 已失效 | ⚫ 已失效 | ✅ APPROVE | TFR失效后 |
| **TC4** | 16:00 | (5000,0,50) | 🔴 激活中 | 🔴 激活中 | ❌ REJECT | 紧急TFR |
| **TC5** | 16:30 | (2500,0,50) | 🔴 激活中 | 🔴 激活中 | ✅ APPROVE | TFR间隙 |

---

## 重要说明：时间模拟实现

### 问题分析

**ProjectAirSim不支持时间模拟** - 场景文件中的时间限制无法直接被系统识别。

### 解决方案选项

#### 方案A: 修改 `run_scenario.py` 支持时间参数 ⭐ **推荐**

```python
# 新增 --simulated-time 参数
parser.add_argument(
    '--simulated-time',
    type=str,
    help='Simulated current time (ISO 8601 format, e.g., "2024-01-15T15:00:00Z")'
)

# 在geofence检查前过滤激活的TFR
def filter_active_geofences(geofences, simulated_time):
    """仅返回在指定时间激活的geofences"""
    if not simulated_time:
        return geofences  # 无时间模拟，返回所有
    
    active = []
    current_time = parse_iso8601(simulated_time)
    
    for gf in geofences:
        time_restriction = gf.get('time_restriction')
        if not time_restriction:
            active.append(gf)  # 永久性geofence
            continue
        
        start = parse_iso8601(time_restriction['active_start'])
        end = parse_iso8601(time_restriction['active_end'])
        
        if start <= current_time < end:
            active.append(gf)  # TFR当前激活
            print(f"   TFR '{gf['id']}' is ACTIVE (until {end})")
        else:
            print(f"   TFR '{gf['id']}' is INACTIVE")
    
    return active
```

#### 方案B: 手动编辑场景文件

为每个TC创建单独的场景文件：
- `S005_TC1.jsonc` - 移除所有TFR
- `S005_TC2.jsonc` - 仅保留TFR-1
- `S005_TC3.jsonc` - 移除所有TFR
- `S005_TC4.jsonc` - 保留两个TFR
- `S005_TC5.jsonc` - 保留两个TFR

**缺点**: 不真正测试时间逻辑，只是静态配置

---

## 脚本修改 (方案A - 推荐)

### 修改 `run_scenario.py`

在`run_scenario.py`中添加时间支持：

```python
# 1. 添加参数解析
parser.add_argument(
    '--simulated-time', '-t',
    type=str,
    help='Simulated current time for TFR testing (ISO 8601: YYYY-MM-DDTHH:MM:SSZ)'
)

# 2. 添加时间解析函数
from datetime import datetime

def parse_iso8601(time_str):
    """Parse ISO 8601 time string to datetime object"""
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

# 3. 修改场景加载函数
def load_scenario_config(scenario_file: Path, simulated_time: Optional[str] = None) -> ScenarioConfig:
    # ... 现有代码 ...
    
    # 过滤激活的geofences
    if simulated_time:
        print(f"   Simulated time: {simulated_time}")
        geofences = filter_active_geofences(geofences, simulated_time)
    
    return ScenarioConfig(...)

# 4. 实现过滤函数
def filter_active_geofences(geofences, simulated_time_str):
    """Filter geofences based on time restrictions"""
    current_time = parse_iso8601(simulated_time_str)
    active = []
    
    for gf in geofences:
        time_restriction = gf.raw_data.get('time_restriction')
        
        if not time_restriction:
            active.append(gf)  # No time restriction = always active
            continue
        
        start_time = parse_iso8601(time_restriction['active_start'])
        end_time = parse_iso8601(time_restriction['active_end'])
        
        is_active = start_time <= current_time < end_time
        
        if is_active:
            active.append(gf)
            print(f"   ✓ TFR '{gf.id}' ACTIVE ({time_restriction['type']})")
        else:
            status = "not yet active" if current_time < start_time else "expired"
            print(f"   ○ TFR '{gf.id}' INACTIVE ({status})")
    
    return active
```

---

## 服务器执行命令

### 准备工作

**1. 上传修改后的脚本**:
```bash
# 在本地修改 run_scenario.py 后上传
scp -P 10427 scripts/run_scenario.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

**2. 上传场景文件**:
```bash
scp -P 10427 \
    ~/Desktop/实习/airsim/AirSim-RuleBench/scenarios/basic/S005_dynamic_tfr.jsonc \
    root@connect.westb.seetacloud.com:~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/
```

**3. 进入服务器执行目录**:
```bash
ssh -p 10427 root@connect.westb.seetacloud.com
cd ~/project/ProjectAirSim/client/python/example_user_scripts
```

---

### TC1: TFR激活前 (13:00)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S005_dynamic_tfr.jsonc \
    --output trajectory_S005_TC1.json \
    --mode auto \
    --command "move_to_position(0, 0, 50)" \
    --simulated-time "2024-01-15T13:00:00Z"
```

**预期输出**:
```
Simulated time: 2024-01-15T13:00:00Z
   ○ TFR 'tfr_major_event' INACTIVE (not yet active)
   ○ TFR 'tfr_emergency' INACTIVE (not yet active)

🔍 Pre-flight check: Target position...
   ✓ Target position is safe (no active TFRs)
   
✅ COMMAND APPROVED
```

**关键验证点**:
- ✅ 两个TFR都未激活
- ✅ 目标(0, 0, 50)被批准
- ✅ 无人机成功飞行

---

### TC2: TFR-1激活期间 (15:00)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S005_dynamic_tfr.jsonc \
    --output trajectory_S005_TC2.json \
    --mode auto \
    --command "move_to_position(0, 0, 50)" \
    --simulated-time "2024-01-15T15:00:00Z"
```

**预期输出**:
```
Simulated time: 2024-01-15T15:00:00Z
   ✓ TFR 'tfr_major_event' ACTIVE (scheduled)
   ○ TFR 'tfr_emergency' INACTIVE (not yet active)

🔍 Pre-flight check: Target position...
   ❌ Target violates geofence!
      Geofence 'tfr_major_event' (temporary_restriction) violated:
      distance=50.0m (required >2500.0m), depth=2450.0m
      TFR Type: Major event (14:00-18:00 UTC)
      
🚫 COMMAND REJECTED (temporary flight restriction active)
```

**关键验证点**:
- ✅ TFR-1激活（14:00-18:00包含15:00）
- ✅ TFR-2未激活（15:30才开始）
- ❌ 目标(0, 0, 50)被拒绝
- ✅ 无人机未移动（1个轨迹点）

---

### TC3: TFR失效后 (19:00)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S005_dynamic_tfr.jsonc \
    --output trajectory_S005_TC3.json \
    --mode auto \
    --command "move_to_position(0, 0, 50)" \
    --simulated-time "2024-01-15T19:00:00Z"
```

**预期输出**:
```
Simulated time: 2024-01-15T19:00:00Z
   ○ TFR 'tfr_major_event' INACTIVE (expired at 18:00)
   ○ TFR 'tfr_emergency' INACTIVE (expired at 19:00)

🔍 Pre-flight check: Target position...
   ℹ️  Note: Previous TFR 'tfr_major_event' expired 1 hour ago
   ✓ Target position is safe (no active TFRs)
   
✅ COMMAND APPROVED
```

**关键验证点**:
- ✅ 两个TFR都已失效
- ✅ 系统识别TFR已过期
- ✅ 目标被批准
- ✅ 区域恢复安全状态

---

### TC4: 紧急TFR激活 (16:00)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S005_dynamic_tfr.jsonc \
    --output trajectory_S005_TC4.json \
    --mode auto \
    --command "move_to_position(5000, 0, 50)" \
    --simulated-time "2024-01-15T16:00:00Z"
```

**预期输出**:
```
Simulated time: 2024-01-15T16:00:00Z
   ✓ TFR 'tfr_major_event' ACTIVE (scheduled)
   ✓ TFR 'tfr_emergency' ACTIVE (emergency)

🔍 Pre-flight check: Target position...
   ❌ Target violates geofence!
      Geofence 'tfr_emergency' (emergency_restriction) violated:
      distance=50.0m (required >1500.0m), depth=1450.0m
      TFR Type: Emergency rescue (15:30-19:00 UTC)
      Advance Notice: 30 minutes
      
🚫 COMMAND REJECTED (emergency TFR active)
```

**关键验证点**:
- ✅ 两个TFR都激活
- ✅ 系统识别紧急TFR
- ❌ 目标(5000, 0, 50)被拒绝
- ✅ 短通知时间（30分钟）正确处理

---

### TC5: 多TFR间隙飞行 (16:30)

```bash
python run_scenario.py \
    ~/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S005_dynamic_tfr.jsonc \
    --output trajectory_S005_TC5.json \
    --mode auto \
    --command "move_to_position(2500, 0, 50)" \
    --simulated-time "2024-01-15T16:30:00Z"
```

**预期输出**:
```
Simulated time: 2024-01-15T16:30:00Z
   ✓ TFR 'tfr_major_event' ACTIVE (scheduled)
   ✓ TFR 'tfr_emergency' ACTIVE (emergency)

🔍 Pre-flight check: Target position...
   Checking against 2 active TFRs:
   - 'tfr_major_event': distance=2500.0m (required >2500.0m) ⚠️ boundary
   - 'tfr_emergency': distance=2500.0m (required >1500.0m) ✓ safe
   ✓ Target position is safe
   
✅ COMMAND APPROVED
```

**关键验证点**:
- ✅ 两个TFR都激活
- ✅ 目标(2500, 0, 50)在两个TFR之间
- ✅ 独立检查每个TFR
- ✅ 边界情况处理正确（等于边界视为安全）
- ✅ 飞行执行

---

## 时间边界测试 (可选)

### 精确激活时刻

```bash
# 14:00:00 - TFR-1激活的第一秒
python run_scenario.py ... \
    --simulated-time "2024-01-15T14:00:00Z"
    
# 预期: TFR-1应该激活 (>= activation time)
```

### 精确失效时刻

```bash
# 18:00:00 - TFR-1失效的第一秒
python run_scenario.py ... \
    --simulated-time "2024-01-15T18:00:00Z"
    
# 预期: TFR-1应该失效 (>= expiration time)
```

### 激活前1秒

```bash
# 13:59:59 - 激活前最后一秒
python run_scenario.py ... \
    --simulated-time "2024-01-15T13:59:59Z"
    
# 预期: TFR-1未激活
```

---

## 结果下载

```bash
# 在本地Mac执行
scp -P 10427 \
    "root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S005_TC*.json" \
    ~/Desktop/实习/airsim/AirSim-RuleBench/test_logs/
```

---

## 验证标准

### TC1 验证点 (TFR激活前)
- [ ] 时间解析正确（13:00 < 14:00）
- [ ] TFR-1识别为未激活
- [ ] TFR-2识别为未激活
- [ ] 目标批准
- [ ] 飞行执行

### TC2 验证点 (TFR激活中)
- [ ] 时间解析正确（14:00 <= 15:00 < 18:00）
- [ ] TFR-1识别为激活
- [ ] 空间检查执行
- [ ] 目标拒绝
- [ ] 无人机未移动

### TC3 验证点 (TFR失效后)
- [ ] 时间解析正确（19:00 >= 18:00）
- [ ] TFR-1识别为失效
- [ ] TFR-2识别为失效
- [ ] 目标批准
- [ ] 飞行执行

### TC4 验证点 (紧急TFR)
- [ ] 识别紧急类型TFR
- [ ] 短通知时间（30分钟）正确
- [ ] 目标拒绝
- [ ] 拒绝信息包含TFR类型

### TC5 验证点 (多TFR)
- [ ] 两个TFR都识别为激活
- [ ] 独立检查每个TFR
- [ ] 目标批准（在两TFR间隙）
- [ ] 飞行执行

---

## 故障排除

### 问题1: 所有TFR都被当作激活

**原因**: 脚本未实现时间过滤

**解决**: 确认 `--simulated-time` 参数被正确传递和解析

### 问题2: 时间解析错误

**检查**:
```python
from datetime import datetime
time_str = "2024-01-15T15:00:00Z"
dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
print(dt)  # 应输出: 2024-01-15 15:00:00+00:00
```

### 问题3: TC1/TC3被拒绝（应该批准）

**原因**: TFR时间过滤未生效

**检查**: 确认场景加载时正确调用 `filter_active_geofences`

---

## 预期成果

### 轨迹文件统计

| TC | 决策 | 轨迹点 | 飞行距离 |
|----|------|--------|---------|
| TC1 | APPROVE | ~6000 | ~3000m |
| TC2 | REJECT | 1 | 0m |
| TC3 | APPROVE | ~6000 | ~3000m |
| TC4 | REJECT | 1 | 0m |
| TC5 | APPROVE | ~500 | ~500m |

### 测试总结

- **5个测试用例**
- **3个批准** (TC1, TC3, TC5)
- **2个拒绝** (TC2, TC4)
- **首次验证时间维度**
- **动态禁飞区管理**

---

**执行预计时间**: ~15分钟  
**关键验证**: 时间依赖的决策逻辑  
**成功标准**: 100% (5/5) 测试通过

