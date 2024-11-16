'use client'

import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'next/navigation';

interface Message {
  _id: string;
  chat_id: string;
  sender_id: string;
  message: string;
  timestamp: string;
}

const ChatPage: React.FC = () => {
  const searchParams = useSearchParams();
  const chatId = searchParams.get('chatId');

  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (chatId) {
      connectWebSocket();
    }

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [chatId]);

  const connectWebSocket = () => {
    const token = localStorage.getItem('token');

    if (!token) {
      setError('Требуется авторизация.');
      return;
    }

    ws.current = new WebSocket(`ws://127.0.0.1:8000/chat/${chatId}/ws?token=${token}`);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setError(null);
    };

    ws.current.onmessage = (event) => {
      const receivedMessage = JSON.parse(event.data);
      if (receivedMessage && receivedMessage.chat_id === chatId) {
        setMessages((prevMessages) => [...prevMessages, receivedMessage]);
      }
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Ошибка соединения с WebSocket сервером.');
    };
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const timestamp = new Date().toISOString();

      const messageData = {
        chat_id: chatId as string,
        sender_id: 'current_user',
        message: newMessage,
        timestamp: timestamp,
      };

      ws.current.send(JSON.stringify(messageData));

      const newMessageData = {
        _id: Math.random().toString(36).substr(2, 9),
        ...messageData,
      };

      setMessages((prevMessages) => [...prevMessages, newMessageData]);
      setNewMessage('');
    } else {
      setError('WebSocket не подключен.');
    }
  };

  return (
    <div className="chat-page">
      <h1>Чат</h1>

      {error && <p className="error">{error}</p>}

      <div className="chat-messages">
        {messages.length === 0 ? (
          <p>Нет сообщений для отображения</p>
        ) : (
          messages.map((message) => (
            <div key={message._id} className="message">
              <strong>{message.sender_id}:</strong> {message.message}
              <span>{new Date(message.timestamp).toLocaleString()}</span>
            </div>
          ))
        )}
      </div>

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
