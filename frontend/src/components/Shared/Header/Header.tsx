import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="bg-gray-800 p-4">
      <nav className="max-w-4xl mx-auto flex justify-between">
        <Link to="/" className="text-white font-bold text-lg">
          Users
        </Link>
        <Link to="/chatbot" className="text-white font-bold text-lg">
          Chatbot
        </Link>
      </nav>
    </header>
  );
};

export default Header;
