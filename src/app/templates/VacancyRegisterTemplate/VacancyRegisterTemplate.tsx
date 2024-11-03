import VacancyRegistration from '@/app/molecules/VacancyRegistration/VacancyRegistration'
import React from 'react'
import styles from './VacancyRegisterTemplate.module.css'

export default function VacancyRegisterTemplate() {
  return (
    <div className={styles.container}>
      <VacancyRegistration />
    </div>
  )
}
