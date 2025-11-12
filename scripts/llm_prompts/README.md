# LLM Prompt Templates

本模块包含用于 AirSim-RuleBench LLM验证的专用prompt构建器。

## 📁 模块结构

```
llm_prompts/
├── __init__.py              # 模块入口，导出所有prompt构建器
├── base_prompt.py           # 通用工具函数（NFZ格式化等）
├── nfz_prompt.py           # S001-S008, S015-S016 (NFZ/障碍物)
├── altitude_prompt.py      # S006-S008 (高度限制)
├── speed_prompt.py         # S009-S010 (速度限制)
├── vlos_prompt.py          # S013-S014 (视距要求)
├── time_prompt.py          # S011-S012 (时间限制)
├── payload_prompt.py       # S017 (载重与投放)
├── multi_drone_prompt.py   # S018 (多机协同)
├── airspace_prompt.py      # S019 (空域分类)
└── timeline_prompt.py      # S020 (审批时限)
```

## 🎯 设计原则

### 1. 模块化
- 每个场景类型独立文件
- 便于维护和扩展
- 减少主脚本复杂度

### 2. 一致性
所有prompt构建器遵循统一接口：
```python
def build_xxx_prompt(start, end, test_case_description: str,
                     scenario_config: Dict, test_case_obj: Any = None) -> str:
    """返回格式化的LLM prompt字符串"""
```

### 3. 专业化
- 每个prompt包含场景特定的规则和检查逻辑
- 明确的输出格式要求（JSON）
- 详细的分步分析指导

## 📊 使用示例

### 导入prompt构建器
```python
from llm_prompts import build_nfz_prompt, build_payload_prompt

# 构建NFZ场景prompt
prompt = build_nfz_prompt(
    start=start_pos,
    end=end_pos,
    nfzs=nfz_configs,
    test_case_description="TC1_SimpleGeofence",
    scenario_config=config,
    test_case_obj=test_case
)
```

### 添加新场景类型
1. 在 `classify_scenario()` 中添加场景ID映射
2. 创建新的 `xxx_prompt.py` 文件
3. 在 `__init__.py` 中导出新函数
4. 在主脚本 `check_compliance_llm()` 中添加调用

## 📈 代码统计

- **总文件**: 11个 (.py)
- **总代码**: ~1650行
- **平均文件大小**: ~150行
- **最大文件**: payload_prompt.py (231行)
- **最小文件**: base_prompt.py (40行)

## 🔄 版本历史

### v1.0 (2025-11-01)
- 初始重构：从单文件 (2077行) 拆分为模块化结构
- 提取9种场景类型的prompt构建器
- 代码精简65%，提升可维护性

## 📝 维护指南

### 修改现有Prompt
直接编辑对应的 `xxx_prompt.py` 文件

### 调试Prompt
在prompt文件中修改后，无需重启Python，重新导入即可：
```python
import importlib
import llm_prompts.nfz_prompt
importlib.reload(llm_prompts.nfz_prompt)
```

### 测试单个Prompt
```bash
python3 -c "
from llm_prompts import build_nfz_prompt
# 测试代码...
"
```

---

**作者**: AirSim-RuleBench Team  
**日期**: 2025-11-01  
**版本**: 1.0

