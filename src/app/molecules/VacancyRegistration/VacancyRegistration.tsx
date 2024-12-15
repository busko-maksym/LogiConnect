"use client";

import React, { useState } from 'react';
import styles from './VacancyRegistration.module.css';
import Input from '@/app/atoms/Input/Input';
import Document from './img/Document.png';
import Image from 'next/image';
import Arrow from './img/Arrow.png';
import Button from '@/app/atoms/Button/Button';
import InputSelect from '@/app/atoms/InputSelect/InputSelect';
import axios from 'axios';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export default function VacancyRegistration() {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        location_from: '',
        location_to: '',
        salary_range: '',
        posted_by: '',
        created_at: new Date().toISOString(),
        requirements: [''],
        additional_info: '',
        currency: '',
        urgency: '',
    });

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState('');
    const [alertSeverity, setAlertSeverity] = useState<'success' | 'error'>('success');

    const options = [
        { value: '$', label: '$' },
        { value: '€', label: '€' },
        { value: '₴', label: '₴' },
    ];

    const handleCloseAlert = () => {
        setAlertOpen(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSelectChange = (selectedOption) => {
        setFormData({
            ...formData,
            currency: selectedOption.value,
        });
    };

    const handleRequirementsChange = (e, index) => {
        const { value } = e.target;
        const newRequirements = [...formData.requirements];
        newRequirements[index] = value;
        setFormData({
            ...formData,
            requirements: newRequirements,
        });
    };

    const handleSubmit = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://127.0.0.1:8000/vacancie/create', formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            setAlertMessage('Вакансія успішно створена!');
            setAlertSeverity('success');
            setAlertOpen(true);
        } catch (error) {
            console.error('Error creating vacancy:', error.response ? error.response.data : error.message);
            setAlertMessage('Помилка створення вакансії: ' + (error.response?.data.msg || 'Невідома помилка'));
            setAlertSeverity('error');
            setAlertOpen(true);
        }
    };

    return (
        <div className={styles.formContainer}>
            <div className={styles.logo}>
                <h1>Створення вакансій</h1>
                <h2>LogiConnect</h2>
            </div>
            <div className={styles.inputContainer}>
                <div className={styles.inputGroup}> 
                    <Input
                        size='large'
                        label='Назва вакансії'
                        placeholder='Назва вакансії'
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                    />
                    <div className={styles.inputRow}>
                        <Input
                            size='medium'
                            label='Локація звідки?'
                            placeholder='Локація звідки?'
                            name="location_from"
                            value={formData.location_from}
                            onChange={handleChange}
                        />
                        <Image src={Arrow} alt="Arrow" />
                        <Input
                            size='medium'
                            label='Локація до куди?'
                            placeholder='Локація до куди?'
                            name="location_to"
                            value={formData.location_to}
                            onChange={handleChange}
                        />
                    </div>
                    <div className={styles.inputRow}>
                        <Input
                            size='small'
                            label='≈ Зарплата'
                            placeholder='≈ Зарплата'
                            name="salary_range"
                            value={formData.salary_range}
                            onChange={handleChange}
                        />
                        <InputSelect
                            size="medium"
                            label="Вибрати валюту"
                            options={options}
                            onChange={handleSelectChange}
                        />
                    </div>
                    <div className={styles.inputRow}>
                        <Input
                            size='medium'
                            label='Терміновість'
                            placeholder='Терміновість'
                            name="urgency"
                            value={formData.urgency}
                            onChange={handleChange}
                        />
                        {formData.requirements.map((req, index) => (
                            <Input
                                key={index}
                                size='medium'
                                label={`Вимога`}
                                placeholder='Вимога'
                                value={req}
                                onChange={(e) => handleRequirementsChange(e, index)}
                            />
                        ))}
                    </div>
                    <Input
                        size='large'
                        label='Опис вакансії'
                        placeholder='Опис вакансії'
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                    />
                </div>
            </div>
            <div className={styles.text}>
                <Image src={Document} alt="Document" />
                <h3>Створення вакансії</h3>
                <p>Створіть свою вакансію для<br /> подальшої роботи. Вакансія<br /> відобразиться на головній сторінці<br /> вакансій</p>
            </div>
            <Button label='Створити вакансію' size='midlarge' onClick={handleSubmit} />

            <Snackbar
                open={alertOpen}
                autoHideDuration={8000}
                onClose={handleCloseAlert}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert
                    onClose={handleCloseAlert}
                    severity={alertSeverity}
                    variant="outlined"
                >
                    {alertMessage}
                </Alert>
            </Snackbar>
        </div>
    );
}
