# AirSim-RuleBench

Benchmark dataset for testing UAV rule compliance in ProjectAirSim simulation.

## 🚀 Quick Start

```bash
# 验证场景
python scripts/validate_scenario.py scenarios/basic/S001_geofence_basic.jsonc

# 检测违规
python scripts/detect_violations.py test_logs/trajectory.json -g ground_truth/S001_violations.json
```

完整指南见 [`docs/QUICKSTART.md`](docs/QUICKSTART.md)

---

## 📁 项目结构

```
AirSim-RuleBench/
├── scenarios/          # 测试场景（按复杂度分类）
│   ├── basic/         # 基础场景（S001-S099）
│   ├── intermediate/  # 中级场景（S100-S199）
│   └── advanced/      # 高级场景（S200+）
├── rules/             # 规则定义
├── ground_truth/      # 标注文件
├── scripts/           # 工具脚本
├── templates/         # 可复用模板
├── test_logs/         # 测试数据
├── reports/           # 实验报告
└── docs/              # 文档
```

---

## ✅ 当前进度

### 空间限制场景（S001-S008）

| 场景 | 规则                  | 状态    | 报告                        |
| ---- | --------------------- | ------- | --------------------------- |
| S001 | R001 (Geofence)       | ✅ 完成 | [查看](reports/S001_REPORT.md) |
| S002 | R001 (Multi-Geofence) | ✅ 完成 | [查看](reports/S002_REPORT.md) |
| S003 | R001 (Path Crossing)  | ✅ 完成 | [查看](reports/S003_REPORT.md) |
| S004 | R001 (Airport Zones)  | ✅ 完成 | [查看](reports/S004_REPORT.md) |
| S005 | R001 (Dynamic TFR) ⭐ | ✅ 完成 | [查看](reports/S005_REPORT.md) |
| S006 | Altitude Limit (120m) | ✅ 完成 | [查看](reports/S006_REPORT.md) |
| S007 | Zone Altitude Limits  | ✅ 完成 | [查看](reports/S007_REPORT.md) |
| S008 | Structure Waiver ⭐   | ✅ 完成 | [查看](reports/S008_REPORT.md) |

### 运动参数场景（S009-S012）

| 场景 | 规则                  | 状态    | 报告                        |
| ---- | --------------------- | ------- | --------------------------- |
| S009 | Global Speed Limit (100 km/h) | ✅ 完成 | [查看](reports/S009_REPORT.md) |
| S010 | Zone Speed Limits ⭐  | ✅ 完成 | [查看](reports/S010_REPORT.md) |
| S011 | Night Flight ⭐⭐     | ✅ 完成 | [查看](reports/S011_REPORT.md) |
| S012 | Time Window Limits ⭐⭐ | ✅ 完成 | [查看](reports/S012_REPORT.md) |

### 视距与避让场景（S013-S016）

| 场景 | 规则                  | 状态    | 报告 | LLM验证 |
| ---- | --------------------- | ------- | ---- | ------- |
| S013 | VLOS Requirement ⭐   | ✅ 完成 | [查看](reports/S013_REPORT.md) | - |
| S014 | BVLOS Waiver ⭐⭐⭐   | ✅ 完成 | [查看](reports/S014_REPORT.md) | - |
| S015 | Dynamic NFZ Avoidance (Pre-flight) ⭐⭐ | ✅ 完成 | [查看](reports/S015_REPORT.md) | 6/6 (100%) 🎉 |
| S016 | Realtime Obstacle Avoidance (In-flight) ⭐⭐ | ✅ 完成 | [查看](reports/S016_REPORT.md) | **6/6 (100%)** 🎉 |

### 载重与审批场景（S017-S020）

| 场景 | 规则                  | 状态    | 报告 | LLM验证 |
| ---- | --------------------- | ------- | ---- | ------- |
| S017 | Payload and Drop Restrictions ⭐⭐ | ✅ 完成 | [查看](reports/S017_REPORT.md) | **8/8 (100%)** 🎉 |
| S018 | Multi-Drone Coordination ⭐⭐⭐ | ✅ 完成 | [查看](reports/S018_REPORT.md) | **8/8 (100%)** 🎉 |
| S019 | Airspace Classification ⭐⭐ | ✅ 完成 | [查看](reports/S019_REPORT.md) | **5/5 (100%)** 🎉 |
| S020 | Approval Timeline ⭐ | ✅ 完成 | [查看](reports/S020_REPORT.md) | **4/4 (100%)** 🎉 |

**LLM验证总结**: S016-S020场景已完成双引擎验证（规则引擎 + LLM引擎），总准确率 **31/31 = 100%** 🎉

---

## 📖 文档

- **快速开始**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **文件清单**: [docs/FILES.md](docs/FILES.md)
- **场景开发标准**: [docs/SCENARIO_STANDARD.md](docs/SCENARIO_STANDARD.md) ⭐ **基于 S002**
- **完整文档**: [docs/README.md](docs/README.md)

---

## 🛠️ 工具

| 脚本                     | 功能     | 适用场景 | 用途   |
| ------------------------ | -------- | -------- | ------ |
| `validate_scenario.py` | 场景验证 | 全部 | 本地   |
| `detect_violations.py` | 违规检测 | 全部 | 本地   |
| `run_scenario.py`      | 场景执行 | S001-S008 | 服务器 |
| `run_scenario_motion.py` | 运动参数场景执行 | S009-S012 | 服务器 |
| `run_scenario_vlos.py` | VLOS与BVLOS场景执行 | S013-S014 ⭐ | 服务器 |
| `run_scenario_path.py` | 避让场景执行（Pre-flight + In-flight） | S015-S016 ⭐⭐ | 服务器 |
| `run_scenario_payload.py` | 载重与投放场景执行（Pre-flight + Drop检测） | S017 ⭐⭐ | 服务器 |
| `run_scenario_multi.py` | 多无人机协同场景执行（Simultaneous + Sequential） | S018 ⭐⭐⭐ | 服务器 |
| `run_scenario_airspace.py` | 空域分类场景执行（高度边界 + 限制区域 + 多目标） | S019 ⭐⭐ | 服务器 |
| `run_scenario_timeline.py` | 申请时限场景执行（时间计算 + 豁免逻辑） | S020 ⭐ | 服务器 |
| **`run_scenario_llm_validator.py`** | **LLM合规性验证（Gemini 2.5 Flash）** | **S016-S020 ⭐⭐⭐** | **本地** |

---

## 📝 创建新场景

```bash
# 1. 复制模板
cp templates/scene_config_template.jsonc scenarios/basic/S00X.jsonc

# 2. 编辑配置
# 修改无人机位置、禁飞区等参数

# 3. 创建标注
cp templates/ground_truth_template.json ground_truth/S00X_violations.json

# 4. 验证
python scripts/validate_scenario.py scenarios/basic/S00X.jsonc
```

详见 [`templates/scenario_template.md`](templates/scenario_template.md)

---

**版本**: 3.0  
**最后更新**: 2025-11-01  
**新增**: 🎉 **S016-S020 LLM验证全部完成！**（31/31测试用例 = 100%准确率）使用Gemini 2.5 Flash完成双引擎对比验证，证明LLM可以替代规则引擎进行UAV合规性判断！  
**里程碑**: 所有20个场景（S001-S020）设计完成并测试通过！
