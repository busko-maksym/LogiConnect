import React from 'react'
import styles from './userHeader.module.css'

export default function UserHeader() {
  return (
    <div className={styles.container}>
      <div className={styles.logo}>
        <h2>LogiConnect</h2>
      </div>
    </div>
  )
}
