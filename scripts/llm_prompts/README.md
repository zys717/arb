# LLM Prompt Templates

This module contains dedicated prompt builders for AirSim-RuleBench LLM validation.

## Module Structure

```
llm_prompts/
 __init__.py # Module entry point, exports all prompt builders
 base_prompt.py # Common utility functions (NFZ formatting, etc.)
 nfz_prompt.py # S001-S008, S015-S016 (NFZ/Obstacles)
 altitude_prompt.py # S006-S008 (Altitude limits)
 speed_prompt.py # S009-S010 (Speed limits)
 vlos_prompt.py # S013-S014 (Line-of-sight requirements)
 time_prompt.py # S011-S012 (Time restrictions)
 payload_prompt.py # S017 (Payload and drop)
 multi_drone_prompt.py # S018 (Multi-drone coordination)
 airspace_prompt.py # S019 (Airspace classification)
 timeline_prompt.py # S020 (Approval timeline)
```

## Design Principles

### 1. Modularity
- Independent file for each scenario type
- Easy to maintain and extend
- Reduces main script complexity

### 2. Consistency
All prompt builders follow a unified interface:
```python
def build_xxx_prompt(start, end, test_case_description: str,
 scenario_config: Dict, test_case_obj: Any = None) -> str:
 """Returns formatted LLM prompt string"""
```

### 3. Specialization
- Each prompt contains scenario-specific rules and checking logic
- Clear output format requirements (JSON)
- Detailed step-by-step analysis guidance

## Usage Examples

### Import prompt builders
```python
from llm_prompts import build_nfz_prompt, build_payload_prompt

# Build NFZ scenario prompt
prompt = build_nfz_prompt(
 start=start_pos,
 end=end_pos,
 nfzs=nfz_configs,
 test_case_description="TC1_SimpleGeofence",
 scenario_config=config,
 test_case_obj=test_case
)
```

### Add new scenario type
1. Add scenario ID mapping in `classify_scenario()`
2. Create new `xxx_prompt.py` file
3. Export new function in `__init__.py`
4. Add invocation in main script `check_compliance_llm()`

## Code Statistics

- Total files: 11 (.py)
- Total lines: ~1650
- Average file size: ~150 lines
- Largest file: payload_prompt.py (231 lines)
- Smallest file: base_prompt.py (40 lines)

## Version History

### v1.0 (2025-11-01)
- Initial refactoring: split from single file (2077 lines) to modular structure
- Extracted 9 scenario type prompt builders
- Code reduced by 65%, improved maintainability

## Maintenance Guide

### Modify existing prompt
Directly edit corresponding `xxx_prompt.py` file

### Debug prompt
After modifying prompt file, no need to restart Python, just reload:
```python
import importlib
import llm_prompts.nfz_prompt
importlib.reload(llm_prompts.nfz_prompt)
```

### Test single prompt
```bash
python3 -c "
from llm_prompts import build_nfz_prompt
# Test code...
"
```

Author: AirSim-RuleBench Team 
Date: 2025-11-01 
Version: 1.0
