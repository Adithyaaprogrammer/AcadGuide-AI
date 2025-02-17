import { Link } from "react-router-dom";
import { AI_BOT } from "../utils/constants";
import { Menu, ChevronLeft } from "lucide-react";
import { useState } from "react";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className={`fixed left-0 h-screen ${isCollapsed ? "w-[60px]" : "w-[175px]"} bg-orange-300 text-black p-5 shadow-lg transition-all duration-300`}>
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)} 
        className="absolute top-5 right-[-20px] bg-orange-400 p-1 rounded-full shadow-md"
      >
        {isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
      </button>

      <nav className={`mt-14 space-y-4 ${isCollapsed ? "text-center" : ""}`}>
        <ul className="text-xl font-medium">
          <li>
            <Link to="/home" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Home"}
            </Link>
          </li>
          <li>
            <Link to="/course-page" className="block p-2 rounded hover:underline">
              {!isCollapsed && "My Courses"}
            </Link>
          </li>
          <li>
            <Link to="/login" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Projects"}
            </Link>
          </li>
          <li>
            <Link to="/student-dashboard" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Dashboard"}
            </Link>
          </li>
          <li className="mt-96">
            <div className="flex flex-col items-center">
              {!isCollapsed && <Link to="/ai-agent">
                <img 
                  src={AI_BOT} 
                  alt="AI_BOT" 
                  className={"transition-all duration-300 w-28 h-24 animate-hop"} 
                />
              </Link>}
              <Link to="/ai-agent" className="block text-lg font-medium p-2 rounded hover:underline">
                {!isCollapsed && "StudySmart AI"}
              </Link>
            </div>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
