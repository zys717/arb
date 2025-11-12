"""
NFZ (No-Fly Zone) Prompt Builder

Handles NFZ-based scenarios including:
- S001-S008: Basic geofence and spatial restrictions
- S015: Dynamic NFZ avoidance (Pre-flight)
- S016: Real-time obstacle avoidance (In-flight)

Supports:
- Time-dependent TFRs (Temporary Flight Restrictions)
- Multi-tier action levels (BLOCK vs WARNING)
- Real-time obstacle avoidance decision logic
"""

from typing import List, Dict, Any
from .base_prompt import format_nfzs_for_llm


def build_nfz_prompt(start, end, nfzs: List, 
                     test_case_description: str, scenario_config: Dict, test_case_obj: Any = None) -> str:
    """
    Build prompt for NFZ-based scenarios (S001-S008, S015-S016), with time-aware TFR support.
    
    Args:
        start: Start Position3D
        end: End Position3D
        nfzs: List of NFZConfig objects
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        test_case_obj: TestCase object (optional, for additional context)
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Detect if this is a real-time obstacle avoidance scenario (S016)
    scenario_id = scenario_config.get('scenario_id', '')
    is_realtime_obstacle = 'S016' in scenario_id.upper() or 'OBSTACLE' in scenario_id.upper()
    
    # Extract time information if available (for S005 dynamic TFR)
    simulated_time = None
    time_context = ""
    if test_case_obj:
        simulated_time = getattr(test_case_obj, 'simulated_time', None) or test_case_obj.__dict__.get('simulated_time')
    
    # If we have simulated time, build time-aware NFZ list
    if simulated_time:
        time_context = f"\n## Current Simulation Time\n**{simulated_time}**\n"
        nfz_text = "**Time-Dependent No-Fly Zones (TFRs):**\n\n"
        if not nfzs:
            nfz_text += "No No-Fly Zones defined.\n"
        else:
            for i, nfz in enumerate(nfzs, 1):
                nfz_text += f"{i}. NFZ: {nfz.nfz_id}\n"
                nfz_text += f"   - Center: ({nfz.center_north}, {nfz.center_east}) meters\n"
                nfz_text += f"   - Total restricted radius: {nfz.total_radius}m\n"
                # Add time window info if available
                raw_data = scenario_config.get('raw_data', {})
                for gf in raw_data.get('geofences', []):
                    if gf.get('id') == nfz.nfz_id:
                        # Check for time restriction (can be nested or flat)
                        time_restriction = gf.get('time_restriction', {})
                        active_start = time_restriction.get('active_start') or gf.get('active_start')
                        active_end = time_restriction.get('active_end') or gf.get('active_end')
                        
                        if active_start and active_end:
                            nfz_text += f"   - **Active period**: {active_start} to {active_end}\n"
                            nfz_text += f"   - **Type**: Temporary Flight Restriction (TFR)\n"
                        break
                nfz_text += "\n"
    else:
        nfz_text = format_nfzs_for_llm(nfzs)
    
    # Build time-aware instructions
    time_instructions = ""
    if simulated_time:
        time_instructions = """
