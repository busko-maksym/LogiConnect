import React from 'react'
import styles from './Suggestion.module.css'
import Card from '@/app/atoms/Card/Card'
import Futures from './img/Futures.png'
import Navigation from './img/Navigation.png'
import Search from './img/Search.png'
import Statistics from './img/Statistics.png'
import User_Location from './img/User Location.png'
import Exchange from './img/Exchange.png'

export default function Suggestion() {
  return (
    <div className={styles.container}>
        <div className={styles.container_header}>
            <h1>Що ми пропунуємо</h1>
        </div>
        <div className={styles.container_cards}>
        <div className={styles.row}>
        <Card 
            icon={Futures}
            title="Рейтинги<br /> та відгуки"
            description="надавайте та отримуйте зворотний зв'язок, щоб обирати надійних партнерів."
        />
        <Card 
            icon={Search}
            title="Зручний пошук"
            description="знайдіть найбільш підходящі пропозиції за допомогою гнучких фільтрів."
        />
        <Card 
            icon={Exchange}
            title="Система торгів"
            description="отримуйте пропозиції від перевізників та обирайте найкращі умови."
        />
    </div>
    <div className={styles.row}>
        <Card 
            icon={User_Location}
            title="Просте подання"
            description="вкажіть тип вантажу, маршрут і терміни доставки — і отримуйте пропозиції від перевізників."
        />
        <Card 
            icon={Navigation}
            title="Трекінг вантажів"
            description="в реальному часі за допомогою інтерактивної карти."
        />
        <Card 
            icon={Statistics}
            title="Аналітика і звіти"
            description="отримуйте детальні дані про виконані перевезення для контролю й планування бізнесу."
        />
    </div>
            
        </div>
    </div>
  )
}
