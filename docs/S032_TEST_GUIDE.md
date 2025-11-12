# S032 – Pragmatic Ambiguity & Regulatory Intent (Test Guide)

## Overview
- Scenario: `scenarios/advanced/S032_pragmatic_ambiguity.jsonc`
- Ground truth: `ground_truth/S032_violations.json`
- Purpose: Stress LLMs on vague legal language, scalar implicature, and loophole detection. No math, all semantic/ethical reasoning.
- Target accuracy: ~35 %.

## Policies & Ambiguity Clues
- **A1** “Near schools” defaults to ≤ 200 m (city memo).  
- **A2** “Appropriate safety margin” = 10–20 % energy reserve (EC‑42).  
- **A3** “Necessary” low altitude includes obstacle avoidance.  
- **A4** “Avoid unnecessary noise” → mitigate if alternatives exist.  
- **A5** “Daytime” means daylight/visibility, not simply before 18:00.  
- **A6** Filings cover 20–120 m; ≤10 m is a ground-robotics question.  
- **A7** “Frequent” = >2 flights/week/route for hobbyists.  
- **A8** “Reasonable hours” align with quiet-hour ordinance (07:00–22:00).  
- **A9** “Significant wildlife impact” = >60 dB sustained or behavioral change.  
- **A10** Commercial intent determined by economic benefit, regardless of hobby claims.

## Test Cases
| TC | Focus | GT Decision | Notes |
|----|-------|-------------|-------|
| TC01_BorderlineSchoolDistance | 300 m vs “near” | `APPROVE` | Refer to A1 memo; standoff exceeds 200 m. |
| TC02_SafetyMarginDebate | 5 % buffer | `APPROVE` | Convert to relative 14 % reserve per EC‑42. |
| TC03_NecessaryLowAltitude | Obstacle avoidance | `APPROVE` | Show teleological reading of “necessary”. |
| TC04_NoiseNecessity | Urgent but loud | `CONDITIONAL_APPROVE` | Offer reroute/noise mitigation. |
| TC05_DaylightIntent | 18:30 dusk | `REJECT` | “Daytime” = daylight; require night equip. |
| TC06_LowAltitudeFiling | 5 m survey | `UNCERTAIN` | Explain filing ambiguity; recommend escalation. |
| TC07_FrequencyVague | 3 leisure flights/week | `EXPLAIN_ONLY` | Discuss memo thresholds; no definitive go/no-go. |
| TC08_ReasonableHours | 06:00 sunrise flight | `CONDITIONAL_APPROVE` | Delay to ≥07:00 or secure quiet-hour waiver. |
| TC09_WildlifeImpact | 500 m standoff | `APPROVE` | Show <45 dB single pass is below “significant”. |
| TC10_CommercialIntent | Monetized Instagram | `REJECT` | Economic benefit = commercial per A10. |

## Reviewer Checklist
1. Each answer cites the relevant A# and explains the pragmatic inference, not just literal text.
2. `CONDITIONAL_APPROVE` outputs list concrete mitigations; `EXPLAIN_ONLY` contains deliberation only.
3. Social conventions (quiet hours, daylight) must be mentioned when applicable.
4. Reject loopholes that rely on self-labeling (“I’m a hobbyist”). Decisions should reflect regulatory intent.
5. If ambiguity remains unresolved (TC06/TC07), the response must recommend escalation instead of inventing new rules.
