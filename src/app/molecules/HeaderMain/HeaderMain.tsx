"use client";

import React, { useEffect, useState } from 'react';
import styles from './HeaderMain.module.css';
import Button from '@/app/atoms/Button/Button';
import { useRouter } from 'next/navigation';

export default function Header() {
  const router = useRouter();
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 25) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleLoginClick = () => {
    router.push('/login')
  }

  const handleRegisterClick = () => {
    router.push('/register')
 };

  return (
    <div className={`${styles.container} ${isScrolled ? styles.scrolled : ''}`}>
      <div className={styles.container_items}>
        <h1>LogiConnect</h1>
        <div className={styles.authVariant}>
          <button onClick={handleLoginClick}>Я вже знайомий</button>
          <Button
            label="Почати"
            onClick={handleRegisterClick}
            variant='primary'
            size='medium'
          />
        </div>
      </div>
    </div>
  );
}
