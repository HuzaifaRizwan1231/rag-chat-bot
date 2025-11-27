import { useState } from "react";

export const useInputArea = (onSendMessage, loading) => {
  // States
  const [input, setInput] = useState("");
  const [rows, setRows] = useState(1);

  // Handlers
  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput("");
      setRows(1);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading) {
        handleSubmit(e);
      }
    }
  };

  const handleInputChange = (e) => {
    const allowedRows = 6;
    const textareaLineHeight = 24;
    const previousRows = e.target.rows;
    e.target.rows = 1;

    const currentRows = Math.floor(e.target.scrollHeight / textareaLineHeight);

    if (currentRows === previousRows) {
      e.target.rows = currentRows;
    }

    if (currentRows >= allowedRows) {
      e.target.rows = allowedRows;
      e.target.scrollTop = e.target.scrollHeight;
    }

    setRows(currentRows < allowedRows ? currentRows : allowedRows);
    setInput(e.target.value);
  };

  return {
    input,
    rows,
    handleSubmit,
    handleKeyDown,
    handleInputChange,
  };
};