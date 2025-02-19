import { useParams } from "react-router-dom";
import { useState } from "react";

const coursesData = {
    SystemCommands : [
        { week: 1, video: "https://www.youtube.com/embed/gSyKCrnjyWg" },
        { week: 2, video: "https://www.youtube.com/embed/LlydR4bEq4U" },
        { week: 3, video: "https://www.youtube.com/embed/TwkA_QtJuB8" },
        { week: 4, video: "https://www.youtube.com/embed/fAa__NWlxWI" },
        { week: 5, video: "https://www.youtube.com/embed/NaRHcdCyh1g" },
        { week: 6, video: "https://www.youtube.com/embed/x4FWYCGGzrE" },
        { week: 7, video: "https://www.youtube.com/embed/x-3hGdoUpew" },
        { week: 8, video: "https://www.youtube.com/embed/xSaYz6xdEWU" },
    ],
    Java : [
        { week: 1, video: "https://www.youtube.com/embed/-26R6VNvu3w", transcripts: { English: "Week 1 Transcript" } },
        { week: 2, video: "https://www.youtube.com/embed/hIXkZuAOD34", transcripts: { English: "Week 2 Transcript" } },
        { week: 3, video: "https://www.youtube.com/embed/hl0Fe5mjYLA", transcripts: { English: "Week 3 Transcript" } },
        { week: 4, video: "https://www.youtube.com/embed/l5YSuL2kgXI", transcripts: { English: "Week 4 Transcript" } },
        { week: 5, video: "https://www.youtube.com/embed/xmr0PuUSeR4", transcripts: { English: "Week 5 Transcript" } }, 
        { week: 6, video: "https://www.youtube.com/embed/RU0_VGXS02w", transcripts: { English: "Week 6 Transcript" } },
        { week: 7, video: "https://www.youtube.com/embed/qv8GQ0NyV1M", transcripts: { English: "Week 7 Transcript" } },
        { week: 8, video: "https://www.youtube.com/embed/pqFTTBhEwQQ", transcripts: { English: "Week 8 Transcript" } },
        { week: 9, video: "https://www.youtube.com/embed/vApT7nEYYco", transcripts: { English: "Week 9 Transcript" } },
        { week: 10, video: "https://www.youtube.com/embed/T76Z59-h2ks", transcripts: { English: "Week 10 Transcript" } },
        { week: 11, video: "https://www.youtube.com/embed/ug3CIqvCH28", transcripts: { English: "Week 11 Transcript" } },
    ],
    Python : [
        { week: 1, video: "https://www.youtube.com/embed/T4qSGMIibzM", transcripts: { English: "Week 1 Transcript" } },
        { week: 2, video: "https://www.youtube.com/embed/7n8lr5z6YD0", transcripts: { English: "Week 2 Transcript" } },
        { week: 3, video: "https://www.youtube.com/embed/x3SYWAXLfM8", transcripts: { English: "Week 3 Transcript" } },
        { week: 4, video: "https://www.youtube.com/embed/w0NGGalpVeQ", transcripts: { English: "Week 4 Transcript" } },
        { week: 5, video: "https://www.youtube.com/embed/pvk7OHXiyCw", transcripts: { English: "Week 5 Transcript" } }, 
        { week: 6, video: "https://www.youtube.com/embed/Sn2OyKK4dU0", transcripts: { English: "Week 6 Transcript" } },
        { week: 7, video: "", transcripts: { English: "Week 7 Transcript" } },
        { week: 8, video: "https://www.youtube.com/embed/ODMWis6i9AY", transcripts: { English: "Week 8 Transcript" } },
        { week: 9, video: "https://www.youtube.com/embed/6LRW0ZADm1g", transcripts: { English: "Week 9 Transcript" } },
        { week: 10, video: "https://www.youtube.com/embed/-NqbCbjKJIE", transcripts: { English: "Week 10 Transcript" } },
        { week: 11, video: "https://www.youtube.com/embed/iKIwg1aLY38", transcripts: { English: "Week 11 Transcript" } },
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
    console.log(useParams());
    const courseKey = Object.keys(coursesData).find(key =>key === name);
    const course = courseKey ? coursesData[courseKey] : [];

    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [selectedLanguage, setSelectedLanguage] = useState("English");
    const [videoUrl, setVideoUrl] = useState("");
    const [selectedWeek, setSelectedWeek] = useState(null);

    const toggleWeek = (week, video) => {
        setSelectedWeek(selectedWeek === week ? null : week);
        setVideoUrl(video || "");
    };

    return (
        <div className="flex">

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

            <main className="flex-grow p-10 ml-32">
                <h2 className="text-xl font-semibold">
                    {courseKey || name} : {selectedWeek ? `Week ${selectedWeek} Content` : "Select a Week"}
                </h2>
                {videoUrl && (
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
                {selectedWeek && (
                    <button className="bg-blue-500 text-white px-4 py-2 mt-4 rounded" onClick={() => setIsDialogOpen(true)}>
                        View Transcript
                    </button>
                )}
            </main>
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
        </div>
    );
};

export default SpecificCoursePage;