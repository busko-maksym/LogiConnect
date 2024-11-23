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
  const [messages, setMessages] = useState<any[]>([]);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement | null>(null);

  // Завантаження повідомлень з бази даних через POST
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
          `http://localhost:8000/chat/${chatId}/messages`,
          { clientId },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (response.data) {
          setMessages(response.data.reverse());
        }
      } catch (error) {
        console.error('Error loading messages:', error);
      }
    };

    if (chatId) {
      fetchMessages();
    }
  }, [chatId, clientId]);

  useEffect(() => {
    if (clientId && chatId) {
      const url = `ws://localhost:8000/chat/ws/${clientId}/${chatId}`;
      const ws = new WebSocket(url);

      ws.onmessage = (e) => {
        try {
          const incomingMessage = JSON.parse(e.data);

          // Виправлення для обробки `incomingMessage.message`
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

  const onEmojiClick = (emoji: any) => {
    setMessage(message + emoji.emoji);
    setShowEmojiPicker(false);
  };

  const getMessageStyles = (senderId: string, message: string) => {
    const token = localStorage.getItem('token');
  
    if (!token) {
      console.log("Token is not available.");
      return;
    }
  
    // Розшифровуємо токен (JWT)
    const decodedToken = JSON.parse(atob(token.split('.')[1])); // Розшифровуємо частину токену
  
    // Витягуємо user_id з розшифрованого токену
    const userIdFromToken = decodedToken?.user_id; 
  
    const messageLength = message.length;
    const dynamicWidth = Math.min(Math.max(messageLength * 7, 220), 500);
  
    // Порівнюємо senderId з user_id з токену
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
  
  // Парсинг повідомлень
  const parseMessage = (message: string) => {
    try {
      const parsedMessage = JSON.parse(message);
      return parsedMessage.message || message; // Якщо є, то повертаємо parsedMessage.message, інакше повертаємо сам текст
    } catch (error) {
      console.error('Error parsing message:', error);
      return message; // Якщо не вдалося, повертаємо оригінальний рядок
    }
  };

  return (
    <div>
      <ChatInfo />
      <Chat_header />
      <Chat_SideBar />
      <div className={styles.container}>
        <div className={styles.chatContainer}>
          <div ref={chatContainerRef} className={styles.chat}>
            {messages.map((msg, index) => {
              const parsedMessage = parseMessage(msg.message); // Парсимо повідомлення

              return (
                <div
                  key={index}
                  className={styles.messageContainer}
                  style={getMessageStyles(msg.sender_id, parsedMessage)} // Використовуємо sender_id для порівняння
                >
                  <p className={styles.name}>{msg.full_name}</p>
                  <p className={styles.message}>{parsedMessage}</p> {/* Виводимо parsedMessage */}
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









// 'use client'

// import { useState, useEffect, useRef } from 'react';
// import { useParams } from 'next/navigation';
// import Input from '@/app/atoms/Input/Input';
// import Chat_SideBar from '@/app/molecules/Chat_SideBar/Chat_SideBar';
// import EmojiPicker from 'emoji-picker-react';
// import styles from './page.module.css';
// import Chat_header from '@/app/molecules/chat_header/Chat_header';
// import Image from 'next/image';
// import Sent from '../img/Sent.png';

// function Chat() {
//   const { chatId, userId } = useParams();
//   const [clientId, setClientId] = useState(userId || Math.floor(new Date().getTime() / 1000));
//   const [websckt, setWebsckt] = useState<WebSocket | null>(null);
//   const [message, setMessage] = useState('');
//   const [messages, setMessages] = useState<any[]>([]);
//   const [showEmojiPicker, setShowEmojiPicker] = useState(false);
//   const chatContainerRef = useRef<HTMLDivElement | null>(null);

//   useEffect(() => {
//     if (clientId && chatId) {
//       const url = `ws://localhost:8000/chat/ws/${clientId}/${chatId}`;
//       const ws = new WebSocket(url);

//       ws.onopen = () => {
//         return console.log("connect")
//       };

//       ws.onmessage = (e) => {
//         try {
//           const incomingMessage = JSON.parse(e.data);
//           const messageData = incomingMessage.message ? JSON.parse(incomingMessage.message) : null;

//           if (messageData && messageData.message) {
//             setMessages((prevMessages) => [
//               ...prevMessages,
//               {
//                 name: incomingMessage.name,
//                 message: messageData.message,
//                 clientId: messageData.clientId,
//               },
//             ]);
//           }
//         } catch (error) {
//           console.error('Error parsing message:', error);
//         }
//       };

//       setWebsckt(ws);

//       return () => {
//         ws.close();
//       };
//     }
//   }, [clientId, chatId]);

//   useEffect(() => {
//     if (chatContainerRef.current) {
//       chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
//     }
//   }, [messages]);

//   const sendMessage = () => {
//     if (websckt && message.trim()) {
//       const messageData = {
//         time: new Date().toLocaleTimeString(),
//         clientId,
//         message: message.trim(),
//       };
//       websckt.send(JSON.stringify(messageData));
//       setMessage('');
//     }
//   };

//   const onEmojiClick = (emoji: any) => {
//     setMessage(message + emoji.emoji);
//     setShowEmojiPicker(false);
//   };

//   const getMessageStyles = (messageClientId: string, message: string) => {
//     const messageLength = message.length;
//     const dynamicWidth = Math.min(Math.max(messageLength * 7, 220), 500);

//     return messageClientId === clientId
//       ? {
//           backgroundColor: 'rgba(49, 107, 255, 1)',
//           color: 'white',
//           alignSelf: 'flex-end',
//           borderRadius: 20,
//           width: dynamicWidth,
//           minHeight: 56,
//           padding: '10px',
//           wordWrap: 'break-word',
//         }
//       : {
//           backgroundColor: '#f1f1f1',
//           color: 'black',
//           alignSelf: 'flex-start',
//           borderRadius: 20,
//           width: dynamicWidth,
//           minHeight: 56,
//           padding: '10px',
//           wordWrap: 'break-word',
//         };
//   };

//   return (
//     <div className={styles.container}>
//       <Chat_header />
//       <Chat_SideBar />
//       <div className={styles.chatContainer}>
//         <div ref={chatContainerRef} className={styles.chat}>
//           {messages.reverse().map((msg, index) => (
//             <div
//               key={index}
//               className={styles.messageContainer}
//               style={getMessageStyles(msg.clientId, msg.message)}
//             >
//               <p className={styles.name}>{msg.name}</p>
//               <p className={styles.message}>{msg.message}</p>
//             </div>
//           ))}
//         </div>
//         <div className={styles.inputChatContainer}>
//           <button
//             className={styles.stickerButton}
//             onClick={() => setShowEmojiPicker(!showEmojiPicker)}
//           >
//             😊
//           </button>
//           {showEmojiPicker && (
//             <div className={styles.emojiPicker}>
//               <EmojiPicker onEmojiClick={onEmojiClick} />
//             </div>
//           )}
//           <Input
//             size="largebig"
//             placeholder="Chat message ..."
//             onChange={(e) => setMessage(e.target.value)}
//             value={message}
//           />
//           <Image className={styles.Sent} src={Sent} onClick={sendMessage} />
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Chat;