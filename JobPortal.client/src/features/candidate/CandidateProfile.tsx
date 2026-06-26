import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { CandidateProfile as ProfileType, CandidateProfileCreate } from '../../types';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Textarea } from '../../components/ui/Textarea';
import { Button } from '../../components/ui/Button';
import { User, Camera, X, CheckCircle, AlertCircle } from 'lucide-react';
import styles from './styles.module.css';

/**
 * Safely joins an array-like value into a comma-separated string.
 * Handles edge cases where the backend may return a flat string instead of an array.
 */
function safeJoin(value: unknown): string {
  if (Array.isArray(value)) return value.join(', ');
  if (typeof value === 'string') return value;
  return '';
}

type FieldErrors = Record<string, string>;

export const CandidateProfile = () => {
  const [fullName, setFullName] = useState(localStorage.getItem('name') || '');
  const [profile, setProfile] = useState({
    skills: '',
    education: '',
    project_summaries: '',
    avatar: '',
    preferences: { locations: '', desired_roles: '', experience_level: '' }
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ text: string, type: 'success' | 'error' } | null>(null);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    api.getProfile().then(data => {
      setProfile({
        skills: safeJoin(data.skills),
        education: data.education || '',
        project_summaries: data.project_summaries || '',
        avatar: data.avatar || '',
        preferences: {
          locations: safeJoin(data.preferences?.locations),
          desired_roles: safeJoin(data.preferences?.desired_roles),
          experience_level: data.preferences?.experience_level || ''
        }
      });
      // Update name from profile if available
      if (data.name) {
        setFullName(data.name);
        localStorage.setItem('name', data.name);
      }
    }).catch(() => { /* normal if new user */ });
  }, []);

  /* ── Validation ── */
  const validate = (): boolean => {
    const e: FieldErrors = {};
    if (!fullName.trim()) e.fullName = 'Full name is required';
    if (!profile.skills.trim()) e.skills = 'At least one skill is required';
    if (!profile.education.trim()) e.education = 'Education is required';
    if (!profile.preferences.locations.trim()) e.locations = 'At least one preferred location is required';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  /** Clears a single field error when the user starts typing */
  const clearError = (key: string) => {
    if (errors[key]) {
      setErrors(prev => { const copy = { ...prev }; delete copy[key]; return copy; });
    }
  };

  /* ── Image handling ── */
  const processImage = (file: File) => {
    if (file.size > 200 * 1024) {
      setMessage({ text: 'File size must be under 200 KB.', type: 'error' });
      return;
    }
    if (!file.type.startsWith('image/')) {
      setMessage({ text: 'Only image files are accepted.', type: 'error' });
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const MAX = 200;
        let w = img.width, h = img.height;
        if (w > h) { if (w > MAX) { h *= MAX / w; w = MAX; } }
        else { if (h > MAX) { w *= MAX / h; h = MAX; } }
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(img, 0, 0, w, h);
          setProfile(prev => ({ ...prev, avatar: canvas.toDataURL('image/jpeg', 0.85) }));
        }
      };
      img.src = event.target?.result as string;
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) processImage(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) processImage(file);
  };

  /* ── Submit ── */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setMessage(null);

    const payload: CandidateProfileCreate = {
      user_id: '00000000-0000-0000-0000-000000000000',
      name: fullName,
      skills: profile.skills.split(',').map(s => s.trim()).filter(Boolean),
      education: profile.education,
      project_summaries: profile.project_summaries,
      avatar: profile.avatar,
      preferences: {
        desired_roles: profile.preferences.desired_roles.split(',').map(s => s.trim()).filter(Boolean),
        locations: profile.preferences.locations.split(',').map(s => s.trim()).filter(Boolean),
        experience_level: profile.preferences.experience_level
      }
    };

    try {
      const savedProfile = await api.upsertProfile(payload);
      if (savedProfile.avatar) {
        localStorage.setItem('avatar', savedProfile.avatar);
      } else {
        localStorage.removeItem('avatar');
      }
      if (savedProfile.name) {
        localStorage.setItem('name', savedProfile.name);
      }
      window.dispatchEvent(new CustomEvent('avatar-updated', { detail: savedProfile.avatar || null }));
      setMessage({ text: 'Profile saved successfully.', type: 'success' });
    } catch (err: any) {
      setMessage({ text: err.message, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  /* ── Render ── */
  return (
    <DashboardLayout title="Complete Your Profile" action={<span className={styles.profileSubtitle}>Manage your personal information and preferences</span>}>
      {message && (
        <div className={message.type === 'success' ? styles.msgSuccess : styles.msgError}>
          {message.type === 'success' ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles.profileForm}>
        {/* ── Section 1: Personal Information ── */}
        <Card className={styles.profileSection}>
          <div className={styles.sectionHeader}>
            <h3>Personal Information</h3>
            <p>Update your photo and personal details</p>
          </div>

          {/* Avatar row */}
          <div className={styles.avatarRow}>
            <div className={styles.avatarPreviewContainer}>
              {profile.avatar ? (
                <img src={profile.avatar} alt="Avatar" className={styles.avatarPreview} />
              ) : (
                <div className={styles.avatarPreviewPlaceholder}>
                  <User size={36} />
                </div>
              )}
            </div>

            <div
              className={`${styles.dropZone} ${isDragging ? styles.dropZoneActive : ''}`}
              onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => document.getElementById('avatar-upload')?.click()}
            >
              <Camera size={20} className={styles.dropZoneIcon} />
              <span className={styles.dropZoneLabel}>Click to upload or drag and drop</span>
              <span className={styles.dropZoneHint}>PNG, JPG or GIF (max. 200×200px, 200KB)</span>
              <input
                id="avatar-upload"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
            </div>

            {profile.avatar && (
              <button
                type="button"
                className={styles.removeAvatarBtn}
                onClick={() => setProfile(prev => ({ ...prev, avatar: '' }))}
                title="Remove photo"
              >
                <X size={14} />
              </button>
            )}
          </div>

          {/* Full Name */}
          <div className={styles.fieldRow}>
            <Input
              label="Username / Full Name *"
              value={fullName}
              onChange={e => { setFullName(e.target.value); clearError('fullName'); }}
              error={errors.fullName}
              placeholder="e.g. Alex Morgan"
            />
          </div>
        </Card>

        {/* ── Section 2: Professional Details ── */}
        <Card className={styles.profileSection}>
          <div className={styles.sectionHeader}>
            <h3>Professional Details</h3>
            <p>Skills, education, and project experience</p>
          </div>

          <div className={styles.fieldRow}>
            <Input
              label="Skills (comma separated) *"
              value={profile.skills}
              onChange={e => { setProfile({ ...profile, skills: e.target.value }); clearError('skills'); }}
              error={errors.skills}
              placeholder="e.g. React, TypeScript, Python, SQL"
            />
            {profile.skills.trim() && (
              <div className={styles.tagPreviewContainer}>
                {profile.skills.split(',').map(s => s.trim()).filter(Boolean).map((tag, idx) => (
                  <span key={idx} className={styles.badgeTag}>{tag}</span>
                ))}
              </div>
            )}
          </div>

          <div className={styles.fieldRow}>
            <Input
              label="Education *"
              value={profile.education}
              onChange={e => { setProfile({ ...profile, education: e.target.value }); clearError('education'); }}
              error={errors.education}
              placeholder="e.g. B.Tech in Computer Science"
            />
            {profile.education.trim() && (
              <div className={styles.tagPreviewContainer}>
                {profile.education.split(',').map(e => e.trim()).filter(Boolean).map((tag, idx) => (
                  <span key={idx} className={styles.badgeTag}>{tag}</span>
                ))}
              </div>
            )}
          </div>

          <Textarea
            label="Project Summaries"
            value={profile.project_summaries}
            onChange={e => setProfile({ ...profile, project_summaries: e.target.value })}
            placeholder="Describe your key projects and accomplishments..."
            rows={4}
          />
        </Card>

        {/* ── Section 3: Preferences ── */}
        <Card className={styles.profileSection}>
          <div className={styles.sectionHeader}>
            <h3>Preferences</h3>
            <p>Your job search preferences help us find better matches</p>
          </div>

          <div className={styles.prefGrid}>
            <div className={styles.fieldRow}>
              <Input
                label="Preferred Locations *"
                value={profile.preferences.locations}
                onChange={e => { setProfile({ ...profile, preferences: { ...profile.preferences, locations: e.target.value } }); clearError('locations'); }}
                error={errors.locations}
                placeholder="e.g. Pune, New York, Remote"
              />
              {profile.preferences.locations.trim() && (
                <div className={styles.tagPreviewContainer}>
                  {profile.preferences.locations.split(',').map(l => l.trim()).filter(Boolean).map((tag, idx) => (
                    <span key={idx} className={styles.badgeTag}>{tag}</span>
                  ))}
                </div>
              )}
            </div>
            <Input
              label="Desired Roles"
              value={profile.preferences.desired_roles}
              onChange={e => setProfile({ ...profile, preferences: { ...profile.preferences, desired_roles: e.target.value } })}
              placeholder="e.g. Fullstack, Software Engineer"
            />
          </div>
          <Input
            label="Experience Level"
            value={profile.preferences.experience_level}
            onChange={e => setProfile({ ...profile, preferences: { ...profile.preferences, experience_level: e.target.value } })}
            placeholder="e.g. Mid Level, Senior, Fresher"
          />
        </Card>

        {/* ── Actions ── */}
        <div className={styles.formActions}>
          <Button type="submit" loading={loading}>Save Changes</Button>
        </div>
      </form>
    </DashboardLayout>
  );
};
