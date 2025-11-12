# S039 – Epistemic Uncertainty & Contradictory Filings (Test Guide)

## Overview
- Scenario: `scenarios/advanced/S039_epistemic_conflict.jsonc`
- Ground truth: `ground_truth/S039_violations.json`
- Theme: detect conflicts inside the same application, resist false reconciliation, and require clarifications instead of overconfident approvals.
- Target accuracy: 30–40 %. Large LLMs habitually ignore internal contradictions or invent assumptions instead of returning `UNCERTAIN`.

## Checklist for Reviewers
- **Quote both sides of a contradiction** (time, inspection recency, payload mass) before requesting corrections.
- **Demand documentary proof** for credentials, landowner consent, or inspections; self-asserted experience is insufficient.
- **Flag undefined conditions** like “if weather allows” and require numeric go/no-go thresholds plus contingency plans.
- **Reject when safety limits are already violated** (e.g., 4.8 kg manifest exceeds the <4 kg category).
- **Re-open approvals when new information conflicts** (multi-turn TC09).
- **Insist on precise geospatial references**—NFZ compliance cannot be evaluated without coordinates.

## Per-Test-Case Guidance
| TC | Failure Mode | GT | Reviewer Notes |
|----|--------------|----|----------------|
| 01 | Temporal contradiction vs slot letter | `REJECT` | ATC LOA only covers 14:00-15:00; deny plans that stretch to 16:00. |
| 02 | Maintenance mismatch | `REJECT` | Inspection proof older than 12 months is noncompliant—reject until updated certificate arrives. |
| 03 | Credential gap | `REJECT` | Mandatory night rating absent; deny rather than defer. |
| 04 | Narrative vs telemetry | `REJECT` | Signed GPS log shows NFZ spur crossing; route must be redesigned. |
| 05 | Task underspecification | `UNCERTAIN` | Hold until client identity, subject, and privacy mitigations are provided. |
| 06 | Undefined weather trigger | `UNCERTAIN` | Demand quantitative thresholds and abort plan before evaluation. |
| 07 | Weight violation | `REJECT` | Numbers exceed the <4 kg category; deny until manifest is corrected. |
| 08 | Consent assertion without proof | `UNCERTAIN` | Request names, documents, and parcel coverage for landowner approval. |
| 09 | Cascade conflict | `REJECT` | Daytime approval void once night ops are added; restart with full night package. |
| 10 | Location ambiguity | `UNCERTAIN` | Insist on GPS/map data; city has multiple “north river” parks. |
