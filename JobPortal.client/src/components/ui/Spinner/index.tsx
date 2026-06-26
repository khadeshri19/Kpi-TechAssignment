import React from 'react';
import styles from './styles.module.css';

export const Spinner: React.FC<{ size?: number }> = ({ size = 24 }) => (
  <div className={styles.wrapper}>
    <div className={styles.spinner} style={{ width: size, height: size }} />
  </div>
);
