import React, { useState, useEffect } from 'react';
import { Job, JobCreate, JobUpdate } from '../../types';
import { Input } from '../../components/ui/Input';
import { Textarea } from '../../components/ui/Textarea';
import { Select } from '../../components/ui/Select';
import { Button } from '../../components/ui/Button';

interface JobFormProps {
  initialData?: Job;
  onSubmit: (data: JobCreate | JobUpdate) => Promise<void>;
  onCancel: () => void;
}

export const JobForm: React.FC<JobFormProps> = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: initialData?.title || '',
    description: initialData?.description || '',
    required_skills: (initialData?.required_skills || []).join(', '),
    experience_level: initialData?.experience_level || '',
    location: initialData?.location || '',
    status: initialData?.status || 'open'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reset form whenever the job being edited changes (e.g. switching from create → edit)
  useEffect(() => {
    setFormData({
      title: initialData?.title || '',
      description: initialData?.description || '',
      required_skills: (initialData?.required_skills || []).join(', '),
      experience_level: initialData?.experience_level || '',
      location: initialData?.location || '',
      status: initialData?.status || 'open',
    });
    setError(null);
  }, [initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await onSubmit({
        ...formData,
        required_skills: formData.required_skills.split(',').map(s => s.trim()).filter(Boolean)
      } as JobCreate | JobUpdate);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--sp-4)' }}>
      {error && <div style={{ color: 'var(--danger)', fontSize: 'var(--fs-sm)' }}>{error}</div>}
      <Input label="Title" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} required minLength={2} />
      <Textarea label="Description" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} required minLength={10} rows={5} />
      <Input label="Required Skills (comma separated)" value={formData.required_skills} onChange={e => setFormData({...formData, required_skills: e.target.value})} />
      <Input label="Experience Level" value={formData.experience_level} onChange={e => setFormData({...formData, experience_level: e.target.value})} required />
      <Input label="Location" value={formData.location} onChange={e => setFormData({...formData, location: e.target.value})} required />
      {initialData && (
        <Select
          label="Status"
          value={formData.status}
          onChange={e => setFormData({...formData, status: e.target.value as any})}
          options={[{ value: 'open', label: 'Open' }, { value: 'closed', label: 'Closed' }]}
        />
      )}
      <div style={{ display: 'flex', gap: 'var(--sp-2)', marginTop: 'var(--sp-4)', justifyContent: 'flex-end' }}>
        <Button variant="ghost" type="button" onClick={onCancel} disabled={loading}>Cancel</Button>
        <Button type="submit" loading={loading}>Save Job</Button>
      </div>
    </form>
  );
};
