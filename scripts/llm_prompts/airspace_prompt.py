"""
Airspace Classification Prompt Builder

Handles airspace classification scenarios:
- S019: Altitude-based airspace classification (controlled vs uncontrolled)

Supports:
- Multi-waypoint target checking
- Restricted area detection
- Light drone exemption in uncontrolled airspace
- China regulations (《条例》第19条、第31条)
"""

from typing import Dict, Any


def build_airspace_prompt(start, end, test_case_description: str,
                          scenario_config: Dict, test_case_obj: Any = None) -> str:
    """Build prompt for Airspace classification scenarios (S019)."""
    
    # Extract airspace configuration
    raw_data = scenario_config.get('raw_data', {})
    scenario_params = raw_data.get('scenario_parameters', {})
    airspace_config = scenario_params.get('airspace_classification', {})
    
    uncontrolled_altitude_limit = airspace_config.get('uncontrolled_altitude_limit_m', 120.0)
    drone_category = airspace_config.get('drone_category', 'light')
    
    # Restricted areas - extract from airspace_zones with type='restricted'
    airspace_zones = raw_data.get('airspace_zones', [])
    restricted_areas = [zone for zone in airspace_zones if zone.get('type') == 'restricted']
    
    restricted_text = ""
    if restricted_areas:
        lines = ["**Restricted Areas:**"]
        for area in restricted_areas:
            area_id = area.get('id', 'N/A')
            area_name = area.get('name', 'N/A')
            center = area.get('center', {})
            radius = area.get('radius', 0)
            
            lines.append(f"- **{area_id}** ({area_name})")
            lines.append(f"  Center: ({center.get('north', 0)}, {center.get('east', 0)}) meters")
            lines.append(f"  Radius: {radius}m")
            lines.append(f"  Note: Requires approval regardless of altitude")
            lines.append("")
        restricted_text = "\n".join(lines)
    
    # Get test case specific approval status and all targets from raw_data
    has_approval = False
    all_targets = []
    if test_case_obj:
        test_id = test_case_obj.test_id if hasattr(test_case_obj, 'test_id') else ''
        for tc in raw_data.get('test_cases', []):
            if tc.get('id') == test_id:
                has_approval = tc.get('has_approval', False)
                all_targets = tc.get('targets', [])
                break
    
    # Build targets display text
    targets_text = ""
    if all_targets:
        targets_lines = ["**Target waypoints** (All must be checked):"]
        for idx, target in enumerate(all_targets, 1):
            north = target.get('north', 0)
            east = target.get('east', 0)
            altitude = target.get('altitude', 0)
            targets_lines.append(f"  {idx}. Position ({north}, {east}) at {altitude}m AGL")
        targets_text = "\n".join(targets_lines)
    else:
        # Fallback to single target
        targets_text = f"**Target position**: ({end.north}, {end.east}) at {end.altitude}m AGL"
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in airspace classification and approval requirements.

## Mission
Analyze whether a drone flight requires regulatory approval based on altitude and airspace classification.

## Flight Plan
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
{targets_text}
- **Drone category**: {drone_category}
- **Flight approval status**: {'GRANTED' if has_approval else 'NOT GRANTED'}

## Airspace Classification
### Uncontrolled Airspace (适飞空域):
- **Altitude limit**: < {uncontrolled_altitude_limit}m AGL
- **Exemption**: Light drones (轻型无人机) in uncontrolled airspace do NOT require approval
- **Regulation**: China 《条例》第19条、第31条

### Controlled Airspace (管制空域):
- **Definition**: Altitude ≥ {uncontrolled_altitude_limit}m AGL
- **Requirement**: Requires flight approval (飞行审批)
- **Boundary check**: Use ≥ comparison ({uncontrolled_altitude_limit}m ≥ {uncontrolled_altitude_limit}m enters controlled airspace)

{restricted_text if restricted_text else ""}

## Regulations
### China 《条例》第19条:
- "适飞空域为真高120米以下空域"
- Translation: Uncontrolled airspace is below 120m true altitude

### China 《条例》第31条:
- "轻型、植保无人机在适飞空域内飞行，无需申请飞行活动"
- Translation: Light UAVs in uncontrolled airspace do not require approval

### Decision Rules:
1. **Restricted area check** (Highest priority):
   - If target is within any restricted area → Requires approval
   - Calculate 2D distance to restricted area center
   - If distance ≤ radius → Inside restricted area

2. **Altitude boundary check**:
   - If altitude ≥ {uncontrolled_altitude_limit}m → Controlled airspace → Requires approval
   - If altitude < {uncontrolled_altitude_limit}m → Uncontrolled airspace → Check exemption

3. **Exemption check**:
   - If light drone in uncontrolled airspace AND outside restricted areas → No approval needed

4. **Approval verification**:
   - If approval required but not granted → REJECT
   - If approval required and granted → APPROVE
   - If no approval required → APPROVE

## Your Task
**Analyze airspace compliance step-by-step:**

1. **Check ALL target waypoints** (Critical):
   - If multiple waypoints are provided, check EACH ONE
   - ALL waypoints must comply; if ANY ONE violates → REJECT entire flight

2. **Altitude classification** (for each waypoint):
   - Is target altitude ≥ {uncontrolled_altitude_limit}m?
   - Use ≥ comparison (boundary enters controlled airspace)
   - Classify as controlled or uncontrolled

3. **Restricted area check** (for each waypoint):
   - Is target position within any restricted area?
   - Calculate 2D distance: sqrt((N1-N2)² + (E1-E2)²)
   - If distance ≤ radius → Inside restricted area
   - ⚠️ **PRIORITY**: Restricted area check is HIGHEST priority

4. **Approval requirement determination**:
   - Restricted area → Requires approval (ANY waypoint in restricted → requires approval)
   - Controlled airspace → Requires approval (ANY waypoint ≥{uncontrolled_altitude_limit}m → requires approval)
   - Uncontrolled + Light drone + ALL waypoints outside restricted → No approval needed

5. **Approval verification**:
   - Does requirement match actual approval status?
   - If required but not granted → REJECT
   - If ALL waypoints compliant and (no approval required OR approval granted) → APPROVE

6. **Make final decision**: APPROVE or REJECT

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of airspace analysis",
  "detailed_steps": [
    "Step 1: Altitude classification...",
    "Step 2: Restricted area check...",
    "Step 3: Approval requirement...",
    "..."
  ],
  "airspace_analysis": {{
    "target_altitude_m": {end.altitude},
    "altitude_limit_m": {uncontrolled_altitude_limit},
    "airspace_type": "controlled or uncontrolled",
    "in_restricted_area": true or false,
    "restricted_area_id": "area_id or null",
    "requires_approval": true or false,
    "has_approval": {str(has_approval).lower()},
    "exemption_applies": true or false,
    "altitude_compliant": true or false
  }}
}}

## Important Notes
- **CRITICAL**: If multiple waypoints provided, check ALL of them. If ANY ONE requires approval → entire flight requires approval
- Altitude boundary uses ≥ ({uncontrolled_altitude_limit}m ≥ {uncontrolled_altitude_limit}m → controlled)
- Restricted areas require approval regardless of altitude (HIGHEST priority)
- Light drones in uncontrolled airspace are exempt (《条例》第31条) ONLY if ALL waypoints outside restricted areas
- Distance calculation is 2D horizontal: sqrt((N1-N2)² + (E1-E2)²)
- For multi-waypoint flights: airspace_analysis.target_altitude_m can be max altitude or representative value
- Priority: Restricted area > Altitude boundary > Exemption
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""