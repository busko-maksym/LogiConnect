'use client'

import React, { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import axios from 'axios';
import ApplicantsBlock from '../../molecules/applicants_block/ApplicantsBlock';
import UserHeader from '../../molecules/user_header/userHeader';
import ApplicantsSearch from '../../molecules/applicants_search/ApplicantsSearch';
import styles from './page.module.css';

export default function Page() {
  const [vacancyTitle, setVacancyTitle] = useState<string>('');
  const pathname = usePathname(); 
  const id = pathname?.split('/').pop(); 
  useEffect(() => {
    if (!id) return; 

    const fetchVacancyTitle = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/vacancies/{id}?_id=${id}`);
        setVacancyTitle(response.data.title); 
      } catch (error) {
        console.error('Ошибка при загрузке данных о вакансии:', error);
      }
    };

    fetchVacancyTitle();
  }, [id]);

  return (
    <div>
      <UserHeader />
      <ApplicantsSearch />
      <div className={styles.Name}>
        <h1>{vacancyTitle || 'Загрузка названия...'}</h1>
      </div>
      <ApplicantsBlock />
    </div>
  );
}
