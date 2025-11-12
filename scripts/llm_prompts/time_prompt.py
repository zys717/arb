"""
Time-based Restriction Prompt Builder

Handles time-based scenarios:
- S011: Night flight requirements (lights + training)
- S012: Time-restricted zones (noise-sensitive areas)

Supports:
- Night flight equipment and training requirements
- Time-restricted zones with specific hours
- Civil twilight boundary definition
"""

from typing import Dict


def build_time_prompt(start, end, test_case_description: str,
                      scenario_config: Dict) -> str:
    """
    Build prompt for Time-based scenarios (S011-S012).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract time and time-restricted zones
    flight_time = scenario_config.get('time_of_day', 'N/A')
    
    time_zones_text = "**No time-restricted zones defined.**"
    if 'time_restricted_zones' in scenario_config:
        zones = scenario_config['time_restricted_zones']
        lines = []
        for zone in zones:
            lines.append(f"- Zone: {zone.get('zone_id', 'N/A')}")
            lines.append(f"  Center: ({zone.get('center_north')}, {zone.get('center_east')}) meters")
            lines.append(f"  Radius: {zone.get('radius')}m")
            lines.append(f"  Restricted hours: {zone.get('start_time')} - {zone.get('end_time')}")
            lines.append(f"  Reason: {zone.get('reason', 'N/A')}")
            lines.append("")
        time_zones_text = "\n".join(lines)
    
    # Night flight requirements
    night_req_text = "**No specific night flight equipment info provided.**"
    if 'night_flight_requirements' in scenario_config:
        reqs = scenario_config['night_flight_requirements']
        lines = ["**Night Flight Requirements:**"]
        if 'anti_collision_lights' in reqs:
            lines.append(f"- Anti-collision lights: {'ON' if reqs['anti_collision_lights'] else 'OFF'}")
        if 'pilot_night_training' in reqs:
            lines.append(f"- Pilot night training: {'COMPLETED' if reqs['pilot_night_training'] else 'NOT COMPLETED'}")
        night_req_text = "\n".join(lines)
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in time-based regulations and night flight rules.

## Mission
Analyze whether a drone's flight violates time-based restrictions or night flight regulations.

## Flight Plan
- **Flight time**: {flight_time}
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Altitude**: {start.altitude}m (constant)

## Time-Restricted Zones
{time_zones_text}

## Night Flight Equipment & Training
{night_req_text}

## Regulations
### Night Flight Definition (FAA Part 107.29 & EASA):
- **Night**: Between end of civil twilight and beginning of civil twilight
- **Typical times** (varies by location and season):
  - Evening civil twilight ends: ~18:30
  - Morning civil twilight begins: ~05:30
- **Night flight requirements**:
  1. Anti-collision lighting visible for 3 statute miles
  2. Pilot training for night operations (FAA: recurrent training recommended, EASA: specific night rating)

### Time-Restricted Zones:
- Certain areas (hospitals, schools, residential) may prohibit flights during specific hours
- Restrictions typically apply to noise-sensitive periods (22:00-06:00)

## Your Task
**Analyze the time-based compliance step-by-step:**

1. **Determine time category**:
   - Is it daytime (06:00-18:29)?
   - Is it nighttime (18:30-05:59)?
   - Is it a boundary case?
   
2. **Check night flight requirements** (if nighttime):
   - Are anti-collision lights ON?
   - Does pilot have night training?
   - Both required for night flight compliance
   
3. **Check time-restricted zones**:
   - Does flight path enter any time-restricted zones?
   - Is current time within restricted hours?
   
4. **Make final decision**: APPROVE (compliant) or REJECT (violation)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of time-based analysis",
  "detailed_steps": [
    "Step 1: Time category determination...",
    "Step 2: Night flight check (if applicable)...",
    "Step 3: Time-restricted zone check...",
    "..."
  ],
  "time_analysis": {{
    "flight_time": "{flight_time}",
    "is_nighttime": true or false,
    "night_equipment_compliant": true or false or null,
    "enters_time_restricted_zone": true or false,
    "time_restriction_violated": true or false
  }}
}}

## Important Notes
- Civil twilight boundary: typically 18:30 (evening) and 05:30 (morning)
- Night flight requires BOTH lights AND training
- Time-restricted zones are checked if path intersects zone geometry
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

