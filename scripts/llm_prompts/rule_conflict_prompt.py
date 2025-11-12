"""
Prompt builder for S022 Rule Conflict and Priority Resolution scenarios.
Guides LLM to identify rule conflicts and perform priority reasoning.
"""

from typing import Dict, Any, List
import json


def build_rule_conflict_prompt(start, end, test_case_description: str,
                                scenario_config: Dict, test_case_obj: Any = None) -> str:
    """
    Build a specialized prompt for rule conflict resolution scenarios (S022).
    
    This prompt guides the LLM to:
    1. Identify all triggered rules
    2. Detect conflicts between rules
    3. Apply priority reasoning framework
    4. Determine exemption applicability
    5. Provide final decision with complete reasoning chain
    """
    
    # Extract test case data from raw_data
    raw_data = scenario_config.get('raw_data', {})
    test_case_data = {}
    
    if test_case_obj:
        test_id = test_case_obj.test_id if hasattr(test_case_obj, 'test_id') else ''
        for tc in raw_data.get('test_cases', []):
            if tc.get('id') == test_id:
                test_case_data = tc
                break
    
    # Extract mission details from test case
    mission_details = test_case_data.get('mission_details', {})
    mission_type = mission_details.get('mission_type', 'unknown')
    urgency = mission_details.get('urgency_level', 'UNKNOWN')
    
    # Extract rules from scenario config (from raw_data)
    rules = raw_data.get('rules', {})
    priority_framework = raw_data.get('priority_framework', {})
    
    # Format rules information
    rules_text = "## Available Rules:\n\n"
    for rule_id, rule_data in rules.items():
        rules_text += f"### {rule_id}\n"
        rules_text += f"- **Name**: {rule_data.get('name', '')}\n"
        rules_text += f"- **Category**: {rule_data.get('category', '')}\n"
        rules_text += f"- **Priority**: {rule_data.get('priority', '')} (Level {rule_data.get('priority_level', '')})\n"
        rules_text += f"- **Description**: {rule_data.get('description', '')}\n"
        
        exemptions = rule_data.get('exemptions', {})
        if exemptions:
            if 'allowed' in exemptions:
                rules_text += f"- **Can be waived by**: {', '.join(exemptions['allowed']) if isinstance(exemptions['allowed'], list) else exemptions['allowed']}\n"
            if 'cannot_waive' in exemptions:
                rules_text += f"- **Cannot waive**: {', '.join(exemptions['cannot_waive']) if isinstance(exemptions['cannot_waive'], list) else 'N/A'}\n"
            if 'conditions' in exemptions:
                rules_text += f"- **Waiver conditions**: {'; '.join(exemptions['conditions']) if isinstance(exemptions['conditions'], list) else exemptions['conditions']}\n"
            if 'reason' in exemptions:
                rules_text += f"- **Waiver reasoning**: {exemptions['reason']}\n"
        
        legal_basis = rule_data.get('legal_basis', '')
        if legal_basis:
            rules_text += f"- **Legal basis**: {legal_basis}\n"
        
        rules_text += "\n"
    
    # Format priority framework
    framework_text = "## Rule Priority Framework:\n\n"
    if priority_framework:
        desc = priority_framework.get('description', '')
        framework_text += f"{desc}\n\n"
        
        levels = priority_framework.get('levels', {})
        for level_key, level_data in sorted(levels.items()):
            framework_text += f"### {level_key.replace('_', ' ').upper()}\n"
            framework_text += f"- **Rules**: {', '.join(level_data.get('rules', []))}\n"
            framework_text += f"- **Characteristics**: {level_data.get('characteristics', '')}\n"
            framework_text += f"- **Rationale**: {level_data.get('rationale', '')}\n\n"
        
        resolution_order = priority_framework.get('conflict_resolution_order', [])
        if resolution_order:
            framework_text += "### Conflict Resolution Order:\n"
            for step in resolution_order:
                framework_text += f"- {step}\n"
            framework_text += "\n"
    
    # Extract specific scenario details
    weather_text = ""
    if 'weather_conditions' in test_case_data:
        weather = test_case_data['weather_conditions']
        weather_text = f"\n## Weather Conditions:\n"
        weather_text += f"- **Visibility**: {weather.get('visibility_m', 'N/A')}m (Required: {weather.get('visibility_required', 500)}m)\n"
        weather_text += f"- **Wind Speed**: {weather.get('wind_speed_ms', 'N/A')}m/s\n"
        weather_text += f"- **Note**: {weather.get('weather_note', '')}\n"
    
    nfz_text = ""
    if 'nfz_proximity' in test_case_data:
        nfz = test_case_data['nfz_proximity']
        nfz_text = f"\n## NFZ Proximity:\n"
        nfz_text += f"- **Nearest NFZ**: {nfz.get('nearest_nfz', 'N/A')}\n"
        nfz_text += f"- **Distance to boundary**: {nfz.get('distance_to_boundary', 'N/A')}m\n"
        nfz_text += f"- **Risk assessment**: {nfz.get('risk', '')}\n"
    elif 'nfz_details' in test_case_data:
        nfz = test_case_data['nfz_details']
        nfz_text = f"\n## NFZ Details:\n"
        nfz_text += f"- **Type**: {nfz.get('type', 'N/A')}\n"
        nfz_text += f"- **Can waive**: {nfz.get('can_waive', 'N/A')}\n"
    
    battery_text = ""
    if 'battery_status' in test_case_data:
        battery = test_case_data['battery_status']
        battery_text = f"\n## Battery Status:\n"
        battery_text += f"- **Current battery**: {battery.get('current_percent', 'N/A')}%\n"
        battery_text += f"- **Base required**: {battery.get('base_required_percent', 'N/A')}%\n"
        if 'wind_multiplier' in battery:
            battery_text += f"- **Wind adjustment**: {battery.get('wind_multiplier', 1.0)}x multiplier\n"
            battery_text += f"- **Adjusted required**: {battery.get('adjusted_required_percent', 'N/A')}%\n"
        battery_text += f"- **Note**: {battery.get('note', '')}\n"
    
    legal_auth_text = ""
    legal_auth = mission_details.get('legal_authorization', {})
    if legal_auth:
        legal_auth_text = f"\n## Legal Authorization:\n"
        legal_auth_text += f"- **Warrant present**: {legal_auth.get('warrant_present', False)}\n"
        legal_auth_text += f"- **Warrant type**: {legal_auth.get('warrant_type', 'N/A')}\n"
        legal_auth_text += f"- **Issued by**: {legal_auth.get('issued_by', 'N/A')}\n"
        legal_auth_text += f"- **Target area**: {legal_auth.get('target_area', 'N/A')}\n"
    
    suspicious_text = ""
    suspicious = mission_details.get('suspicious_indicators', {})
    if suspicious:
        suspicious_text = f"\n## Suspicious Indicators (Check for fake emergency):\n"
        for key, value in suspicious.items():
            suspicious_text += f"- **{key.replace('_', ' ').title()}**: {value}\n"
    
    multi_mission_text = ""
    if 'mission_a' in test_case_data:
        mission_a = test_case_data['mission_a']
        mission_b = test_case_data['mission_b']
        multi_mission_text = f"\n## Multi-Mission Scenario:\n"
        multi_mission_text += f"### Mission A (Commercial):\n"
        multi_mission_text += f"- **Description**: {mission_a.get('description', '')}\n"
        multi_mission_text += f"- **Client**: {mission_a.get('client', '')}\n"
        multi_mission_text += f"- **Penalty**: {mission_a.get('contract_penalty', '')}\n"
        multi_mission_text += f"\n### Mission B (Emergency):\n"
        multi_mission_text += f"- **Description**: {mission_b.get('description', '')}\n"
        multi_mission_text += f"- **Condition**: {mission_b.get('patient_condition', '')}\n"
        multi_mission_text += f"- **Urgency**: {mission_b.get('urgency_level', '')}\n"
        multi_mission_text += f"\n**Note**: Only one drone available, must choose one mission.\n"
    
    # Build the complete prompt
    prompt = f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in **rule conflict resolution and priority reasoning**.

