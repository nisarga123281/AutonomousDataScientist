import { useState } from "react";
import "./Chat.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm your AUTODS AI assistant. Ask me anything about your dataset, analysis results, models, or insights.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed.");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't process that request. Please make sure the AUTODS backend and AI service are running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div>
          <span className="chat-eyebrow">AUTODS AI</span>
          <h1>AI Data Scientist</h1>
          <p>
            Ask questions about your dataset, analysis, models and insights.
          </p>
        </div>

        <div className="chat-status">
          <span className="chat-status-dot"></span>
          ONLINE
        </div>
      </div>

      <div className="chat-card">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${
                message.role === "user" ? "user-message" : "assistant-message"
              }`}
            >
              <div className="message-label">
                {message.role === "user" ? "YOU" : "AUTODS AI"}
              </div>

              <div className="message-content">{message.content}</div>
            </div>
          ))}

          {loading && (
            <div className="chat-message assistant-message">
              <div className="message-label">AUTODS AI</div>
              <div className="typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>

        <div className="chat-input-area">
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something about your dataset..."
            rows={2}
            disabled={loading}
          />

          <button
            className="chat-send-btn"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>

        <div className="chat-hint">
          Press Enter to send • Shift + Enter for a new line
        </div>
      </div>
    </div>
  );
}

export default Chat;