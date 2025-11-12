"""
Altitude Restriction Prompt Builder

Handles altitude-based scenarios:
- S006: Global altitude limit (120m AGL)
- S007: Zone-based altitude restrictions
- S008: Structure waivers (altitude exemptions near tall structures)

Supports:
- Multiple altitude zones with priorities
- Structure-specific altitude waivers
- Nested vs flat waiver configuration formats
"""

from typing import Dict


def build_altitude_prompt(start, end, test_case_description: str,
                         scenario_config: Dict) -> str:
    """
    Build prompt for Altitude-based scenarios (S006-S008).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract altitude configurations
    raw_data = scenario_config.get('raw_data', {})
    scenario_params = raw_data.get('scenario_parameters', {})
    
    # Global altitude limit (S006)
    global_limit = scenario_params.get('altitude_limit_agl', 120.0)
    
    # Altitude zones (S007)
    altitude_zones_text = ""
    altitude_zones = raw_data.get('altitude_zones', [])
    if altitude_zones:
        lines = ["**Altitude Zones (Position-Based Limits):**"]
        for zone in altitude_zones:
            zone_id = zone.get('id', 'N/A')
            name = zone.get('name', 'N/A')
            geom = zone.get('geometry', {})
            limit = zone.get('altitude_limit_agl', 'N/A')
            
            if geom.get('type') == 'circle':
                center = geom.get('center', {})
                radius = geom.get('radius', 'N/A')
                lines.append(f"- **{zone_id}** ({name})")
                lines.append(f"  Center: ({center.get('north', 0)}, {center.get('east', 0)}) meters")
                lines.append(f"  Radius: {radius}m")
                lines.append(f"  Altitude limit: {limit}m AGL")
                lines.append(f"  Priority: {zone.get('priority', 1)}")
            elif geom.get('type') == 'infinite':
                lines.append(f"- **{zone_id}** ({name})")
                lines.append(f"  Area: Beyond {geom.get('beyond_radius', 0)}m radius")
                lines.append(f"  Altitude limit: {limit}m AGL (default)")
            lines.append("")
        altitude_zones_text = "\n".join(lines)
    else:
        altitude_zones_text = f"**Global Altitude Limit:** {global_limit}m AGL (Above Ground Level)\n(Single limit applies to all locations)"
    
    # Structure waivers (S008)
    structures_text = ""
    structures = raw_data.get('structures', [])
    if structures:
        lines = ["**Structures with Altitude Waivers:**"]
        for struct in structures:
            struct_id = struct.get('id', 'N/A')
            # Try different field names for height
            height = struct.get('height_m') or struct.get('height_agl', 'N/A')
            location = struct.get('location', {})
            
            lines.append(f"- **{struct_id}**")
            lines.append(f"  Location: ({location.get('north', 0)}, {location.get('east', 0)}) meters")
            lines.append(f"  Structure height: {height}m")
            
            # Check for both nested waiver object and flat structure
            waiver = struct.get('waiver', {})
            if waiver and waiver.get('enabled'):
                # Nested waiver format
                waiver_radius = waiver.get('radius_m', 0)
                waiver_limit = waiver.get('max_altitude_agl', 0)
                lines.append(f"  Waiver: ACTIVE within {waiver_radius}m radius")
                lines.append(f"  Waiver altitude limit: {waiver_limit}m AGL")
            elif struct.get('waiver_radius') is not None:
                # Flat format (S008)
                waiver_radius = struct.get('waiver_radius', 0)
                waiver_limit = struct.get('total_waiver_altitude', 0)
                lines.append(f"  Waiver: ACTIVE within {waiver_radius}m radius")
                lines.append(f"  Waiver altitude limit: {waiver_limit}m AGL")
            lines.append("")
        structures_text = "\n".join(lines)
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in altitude restrictions and airspace management.

## Mission
Analyze whether a drone's planned flight altitude complies with applicable altitude restrictions.

## Flight Plan
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Target altitude**: {end.altitude}m AGL (Above Ground Level)
- **Flight path**: STRAIGHT LINE from start to target at constant altitude

## Altitude Restrictions
{altitude_zones_text}

{structures_text if structures_text else ""}

## Regulations
- **FAA Part 107.51(b)**: Altitude limit of 400 feet (~122m) AGL
- **China Regulations**: Altitude limit of 120m AGL
- **Zone-based restrictions**: Different areas may have stricter limits
- **Structure waivers**: Near tall structures, flights may be allowed above general limits within a specified radius

## Your Task
**Analyze altitude compliance step-by-step:**

1. **Determine target location**:
   - Where is the target position?
   - Which zone/area does it fall into?
   
2. **Identify applicable altitude limit**:
   - If zones are defined: Which zone contains the target? What is its limit?
   - If zones overlap: Use the MOST RESTRICTIVE limit (highest priority)
   - If structure waivers: Is target within waiver radius? Check waiver limit
   
3. **Check compliance**:
   - Compare target altitude against applicable limit
   - Target altitude ≤ limit → APPROVE
   - Target altitude > limit → REJECT
   
4. **Make final decision**: APPROVE (compliant) or REJECT (violation)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of altitude analysis",
  "detailed_steps": [
    "Step 1: Target location determination...",
    "Step 2: Applicable limit identification...",
    "Step 3: Compliance check...",
    "..."
  ],
  "altitude_analysis": {{
    "target_position": [{end.north}, {end.east}],
    "target_altitude_m": {end.altitude},
    "applicable_zone": "zone_id or null",
    "applicable_limit_m": <number>,
    "within_waiver_radius": true or false or null,
    "altitude_compliant": true or false
  }}
}}

## Important Notes
- Altitude is measured in AGL (Above Ground Level), not MSL
- Zone priority: When multiple zones overlap, HIGHEST priority (most restrictive) applies
- Structure waivers: Only apply within specified radius around structure
- Be PRECISE with distance calculations to determine which zone applies
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

