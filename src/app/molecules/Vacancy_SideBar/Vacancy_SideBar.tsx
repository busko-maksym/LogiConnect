import React from 'react'
import styles from './Vacancy_SideBar.module.css'
import Image from 'next/image'
import ProfilePlaceholder from './img/Rectangle 51.png' // Заміни на зображення для аватару

export default function Vacancy_SideBar() {
  return (
    <div className={styles.container}>
      <div className={styles.user_info}>
        <Image src={ProfilePlaceholder} />
        <div className={styles.text}>
          <h1>Ім’я Прізвище</h1>
          <h2>Професія</h2>
        </div>
      </div>
      <div className={styles.func_category}>
        <button>Чат</button>
        <button>Мої вакансії</button>
      </div>
    </div>
  )
}
