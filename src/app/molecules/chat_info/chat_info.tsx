import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
import styles from './chat_info.module.css';

type Chat = {
  _id: string;
  participants: string[];
  last_message: string | null;
  updated_at: string;
  name: string;
};

export default function ChatInfo() {
  const [chatName, setChatName] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  const token = localStorage.getItem('token');

  // Отримання chatId із параметрів пошуку
  const chatId = searchParams.get('chatId');

  // Функція для отримання імені чату
  const fetchChatName = async () => {
    try {
      const response = await axios.get('http://localhost:8000/chat/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      // Знаходимо чат за ID
      const chatData = response.data.msg.find((chat: Chat) => chat._id === chatId);
      // Зберігаємо ім'я чату
      setChatName(chatData ? chatData.name : 'Невідомий чат');
    } catch (error) {
      console.error('Error fetching chat name:', error);
      setError('Не вдалося завантажити ім\'я чату. Спробуйте пізніше.');
    }
  };

  useEffect(() => {
    if (chatId) {
      fetchChatName();
    }
  }, [chatId]);

  if (error) {
    return <p className={styles.error}>{error}</p>;
  }

  return (
    <div className={styles.container}>
      <h1>{chatName || 'Завантаження...'}</h1>
    </div>
  );
}
