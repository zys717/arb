# AirSim-RuleBench 快速开始

## 本地验证（Mac）

```bash
cd AirSim-RuleBench/scripts

# 1. 验证场景配置
python validate_scenario.py ../scenarios/basic/S001_geofence_basic.jsonc

# 2. 生成测试轨迹
python detect_violations.py --generate-test-trajectory ../test_logs/test.json --scenario violating

# 3. 检测违规
python detect_violations.py ../test_logs/test.json -g ../ground_truth/S001_violations.json
```

## 服务器执行

### 传输文件
```bash
# 场景文件
scp -P 10427 scenarios/basic/S001_geofence_basic.jsonc \
    root@SERVER:/home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/

# 运行脚本
scp -P 10427 scripts/run_scenario.py \
    root@SERVER:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/
```

### 运行场景
```bash
# 在服务器上
cd ~/project/ProjectAirSim/client/python/example_user_scripts

python run_scenario.py \
    /home/sduser/project/ProjectAirSim/client/python/airsimv1_scripts_migrated/multirotor/sim_config/S001_geofence_basic.jsonc \
    --output trajectory_S001.json \
    --mode auto
```

### 下载结果
```bash
# 在本地 Mac
scp -P 10427 \
    root@SERVER:/home/sduser/project/ProjectAirSim/client/python/example_user_scripts/trajectory_S001.json \
    test_logs/
```

## 分析结果

```bash
cd scripts
python detect_violations.py ../test_logs/trajectory_S001.json \
    -g ../ground_truth/S001_violations.json
```

## 创建新场景

1. 复制模板：`cp templates/scene_config_template.jsonc scenarios/basic/S00X.jsonc`
2. 修改场景参数
3. 复制标注模板：`cp templates/ground_truth_template.json ground_truth/S00X_violations.json`
4. 定义预期行为
5. 验证：`python validate_scenario.py scenarios/basic/S00X.jsonc`

---

详细文档见 `README.md` 和 `templates/` 目录。

