import React from 'react'
import styles from './UserRating.module.css'
import Input from '@/app/atoms/Input/Input'
import Button from '@/app/atoms/Button/Button'

export default function UserRating() {
  return (
    <div className={styles.container}>
      <div className={styles.containerHeader}>
        <h1>Відгуки</h1>
        <p>n відгуків</p>
      </div>
      <div className={styles.inputRating}>
        <h1>Залиште свій відгук</h1>
        <Input
         />
        <p>Ваша оцінка:</p>
        <Button 
        label='Надіслати'
        />
      </div>
      <div className={styles.ratings}>
        <div className={styles.rating}>
          <h2>Ім’я Прізвище</h2>
          <p>Хороший водій!</p>
          <h3>Оцінка:</h3>
        </div>
      </div>
    </div>
  )
}
