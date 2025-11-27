import React from "react";
import { motion } from "framer-motion";
import ChatBotIcon from "./icons/ChatBotIcon";
import MarkdownRenderer from "./MarkdownRenderer";

const MessageItem = ({ message }) => {
  const isUser = message.sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      {isUser ? (
        <>
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl rounded-3xl px-4 py-2 bg-secondaryColorLight dark:bg-secondaryColorDark text-black dark:text-white"
          >
            <MarkdownRenderer
              message={message}
              classStyles={"text-base leading-loose"}
            />
          </motion.div>
        </>
      ) : (
        <>
          <div className="w-full flex items-start gap-4 rounded-3xl px-4 py-2 text-gray-800 dark:text-white">
            <div className="w-[24px] h-[24px] pt-1">
              <ChatBotIcon model={message.sender} />
            </div>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1.5 }}
              className="w-full overflow-x-auto"
            >
              <MarkdownRenderer
                message={message}
                classStyles={"text-base leading-loose"}
              />
            </motion.div>
          </div>
        </>
      )}
    </div>
  );
};

export default MessageItem;
