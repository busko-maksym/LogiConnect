'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Vacancy_Block.module.css';
import Image from 'next/image';
import Link from 'next/link';
import Vacancy_SideBar from '../Vacancy_SideBar/Vacancy_SideBar';

type Vacancy = {
  _id: string;
  title: string;
  description: string;
  location_from: string;
  location_to: string;
  salary_range: string;
  currency: string;
  distance: string;
};

const VacancyList = () => {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [filteredVacancies, setFilteredVacancies] = useState<Vacancy[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    minSalary: '',
    maxSalary: '',
    minDistance: '',
    maxDistance: '',
    maxWeight: '',
    maxVolume: '',
    urgency: [],
  });

  useEffect(() => {
    const fetchVacancies = async () => {
      try {
        const response = await axios.get('http://localhost:8000/vacancies/');
        setVacancies(response.data.msg);
        setFilteredVacancies(response.data.msg);
      } catch (error) {
        console.error('Error fetching vacancies:', error);
        setError('Failed to fetch vacancies. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchVacancies();
  }, []);

  useEffect(() => {
    const applyFilters = () => {
      let filtered = vacancies;

      if (filters.minSalary) {
        filtered = filtered.filter((vacancy) => parseInt(vacancy.salary_range) >= filters.minSalary);
      }
      if (filters.maxSalary) {
        filtered = filtered.filter((vacancy) => parseInt(vacancy.salary_range) <= filters.maxSalary);
      }
      if (filters.minDistance) {
        filtered = filtered.filter((vacancy) => parseFloat(vacancy.distance) >= filters.minDistance);
      }
      if (filters.maxDistance) {
        filtered = filtered.filter((vacancy) => parseFloat(vacancy.distance) <= filters.maxDistance);
      }

      setFilteredVacancies(filtered);
    };

    applyFilters();
  }, [filters, vacancies]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  if (loading) return <p>Завантаження вакансій...</p>;

  return (
    <div className={styles.container}>
      {error && <p className={styles.error}>{error}</p>}
      <Vacancy_SideBar onFilterChange={handleFilterChange} />
      <div className={styles.vacancyList}>
        {filteredVacancies.map((vacancy) => (
          <Link key={vacancy._id} href={`/vacancies?id=${vacancy._id}`} className={styles.vacancyLink}>
            <div className={styles.vacancy}>
              <div className={styles.Road}>
                <h3>Від: {vacancy.location_from || 'Невідомо'}</h3>
                <h3>До: {vacancy.location_to || 'Невідомо'}</h3>
                <p>{vacancy.distance} KM</p>
              </div>
              <h4>{vacancy.description || 'Опис відсутній...'}</h4>
              <h5>
               ${vacancy.salary_range ? `${vacancy.salary_range} ${vacancy.currency || ''}` : 'Зарплата не вказана'}
              </h5>
            </div>
            <div className={styles.income}>
              <h6>Чистий заробіток</h6>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default VacancyList;
