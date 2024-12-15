'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams } from 'next/navigation';
import Input from '@/app/atoms/Input/Input';
import Chat_SideBar from '@/app/molecules/Chat_SideBar/Chat_SideBar';
import EmojiPicker from 'emoji-picker-react';
import styles from './page.module.css';
import Chat_header from '@/app/molecules/chat_header/Chat_header';
import Image from 'next/image';
import Sent from '../img/Sent.png';
import ChatInfo from '@/app/molecules/chat_info/chat_info';
import axios from 'axios';

function Chat() {
  const { chatId, userId } = useParams();
  const [clientId, setClientId] = useState(userId || Math.floor(new Date().getTime() / 1000));
  const [websckt, setWebsckt] = useState<WebSocket | null>(null);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<any[]>([]); // Ініціалізація як порожній масив
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [isLoading, setIsLoading] = useState(true);  // Стан для перевірки завантаження токена
  const chatContainerRef = useRef<HTMLDivElement | null>(null);

  // Завантаження повідомлень з сервера
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }

        const response = await axios.post(
          `http://localhost:8000/chat/${chatId}/messages`,
          { clientId },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Перевірка, чи є відповідь масивом
        if (Array.isArray(response.data)) {
          setMessages(response.data);
        } else {
          console.error("Expected an array of messages, but received:", response.data);
        }
      } catch (error) {
        console.error('Error loading messages:', error);
      }
    };

    if (chatId) {
      fetchMessages();
    }
  }, [chatId, clientId]);

  // Налаштування WebSocket для реального часу
  useEffect(() => {
    if (clientId && chatId) {
      const url = `ws://localhost:8000/chat/ws/${clientId}/${chatId}`;
      const ws = new WebSocket(url);

      ws.onmessage = (e) => {
        try {
          const incomingMessage = JSON.parse(e.data);
          const messageContent =
            typeof incomingMessage.message === 'string'
              ? incomingMessage.message
              : JSON.stringify(incomingMessage.message);

          setMessages((prevMessages) => [
            ...prevMessages,
            {
              sender_id: incomingMessage.sender_id,
              message: messageContent,
              clientId: incomingMessage.clientId,
              full_name: incomingMessage.full_name,
              timestamp: incomingMessage.timestamp || new Date().toISOString(),
            },
          ]);
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };

      setWebsckt(ws);

      return () => {
        ws.close();
      };
    }
  }, [clientId, chatId]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Відправка повідомлення через WebSocket
  const sendMessage = () => {
    if (websckt && message.trim()) {
      const messageData = {
        sender_id: clientId,
        chat_id: chatId,
        message: message.trim(),
        timestamp: new Date().toISOString(),
      };

      websckt.send(JSON.stringify(messageData));
      setMessage('');
    }
  };

  // Обробка емоційних значків
  const onEmojiClick = (emoji: any) => {
    setMessage(message + emoji.emoji);
    setShowEmojiPicker(false);
  };

  // Стилізація повідомлень
  const getMessageStyles = (senderId: string, message: string) => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.log("Token is not available.");
      return {};
    }

    const decodedToken = JSON.parse(atob(token.split('.')[1])); 
    const userIdFromToken = decodedToken?.user_id;

    const messageLength = message.length;
    const dynamicWidth = Math.min(Math.max(messageLength * 7, 220), 500);

    const isOwnMessage = senderId === userIdFromToken;

    return isOwnMessage
      ? {
          backgroundColor: 'rgba(49, 107, 255, 1)',
          color: 'white',
          alignSelf: 'flex-end',
          borderRadius: 20,
          width: dynamicWidth,
          minHeight: 56,
          padding: '10px',
          wordWrap: 'break-word',
        }
      : {
          backgroundColor: '#f1f1f1',
          color: 'black',
          alignSelf: 'flex-start',
          borderRadius: 20,
          width: dynamicWidth,
          minHeight: 56,
          padding: '10px',
          wordWrap: 'break-word',
        };
  };

  // Перевірка і парсинг повідомлень
  const parseMessage = (message: string) => {
    try {
      const parsedMessage = JSON.parse(message);
      return parsedMessage.message || message;
    } catch (error) {
      return message;
    }
  };

  // Перевірка завантаження токена
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return <div>Loading...</div>; // Показуємо індикатор завантаження до моменту, поки не отримаємо токен
  }

  return (
    <div>
      <ChatInfo />
      <Chat_header />
      <Chat_SideBar />
      <div className={styles.container}>
        <div className={styles.chatContainer}>
          <div ref={chatContainerRef} className={styles.chat}>
            {Array.isArray(messages) && messages.map((msg, index) => {
              const parsedMessage = parseMessage(msg.message);

              return (
                <div
                  key={index}
                  className={styles.messageContainer}
                  style={getMessageStyles(msg.sender_id, parsedMessage)}
                >
                  <p className={styles.name}>{msg.full_name}</p>
                  <p className={styles.message}>{parsedMessage}</p>
                </div>
              );
            })}
          </div>

          <div className={styles.inputChatContainer}>
            <button
              className={styles.stickerButton}
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
            >
              😊
            </button>

            {showEmojiPicker && (
              <div className={styles.emojiPicker}>
                <EmojiPicker onEmojiClick={onEmojiClick} />
              </div>
            )}

            <Input
              size="largebig"
              placeholder="Chat message ..."
              onChange={(e) => setMessage(e.target.value)}
              value={message}
            />

            <Image className={styles.Sent} src={Sent} onClick={sendMessage} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
