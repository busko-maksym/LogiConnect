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
            size='large'
            label='Пошук по назві'
            placeholder='Пошук по назві'
        />
        <Button 
            size='largemid'
            variant='primary'
            label='Пошук'
        />
        </div>
        <h3><b>100 000+</b> актуальних вакансій від <b>30 000+</b> компаній</h3>
        <Image src={Line} />
    </div>
  )
}
