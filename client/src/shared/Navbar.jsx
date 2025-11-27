import React, { useState } from "react";
import { motion } from "framer-motion";
import { SunIcon, MoonIcon, MenuIcon, PlusIcon } from "@heroicons/react/solid";

const Navbar = ({
  darkMode,
  toggleDarkMode,
  selectedModel,
  setSelectedModel,
  modelOptions,
  toggleCollapse,
  isCollapsed,
  handleCreateNewChat,
}) => {
  return (
    <nav className="bg-primaryColorLight dark:bg-primaryColorDark shadow-md">
      <div className="mx-auto px-4 sm:px-4 lg:px-4">
        <div className="flex flex-col items-center sm:flex-row justify-between py-4">
          <div className="items-center text-center sm:text-left sm:justify-start justify-center w-full sm:w-1/3 mb-2 sm:mb-0">
            <span className="text-2xl gap-4 flex items-center font-bold text-gray-800 dark:text-white">
              {isCollapsed && (
                <div className="flex gap-2">
                  <button
                    onClick={toggleCollapse}
                    className="p-2 rounded-lg bg-secondaryColorLight dark:bg-secondaryColorDark text-gray-800 dark:text-white"
                  >
                    <MenuIcon className="h-5 w-5" />
                  </button>

                  <button
                    onClick={handleCreateNewChat}
                    className="p-2 rounded-lg bg-secondaryColorLight dark:bg-secondaryColorDark text-gray-800 dark:text-white"
                  >
                    <PlusIcon className="h-5 w-5" />
                  </button>
                </div>
              )}
              <span className="text-nowrap">AI Chatbot</span>
            </span>
          </div>
          <div className="flex items-center w-full sm:w-2/3">
            <div className="flex w-1/2 justify-start sm:justify-center">
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="p-2 rounded bg-secondaryColorLight dark:bg-secondaryColorDark text-gray-800 dark:text-white w-full sm:w-auto"
              >
                {modelOptions
                  .filter((option) => option.enable)
                  .map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
              </select>
            </div>
            <div className="flex w-1/2 justify-end ">
              <motion.button
                onClick={toggleDarkMode}
                className="p-2 rounded-full bg-secondaryColorLight dark:bg-secondaryColorDark text-gray-800 dark:text-white"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {darkMode ? (
                  <SunIcon className="h-6 w-6" />
                ) : (
                  <MoonIcon className="h-6 w-6" />
                )}
              </motion.button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
