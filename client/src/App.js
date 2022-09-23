import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/SignUp"
import ChatRoom from "./pages/ChatRoom"
import { ChakraProvider } from '@chakra-ui/react'


export default function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <div>
          <Routes>
            <Route path="/login" element={<Login />}>
            </Route>

            <Route path="/" element={<Login />}>
            </Route>
            <Route path="/signup" element={<Signup />}>
            </Route>
            <Route path="/chatroom" element={<ChatRoom />}>
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </ChakraProvider>
  );
}

