'use client'

import { notFound } from 'next/navigation';
import axios from 'axios';
import Image from 'next/image';
import Button from '@/app/atoms/Button/Button';
import styles from './Vacancy_SinglePage.module.css';
import Arrow from '@/app/img/Arrow 8.png';

type Vacancy = {
  title: string;
  description: string;
  location_from: string;
  location_to: string;
  salary_range: string;
  currency: string;
  owner_phone: string;
};

type VacancyPageProps = {
  vacancy: Vacancy;
};

const VacancyPage = async ({ params }: { params: { id: string } }) => {
  try {
    // Використовуємо fetch або axios для отримання даних на сервері
    const response = await axios.get(`http://localhost:8000/vacancies/${params.id}`);
    const vacancy = response.data.msg;

    if (!vacancy) {
      notFound(); // Якщо вакансії не знайдено, повертається сторінка 404
    }

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
          size='large'
        />
      </div>
    );
  } catch (error) {
    console.error('Error fetching vacancy:', error);
    notFound();
  }
};

export default VacancyPage;
