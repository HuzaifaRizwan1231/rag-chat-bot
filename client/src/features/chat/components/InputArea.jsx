import React from "react";
import { motion } from "framer-motion";
import { ArrowUpIcon, MicrophoneIcon } from "@heroicons/react/solid";
import { useInputArea } from "../hooks/useInputArea";

const InputArea = ({
  onSendMessage,
  loading,
  handleAudioRecording,
  recording,
  transcribing,
  isCollapsed,
}) => {
  const { input, rows, handleSubmit, handleKeyDown, handleInputChange, handleDocumentUpload, uploadDocumentLoading, uploadDocumentStatus } =
    useInputArea(onSendMessage, loading);

  return (
    <motion.div
      className={`dark:bg-secondaryColorDark bg-secondaryColorLight p-4 my-4 shadow-md mx-auto rounded-3xl ${isCollapsed ? "w-11/12 sm:w-3/4 lg:w-1/2 " : "w-11/12 sm:w-3/4 lg:w-3/5"
        }`}
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <form onSubmit={handleSubmit} className="flex gap-2">
        <textarea
          onKeyDown={handleKeyDown}
          value={input}
          onChange={handleInputChange}
          placeholder="Message AI Chatbot"
          className="flex-1 w-full rounded-lg focus:outline-none dark:bg-secondaryColorDark dark:text-white bg-secondaryColorLight text-black resize-none"
          rows={rows}
        />
        <motion.button
          disabled={loading || recording || transcribing}
          type="submit"
          className={`px-4 py-2 h-8 w-8 flex items-center justify-center mt-auto ${loading || recording || transcribing || input.length == 0
            ? "dark:bg-[#676767] dark:text-[#2f2f2f] bg-[#d7d7d7] text-[#f4f4f4]"
            : "dark:bg-white bg-black dark:text-black text-white dark:hover:bg-slate-300"
            } rounded-full focus:outline-none`}
        >
          <div>
            <ArrowUpIcon className="w-5 h-5" />
          </div>
        </motion.button>

        <motion.button
          disabled={loading || transcribing}
          type="button"
          onClick={handleAudioRecording}
          className={`px-4 py-2 h-8 w-8 flex items-center justify-center mt-auto ${loading || transcribing
            ? "dark:bg-[#676767] dark:text-[#2f2f2f] bg-[#d7d7d7] text-[#f4f4f4]"
            : recording
              ? "dark:bg-red-500 bg-red-500 dark:text-white text-white"
              : "dark:bg-white bg-black dark:text-black text-white dark:hover:bg-slate-300"
            } rounded-full focus:outline-none`}
        >
          <div>
            <MicrophoneIcon className="w-5 h-5" />
          </div>
        </motion.button>
      </form>
      <button
        type="button"
        disabled={loading || transcribing || uploadDocumentLoading}
        onClick={() => document.getElementById("document_upload").click()}
        className={`px-3 py-2 rounded-md ${uploadDocumentLoading ? 'bg-gray-300' : 'bg-blue-600 hover:bg-blue-700'}  text-white  transition`}
      >
        Upload PDF
      </button>
      <input
        id="document_upload"
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={handleDocumentUpload}
      />
      {uploadDocumentStatus &&
        <p className="text-xs !text-white">{uploadDocumentStatus}</p>
      }
    </motion.div>
  );
};

export default InputArea;
