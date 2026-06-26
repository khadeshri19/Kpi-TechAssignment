import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { AlertCircle, CheckCircle, User, UserPlus } from 'lucide-react';
import styles from './styles.module.css';

type AuthMode = 'signin' | 'signup';
type FieldErrors = Record<string, string>;

export const Login = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState<AuthMode>('signin');

  /* Shared state */
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
  const [errors, setErrors] = useState<FieldErrors>({});

  /* Sign-up only state */
  const [name, setName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<'candidate' | 'admin' | ''>('');

  const clearError = (key: string) => {
    if (errors[key]) {
      setErrors(prev => { const copy = { ...prev }; delete copy[key]; return copy; });
    }
  };

  const switchMode = (m: AuthMode) => {
    setMode(m);
    setErrors({});
    setMessage(null);
    // Clear shared fields to avoid stale data leaking between sign-in and sign-up forms
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setName('');
    setRole('');
  };

  /* ── Validation ── */
  const validateSignIn = (): boolean => {
    const e: FieldErrors = {};
    if (!email.trim()) e.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = 'Enter a valid email';
    if (!password) e.password = 'Password is required';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const validateSignUp = (): boolean => {
    const e: FieldErrors = {};
    if (!name.trim()) e.name = 'Username is required';
    if (!email.trim()) e.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = 'Enter a valid email';
    if (!password) e.password = 'Password is required';
    else if (password.length < 6) e.password = 'Must be at least 6 characters';
    if (!confirmPassword) e.confirmPassword = 'Please confirm your password';
    else if (password !== confirmPassword) e.confirmPassword = 'Passwords do not match';
    if (!role) e.role = 'Please select a role';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  /* ── Sign In ── */
  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateSignIn()) return;
    setLoading(true);
    setMessage(null);

    try {
      const data = await api.login({ email, password });

      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', data.role);
      localStorage.setItem('name', data.name);
      localStorage.setItem('email', data.email);

      if (data.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/candidate/profile');
      }
    } catch (err: any) {
      setMessage({ text: err.message || 'Incorrect email or password.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  /* ── Sign Up ── */
  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateSignUp()) return;
    setLoading(true);
    setMessage(null);

    try {
      await api.register({ name, email, password, role: role as 'admin' | 'candidate' });

      // Auto-login after successful registration
      const data = await api.login({ email, password });
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', data.role);
      localStorage.setItem('name', data.name);
      localStorage.setItem('email', data.email);

      if (data.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/candidate/profile');
      }
    } catch (err: any) {
      setMessage({ text: err.message || 'Registration failed. Please try again.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <Card className={styles.card} padding="lg">
        {/* Tab switcher */}
        <div className={styles.tabBar}>
          <button
            type="button"
            className={`${styles.tab} ${mode === 'signin' ? styles.tabActive : ''}`}
            onClick={() => switchMode('signin')}
          >
            <User size={15} />
            Sign In
          </button>

        </div>

        <div className={styles.header}>
          <h2>{mode === 'signin' ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{mode === 'signin' ? 'Sign in to your account' : 'Register as a Candidate or HR Admin'}</p>
        </div>

        {/* Banner message */}
        {message && (
          <div className={message.type === 'success' ? styles.successBanner : styles.errorBanner}>
            {message.type === 'success' ? <CheckCircle size={14} /> : <AlertCircle size={14} />}
            {message.text}
          </div>
        )}

        {/* ── Sign In Form ── */}
        {mode === 'signin' && (
          <form onSubmit={handleSignIn} className={styles.form}>
            <Input
              label="Email Address"
              type="email"
              value={email}
              onChange={e => { setEmail(e.target.value); clearError('email'); }}
              error={errors.email}
              placeholder="you@example.com"
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={e => { setPassword(e.target.value); clearError('password'); }}
              error={errors.password}
              placeholder="••••••••"
            />
            <Button type="submit" loading={loading} style={{ width: '100%', marginTop: 'var(--sp-2)' }}>
              Sign In
            </Button>
          </form>
        )}

        {/* ── Sign Up Form ── */}
        {mode === 'signup' && (
          <form onSubmit={handleSignUp} className={styles.form}>
            <Input
              label="Username *"
              value={name}
              onChange={e => { setName(e.target.value); clearError('name'); }}
              error={errors.name}
              placeholder="e.g. alexmorgan"
            />
            <Input
              label="Email Address *"
              type="email"
              value={email}
              onChange={e => { setEmail(e.target.value); clearError('email'); }}
              error={errors.email}
              placeholder="you@example.com"
            />
            <div className={styles.fieldRow}>
              <Input
                label="Password *"
                type="password"
                value={password}
                onChange={e => { setPassword(e.target.value); clearError('password'); }}
                error={errors.password}
                placeholder="Min. 6 characters"
              />
              <Input
                label="Confirm Password *"
                type="password"
                value={confirmPassword}
                onChange={e => { setConfirmPassword(e.target.value); clearError('confirmPassword'); }}
                error={errors.confirmPassword}
                placeholder="Re-enter password"
              />
            </div>

            {/* Role selector */}
            <div className={styles.roleSection}>
              <label className={styles.roleLabel}>I want to join as *</label>
              <div className={styles.roleOptions}>
                <button
                  type="button"
                  className={`${styles.roleCard} ${role === 'candidate' ? styles.roleCardActive : ''} ${errors.role ? styles.roleCardError : ''}`}
                  onClick={() => { setRole('candidate'); clearError('role'); }}
                >
                  <span className={styles.roleTitle}>Candidate</span>
                  <span className={styles.roleDesc}>Browse &amp; apply for jobs</span>
                </button>
                <button
                  type="button"
                  className={`${styles.roleCard} ${role === 'admin' ? styles.roleCardActive : ''} ${errors.role ? styles.roleCardError : ''}`}
                  onClick={() => { setRole('admin'); clearError('role'); }}
                >
                  <span className={styles.roleTitle}>HR Admin</span>
                  <span className={styles.roleDesc}>Post jobs &amp; manage pipeline</span>
                </button>
              </div>
              {errors.role && <span className={styles.roleError}>{errors.role}</span>}
            </div>

            <Button type="submit" loading={loading} style={{ width: '100%', marginTop: 'var(--sp-2)' }}>
              Create Account
            </Button>
          </form>
        )}

        {/* Quick switch hint */}
        <div className={styles.switchHint}>
          {mode === 'signin' ? (
            <p>Don't have an account? <button type="button" onClick={() => switchMode('signup')}>Sign up</button></p>
          ) : (
            <p>Already have an account? <button type="button" onClick={() => switchMode('signin')}>Sign in</button></p>
          )}
        </div>
      </Card>
    </div>
  );
};
