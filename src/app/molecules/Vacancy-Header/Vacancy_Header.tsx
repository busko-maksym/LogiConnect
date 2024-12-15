import React from 'react'
import styles from './Vacancy_Header.module.css'

export default function Vacancy_Header() {
  return (
    <div className={styles.container}>
      <h3>UA | EN</h3>
      <div className={styles.logo}>
        <h2>LogiConnect</h2>
      </div>
    </div>
  )
}
