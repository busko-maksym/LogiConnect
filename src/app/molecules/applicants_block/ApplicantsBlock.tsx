import React, { useEffect, useState } from 'react';
import Axios from 'axios';
import styles from './ApplicantsBlock.module.css';
import { usePathname } from 'next/navigation';
import Button from '@/app/atoms/Button/Button';

export default function ApplicantsBlock() {
  const [applicants, setApplicants] = useState([]);
  const pathname = usePathname(); 
  const id = pathname?.split('/').pop(); 

  const token = localStorage.getItem('token');
  
  useEffect(() => {
    const fetchApplicants = async () => {
      try {
        const response = await Axios.get(`http://127.0.0.1:8000/vacancies/{id}/applicants?vacancies_id=${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`, // Передаємо токен в заголовках
          }
        });
        setApplicants(response.data.list); // Отримуємо список аплікантів
      } catch (error) {
        console.error("Error fetching applicants:", error.response ? error.response.data : error);
      }
    };

    if (id && token) {
      fetchApplicants();
    }
  }, [id, token]);

  return (
    <div className={styles.container}>
      {applicants.map((applicant) => (
        <div key={applicant._id} className={styles.block}>
          <div className={styles.header} />
          <h1>{applicant.first_name} {applicant.last_name}</h1>
          <h2>Тип прав: {applicant.driver_license_type}</h2>
          <div className={styles.button}>
          <Button size='accept' label='Прийняти'/>
          <Button size='write'/>
          </div>
        </div>
      ))}
    </div>
  );
}
