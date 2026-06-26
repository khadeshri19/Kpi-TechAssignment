import type {
  LoginPayload, LoginResponse, RegisterPayload, RegisterResponse,
  Job, JobCreate, JobUpdate, JobFilters,
  ApplicationDetail, ApplicationStatusUpdate, ApplicationCreate,
  CandidateProfile, CandidateProfileCreate,
  MatchRequest, MatchResult,
  DashboardMetrics,
} from '../types';

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function authHeaders(): Record<string, string> {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (res.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('avatar');
    window.location.href = '/login';
    throw new ApiError('Unauthorized', 401);
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(body.detail || res.statusText, res.status);
  }
  return res.json();
}

export const api = {
  /* ── Auth ── */
  login: (payload: LoginPayload) =>
    request<LoginResponse>(`${BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),

  register: (payload: RegisterPayload) =>
    request<RegisterResponse>(`${BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),

  /* ── Jobs ── */
  getJobs: (filters?: JobFilters) => {
    const params = new URLSearchParams();
    if (filters?.skill) params.set('skill', filters.skill);
    if (filters?.location) params.set('location', filters.location);
    if (filters?.experience_level) params.set('experience_level', filters.experience_level);
    const qs = params.toString();
    return request<Job[]>(`${BASE}/jobs${qs ? `?${qs}` : ''}`, { headers: authHeaders() });
  },

  createJob: (payload: JobCreate) =>
    request<Job>(`${BASE}/jobs`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  updateJob: (id: string, payload: JobUpdate) =>
    request<Job>(`${BASE}/jobs/${id}`, {
      method: 'PUT',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  /* ── Applications ── */
  getJobApplications: (jobId: string) =>
    request<ApplicationDetail[]>(`${BASE}/jobs/${jobId}/applications/details`, {
      headers: authHeaders(),
    }),

  updateApplicationStatus: (id: string, payload: ApplicationStatusUpdate) =>
    request<unknown>(`${BASE}/applications/${id}/status`, {
      method: 'PATCH',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  applyToJob: (payload: ApplicationCreate) =>
    request<unknown>(`${BASE}/apply`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  /* ── Candidates ── */
  getProfile: () =>
    request<CandidateProfile>(`${BASE}/candidate/profile`, {
      headers: authHeaders(),
    }),

  upsertProfile: (payload: CandidateProfileCreate) =>
    request<CandidateProfile>(`${BASE}/candidate/profile`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  matchJobs: (payload: MatchRequest) =>
    request<MatchResult[]>(`${BASE}/candidate/match`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload),
    }),

  /* ── Dashboard ── */
  getDashboardMetrics: () =>
    request<DashboardMetrics>(`${BASE}/dashboard/metrics`, {
      headers: authHeaders(),
    }),
};
