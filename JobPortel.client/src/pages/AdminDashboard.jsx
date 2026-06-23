import React, { useState, useEffect } from 'react';
import '../index.css';

const API_BASE_URL = 'http://localhost:8000';

export default function AdminDashboard() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch jobs and their application counts on mount
  useEffect(() => {
    fetchJobsAndCounts();
  }, []);

  // Fetch application details when a job is selected
  useEffect(() => {
    if (selectedJob) {
      fetchApplications(selectedJob.id);
    } else {
      setApplications([]);
    }
  }, [selectedJob]);

  const fetchJobsAndCounts = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE_URL}/jobs`);
      if (!res.ok) throw new Error('Failed to fetch jobs');
      const jobsData = await res.json();

      // Retrieve applications for each job to count them
      const jobsWithCounts = await Promise.all(
        jobsData.map(async (job) => {
          try {
            const appRes = await fetch(`${API_BASE_URL}/jobs/${job.id}/applications`);
            if (appRes.ok) {
              const appData = await appRes.json();
              return { ...job, applicationCount: appData.length };
            }
          } catch (e) {
            console.error(`Error fetching applications for job ${job.id}:`, e);
          }
          return { ...job, applicationCount: 0 };
        })
      );

      setJobs(jobsWithCounts);
      // Keep selected job updated if it exists
      if (selectedJob) {
        const updatedSelected = jobsWithCounts.find(j => j.id === selectedJob.id);
        if (updatedSelected) setSelectedJob(updatedSelected);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async (jobId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/jobs/${jobId}/applications/details`);
      if (!res.ok) throw new Error('Failed to fetch application details');
      const data = await res.json();
      setApplications(data);
    } catch (err) {
      console.error(err);
    }
  };

  const toggleJobStatus = async (job, e) => {
    e.stopPropagation();
    const updatedStatus = job.status === 'open' ? 'closed' : 'open';
    try {
      const res = await fetch(`${API_BASE_URL}/jobs/${job.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: job.title,
          description: job.description,
          required_skills: job.required_skills,
          experience_level: job.experience_level,
          location: job.location,
          status: updatedStatus
        }),
      });
      if (!res.ok) throw new Error('Failed to update job status');
      fetchJobsAndCounts();
    } catch (err) {
      alert(err.message);
    }
  };

  const updateApplicationStatus = async (appId, newStatus) => {
    try {
      const res = await fetch(`${API_BASE_URL}/applications/${appId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      if (!res.ok) throw new Error('Failed to update application status');
      if (selectedJob) {
        fetchApplications(selectedJob.id);
        fetchJobsAndCounts();
      }
    } catch (err) {
      alert(err.message);
    }
  };

  // Pipeline Status breakdown counts
  const pipelineBreakdown = () => {
    const counts = { applied: 0, shortlisted: 0, rejected: 0 };
    applications.forEach(app => {
      if (counts[app.status] !== undefined) counts[app.status]++;
    });
    return counts;
  };

  // Skill occurrences across all candidates for the selected job
  const getSkillDistribution = () => {
    const counts = {};
    applications.forEach(app => {
      (app.candidate_skills || []).forEach(skill => {
        const cleanSkill = skill.trim();
        counts[cleanSkill] = (counts[cleanSkill] || 0) + 1;
      });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  };

  return (
    <div style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
      <header style={{ marginBottom: '40px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', margin: 0, background: 'linear-gradient(to right, var(--accent-cyan), var(--accent-purple))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            TalentLink Admin
          </h1>
          <p style={{ color: 'var(--text-muted)', margin: '5px 0 0 0' }}>Pipeline Analytics & Applicant Tracker</p>
        </div>
        <div style={{ display: 'flex', gap: '15px' }}>
          <div className="glass-panel" style={{ padding: '10px 20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ height: '8px', width: '8px', borderRadius: '50%', backgroundColor: 'var(--accent-green)', display: 'inline-block' }}></span>
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>System Online</span>
          </div>
        </div>
      </header>

      {error && (
        <div style={{ padding: '15px', backgroundColor: 'rgba(255, 94, 98, 0.1)', border: '1px solid var(--accent-red)', borderRadius: '8px', color: 'var(--accent-red)', marginBottom: '20px' }}>
          Error: {error}
        </div>
      )}

      {/* Main Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '30px', alignItems: 'start' }}>
        
        {/* Job Management Panel */}
        <section className="glass-panel">
          <h2>Job Management</h2>
          {loading ? (
            <p style={{ color: 'var(--text-muted)' }}>Loading jobs...</p>
          ) : jobs.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No jobs found. Create some in the database first.</p>
          ) : (
            <table className="clean-table">
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Status</th>
                  <th>Applications</th>
                  <th>Toggle</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map(job => (
                  <tr key={job.id} onClick={() => setSelectedJob(job)} style={{ background: selectedJob?.id === job.id ? 'var(--bg-tertiary)' : 'transparent' }}>
                    <td style={{ fontWeight: '500' }}>{job.title}</td>
                    <td>
                      <span className={`badge ${job.status === 'open' ? 'badge-open' : 'badge-closed'}`}>
                        {job.status}
                      </span>
                    </td>
                    <td style={{ textAlign: 'center', color: 'var(--accent-cyan)', fontWeight: '600' }}>
                      {job.applicationCount}
                    </td>
                    <td>
                      <label className="switch" onClick={(e) => e.stopPropagation()}>
                        <input type="checkbox" checked={job.status === 'open'} onChange={(e) => toggleJobStatus(job, e)} />
                        <span className="slider"></span>
                      </label>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        {/* Application Details & Pipeline Panel */}
        <section className="glass-panel">
          {selectedJob ? (
            <>
              <h2>Applications for {selectedJob.title}</h2>
              
              {/* Analytics widgets */}
              <div className="analytics-grid">
                <div className="analytics-card">
                  <h4>Total Applicants</h4>
                  <div className="value">{applications.length}</div>
                </div>
                <div className="analytics-card">
                  <h4>Shortlisted</h4>
                  <div className="value" style={{ color: 'var(--accent-green)' }}>
                    {pipelineBreakdown().shortlisted}
                  </div>
                </div>
                <div className="analytics-card">
                  <h4>Applied / Active</h4>
                  <div className="value" style={{ color: 'var(--accent-cyan)' }}>
                    {pipelineBreakdown().applied}
                  </div>
                </div>
              </div>

              {applications.length === 0 ? (
                <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px 0' }}>No candidates have applied to this job yet.</p>
              ) : (
                <>
                  {/* Applicant Tracker Table */}
                  <table className="clean-table">
                    <thead>
                      <tr>
                        <th>Candidate</th>
                        <th>Skills</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {applications.map(app => (
                        <tr key={app.id}>
                          <td>
                            <div style={{ fontWeight: '600', color: '#fff' }}>{app.candidate_name}</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{app.candidate_email}</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic', marginTop: '4px' }}>
                              Edu: {app.candidate_education || 'N/A'}
                            </div>
                          </td>
                          <td>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px', maxWidth: '200px' }}>
                              {(app.candidate_skills || []).map((skill, i) => (
                                <span key={i} style={{ fontSize: '0.75rem', backgroundColor: 'var(--bg-tertiary)', padding: '2px 6px', borderRadius: '4px', border: '1px solid var(--border-muted)' }}>
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </td>
                          <td>
                            <select value={app.status} onChange={(e) => updateApplicationStatus(app.id, e.target.value)}>
                              <option value="applied">Applied</option>
                              <option value="shortlisted">Shortlisted</option>
                              <option value="rejected">Rejected</option>
                            </select>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  {/* Skills distribution visualizer */}
                  <div style={{ marginTop: '30px' }} className="glass-panel">
                    <h3 style={{ margin: '0 0 15px 0', fontSize: '1.1rem', fontWeight: '600' }}>Candidate Skills Distribution</h3>
                    {getSkillDistribution().length === 0 ? (
                      <p style={{ color: 'var(--text-muted)' }}>No skills data available.</p>
                    ) : (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {getSkillDistribution().map(([skill, count]) => {
                          const percentage = (count / applications.length) * 100;
                          return (
                            <div key={skill} style={{ display: 'grid', gridTemplateColumns: '120px 1fr 30px', alignItems: 'center', gap: '10px' }}>
                              <span style={{ fontSize: '0.85rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{skill}</span>
                              <div style={{ background: 'var(--bg-tertiary)', borderRadius: '4px', height: '8px', overflow: 'hidden' }}>
                                <div style={{ background: 'linear-gradient(to right, var(--accent-cyan), var(--accent-purple))', width: `${percentage}%`, height: '100%', borderRadius: '4px' }}></div>
                              </div>
                              <span style={{ fontSize: '0.85rem', textAlign: 'right', fontWeight: '600', color: 'var(--accent-cyan)' }}>{count}</span>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                </>
              )}
            </>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '300px', border: '1px dashed var(--border-muted)', borderRadius: '12px' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Select a job from the panel to track the applicant pipeline.</p>
            </div>
          )}
        </section>

      </div>
    </div>
  );
}
