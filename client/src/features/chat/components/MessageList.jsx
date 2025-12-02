import React, { forwardRef } from "react";
import { motion } from "framer-motion";
import MessageItem from "./MessageItem";
import MessageItemSkeleton from "./skeletons/MessageItemSkeleton";
import { PlusIcon, RefreshIcon } from "@heroicons/react/outline";

const MessageList = forwardRef(
  (
    {
      loading,
      messages,
      selectedModel,
      isCollapsed,
      selectedChat,
      handleCreateNewChat,
      chatLoading,
    },
    ref
  ) => {
    return (
      <motion.div
        ref={ref}
        className={`  ${
          chatLoading && "flex justify-center items-center"
        } flex-1 overflow-y-auto pt-4 pb-8 space-y-4 ${
          isCollapsed
            ? "px-4 sm:px-8 md:px-[7rem] lg:px-[16rem] xl:px-[21rem]"
            : "px-4 sm:px-8 md:px-[4rem] lg:px-[8.5rem] xl:px-[12rem]"
        }`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-500 dark:text-gray-400">
              {selectedChat ? (
                <>
                  <h2 className="text-2xl font-bold mb-2">
                    Welcome to AI Chatbot!
                  </h2>
                  <p className="text-lg">
                    Start a conversation by typing a message below.
                  </p>
                </>
              ) : (
                <>
                  <h2 className="text-2xl font-bold mb-2">
                    Start a conversation in a new chat!
                  </h2>
                  <p className="text-lg mb-4">
                    Click the button below to start a new chat.
                  </p>
                  <button
                    onClick={handleCreateNewChat}
                    className="inline-flex items-center gap-2 bg-black dark:bg-white text-white dark:text-black font-semibold px-4 py-2 rounded-lg"
                  >
                    <PlusIcon className="h-5 w-5 " />
                    <span>New Chat</span>
                  </button>
                </>
              )}
            </div>
          </div>
        ) : (
          <>
            {chatLoading ? (
              <>
                <div className="spinner"></div>
              </>
            ) : (
              messages.map((message) => (
                <MessageItem
                  loading={loading}
                  key={message.id}
                  message={message}
                />
              ))
            )}
          </>
        )}

        {/* Skeleton loader indicating response generation */}
        {loading && <MessageItemSkeleton selectedModel={selectedModel} />}
      </motion.div>
    );
  }
);

export default MessageList;
