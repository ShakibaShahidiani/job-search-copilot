import math

import pytest

from app.models.enums import Confidence, FeatureType, FeedbackAction, RejectReason
from app.models.feedback import Feedback
from app.models.preference_signal import PreferenceSignal
from app.services.preference_learner import BASE_STEP, recalculate_all
from tests.conftest import job_id_for


def _signal(db, feature_type, feature_value):
    return (
        db.query(PreferenceSignal)
        .filter(
            PreferenceSignal.feature_type == feature_type,
            PreferenceSignal.feature_value == feature_value,
        )
        .one_or_none()
    )


def test_recalculate_with_no_feedback_produces_no_signals(seeded_db):
    recalculate_all(seeded_db)
    assert seeded_db.query(PreferenceSignal).count() == 0


def test_single_like_creates_observation_level_signals(seeded_db):
    job_id = job_id_for("Northwind Cognition")
    seeded_db.add(Feedback(job_id=job_id, action=FeedbackAction.LIKE))
    seeded_db.commit()

    recalculate_all(seeded_db)

    role_signal = _signal(seeded_db, FeatureType.ROLE_FAMILY, "agentic_ai_engineer")
    assert role_signal is not None
    assert role_signal.evidence_count == 1
    assert role_signal.confidence == Confidence.OBSERVATION
    assert role_signal.weight == pytest.approx(BASE_STEP, abs=1e-6)


def test_explicit_reason_gets_stronger_targeted_weight_than_inferred(seeded_db):
    """consulting reason must move company_type more than the other,
    merely-inferred features from the same event (explicit > inferred)."""
    job_id = job_id_for("Deltaworks Consulting")  # company_type = consultancy
    seeded_db.add(
        Feedback(job_id=job_id, action=FeedbackAction.REJECT, reason=RejectReason.CONSULTING)
    )
    seeded_db.commit()

    recalculate_all(seeded_db)

    targeted = _signal(seeded_db, FeatureType.COMPANY_TYPE, "consultancy")
    inferred = _signal(seeded_db, FeatureType.DOMAIN, "general_ai")

    assert targeted is not None and inferred is not None
    assert abs(targeted.weight) > abs(inferred.weight)
    assert targeted.weight == pytest.approx(-2 * BASE_STEP, abs=1e-6)
    assert inferred.weight == pytest.approx(-BASE_STEP, abs=1e-6)


def test_reject_reasons_without_a_modeled_feature_fall_back_to_weak_update(seeded_db):
    """'company' and 'other' reasons aren't in REASON_FEATURE_MAP (they
    don't generalize), so they must behave like a reasonless reject."""
    job_id = job_id_for("Aether Labs")
    seeded_db.add(
        Feedback(job_id=job_id, action=FeedbackAction.REJECT, reason=RejectReason.COMPANY)
    )
    seeded_db.commit()

    recalculate_all(seeded_db)

    domain_signal = _signal(seeded_db, FeatureType.DOMAIN, "general_ai")
    assert domain_signal.weight == pytest.approx(-BASE_STEP, abs=1e-6)


def test_repeated_evidence_has_diminishing_marginal_effect(seeded_db):
    """A second LIKE touching the same feature should move its weight by
    less than the first, so no small number of clicks can swing rankings
    disproportionately."""
    job_a = job_id_for("Northwind Cognition")  # agentic_ai_engineer, general_ai
    job_b = job_id_for("Aether Labs")  # llm_engineer, general_ai (shares "general_ai" domain)

    seeded_db.add(Feedback(job_id=job_a, action=FeedbackAction.LIKE))
    seeded_db.commit()
    recalculate_all(seeded_db)
    domain_after_one = _signal(seeded_db, FeatureType.DOMAIN, "general_ai").weight

    seeded_db.add(Feedback(job_id=job_b, action=FeedbackAction.LIKE))
    seeded_db.commit()
    recalculate_all(seeded_db)
    domain_after_two = _signal(seeded_db, FeatureType.DOMAIN, "general_ai")

    second_step = domain_after_two.weight - domain_after_one
    first_step = domain_after_one
    assert domain_after_two.evidence_count == 2
    assert second_step < first_step
    assert second_step == pytest.approx(BASE_STEP / math.sqrt(2), abs=1e-4)


def test_confidence_thresholds_follow_evidence_count(seeded_db):
    job_id = job_id_for("Northwind Cognition")
    for _ in range(7):
        seeded_db.add(Feedback(job_id=job_id, action=FeedbackAction.LIKE))
    seeded_db.commit()

    recalculate_all(seeded_db)

    signal = _signal(seeded_db, FeatureType.ROLE_FAMILY, "agentic_ai_engineer")
    assert signal.evidence_count == 7
    assert signal.confidence == Confidence.STRONG


def test_recalculate_all_is_idempotent(seeded_db):
    job_id = job_id_for("Northwind Cognition")
    seeded_db.add(Feedback(job_id=job_id, action=FeedbackAction.LIKE))
    seeded_db.commit()

    recalculate_all(seeded_db)
    first_pass = {
        (s.feature_type, s.feature_value): s.weight
        for s in seeded_db.query(PreferenceSignal).all()
    }

    recalculate_all(seeded_db)
    second_pass = {
        (s.feature_type, s.feature_value): s.weight
        for s in seeded_db.query(PreferenceSignal).all()
    }

    assert first_pass == second_pass
