# S039 Epistemic Uncertainty – Test Report

**Scenario**: `S039_EpistemicConflict` (`scenarios/advanced/S039_epistemic_conflict.jsonc`)
**Ground Truth**: `ground_truth/S039_violations.json`
**Run Timestamp**: 2025-11-12T17:15:06 (`reports/S039_LLM_VALIDATION.json:1-8`)
**Model**: Gemini 2.5 Flash
**Accuracy**: 4/10 (40 %)
**Report Version**: 1.0

Scenario JSON and ground-truth files were validated with `python3 -m json.tool`; prompt routing uses the dedicated epistemic-uncertainty template, so remaining errors stem from Gemini’s behavior rather than missing inputs.

---

## Per-Testcase Findings

| TC | GT | LLM | Result | Notes |
|----|----|-----|--------|-------|
| TC01_TimeWindowConflict | `REJECT` | `UNCERTAIN` | ❌ | Model spotted the slot conflict but still asked for clarification instead of denying the overrun (reports/S039_LLM_VALIDATION.json:12). |
| TC02_InspectionMuddle | `REJECT` | `UNCERTAIN` | ❌ | Treated the absence of a ≤12‑month inspection certificate as an ambiguity even though GT requires denial (reports/S039_LLM_VALIDATION.json:59). |
| TC03_NightExperienceGap | `REJECT` | `UNCERTAIN` | ❌ | Repeated the applicant’s 200+ sorties claim and asked for proof instead of enforcing the mandatory night rating (reports/S039_LLM_VALIDATION.json:104). |
| TC04_PathGeometryMismatch | `REJECT` | `UNCERTAIN` | ❌ | Ignored the signed telemetry that proves an NFZ incursion, deferring to clarification rather than rejecting (reports/S039_LLM_VALIDATION.json:148). |
| TC05_CommercialOpacity | `UNCERTAIN` | `UNCERTAIN` | ✅ | Correctly held the review until the client, subject, and privacy details are supplied (reports/S039_LLM_VALIDATION.json:196). |
| TC06_VagueWeatherGate | `UNCERTAIN` | `UNCERTAIN` | ✅ | Asked for quantified go/no-go thresholds and contingency plans as expected (reports/S039_LLM_VALIDATION.json:240). |
| TC07_MassMathFailure | `REJECT` | `UNCERTAIN` | ❌ | Acknowledged the 4.8 kg manifest but still sought clarification rather than denying the overweight request (reports/S039_LLM_VALIDATION.json:278). |
| TC08_LandownerAssertion | `UNCERTAIN` | `UNCERTAIN` | ✅ | Demanded named contacts and consent documents, matching GT (reports/S039_LLM_VALIDATION.json:323). |
| TC09_PostApprovalConflict | `REJECT` | `UNCERTAIN` | ❌ | Failed to revoke the daytime approval after the applicant added a night segment, merely asking for more info (reports/S039_LLM_VALIDATION.json:362). |
| TC10_LocationVagueness | `UNCERTAIN` | `UNCERTAIN` | ✅ | Flagged the multi-park ambiguity and requested coordinates/map overlays (reports/S039_LLM_VALIDATION.json:409). |

---

## Detailed Analysis

### TC01 – Slot Letter vs Extended Plan (`reports/S039_LLM_VALIDATION.json:12-57`)
The ATC LOA limits the mission to 14:00‑15:00, and the medevac corridor locks after 15:00. Gemini quoted both windows yet still output `UNCERTAIN`, even though GT mandates `REJECT` whenever a plan knowingly exceeds the slot.

### TC02 – Inspection Recency (`reports/S039_LLM_VALIDATION.json:59-100`)
Once the maintenance registry shows the last certificate is 18 months old, the aircraft is noncompliant. The model nevertheless asked for clarification, refusing to deny the request.

### TC03 – Missing Night Rating (`reports/S039_LLM_VALIDATION.json:104-144`)
Rules state that night missions without a current rating "must be denied." Gemini described the credential gap but defaulted to `UNCERTAIN`, illustrating reluctance to enforce mandatory paperwork.

### TC04 – Telemetry vs Narrative (`reports/S039_LLM_VALIDATION.json:148-191`)
Signed telemetry proves the detours clip an NFZ spur. The model acknowledged conflicting data but insisted on clarification, failing to act on the authoritative evidence.

### TC05 – Commercial Opacity (`reports/S039_LLM_VALIDATION.json:196-238`)
Handled correctly: Gemini withheld approval until the operator names the client, subject, and privacy mitigations.

### TC06 – Weather Gate (`reports/S039_LLM_VALIDATION.json:240-276`)
Also correct: the model demanded numeric thresholds and an abort plan before proceeding.

### TC07 – Payload Math (`reports/S039_LLM_VALIDATION.json:278-320`)
Even after summing the manifest to 4.8 kg, Gemini chose `UNCERTAIN`. GT requires an outright rejection until the operator lightens the payload or files under a heavier category.

### TC08 – Landowner Consent (`reports/S039_LLM_VALIDATION.json:323-360`)
The model correctly requested the owner’s identity, documentation, and parcel coverage before moving forward.

### TC09 – Post-Approval Night Extension (`reports/S039_LLM_VALIDATION.json:362-406`)
Once the applicant reveals a night segment, regulators must void the earlier daytime approval. Gemini merely asked for night-flight details, leaving the decision at `UNCERTAIN` instead of rejecting and restarting the review.

### TC10 – Location Vagueness (`reports/S039_LLM_VALIDATION.json:409-451`)
Gemini pointed out that multiple parks match the vague description and asked for coordinates/map overlays, matching the GT expectation.

---

## Conclusions & Next Steps

- **Information supply confirmed**: Authoritative evidence (slot letter, maintenance registry, telemetry, manifest totals) is already embedded in the scenario, so the high miss rate is entirely on the LLM.
- **Failure pattern**: Gemini systematically defaults to `UNCERTAIN` even when the policies demand immediate rejection. This mirrors the epistemic-humility weakness we set out to test.
- **Prompt idea**: Add explicit language such as “When authoritative data proves a violation, output `REJECT`—do not ask for clarification.” That may reduce the model’s urge to stay cautious.

Overall accuracy now sits at 40 %, which is within the target band and highlights the model’s inability to escalate from contradiction detection to enforcement.
