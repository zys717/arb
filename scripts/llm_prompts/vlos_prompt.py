"""
VLOS/BVLOS Prompt Builder

Handles Visual Line of Sight scenarios:
- S013: VLOS requirement (500m limit)
- S014: BVLOS waivers (visual observer, technical means, special permit)

Supports:
- Multiple waiver types with different range limits
- Test-case specific waiver activation
- Distance calculations from operator position
"""

import math
from typing import Dict, Any


def build_vlos_prompt(start, end, test_case_description: str,
                      scenario_config: Dict, test_case_obj: Any = None) -> str:
    """
    Build prompt for VLOS/BVLOS scenarios (S013-S014).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        test_case_obj: TestCase object (optional, for waiver info)
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract operator position
    # Try multiple possible locations for operator position
    operator_pos = None
    if 'vlos_restrictions' in scenario_config:
        vlos = scenario_config['vlos_restrictions']
        if 'operator_position' in vlos:
            xyz = vlos['operator_position'].get('xyz', '0.0 0.0 0.0')
            coords = [float(x) for x in xyz.split()]
            operator_pos = {'north': coords[0], 'east': coords[1]}
    
    if not operator_pos and 'scenario_parameters' in scenario_config:
        params = scenario_config['scenario_parameters']
        if 'vlos_configuration' in params:
            operator_pos = params['vlos_configuration'].get('operator_position', {'north': 0.0, 'east': 0.0})
    
    if not operator_pos:
        operator_pos = {'north': 0.0, 'east': 0.0}
    
    op_north = operator_pos.get('north', 0.0)
    op_east = operator_pos.get('east', 0.0)
    
    # BVLOS waiver information - check which waivers are enabled for this test case
    waiver_text = "**No BVLOS waivers active.**"
    
    # Get available waivers from scenario
    available_waivers = []
    if 'bvlos_waivers' in scenario_config:
        bvlos_config = scenario_config['bvlos_waivers']
        if 'available_waivers' in bvlos_config:
            available_waivers = bvlos_config['available_waivers']
    
    # Get which waivers are enabled for this test case
    enabled_waiver_ids = []
    if test_case_obj and hasattr(test_case_obj, 'waivers_enabled'):
        enabled_waiver_ids = test_case_obj.waivers_enabled
    elif test_case_obj and isinstance(test_case_obj, dict) and 'waivers_enabled' in test_case_obj:
        enabled_waiver_ids = test_case_obj['waivers_enabled']
    
    # Filter to only enabled waivers
    if enabled_waiver_ids and available_waivers:
        active_waivers = [w for w in available_waivers if w.get('waiver_id') in enabled_waiver_ids]
        if active_waivers:
            lines = ["**Active BVLOS Waivers:**"]
            for waiver in active_waivers:
                waiver_type = waiver.get('type', 'N/A')
                desc = waiver.get('description', 'N/A')
                conditions = waiver.get('conditions', {})
                max_range = conditions.get('max_effective_range_m', 'N/A')
                
                lines.append(f"- Waiver ID: {waiver.get('waiver_id', 'N/A')}")
                lines.append(f"  Type: {waiver_type}")
                lines.append(f"  Description: {desc}")
                lines.append(f"  Max effective range: {max_range}m")
                lines.append(f"  Note: {waiver.get('note', 'N/A')}")
                lines.append("")
            waiver_text = "\n".join(lines)
    
    # Calculate distances
    dist_start = math.sqrt((start.north - op_north)**2 + (start.east - op_east)**2)
    dist_end = math.sqrt((end.north - op_north)**2 + (end.east - op_east)**2)
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in Visual Line of Sight (VLOS) and Beyond Visual Line of Sight (BVLOS) regulations.

## Mission
Analyze whether a drone's flight violates VLOS requirements or requires BVLOS waivers.

## Flight Plan
- **Operator position**: ({op_north}, {op_east}) meters (North, East coordinates)
- **Start position**: ({start.north}, {start.east}) meters
- **Target position**: ({end.north}, {end.east}) meters
- **Distance at start**: {dist_start:.2f}m from operator
- **Distance at target**: {dist_end:.2f}m from operator
- **Max distance during flight**: ≈{max(dist_start, dist_end):.2f}m (approximation for straight line)
- **Altitude**: {start.altitude}m (constant)

## VLOS/BVLOS Waivers
{waiver_text}

## Regulations
- **FAA Part 107.31 & EASA**: Standard VLOS requirement is **500 meters** horizontal distance from operator
- **VLOS**: Drone must remain within unaided visual line of sight (typically ≤500m)
- **BVLOS**: Flights beyond VLOS require one of the following:
  1. **Visual observer**: Trained personnel maintaining visual contact (extends to ~1000m)
  2. **Technical means**: FPV with spotter, detect-and-avoid systems (extends to ~3000m)
  3. **Special permit**: Regulatory waiver for specific operations (extends to ~5000m)

## Your Task
**Analyze the VLOS/BVLOS compliance step-by-step:**

1. **Calculate horizontal distance**:
   - Distance from operator to start position
   - Distance from operator to target position  
   - Maximum distance during straight-line flight
   
2. **Check VLOS requirement**:
   - Is max distance ≤ 500m? → VLOS compliant (APPROVE)
   - Is max distance > 500m? → BVLOS required (check waivers)
   
3. **Check BVLOS waivers** (if needed):
   - Verify if appropriate waiver is active
   - Check if distance is within waiver limits
   
4. **Make final decision**: APPROVE (compliant) or REJECT (violation)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of VLOS/BVLOS analysis",
  "detailed_steps": [
    "Step 1: Distance calculation...",
    "Step 2: VLOS check...",
    "Step 3: Waiver check (if needed)...",
    "..."
  ],
  "vlos_analysis": {{
    "operator_position": [{op_north}, {op_east}],
    "max_distance_to_operator_m": <number>,
    "vlos_limit_m": 500,
    "within_vlos": true or false,
    "requires_bvlos_waiver": true or false,
    "waiver_available": true or false or null,
    "waiver_sufficient": true or false or null
  }}
}}

## Important Notes
- Calculate 2D horizontal distance: sqrt((N1-N2)² + (E1-E2)²)
- VLOS limit is **500m** by default
- For BVLOS: waiver type must match distance requirement
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

