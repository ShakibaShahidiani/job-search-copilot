# Initial Data Model

Milestone 1 requires four core entities.

## Job

Fields:
- id
- company
- title
- location
- work_model
- source_url
- direct_application_url
- posted_date
- discovered_at
- description
- required_skills
- preferred_skills
- experience_requirement
- language_requirements
- employment_type
- status

## MatchScore

Fields:
- id
- job_id
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
- final_score
- rationale
- blockers
- created_at

## Feedback

Fields:
- id
- job_id
- action
- reason
- free_text
- created_at

Actions:
- LIKE
- REJECT
- SHORTLIST
- APPLY
- INTERVIEW
- OFFER

## PreferenceSignal

Fields:
- id
- feature_type
- feature_value
- weight
- evidence_count
- confidence
- updated_at

Examples:
- domain | healthcare | +0.3
- company_type | consultancy | -0.4
- technology | agentic_ai | +0.5

## Important data rule

Raw feedback is immutable history.

Derived preference signals can be recalculated from raw feedback.
