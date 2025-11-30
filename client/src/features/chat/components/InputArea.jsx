import React from "react";
import { motion } from "framer-motion";
import { ArrowUpIcon, MicrophoneIcon } from "@heroicons/react/solid";
import { useInputArea } from "../hooks/useInputArea";
import { uploadDocumentApiCall } from "../api/chat.api";

const InputArea = ({
  onSendMessage,
  loading,
  handleAudioRecording,
  recording,
  transcribing,
  isCollapsed,
}) => {
  const { input, rows, handleSubmit, handleKeyDown, handleInputChange } =
    useInputArea(onSendMessage, loading);

  // -------------------------
  // 📌 Handle PDF Upload
  // -------------------------
  const handleDocumentUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    await uploadDocumentApiCall(formData);
  };

  return (
    <motion.div
      className={`dark:bg-secondaryColorDark bg-secondaryColorLight p-4 my-4 shadow-md mx-auto rounded-3xl ${
        isCollapsed
          ? "w-11/12 sm:w-3/4 lg:w-1/2 "
          : "w-11/12 sm:w-3/4 lg:w-3/5"
      }`}
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <form onSubmit={handleSubmit} className="flex gap-2 items-end">
        <textarea
          onKeyDown={handleKeyDown}
          value={input}
          onChange={handleInputChange}
          placeholder="Message AI Chatbot"
          className="flex-1 w-full rounded-lg focus:outline-none dark:bg-secondaryColorDark dark:text-white bg-secondaryColorLight text-black resize-none"
          rows={rows}
        />

        {/* SEND BUTTON */}
        <motion.button
          disabled={loading || recording || transcribing || input.length === 0}
          type="submit"
          className={`px-4 py-2 h-8 w-8 flex items-center justify-center mt-auto ${
            loading || recording || transcribing || input.length === 0
              ? "dark:bg-[#676767] bg-[#d7d7d7] text-[#f4f4f4]"
              : "dark:bg-white bg-black text-white dark:text-black dark:hover:bg-slate-300"
          } rounded-full`}
        >
          <ArrowUpIcon className="w-5 h-5" />
        </motion.button>

        {/* AUDIO BUTTON */}
        <motion.button
          disabled={loading || transcribing}
          type="button"
          onClick={handleAudioRecording}
          className={`px-4 py-2 h-8 w-8 flex items-center justify-center mt-auto ${
            loading || transcribing
              ? "dark:bg-[#676767] bg-[#d7d7d7] text-[#f4f4f4]"
              : recording
              ? "bg-red-500 text-white"
              : "dark:bg-white bg-black text-white dark:text-black dark:hover:bg-slate-300"
          } rounded-full`}
        >
          <MicrophoneIcon className="w-5 h-5" />
        </motion.button>

        {/* UPLOAD BUTTON */}
        <button
          type="button"
          onClick={() => document.getElementById("document_upload").click()}
          className="px-3 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition"
        >
          Upload PDF
        </button>

        {/* HIDDEN INPUT */}
        <input
          id="document_upload"
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={handleDocumentUpload}
        />
      </form>
    </motion.div>
  );
};

export default InputArea;
