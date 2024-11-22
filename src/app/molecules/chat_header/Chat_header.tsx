import React from 'react'
import styles from './Chat_header.module.css'

export default function Chat_header() {
  return (
    <div>
      <div className={styles.logo}>
        <h1>Вхід</h1>
        <h2>LogiConnect</h2>
      </div>
    </div>
  )
}
