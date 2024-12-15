import React from 'react'
import styles from './Vacancy_Search.module.css'
import Button from '@/app/atoms/Button/Button'
import Input from '@/app/atoms/Input/Input'
import Line from './img/Vector 30.png'
import Image from 'next/image'

export default function Vacancy_Search() {
  return (
    <div className={styles.container}>
      <div className={styles.inputForm}>
        <Input
            size='smallmed'
            label='Пошук'
            placeholder='Пошук'
        />
        </div>
    </div>
  )
}
