import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import styles from './Chat_SideBar.module.css';
import Input from '@/app/atoms/Input/Input';
import axios from 'axios';

type Chat = {
  _id: string;
  participants: string[];
  last_message: string | null;
  updated_at: string;
  name: string;
};

export default function Chat_SideBar() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  const token = localStorage.getItem('token');

  const fetchChats = async () => {
    try {
      const response = await axios.get('http://localhost:8000/chat/', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      setChats(response.data.msg);
    } catch (error) {
      console.error('Error fetching chats:', error);
      setError('Не вдалося завантажити чати. Спробуйте пізніше.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChats();

    const chatIdFromUrl = searchParams.get('chatId');
    if (chatIdFromUrl) {
      setSelectedChatId(chatIdFromUrl);
    }
  }, [searchParams]);

  const filteredChats = chats.filter((chat) =>
    chat._id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleChatSelect = (chatId: string) => {
    setSelectedChatId(chatId);
    if (token) {
      router.push(`/chat/${chatId}/${token}?chatId=${chatId}`);
    }
  };

  if (loading) {
    return console.log("loading");
  }

  return (
    <div className={styles.container}>
      <div className={styles.search}>
        <Input
          placeholder="Пошук по ID чату"
          label="Пошук"
          size="midlarge"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
      <div className={styles.chatList}>
        {error && <p className={styles.error}>{error}</p>}
        {filteredChats.length === 0 ? (
          <p>Чатів немає, або вони не відповідають запиту.</p>
        ) : (
          filteredChats.map((chat) => (
            <div
              key={chat._id}
              className={`${styles.chatItem} ${selectedChatId === chat._id ? styles.selectedChat : ''}`}
              onClick={() => handleChatSelect(chat._id)}
            >
              <div className={styles.chatDetails}>
                <p>{chat.name}</p>
                <p><strong>{chat.last_message || 'Немає останнього повідомлення'}</strong></p>
                <p><strong>{new Date(chat.updated_at).toLocaleString()}</strong></p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
