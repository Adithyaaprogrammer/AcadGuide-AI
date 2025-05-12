import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";

const StudentDashboard = () => {
  const [subjectsProgress, setSubjectsProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const progressResponse = await fetch("http://localhost:8000/student/dashboard", {
          method: "GET",
          credentials: "include",
        });

        if (!progressResponse.ok) {
          throw new Error("Failed to fetch student progress.");
        }

        const progressData = await progressResponse.json();
        setSubjectsProgress(progressData.subjects_progress);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <p className="text-center text-xl">Loading...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;

  const barChartDataAvg = subjectsProgress.map((subject) => ({
    name: subject.course_name,
    student: subject.student_progress,
    average: subject.average_progress,
  }));

  const barChartDataMedian = subjectsProgress.map((subject) => ({
    name: subject.course_name,
    student: subject.student_progress,
    median: subject.median_progress,
  }));

  return (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold text-center mb-6 mt-10">Student Dashboard</h2>

      {/* Side-by-side Charts */}
      <div className="flex flex-wrap justify-center gap-10">
        {/* Student Progress vs Average Progress */}
        <div className="bg-orange-200 p-6 rounded-lg shadow-lg w-[600px]">
          <h3 className="text-xl font-bold text-center mb-4">Your Progress vs Average Progress</h3>
          <BarChart width={550} height={400} data={barChartDataAvg}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="student" fill="#DC006A" name="Your Progress" />
            <Bar dataKey="average" fill="#00BF63" name="Average Progress" />
          </BarChart>
        </div>

        {/* Student Progress vs Median Progress */}
        <div className="bg-blue-200 p-6 rounded-lg shadow-lg w-[600px]">
          <h3 className="text-xl font-bold text-center mb-4">Your Progress vs Median Progress</h3>
          <BarChart width={550} height={400} data={barChartDataMedian}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="student" fill="#DC006A" name="Your Progress" />
            <Bar dataKey="median" fill="#007BFF" name="Median Progress" />
          </BarChart>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
