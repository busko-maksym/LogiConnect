import React from 'react';
import styles from './Input.module.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    placeholder?: string; 
    size?: 'small' | 'medium' | 'large' | 'big';
}

const Input: React.FC<InputProps> = ({ label, placeholder, size = 'medium', ...props }) => {
    const classNames = `${styles.input} ${styles[size]}`;

    return (
        <div className={`${styles.inputContainer} ${styles[size]}`}>
            <input className={classNames} placeholder={placeholder} {...props} />
            <label className={styles.label}>{label}</label>
        </div>
    );
};


export default Input;
