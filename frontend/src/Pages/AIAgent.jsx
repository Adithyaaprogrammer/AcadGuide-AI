import { useState } from "react";
import { Search } from "lucide-react";

const AiAgent = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const sections = {
    student_resources: "Recommending resource materials for learning.",
    student_questions: "Important questions after entering a particular topic/subject.",
    instructor_errors: "Top 10 common errors in assignments.",
    instructor_faq: "20 frequent questions asked by students.",
    instructor_report: "Generate student participation report.",
  };

  const youtubeVideos = [
    { title: "Python for Beginners", url: "https://www.youtube.com/embed/_uQrJ0TkZlc" },
    { title: "Python Full Course", url: "https://www.youtube.com/embed/rfscVS0vtbw" },
    { title: "Python in One Video", url: "https://www.youtube.com/embed/4F2m91eKmts" },
  ];

  const pythonQuestions = [
    "What are Python's key features?",
    "Explain Python's memory management.",
    "Differentiate between list and tuple.",
    "What is Python's GIL?",
    "How does Python handle memory allocation?",
    "What are Python's built-in data types?",
    "How do you manage exceptions in Python?",
    "What is the difference between deep copy and shallow copy?",
    "Explain Python decorators with an example.",
    "What are Python lambda functions?",
  ];

  const commonErrors = [
    "Using '=' instead of '==' in conditions.",
    "Indentation errors due to inconsistent spacing.",
    "Using a mutable default argument in functions.",
    "Accessing list indexes out of range.",
    "Using incorrect indentation levels in loops.",
    "Forgetting to close opened files.",
    "Forgetting colons ':' in loops or function definitions.",
    "Using undefined variables due to misspelling.",
    "Incorrect indentation in Python blocks.",
  ];

  const filteredSections = Object.keys(sections).filter((key) =>
    key.replace("_", " ").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-6 mt-10">
      <div className="w-full max-w-2xl mb-6 relative">
        <input
          type="text"
          placeholder="Search AI Agent..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full p-3 pl-12 border border-gray-300 rounded-full shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg"
        />
        <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
      </div>

      <div className="flex flex-wrap gap-4 justify-center mb-6 mt-20">
        {filteredSections.map((key) => (
          <button
            key={key}
            className="bg-gray-700 text-white px-6 py-3 rounded-lg shadow-md hover:bg-gray-800"
            onClick={() => setSelectedOption(key)}
          >
            {key.replace("_", " ").replace("student", "Student").replace("instructor", "Instructor")}
          </button>
        ))}
      </div>

      <div className="w-full max-w-4xl bg-white p-6 rounded-lg shadow-md">
        {selectedOption ? (
          <p className="text-lg font-semibold text-gray-800">{sections[selectedOption]}</p>
        ) : (
          <p className="text-gray-500 text-lg text-center">Select an option above to see details.</p>
        )}

        {selectedOption === "student_resources" && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Python Learning Resources:</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
              {youtubeVideos.map((video, index) => (
                <iframe
                  key={index}
                  className="w-full h-48 border rounded-lg"
                  src={video.url}
                  title={video.title}
                  allowFullScreen
                />
              ))}
            </div>
          </div>
        )}

        {selectedOption === "student_questions" && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Python Important Questions:</h3>
            <ul className="list-disc list-inside mt-2">
              {pythonQuestions.map((question, index) => (
                <li key={index} className="text-gray-700">{question}</li>
              ))}
            </ul>
          </div>
        )}

        {selectedOption === "instructor_errors" && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Common Mistakes in Assignments:</h3>
            <ul className="list-disc list-inside mt-2">
              {commonErrors.map((error, index) => (
                <li key={index} className="text-gray-700">{error}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AiAgent;
