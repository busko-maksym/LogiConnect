'use client'

import React, { useEffect, useState } from 'react';
import styles from './userInfo.module.css';
import Button from '@/app/atoms/Button/Button';
import { fetchUserData } from '@/app/services/UserService';
import { useParams } from 'next/navigation';

export default function UserInfo() {
  const { id } = useParams(); // Отримуємо ID користувача з URL
  const [userData, setUserData] = useState<any>(null);

  useEffect(() => {
    if (id) {
      fetchUserData(id).then(data => setUserData(data));
    }
  }, [id]);

  if (!userData) {
    return <div>Loading...</div>;
  }

  let accountStatus = userData.acc_status;
  if (accountStatus === 'driver') {
    accountStatus = 'Далекобійник';
  }

  return (
    <div className={styles.container}>
      <div className={styles.info}>
        <h1>Особисті дані</h1>
        <Button size="sykaBlyatAndriyNahui" />
      </div>
      <div className={styles.userInfo}>
        <div className={styles.userRating}>
          <h2>Рейтинг:</h2>
        </div>
        <h3>Професія: <strong>{accountStatus}</strong></h3>
        <h3>Ім’я: <strong>{userData.first_name}</strong></h3>
        <h3>Прізвище: <strong>{userData.last_name}</strong></h3>
        <div className={styles.row}>
          <h3>Ел. пошта: <strong>{userData.email}</strong></h3>
          <h4>Посилання: <strong>{userData.driver_license_number}</strong></h4>
        </div>
      </div>
    </div>
  );
}
