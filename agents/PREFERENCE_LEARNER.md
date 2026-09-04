# Preference Learner Contract

## Objective

Use explicit user feedback to improve ranking without overfitting to isolated reactions.

## Feedback events

Supported primary actions:
- LIKE
- REJECT
- SHORTLIST
- APPLY
- INTERVIEW
- OFFER

Optional reasons:
- too_senior
- too_junior
- consulting
- company
- domain
- compensation
- location
- technology
- role_content
- language
- visa
- other

## Principle

Explicit reason > inferred reason.

## Initial implementation

Milestone 1 should NOT use an ML model.

Use transparent weighted preference signals based on:
- role family
- technologies
- domain
- company type
- work model
- seniority
- location
- consulting vs product

Store raw feedback separately from derived preference weights.

## Later implementation

After sufficient observations, evaluate:
- logistic regression
- pairwise preference learning
- learning-to-rank

Do not add ML unless offline evaluation shows improvement over the deterministic baseline.
