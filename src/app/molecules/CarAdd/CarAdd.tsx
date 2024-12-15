'use client'

import React, { useState } from 'react';
import UserHeader from '../user_header/userHeader';
import styles from './CarAdd.module.css';
import Input from '@/app/atoms/Input/Input';
import Button from '@/app/atoms/Button/Button';
import truck from './img/Icon.png';
import Image from 'next/image';
import axios from 'axios';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export default function CarAdd() {
  const [waste, setWaste] = useState('');
  const [maxVolume, setMaxVolume] = useState('');
  const [maxWeight, setMaxWeight] = useState('');
  const [fridge, setFridge] = useState(false);
  const [alertOpen, setAlertOpen] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [alertSeverity, setAlertSeverity] = useState<'success' | 'error' | 'warning' | 'info'>('success');

  const handleCloseAlert = () => {
    setAlertOpen(false);
  };

  const handleSubmit = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setAlertMessage('Пользователь не авторизован');
      setAlertSeverity('error');
      setAlertOpen(true);
      return;
    }

    const data = {
      waste: Number(waste),
      max_volume: Number(maxVolume),
      max_weight: Number(maxWeight),
      fridge,
    };

    try {
      const response = await axios.post(
        'http://localhost:8000/user/car',
        data,
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAlertMessage('Автомобиль успешно добавлен!');
      setAlertSeverity('success');
      setAlertOpen(true);
    } catch (error) {
      setAlertMessage('Ошибка при добавлении автомобиля');
      setAlertSeverity('error');
      setAlertOpen(true);
    }
  };

  return (
    <div className={styles.container}>
      <UserHeader />
      <div className={styles.inputContainer}>
        <Input
          size="large"
          label="Розхід"
          placeholder="Розхід"
          value={waste}
          onChange={(e) => setWaste(e.target.value)}
        />
        <Input
          size="large"
          label="Максимальний об'єм"
          placeholder="Максимальний об'єм"
          value={maxVolume}
          onChange={(e) => setMaxVolume(e.target.value)}
        />
        <Input
          size="large"
          label="Максимальна вага"
          placeholder="Максимальна вага"
          value={maxWeight}
          onChange={(e) => setMaxWeight(e.target.value)}
        />
        <div className={styles.checkbox}>
          <span>Холодильник</span>
          <input
            type="checkbox"
            checked={fridge}
            onChange={(e) => setFridge(e.target.checked)}
          />
        </div>
      </div>
      <div className={styles.text}>
        <Image src={truck} alt="truck" />
        <h3>Створення вакансії</h3>
        <p>
          Створіть свою вакансію для
          <br /> подальшої роботи. Вакансія
          <br /> відобразиться на головній сторінці
          <br /> вакансій
        </p>
      </div>
      <Button label="Створити вакансію" size="midlarge" onClick={handleSubmit} />

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
