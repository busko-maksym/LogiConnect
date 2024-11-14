'use client'

import React, { useState, useEffect } from 'react';
import Chat_SideBar from '../Chat_SideBar'; // Ваш компонент для сайдбара
import styles from './ChatInterface.module.css';
import axios from 'axios';
import { io } from 'socket.io-client';

const ChatInterface = () => {
  const [selectedChat, setSelectedChat] = useState<string | null>(null);
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [socket, setSocket] = useState(null);

  // Инициализация WebSocket
  useEffect(() => {
    const newSocket = io('http://localhost:8000'); // URL вашего бэкенда
    setSocket(newSocket);
    return () => newSocket.close();
  }, []);

  // Загрузка сообщений для выбранного чата
  useEffect(() => {
    if (selectedChat) {
      axios.get(`http://localhost:8000/chat/${selectedChat}/messages`)
        .then(response => setMessages(response.data))
        .catch(error => console.error(error));
    }
  }, [selectedChat]);

  // Обработка новых сообщений через WebSocket
  useEffect(() => {
    if (socket) {
      socket.on('receive_message', (newMessage) => {
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      });
    }
  }, [socket]);

  const sendMessage = () => {
    if (messageInput.trim() !== '') {
      const messageData = {
        chat_id: selectedChat,
        message: messageInput,
      };

      // Отправка сообщения через API
      axios.post(`http://localhost:8000/chat/${selectedChat}/messages/send`, messageData)
        .then(response => {
          socket.emit('send_message', response.data);
          setMessageInput('');
        })
        .catch(error => console.error(error));
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatWindow}>
        <div className={styles.messages}>
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender_id === 'YOUR_USER_ID' ? styles.myMessage : styles.otherMessage}>
              {msg.message}
            </div>
          ))}
        </div>
        <div className={styles.inputContainer}>
          <input
            type="text"
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            placeholder="Введіть повідомлення..."
          />
          <button onClick={sendMessage}>Відправити</button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
