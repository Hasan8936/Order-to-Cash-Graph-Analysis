/**
 * ChatPanel component for natural language queries.
 */
import React, { useState } from "react";
import { useChat } from "../hooks/useChat";
import MessageBubble from "./MessageBubble";
import "../styles/ChatPanel.css";

function ChatPanel() {
  const { messages, isLoading, sendMessage, clearHistory } = useChat();
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue);
      setInputValue("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>Chat with Graph</h2>
        <button
          className="clear-button"
          onClick={clearHistory}
          disabled={messages.length === 0}
        >
          Clear
        </button>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Welcome to O2C Analysis</h3>
            <p>Ask me about sales orders, deliveries, billing, or payments.</p>
            <p className="example">
              Example: "Show me orders that haven't been delivered yet"
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble key={idx} message={msg} />
          ))
        )}
        {isLoading && (
          <div className="loading-message">
            <span className="spinner"></span>
            <p>Analyzing...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about the Order-to-Cash process..."
          disabled={isLoading}
          className="input-field"
        />
        <button
          onClick={handleSendMessage}
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;
