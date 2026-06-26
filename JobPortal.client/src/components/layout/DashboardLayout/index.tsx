import React from 'react';
import styles from './styles.module.css';

export const DashboardLayout: React.FC<{ children: React.ReactNode; title: string; action?: React.ReactNode }> = ({ children, title, action }) => {
  return (
    <div className={styles.layout}>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>{title}</h1>
          {action && <div>{action}</div>}
        </div>
        <div className={styles.content}>
          {children}
        </div>
      </div>
    </div>
  );
};