## Mission Overview
You are analyzing a flight request where **multiple rules may be triggered, and some rules may conflict with each other**.

**Test Case**: {test_case_description}
**Mission Type**: {mission_type}
**Urgency Level**: {urgency}

## Your Task
Analyze this flight request and determine the appropriate decision by:
1. **Identifying ALL applicable rules** from the rule database below
2. **Detecting conflicts** between rules
3. **Applying the priority framework** to resolve conflicts
4. **Checking exemption clauses** to see if lower-priority rules can be waived
5. **Providing a final decision** with complete reasoning chain

{rules_text}

{framework_text}

## Critical Principles for Conflict Resolution

### 1. **Physical Constraints are ABSOLUTE**
- Rules about weather (R005), battery (R021), and physical limitations **CANNOT be waived**, even by emergency exemptions
- Physical laws cannot be changed by urgency or authorization
- Example: If wind speed exceeds safe limits, no amount of urgency makes it safe to fly

### 2. **Emergency Exemption Scope (R002)**
- **Can waive**: Procedural rules (noise R003, some privacy rules)
- **Cannot waive**: Physical constraints (weather, battery), absolute NFZ without prior approval
- **Requires verification**: Check if claimed "emergency" is truly life-threatening
- **Fake emergencies**: Commercial delivery disguised as "emergency" should be rejected

