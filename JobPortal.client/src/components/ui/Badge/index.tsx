import React from 'react';
import styles from './styles.module.css';

interface BadgeProps {
  variant?: 'success' | 'warning' | 'danger' | 'neutral';
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'neutral', children }) => (
  <span className={`${styles.badge} ${styles[variant]}`}>{children}</span>
);
