/**
 * MessageBubble component for displaying chat messages.
 */
import { useState } from "react";
import type { Message } from "../types";
import "../styles/MessageBubble.css";

interface MessageBubbleProps {
  message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const [showSql, setShowSql] = useState(false);
  const isUser = message.role === "user";

  return (
    <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>
      <div className="message-content">
        {message.content}
      </div>
      {message.sql && (
        <div className="sql-section">
          <button
            className="sql-toggle"
            onClick={() => setShowSql(!showSql)}
          >
            {showSql ? "Hide SQL" : "View SQL"}
          </button>
          {showSql && (
            <div className="sql-code">
              <pre>{message.sql}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default MessageBubble;
