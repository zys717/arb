# AirSim-RuleBench 文件清单 

**最后更新**: 2025-10-22
**项目版本**: v0.2
**文件总数**: 29 个主要文件

---

## 📁 项目结构

```
AirSim-RuleBench/
├── README.md                                    # 项目主页（简洁版）
│
├── docs/                                        # 📚 文档目录
│   ├── README.md                               # 完整项目文档
│   ├── QUICKSTART.md                           # 快速开始指南
│   ├── SCENARIO_STANDARD.md                    # ⭐ 场景开发标准（基于 S002）
│   └── FILES.md                                # 本文件清单
│
├── reports/                                     # 📊 测试报告
│   ├── S001_REPORT.md                          # S001 实验报告
│   └── S002_REPORT.md                          # ⭐ S002 综合测试报告（4个测试用例）
│
├── rules/                                       # 📋 规则定义
│   └── R001_geofence.json                      # 地理围栏规则（R001）
│
├── ground_truth/                                # 🎯 Ground Truth（测试预期）
│   ├── S001_violations.json                    # S001 预期行为（1个测试用例）
│   └── S002_violations.json                    # ⭐ S002 预期行为（4个测试用例）
│
├── scenarios/                                   # 🗺️ 测试场景
│   └── basic/                                  # 基础场景（S001-S099）
│       ├── S001_geofence_basic.jsonc          # S001 场景配置
│       ├── S001_README.md                     # S001 说明文档
│       ├── S002_multi_geofence.jsonc          # ⭐ S002 场景配置（2个地理围栏）
│       ├── S002_README.md                     # ⭐ S002 说明文档（更新版）
│       └── scene_basic_drone.jsonc            # 基础模板（从服务器获取）
│
├── scripts/                                     # 🔧 工具脚本
│   ├── run_scenario.py                         # 场景执行脚本（服务器端）
│   ├── detect_violations.py                    # 违规检测脚本（本地分析）
│   ├── validate_scenario.py                    # 场景验证脚本
│   └── run_test_suite.py                       # ⭐ 批量测试工具（新增）
│
├── templates/                                   # 📝 模板文件
│   ├── scenario_template.md                    # 场景设计模板
│   ├── ground_truth_template.json              # Ground Truth 模板
│   └── scene_config_template.jsonc             # 场景配置模板
│
└── test_logs/                                   # 📈 测试数据
    ├── trajectory_S001_auto.json               # S001 测试轨迹
    ├── trajectory_S001_violating.json          # S001 模拟违规轨迹
    ├── trajectory_S002_auto.json               # S002 初始测试（已替换）
    ├── trajectory_S002_TC2.json                # ⭐ S002 TC2: 军事基地违规
    ├── trajectory_S002_TC3.json                # ⭐ S002 TC3: 安全飞行（440点）
    ├── trajectory_S002_TC4.json                # ⭐ S002 TC4: 边界测试（135点）
    └── trajectory_S002_violating.json          # S002 模拟违规轨迹
```

**注**: ⭐ 标记的文件为 S002 新增或重大更新的文件

---

## 📊 文件统计

| 类型                        | 数量         | 说明                     |
| --------------------------- | ------------ | ------------------------ |
| **文档** (`.md`)    | 11           | README、报告、说明       |
| **配置** (`.jsonc`) | 5            | 场景配置文件             |
| **数据** (`.json`)  | 9            | 规则、Ground Truth、轨迹 |
| **脚本** (`.py`)    | 4            | Python 工具脚本          |
| **总计**              | **29** | -                        |

---

## 📋 文件详细说明

### 核心文档 (`README.md`, `docs/`)

#### `README.md`

- **作用**: 项目主页，简洁版文档
- **包含**: 项目简介、当前进度、快速链接
- **维护**: 随项目进展更新

#### `docs/README.md`

- **作用**: 完整项目文档
- **包含**: 详细说明、使用方法、设计理念
- **受众**: 新用户、开发者

#### `docs/QUICKSTART.md`

- **作用**: 5分钟快速上手指南
- **包含**: 常用命令、快速测试流程
- **受众**: 快速入门用户

