export interface CandidateProfile {
  id: string;
  user_id: string;
  skills: string[];
  education: string;
  project_summaries: string;
  preferences: {
    desired_roles: string[];
    locations: string[];
    experience_level: string;
  };
  avatar?: string;
}

export interface MatchScore {
  score: number;
  explanation: string;
}
