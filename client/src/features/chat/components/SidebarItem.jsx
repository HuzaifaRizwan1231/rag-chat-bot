import React, { useEffect, useRef, useState } from "react";
import { DotsHorizontalIcon, TrashIcon } from "@heroicons/react/outline";

const SidebarItem = ({
  chat,
  getLabel,
  handleSelectChat,
  handleDeleteChat,
  showLabel,
  selectedChat,
}) => {
  const [showOptions, setShowOptions] = useState(false);
  const [showIcon, setShowIcon] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  const optionsRef = useRef(null);
  const prevTitleRef = useRef(chat.title);

  const toggleOptions = () => {
    setShowOptions(!showOptions);
  };

  const handleClickOutside = (event) => {
    if (optionsRef.current && !optionsRef.current.contains(event.target)) {
      setShowOptions(false);
    }
  };

  useEffect(() => {
    if (showOptions) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showOptions]);

  //   useEffect(() => {
  //     // if previous title was null but it has set to a new title
  //     if (!prevTitleRef.current && chat.title) {
  //       setIsTyping(true);
  //       const timer = setTimeout(() => {
  //         setIsTyping(false);
  //       }, 2000); // Duration of the typing animation

  //       return () => clearTimeout(timer);
  //     }
  //     prevTitleRef.current = chat.title;
  //   }, [chat.title]);

  return (
    <>
      {showLabel && (
        <div className="text-black text-nowrap dark:text-white font-semibold px-2">
          {getLabel(chat.created_at)}
        </div>
      )}
      <div
        title={chat.title ? chat.title : "New Chat"}
        onMouseEnter={() => setShowIcon(true)}
        onMouseLeave={() => setShowIcon(false)}
        onClick={() => handleSelectChat(chat)}
        className={`relative flex justify-between items-center p-2 text-nowrap dark:text-white text-black ${
          chat.id === selectedChat?.id &&
          "bg-primaryColorLight dark:bg-primaryColorDark"
        } rounded-lg cursor-pointer hover:bg-primaryColorLight dark:hover:bg-primaryColorDark`}
      >
        <span className={`truncate ${isTyping ? "typing-animation" : ""}`}>
          {chat.title ? chat.title : "New Chat"}
        </span>
        <div className="relative">
          <DotsHorizontalIcon
            className={`h-5 w-5 ml-2 cursor-pointer opacity-0 ${
              showIcon && "opacity-100"
            }`}
            onClick={(e) => {
              e.stopPropagation();
              toggleOptions();
            }}
          />
          {showOptions && (
            <div
              ref={optionsRef}
              className="absolute right-0 mt-4 w-32 bg-primaryColorLight dark:bg-primaryColorDark hover:bg-secondaryColorLight dark:hover:bg-secondaryColorDark shadow-lg rounded-lg z-30"
            >
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteChat(chat.id);
                  setShowOptions(false);
                }}
                className="flex items-center px-4 py-2 text-sm text-red-600 dark:text-red-400 w-full"
              >
                <TrashIcon className="h-5 w-5 mr-2" />
                Delete
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default SidebarItem;
