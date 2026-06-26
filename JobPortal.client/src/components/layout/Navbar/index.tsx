import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LogOut, User } from 'lucide-react';
import { api } from '../../../services/api';
import styles from './styles.module.css';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  const [avatar, setAvatar] = useState<string | null>(localStorage.getItem('avatar'));
  const fetchedRef = useRef(false);

  useEffect(() => {
    const handleAvatarUpdate = (e: Event) => {
      const customEvent = e as CustomEvent;
      setAvatar(customEvent.detail);
    };

    window.addEventListener('avatar-updated', handleAvatarUpdate);

    // Only fetch profile once, and only if we don't already have a cached avatar
    if (token && role === 'candidate' && !avatar && !fetchedRef.current) {
      fetchedRef.current = true;
      api.getProfile()
        .then((data) => {
          if (data.avatar) {
            localStorage.setItem('avatar', data.avatar);
            setAvatar(data.avatar);
          }
        })
        .catch(() => {});
    }

    return () => {
      window.removeEventListener('avatar-updated', handleAvatarUpdate);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('avatar');
    localStorage.removeItem('name');
    localStorage.removeItem('email');
    setAvatar(null);
    navigate('/login');
  };

  return (
    <header className={styles.navbar}>
      <div className={styles.inner}>
        <Link to="/" className={styles.logo}>
          Job<span>Board</span>
        </Link>

        {token && (
          <div className={styles.right}>
            <span className={styles.role}>{role === 'admin' ? 'Admin' : 'Candidate'}</span>
            <button className={styles.logoutBtn} onClick={handleLogout}>
              <LogOut size={14} />
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
