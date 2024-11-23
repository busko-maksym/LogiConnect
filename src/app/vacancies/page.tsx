'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Vacancy_SinglePage.module.css';
import Image from 'next/image';
import Arrow from './img/Arrow 8.png';
import Vacancy_Header from '../molecules/Vacancy-Header/Vacancy_Header';
import Button from '../atoms/Button/Button';
import Vacancy_SideBar from '../molecules/Vacancy_SideBar/Vacancy_SideBar';
import { useRouter } from 'next/navigation';

type Vacancy = {
  _id: string;
  title: string;
  description: string;
  location_from: string;
  location_to: string;
  salary_range: string;
  currency: string;
  posted_by: string;
  created_at: string;
  requirements: string[];
  additional_info: string;
  urgency: string;
};

const VacancySinglePage = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');
  const [vacancy, setVacancy] = useState<Vacancy | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (id) {
      axios.get(`http://localhost:8000/vacancies/{id}?_id=${id}`)
        .then((response) => {
          setVacancy(response.data);
        })
        .catch((err) => {
          setError('Вакансия не найдена');
        });
    }
  }, [id]);

  const handleCreateChat = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      router.push('/login');
      return;
    }
    
    try {
      // Перевірка, яке поле містить правильний ID користувача
      const secondUserId = vacancy?.posted_by;  // або vacancy?.user_id, залежно від вашої структури
      
      if (!secondUserId) {
        setError('Немає ідентифікатора користувача для створення чату');
        return;
      }
  
      // Відправка POST-запиту для створення чату
      const response = await axios.post(
        `http://127.0.0.1:8000/chat/create?second_user=${secondUserId}`,
        {}, // Пусте тіло запиту
        {
          headers: {
            Authorization: `Bearer ${token}`,
            accept: 'application/json',
          },
        }
      );
    
      // Перенаправлення користувача на сторінку чату з chat_id та jwt токеном
      const chatId = response.data.chat_id;
      if (!chatId) {
        setError('Не вдалося отримати chatId');
        return;
      }
      router.push(`/chat/${chatId}/${token}`);
    } catch (error) {
      console.error(error);
      setError('Помилка при створенні чату');
    }
  };
  

  const handleApply = async () => {
    const token = localStorage.getItem('token');
  
    if (!token) {
      router.push('/login');
      return;
    }
  
    if (id) {
      try {
        const response = await axios.post(`http://localhost:8000/vacancies/{id}/apply?vacancies_id=${id}`, {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
  
        alert(response.data.msg);
      } catch (err) {
        console.error(err);
        setError('Ошибка при подаче заявки');
      }
    } else {
      setError('Неверный идентификатор вакансии');
    }
  };

  if (error) return <p>{error}</p>;
  if (!vacancy) return <p>Загрузка...</p>;

  return (
    <div>
      <Vacancy_Header />
      <Vacancy_SideBar />
      <div className={styles.container}>
        <h1>{vacancy.title}</h1>
        <h2>{vacancy.salary_range} {vacancy.currency}</h2>
        <div className={styles.Road}>
          <h3>{vacancy.location_from}</h3>
          <Image src={Arrow} alt="Arrow" />
          <h3>{vacancy.location_to}</h3>
        </div>
        <p>{vacancy.description}</p>
        <Button 
          label="Податися"
          variant="primary"
          size="ZaebavAndriy"
          onClick={handleApply}
        />
        <Button 
          label="Написати"
          variant="primary"
          size="ZaebavAndriy"
          onClick={handleCreateChat}
        />
      </div>
    </div>
  );
};



export default VacancySinglePage;
