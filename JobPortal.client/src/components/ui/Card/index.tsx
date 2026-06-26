import React from 'react';
import styles from './styles.module.css';

interface CardProps {
  children: React.ReactNode;
  padding?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, padding = 'md', className }) => (
  <div className={`${styles.card} ${styles[padding]} ${className || ''}`}>{children}</div>
);
