import React from 'react';
import styles from './styles.module.css';

export const Footer: React.FC = () => (
  <footer className={styles.footer}>
    <p>&copy; {new Date().getFullYear()} JobBoard. All rights reserved.</p>
  </footer>
);