#### `docs/SCENARIO_STANDARD.md` ⭐ **新增**

- **作用**: 场景开发标准和最佳实践
- **基于**: S002 的成功经验
- **包含**:
  - 文件结构标准
  - 命名规范
  - 测试用例要求（最少3-4个）
  - 文档模板
  - 质量检查清单
- **用途**: 开发新场景时的参考指南

#### `docs/FILES.md`

- **作用**: 本文件，项目文件清单
- **包含**: 所有文件的说明和统计

---

### 测试报告 (`reports/`)

#### `reports/S001_REPORT.md`

- **场景**: S001 基础地理围栏
- **测试用例**: 1个
- **状态**: ✅ 完成
- **要点**: 单一地理围栏，命令拒绝验证

#### `reports/S002_REPORT.md` ⭐ **综合报告**

- **场景**: S002 多地理围栏
- **测试用例**: **4个**（TC1-TC4）
- **状态**: ✅ 完成（100% 通过率）
- **篇幅**: 413 行
- **要点**:
  - 多围栏检测
  - 违规 + 批准测试
  - 边界条件验证
  - 实际飞行验证（577 轨迹点）
- **亮点**: 作为未来场景报告的标准模板

---

### 规则定义 (`rules/`)

#### `rules/R001_geofence.json`

- **规则**: R001 - 地理围栏违规防止
- **内容**:
  - 自然语言描述
  - 形式化定义
  - 检测方法（3D 欧氏距离）
  - 安全边距：500m
- **应用场景**: S001, S002

---

### Ground Truth (`ground_truth/`)

#### `ground_truth/S001_violations.json`

- **场景**: S001
- **测试用例**: 1个
- **格式**: 单一测试用例格式

#### `ground_truth/S002_violations.json` ⭐ **多测试用例格式**

- **场景**: S002
- **测试用例**: **4个**（TC1-TC4）
- **格式**:
  - `test_cases` 数组
  - 每个用例独立定义
  - 包含预期行为和验证数据
- **用途**:
  - 自动化测试的参考标准
  - `detect_violations.py` 的输入

---

### 场景配置 (`scenarios/`)

#### `scenarios/basic/S001_geofence_basic.jsonc`

- **场景**: S001 基础地理围栏
- **地理围栏**: 1个（军事基地）
- **初始位置**: (700, 0, 50)

#### `scenarios/basic/S002_multi_geofence.jsonc` ⭐

- **场景**: S002 多地理围栏
- **地理围栏**: **2个**（军事基地 + 医院）
- **初始位置**: (650, 0, 50)
- **测试用例**: 4个定义在 `test_info.test_cases`
- **特点**:
  - 不同半径和安全边距
  - 优先级系统
  - 详细的测试用例元数据

#### `scenarios/basic/scene_basic_drone.jsonc`

- **作用**: ProjectAirSim 原始场景模板
- **来源**: 从服务器下载
- **用途**: 理解 ProjectAirSim 场景结构

#### `scenarios/basic/S001_README.md`

- **场景说明**: S001 的使用文档
- **包含**: 配置、测试方法、预期结果

#### `scenarios/basic/S002_README.md` ⭐ **更新版**

- **场景说明**: S002 的使用文档
- **包含**:
  - 4个测试用例详细说明
  - 测试结果汇总表
  - 执行命令（复制粘贴即用）
  - 与 S001 对比
- **标准**: 作为未来场景 README 的模板

---

### 工具脚本 (`scripts/`)

#### `scripts/run_scenario.py`

- **功能**: 在 ProjectAirSim 中执行场景
- **运行位置**: 服务器
- **主要特性**:
  - 场景加载
  - 无人机控制
  - 客户端地理围栏检测
  - 轨迹记录
  - 支持 auto/manual 模式
- **关键API**:
  - `ProjectAirSimClient.connect()` (同步)
  - `World(client, scene_path)`
  - `drone.get_ground_truth_pose()` (返回字典)

#### `scripts/detect_violations.py`

