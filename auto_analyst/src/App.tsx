import React, { useState, useEffect } from 'react';
import './App.css';

const App: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot' }[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setInput('');
      setIsTyping(true);

      // Simulate bot response
      setTimeout(() => {
        setIsTyping(false);
        setMessages(prev => [...prev, { text: `I understand you said: "${input}". How can I assist you further?`, sender: 'bot' }]);
      }, 2000);
    }
  };

  useEffect(() => {
    // Scroll to bottom of chat when new messages are added
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h2>Auto Analyst Chat</h2>
        </div>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-content">{message.text}</div>
            </div>
          ))}
          {isTyping && (
            <div className="message bot typing">
              <span>Bot is typing</span>
              <span className="dot-animation">...</span>
            </div>
          )}
        </div>
        <div className="chat-input">
          <div className="input-container" style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type a message..."
              className="modern-input"
              style={{ width: '90%', marginBottom: '10px' }}
            />
            <button onClick={handleSend} className="send-button" style={{ width: '90%' }}>
              Send
            </button>
          </div>  
        </div>
      </div>
    </div>
  );
}

export default App;
