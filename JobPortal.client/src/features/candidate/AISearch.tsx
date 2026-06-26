import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { Job, MatchResult } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EmptyState } from '../../components/ui/EmptyState';
import { Sparkles, Shield, Lock, ArrowRight } from 'lucide-react';
import styles from './styles.module.css';

export const AISearch = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<MatchResult[]>([]);
  const [jobsMap, setJobsMap] = useState<Record<string, Job>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      // Fetch profile and all jobs in parallel
      const [profile, allJobs] = await Promise.all([
        api.getProfile(),
        api.getJobs(),
      ]);

      if (!profile || !profile.id) {
        throw new Error('You must create a candidate profile first before running AI matching.');
      }

      // Build a quick lookup map: job.id → job
      const map: Record<string, Job> = {};
      allJobs.forEach((j) => { map[j.id] = j; });
      setJobsMap(map);

      const matches = await api.matchJobs({ candidate_id: profile.id, query });
      setResults(matches);
    } catch (err: any) {
      setError(err.message || 'Matching failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  return (
    <DashboardLayout title="AI Job Matcher">
      <div className={styles.searchContainer}>
        <div className={styles.searchBox}>
          <div className={styles.topGlow}></div>
          <Sparkles className={styles.sparklesIcon} size={20} strokeWidth={2.5} />
          <textarea
            className={styles.aiTextarea}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your ideal role... e.g. 'Looking for a senior backend role using Python and FastAPI'"
            rows={3}
          />
        </div>

        <div className={styles.searchFooter}>
          <div className={styles.footerLeft}>
            <div className={styles.disclaimer}>
              AI-powered matching using semantic similarity — press Enter or click →
            </div>
          </div>
          <div className={styles.footerRight}>
            <div className={styles.shieldWrapper}>
              <Shield className={styles.shieldIcon} size={28} strokeWidth={1.5} />
              <Lock className={styles.lockIcon} size={12} strokeWidth={2.5} />
            </div>
            <button
              className={styles.submitRoundBtn}
              onClick={handleSearch}
              disabled={!query.trim() || loading}
            >
              <ArrowRight size={20} />
            </button>
          </div>
        </div>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: 'var(--sp-8)', color: 'var(--text-secondary)' }}>
          Matching your profile against open roles…
        </div>
      )}

      {error && <div className={styles.msgError} style={{ marginTop: 'var(--sp-4)' }}>{error}</div>}

      <div className={styles.resultsList}>
        {results.length === 0 && !loading && !error && (
          <EmptyState title="Enter a description above to see AI-ranked matches" />
        )}

        {results.map((res) => {
          const job = jobsMap[res.job_id];
          return (
            <Card key={res.job_id} className={styles.matchCard}>
              <div className={styles.matchHeader}>
                <div>
                  <h4 style={{ fontWeight: 'var(--fw-semibold)', color: 'var(--text)' }}>
                    {job?.title ?? `Job ${res.job_id.substring(0, 8)}…`}
                  </h4>
                  {job && (
                    <div style={{ fontSize: 'var(--fs-sm)', color: 'var(--text-secondary)', marginTop: '2px' }}>
                      {job.location} · {job.experience_level}
                    </div>
                  )}
                </div>
                <Badge variant={res.match_score >= 80 ? 'success' : res.match_score >= 50 ? 'warning' : 'neutral'}>
                  {res.match_score}% Match
                </Badge>
              </div>
              <p className={styles.explanation}>{res.explanation}</p>
              {job && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--sp-1)', margin: 'var(--sp-3) 0' }}>
                  {job.required_skills.map(s => (
                    <span key={s} style={{
                      background: 'var(--surface)', border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-sm)', padding: '2px 6px', fontSize: '11px'
                    }}>{s}</span>
                  ))}
                </div>
              )}
              <div style={{ marginTop: 'var(--sp-3)' }}>
                <Button size="sm" variant="secondary" onClick={() => navigate(`/candidate?jobId=${res.job_id}`)}>
                  View &amp; Apply
                </Button>
              </div>
            </Card>
          );
        })}
      </div>
    </DashboardLayout>
  );
};
