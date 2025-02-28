import { Link } from "react-router-dom";
import { Menu, ChevronLeft } from "lucide-react";
import { useState } from "react";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

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
          <li>
            <Link to="/home" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Home"}
            </Link>
          </li>

          <li>
            <Link to="/course-page" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Student Courses"}
            </Link>
          </li>

          <li>
            <Link to="/student-dashboard" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Student Dashboard"}
            </Link>
          </li>

          <li>
            <Link to="/instructor-course-page" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Instructor Courses"}
            </Link>
          </li>

          <li>
            <Link to="/instructor-dashboard" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Instructor Dashboard"}
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
