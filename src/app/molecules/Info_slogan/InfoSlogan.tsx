import Image from 'next/image'
import React from 'react'
import Checkmark from './img/Checkmark.png'
import styles from './InfoSlogan.module.css'
import Truck from './img/delivery truck back side view.png'
import Line from './img/Line.png'

export default function InfoSlogan() {
  return (
    <div className={styles.container}>
      <div className={styles.itemContainer}>
        <Image src={Checkmark} className={styles.centeredImage} alt="Checkmark"/>
        <h1>Міжнародні перевезення по всій<br /> Європі та в інших континентах</h1>
        <p>Швидко, Надійно, Доступно</p>
        <p>Пунктуальність та Безпека<br /> на Першому Місці</p>
        <Image src={Truck} className={styles.Truck} alt="Truck" />
        </div>
        <Image src={Line} className={styles.Line} alt="Line" />
      </div>
  )
}
