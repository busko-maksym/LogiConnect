"use client"

import Button from '@/app/atoms/Button/Button'
import React from 'react'
import WelcomeLogo from "./img/welcomePng.png"
import styles from "./Welcome.module.css"
import Image from 'next/image'

export default function Welcome() {
    const handleClick = () => {
        alert('Button Clicked!') 
    };
  return (
    <div className={styles.container}>
      <div className={styles.itemContainer}>
        <h1>Ласкаво просимо до LogiConnect!</h1>
        <h2>З'єднуємо світ логістики</h2>
        <h3>Приєднуйтесь до LogiConnect і оптимізуйте свої логістичні<br /> процеси вже сьогодні!</h3>
        <Button
        label="Створити акаунт"
        onClick={handleClick}
        variant='primary'
        size='large'
        ></Button>
        </div>
        <Image src={WelcomeLogo} alt="WelcomeLogo" />
    </div>
  )
}
