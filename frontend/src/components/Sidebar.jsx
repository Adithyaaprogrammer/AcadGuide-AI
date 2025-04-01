import { Link } from "react-router-dom";
import { Menu, ChevronLeft } from "lucide-react";
import { useState, useEffect } from "react";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const updateUser = () => {
      const storedUser = localStorage.getItem("user");
      setUser(storedUser ? JSON.parse(storedUser) : null);
    };

    updateUser();
    window.addEventListener("storage", updateUser);

    return () => {
      window.removeEventListener("storage", updateUser);
    };
  }, []);

  const navItems = {
    student: [
      { path: "/home", label: "Home" },
      { path: "/course-page", label: "Student Courses" },
      { path: "/student-dashboard", label: "Student Dashboard" },
    ],
    instructor: [
      { path: "/home", label: "Home" },
      { path: "/instructor-course-page", label: "Instructor Courses" },
      { path: "/instructor-dashboard", label: "Instructor Dashboard" },
    ],
  };

  const userRole = user?.role;

  return (
    <div
      className={`fixed top-0 left-0 h-screen z-0 ${
        isCollapsed ? "w-[60px]" : "w-[210px]"
      } bg-orange-300 text-black shadow-lg transition-all duration-300`}
    >
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute top-28 right-[-20px] bg-orange-400 p-1 rounded-full shadow-md"
      >
        {isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
      </button>

      <nav className={`space-y-4 ${isCollapsed ? "text-center" : ""} mt-32 ml-1`}>
        <ul className="text-lg font-medium">
          {navItems[userRole]?.map((item) => (
            <li key={item.path}>
              <Link to={item.path} className="block p-2 rounded hover:underline">
                {!isCollapsed && item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
