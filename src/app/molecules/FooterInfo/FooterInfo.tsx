import React from 'react'
import styles from './FooterInfo.module.css'
import Image from 'next/image'
import Facebook from './img/Facebook.png'
import LinkedIn from './img/LinkedIn.png'

export default function FooterInfo() {
  return (
    <div className={styles.container}>
      <div className={styles.itemsContainer}>
        <div className={styles.Finder}>
          <h1>Де нас знайти:</h1>
          <div className={styles.imageContainer}>
            <Image src={Facebook} alt='Facebook'  />
            <Image src={LinkedIn} alt='LinkedIn'  />
          </div>
        </div>
        <div className={styles.otherInfo}>
          <p>Зона для клієнтів</p>
          <p>Правова інформація</p>
          <p>Політика конфіденційності</p>
          <p>Використання Cookies</p>
        </div>
        <div className={styles.logo}>
          <h1>LogiConnect</h1>
          <p>«LOGICONNECT» пропонує комплексні послуги внутрішніх та міжнародних перевезень, контрактної логістики.</p>
        </div>
      </div>
    </div>
  )
}
