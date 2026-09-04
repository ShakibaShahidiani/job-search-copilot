import { useState } from "react";
import { fetchJobDetail } from "../api/client";
import type { JobDetail, RankedJob, RejectReason } from "../types";
import { RejectReasonPicker } from "./RejectReasonPicker";

interface Props {
  job: RankedJob;
  onFeedback: (action: "LIKE" | "REJECT" | "SHORTLIST", reason?: RejectReason) => void;
}

const GAP_ORDER: Record<string, number> = { BLOCKER: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };

function scoreClass(score: number, hasBlocker: boolean): string {
  if (hasBlocker) return "score-badge score-blocked";
  if (score >= 8.5) return "score-badge score-high";
  if (score >= 7) return "score-badge score-medium";
  return "score-badge score-low";
}

export function JobCard({ job, onFeedback }: Props) {
  const [showReasonPicker, setShowReasonPicker] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [detail, setDetail] = useState<JobDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const hasBlocker = job.blockers.length > 0;
  const gaps = [...job.gaps].sort((a, b) => GAP_ORDER[a.severity] - GAP_ORDER[b.severity]).slice(0, 3);

  async function toggleExpanded() {
    if (!expanded && !detail) {
      setLoadingDetail(true);
      try {
        const d = await fetchJobDetail(job.id);
        setDetail(d);
      } finally {
        setLoadingDetail(false);
      }
    }
    setExpanded((e) => !e);
  }

  function handleReject(reason?: RejectReason) {
    setShowReasonPicker(false);
    onFeedback("REJECT", reason);
  }

  return (
    <article className={`job-card${hasBlocker ? " job-card-blocked" : ""}`}>
      <div className="job-card-top">
        <div className={scoreClass(job.final_score, hasBlocker)}>{job.final_score.toFixed(1)}</div>
        <div className="job-card-heading">
          <h3>{job.title}</h3>
          <div className="job-card-sub">
            {job.company} · {job.location} · {job.work_model}
          </div>
        </div>
      </div>

      {hasBlocker && (
        <div className="blocker-banner">
          Hard constraint: {job.blockers.join(", ").replaceAll("_", " ")}
        </div>
      )}

      {job.preference_adjustment !== 0 && (
        <div className="pref-adjustment">
          preference adjustment: {job.preference_adjustment > 0 ? "+" : ""}
          {job.preference_adjustment.toFixed(2)} (base {job.base_score.toFixed(1)})
          {job.preference_explanation.length > 0 && (
            <span className="pref-explanation"> — {job.preference_explanation.join(", ")}</span>
          )}
        </div>
      )}

      <div className="chip-row">
        {job.top_matches.slice(0, 5).map((m) => (
          <span key={m} className="chip chip-match">
            {m}
          </span>
        ))}
      </div>

      {gaps.length > 0 && (
        <div className="chip-row">
          {gaps.map((g) => (
            <span key={g.skill} className={`chip chip-gap chip-gap-${g.severity.toLowerCase()}`}>
              {g.skill}
            </span>
          ))}
        </div>
      )}

      <div className="job-card-actions">
        <button type="button" className="btn btn-like" onClick={() => onFeedback("LIKE")}>
          Like
        </button>
        <button
          type="button"
          className="btn btn-reject"
          onClick={() => setShowReasonPicker((s) => !s)}
        >
          Reject
        </button>
        <button
          type="button"
          className="btn btn-shortlist"
          onClick={() => onFeedback("SHORTLIST")}
        >
          Shortlist
        </button>
        <button type="button" className="btn btn-more" onClick={toggleExpanded}>
          {expanded ? "Less" : "More"}
        </button>
      </div>

      {showReasonPicker && (
        <RejectReasonPicker onPick={handleReject} onCancel={() => setShowReasonPicker(false)} />
      )}

      {expanded && (
        <div className="job-card-detail">
          {loadingDetail && <p>Loading…</p>}
          {detail && (
            <>
              <p className="job-description">{detail.description}</p>
              <p>
                <strong>Experience:</strong> {detail.experience_requirement} ·{" "}
                <strong>Language:</strong> {detail.language_requirements}
              </p>
              <p>
                <strong>Required:</strong> {detail.required_skills.join(", ")}
              </p>
              <p>
                <strong>Preferred:</strong> {detail.preferred_skills.join(", ")}
              </p>
              <p className="rationale">{detail.rationale}</p>
              <a href={detail.source_url} target="_blank" rel="noreferrer">
                source (fixture)
              </a>
            </>
          )}
        </div>
      )}
    </article>
  );
}
