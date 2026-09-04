from tests.conftest import job_id_for


def test_list_jobs_returns_all_ten_ranked(seeded_client):
    resp = seeded_client.get("/api/jobs")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 10
    for job in data:
        assert "final_score" in job
        assert "base_score" in job
        assert "preference_adjustment" in job
        assert "preference_explanation" in job
        assert "top_matches" in job
        assert "gaps" in job

    non_blocked = [j["final_score"] for j in data if not j["blockers"]]
    assert non_blocked == sorted(non_blocked, reverse=True)
    blocked_indexes = [i for i, j in enumerate(data) if j["blockers"]]
    non_blocked_indexes = [i for i, j in enumerate(data) if not j["blockers"]]
    if blocked_indexes and non_blocked_indexes:
        assert min(blocked_indexes) > max(non_blocked_indexes)


def test_get_single_job_returns_full_detail(seeded_client):
    job_id = job_id_for("Northwind Cognition")
    resp = seeded_client.get(f"/api/jobs/{job_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["company"] == "Northwind Cognition"
    assert "technical_fit" in data
    assert "rationale" in data
    assert "description" in data


def test_get_unknown_job_returns_404(seeded_client):
    resp = seeded_client.get("/api/jobs/9999")
    assert resp.status_code == 404


def test_post_feedback_persists_and_returns_201(seeded_client):
    job_id = job_id_for("Aether Labs")
    resp = seeded_client.post("/api/feedback", json={"job_id": job_id, "action": "LIKE"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["job_id"] == job_id
    assert body["action"] == "LIKE"
    assert body["id"] is not None


def test_post_feedback_for_unknown_job_returns_404(seeded_client):
    resp = seeded_client.post("/api/feedback", json={"job_id": 9999, "action": "LIKE"})
    assert resp.status_code == 404


def test_post_feedback_reason_without_reject_is_rejected(seeded_client):
    job_id = job_id_for("Aether Labs")
    resp = seeded_client.post(
        "/api/feedback", json={"job_id": job_id, "action": "LIKE", "reason": "consulting"}
    )
    assert resp.status_code == 422


def test_feedback_history_filters_by_job(seeded_client):
    job_a = job_id_for("Aether Labs")
    job_b = job_id_for("Northwind Cognition")
    seeded_client.post("/api/feedback", json={"job_id": job_a, "action": "LIKE"})
    seeded_client.post("/api/feedback", json={"job_id": job_b, "action": "SHORTLIST"})

    resp = seeded_client.get(f"/api/feedback/history?job_id={job_a}")
    assert resp.status_code == 200
    events = resp.json()
    assert len(events) == 1
    assert events[0]["job_id"] == job_a


def test_feedback_history_without_filter_returns_all(seeded_client):
    job_a = job_id_for("Aether Labs")
    job_b = job_id_for("Northwind Cognition")
    seeded_client.post("/api/feedback", json={"job_id": job_a, "action": "LIKE"})
    seeded_client.post("/api/feedback", json={"job_id": job_b, "action": "SHORTLIST"})

    resp = seeded_client.get("/api/feedback/history")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_feedback_then_preferences_reflects_new_signal(seeded_client):
    job_id = job_id_for("Deltaworks Consulting")
    seeded_client.post(
        "/api/feedback",
        json={"job_id": job_id, "action": "REJECT", "reason": "consulting"},
    )

    resp = seeded_client.get("/api/preferences")
    assert resp.status_code == 200
    signals = resp.json()
    company_type_signal = next(
        s
        for s in signals
        if s["feature_type"] == "company_type" and s["feature_value"] == "consultancy"
    )
    assert company_type_signal["weight"] < 0
    assert company_type_signal["evidence_count"] == 1


def test_feedback_triggers_rerank(seeded_client):
    job_id = job_id_for("Deltaworks Consulting")
    before = seeded_client.get("/api/jobs").json()
    before_score = next(j for j in before if j["id"] == job_id)["final_score"]

    seeded_client.post(
        "/api/feedback",
        json={"job_id": job_id, "action": "REJECT", "reason": "consulting"},
    )

    after = seeded_client.get("/api/jobs").json()
    after_score = next(j for j in after if j["id"] == job_id)["final_score"]

    assert after_score < before_score
