import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../../services/api';
import { ApplicationDetail, ApplicationStatus } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Select } from '../../components/ui/Select';
import { Spinner } from '../../components/ui/Spinner';
import { EmptyState } from '../../components/ui/EmptyState';
import styles from './styles.module.css';

export const ApplicationPipeline = () => {
  const { id } = useParams();
  const [apps, setApps] = useState<ApplicationDetail[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchApps = () => {
    if (!id) return;
    setLoading(true);
    api.getJobApplications(id)
      .then(setApps)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchApps();
  }, [id]);

  const updateStatus = async (appId: string, status: ApplicationStatus) => {
    try {
      await api.updateApplicationStatus(appId, { status });
      fetchApps();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <DashboardLayout title="Pipeline"><Spinner size={32} /></DashboardLayout>;

  const columns: { title: string; status: ApplicationStatus }[] = [
    { title: 'Applied', status: 'applied' },
    { title: 'Shortlisted', status: 'shortlisted' },
    { title: 'Rejected', status: 'rejected' },
  ];

  return (
    <DashboardLayout 
      title="Application Pipeline" 
      action={<Link to="/admin/jobs" style={{ color: 'var(--text-secondary)', textDecoration: 'underline' }}>Back to Jobs</Link>}
    >
      <div className={styles.kanban}>
        {columns.map(col => {
          const colApps = apps.filter(a => a.status === col.status);
          return (
            <div key={col.status} className={styles.column}>
              <div className={styles.colHeader}>
                {col.title}
                <span style={{ background: 'var(--bg)', padding: '2px 8px', borderRadius: 'var(--radius-pill)' }}>{colApps.length}</span>
              </div>
              
              {colApps.length === 0 ? (
                <EmptyState title={`No ${col.status} candidates`} />
              ) : (
                colApps.map(app => (
                  <div key={app.id} className={styles.appCard}>
                    <div className={styles.appName}>{app.candidate_name}</div>
                    <div className={styles.appEmail}>{app.candidate_email}</div>
                    <div className={styles.appSkills}>
                      {app.candidate_skills.slice(0, 3).map(s => (
                        <span key={s} style={{ background: 'var(--surface)', fontSize: '10px', padding: '2px 6px', borderRadius: '4px' }}>{s}</span>
                      ))}
                    </div>
                    <Select 
                      value={app.status} 
                      onChange={e => updateStatus(app.id, e.target.value as ApplicationStatus)}
                      options={[
                        { value: 'applied', label: 'Applied' },
                        { value: 'shortlisted', label: 'Shortlist' },
                        { value: 'rejected', label: 'Reject' }
                      ]}
                    />
                  </div>
                ))
              )}
            </div>
          );
        })}
      </div>
    </DashboardLayout>
  );
};
