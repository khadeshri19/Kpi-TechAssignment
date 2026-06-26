import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { Job, JobFilters } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Spinner } from '../../components/ui/Spinner';
import { EmptyState } from '../../components/ui/EmptyState';
import { Modal } from '../../components/ui/Modal';
import styles from './styles.module.css';

export const JobBrowser = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filters, setFilters] = useState<JobFilters>({});
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState<string | null>(null);
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(new Set());
  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [errorModalMsg, setErrorModalMsg] = useState<string | null>(null);

  const targetJobId = searchParams.get('jobId');

  useEffect(() => {
    if (targetJobId && jobs.length > 0) {
      const job = jobs.find(j => j.id === targetJobId);
      if (job) {
        setSelectedJob(job);
      }
    }
  }, [targetJobId, jobs]);

  const handleCloseModal = () => {
    setSelectedJob(null);
    if (searchParams.has('jobId')) {
      const newParams = new URLSearchParams(searchParams);
      newParams.delete('jobId');
      setSearchParams(newParams);
    }
  };

  useEffect(() => {
    setLoading(true);
    api.getJobs(filters)
      .then(setJobs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filters]);

  const handleApply = async (jobId: string, fromModal = false) => {
    setApplying(jobId);
    try {
      const profile = await api.getProfile();
      if (!profile || !profile.id) {
        throw new Error("You must create a candidate profile first.");
      }
      await api.applyToJob({ job_id: jobId, candidate_id: profile.id });
      setAppliedJobs(prev => new Set(prev).add(jobId));
      // Close the detail modal after successful application
      if (fromModal) setSelectedJob(null);
    } catch (err: any) {
      setErrorModalMsg(err.message || 'Application failed. Please make sure your profile is completed.');
    } finally {
      setApplying(null);
    }
  };

  return (
    <DashboardLayout title="Browse Jobs">
      <div className={styles.filters}>
        <Input placeholder="Filter by skill..." onChange={e => setFilters(f => ({ ...f, skill: e.target.value }))} />
        <Input placeholder="Filter by location..." onChange={e => setFilters(f => ({ ...f, location: e.target.value }))} />
        <Input placeholder="Filter by experience..." onChange={e => setFilters(f => ({ ...f, experience_level: e.target.value }))} />
      </div>

      {loading ? (
        <Spinner size={32} />
      ) : jobs.length === 0 ? (
        <EmptyState title="No open jobs match your filters" />
      ) : (
        <div className={styles.jobGrid}>
          {jobs.map(job => (
            <Card key={job.id} className={styles.jobCard}>
              <div className={styles.jobHeader}>
                <h3 className={styles.jobTitle}>{job.title}</h3>
                <Badge variant={job.status === 'open' ? 'success' : 'neutral'}>{job.status}</Badge>
              </div>
              <div className={styles.jobMeta}>
                <span>{job.location}</span>
                <span>•</span>
                <span>{job.experience_level}</span>
              </div>
              <p className={styles.jobDesc}>{job.description}</p>
              <div className={styles.jobSkills}>
                {job.required_skills.map(s => (
                  <span key={s} className={styles.skillTag}>{s}</span>
                ))}
              </div>
              <div className={styles.jobFooter} style={{ display: 'flex', gap: 'var(--sp-2)' }}>
                <Button
                  variant="secondary"
                  onClick={() => setSelectedJob(job)}
                  style={{ flex: 1 }}
                >
                  View Details
                </Button>
                <Button
                  onClick={() => handleApply(job.id)}
                  disabled={job.status === 'closed' || appliedJobs.has(job.id)}
                  loading={applying === job.id}
                  style={{ flex: 1.5 }}
                >
                  {appliedJobs.has(job.id) ? 'Applied ✓' : 'Apply Now'}
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* ── Job Detail Modal ── */}
      <Modal
        isOpen={selectedJob !== null}
        onClose={handleCloseModal}
        title={selectedJob?.title || ''}
      >
        {selectedJob && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div className={styles.jobMeta} style={{ marginBottom: 0 }}>
                <span>{selectedJob.location}</span>
                <span>•</span>
                <span>{selectedJob.experience_level}</span>
              </div>
              <Badge variant={selectedJob.status === 'open' ? 'success' : 'neutral'}>
                {selectedJob.status}
              </Badge>
            </div>

            <div style={{ borderTop: '1px solid var(--border)', paddingTop: 'var(--sp-4)' }}>
              <h4 style={{ marginBottom: 'var(--sp-2)', fontSize: 'var(--fs-base)', fontWeight: 'var(--fw-semibold)' }}>Job Description</h4>
              <p style={{ color: 'var(--text-secondary)', whiteSpace: 'pre-wrap', lineHeight: 'var(--lh)', fontSize: 'var(--fs-sm)' }}>
                {selectedJob.description}
              </p>
            </div>

            <div style={{ borderTop: '1px solid var(--border)', paddingTop: 'var(--sp-4)' }}>
              <h4 style={{ marginBottom: 'var(--sp-2)', fontSize: 'var(--fs-base)', fontWeight: 'var(--fw-semibold)' }}>Required Skills</h4>
              <div className={styles.jobSkills} style={{ marginBottom: 0 }}>
                {selectedJob.required_skills.map(s => (
                  <span key={s} className={styles.skillTag}>{s}</span>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', gap: 'var(--sp-2)', borderTop: '1px solid var(--border)', paddingTop: 'var(--sp-4)', marginTop: 'var(--sp-2)' }}>
              <Button
                variant="ghost"
                onClick={handleCloseModal}
                style={{ flex: 1 }}
              >
                Close
              </Button>
              <Button
                onClick={() => handleApply(selectedJob.id, true)}
                disabled={selectedJob.status === 'closed' || appliedJobs.has(selectedJob.id)}
                loading={applying === selectedJob.id}
                style={{ flex: 1.5 }}
              >
                {appliedJobs.has(selectedJob.id) ? 'Applied ✓' : 'Apply Now'}
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* ── Error / Incomplete Profile Modal ── */}
      <Modal
        isOpen={errorModalMsg !== null}
        onClose={() => setErrorModalMsg(null)}
        title="Application Status"
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)', textAlign: 'center', padding: 'var(--sp-2) 0' }}>
          <div style={{ color: 'var(--danger)', fontSize: '2rem' }}>⚠️</div>
          <p style={{ color: 'var(--text)', fontSize: 'var(--fs-base)', lineHeight: 'var(--lh)' }}>{errorModalMsg}</p>
          <div style={{ display: 'flex', gap: 'var(--sp-2)', marginTop: 'var(--sp-2)', justifyContent: 'center' }}>
            <Button variant="secondary" onClick={() => setErrorModalMsg(null)}>Close</Button>
            {errorModalMsg?.toLowerCase().includes('profile') && (
              <Button onClick={() => { setErrorModalMsg(null); navigate('/candidate/profile'); }}>Complete Profile</Button>
            )}
          </div>
        </div>
      </Modal>
    </DashboardLayout>
  );
};
