import React from 'react'
import styles from './ApplicantsSearch.module.css'
import Input from '@/app/atoms/Input/Input'
import Button from '@/app/atoms/Button/Button'


export default function ApplicantsSearch() {
  return (
    <div className={styles.container}>
      <div className={styles.inputContainer}>
        <Input 
        placeholder=''
        label='Пошук по імені'
        />
      </div>
      <Button 
      label='Пошук'
      />
    </div>
  )
}
