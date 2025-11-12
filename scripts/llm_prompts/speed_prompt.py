"""
Speed Limit Prompt Builder

Handles speed-based scenarios:
- S009: Global speed limit (100 km/h)
- S010: Zone-based speed restrictions

Supports:
- Zone-specific speed limits
- Speed calculation from flight parameters
"""

import math
from typing import Dict


def build_speed_prompt(start, end, test_case_description: str, 
                       scenario_config: Dict) -> str:
    """
    Build prompt for Speed-based scenarios (S009-S010).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract speed limit zones if available
    speed_zones_text = "**No specific speed zones defined.**"
    if 'speed_limit_zones' in scenario_config:
        zones = scenario_config['speed_limit_zones']
        lines = []
        for zone in zones:
            lines.append(f"- Zone: {zone.get('zone_id', 'N/A')}")
            lines.append(f"  Center: ({zone.get('center_north')}, {zone.get('center_east')}) meters")
            lines.append(f"  Radius: {zone.get('radius')}m")
            lines.append(f"  Speed limit: {zone.get('speed_limit')} m/s")
            lines.append("")
        speed_zones_text = "\n".join(lines)
    
    # Calculate flight distance
    distance = math.sqrt((end.north - start.north)**2 + (end.east - start.east)**2)
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in motion constraints and speed regulations.

## Mission
Analyze whether a drone's flight violates speed limit regulations.

## Flight Plan
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Flight distance**: {distance:.2f} meters (straight-line)
- **Altitude**: {start.altitude}m (constant)

## Speed Limit Zones
{speed_zones_text}

## Regulations
- FAA Part 107: Maximum groundspeed of 100 mph (44.7 m/s) for all operations
- EASA: Typical speed restrictions in urban areas: 15-20 m/s
- Zone-specific limits may apply based on location (residential, school, hospital, etc.)

## Your Task
**Analyze the flight speed compliance step-by-step:**

1. **Calculate flight parameters**:
   - Estimated flight time (if provided in test case)
   - Calculate average speed: distance / time (m/s)
   
2. **Determine applicable speed limits**:
   - Check if drone enters any speed-restricted zones
   - Identify the strictest applicable limit
   
3. **Check compliance**:
   - Compare actual/planned speed against limits
   - Determine if speed is within acceptable range
   
4. **Make final decision**: APPROVE (compliant) or REJECT (violation)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of speed analysis",
  "detailed_steps": [
    "Step 1: Flight parameters...",
    "Step 2: Speed limit analysis...",
    "..."
  ],
  "speed_analysis": {{
    "flight_distance_m": <number>,
    "estimated_time_s": <number or null>,
    "calculated_speed_ms": <number or null>,
    "applicable_speed_limit_ms": <number>,
    "violation": true or false
  }}
}}

## Important Notes
- Speed limits are in meters per second (m/s)
- 1 m/s ≈ 3.6 km/h ≈ 2.24 mph
- If flight enters multiple zones, the STRICTEST limit applies
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

