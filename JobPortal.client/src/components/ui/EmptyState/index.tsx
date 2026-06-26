import React from 'react';
import styles from './styles.module.css';

interface EmptyStateProps {
  title: string;
  description?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ title, description }) => (
  <div className={styles.empty}>
    <p className={styles.title}>{title}</p>
    {description && <p className={styles.description}>{description}</p>}
  </div>
);
