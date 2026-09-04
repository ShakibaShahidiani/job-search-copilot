# Job Match Evaluation Rubric

Use this rubric to evaluate whether ranking quality is improving.

## 1. Relevance

Does the role match one of the target role families?

Score:
- 0: unrelated
- 1: weak adjacency
- 2: relevant
- 3: highly relevant

## 2. Technical evidence

Can claimed matches be demonstrated from candidate evidence?

Score:
- 0: mostly unsupported
- 1: partially supported
- 2: strongly supported
- 3: direct project/professional evidence

## 3. Seniority realism

Score:
- 0: clearly unrealistic
- 1: major stretch
- 2: reasonable stretch
- 3: appropriate

## 4. Constraints

Score:
- 0: hard constraint violation
- 1: important uncertainty
- 2: acceptable
- 3: ideal

## 5. User preference

Score:
- 0: contradicts strong learned preferences
- 1: mixed
- 2: likely attractive
- 3: strongly aligned

## Failure conditions

Automatic failure:
- mandatory Dutch;
- job confirmed expired/closed;
- role unrelated to AI/ML target space;
- recommendation contains fabricated candidate evidence.

## Offline ranking metric ideas

Later evaluate:
- Precision@10
- Like rate@10
- Apply rate@10
- NDCG@10 using explicit feedback labels
- Duplicate rate
- Stale-role rate
- Blocker leakage rate
