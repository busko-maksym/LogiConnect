import React from 'react'
import styles from './Chat_SideBar.module.css'
import Input from '@/app/atoms/Input/Input'

export default function Chat_SideBar() {
  return (
    <div className={styles.container}>
      <div className={styles.search}>
        <Input 
        placeholder='Пошук'
        label='Пошук'
        size='midlarge'
        />
      </div>
    </div>
  )
}
