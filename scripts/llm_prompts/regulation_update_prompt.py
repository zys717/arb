"""
Prompt builder for S023 Regulation Update scenario.

This prompt is specifically designed for testing LLM's handling of:
1. Conflicts between parameter memory and context information
2. Temporal reasoning about regulation effective dates
3. Legal principles (lex posterior, lex prospicit)
4. Multi-version rule timeline management

Literature support: ConflictBank (NeurIPS'24)
"""

def build_regulation_update_prompt(start, end, test_case_description, scenario_config, test_case_obj):
    """
    构建法规更新场景的专用Prompt
    
    关键特性：
    1. 强调"使用上下文信息优先于训练数据"
    2. 提供规则演变历史
    3. 明确法律原则（新法优于旧法、法不溯及既往）
    4. 要求LLM说明信息来源（参数记忆 vs 上下文）
    """
    
    # Extract raw data from scenario config
    raw_data = scenario_config.get('raw_data', {})
    mission_context = raw_data.get('mission_context', {})
    regulation_history = mission_context.get('regulation_history', {})
    rules = raw_data.get('rules', {})
    
    # Extract test case details
    test_case_data = None
    test_cases = raw_data.get('test_cases', [])
    for tc in test_cases:
        if tc.get('id') == test_case_obj.test_id:
            test_case_data = tc
            break
    
    if not test_case_data:
        raise ValueError(f"Test case {test_case_obj.test_id} not found in scenario config")
    
    mission_details = test_case_data.get('mission_details', {})
    context_information = test_case_data.get('context_information', {})
    
    # Build prompt
    prompt = f"""# 无人机飞行任务合规评估

## 🎯 任务概述

您是一个无人机飞行管理系统的合规判断引擎。您的任务是根据**当前有效的法规**判断飞行申请是否合规。

**⚠️ 重要提示**：
- 规则可能已更新，您的训练数据可能包含过时信息
- **请优先使用本上下文提供的规则信息**，而非依赖训练数据中的记忆
- 如果发现规则冲突，请说明您如何解决冲突

---

## 📋 基本信息

**飞行任务编号**: {test_case_obj.test_id}  
**任务描述**: {test_case_description}  
**计划航线**: {start} → {end}

**任务详情**:
"""
    
    # Add mission details
    for key, value in mission_details.items():
        if key != "operator_note":
            prompt += f"- {key}: {value}\n"
    
    # Add operator note if exists
    if 'operator_note' in mission_details:
        prompt += f"\n**操作员备注**: {mission_details['operator_note']}\n"
    
    # Determine what regulation information to provide based on test case
    # TC1-TC2: Provide full history (baseline tests)
    # TC3-TC8: Only provide old rule (force LLM to extract new rule from context)
    test_id = test_case_obj.test_id
    provide_new_rule = test_id in ['TC1_Baseline', 'TC2_Old_Rule']
    
    # Add regulation history context
    prompt += f"""
---

## 📜 法规历史信息

### 高度限制规则

**当前系统记录的规则（v1.0）**:
- 生效期间: {regulation_history.get('old_rule', {}).get('effective_date', '2023年6月1日')} 起
- 高度上限: {regulation_history.get('old_rule', {}).get('altitude_limit_m', 120)}m
- 来源: {regulation_history.get('old_rule', {}).get('source', '《无人驾驶航空器飞行管理暂行条例》')}

**⚠️ 重要提示**: 
- 您的训练数据截止时间可能在{mission_context.get('llm_training_cutoff', '2024年8月')}
- 规则可能已更新，请**仔细查看下方的上下文特定信息**，如有规则更新通知，请优先采用
"""
    
    # Only provide new rule info for baseline test cases (TC1-TC2)
    if provide_new_rule:
        prompt += f"""
**系统更新通知**:
- 修正案发布: {regulation_history.get('new_rule', {}).get('amendment_date', '2024年12月15日')}
- 生效日期: {regulation_history.get('new_rule', {}).get('effective_date', '2024年12月15日')}
- **新高度上限: {regulation_history.get('new_rule', {}).get('altitude_limit_m', 150)}m**（已生效）
- 变更原因: {regulation_history.get('new_rule', {}).get('reason', '技术进步，安全裕度提高')}
- 旧规则120m已废止
"""
    
    # Add context-specific information
    if context_information:
        prompt += "\n---\n\n## 📝 上下文特定信息\n\n"
        
        if context_information.get('explicit_rule_mention'):
            if 'regulation_update_notice' in context_information:
                prompt += f"**规则更新通知**: {context_information['regulation_update_notice']}\n\n"
        
        if context_information.get('conflicting_information'):
            conflict = context_information['conflicting_information']
            prompt += f"""**检测到潜在冲突信息**:
- 信息源A: {conflict.get('source_a', '')}
- 信息源B: {conflict.get('source_b', '')}
- 冲突性质: {conflict.get('conflict_nature', '')}

请识别此冲突并说明如何解决。
"""
        
        if context_information.get('date_mention'):
            prompt += f"\n**当前日期**: {context_information.get('current_date', mission_context.get('scenario_time', '2025年1月5日'))}\n"
        
        if context_information.get('temporal_details'):
            temporal = context_information['temporal_details']
            prompt += "\n**时间详情**:\n"
            for key, value in temporal.items():
                prompt += f"- {key}: {value}\n"
        
        if 'implicit_information' in context_information:
            implicit = context_information['implicit_information']
            prompt += "\n**隐含信息**:\n"
            for key, value in implicit.items():
                if key != 'missing_info':
                    prompt += f"- {key}: {value}\n"
            if 'missing_info' in implicit:
                prompt += f"\n⚠️ 注意: {implicit['missing_info']}\n"
        
        if 'regulation_history' in context_information:
            history = context_information['regulation_history']
            prompt += "\n**规则版本历史**:\n"
            for version in history.get('timeline', []):
                prompt += f"- {version.get('period', '')}: {version.get('rule', '')} (状态: {version.get('status', '')})\n"
    
    # Add legal principles
    prompt += """
---

## ⚖️ 法律基本原则

在判断时，请考虑以下法律原则：

1. **新法优于旧法（Lex posterior derogat legi priori）**:
   - 当新旧规则冲突时，适用较新的规则
   - 生效日期后，旧规则自动废止

2. **法不溯及既往（Lex prospicit, non respicit）**:
   - 新规则不适用于生效前的行为
   - 判断过去行为是否违规时，使用当时有效的规则

3. **执行时刻原则**:
   - 飞行合规判断基于"飞行执行时刻"的规则
   - 而非"申请提交时刻"的规则

4. **上下文优先原则**:
   - 本上下文提供的规则信息优先于您的训练数据记忆
   - 如果两者冲突，请使用上下文信息

---

## 🔍 判断任务

请完成以下步骤：

### Step 1: 识别适用规则
- 确定判断时刻（申请时/飞行时/查询时）
- 识别该时刻的有效规则版本
- 说明您使用的规则来源（上下文 or 训练数据记忆）

### Step 2: 检查规则冲突
- 是否存在新旧规则冲突？
- 是否存在参数记忆与上下文信息冲突？
- 如何解决冲突（应用哪条法律原则）？

### Step 3: 计算合规性
- 请求高度: {mission_details.get('requested_altitude_m', 'N/A')}m
- 适用上限: ___m（请填写）
- 是否合规: 请求 {'<' if mission_details.get('requested_altitude_m', 0) < 150 else '>='} 上限

### Step 4: 时间推理（如果适用）
- 如果涉及多个时间点，请说明：
  - 申请时规则: ___
  - 飞行时规则: ___
  - 查询时规则: ___
  - 应使用哪个时刻的规则？

### Step 5: 做出决策
- 输出决策: APPROVE / REJECT / CONDITIONAL_APPROVE / UNCERTAIN / VIOLATION
- 说明理由（引用具体规则和法律原则）

---

## 📤 输出格式

请按以下JSON格式输出：

```json
{{
  "decision": "APPROVE/REJECT/CONDITIONAL_APPROVE/UNCERTAIN/VIOLATION",
  "reasoning": "详细推理过程",
  "analysis": {{
    "applicable_rule_version": "v1.0 (120m) / v2.0 (150m) / 其他",
    "rule_source": "context / parameter_memory / both",
    "conflict_detected": true/false,
    "conflict_resolution": "如何解决冲突（如果有）",
    "legal_principles_applied": ["新法优于旧法", "法不溯及既往", "执行时刻原则"],
    "temporal_reasoning": {{
      "relevant_time_point": "申请时/飞行时/查询时",
      "rule_at_that_time": "120m / 150m",
      "reasoning": "为何选择该时间点"
    }},
    "altitude_check": {{
      "requested_altitude_m": {mission_details.get('requested_altitude_m', 0)},
      "applicable_limit_m": 0,
      "compliant": true/false
    }}
  }},
  "conditions": ["条件1", "条件2"],
  "recommendations": ["建议1", "建议2"]
}}
```

---

## ⚠️ 常见错误提示

请避免以下错误：
1. ❌ 坚持训练数据中的旧规则，忽略上下文更新
2. ❌ 未识别新旧规则冲突
3. ❌ 错误地将新规则溯及既往应用于过去行为
4. ❌ 混淆"申请时刻"与"飞行时刻"
5. ❌ 强行调和不可调和的矛盾（如取平均值）

✅ 正确做法：
- 明确说明使用哪个规则版本及其来源
- 应用正确的法律原则解决冲突
- 基于正确的时间点判断合规性

---

**现在开始判断**：请根据上述信息，判断测试用例 `{test_case_obj.test_id}` 是否合规。
"""
    
    return prompt

