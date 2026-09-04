from app.models.enums import FeedbackAction, RejectReason
from app.models.feedback import Feedback
from tests.conftest import job_id_for


def test_feedback_is_persisted(seeded_db):
    job_id = job_id_for("Northwind Cognition")
    fb = Feedback(job_id=job_id, action=FeedbackAction.LIKE)
    seeded_db.add(fb)
    seeded_db.commit()

    stored = seeded_db.query(Feedback).filter(Feedback.job_id == job_id).all()
    assert len(stored) == 1
    assert stored[0].action == FeedbackAction.LIKE
    assert stored[0].id is not None
    assert stored[0].created_at is not None


def test_feedback_reject_with_reason_is_persisted(seeded_db):
    job_id = job_id_for("Deltaworks Consulting")
    fb = Feedback(job_id=job_id, action=FeedbackAction.REJECT, reason=RejectReason.CONSULTING)
    seeded_db.add(fb)
    seeded_db.commit()

    stored = seeded_db.query(Feedback).filter(Feedback.job_id == job_id).one()
    assert stored.reason == RejectReason.CONSULTING


def test_changed_opinion_appends_new_row_instead_of_overwriting(seeded_db):
    """A user liking then later rejecting the same job must produce TWO rows,
    never an update of the first one. Feedback is append-only history.
    """
    job_id = job_id_for("Northwind Cognition")

    seeded_db.add(Feedback(job_id=job_id, action=FeedbackAction.LIKE))
    seeded_db.commit()

    seeded_db.add(
        Feedback(job_id=job_id, action=FeedbackAction.REJECT, reason=RejectReason.DOMAIN)
    )
    seeded_db.commit()

    events = (
        seeded_db.query(Feedback)
        .filter(Feedback.job_id == job_id)
        .order_by(Feedback.id)
        .all()
    )
    assert len(events) == 2
    assert events[0].action == FeedbackAction.LIKE
    assert events[1].action == FeedbackAction.REJECT
    # the original LIKE event must remain untouched
    assert events[0].reason is None


def test_feedback_history_survives_across_many_jobs(seeded_db):
    for i in range(1, 11):
        seeded_db.add(Feedback(job_id=i, action=FeedbackAction.SHORTLIST))
    seeded_db.commit()

    assert seeded_db.query(Feedback).count() == 10
