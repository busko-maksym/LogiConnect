import React from 'react';
import Image from 'next/image';
import Button from '@/components/Button/Button';  // Якщо це ваша кнопка
import styles from './Vacancy_SinglePage.module.css';  // Ваші стилі
import Arrow from '@/img/Arrow 8.png';  // Зображення стрілки

type VacancyProps = {
  vacancy: {
    title: string;
    description: string;
    location_from: string;
    location_to: string;
    salary_range: string;
    currency: string;
    owner_phone: string;
  };
};

const Vacancy_SinglePage = ({ vacancy }: VacancyProps) => {
  return (
    <div className={styles.container}>
      <h1>{vacancy.title}</h1>
      <h2>{vacancy.salary_range} {vacancy.currency}</h2>

      <div className={styles.Road}>
        <h3>Від: {vacancy.location_from || 'Невідомо'}</h3>
        <Image src={Arrow} alt="Arrow" />
        <h3>До: {vacancy.location_to || 'Невідомо'}</h3>
      </div>

      <p>{vacancy.description || 'Опис вакансії відсутній.'}</p>

      <h4>Власник вакансії:</h4>
      <h5>{vacancy.owner_phone || 'Невідомо'}</h5>

      <Button 
        label='Податися'
        variant='primary'
        size='large' // Можна налаштувати розмір кнопки
      />
    </div>
  );
};

export default Vacancy_SinglePage;
