"use client";

import React, { useState } from 'react';
import axios from 'axios';
import styles from './PasswordResetForm.module.css';
import Input from '@/app/atoms/Input/Input';
import Button from '@/app/atoms/Button/Button';

export default function PasswordResetForm() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await axios.post(`http://127.0.0.1:8000/user/password/reset?email=${encodeURIComponent(email)}`);

      setMessage(response.data.msg || 'Запит на скидання пароля надіслано.');
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setError(error.response.data.msg || 'Помилка при надсиланні запиту на скидання пароля.');
      } else {
        setError('Помилка сервера. Спробуйте ще раз.');
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.Logo}>
        <h1>Вхід</h1>
        <h2>LogiConnect</h2>
      </div>
      <div className={styles.formContainer}>
        <h3>Відновлення паролю</h3>
        <p>Будь ласка, введіть свою електронну пошту для відновлення паролю до свого облікового запису</p>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <Input 
              label="Електронна пошта"
              type="email"
              placeholder="Електронна пошта"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <Button variant='secondary' label='Далі' />
        </form>
        {message && <p className={styles.success}>{message}</p>}
        {error && <p className={styles.error}>{error}</p>}
      </div>
    </div>
  );
}
