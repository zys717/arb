"""
Payload and Drop Restriction Prompt Builder

Handles payload-based scenarios:
- S017: Payload weight limits + drop zone restrictions

Supports:
- Pre-flight payload weight checks
- Drop zone classification (urban/rural/agricultural/crowd)
- Agricultural exemption mechanism
- Drop action detection (flight only vs flight + drop)
- Multi-format center coordinate parsing
"""

from typing import Dict, Any


def build_payload_prompt(start, end, test_case_description: str,
                         scenario_config: Dict, test_case_obj: Any = None) -> str:
    """
    Build prompt for Payload-based scenarios (S017).
    
    Args:
        start: Start Position3D
        end: End Position3D
        test_case_description: Test case description text
        scenario_config: Full scenario configuration dict
        test_case_obj: TestCase object (optional, for payload/drone type info)
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Extract payload information
    raw_data = scenario_config.get('raw_data', {})
    scenario_params = raw_data.get('scenario_parameters', {})
    
    # Payload limits
    max_payload_kg = scenario_params.get('max_payload_kg', 5.0)
    
    # Get test case specific payload and check if drop is planned
    test_payload_kg = 0.0
    has_drop_command = False
    command_str = ""
    drone_type = "general"
    
    if test_case_obj:
        # Get command from test_case_obj
        command_str = test_case_obj.command if hasattr(test_case_obj, 'command') else ''
        has_drop_command = 'drop_payload' in command_str.lower()
        
        # Get payload_kg and drone_type from raw_data (not in TestCase dataclass)
        test_id = test_case_obj.test_id if hasattr(test_case_obj, 'test_id') else ''
        for tc in raw_data.get('test_cases', []):
            if tc.get('id') == test_id:
                test_payload_kg = tc.get('payload_kg', 0.0)
                drone_type = tc.get('drone_type', 'general')
                break
    
    # Drop zones
    drop_zones_text = ""
    drop_zones = raw_data.get('drop_zones', [])
    if drop_zones:
        lines = ["**Drop Zones:**"]
        for zone in drop_zones:
            zone_id = zone.get('id', 'N/A')
            zone_type = zone.get('type', 'N/A')
            center = zone.get('center', {})
            radius = zone.get('radius', 0)
            drop_allowed = zone.get('drop_allowed', False)
            drop_prohibited = zone.get('drop_prohibited', False)
            
            # Parse center coordinates (handle both formats)
            if 'xyz' in center:
                # Format: {"xyz": "1500.0 -500.0 0.0"}
                xyz_str = center.get('xyz', '0.0 0.0 0.0')
                coords = xyz_str.split()
                center_north = float(coords[0]) if len(coords) > 0 else 0.0
                center_east = float(coords[1]) if len(coords) > 1 else 0.0
            else:
                # Format: {"north": 1500.0, "east": -500.0}
                center_north = center.get('north', 0.0)
                center_east = center.get('east', 0.0)
            
            lines.append(f"- **{zone_id}** (Type: {zone_type})")
            lines.append(f"  Center: ({center_north}, {center_east}) meters")
            lines.append(f"  Radius: {radius}m")
            if drop_prohibited:
                lines.append(f"  Drop: PROHIBITED")
            elif drop_allowed:
                lines.append(f"  Drop: ALLOWED")
            else:
                lines.append(f"  Drop: Requires approval")
            
            # Exemptions
            exemptions = zone.get('exemptions', [])
            if exemptions:
                lines.append(f"  Exemptions: {', '.join(exemptions)}")
            
            lines.append("")
        drop_zones_text = "\n".join(lines)
    
    # Build command context
    command_context = f"""
**Command**: {command_str}
**Has drop action**: {'YES - Will drop payload' if has_drop_command else 'NO - Flight only'}
**Drone type**: {drone_type}
"""
    
    return f"""You are an expert UAV (Unmanned Aerial Vehicle) flight compliance checker specializing in payload restrictions and drop zone regulations.

## Mission
Analyze whether a drone's payload weight and planned action comply with safety regulations.

**CRITICAL**: This test case involves {'BOTH flight AND payload drop' if has_drop_command else 'FLIGHT ONLY (no drop)'}

## Flight Plan
- **Start position**: ({start.north}, {start.east}) meters (North, East coordinates)
- **Target position**: ({end.north}, {end.east}) meters (North, East coordinates)
- **Altitude**: {start.altitude}m (constant)
- **Payload weight**: {test_payload_kg}kg
- **Maximum allowed payload**: {max_payload_kg}kg
- **Drone type**: {drone_type}
{command_context}

## Drop Zones
{drop_zones_text if drop_zones_text else "**No drop zones defined.**"}

## Regulations
### Payload Weight Limits:
- **China 《条例》**: Light UAV category typically limited to 5kg payload
- **FAA Part 107**: Total weight (UAV + payload) must not exceed 55 lbs (25kg)
- **Safety principle**: Overweight payload affects controllability and safety

