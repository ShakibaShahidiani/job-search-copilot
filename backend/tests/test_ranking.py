from app.models.enums import FeatureType, FeedbackAction, RejectReason
from app.models.feedback import Feedback
from app.models.job import Job
from app.models.preference_signal import PreferenceSignal
from app.services.preference_learner import recalculate_all
from app.services.ranking import rank_jobs
from tests.conftest import job_id_for


def test_blocked_job_always_ranks_last(seeded_db):
    ranked = rank_jobs(seeded_db)
    fortress_id = job_id_for("Fortress Dynamics")

    assert ranked[-1].job.id == fortress_id
    assert ranked[-1].has_blocker is True


def test_blocked_job_ranks_last_even_with_an_inflated_base_score(seeded_db):
    """The hard-constraint sort must not depend on the blocked job simply
    having the lowest raw score -- it must sink even if its base score is
    artificially made the highest of all jobs."""
    fortress_id = job_id_for("Fortress Dynamics")
    fortress = seeded_db.get(Job, fortress_id)
    fortress.match_score.final_score = 9.99
    seeded_db.commit()

    ranked = rank_jobs(seeded_db)
    assert ranked[-1].job.id == fortress_id


def test_ranking_changes_after_feedback(seeded_db):
    before = {r.job.id: r.final_score for r in rank_jobs(seeded_db)}

    # Repeatedly reject "general_ai" domain roles specifically for their
    # domain -> the general_ai domain signal should turn negative and pull
    # those jobs' rankings down.
    for company in ["Northwind Cognition", "Aether Labs", "Orion Applied AI"]:
        seeded_db.add(
            Feedback(
                job_id=job_id_for(company),
                action=FeedbackAction.REJECT,
                reason=RejectReason.DOMAIN,
            )
        )
    seeded_db.commit()
    recalculate_all(seeded_db)

    after = {r.job.id: r.final_score for r in rank_jobs(seeded_db)}

    # The explicitly domain-rejected jobs must have dropped.
    northwind_id = job_id_for("Northwind Cognition")
    assert after[northwind_id] < before[northwind_id]

    # "biomedical" domain was never touched by any feedback event.
    biomedical_signal = (
        seeded_db.query(PreferenceSignal)
        .filter(
            PreferenceSignal.feature_type == FeatureType.DOMAIN,
            PreferenceSignal.feature_value == "biomedical",
        )
        .one_or_none()
    )
    assert biomedical_signal is None

    # Biomedical jobs may still move slightly from shared, weakly-inferred
    # features (e.g. both use Python), but strictly less than a job that
    # was explicitly, repeatedly rejected for its domain.
    northwind_drop = before[northwind_id] - after[northwind_id]
    veridian_id = job_id_for("Veridian Health AI")
    veridian_drop = before[veridian_id] - after[veridian_id]
    assert veridian_drop < northwind_drop


def test_single_feedback_event_does_not_drastically_reorder_rankings(seeded_db):
    before = {r.job.id: r.final_score for r in rank_jobs(seeded_db)}

    seeded_db.add(
        Feedback(job_id=job_id_for("Northwind Cognition"), action=FeedbackAction.REJECT)
    )
    seeded_db.commit()
    recalculate_all(seeded_db)

    after = {r.job.id: r.final_score for r in rank_jobs(seeded_db)}

    for job_id, before_score in before.items():
        assert abs(after[job_id] - before_score) <= 1.0


def test_preference_explanation_is_present_and_explains_score_movement(seeded_db):
    job_id = job_id_for("Deltaworks Consulting")
    seeded_db.add(
        Feedback(job_id=job_id, action=FeedbackAction.REJECT, reason=RejectReason.CONSULTING)
    )
    seeded_db.commit()
    recalculate_all(seeded_db)

    ranked = rank_jobs(seeded_db)
    target = next(r for r in ranked if r.job.id == job_id)

    assert target.preference_adjustment < 0
    assert any("consultancy" in line for line in target.preference_explanation)
