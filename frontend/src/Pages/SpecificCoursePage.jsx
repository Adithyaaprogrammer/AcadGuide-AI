import { useParams } from "react-router-dom";
import { useState } from "react";

const coursesData = {
    SC : [
        { week: 1, video: "https://www.youtube.com/embed/gSyKCrnjyWg", assignment: [
            { id: 1, question: "Which directory contains the information related to host specific system configuration files?", options: ["/bin","/opt","/media","/etc"] },
          { id: 2, question: "What does the first column of the output of the following command represent? ---> ls -l", options: ["Name of the user","Name of the group","Type of files and permissions","Number of hard links"] },
          { id: 3, question: "What is the command to change the permission of the file myfile.sh such that the owner has full access, the group has read and execute access and other users have only read access?", options: ["chmod 457 myfile.sh","chmod 754 myfile.sh","chmod 751 myfile.sh","chmod 157 myfile.sh"] },
          { id: 4, question: "What is the expected output of the command? ---> date 'myfile.txt'", options: ["Displays the date at which file was last edited.","Modifies the time stamp of the file.","date: invalid date ‘myfile.txt’","None of the above"] },
        ] },
        { week: 2, video: "https://www.youtube.com/embed/LlydR4bEq4U", assignment: [
            { id: 1, question: "Write a bash command to move all the .txt files present in the current directory to the directory named level1 present inside the current directory. Do not move any other files other than .txt files anywhere from the current directory. Write only a single line bash command to perform the above task.", options: [] },
        ] },
    ],
    Java : [
        { week: 1, video: "https://www.youtube.com/embed/-26R6VNvu3w", transcripts: { English: "Week 1 Transcript" }, assignment: [
          { id: 1, question: "Consider the statements given below and Identify the correct option regarding subtyping with respect to Player objects and Captain objects. ---> Statement 1: Player is an object that has name, age and role, as its data. ---> Statement 2: Captain is an object that has name, age, role, date of appointment as a captain, and number of years of experience, as its data.", options: ["Captain can be a subtype of Player.","Player can be a subtype of Captain.","Captain cannot be a subtype of Player.","Player cannot be a subtype of Captain."] },
          { id: 2, question: "Identify the correct definition(s) of a boolean variable named flag in Java from the following.", options: ["boolean flag = 1;","boolean flag = true;","boolean flag = TRUE;","boolean flag = false;"] },
          { id: 3, question: "How is it possible to run the main method in Java without creating an object?", options: ["Java is an object oriented programming language. Thus we need to create an object of the main class, and call our main() method to run. Hence the question is fallacious.","The modifier static helps the main() method to run independently without creating an object.","The access modifier public helps the main() method to run independently without creating an object.","The main() method is an exception. It is the only method that exist independently without the dynamic creation of an object."] },
          { id: 4, question: "Consider the following abstract types and Identify the correct subtype and inheritance relationships between the classes. --->• Scanner, with method scanDocuments().--->• Printer, with method printDocuments().--->• Copier, with methods scanDocuments() and printDocuments().", options: ["Scanner and Printer are subtypes of Copier","Scanner and Printer both inherit from Copier","Copier inherits from both Scanner and Printer"] },
        ] },
        { week: 2, video: "https://www.youtube.com/embed/hIXkZuAOD34", transcripts: { English: "Week 2 Transcript" }, assignment: [
            { id: 1, question: " Write a program to accept a string input from user and print the characters at even indices.", options: [] },
        ] },
    ],
    Python : [
        { week: 1, video: "https://www.youtube.com/embed/T4qSGMIibzM", transcripts: { English: "Week 1 Transcript" }, assignment: [
            { id: 1, question: "What is the type of the following expression --->  1 + 4 / 2", options: ["int","float","str","bool"] },
            { id: 2, question: "What is the type of the following expression --->  (1 > 0) and (-1 < 0) and (1 == 1)", options: ["str","bool","True","False"] },
            { id: 3, question: "Find the number of integer-zeros of the polynomial in the range [0,4], endpoints inclusive. ---> f(x) = x^6 - 4x^5 - 18x^4 + 52x^3 + 101x^2 − 144x − 180", options: ["2","3","4","5"] },
            { id: 4, question: "What is the output of the following snippet of code? ---> L = ['one', 'two', 'one', 'three', 'one'] ---> freq = {word: L.count(word) for word in L} ---> print(freq)", options: ["{'one': 3, 'two': 1, 'three': 1}","[('one', 3), ('two', 1), ('three', 1)]","{'one': 1, 'two': 1, 'three': 1}"] },
        ] },
        { week: 2, video: "https://www.youtube.com/embed/7n8lr5z6YD0", transcripts: { English: "Week 2 Transcript" }, assignment: [
            { id: 1, question: "Accept the date in DD-MM-YYYY format as input and print the year as output.", options: [] },
        ] },
   ],
};

