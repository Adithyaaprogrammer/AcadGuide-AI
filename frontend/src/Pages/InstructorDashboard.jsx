import React, { useState, useEffect } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from "recharts";

// Define colors for GA bars (reuse the same pattern)
const colors = ["#DC006A", "#00BF63", "#8A2BE2", "#1E90FF", "#FF6347", "#8A2BE2"];

// Generate random student performance data
const generateRandomData = () => ({
  you: Math.floor(Math.random() * 100) + 1, // Instructor's students (1-10)
  peers: 100 - (Math.floor(Math.random() * 100) + 1), // Other students (remaining percentage)
});

const InstructorDashboard = () => {
  const [courses, setCourses] = useState([]); // Store fetched courses
  const [gaData, setGaData] = useState([]); // Bar Chart data
  const [pieData, setPieData] = useState({}); // Pie Chart data

  // Fetch courses from backend
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/courses"); // Replace with your API URL
        const fetchedCourses = response.data;

        // Generate data dynamically based on fetched courses
        const generatedGaData = [
          { name: "Your Students", ...Object.fromEntries(fetchedCourses.map(course => [course.title, generateRandomData().you])) },
          { name: "All Students", ...Object.fromEntries(fetchedCourses.map(course => [course.title, 100])) },
        ];

        const generatedPieData = fetchedCourses.reduce((acc, course) => {
          acc[course.title] = [
            { name: "Your Students", value: generateRandomData().you, color: "#FFD700", head: course.title },
            { name: "Other Students", value: generateRandomData().peers, color: "#DC006A", head: course.title },
          ];
          return acc;
        }, {});

        setCourses(fetchedCourses);
        setGaData(generatedGaData);
        setPieData(generatedPieData);
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };

    fetchCourses();
  }, []);

  return (
    <div className="ml-16 container mx-auto my-auto px-5 py-2">
      <div className="grid grid-cols-2 gap-8">

        {/* PA/GA Submission Chart */}
        <div className="space-y-4">
          <h3 className="text-2xl font-bold text-center mb-10">PAs/GAs Completed</h3>
          <div className="bg-orange-200 p-4 rounded-lg shadow-lg">
            <BarChart width={500} height={520} data={gaData} className="mx-auto">
              <XAxis dataKey="name" tick={{ fill: "black" }} />
              <YAxis tick={{ fill: "black" }} />
              <Tooltip />
              <Legend wrapperStyle={{ marginTop: "20px" }} />
              {courses.map((course, index) => (
                <Bar 
                  key={course.title} 
                  dataKey={course.title} 
                  fill={colors[index % colors.length]} 
                  name={course.title} 
                />
              ))}
            </BarChart>
          </div>
        </div>

        {/* Summary of Student Performance */}
        <div className="space-y-4">
          <h3 className="text-2xl font-bold text-center mb-10">Overall Student Performance</h3>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(pieData).map(([courseTitle, data]) => (
              <div key={courseTitle} className="bg-orange-200 p-4 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">{courseTitle}</h2>
                <div className="flex justify-center">
                  <PieChart width={200} height={200}>
                    <Pie data={data} dataKey="value" cx="50%" cy="50%" outerRadius={80}>
                      {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </div>
              </div>
            ))}
          </div><br />
        </div>

      </div>
    </div>
  );
};

export default InstructorDashboard;