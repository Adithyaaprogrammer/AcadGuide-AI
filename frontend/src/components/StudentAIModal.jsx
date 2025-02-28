import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Send, X } from "lucide-react";

const ChatbotModal = ({ onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim() !== "") {
      setMessages([...messages, { text: input, sender: "user" }]);
      setInput("");
      setTimeout(() => {
        setMessages((prev) => [...prev, { text: "AI: " + input, sender: "ai" }]);
      }, 1000);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center mt-18 z-20 justify-center" style={{ backgroundColor: "rgba(0, 0, 0, 0.6)" }}>
      <div className="bg-white p-6 rounded-lg w-full max-w-lg flex flex-col h-4/5 shadow-lg">
        <div className="flex justify-between items-center mb-4 border-b pb-2">
          <h2 className="text-xl font-bold">Student AI Chatbot</h2>
          <button onClick={onClose} className="text-red-500 hover:text-red-700">
            <X size={24} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto border p-3 rounded mb-4 bg-gray-50 space-y-2">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-3 max-w-xs rounded-lg ${
                msg.sender === "user" ? "bg-orange-400 text-white self-end ml-auto" : "bg-gray-300 text-black self-start mr-auto"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className="flex items-center border-t pt-3">
          <input
            type="text"
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-orange-500"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage} className="bg-orange-500 text-white p-2 rounded-lg ml-2 hover:bg-orange-600">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

const StudentAIModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleAIButtonClick = (event) => {
      const allowedRoutes = ["/student-dashboard", "/course-page"];
      const isCoursePath = location.pathname.startsWith("/course/");

      if (allowedRoutes.includes(location.pathname) || isCoursePath) {
        setIsOpen(true);
      } else {
        console.log("AI Chatbot not allowed on this page");
      }
    };

    window.addEventListener("AIButtonClick", handleAIButtonClick);
    return () => {
      window.removeEventListener("AIButtonClick", handleAIButtonClick);
    };
  }, [location.pathname]);

  return <>{isOpen && <ChatbotModal onClose={() => setIsOpen(false)} />}</>;
};

export default StudentAIModal;
