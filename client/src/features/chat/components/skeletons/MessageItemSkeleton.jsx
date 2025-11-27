import React from "react";
import ChatBotIcon from "../icons/ChatBotIcon";
import { motion } from "framer-motion";

const MessageItemSkeleton = ({ selectedModel }) => {
  return (
    <motion.div
      className={`flex justify-start pt-1`}
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="w-full flex items-start gap-4 rounded-3xl px-4 py-2 text-gray-800 dark:text-white">
        <div className="w-[24px] h-[24px]">
          <ChatBotIcon model={selectedModel} />
        </div>
        <div className="animate-pulse flex flex-col gap-2 w-full">
          <div className="h-6 bg-secondaryColorLight dark:bg-secondaryColorDark rounded w-3/4"></div>
        </div>
      </div>
    </motion.div>
  );
};

export default MessageItemSkeleton;
