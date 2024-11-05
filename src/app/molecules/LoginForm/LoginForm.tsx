"use client"

import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; 
import axios from 'axios';
import styles from './LoginForm.module.css';
import Input from '@/app/atoms/Input/Input';
import Button from '@/app/atoms/Button/Button';
import bcrypt from 'bcryptjs'

const LoginForm = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const hashedPassword = bcrypt.hashSync(password, 10);
    setError('');
    setMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/user/login', {
        email: email,
        password: hashedPassword,
      });

      const token = response.data.cookie;
      localStorage.setItem('token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      setMessage(response.data.msg);
      
    } catch (error) {
      if (error.response) {
        setError(error.response.data.msg || 'Помилка логіну');
      } else {
        setError('Помилка під час входу');
      }
    }
  };

  const handleForgotPassword = () => {
    router.push('/password-reset'); // Зміна шляху на вашу сторінку скидання пароля
  };

  return (
    <div className={styles.container}>
      <h3>UA | EN</h3>
      <div className={styles.logo}>
        <h1>Вхід</h1>
        <h2>LogiConnect</h2>
      </div>
      <div className={styles.loginContainer}>
        <h1>Ласкаво просимо в LogiConnect!</h1>
        <p>Будь ласка, введіть дані для входу у <br /> ваш обліковий запис</p>
        <div className={styles.inputContainer}>
          <Input
            label="Електронна пошта"
            placeholder="Електронна пошта"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            label="Пароль"
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p className={styles.error}>{error}</p>}
        {message && <p className={styles.success}>{message}</p>}
        <a href="#" onClick={handleForgotPassword}>Забули пароль?</a>
        <Button
          label="Далі"
          variant="secondary"
          onClick={handleLogin}
        />
      </div>
    </div>
  );
};

export default LoginForm;
