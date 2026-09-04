# Matching Agent Contract

## Objective

Estimate how worthwhile a role is for this candidate.

Do not perform naive keyword matching.

## Match dimensions

Score each dimension from 0 to 1:

- technical_fit
- demonstrated_evidence
- seniority_fit
- domain_fit
- infrastructure_fit
- location_fit
- language_fit
- career_direction_fit
- preference_fit
- freshness

## Initial deterministic weighting

Suggested initial weights:

- technical_fit: 0.22
- demonstrated_evidence: 0.18
- seniority_fit: 0.15
- career_direction_fit: 0.12
- preference_fit: 0.10
- infrastructure_fit: 0.08
- domain_fit: 0.06
- location_fit: 0.04
- language_fit: 0.03
- freshness: 0.02

Convert the weighted score to a 1–10 user-facing score.

## Evidence rule

Every claimed overlap must map to a verified item in `context/CANDIDATE.md`.

## Gap classification

Classify gaps as:

- LOW: easily bridgeable / nice-to-have
- MEDIUM: relevant missing tool or limited demonstrated experience
- HIGH: central requirement not supported by candidate evidence
- BLOCKER: hard incompatibility such as mandatory Dutch or extreme seniority mismatch

## Output

For each role return:
- fit_score
- top_matches
- gaps
- blocker_status
- concise rationale
- recommended_action:
  - APPLY
  - CONSIDER
  - SKIP
