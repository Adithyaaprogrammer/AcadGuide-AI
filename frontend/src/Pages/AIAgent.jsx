import { useState } from "react";
import { Search } from "lucide-react";

const AiAgent = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const sections = {
    student_transcript: "Display video transcript in English and native language.",
    student_resources: "Recommend resource materials for learning.",
    student_questions: "Generate important questions after entering a topic/subject.",
    instructor_errors: "List the top 10 common errors in assignments.",
    instructor_faq: "List down 20 frequent questions asked by students.",
    instructor_report: "Generate student participation report.",
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-2xl mb-6 relative">
        <input
          type="text"
          placeholder="Search AI Agent..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full p-3 pl-12 border border-gray-300 rounded-full shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg"
        />
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
      </div>

      <div className="flex flex-wrap gap-4 justify-center mb-6">
        {Object.keys(sections).map((key) => (
          <button
            key={key}
            className="bg-gray-700 text-white px-6 py-3 rounded-lg shadow-md hover:bg-gray-800"
            onClick={() => setSelectedOption(key)}
          >
            {key.replace("_", " ").replace("student", "Student").replace("instructor", "Instructor")}
          </button>
        ))}
      </div>

      <div className="w-full max-w-3xl bg-white p-6 rounded-lg shadow-md">
        {selectedOption ? (
          <p className="text-lg font-semibold text-gray-800">
            {sections[selectedOption]}
          </p>
        ) : (
          <p className="text-gray-500 text-lg text-center">Select an option above to see details.</p>
        )}
      </div>
    </div>
  );
};

export default AiAgent;