**⚠️ IMPORTANT: Time-Dependent Restrictions**
- Some NFZs are Temporary Flight Restrictions (TFRs) that are only active during specific time windows
- **You MUST check if the current simulation time falls within each TFR's active period**
- Only enforce spatial restrictions for TFRs that are CURRENTLY ACTIVE
- TFRs outside their active period should be IGNORED (treat as if they don't exist)
"""
    
    # Build obstacle avoidance instructions for S016
    obstacle_instructions = ""
    if is_realtime_obstacle:
        obstacle_instructions = """
**⚠️ SPECIAL: Real-time Obstacle Avoidance Scenario (S016)**
This is an IN-FLIGHT detection scenario, not pre-flight planning. The obstacles are detected during flight.

- **WARNING-level obstacles**: These represent physical obstacles (buildings, towers, cranes)
- **Action level 'warn'**: Means the system should STOP before reaching the obstacle (NOT "flight allowed")
- **Decision logic for obstacles**:
  * If path will approach within the obstacle's total restricted radius → **APPROVE_WITH_STOP**
  * If path stays clear of all obstacles → **APPROVE**
  
**CRITICAL**: For WARNING-level obstacles in S016:
- Do NOT interpret 'warn' as "flight allowed with notification"
- If minimum distance < total restricted radius → Use **APPROVE_WITH_STOP** (not REJECT)
- The drone should stop BEFORE entering the obstacle zone, not be rejected entirely
"""
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker with strong spatial reasoning and mathematical skills.

## Mission
Analyze whether a drone's planned flight path will conflict with any No-Fly Zones (NFZs).
{time_context}
## Flight Path
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Flight path**: STRAIGHT LINE from start to target
- **Altitude**: {start.altitude}m (constant throughout flight)

⚠️ **IMPORTANT - Distance Calculation**:
- The system uses **3D Euclidean distance** that includes altitude
- Distance to NFZ center = √((north_diff)² + (east_diff)² + (altitude_diff)²)
- For a target at ({end.north}, {end.east}, {start.altitude}) and NFZ center at (center_north, center_east, 0):
  * 3D distance = √((target_north - center_north)² + (target_east - center_east)² + altitude²)
- **You MUST use 3D distance when comparing against NFZ restricted radius**

## No-Fly Zones (NFZs)
{nfz_text}
{time_instructions}
{obstacle_instructions}
## Regulations
- FAA Part 107 & EASA: Drones must follow airspace restrictions based on zone action level
- **NFZ Action Levels**:
  * **BLOCK** (absolute prohibition): Flight path must NOT enter these zones → **REJECT**
  * **WARNING** (context-dependent):
    - Pre-flight scenarios (S001-S015): Flight allowed with notification → **APPROVE**
    - In-flight obstacle avoidance (S016): Must stop before obstacle → **APPROVE_WITH_STOP**
- For BLOCK-level NFZs: The drone's path must maintain at least the "Total restricted radius" distance from the NFZ center
- For WARNING-level NFZs in pre-flight: Entry is allowed but should be noted in the analysis
- For WARNING-level obstacles in S016: Drone must stop before entering the restricted radius
- If the minimum distance from the path to any BLOCK-level NFZ center is LESS than the "Total restricted radius", it's a CONFLICT
- **IMPORTANT**: For pre-flight planning, if the start position is already in a BLOCK-level NFZ, check if the TARGET can reach a safe location (this is allowed as an exit path)

## Your Task
**Analyze the flight path step-by-step:**

1. **Calculate path vector**: Describe the straight-line path from start to target
2. **Check TFR activation** (if time info provided): Determine which TFRs are active at the current simulation time
3. **Check NFZ action levels**: Separate NFZs into BLOCK-level (must avoid) and WARNING-level (allowed with notice)
4. **Check target position**: Is the TARGET position outside all BLOCK-level NFZs? (Primary check)
   - TARGET in WARNING zone is OK (note it, but don't reject)
   - TARGET in BLOCK zone → CONFLICT
5. **Check path safety** (secondary): Does the flight path pass through any BLOCK-level NFZs?
   - Path through WARNING zone is OK
   - If start is ALREADY in BLOCK-level NFZ but target is SAFE → This may be an exit path (context dependent)
   - If target is in BLOCK-level NFZ or path enters BLOCK-level NFZ from safe area → CONFLICT
6. **Make final decision**: 
   - If TARGET in BLOCK-level NFZ → **REJECT**
   - If S016 AND path approaches WARNING obstacle (distance < restricted radius) → **APPROVE_WITH_STOP**
   - If TARGET outside all BLOCK zones but inside WARNING zone (non-S016) → **APPROVE**
   - If TARGET is in safe area → **APPROVE**

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT or APPROVE_WITH_STOP",
  "reasoning": "Brief summary of your analysis",
  "detailed_steps": [
    "Step 1: Path analysis...",
    "Step 2: NFZ check...",
    "..."
  ],
  "nfz_analysis": [
    {{
      "nfz_id": "NFZ identifier",
      "min_distance_to_path": <number>,
      "required_clearance": <number>,
      "clearance_margin": <number (positive=safe, negative=conflict)>,
      "safe": true or false
    }}
  ]
}}

## Important Notes
- Be PRECISE with calculations
- Show your mathematical reasoning
- Consider 2D horizontal distance only (ignore altitude for now)
- A clearance margin < 0 means CONFLICT
- If NO NFZs are defined, return APPROVE with empty nfz_analysis array
- DO NOT assume or invent NFZ data that wasn't provided
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

