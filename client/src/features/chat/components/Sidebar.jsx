import React, { useState } from "react";
import { motion } from "framer-motion";
import { MenuIcon, PlusIcon } from "@heroicons/react/solid";
import { format, differenceInDays } from "date-fns";
import SidebarItem from "./SidebarItem";

const Sidebar = ({
  chats,
  handleCreateNewChat,
  handleSelectChat,
  selectedChat,
  isCollapsed,
  toggleCollapse,
  handleDeleteChat,
}) => {
  // Sort chats in descending order by date
  const sortedChats = [...chats].sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );

  const getLabel = (date) => {
    const diff = differenceInDays(new Date(), new Date(date));
    if (diff === 0) return "Today";
    if (diff === 1) return "Yesterday";
    return format(new Date(date), "MMMM dd, yyyy");
  };

  return (
    <motion.div
      className={`overflow-y-auto transition-width bg-sidebarColorLight dark:bg-sidebarColorDark shadow-md fixed top-0 left-0 z-10 h-full xs:static ${
        isCollapsed ? "w-0" : "w-full xs:w-5/12 sm:w-2/12 md:w-3/12 lg:w-2/12"
      }`}
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <>
        <div className="p-4">
          <div className="flex gap-2 mb-4">
            <button
              onClick={toggleCollapse}
              className="bg-primaryColorLight dark:bg-primaryColorDark text-black dark:text-white p-2 rounded-lg"
            >
              <MenuIcon className="h-5 w-5" />
            </button>

            <button
              onClick={handleCreateNewChat}
              className="bg-primaryColorLight dark:bg-primaryColorDark text-black dark:text-white p-2 rounded-lg"
            >
              <PlusIcon className="h-5 w-5" />
            </button>
          </div>

          <div className="space-y-2 text-sm">
            {sortedChats.map((chat, index) => {
              const showLabel =
                index === 0 ||
                getLabel(chat.created_at) !==
                  getLabel(sortedChats[index - 1].created_at);
              return (
                <SidebarItem
                  key={index}
                  handleDeleteChat={handleDeleteChat}
                  chat={chat}
                  getLabel={getLabel}
                  handleSelectChat={handleSelectChat}
                  showLabel={showLabel}
                  selectedChat={selectedChat}
                />
              );
            })}
          </div>
        </div>
      </>
    </motion.div>
  );
};

export default Sidebar;
