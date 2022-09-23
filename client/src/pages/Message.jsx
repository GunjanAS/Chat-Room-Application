import { Avatar, Flex, Text } from "@chakra-ui/react";
import React, { useEffect, useRef } from "react";

function classNames(...classes) {
    return classes.filter(Boolean).join(" ");
}

export default function Message({ message, ind, user_email }) {
    const AlwaysScrollToBottom = () => {
        const elementRef = useRef();
        useEffect(() => elementRef.current.scrollIntoView());
        return <div ref={elementRef} />;
    };
    return (
        <>
            <li key={ind}
                className={classNames(
                    user_email !== message.user_email ? "justify-start" : "justify-end",
                    "flex")}
            >
                <div>
                    <span className="block ml-2 text-gray-500 dark:text-gray-400">
                        {message?.user_email}
                    </span>
                    <div
                    >
                        <span className={classNames(
                            user_email !== message.user_email ? "bg-red-200 block font-strong" : "bg-green-200 block font-strong", "rounded-lg pl-2")}>{message.text}</span>
                    </div>
                    <span className="block text-sm text-gray-700 dark:text-gray-400">
                        {(message.timestamp)}
                    </span>
                </div>
            </li>
        </>

    );
}
