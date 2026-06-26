import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { Job, JobFilters } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Table } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Modal } from '../../components/ui/Modal';
import { JobForm } from './JobForm';
import styles from './styles.module.css';

export const JobList = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filters, setFilters] = useState<JobFilters>({});
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingJob, setEditingJob] = useState<Job | undefined>();
  const navigate = useNavigate();

  const loadJobs = () => {
    setLoading(true);
    api.getJobs(filters)
      .then(setJobs)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadJobs();
  }, [filters]);

  const handleCreateOrUpdate = async (data: any) => {
    if (editingJob) {
      await api.updateJob(editingJob.id, data);
    } else {
      await api.createJob(data);
    }
    setIsModalOpen(false);
    loadJobs();
  };

  const openCreateModal = () => {
    setEditingJob(undefined);
    setIsModalOpen(true);
  };

  const columns = [
    { key: 'title', header: 'Title' },
    { key: 'location', header: 'Location' },
    { key: 'experience_level', header: 'Experience' },
    { 
      key: 'status', 
      header: 'Status',
      render: (job: Job) => <Badge variant={job.status === 'open' ? 'success' : 'neutral'}>{job.status}</Badge> 
    },
    {
      key: 'actions',
      header: '',
      render: (job: Job) => (
        <div style={{ display: 'flex', gap: 'var(--sp-2)', justifyContent: 'flex-end' }}>
          <Button variant="ghost" size="sm" onClick={(e) => { e.stopPropagation(); setEditingJob(job); setIsModalOpen(true); }}>Edit</Button>
          <Button variant="secondary" size="sm" onClick={() => navigate(`/admin/jobs/${job.id}/pipeline`)}>Pipeline</Button>
        </div>
      )
    }
  ];

  return (
    <DashboardLayout 
      title="Job Listings" 
      action={<Button onClick={openCreateModal}>Create Job</Button>}
    >
      <div className={styles.filters}>
        <Input placeholder="Filter by skill..." onChange={e => setFilters(f => ({ ...f, skill: e.target.value }))} />
        <Input placeholder="Filter by location..." onChange={e => setFilters(f => ({ ...f, location: e.target.value }))} />
        <Input placeholder="Filter by experience..." onChange={e => setFilters(f => ({ ...f, experience_level: e.target.value }))} />
      </div>

      <Table 
        data={jobs} 
        columns={columns} 
        keyExtractor={j => j.id} 
        onRowClick={j => navigate(`/admin/jobs/${j.id}/pipeline`)} 
      />

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingJob ? "Edit Job" : "Create Job"}>
        <JobForm initialData={editingJob} onSubmit={handleCreateOrUpdate} onCancel={() => setIsModalOpen(false)} />
      </Modal>
    </DashboardLayout>
  );
};
