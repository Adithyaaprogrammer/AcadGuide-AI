import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const CoursePage = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]); // Store fetched courses

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/courses", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Failed to fetch courses");
        }

        const data = await response.json();
        console.log("Fetched Courses:", data);

        // Map API response to match expected format
        setCourses(data.map((course) => ({ id: course.id, name: course.title })));

      } catch (error) {
        console.error("Error fetching courses:", error.message);
      }
    };

    fetchCourses();
  }, []);

  return (
    <div className="min-h-screen ml-16 flex flex-col items-left p-6 m-14">
      <h1 className="text-4xl font-bold mb-6">My Current Courses</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-10">
        {courses.length > 0 ? (
          courses.map((course) => (
            <div
              key={course.id}
              onClick={() => navigate(`/course/${course.name}`)}
              className="bg-orange-200 p-6 rounded-lg text-center text-2xl shadow-xl font-semibold w-80 h-32 flex items-center justify-center cursor-pointer hover:bg-orange-300 transition"
            >
              {course.name}
            </div>
          ))
        ) : (
          <p className="text-lg">Loading courses...</p>
        )}
      </div>
    </div>
  );
};

export default CoursePage;
