import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { DashboardMetrics } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Card } from '../../components/ui/Card';
import { Spinner } from '../../components/ui/Spinner';
import { EmptyState } from '../../components/ui/EmptyState';
import styles from './styles.module.css';

export const Overview = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboardMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <DashboardLayout title="Overview"><Spinner size={32} /></DashboardLayout>;
  if (!metrics) return <DashboardLayout title="Overview"><EmptyState title="Failed to load metrics" /></DashboardLayout>;

  const totalApplications = Object.values(metrics.pipeline_status_counts).reduce((a, b) => a + b, 0);

  return (
    <DashboardLayout title="Dashboard Overview">
      <div className={styles.statsGrid}>
        <Card>
          <div className={styles.statLabel}>Total Jobs</div>
          <div className={styles.statValue}>{metrics.applications_per_job.length}</div>
        </Card>
        <Card>
          <div className={styles.statLabel}>Total Applications</div>
          <div className={styles.statValue}>{totalApplications}</div>
        </Card>
        <Card>
          <div className={styles.statLabel}>Shortlisted</div>
          <div className={styles.statValue}>{metrics.pipeline_status_counts.shortlisted || 0}</div>
        </Card>
        <Card>
          <div className={styles.statLabel}>Rejected</div>
          <div className={styles.statValue}>{metrics.pipeline_status_counts.rejected || 0}</div>
        </Card>
      </div>

      <div className={styles.chartsGrid}>
        <Card>
          <h3 className={styles.chartTitle}>Top Skills</h3>
          {metrics.skill_distribution.length === 0 ? (
            <EmptyState title="No skill data available" />
          ) : (
            <div className={styles.barList}>
              {metrics.skill_distribution.map((item) => (
                <div key={item.skill} className={styles.barItem}>
                  <div className={styles.barLabel}>
                    <span>{item.skill}</span>
                    <span>{item.count}</span>
                  </div>
                  <div className={styles.barTrack}>
                    <div 
                      className={styles.barFill} 
                      style={{ width: `${Math.min((item.count / metrics.skill_distribution[0].count) * 100, 100)}%` }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card>
          <h3 className={styles.chartTitle}>Applications per Job</h3>
          {metrics.applications_per_job.length === 0 ? (
            <EmptyState title="No job data available" />
          ) : (
            <div className={styles.barList}>
              {metrics.applications_per_job.map((item) => (
                <div key={item.job_title} className={styles.barItem}>
                  <div className={styles.barLabel}>
                    <span className={styles.truncate}>{item.job_title}</span>
                    <span>{item.count}</span>
                  </div>
                  <div className={styles.barTrack}>
                    <div 
                      className={styles.barFillAlt} 
                      style={{ width: `${Math.min((item.count / (Math.max(...metrics.applications_per_job.map(j => j.count)) || 1)) * 100, 100)}%` }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
};
