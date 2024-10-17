import { BrowserRouter, Route, Routes } from "react-router-dom";
import Users from "./Users/Users";
import Chatbot from "./Chatbot/Chatbot";
import Header from "../components/Shared/Header/Header";

const PageRoutes = () => {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Users />} />
        <Route path="/chatbot" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
};

export default PageRoutes;
