import React from 'react';
import styles from './styles.module.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md';
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  children,
  className,
  ...props
}) => (
  <button
    className={`${styles.btn} ${styles[variant]} ${styles[size]} ${className || ''}`}
    disabled={disabled || loading}
    {...props}
  >
    {loading ? <span className={styles.spinner} /> : children}
  </button>
);