const languages = [
    "English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi",
    "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri",
    "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi",
    "Tamil", "Telugu", "Urdu",
  ];

const SpecificCoursePage = () => {
    const { name } = useParams();
    const courseKey = Object.keys(coursesData).find(key => key === name);
    const course = courseKey ? coursesData[courseKey] : [];

    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [selectedLanguage, setSelectedLanguage] = useState("English");
    const [videoUrl, setVideoUrl] = useState("");
    const [selectedWeek, setSelectedWeek] = useState(null);
    const [assignment, setAssignment] = useState(null);
    const [answers, setAnswers] = useState({});
    const [codeAnswer, setCodeAnswer] = useState("");
    const [viewMode, setViewMode] = useState("video");

    const toggleWeek = (weekNumber, videoUrl) => {
        setSelectedWeek(weekNumber);
        setVideoUrl(videoUrl);

        const selectedWeekData = course.find(w => w.week === weekNumber);
        if (selectedWeekData && selectedWeekData.assignment) {
            setAssignment(selectedWeekData.assignment);
        } else {
            setAssignment([]);
        }
        setViewMode("video");
    };

    const handleAnswerChange = (questionId, option) => {
        setAnswers((prevAnswers) => ({
            ...prevAnswers,
            [questionId]: option
        }));
    };

    const handleCodeChange = (event) => {
        const lines = event.target.value.split("\n");
        if (lines.length <= 100) {
            setCodeAnswer(event.target.value);
        }
    };

    const handleSubmit = () => {
        if (selectedWeek === 2) {
            console.log("Submitted Code:", codeAnswer);
        } else {
            console.log("Submitted Answers:", answers);
        }
        alert("Assignment Submitted Successfully!");
    };

    return (
        <div className="flex">
            {/* Sidebar */}
            <aside className="right-0 w-52 bg-orange-300 p-4 h-screen fixed overflow-y-auto">
                <div className="space-y-2">
                    {course.length > 0 ? (
                        course.map(week => (
                            <div key={week.week} className="bg-white p-3 text-center rounded shadow cursor-pointer">
                                <span onClick={() => toggleWeek(week.week, week.video)} className="block">
                                    {selectedWeek === week.week ? "▼" : "▶"} Week {week.week}
                                </span>
                            </div>
                        ))
                    ) : (
                        <p className="text-center text-red-600">Course not found</p>
                    )}
                </div>
            </aside>

            {/* Main Content */}
      <main className="flex-grow p-10 ml-32">
        <h2 className="text-xl font-semibold">
          {courseKey || name} : {selectedWeek ? `Week ${selectedWeek} Content` : "Select a Week"}
        </h2>

        {/* Toggle between Video & Assignment */}
        {selectedWeek && (
          <div className="mt-4 flex space-x-4">
            <button
              className={`px-4 py-2 rounded ${viewMode === "video" ? "bg-gray-300" : "bg-yellow-300"}`}
              onClick={() => setViewMode("video")}
            >
              Video
            </button>
            <button
              className={`px-4 py-2 rounded ${viewMode === "assignment" ? "bg-gray-300" : "bg-blue-300"}`}
              onClick={() => setViewMode("assignment")}
            >
              Assignment
            </button>
            <button
              className={`px-4 py-2 rounded ${viewMode === "transcript" ? "bg-gray-300" : "bg-red-300"}`}
              onClick={() => {
                setViewMode("transcript");
                setIsDialogOpen(true);
              }}
            >
              Transcript
            </button>
          </div>
        )}

        {/* Video Player */}
        {viewMode === "video" && videoUrl && (
          <div className="mt-4 rounded overflow-hidden">
            <iframe
              width="80%"
              height="450"
              title={`Week ${selectedWeek} Video`}
              src={videoUrl}
              allowFullScreen
            ></iframe>
          </div>
        )}

                {/* Assignments */}
                {viewMode === "assignment" && selectedWeek && assignment && (
                    <div className="mt-6 max-w-[1100px] max-h-[500px] overflow-y-auto scroll-smooth p-4 bg-white shadow-lg rounded-lg">
                        {selectedWeek === 1 ? (
                            // Week 1: MCQ Questions
                            <div className="space-y-6 mt-4">
                                {assignment.map((question, index) => {
        const parts = question.question.split("--->");
        return (
          <div key={question.id} className="p-4 border border-gray-300 rounded-lg bg-gray-50 shadow-md">
            <p className="font-medium text-lg text-gray-900">
          {index + 1}. {parts[0]}
        </p>

        {/* Display subsequent lines inside a gray box */}
        {parts.length > 1 && (
          <div className="mt-4 p-4 bg-gray-200 text-sm font-mono text-xl font-semibold text-grey-900 rounded-lg whitespace-pre-wrap">
            {parts.slice(1).map((line, i) => (
              <p key={i} className="mt-1">{line.trim()}</p>
            ))}
          </div>
        )}

            <div className="mt-3 space-y-2">
              {question.options.map((option, optIndex) => (
                <label
                  key={optIndex}
                  className="flex items-center space-x-3 p-2 rounded-lg cursor-pointer bg-white border border-gray-300 transition duration-200 hover:bg-gray-100"
                >
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value={option}
                    checked={answers[question.id] === option}
                    onChange={() => handleAnswerChange(question.id, option)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-gray-800">{option || "Option not provided"}</span>
                </label>
              ))}
            </div><br />
          </div>
        );
      })}
    </div>
                        ) : (
                            // Week 2: Programming Question
                            <div>
                                {assignment.map((q) => (
                                    <div key={q.id} className="mb-4">
                                        <p className="font-semibold">{q.question}</p><br /><br />
                                        <textarea
                                            value={codeAnswer}
                                            onChange={handleCodeChange}
                                            rows={10}
                                            className="w-full p-2 border rounded bg-gray-100"
                                            placeholder="Write your code here..."
                                        />
                                        <p className="text-sm text-gray-500">{codeAnswer.split("\n").length} / 100 lines</p>
                                    </div>
                                ))}
                            </div>
                        )}

                        <button onClick={handleSubmit} className="mt-4 px-6 py-2 bg-green-500 text-white rounded">
                            Submit Assignment
                        </button><br /><br />
                    </div>
                )}

                {/* Open Transcript Dialog */}
        {viewMode === "transcript" && (
            <div><br /><br /><div className="mt-2 max-w-[1100px] p-2 border">
              {course.find(w => w.week === selectedWeek)?.transcripts?.English || "Transcript not available"}
            </div></div>
          )}

{isDialogOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded shadow-lg w-1/3">
            <h3 className="text-lg font-bold mb-4">Transcripts for Week {selectedWeek}</h3>
            <label className="block mb-2">Select Language:</label>
            <select
              className="w-full p-2 border rounded"
              value={selectedLanguage}
              onChange={e => setSelectedLanguage(e.target.value)}
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
            <button className="mt-4 bg-red-500 text-white px-4 py-2 rounded" onClick={() => setIsDialogOpen(false)}>
              Close
            </button>
          </div>
        </div>
      )}

            </main>
        </div>
    );
};

export default SpecificCoursePage;