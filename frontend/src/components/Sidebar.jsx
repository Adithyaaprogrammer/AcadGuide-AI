import { Link } from "react-router-dom";
import { AI_BOT } from "../utils/constants";
import { Menu, ChevronLeft, ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [showStudentLinks, setShowStudentLinks] = useState(false);
  const [showInstructorLinks, setShowInstructorLinks] = useState(false);

  const toggleStudentLinks = () => {
    setShowStudentLinks(!showStudentLinks);
    setShowInstructorLinks(false);
  };

  const toggleInstructorLinks = () => {
    setShowInstructorLinks(!showInstructorLinks);
    setShowStudentLinks(false);
  };

  return (
    <div className={`fixed left-0 h-screen ${isCollapsed ? "w-[60px]" : "w-[210px]"} bg-orange-300 text-black shadow-lg transition-all duration-300`}>
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)} 
        className="absolute top-5 right-[-20px] bg-orange-400 p-1 rounded-full shadow-md"
      >
        {isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
      </button>

      <nav className={`space-y-4 ${isCollapsed ? "text-center" : ""} mt-12 ml-1`}>
        <ul className="text-lg font-medium">
          <li>
            <Link to="/home" className="block p-2 rounded hover:underline">
              {!isCollapsed && "Home"}
            </Link>
          </li>

          <li>
            <button 
              className="flex items-center w-full p-2 hover:underline my-3"
              onClick={toggleStudentLinks}
            >
              {!isCollapsed && (
                <>
                  Student Section {showStudentLinks ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                </>
              )}
            </button>
            {showStudentLinks && !isCollapsed && (
              <ul className="pl-6 space-y-2">
                <li><Link to="/course-page" className="block hover:underline">Student Courses</Link></li>
                <li><Link to="/student-dashboard" className="block hover:underline mb-3">Student Dashboard</Link></li>
              </ul>
            )}
          </li>

          <li>
            <button 
              className="flex items-center w-full p-2 hover:underline my-3"
              onClick={toggleInstructorLinks}
            >
              {!isCollapsed && (
                <>
                  Instructor Section {showInstructorLinks ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                </>
              )}
            </button>
            {showInstructorLinks && !isCollapsed && (
              <ul className="pl-6 space-y-2">
                <li><Link to="/instructor-course-page" className="block hover:underline">Instructor Courses</Link></li>
                <li><Link to="/instructor-dashboard" className="block hover:underline">Instructor Dashboard</Link></li>
              </ul>
            )}
          </li>

          <li className="mt-[335px] -ml-4">
            <div className="flex flex-col items-center">
              {!isCollapsed && (
                <Link to="/ai-agent">
                  <img src={AI_BOT} alt="AI_BOT" className="w-28 h-24" />
                </Link>
              )}
              <Link to="/ai-agent" className="block text-lg font-medium p-2 hover:underline">
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
