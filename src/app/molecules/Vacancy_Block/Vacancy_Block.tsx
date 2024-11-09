// app/vacancies/VacancyList.tsx
'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Vacancy_Block.module.css';
import Image from 'next/image';
import Arrow from './img/Arrow 8.png';

type Vacancy = {
  _id: string;
  title: string;
  description: string;
  location_from: string;
  location_to: string;
  salary_range: string;
  currency: string;
  urgency: string;
};

const VacancyList = () => {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVacancies = async () => {
      try {
        const response = await axios.get('http://localhost:8000/vacancies/');
        setVacancies(response.data.msg);
      } catch (error) {
        console.error('Error fetching vacancies:', error);
        setError('Failed to fetch vacancies. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchVacancies();
  }, []);

  if (loading) return <p>Завантаження вакансій...</p>;

  return (
    <div className={styles.container}>
      {error && <p className={styles.error}>{error}</p>}

      {vacancies.map((vacancy) => (
        <a href={`/vacancies/${vacancy._id}`} key={vacancy._id} className={styles.vacancyLink}>
          <div className={styles.vacancy}>
            <h2>{vacancy.title}</h2>
            <div className={styles.Road}>
              <h3>Від: {vacancy.location_from || 'Невідомо'}</h3>
              <Image src={Arrow} alt="Arrow" />
              <h3>До: {vacancy.location_to || 'Невідомо'}</h3>
            </div>
            <h4>{vacancy.description || 'Опис відсутній...'}</h4>
            <h5>
              {vacancy.salary_range ? `${vacancy.salary_range} ${vacancy.currency || ''}` : 'Зарплата не вказана'}
            </h5>
          </div>
        </a>
      ))}
    </div>
  );
};

export default VacancyList;
