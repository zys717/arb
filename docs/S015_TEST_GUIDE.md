# S015 - Dynamic No-Fly Zone Avoidance Test Guide

# S015 - 动态禁飞区避让测试指南

**创建日期**: 2025-10-31
**场景ID**: S015_DynamicNFZAvoidance
**测试用例**: 6个
**预期通过率**: 100%

---

## 测试前准备 | Pre-Test Setup

### 1. 文件清单检查

确认以下文件已准备：

```
本地文件:
✅ scenarios/basic/S015_dynamic_nfz_avoidance.jsonc  (场景配置)
✅ ground_truth/S015_violations.json                (预期结果)
⏳ scripts/run_scenario_path.py                     (待实现/扩展)

服务器文件:
📤 需上传: S015_dynamic_nfz_avoidance.jsonc
📤 需上传: run_scenario_path.py (或扩展的run_scenario.py)
```

### 2. 核心实现需求

**⚠️ 重要**: S015需要新增**路径冲突检测**功能！

#### 当前脚本能力对比

| 脚本                   | 检测能力      | S015需求     | 是否适用    |
| ---------------------- | ------------- | ------------ | ----------- |
| run_scenario.py        | 点在圆内检测  | 路径穿圆检测 | ⚠️ 需扩展 |
| run_scenario_motion.py | 速度/时间检测 | 路径几何检测 | ❌ 不适用   |
| run_scenario_vlos.py   | 距离检测      | 路径-NFZ冲突 | ⚠️ 需扩展 |

#### 推荐方案：扩展 run_scenario.py

```python
# 需要添加的功能模块

class PathConflictDetector:
    """路径-NFZ冲突检测器"""
  
    def check_straight_path_conflict(self, start, end, nfzs):
        """
        检查直线路径是否与任何NFZ冲突
    
        Args:
            start: 起点 (north, east, down)
            end: 终点 (north, east, down)
            nfzs: 禁飞区列表
    
        Returns:
            (has_conflict, conflict_details)
        """
        conflicts = []
    
        for nfz in nfzs:
            # 1. 提取NFZ参数
            center = nfz['center']
            radius = nfz.get('radius', 0)
            safety_margin = nfz.get('safety_margin', 0)
            total_radius = radius + safety_margin
        
            # 2. 计算路径到NFZ中心的最小距离
            min_dist = self.point_to_line_distance_2d(
                center, start, end
            )
        
            # 3. 判断冲突
            if min_dist < total_radius:
                conflicts.append({
                    'nfz_id': nfz['id'],
                    'min_distance': min_dist,
                    'required_distance': total_radius,
                    'clearance_deficit': total_radius - min_dist
                })
    
        return (len(conflicts) > 0), conflicts
  
    @staticmethod
    def point_to_line_distance_2d(point, line_start, line_end):
        """
        计算点到线段的最短距离（2D水平投影）
    
        算法:
        1. 计算投影参数 t ∈ [0, 1]
        2. 找到线段上最近点
        3. 计算欧式距离
        """
        import math
    
        # 提取2D坐标（north, east）
        px, py = point[0], point[1]
        ax, ay = line_start[0], line_start[1]
        bx, by = line_end[0], line_end[1]
    
        # 线段向量
        dx, dy = bx - ax, by - ay
        line_length_sq = dx*dx + dy*dy
    
        if line_length_sq == 0:
            # 起点=终点，直接返回点到起点距离
            return math.sqrt((px-ax)**2 + (py-ay)**2)
    
        # 投影参数 t
        t = ((px-ax)*dx + (py-ay)*dy) / line_length_sq
        t = max(0, min(1, t))  # 限制在[0, 1]
    
        # 最近点
        closest_x = ax + t*dx
        closest_y = ay + t*dy
    
        # 距离
        return math.sqrt((px-closest_x)**2 + (py-closest_y)**2)
```

---

## 测试执行步骤 | Test Execution

### 步骤1: 准备服务器环境

```bash
# 1. SSH连接
ssh -p 10427 root@connect.westb.seetacloud.com

# 2. 进入工作目录
cd /home/sduser/project/ProjectAirSim/client/python/example_user_scripts

# 3. 激活虚拟环境
source ~/project/airsim-venv/airsim-venv/bin/activate
```

### 步骤2: 上传测试文件

**本地执行**:

```bash
# 上传场景配置
scp -P 10427 \
    AirSim-RuleBench/scenarios/basic/S015_dynamic_nfz_avoidance.jsonc \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 上传扩展后的脚本
scp -P 10427 \
    AirSim-RuleBench/scripts/run_scenario_path.py \
    root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 步骤3: 执行测试用例

#### TC1: 路径前方有NFZ（应拒绝）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC1.json \
    --mode auto \
    --test-case TC1
```

**预期输出**:

