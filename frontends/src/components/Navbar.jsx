import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { PROFILE } from "../utils/constants";

const Navbar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const updateUser = () => {
      const storedUser = localStorage.getItem("user");
      setUser(storedUser ? JSON.parse(storedUser) : null);
    };

    // Initial check
    updateUser();

    // Listen for storage changes
    window.addEventListener("storage", updateUser);

    return () => {
      window.removeEventListener("storage", updateUser);
    };
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Logout failed");
      }
    } catch (error) {
      console.error(error.message);
    } finally {
      localStorage.removeItem("user");
      window.dispatchEvent(new Event("storage"));
      setUser(null);
      navigate("/");
    }
  };

  return (
    <div className="flex justify-between bg-orange-400 p-4 items-center z-10">
      <Link to="/">
        <h1 className="text-2xl text-black font-medium font-sans">StudySmart AI</h1>
      </Link>

      {user ? (
        <div className="flex items-center space-x-4">
          <span className="text-black font-medium text-lg">{user.username}</span>
          <img src={PROFILE} alt="Profile" className="w-10 h-10 rounded-full" />
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded-lg"
          >
            Logout
          </button>
        </div>
      ) : null}
    </div>
  );
};

export default Navbar;
