import type {
  FeedbackAction,
  FeedbackEvent,
  JobDetail,
  PreferenceSignal,
  RankedJob,
  RejectReason,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${init?.method ?? "GET"} ${path} failed (${res.status}): ${body}`);
  }
  return res.json() as Promise<T>;
}

export function fetchRankedJobs(): Promise<RankedJob[]> {
  return request<RankedJob[]>("/jobs");
}

export function fetchJobDetail(jobId: number): Promise<JobDetail> {
  return request<JobDetail>(`/jobs/${jobId}`);
}

export interface FeedbackPayload {
  job_id: number;
  action: FeedbackAction;
  reason?: RejectReason;
  free_text?: string;
}

export function postFeedback(payload: FeedbackPayload): Promise<FeedbackEvent> {
  return request<FeedbackEvent>("/feedback", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchFeedbackHistory(jobId?: number): Promise<FeedbackEvent[]> {
  const query = jobId != null ? `?job_id=${jobId}` : "";
  return request<FeedbackEvent[]>(`/feedback/history${query}`);
}

export function fetchPreferences(): Promise<PreferenceSignal[]> {
  return request<PreferenceSignal[]>("/preferences");
}