```
Loading scenario: S015_DynamicNFZAvoidance
✓ Scenario loaded
✓ Loading test case: TC1

Test Command: move_to_position(800, 0, 50)

🔍 Pre-flight check: Path conflict detection...
   ⚠️  Analyzing path: (0, 0, 50) → (800, 0, 50)
   
   Checking NFZ: nfz_emergency_landing
     - Center: (500, 0, 0)
     - Total radius: 300m
     - Min distance to path: 0.0m
     - ❌ CONFLICT: 0.0m < 300.0m
   
🚫 COMMAND REJECTED (Path conflict detected)
   Reason: Path intersects NFZ_Emergency_Landing at N=500m
   
✓ Trajectory saved: trajectory_S015_TC1.json (1 points)

======================================================================
⚠️  SCENARIO EXECUTION COMPLETED WITH WARNINGS
======================================================================
```

**验证点**:

- ✅ Pre-flight检查失败
- ✅ 拒绝原因明确
- ✅ 轨迹仅1个点（初始位置）

---

#### TC2: 路径旁边有NFZ但不冲突（应批准）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC2.json \
    --mode auto \
    --test-case TC2
```

**预期输出**:

```
Test Command: move_to_position(1500, 0, 50)

🔍 Pre-flight check: Path conflict detection...
   ⚠️  Analyzing path: (0, 0, 50) → (1500, 0, 50)
   
   Checking all NFZs...
   ✓ NFZ_Emergency_Landing: distance=... (SAFE/CONFLICT - 需验证逻辑)
   ✓ NFZ_Police_Operation: distance=800m (SAFE)
   ✓ NFZ_Fire_Rescue: distance=... (SAFE)
   
✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
✓ Trajectory saved: trajectory_S015_TC2.json (~3000 points)

======================================================================
✓ SCENARIO EXECUTION COMPLETED
======================================================================
```

**⚠️ 注意**: TC2的逻辑需要仔细验证！

- 如果路径 (0,0)→(1500,0) 会穿过 NFZ_Emergency(500,0,R=300)
- 应该被拒绝，但ground truth说APPROVE
- **可能需要重新设计TC2**

---

#### TC3: 多NFZ冲突（应拒绝）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC3.json \
    --mode auto \
    --test-case TC3
```

**预期输出**:

```
Test Command: move_to_position(3000, 0, 50)

🔍 Pre-flight check: Path conflict detection...
   
   Conflicts detected:
   1. NFZ_Emergency_Landing (N=500m): 距离0m < 300m ❌
   2. NFZ_Fire_Rescue (N=2500m): 距离0m < 500m ❌
   
🚫 COMMAND REJECTED (Multiple path conflicts)
   First conflict: NFZ_Emergency_Landing at N=500m
   
✓ Trajectory saved: trajectory_S015_TC3.json (1 points)
```

**验证点**:

- ✅ 检测到2个冲突
- ✅ 报告第一个冲突（距离最近）
- ✅ 拒绝飞行

---

#### TC4: 短路径无冲突（应批准）

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC4.json \
    --mode auto \
    --test-case TC4
```

**预期输出**:

```
Test Command: move_to_position(300, 0, 50)

🔍 Pre-flight check: Path conflict detection...
   ✓ NFZ_Emergency_Landing: Min distance=200m from boundary (SAFE)
   
✅ All pre-flight checks passed
✓ Executing movement...
✓ Target reached
✓ Trajectory saved: trajectory_S015_TC4.json (~600 points)
```

**验证点**:

- ✅ 路径终点距NFZ边界100m+
- ✅ 批准飞行
- ✅ 完整轨迹

---

#### TC5: 边界测试（应批准）⭐

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC5.json \
    --mode auto \
    --test-case TC5
```

**预期输出**:

```
Test Command: move_to_position(500, 350, 50)

🔍 Pre-flight check: Path conflict detection...
   Checking NFZ_Emergency_Landing:
     - Center: (500, 0, 0)
     - Target: (500, 350, 50)
     - Distance to center: 350.0m
     - Safety margin: 300.0m
     - Clearance: 50.0m ✅
   
✅ All pre-flight checks passed (boundary case)
✓ Executing movement...
✓ Target reached
✓ Trajectory saved: trajectory_S015_TC5.json (~1220 points)
```

**验证点**:

- ✅ 边界余量50m被正确判定为安全
- ✅ 距离计算精度 ±5m
- ⭐ **关键测试**: 验证边界条件处理

---

#### TC6: 对角线冲突（应拒绝）⭐

```bash
python run_scenario_path.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S015_dynamic_nfz_avoidance.jsonc \
    --output trajectory_S015_TC6.json \
    --mode auto \
    --test-case TC6
```

**预期输出**:

```
Test Command: move_to_position(1500, 500, 50)

🔍 Pre-flight check: Path conflict detection...
   Checking NFZ_Police_Operation:
     - Center: (1500, 800, 0)
     - Path: (0,0) → (1500,500)
     - Point-to-line distance: ~300.0m
     - Safety margin: 400.0m
     - ❌ CONFLICT: 300.0m < 400.0m
   
🚫 COMMAND REJECTED (Diagonal path too close to NFZ)
   
✓ Trajectory saved: trajectory_S015_TC6.json (1 points)
```

