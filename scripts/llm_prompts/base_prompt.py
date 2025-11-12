"""
Base utilities for LLM prompt building.

Provides common formatting functions used across different prompt builders.
"""

from typing import List, Any


def format_nfzs_for_llm(nfzs: List[Any]) -> str:
    """
    Format NFZs for LLM prompt.
    Handles empty NFZ lists gracefully.
    
    Args:
        nfzs: List of NFZConfig objects
        
    Returns:
        Formatted string describing all NFZs
    """
    if not nfzs:
        return "**No No-Fly Zones defined for this scenario.**\n(The airspace is clear of static NFZ restrictions. Focus on other regulations.)"
    
    lines = []
    for i, nfz in enumerate(nfzs, 1):
        lines.append(f"{i}. NFZ: {nfz.nfz_id}")
        lines.append(f"   - Type: {nfz.zone_type}")
        lines.append(f"   - Center: ({nfz.center_north}, {nfz.center_east}) meters (North, East)")
        lines.append(f"   - Physical radius: {nfz.radius}m")
        lines.append(f"   - Safety margin: {nfz.safety_margin}m")
        lines.append(f"   - Total restricted radius: {nfz.total_radius}m")
        # Add action information for tiered NFZ systems
        if nfz.action == "warn":
            lines.append(f"   - **Action level**: WARNING (flight allowed with notification)")
        else:
            lines.append(f"   - **Action level**: BLOCK (absolute prohibition)")
        lines.append(f"   - Description: {nfz.description}")
        lines.append("")
    return "\n".join(lines)

