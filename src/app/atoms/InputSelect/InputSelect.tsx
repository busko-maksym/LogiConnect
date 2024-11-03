"use client";

import React, { useState } from 'react';
import styles from './InputSelect.module.css';

interface Option {
    value: string;
    label: string;
}

interface InputSelectProps {
    label: string;
    options: Option[];
    size?: 'small' | 'medium' | 'large';
    onChange?: (value: string) => void;
}

const InputSelect: React.FC<InputSelectProps> = ({ label, options, size = 'medium', onChange }) => {
    const [selectedOption, setSelectedOption] = useState('');

    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = e.target.value;
        setSelectedOption(value);

        if (onChange) {
            onChange(value);
        }
    };

    const selectClassNames = `${styles.select} ${styles[size]}`;

    return (
        <div className={`${styles.inputSelectContainer} ${styles[size]}`}>
            <select value={selectedOption} onChange={handleSelectChange} className={selectClassNames}>
                <option value="">$</option>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default InputSelect;
