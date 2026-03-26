/**
 * Custom hook for handling chat interactions.
 */
import { useState, useCallback } from "react";
import axios from "axios";
import { useGraphStore } from "../store/graphStore";
import type { ChatRequest, ChatResponse, Message } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { setHighlightedNodes } = useGraphStore();

  const sendMessage = useCallback(
    async (userMessage: string) => {
      if (!userMessage.trim()) return;

      // Add user message to history
      const newUserMessage: Message = { role: "user", content: userMessage };
      setMessages((prev) => [...prev, newUserMessage]);
      setIsLoading(true);

      try {
        const request: ChatRequest = {
          message: userMessage,
          history: messages,
        };

        const response = await axios.post<ChatResponse>(
          `${API_BASE}/api/chat`,
          request
        );

        if (response.data) {
          // Add assistant message to history
          const assistantMessage: Message = {
            role: "assistant",
            content: response.data.answer,
            sql: response.data.sql,
          };
          setMessages((prev) => [...prev, assistantMessage]);

          // Highlight nodes from the response
          if (response.data.highlighted_nodes.length > 0) {
            setHighlightedNodes(response.data.highlighted_nodes);
          }

          return response.data;
        }
      } catch (err) {
        console.error("Error sending message:", err);
        const errorMessage: Message = {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [messages, setHighlightedNodes]
  );

  const clearHistory = useCallback(() => {
    setMessages([]);
  }, []);

  return { messages, isLoading, sendMessage, clearHistory };
}
