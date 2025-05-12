import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { X } from "lucide-react";

const ChatbotModal = ({ onClose }) => {
  const [response, setResponse] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAIResponse = async () => {
    setLoading(true);

    try {
      const aiResponse = await fetch("http://localhost:8000/api/ai/common_errors_faqs");
      const data = await aiResponse.json();
      setResponse(data.top_5_faqs || []);
    } catch (error) {
      setResponse([]);
    }

    setLoading(false);
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
          {loading ? (
            <p>Loading...</p>
          ) : (
            response.length > 0 ? (
              response.map((faq, index) => (
                <div key={index} className="p-2 border-b">
                  <p className="font-semibold">Q: {faq.question}</p>
                  <p className="text-gray-700">A: {faq.answer}</p>
                </div>
              ))
            ) : (
              <p>No response received.</p>
            )
          )}
        </div>
        <div className="flex items-center border-t pt-3">
          <button onClick={fetchAIResponse} className="bg-orange-500 text-white p-2 rounded-lg w-full hover:bg-orange-600" disabled={loading}>
            {loading ? "Loading..." : "FAQs"}
          </button>
        </div>
      </div>
    </div>
  );
};

const InstructorAIModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleAIButtonClick = (event) => {
      const allowedRoutes = ["/instructor-dashboard", "/instructor-course-page"];

      if (allowedRoutes.includes(location.pathname)) {
        setIsOpen(true);
      }
    };

    window.addEventListener("AIButtonClick", handleAIButtonClick);
    return () => {
      window.removeEventListener("AIButtonClick", handleAIButtonClick);
    };
  }, [location.pathname]);

  return <>{isOpen && <ChatbotModal onClose={() => setIsOpen(false)} />}</>;
};

export default InstructorAIModal;
