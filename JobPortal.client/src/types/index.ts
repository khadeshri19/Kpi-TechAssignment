/* ── Auth ── */
export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  role: 'admin' | 'candidate';
  name: string;
  email: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'candidate';
}

export interface RegisterResponse {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'candidate';
  created_at: string;
}

/* ── Jobs ── */
export interface Job {
  id: string;
  title: string;
  description: string;
  required_skills: string[];
  experience_level: string;
  location: string;
  status: 'open' | 'closed';
  created_at: string;
}

export interface JobCreate {
  title: string;
  description: string;
  required_skills: string[];
  experience_level: string;
  location: string;
  status: 'open' | 'closed';
}

export interface JobUpdate {
  title?: string;
  description?: string;
  required_skills?: string[];
  experience_level?: string;
  location?: string;
  status?: 'open' | 'closed';
}

export interface JobFilters {
  skill?: string;
  location?: string;
  experience_level?: string;
}

/* ── Applications ── */
export type ApplicationStatus = 'applied' | 'shortlisted' | 'rejected';

export interface Application {
  id: string;
  job_id: string;
  candidate_id: string;
  status: ApplicationStatus;
  applied_at: string;
  profile_snapshot: Record<string, unknown>;
}

export interface ApplicationDetail extends Application {
  candidate_name: string;
  candidate_email: string;
  candidate_skills: string[];
  candidate_education?: string;
}

export interface ApplicationStatusUpdate {
  status: ApplicationStatus;
}

export interface ApplicationCreate {
  job_id: string;
  candidate_id: string;
}

/* ── Candidates ── */
export interface CandidatePreferences {
  desired_roles: string[];
  locations: string[];
  experience_level: string;
}

export interface CandidateProfile {
  id: string;
  user_id: string;
  skills: string[];
  education: string;
  project_summaries: string;
  preferences: CandidatePreferences;
  avatar?: string;
  name?: string;
  created_at: string;
}

export interface CandidateProfileCreate {
  user_id: string;
  skills: string[];
  education: string;
  project_summaries: string;
  preferences: CandidatePreferences;
  avatar?: string;
  name?: string;
}


/* ── AI Matching ── */
export interface MatchRequest {
  candidate_id: string;
  query: string;
}

export interface MatchResult {
  job_id: string;
  match_score: number;
  explanation: string;
}

/* ── Dashboard Metrics ── */
export interface DashboardMetrics {
  applications_per_job: Array<{ job_title: string; count: number }>;
  pipeline_status_counts: Record<ApplicationStatus, number>;
  skill_distribution: Array<{ skill: string; count: number }>;
}
