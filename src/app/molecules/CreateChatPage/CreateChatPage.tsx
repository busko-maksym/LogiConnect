'use client'

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const CreateChatPage: React.FC = () => {
  // Состояние для хранения ID второго пользователя
  const [secondUserId, setSecondUserId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Используем useRouter для перенаправления
  const router = useRouter();

  // Обработчик отправки формы
  const handleCreateChat = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Получение токена из localStorage (например)
      const token = localStorage.getItem('token');

      if (!token) {
        setError('Требуется авторизация.');
        setLoading(false);
        return;
      }

      // Отправка POST-запроса на создание чата с использованием query-параметра
      const response = await axios.post(
        `http://127.0.0.1:8000/chat/create?second_user=${secondUserId}`,
        {}, // Пустое тело запроса
        {
          headers: {
            'Authorization': `Bearer ${token}`, // Передача токена в заголовке
            'accept': 'application/json',
          },
        }
      );

      // Перенаправление пользователя на страницу чата
      const chatId = response.data.chat_id;
      router.push(`/chat/${chatId}`);

    } catch (error) {
      setError('Ошибка при создании чата. Пожалуйста, проверьте данные.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-chat-page">
      <h1>Создание чата</h1>
      <form onSubmit={handleCreateChat}>
        <div className="form-group">
          <label htmlFor="secondUserId">ID второго пользователя:</label>
          <input
            type="text"
            id="secondUserId"
            value={secondUserId}
            onChange={(e) => setSecondUserId(e.target.value)}
            required
          />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Создание...' : 'Создать чат'}
        </button>
      </form>
    </div>
  );
};

export default CreateChatPage;
