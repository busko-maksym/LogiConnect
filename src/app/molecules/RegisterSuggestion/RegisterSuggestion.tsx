"use client"

import React from 'react'
import styles from './RegisterSuggestion.module.css'
import Image from 'next/image'
import Photo from './img/Photo.png'
import Arrow from './img/Arrow.png'
import Idea from './img/Idea.png'
import Button from '@/app/atoms/Button/Button'
import { useRouter } from 'next/navigation'


export default function RegisterSuggestion() {
    const router = useRouter();
    const handleClick = () => {
        router.push('/register')
      };
  return (
    <div className={styles.container}>
      <Image src={Photo} className={styles.Photo} alt='Photo' />
      <div className={styles.itemsContainer}>
        <Image src={Idea} className={styles.idea} alt='Idea' />
        <h1>Приєднуйтесь до LogiConnect!</h1>
        <h2>Скористайтеся можливістю оптимізувати<br /> свої логістичні процеси сьогодні!</h2>
        <Button 
        label="Створити акаунт"
        onClick={handleClick}
        variant='primary'
        size='large'
        />
      </div>
      <Image src={Arrow} className={styles.Arrow} alt='Arrow'/>
    </div>
  )
}
