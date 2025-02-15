import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X } from "lucide-react";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(true);

  return (
    <>
      <button
        className="p-3 -mt-2 text-black fixed top-4 left-2 z-50"
        onClick={() => setCollapsed(!collapsed)}
      >
        {collapsed ? <Menu size={24} /> : null}
      </button>

      <div
        className={`fixed top-0 left-0 h-screen bg-gray-800 text-white p-5 transition-transform duration-300 ${
          collapsed ? "-translate-x-full" : "translate-x-0"
        } w-52 shadow-lg absolute z-40`}
      >
        <button
          className="absolute top-4 right-4 text-white"
          onClick={() => setCollapsed(true)}
        >
          <X size={24} className="mt-2"/>
        </button>
        <h2 className="text-xl font-bold mb-5">Menu</h2>
        <nav>
          <ul className="space-y-3 mt-10">
            <li>
              <Link to="/course-page" className="block p-2 rounded hover:bg-gray-700" onClick={() => setCollapsed(true)}>My Courses</Link>
            </li>
            <li>
              <Link to="/login" className="block p-2 rounded hover:bg-gray-700" onClick={() => setCollapsed(true)}>Projects</Link>
            </li>
            <li>
              <Link to="/student-dashboard" className="block p-2 rounded hover:bg-gray-700" onClick={() => setCollapsed(true)}>Dashboard</Link>
            </li>
            <li>
              <Link to="/ai-agent" className="block p-2 rounded hover:bg-gray-700" onClick={() => setCollapsed(true)}>StudySmart AI</Link>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default Sidebar;
