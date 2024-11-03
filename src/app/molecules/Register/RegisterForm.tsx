
"use client";

import React, { useState } from 'react';
import styles from './RegisterForm.module.css';
import Direction from '@/app/atoms/Direction/Direction';
import Truck from './img/Semi Truck.png';
import Edit from './img/Edit Property.png';
import Skyscrapers from './img/Skyscrapers.png';
import House from './img/Organization.png';
import Image from 'next/image';
import Contacts from './img/Contacts.png';
import BuisnessOwner from './components/versions/BuisnessOwner/BuisnessOwner';
import TruckDriver from './components/versions/TruckDriver/TruckDriver';
import TransportationOwner from './components/versions/TransportationOwner/TransportationOwner';

export default function RegisterForm() {
  const [selectedDirection, setSelectedDirection] = useState<string | null>(null);

  const handleSelect = (direction: string) => {
    setSelectedDirection(direction);
  };

  const renderVersion = () => {
    switch (selectedDirection) {
      case 'Власник бізнесу':
        return <BuisnessOwner />;
      case 'Логіст':
        return null;
      case 'Далекобійник':
        return <TruckDriver />;
      case 'Власник транспортних компаній':
        return <TransportationOwner />
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.Text}>
        <h1>Крок №1</h1>
      </div>
      <div className={styles.About}>
        <Image src={Contacts} alt="Contacts" />
        <h3>Створення<br /> облікового запису</h3>
        <p>Для початку роботи нам потрібна<br /> деяка основна інформація</p>
      </div>
      <div className={styles.direction}>
        <h2>Виберіть своє направлення</h2>
        <p>
          Виберіть своє направлення для створення нового облікового<br /> запису та
          зручної співпраці з нами
        </p>
        <div className={styles.direction_choose}>
          <Direction 
            icon={Truck}
            title="Далекобійник"
            selected={selectedDirection === 'Далекобійник'}
            onClick={() => handleSelect('Далекобійник')}
          />
          <Direction 
            icon={Edit}
            title="Логіст"
            selected={selectedDirection === 'Логіст'}
            onClick={() => handleSelect('Логіст')}
          />
          <Direction 
            icon={House}
            title="Власник бізнесу"
            selected={selectedDirection === 'Власник бізнесу'}
            onClick={() => handleSelect('Власник бізнесу')}
          />
          <Direction 
            icon={Skyscrapers}
            title="Власник транспортних компаній"
            selected={selectedDirection === 'Власник транспортних компаній'}
            onClick={() => handleSelect('Власник транспортних компаній')}
          />
        </div>
      </div>
      <div className={styles.version}>
        {renderVersion()}
      </div>
    </div>
  );
}