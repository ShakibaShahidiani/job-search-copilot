export type WorkModel = "remote" | "hybrid" | "onsite";
export type EmploymentType = "full_time" | "part_time" | "contract" | "internship";
export type CompanyType = "product" | "consultancy";
export type SeniorityLevel = "junior" | "medior" | "senior";
export type JobStatus = "active" | "closed" | "expired";

export type FeedbackAction =
  | "LIKE"
  | "REJECT"
  | "SHORTLIST"
  | "APPLY"
  | "INTERVIEW"
  | "OFFER";

export type RejectReason =
  | "too_senior"
  | "too_junior"
  | "consulting"
  | "company"
  | "domain"
  | "compensation"
  | "location"
  | "technology"
  | "role_content"
  | "language"
  | "visa"
  | "other";

export const REJECT_REASONS: { value: RejectReason; label: string }[] = [
  { value: "too_senior", label: "Too senior" },
  { value: "too_junior", label: "Too junior" },
  { value: "consulting", label: "Consulting" },
  { value: "company", label: "Company" },
  { value: "domain", label: "Domain" },
  { value: "compensation", label: "Compensation" },
  { value: "location", label: "Location" },
  { value: "technology", label: "Technology" },
  { value: "role_content", label: "Role content" },
  { value: "language", label: "Language" },
  { value: "visa", label: "Visa" },
  { value: "other", label: "Other" },
];

export interface Gap {
  skill: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "BLOCKER";
}

export interface RankedJob {
  id: number;
  company: string;
  title: string;
  location: string;
  work_model: WorkModel;
  employment_type: EmploymentType;
  role_family: string;
  domain: string;
  company_type: CompanyType;
  seniority_level: SeniorityLevel;
  status: JobStatus;
  top_matches: string[];
  gaps: Gap[];
  blockers: string[];
  base_score: number;
  preference_adjustment: number;
  final_score: number;
  preference_explanation: string[];
}

export interface JobDetail extends RankedJob {
  source_url: string;
  direct_application_url: string | null;
  posted_date: string | null;
  discovered_at: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_requirement: string;
  language_requirements: string;
  technologies: string[];
  technical_fit: number;
  demonstrated_evidence: number;
  seniority_fit: number;
  domain_fit: number;
  infrastructure_fit: number;
  location_fit: number;
  language_fit: number;
  career_direction_fit: number;
  preference_fit: number;
  freshness: number;
  rationale: string;
}

export interface FeedbackEvent {
  id: number;
  job_id: number;
  action: FeedbackAction;
  reason: RejectReason | null;
  free_text: string | null;
  created_at: string;
}

export type FeatureType =
  | "role_family"
  | "technology"
  | "domain"
  | "company_type"
  | "seniority"
  | "location"
  | "work_model";

export type Confidence = "observation" | "weak" | "medium" | "strong";

export interface PreferenceSignal {
  feature_type: FeatureType;
  feature_value: string;
  weight: number;
  evidence_count: number;
  confidence: Confidence;
  updated_at: string;
}
