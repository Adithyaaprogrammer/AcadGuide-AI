import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Send, X } from "lucide-react";

const ChatbotModal = ({ onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [selectedFeature, setSelectedFeature] = useState("chat");

  const sendMessage = async () => {
    if (input.trim() !== "") {
      const userMessage = { text: input, sender: "user" };
      setMessages([...messages, userMessage]);
      setInput("");
      
      let response = "";
      try {
        let aiResponse;
        let url = "http://localhost:8000/api/ai/";
        let options = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) };

        if (selectedFeature === "chat") {
          url += `answer_question?question=${encodeURIComponent(input)}`;
          options = { method: "POST", headers: { "Content-Type": "application/json" } };
        } else if (selectedFeature === "study_plan") {
          url += "generate_study_plan";
          options.body = JSON.stringify({ course_id: input, student_id: 123 });
        } else if (selectedFeature === "debugging") {
          url += "debugging_tips";
          options.body = JSON.stringify({ code: input });
        } else if (selectedFeature === "resource") {
          url += "resource_recommendation";
          options.body = JSON.stringify({ topic: input });
        } else if (selectedFeature === "structured_learning") {
          url += "structured_learning_path";
          options.body = JSON.stringify({ level: input, completed_courses: [] });
        }

        aiResponse = await fetch(url, options);
        const data = await aiResponse.json();
        response = data.answer || data.study_plan || data.tips || data.recommended_resources || "No response received.";
      } catch (error) {
        response = "Error fetching AI response.";
      }

      setMessages((prev) => [...prev, { text: "AI: " + response, sender: "ai" }]);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center mt-18 z-20 justify-center" style={{ backgroundColor: "rgba(0, 0, 0, 0.6)" }}>
      <div className="bg-white p-6 rounded-lg w-full max-w-lg flex flex-col h-4/5 shadow-lg">
        <div className="flex justify-between items-center mb-4 border-b pb-2">
          <h2 className="text-xl font-bold">AI Chatbot</h2>
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
        <div className="flex flex-col border-t pt-3 space-y-2">
          <div className="flex space-x-2">
            <button onClick={() => setSelectedFeature("chat")} className={`p-2 text-sm rounded-lg ${selectedFeature === "chat" ? "bg-orange-500 text-white" : "bg-gray-300"}`}>Chat</button>
            <button onClick={() => setSelectedFeature("study_plan")} className={`p-2 text-sm rounded-lg ${selectedFeature === "study_plan" ? "bg-orange-500 text-white" : "bg-gray-300"}`}>Study Plan</button>
            <button onClick={() => setSelectedFeature("debugging")} className={`p-2 text-sm rounded-lg ${selectedFeature === "debugging" ? "bg-orange-500 text-white" : "bg-gray-300"}`}>Debugging</button>
            <button onClick={() => setSelectedFeature("resource")} className={`p-2 text-sm rounded-lg ${selectedFeature === "resource" ? "bg-orange-500 text-white" : "bg-gray-300"}`}>Resources</button>
            <button onClick={() => setSelectedFeature("structured_learning")} className={`p-2 text-sm rounded-lg ${selectedFeature === "structured_learning" ? "bg-orange-500 text-white" : "bg-gray-300"}`}>Structured Learning</button>
          </div>
          <div className="flex items-center">
            <input
              type="text"
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-orange-500"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder={
                selectedFeature === "study_plan" ? "Enter course ID" :
                selectedFeature === "debugging" ? "Enter code snippet" :
                selectedFeature === "resource" ? "Enter topic" :
                selectedFeature === "structured_learning" ? "Enter your level" : "Type your message..."
              }
            />
            <button onClick={sendMessage} className="bg-orange-500 text-white p-2 rounded-lg ml-2 hover:bg-orange-600">
              <Send size={20} />
            </button>
          </div>
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
      const allowedRoutes = ["/home","/student-dashboard", "/course-page"];
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
