import { useEffect, useState } from "react";
import { fetchPreferences, fetchRankedJobs, postFeedback } from "./api/client";
import { JobCard } from "./components/JobCard";
import { PreferencePanel } from "./components/PreferencePanel";
import type { PreferenceSignal, RankedJob, RejectReason } from "./types";
import "./App.css";

function App() {
  const [jobs, setJobs] = useState<RankedJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPreferences, setShowPreferences] = useState(false);
  const [preferences, setPreferences] = useState<PreferenceSignal[]>([]);

  async function loadJobs() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchRankedJobs();
      setJobs(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load jobs");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadJobs();
  }, []);

  async function handleFeedback(
    jobId: number,
    action: "LIKE" | "REJECT" | "SHORTLIST",
    reason?: RejectReason,
  ) {
    await postFeedback({ job_id: jobId, action, reason });
    await loadJobs();
  }

  async function openPreferences() {
    const data = await fetchPreferences();
    setPreferences(data);
    setShowPreferences(true);
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Job Search Copilot</h1>
        <button type="button" className="btn btn-secondary" onClick={openPreferences}>
          View learned preferences
        </button>
      </header>

      {loading && <p className="status-text">Loading jobs…</p>}
      {error && <p className="status-text status-error">{error}</p>}

      <div className="job-grid">
        {jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            onFeedback={(action, reason) => handleFeedback(job.id, action, reason)}
          />
        ))}
      </div>

      {showPreferences && (
        <PreferencePanel signals={preferences} onClose={() => setShowPreferences(false)} />
      )}
    </div>
  );
}

export default App;
