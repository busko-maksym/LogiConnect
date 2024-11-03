import React from 'react'
import RegisterForm from '../../molecules/Register/RegisterForm'
import styles from './RegisterTemplate.module.css'

export default function RegisterTemplate() {
  return (
    <div>
      <div className={styles.container}>
        <h3>Реєстрація</h3>
        <h4>LogiConnect</h4>
      </div>
      <RegisterForm />
    </div>
  )
}
