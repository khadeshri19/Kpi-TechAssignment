import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Login } from '../features/auth/Login';
import { ProtectedRoute } from '../components/common/ProtectedRoute';
import { User } from 'lucide-react';
import { api } from '../services/api';

// Admin
import { Overview } from '../features/admin/Overview';
import { JobList } from '../features/admin/JobList';
import { ApplicationPipeline } from '../features/admin/ApplicationPipeline';

// Candidate
import { JobBrowser } from '../features/candidate/JobBrowser';
import { CandidateProfile } from '../features/candidate/CandidateProfile';
import { AISearch } from '../features/candidate/AISearch';

const AdminNav = () => {
  const loc = useLocation();
  return (
    <div className="subnav">
      <div className="subnav-container">
        <div className="subnav-links">
          <Link to="/admin" className="subnav-link" style={{ color: loc.pathname === '/admin' ? 'var(--accent)' : 'var(--text-secondary)', fontWeight: loc.pathname === '/admin' ? 600 : 400 }}>Overview</Link>
          <Link to="/admin/jobs" className="subnav-link" style={{ color: loc.pathname.startsWith('/admin/jobs') ? 'var(--accent)' : 'var(--text-secondary)', fontWeight: loc.pathname.startsWith('/admin/jobs') ? 600 : 400 }}>Jobs & Pipeline</Link>
        </div>
      </div>
    </div>
  );
};

const CandidateNav = () => {
  const loc = useLocation();
  const [avatar, setAvatar] = useState<string | null>(localStorage.getItem('avatar'));
  const [name, setName] = useState<string | null>(localStorage.getItem('name'));

  useEffect(() => {
    const handleAvatarUpdate = (e: Event) => {
      const customEvent = e as CustomEvent;
      setAvatar(customEvent.detail);
    };

    window.addEventListener('avatar-updated', handleAvatarUpdate);

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (token && role === 'candidate') {
      api.getProfile()
        .then((data) => {
          if (data.avatar) {
            localStorage.setItem('avatar', data.avatar);
            setAvatar(data.avatar);
          }
          if (data.name) {
            localStorage.setItem('name', data.name);
            setName(data.name);
          }
        })
        .catch(() => {});
    }

    return () => {
      window.removeEventListener('avatar-updated', handleAvatarUpdate);
    };
  }, []);

  const isActive = (path: string) => loc.pathname === path;

  return (
    <div className="subnav">
      <div className="subnav-container">
        <div className="subnav-links">
          <Link to="/candidate" className="subnav-link" style={{ color: isActive('/candidate') ? 'var(--accent)' : 'var(--text-secondary)', fontWeight: isActive('/candidate') ? 600 : 400 }}>Browse Jobs</Link>
          <Link to="/candidate/search" className="subnav-link" style={{ color: isActive('/candidate/search') ? 'var(--accent)' : 'var(--text-secondary)', fontWeight: isActive('/candidate/search') ? 600 : 400 }}>AI Matcher</Link>
          <Link to="/candidate/profile" className="subnav-link" style={{ color: isActive('/candidate/profile') ? 'var(--accent)' : 'var(--text-secondary)', fontWeight: isActive('/candidate/profile') ? 600 : 400 }}>My Profile</Link>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--sp-2)' }}>
          <span style={{ fontSize: 'var(--fs-sm)', fontWeight: 'var(--fw-medium)', color: 'var(--text-secondary)' }}>
            {name || 'Candidate'}
          </span>
          <Link
            to="/candidate/profile"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              border: '2px solid var(--border)',
              overflow: 'hidden',
              cursor: 'pointer',
              transition: 'border-color var(--transition), transform var(--transition)'
            }}
            title="My Profile"
          >
            {avatar ? (
              <img src={avatar} alt="Profile" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', height: '100%', background: 'var(--surface)', color: 'var(--text-secondary)' }}>
                <User size={16} />
              </div>
            )}
          </Link>
        </div>
      </div>
    </div>
  );
};

export const App = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Routes>
        <Route path="/admin/*" element={<AdminNav />} />
        <Route path="/candidate/*" element={<CandidateNav />} />
      </Routes>
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />

          {/* Admin Routes */}
          <Route path="/admin" element={<ProtectedRoute allowedRole="admin"><Overview /></ProtectedRoute>} />
          <Route path="/admin/jobs" element={<ProtectedRoute allowedRole="admin"><JobList /></ProtectedRoute>} />
          <Route path="/admin/jobs/:id/pipeline" element={<ProtectedRoute allowedRole="admin"><ApplicationPipeline /></ProtectedRoute>} />

          {/* Candidate Routes */}
          <Route path="/candidate" element={<ProtectedRoute allowedRole="candidate"><JobBrowser /></ProtectedRoute>} />
          <Route path="/candidate/search" element={<ProtectedRoute allowedRole="candidate"><AISearch /></ProtectedRoute>} />
          <Route path="/candidate/profile" element={<ProtectedRoute allowedRole="candidate"><CandidateProfile /></ProtectedRoute>} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
};
