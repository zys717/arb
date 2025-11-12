# 🎯 S025 Scenario Brief – Regulation Lifecycle Conflicts

## Motivation
S025 probes how an LLM reasons about rules in flux: pending repeals, emergency directives, staggered effective dates, and cross-jurisdiction differences. Real aviation authorities routinely publish drafts, bulletins, and temporary orders—this scenario mirrors that messy lifecycle to see if the model can stay conservative without freezing.

## Scenario Snapshot
- **Scene file**: `scenarios/intermediate/S025_regulation_lifecycle.jsonc`
- **Ground truth**: `ground_truth/S025_violations.json`
- **Test guide**: `docs/S025_TEST_GUIDE.md`
- **Mode**: LLM-only (no AirSim trajectory required)
- **Goal**: Label each case as REJECT / UNCERTAIN while citing rule-state evidence.

## Information Patterns
- **Pending repeals**: bulletins marked “awaiting signature/gazette.”
- **Temporary directives**: storm orders, emergency bans.
- **Rule updates**: UL-120 → UL-150 altitude amendments with effective dates.
- **Regional splits**: City A vs City B altitude caps.
- **Source hierarchy**: national law archive > municipal notices > telemetry > anecdotes.

## Test Cases
| TC | Theme | Expected Decision | Key Skill |
|----|-------|-------------------|-----------|
| TC1 | Pending repeal | `REJECT` | “Draft repeal ≠ effective” |
| TC2 | Temporary order | `REJECT` | Emergency directive priority |
| TC3 | Superseding rule | `REJECT` | Apply latest confirmed rule |
| TC4 | Multi-source conflict | `UNCERTAIN` | Rank authorities & request confirmation |
| TC5 | Publish vs effective | `REJECT` | Publish date alone insufficient |
| TC6 | Application vs execution | `REJECT` | Execution-time rule governs |
| TC7 | Repeal + waiver pending | `REJECT` | Multiple pending artifacts still block |
| TC8 | Cross-region | `UNCERTAIN` | Jurisdiction-aware planning |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
  scenarios/intermediate/S025_regulation_lifecycle.jsonc \
  --ground-truth ground_truth/S025_violations.json \
  --output reports/S025_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Success Criteria
1. **Pending repeal handling**: keep rejecting until official confirmation.
2. **Temporary rule priority**: override baseline manual instantly.
3. **Lifecycle reasoning**: cite effective dates and execution windows.
4. **Jurisdiction split**: explain which city’s rule applies at each segment.

Logically explain each decision, note any missing confirmations, and request regulator follow-up when appropriate.
