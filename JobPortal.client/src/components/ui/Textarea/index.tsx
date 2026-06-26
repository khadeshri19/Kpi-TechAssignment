import React from 'react';
import styles from './styles.module.css';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea: React.FC<TextareaProps> = ({ label, error, id, ...props }) => {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
  return (
    <div className={styles.field}>
      {label && <label htmlFor={inputId} className={styles.label}>{label}</label>}
      <textarea id={inputId} className={`${styles.textarea} ${error ? styles.textareaError : ''}`} {...props} />
      {error && <span className={styles.error}>{error}</span>}
    </div>
  );
};
