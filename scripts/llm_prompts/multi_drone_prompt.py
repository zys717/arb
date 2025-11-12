"""
Multi-Drone Coordination Prompt Builder

Handles multi-drone scenarios:
- S018: Multi-drone coordination, operator limits, separation distance, swarm approval

Supports:
- Operator extraction from actor metadata
- Sequential vs simultaneous operation modes
- Swarm flight approval mechanism
- Operator limit waivers
"""

from typing import Dict, Any


def build_multi_drone_prompt(start, end, test_case_description: str,
                             scenario_config: Dict, test_case_obj: Any = None) -> str:
    """
    Build prompt for Multi-drone scenarios (S018).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        test_case_obj: TestCase object (optional, for multi-drone info)
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract multi-drone configuration
    raw_data = scenario_config.get('raw_data', {})
    scenario_params = raw_data.get('scenario_parameters', {})
    coordination = scenario_params.get('coordination_rules', {})
    
    max_drones_per_operator = coordination.get('max_drones_per_operator', 1)
    min_separation_m = coordination.get('min_separation_distance_m', 50.0)
    swarm_threshold = coordination.get('swarm_flight_threshold', 3)
    
    # Get test case specific info from raw_data (not in TestCase dataclass)
    active_drones = []
    operators = []
    operation_mode = "simultaneous"
    swarm_approval = False
    
    if test_case_obj:
        test_id = test_case_obj.test_id if hasattr(test_case_obj, 'test_id') else ''
        for tc in raw_data.get('test_cases', []):
            if tc.get('id') == test_id:
                active_drones = tc.get('active_drones', [])
                
                # Handle both operation_mode (string) and sequential_mode (bool) fields
                if 'operation_mode' in tc:
                    operation_mode = tc.get('operation_mode', 'simultaneous')
                elif tc.get('sequential_mode', False):
                    operation_mode = 'sequential'
                else:
                    operation_mode = 'simultaneous'
                
                swarm_approval = tc.get('has_approval', False) or tc.get('swarm_approval', False)
                
                # Extract operators from actors metadata (based on active_drones)
                actors = raw_data.get('actors', [])
                operator_set = set()
                for drone_name in active_drones:
                    for actor in actors:
                        if actor.get('name') == drone_name:
                            operator_id = actor.get('metadata', {}).get('operator_id')
                            if operator_id:
                                operator_set.add(operator_id)
                            break
                operators = list(operator_set)
                break
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in multi-drone coordination and operator regulations.

## Mission
Analyze whether a multi-drone operation complies with operator limits, separation distances, and swarm flight approval requirements.

## Flight Plan
- **Active drones**: {len(active_drones)} drone(s): {', '.join(active_drones) if active_drones else 'N/A'}
- **Operators**: {len(operators)} operator(s)
- **Operation mode**: {operation_mode}
- **Swarm approval**: {'YES' if swarm_approval else 'NO'}

## Multi-Drone Configuration
- **Maximum drones per operator**: {max_drones_per_operator}
- **Minimum separation distance**: {min_separation_m}m
- **Swarm flight threshold**: {swarm_threshold} drones (≥{swarm_threshold} requires approval)

## Regulations
### Single Operator Limit (FAA Part 107.35):
- **Rule**: "One person may not operate more than one UAS at the same time"
- **Standard limit**: 1 drone per operator (max_drones_per_operator = {max_drones_per_operator})
- **Exception**: Sequential operation mode (one at a time, not simultaneous)
- **Swarm approval**: If granted, operator limit may be waived for coordinated swarm operations

### Separation Distance:
- **Minimum safe distance**: {min_separation_m}m between any two drones
- **Purpose**: Collision avoidance and safe operation
- **Check**: Use ≥ comparison (50.0m ≥ 50.0m is compliant, boundary inclusive)

### Swarm Flight Approval:
- **Threshold**: {swarm_threshold}+ drones flying together requires special approval
- **If approved**: Waives single-operator limit, allows coordinated multi-drone operations
- **If not approved**: Standard limits apply (1 drone per operator, separation required)

## Decision Logic Priority (Highest to Lowest):
1. **Swarm approval check**: If ≥{swarm_threshold} drones AND swarm_approval=YES → Waive operator limits
2. **Operator limit check**: Each operator controls ≤ {max_drones_per_operator} drones (unless swarm approved)
3. **Separation distance**: All drone pairs maintain ≥ {min_separation_m}m distance
4. **Sequential mode exemption**: If operation_mode='sequential' → Waive operator limit

## Your Task
**Analyze multi-drone compliance step-by-step:**

1. **Count drones and operators**:
   - How many active drones?
   - How many operators?
   - Which operator controls which drones?

2. **Check swarm approval** (if applicable):
   - Is drone count ≥ {swarm_threshold}?
   - Is swarm approval granted?
   - If both YES → Operator limits waived, proceed to separation check

3. **Check operator limits** (if not swarm-approved):
   - Is operation mode 'sequential'? → Operator limit waived
   - Does any operator control > {max_drones_per_operator} drones simultaneously?
   - Violation if YES

4. **Check separation distances**:
   - Calculate distance between all drone pairs
   - Are all distances ≥ {min_separation_m}m?
   - Use 2D horizontal distance

5. **Make final decision**: 
   - REJECT: Operator limit violated OR separation insufficient
   - APPROVE: All checks passed

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of analysis",
  "detailed_steps": [
    "Step 1: Drone and operator count...",
    "Step 2: Swarm approval check...",
    "Step 3: Operator limit check...",
    "Step 4: Separation distance check...",
    "..."
  ],
  "multi_drone_analysis": {{
    "total_drones": <number>,
    "total_operators": <number>,
    "operation_mode": "{operation_mode}",
    "swarm_approval_required": true or false,
    "swarm_approval_granted": {str(swarm_approval).lower()},
    "operator_limit_check": "PASS or FAIL or WAIVED",
    "separation_check": "PASS or FAIL or N/A",
    "min_separation_found_m": <number or null>,
    "violations": []
  }}
}}

## Important Notes
- Swarm approval waives operator limits but NOT separation requirements
- Sequential mode waives operator limits (drones operate one at a time)
- Separation uses ≥ comparison (50.0m ≥ 50.0m is OK)
- Priority: Swarm approval > Operator limit > Separation distance
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""
