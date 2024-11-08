import React from 'react'
import styles from './Vacancy_Search.module.css'
import Button from '@/app/atoms/Button/Button'
import Input from '@/app/atoms/Input/Input'

export default function Vacancy_Search() {
  return (
    <div className={styles.container}>
      <Input
        size='large'
        label='Пошук по назві'
        placeholder='Пошук по назві'
      />
    </div>
  )
}
