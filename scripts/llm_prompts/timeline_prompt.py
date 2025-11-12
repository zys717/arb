"""
Timeline/Approval Advance Notice Prompt Builder

Handles timeline-based approval scenarios:
- S020: Flight application advance notice requirements (36 hours)

Supports:
- ISO 8601 timestamp parsing
- Emergency mission exemption
- Uncontrolled airspace exemption
- Time difference calculation
"""

from typing import Dict, Any


def build_timeline_prompt(start, end, test_case_description: str,
                          scenario_config: Dict, test_case_obj: Any = None) -> str:
    """Build prompt for Timeline/approval advance notice scenarios (S020)."""
    
    # Extract timeline configuration
    raw_data = scenario_config.get('raw_data', {})
    scenario_params = raw_data.get('scenario_parameters', {})
    timeline_config = scenario_params.get('approval_timeline', {})
    
    required_advance_hours = timeline_config.get('required_advance_notice_hours', 36.0)
    
    # Get test case specific info from raw_data
    current_time = ""
    application_time = ""
    planned_flight_time = ""
    flight_type = "normal"
    in_controlled_zone = False
    
    if test_case_obj:
        test_id = test_case_obj.test_id if hasattr(test_case_obj, 'test_id') else ''
        for tc in raw_data.get('test_cases', []):
            if tc.get('id') == test_id:
                current_time = tc.get('current_time', '')
                application_time = tc.get('application_time', '')
                planned_flight_time = tc.get('planned_flight_time', '')
                flight_type = tc.get('flight_type', 'normal')
                in_controlled_zone = tc.get('in_controlled_zone', False)
                break
    
    # Restricted zones
    restricted_zones = raw_data.get('restricted_areas', [])
    restricted_text = ""
    if restricted_zones:
        lines = ["**Restricted/Controlled Zones:**"]
        for zone in restricted_zones:
            zone_id = zone.get('id', 'N/A')
            center = zone.get('center', {})
            radius = zone.get('radius', 0)
            
            lines.append(f"- **{zone_id}**")
            lines.append(f"  Center: ({center.get('north', 0)}, {center.get('east', 0)}) meters")
            lines.append(f"  Radius: {radius}m")
            lines.append(f"  Note: Flights in this zone require advance approval")
            lines.append("")
        restricted_text = "\n".join(lines)
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in flight approval timeline requirements.

## Mission
Analyze whether a flight application meets the advance notice requirement for regulatory approval.

## Flight Plan
- **Current time**: {current_time}
- **Application submitted**: {application_time}
- **Planned flight time**: {planned_flight_time}
- **Flight type**: {flight_type}
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Target altitude**: {end.altitude}m AGL
- **In controlled zone**: {'YES' if in_controlled_zone else 'NO'}

## Timeline Requirements
- **Required advance notice**: {required_advance_hours} hours (提前36小时申请)
- **Calculation**: Time difference = Planned flight time - Application time
- **Boundary check**: Use ≥ comparison ({required_advance_hours}h ≥ {required_advance_hours}h is compliant)

{restricted_text if restricted_text else ""}

## Regulations
### China 《条例》第26条:
- "飞行活动应当在拟飞行前1日12时前提出申请"
- Translation: Applications should be submitted before 12:00 noon, 1 day before intended flight
- **Interpretation**: Approximately 36 hours advance notice

### Exemptions (China 《条例》第31条):
1. **Emergency missions** (紧急任务):
   - Search and rescue, disaster relief, medical emergency
   - Exempted from timeline requirement
   - flight_type = 'emergency' → No advance notice required

2. **Uncontrolled airspace** (适飞空域):
   - Light drones flying < 120m altitude AND outside restricted areas
   - No approval required → Timeline check not applicable
   - Altitude < 120m AND in_controlled_zone = False → Exempt

### Decision Logic Priority (Highest to Lowest):
1. **Uncontrolled airspace exemption**: If altitude < 120m AND outside controlled zone → APPROVE (no approval needed)
2. **Emergency mission exemption**: If flight_type = 'emergency' → APPROVE (timeline waived)
3. **Timeline requirement check**: Time difference ≥ {required_advance_hours}h
4. **Approval requirement**: If in controlled zone OR altitude ≥ 120m → Timeline applies

## Your Task
**Analyze timeline compliance step-by-step:**

1. **Exemption checks** (Check these FIRST):
   - Is altitude < 120m AND outside controlled zone? → Uncontrolled airspace exemption (APPROVE)
   - Is flight_type = 'emergency'? → Emergency exemption (APPROVE)
   - If any exemption applies → Skip timeline check

2. **Parse ISO 8601 timestamps**:
   - Application time: {application_time}
   - Planned flight time: {planned_flight_time}
   - Format: YYYY-MM-DDTHH:MM:SSZ

3. **Calculate time difference**:
   - Difference (hours) = (Planned flight time - Application time) in hours
   - Example: 2024-10-21T15:00:00Z - 2024-10-21T09:00:00Z = 6 hours

4. **Check timeline requirement**:
   - Is time difference ≥ {required_advance_hours} hours?
   - Use ≥ comparison (36.0h ≥ 36.0h is compliant, boundary inclusive)

5. **Check zone requirement**:
   - Is target in controlled zone OR altitude ≥ 120m?
   - Calculate 2D distance to restricted zone centers
   - If distance ≤ radius → Inside controlled zone

6. **Make final decision**: 
   - APPROVE: Exemption applies OR timeline requirement met
   - REJECT: Timeline requirement not met (and no exemption)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of timeline analysis",
  "detailed_steps": [
    "Step 1: Exemption check...",
    "Step 2: Time parsing...",
    "Step 3: Time difference calculation...",
    "Step 4: Timeline requirement check...",
    "..."
  ],
  "timeline_analysis": {{
    "application_time": "{application_time}",
    "planned_flight_time": "{planned_flight_time}",
    "time_difference_hours": <number or null>,
    "required_hours": {required_advance_hours},
    "timeline_compliant": true or false,
    "flight_type": "{flight_type}",
    "emergency_exemption": true or false,
    "uncontrolled_airspace_exemption": true or false,
    "in_controlled_zone": {str(in_controlled_zone).lower()},
    "requires_approval": true or false
  }}
}}

## Important Notes
- Time difference uses ≥ comparison (36.0h ≥ 36.0h is OK, boundary inclusive)
- ISO 8601 format: Parse carefully (2024-10-21T15:00:00Z)
- Exemption priority: Uncontrolled airspace > Emergency > Timeline check
- Light drones in uncontrolled airspace (< 120m, outside restricted areas) are exempt
- Emergency missions waive timeline requirements
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""