### 3. **Legal Rights Require Legal Process**
- Privacy protection (R004) can be waived ONLY with proper legal authorization (e.g., search warrant)
- Check for warrant presence, validity, and scope

### 4. **Priority Hierarchy**
When rules conflict, apply this hierarchy:
```
Level 1 (CRITICAL): Physical safety (weather, battery) + Absolute NFZ
    ↓
Level 2 (HIGH): Emergency exemptions + Mission priority
    ↓
Level 3 (HIGH-LEGAL): Legal rights (privacy, requiring legal process)
    ↓
Level 4 (MEDIUM): Procedural rules (noise, comfort)
```

### 5. **Multi-Rule Conflicts**
When 3+ rules conflict:
- Identify non-negotiable constraints (Level 1 CRITICAL)
- If ANY Level 1 constraint fails AND cannot be waived → **REJECT immediately**
- Apply exemptions to negotiable rules (Level 3-4)
- Provide reasoning chain showing the failure point

### 6. **Balancing Rights (Complex Cases)**
For privacy vs. public interest:
- Consider: location privacy expectation, activity nature, public interest level
- Apply "minimum intrusion" principle
- Use CONDITIONAL_APPROVE with strict boundaries when both rights have merit

## Mission-Specific Details
{weather_text}{nfz_text}{battery_text}{legal_auth_text}{suspicious_text}{multi_mission_text}

## Output Format

Provide your analysis in the following JSON format:

```json
{{
  "decision": "APPROVE | REJECT | CONDITIONAL_APPROVE | CHOOSE_A | CHOOSE_B",
  "confidence": "low | medium | high",
  "triggered_rules": [
    "R001_NFZ_absolute",
    "R002_emergency_exemption",
    ...
  ],
  "conflicts_identified": [
    {{
      "rule_a": "R001",
      "rule_b": "R002",
      "conflict_type": "absolute_constraint_vs_exemption",
      "resolution": "R001 priority higher, R002 cannot waive R001 without approval"
    }}
  ],
  "priority_analysis": {{
    "R001": {{
      "priority_level": 1,
      "can_waive": false,
      "status": "FAIL | PASS | WAIVED",
      "reason": "..."
    }},
    "R002": {{
      "priority_level": 2,
      "applicable": true,
      "waive_scope": ["R003"],
      "cannot_waive": ["R001", "R005"],
      "reason": "..."
    }}
  }},
  "reasoning_steps": [
    "Step 1: Identified triggered rules: ...",
    "Step 2: Detected conflict between R001 and R002: ...",
    "Step 3: Applied priority framework: R001 (Level 1) > R002 (Level 2)",
    "Step 4: Checked R002 exemption scope: cannot waive absolute NFZ",
    "Step 5: Final decision: REJECT due to Level 1 constraint failure",
    ...
  ],
  "emergency_verification": {{
    "is_genuine_emergency": true | false,
    "reason": "...",
    "suspicious_indicators": []
  }},
  "legal_basis": [
    "中国《条例》第XX条",
    "民法典第XXX条",
    ...
  ],
  "conditions": [
    "Only if CONDITIONAL_APPROVE: list specific conditions here"
  ],
  "alternative_suggested": "None | Specific alternative action"
}}
```

## Important Reminders
1. **Always check for physical constraints first** - they cannot be waived
2. **Verify genuine emergency** - don't be fooled by fake urgency
3. **Understand exemption scope** - R002 has clear limitations
4. **Multi-rule conflicts** - trace through the complete reasoning chain
5. **Legal process matters** - warrants are required for privacy waivers
6. **Balance carefully** - for rights conflicts, use CONDITIONAL_APPROVE with boundaries

Begin your analysis now.
"""
    
    return prompt


def extract_rule_conflict_response(llm_response: Dict) -> Dict:
    """
    Extract and validate the rule conflict response from LLM.
    
    Returns a normalized response dictionary with conflict analysis.
    """
    # Normalize the response
    normalized = {
        'decision': llm_response.get('decision', 'UNKNOWN').upper(),
        'confidence': llm_response.get('confidence', 'unknown').lower(),
        'triggered_rules': llm_response.get('triggered_rules', []),
        'conflicts_identified': llm_response.get('conflicts_identified', []),
        'priority_analysis': llm_response.get('priority_analysis', {}),
        'reasoning_steps': llm_response.get('reasoning_steps', []),
        'emergency_verification': llm_response.get('emergency_verification', {}),
        'legal_basis': llm_response.get('legal_basis', []),
        'conditions': llm_response.get('conditions', []),
        'alternative_suggested': llm_response.get('alternative_suggested', 'None')
    }
    
    # Build a combined reasoning string
    reasoning_text = '\n'.join(normalized['reasoning_steps']) if normalized['reasoning_steps'] else 'No reasoning provided'
    normalized['reasoning'] = reasoning_text
    
    return normalized

