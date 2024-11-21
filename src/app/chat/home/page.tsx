// app/home/page.tsx
import { useState } from 'react';
import { useRouter } from 'next/navigation';  // Використовуємо хук з next/navigation для навігації

function Home() {
  const router = useRouter();
  const [userId, setUserId] = useState('');
  const [chatId, setChatId] = useState('general'); // За замовчуванням обрано чат general

  const handleJoin = () => {
    if (userId.trim()) {
      router.push(`/chat/${chatId}/${userId}`);  // Навігація до чату з параметрами
    }
  };

  return (
    <div className="container">
      <h1>Select a Chat Room and Enter Your User ID</h1>
      <div>
        <label>
          User ID:
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter your user ID"
          />
        </label>
      </div>
      <div>
        <label>
          Chat Room:
          <select onChange={(e) => setChatId(e.target.value)} value={chatId}>
            <option value="general">General Chat</option>
            <option value="random">Random Chat</option>
            <option value="tech">Tech Chat</option>
          </select>
        </label>
      </div>
      <button onClick={handleJoin}>Join Chat</button>
    </div>
  );
}

export default Home;