**验证点**:

- ✅ 对角线路径冲突检测
- ✅ 点到线距离算法正确
- ⭐ **关键测试**: 验证2D几何计算

---

### 步骤4: 下载测试结果

```bash
# 本地执行
scp -P 10427 \
    'root@connect.westb.seetacloud.com:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S015_TC*.json' \
    AirSim-RuleBench/test_logs/
```

### 步骤5: 快速验证

```bash
# 检查文件大小
ls -lh AirSim-RuleBench/test_logs/trajectory_S015_TC*.json

# 预期文件大小:
# TC1: ~240B  (拒绝，1个点)
# TC2: ~100KB+ (批准，完整轨迹)
# TC3: ~240B  (拒绝，1个点)
# TC4: ~30KB  (批准，短轨迹)
# TC5: ~60KB  (批准，中轨迹)
# TC6: ~240B  (拒绝，1个点)
```

---

## 测试验证清单 | Verification Checklist

### 决策准确性

| TC  | 预期决策 | 实际决策 | 轨迹点数 | 通过 |
| --- | -------- | -------- | -------- | ---- |
| TC1 | REJECT   | ?        | 1        | ☐   |
| TC2 | APPROVE  | ?        | >1000    | ☐   |
| TC3 | REJECT   | ?        | 1        | ☐   |
| TC4 | APPROVE  | ?        | >300     | ☐   |
| TC5 | APPROVE  | ?        | >500     | ☐   |
| TC6 | REJECT   | ?        | 1        | ☐   |

**目标**: 6/6 (100%)

### 功能验证

- [ ] Pre-flight路径冲突检测功能正常
- [ ] 点到线距离算法正确
- [ ] 多NFZ冲突优先级处理正确
- [ ] 边界条件（TC5）正确处理
- [ ] 对角线路径（TC6）冲突检测正确
- [ ] 拒绝原因日志清晰
- [ ] 轨迹记录一致性

### 性能验证

- [ ] Pre-flight检查时间 < 1秒
- [ ] 内存占用合理
- [ ] 无异常或错误日志

---

## 常见问题 | Troubleshooting

### 问题1: 脚本不存在

**症状**: `run_scenario_path.py: No such file`

**原因**: 路径冲突检测功能尚未实现

**解决**:

1. 选择扩展现有脚本（推荐 `run_scenario.py`）
2. 或创建新脚本 `run_scenario_path.py`
3. 实现核心算法（见上文）

### 问题2: TC2逻辑矛盾

**症状**: TC2路径 (0,0)→(1500,0) 应该穿过 NFZ_Emergency(500,0,R=300)

**可能原因**:

- Ground truth设计有误
- 或需要特殊逻辑（如"飞过已激活但当前失效的NFZ"）

**建议**:

1. 重新验证TC2的设计意图
2. 或修改TC2目标点避开NFZ
3. 或修改NFZ位置

### 问题3: 距离计算精度问题

**症状**: TC5边界测试失败（50m余量被判定为不安全）

**解决**:

- 检查点到线距离算法实现
- 确认2D投影正确（忽略高度）
- 使用 `math.sqrt()` 而非整数运算

---

## 实现优先级 | Implementation Priority

### 阶段1: 核心功能（必需）⭐⭐⭐

```python
✅ 1. 点到线段距离计算（2D）
✅ 2. 路径-NFZ冲突检测
✅ 3. Pre-flight检查集成
✅ 4. 冲突日志输出
```

### 阶段2: 增强功能（推荐）⭐⭐

```python
□ 5. 多NFZ优先级排序
□ 6. 冲突点可视化
□ 7. 路径重规划建议
```

### 阶段3: 高级功能（可选）⭐

```python
□ 8. In-flight实时检测
□ 9. 曲线路径支持
□ 10. 3D路径冲突检测
```

---

## 下一步计划 | Next Steps

### 短期目标

1. ✅ 完成场景配置文件
2. ✅ 完成ground truth文件
3. ✅ 完成README和TEST_GUIDE
4. ⏳ **实现路径冲突检测功能**
5. ⏳ 执行服务器测试
6. ⏳ 生成测试报告

### 长期展望

- 扩展至S016（障碍物避让+VLOS）
- 开发路径规划可视化工具
- 集成自动路径重规划功能

---

## 参考资料 | References

### 算法参考

- [Point to Line Segment Distance](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line)
- [Geometric Algorithms in Python](https://github.com/...)

### 相关场景

- S001: 基础地理围栏（点检测）
- S002: 多地理围栏（多点检测）
- S005: 临时禁飞区（时间限制）

### 技术文档

- `run_scenario.py`: 基础geofence检测实现
- `detect_violations.py`: 违规检测逻辑参考

---

**测试工程师**: _____________
**测试日期**: _____________
**测试环境**: ProjectAirSim v1.0
**最后更新**: 2025-10-31
