'use client'

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'next/navigation';

interface Message {
  _id: string;
  chat_id: string;
  sender_id: string;
  message: string;  // Використовуємо message, а не content
  timestamp: string;
}

const ChatPage: React.FC = () => {
  const searchParams = useSearchParams();
  const chatId = searchParams.get('chatId'); // Отримуємо параметр chatId

  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Загрузка повідомлень при завантаженні компонента
  useEffect(() => {
    if (chatId) {
      fetchMessages();
    }
  }, [chatId]);

  // Функція для отримання повідомлень
  const fetchMessages = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');

      if (!token) {
        setError('Требуется авторизация.');
        setLoading(false);
        return;
      }

      const response = await axios.post(
        `http://127.0.0.1:8000/chat/${chatId}/messages`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'accept': 'application/json',
          },
        }
      );

      if (Array.isArray(response.data)) {
        setMessages(response.data);
      } else {
        setError('Ошибка: полученные данные не являются массивом.');
      }
    } catch (error) {
      setError('Ошибка при загрузке сообщений.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Функція для відправки нового повідомлення
  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const token = localStorage.getItem('token');

      if (!token) {
        setError('Требуется авторизация.');
        return;
      }

      const timestamp = new Date().toISOString();  // Отримуємо поточний час

      const messageData = {
        sender_id: 'current_user',  // Тут вказуйте ID поточного користувача
        chat_id: chatId as string,   // Використовуємо chatId з query-параметрів
        message: newMessage,         // Текст повідомлення
        timestamp: timestamp,       // Час відправки
      };

      const response = await axios.post(
        `http://127.0.0.1:8000/chat/${chatId}/messages/send`,
        messageData, // Відправляємо дані у потрібному форматі
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'accept': 'application/json',
          },
        }
      );

      // Додавання нового повідомлення в список
      const newMessageData = {
        _id: response.data.message_id,   // Використовуємо message_id від сервера
        chat_id: chatId as string,       // Використовуємо chatId
        sender_id: 'current_user',       // Тут має бути реальний ID користувача
        message: newMessage,             // Текст повідомлення
        timestamp: timestamp,            // Час відправки
      };

      setMessages((prevMessages) => [
        ...prevMessages,
        newMessageData,
      ]);

      setNewMessage(''); // Очищення поля вводу після відправки

    } catch (error) {
      setError('Ошибка при отправке сообщения.');
      console.error(error);
    }
  };

  return (
    <div className="chat-page">
      <h1>Чат</h1>

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p>Загрузка сообщений...</p>
      ) : (
        <div className="chat-messages">
          {messages.length === 0 ? (
            <p>Нет сообщений для отображения</p>
          ) : (
            messages.map((message) => (
              <div key={message._id} className="message">
                <strong>{message.sender_id}:</strong> {message.message}  {/* Використовуємо message */}
                <span>{new Date(message.timestamp).toLocaleString()}</span>
              </div>
            ))
          )}
        </div>
      )}

      <form onSubmit={sendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Введите сообщение..."
          required
        />
        <button type="submit">Отправить</button>
      </form>
    </div>
  );
};

export default ChatPage;
