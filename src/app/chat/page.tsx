'use client'

import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useParams, useNavigate } from "react-router-dom";
import "./App.css";

// Chat component to handle the chat room with the user_id
function Chat() {
  const { chatId, userId } = useParams(); // Get chatId and userId from the URL
  const [clientId, setClientId] = useState(userId || Math.floor(new Date().getTime() / 1000)); // Default to generated ID if no userId
  const [websckt, setWebsckt] = useState();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const url = `ws://localhost:8000/chat/ws/${clientId}/${chatId}`;
    const ws = new WebSocket(url);

    ws.onopen = () => {
      ws.send("Connect");
    };

    ws.onmessage = (e) => {
      const incomingMessage = JSON.parse(e.data);
      setMessages((prevMessages) => [...prevMessages, incomingMessage]);
    };

    setWebsckt(ws);

    // Cleanup function to close the WebSocket connection when the component unmounts
    return () => ws.close();
  }, [clientId, chatId]);

  const sendMessage = () => {
    if (websckt && message.trim()) {
      const messageData = {
        time: new Date().toLocaleTimeString(),
        clientId,
        message: message.trim(),
      };
      websckt.send(JSON.stringify(messageData));
      setMessage(""); // Clear input after sending
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
          <input
            className="input-chat"
            type="text"
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

// Home component to allow users to select a chat room
function Home() {
  const navigate = useNavigate();
  const [userId, setUserId] = useState("");
  const [chatId, setChatId] = useState("general"); // Default chat room

  const handleJoin = () => {
    if (userId.trim()) {
      navigate(`/chat/${chatId}/${userId}`);
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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat/:chatId/:userId" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;
