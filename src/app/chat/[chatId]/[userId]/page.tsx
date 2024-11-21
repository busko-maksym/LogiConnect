// app/chat/[chatId]/[userId]/page.tsx
'use client'

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';  // Використовуємо useParams з next/navigation
import Input from '@/app/atoms/Input/Input';

function Chat() {
  const { chatId, userId } = useParams();  // Отримуємо параметри chatId та userId з URL
  const [clientId, setClientId] = useState(userId || Math.floor(new Date().getTime() / 1000)); // ID за замовчуванням
  const [websckt, setWebsckt] = useState<WebSocket | null>(null);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    if (clientId && chatId) {
      const url = `ws://localhost:8000/chat/ws/${clientId}/${chatId}`;
      const ws = new WebSocket(url);

      ws.onopen = () => {
        ws.send('Connect');
      };

      ws.onmessage = (e) => {
        const incomingMessage = JSON.parse(e.data);
        setMessages((prevMessages) => [...prevMessages, incomingMessage]);
      };

      setWebsckt(ws);

      return () => {
        ws.close();
      };
    }
  }, [clientId, chatId]);

  const sendMessage = () => {
    if (websckt && message.trim()) {
      const messageData = {
        time: new Date().toLocaleTimeString(),
        clientId,
        message: message.trim(),
      };
      websckt.send(JSON.stringify(messageData));
      setMessage('');
    }
  };

  return (
    <div className="container">
      <h1>Chat Room: {chatId}</h1>
      <h2>Client ID: {clientId}</h2>
      <div className="chat-container">
        <div className="chat">
          {messages.map((value, index) => {
            return value.clientId === clientId ? (
              <div key={index} className="my-message-container">
                <div className="my-message">
                  <p className="client">Client ID: {value.name}</p>
                  <p className="message">{value.message}</p>
                </div>
              </div>
            ) : (
              <div key={index} className="another-message-container">
                <div className="another-message">
                  <p className="client">Client ID: {value.clientId}</p>
                  <p className="message">{value.message}</p>
                </div>
              </div>
            );
          })}
        </div>
        <div className="input-chat-container">
          <Input
            size='small'
            placeholder="Chat message ..."
            onChange={(e) => setMessage(e.target.value)}
            value={message}
          />
          <button className="submit-chat" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
