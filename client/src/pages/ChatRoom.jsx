import { useEffect, useState, useRef, useId } from "react";
import { io } from "socket.io-client";
import { Link, useNavigate } from "react-router-dom";
import Message from "./Message";
import Header from "./Header";
import services from "../services";


export default function ChatRoom() {
    const navigate = useNavigate();
    const [user_email, setUserEmail] = useState("")

    const loadSocketInstance = function () {
        const env = "Prod";
        const token = "?jwt=" + localStorage.getItem('token');
        let socket = null;
        if (env === "Dev") {
            let url = "localhost:5000/"
            socket = io(url + token, {
                transports: ["websocket"],
                cors: {
                    origin: "http://localhost:3000/",
                },
            });
        } else {
            socket = io("/" + token, {
                transports: ["websocket"],
            });
        }
        setSocketInstance(socket);
    }

    const gethistory = function () {
        services.fetch_auth("chatlog").then(data => {
            console.log(data);
            setHistory(data.data.filter(d => d.type === "chat"));
        });;
    }

    const fetchUser = function () {
        services.fetch_auth("users").then(data => {
            setUserEmail(data.data)
        });
    }


    const [socket, setSocketInstance] = useState(null);
    const [token, setToken] = useState(null);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [history, setHistory] = useState([]);

    const scrollRef = useRef();
    useEffect(() => {
        scrollRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    const handleText = (e) => {
        const inputMessage = e.target.value;
        setMessage(inputMessage);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!message) return;

        socket.emit("data", message);
        setMessage("");
    };

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        setToken(null);
    }

    useEffect(() => {
        setToken(localStorage.getItem('token'))
        fetchUser();
        loadSocketInstance();
        gethistory();
    }, [])
    useEffect(() => {
        if (socket) {
            socket.on("connect", (data) => {
                console.log(data);
            });
            socket.on("disconnect", (data) => {
                console.log(data);
            });
            socket.on("data", (data) => {
                console.log(data, messages);
                setMessages([...messages, { ...data }]);
            });
            return () => {
                socket.off("data", () => {
                    console.log("data event was removed");
                });
            };
        }
    }, [socket, messages]);

    useEffect(() => {
        if (!localStorage.getItem('token')) {
            navigate("/login");
        }
    }, [token])

    return (
        token && user_email && <div className="pt-2">
            <Header prop={user_email}></Header>
            <div className="container mx-auto">
                <div className="min-w-full bg-pink border-x border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700 rounded lg:grid lg:grid-cols-1">
                    <div className="bg-white border-r border-gray-200 dark:bg-gray-900 dark:border-gray-700 lg:col-span-1">
                        <div className="relative w-full p-6 overflow-y-auto h-[30rem] bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700">
                            <div className="lg:col-span-2 lg:block">
                                <div className="w-full">
                                    <div className="relative w-full p-6 overflow-y-auto h-[30rem] bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700">

                                        <ul className="space-y-2">

                                            {history.map((message, idx) => {
                                                return <Message message={message} ind={idx} user_email={user_email} />
                                            })}

                                        </ul>
                                    </div>
                                    <ul className="space-y-2">
                                        {messages.map((message, ind) => {
                                            return <Message message={message} ind={ind} user_email={user_email} />
                                        })}
                                    </ul>
                                </div >
                            </div >
                            <div ref={scrollRef} />
                        </div >
                        <form onSubmit={handleSubmit}>
                            <div className="flex items-center justify-between w-full p-3 bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700">
                                <input
                                    type="text"
                                    placeholder="Write a message"
                                    className="block w-full py-2 pl-4 mx-3 outline-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                    name="message"
                                    required
                                    value={message}
                                    onChange={handleText}
                                />
                                <button type="submit" className="h-6 text-blue-600 dark:text-blue-500"
                                    aria-hidden="true"> Submit
                                </button>
                            </div>
                        </form>

                    </div >
                </div>
            </div>
            <form onSubmit={handleLogout}>
                <div className=" flex items-center justify-center pt-8">
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full transform -translate-y-6 ">
                        Logout
                    </button>
                </div>
            </form>
        </div>
    );
}