- **功能**: 分析轨迹，检测违规
- **运行位置**: 本地
- **主要特性**:
  - 加载 Ground Truth
  - 3D 距离计算
  - 违规检测和分类
  - 生成详细报告
- **更新**: 支持单一和多地理围栏格式

#### `scripts/validate_scenario.py`

- **功能**: 验证场景配置文件
- **检查项**:
  - JSON 语法
  - 必需字段
  - 坐标范围
  - 地理围栏参数

#### `scripts/run_test_suite.py` ⭐ **新增**

- **功能**: 批量执行多个测试用例
- **特性**:
  - 自动加载 Ground Truth 中的所有测试用例
  - 依次执行每个测试
  - 生成综合报告
  - 评估通过/失败
- **状态**: 已实现框架，待集成

---

### 模板文件 (`templates/`)

#### `templates/scenario_template.md`

- **作用**: 场景设计文档模板
- **用途**: 设计新场景时的起点

#### `templates/ground_truth_template.json`

- **作用**: Ground Truth 文件模板
- **格式**: 遵循 S002 多测试用例格式

#### `templates/scene_config_template.jsonc`

- **作用**: 场景配置文件模板
- **基于**: ProjectAirSim 场景结构

---

### 测试数据 (`test_logs/`)

#### S001 测试数据

- `trajectory_S001_auto.json`: 自动测试轨迹（1点）
- `trajectory_S001_violating.json`: 模拟违规轨迹

#### S002 测试数据 ⭐

- `trajectory_S002_TC2.json`: 军事基地违规测试（1点）
- `trajectory_S002_TC3.json`: 安全飞行测试（**440点**, 44.7秒）
- `trajectory_S002_TC4.json`: 边界测试（**135点**, 13.5秒）
- `trajectory_S002_violating.json`: 模拟违规轨迹

**数据量**:

- S001: 1 点
- S002: **577 点**（实际飞行数据）
- 文件大小: TC3 (80KB), TC4 (25KB)

---

## 🎯 关键文件快速索引

### 开始新项目

1. `docs/SCENARIO_STANDARD.md` - 了解标准
2. `scenarios/basic/S002_README.md` - 参考实现
3. `templates/` - 使用模板

### 运行测试

1. `scripts/run_scenario.py` - 服务器执行
2. `scripts/detect_violations.py` - 本地分析

### 查看结果

1. `reports/S002_REPORT.md` - 综合报告示例
2. `test_logs/trajectory_S002_TC*.json` - 原始数据

### 了解项目

1. `README.md` - 快速概览
2. `docs/QUICKSTART.md` - 快速上手
3. `docs/README.md` - 完整文档

---

## 📈 项目演进

### v0.1 → v0.2 主要变化

| 方面                   | v0.1 (S001) | v0.2 (S002)                         |
| ---------------------- | ----------- | ----------------------------------- |
| **测试用例**     | 1个/场景    | **3-4个/场景**                |
| **文档标准**     | 基础        | **综合（SCENARIO_STANDARD）** |
| **测试类型**     | 仅拒绝      | **拒绝+批准+边界**            |
| **实际飞行**     | 否          | **是（577点）**               |
| **报告深度**     | 基础        | **详细（413行）**             |
| **Ground Truth** | 单一格式    | **多测试用例格式**            |
| **文件数量**     | ~15         | **29**                        |

---

## 🔄 文件依赖关系

```
S002_multi_geofence.jsonc (场景配置)
    ↓ 
run_scenario.py (执行)
    ↓
trajectory_S002_TC*.json (轨迹数据)
    ↓
detect_violations.py (分析)
    ↑
S002_violations.json (Ground Truth)
    ↓
S002_REPORT.md (报告)
```

---

## 🚀 未来扩展

随着新场景添加，预计文件结构将扩展：

```
scenarios/
├── basic/
│   ├── S001_* (完成)
│   ├── S002_* (完成)
│   ├── S003_* (计划中: 3D高度约束)
│   └── ...
├── intermediate/
│   └── S100_* (未来)
└── advanced/
    └── S200_* (未来)
```

---

**维护**: 随项目更新自动更新
**版本**: 与项目版本同步
**最后检查**: 2025-10-22
