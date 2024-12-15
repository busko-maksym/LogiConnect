'use client';

import React, { useEffect, useState } from 'react';
import styles from './WorkingInfo.module.css';
import Image from 'next/image';
import { useParams } from 'next/navigation';
import Tick from './img/Vector 35.png';
import { fetchUserData } from '@/app/services/UserService';

export default function WorkingInfo() {
  const [userData, setUserData] = useState<any>(null);
  const { id } = useParams(); // Отримання ID користувача з URL

  useEffect(() => {
    if (id) {
      fetchUserData(id).then(data => setUserData(data));
    }
  }, [id]);

  if (!userData) {
    return console.log("loading"); // Можна додати loader або повідомлення про завантаження
  }


  return (
    <div className={styles.container}>
      <div className={styles.info}>
        <h1>Робоча інформація</h1>
      </div>
      <div className={styles.aboutUserExperience}>
        <h3>Досвід роботи: <strong>{userData.experience_years || 0} років</strong></h3>
        <h3>Міжнародні перевезення: <strong>{userData.has_international_permit ? 'Так' : 'Ні'}</strong></h3>
        <h3>Бажані маршрути: <strong>{userData.vehicle_types.join(', ') || 'Немає'}</strong></h3>
      </div>
      <div className={styles.userTransport}>
        <h4>Типи транспортних засобів, які <br />дозволені керувати:</h4>
        <div className={styles.transport}>
          <div className={styles.column}>
            <div className={styles.block}>
              <h1>B</h1>
            </div>
            <div className={styles.check}>
              <Image src={Tick} alt="Tick" />
            </div>
          </div>
          <div className={styles.column}>
            <div className={styles.block}>
              <h1>BE</h1>
            </div>
          </div>
          <div className={styles.blockContainer}>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>C</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>C1</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>CE</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>C1E</h1>
              </div>
            </div>
          </div>

          <div className={styles.secondBlockContainer}>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>D</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>D1</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>DE</h1>
              </div>
            </div>
            <div className={styles.column}>
              <div className={styles.block}>
                <h1>D1E</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