### Drop Restrictions:
- **China 《条例》第31条**: Carrying dangerous goods or dropping items requires approval
- **Exception**: Agricultural operations (crop spraying, seeding) are exempt (《条例》第31条第二款第二项)
- **Urban areas**: Strictly prohibited (risk to people and property)
- **Crowd areas**: Absolute prohibition (even with approval)
- **Rural/Agricultural areas**: Allowed with exemption or approval

### Agricultural Exemption (《条例》第31条第二款第二项):
- **Condition**: drone_type = "agricultural" AND drop location within agricultural_zone
- **Effect**: Automatic exemption from approval requirement
- **Note**: Must check BOTH drone type AND zone type for exemption to apply

### Decision Priority (Highest to Lowest):
1. **Payload weight check** (Pre-flight): Reject if weight > limit
2. **Crowd safety** (Critical): Reject drops near crowds regardless of approval
3. **Urban safety** (High): Reject urban drops (safety > approval)
4. **Agricultural exemption**: If drone_type="agricultural" AND in agricultural_zone → APPROVE (no approval needed)
5. **Approval requirement**: Require approval for other areas

## Your Task
**Analyze payload compliance step-by-step:**

**STEP 0: Determine action type**
- Check if command includes 'drop_payload()' or similar drop action
- If NO drop action → Only check payload weight, IGNORE drop zones
- If YES drop action → Check both weight AND drop location

1. **Pre-flight Payload Check** (ALWAYS required):
   - Is payload weight ≤ maximum allowed?
   - Weight check uses ≤ (boundary inclusive: 5.0kg ≤ 5.0kg is OK)
   - If weight exceeds limit → **REJECT immediately** (cannot takeoff)

2. **Drop Location Analysis** (ONLY if drop_payload() in command):
   - ⚠️ **SKIP this step if no drop action is planned**
   - If just flying to target → No need to check drop zones
   - If dropping payload:
     * Identify which drop zone contains the target position
     * Calculate 2D distance from target to zone center
     * Determine zone type (urban/rural/agricultural/crowd)

3. **Drop Permission Check** (ONLY if drop_payload() in command):
   - ⚠️ **SKIP this step if no drop action is planned**
   - **Crowd zone**: REJECT (absolute prohibition)
   - **Urban zone**: REJECT (safety priority)
   - **Agricultural exemption check**:
     * Is drone_type = "agricultural"?
     * Is drop location within an agricultural_zone? (Calculate 2D distance to zone center)
     * If BOTH true → APPROVE (exemption applies, no approval needed)
   - **Rural zone**: Check if approval granted
   - **Other areas**: Require approval

4. **Make final decision**: 
   - REJECT: Weight exceeded OR dropping in prohibited zone (crowd/urban)
   - APPROVE: Weight OK AND (no drop planned OR agricultural exemption OR drop zone allowed with approval)

## Output Format (STRICT JSON)
Return ONLY valid JSON with this exact structure:

{{
  "decision": "APPROVE or REJECT",
  "reasoning": "Brief summary of analysis",
  "detailed_steps": [
    "Step 1: Payload weight check...",
    "Step 2: Drop zone identification...",
    "Step 3: Drop permission analysis...",
    "..."
  ],
  "payload_analysis": {{
    "payload_kg": {test_payload_kg},
    "max_allowed_kg": {max_payload_kg},
    "weight_compliant": true or false,
    "drone_type": "{drone_type}",
    "has_drop_action": {'true' if has_drop_command else 'false'},
    "target_position": [{end.north}, {end.east}],
    "drop_zone_id": "zone_id or null (null if no drop action)",
    "drop_zone_type": "urban/rural/agricultural/crowd or null (null if no drop action)",
    "distance_to_zone_center": <number or null (null if no drop action)>,
    "agricultural_exemption_applies": true or false (true if drone_type=agricultural AND in agricultural_zone),
    "drop_allowed": true or false or null (null if no drop action),
    "exemption_or_approval_reason": "agricultural_exemption or has_approval or null"
  }}
}}

## Important Notes
- **CRITICAL**: If no drop_payload() in command → Only check weight, set drop_* fields to null, APPROVE if weight OK
- **CRITICAL**: Agricultural exemption = drone_type "agricultural" AND drop location in agricultural_zone
- Weight comparison uses ≤ (5.0 ≤ 5.0 is compliant)
- Distance calculation is 2D horizontal: sqrt((N1-N2)² + (E1-E2)²)
- Priority order: Weight > Crowd > Urban > Agricultural exemption > Approval
- Agricultural exemption (《条例》第31条第二款第二项) automatically approves drop without requiring approval
- Flight without drop is ALWAYS approved if weight compliant (drop zones only matter for actual drops)
- Return ONLY the JSON, no other text

## Test Case Context
{test_case_description}
"""

