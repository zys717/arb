# AirSim-RuleBench

Benchmark dataset for testing UAV rule compliance in ProjectAirSim simulation.

## Quick Start

```bash
# Validate scenario
python scripts/validate_scenario.py scenarios/basic/S001_geofence_basic.jsonc

# Detect violations
python scripts/detect_violations.py test_logs/trajectory.json -g ground_truth/S001_violations.json
```

See complete guide in [`docs/QUICKSTART.md`](docs/QUICKSTART.md)

## Project Structure

```
AirSim-RuleBench/
 scenarios/ # Test scenarios (classified by complexity)
 basic/ # Basic scenarios (S001-S099)
 intermediate/ # Intermediate scenarios (S100-S199)
 advanced/ # Advanced scenarios (S200+)
 rules/ # Rule definitions
 ground_truth/ # Ground truth annotations
 scripts/ # Utility scripts
 templates/ # Reusable templates
 test_logs/ # Test data
 reports/ # Experiment reports
 docs/ # Documentation
```

## Current Progress

### Spatial Constraint Scenarios (S001-S008)

| Scenario | Rule | Status | Report |
| ---- | --------------------- | ------- | --------------------------- |
| S001 | R001 (Geofence) | Completed | [View](reports/S001_REPORT.md) |
| S002 | R001 (Multi-Geofence) | Completed | [View](reports/S002_REPORT.md) |
| S003 | R001 (Path Crossing) | Completed | [View](reports/S003_REPORT.md) |
| S004 | R001 (Airport Zones) | Completed | [View](reports/S004_REPORT.md) |
| S005 | R001 (Dynamic TFR) | Completed | [View](reports/S005_REPORT.md) |
| S006 | Altitude Limit (120m) | Completed | [View](reports/S006_REPORT.md) |
| S007 | Zone Altitude Limits | Completed | [View](reports/S007_REPORT.md) |
| S008 | Structure Waiver | Completed | [View](reports/S008_REPORT.md) |

### Motion Parameter Scenarios (S009-S012)

| Scenario | Rule | Status | Report |
| ---- | --------------------- | ------- | --------------------------- |
| S009 | Global Speed Limit (100 km/h) | Completed | [View](reports/S009_REPORT.md) |
| S010 | Zone Speed Limits | Completed | [View](reports/S010_REPORT.md) |
| S011 | Night Flight | Completed | [View](reports/S011_REPORT.md) |
| S012 | Time Window Limits | Completed | [View](reports/S012_REPORT.md) |

### Line-of-Sight and Avoidance Scenarios (S013-S016)

| Scenario | Rule | Status | Report | LLM Validation |
| ---- | --------------------- | ------- | ---- | ------- |
| S013 | VLOS Requirement | Completed | [View](reports/S013_REPORT.md) | - |
| S014 | BVLOS Waiver | Completed | [View](reports/S014_REPORT.md) | - |
| S015 | Dynamic NFZ Avoidance (Pre-flight) | Completed | [View](reports/S015_REPORT.md) | 6/6 (100%) |
| S016 | Realtime Obstacle Avoidance (In-flight) | Completed | [View](reports/S016_REPORT.md) | 6/6 (100%) |

### Payload and Approval Scenarios (S017-S020)

| Scenario | Rule | Status | Report | LLM Validation |
| ---- | --------------------- | ------- | ---- | ------- |
| S017 | Payload and Drop Restrictions | Completed | [View](reports/S017_REPORT.md) | 8/8 (100%) |
| S018 | Multi-Drone Coordination | Completed | [View](reports/S018_REPORT.md) | 8/8 (100%) |
| S019 | Airspace Classification | Completed | [View](reports/S019_REPORT.md) | 5/5 (100%) |
| S020 | Approval Timeline | Completed | [View](reports/S020_REPORT.md) | 4/4 (100%) |

LLM Validation Summary: S016-S020 scenarios completed dual-engine validation (Rule Engine + LLM Engine), total accuracy 31/31 = 100%

## Documentation

- Quick Start: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- File List: [docs/FILES.md](docs/FILES.md)
- Scenario Development Standard: [docs/SCENARIO_STANDARD.md](docs/SCENARIO_STANDARD.md)
- Complete Documentation: [docs/README.md](docs/README.md)

## Tools

| Script | Function | Applicable Scenarios | Usage |
| ------------------------ | -------- | -------- | ------ |
| `validate_scenario.py` | Scenario validation | All | Local |
| `detect_violations.py` | Violation detection | All | Local |
| `run_scenario.py` | Scenario execution | S001-S008 | Server |
| `run_scenario_motion.py` | Motion parameter scenario execution | S009-S012 | Server |
| `run_scenario_vlos.py` | VLOS and BVLOS scenario execution | S013-S014 | Server |
| `run_scenario_path.py` | Avoidance scenario execution (Pre-flight + In-flight) | S015-S016 | Server |
| `run_scenario_payload.py` | Payload and drop scenario execution (Pre-flight + Drop detection) | S017 | Server |
| `run_scenario_multi.py` | Multi-drone coordination scenario execution (Simultaneous + Sequential) | S018 | Server |
| `run_scenario_airspace.py` | Airspace classification scenario execution (Altitude boundaries + Restricted zones + Multi-target) | S019 | Server |
| `run_scenario_timeline.py` | Approval timeline scenario execution (Time calculation + Waiver logic) | S020 | Server |
| `run_scenario_llm_validator.py` | LLM compliance validation (Gemini 2.5 Flash) | S016-S020 | Local |

## Creating New Scenarios

```bash
# 1. Copy template
cp templates/scene_config_template.jsonc scenarios/basic/S00X.jsonc

# 2. Edit configuration
# Modify drone position, no-fly zones and other parameters

# 3. Create ground truth
cp templates/ground_truth_template.json ground_truth/S00X_violations.json

# 4. Validate
python scripts/validate_scenario.py scenarios/basic/S00X.jsonc
```

See [`templates/scenario_template.md`](templates/scenario_template.md) for details

Version: 3.0 
Last Updated: 2025-11-01 
New: S016-S020 LLM validation completed (31/31 test cases = 100% accuracy) using Gemini 2.5 Flash for dual-engine comparative validation, proving LLMs can replace rule engines for UAV compliance assessment 
Milestone: All 20 scenarios (S001-S020) designed and tested successfully
