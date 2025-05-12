import { useState, useEffect } from "react";
import axios from "axios";

const InstructorCoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [students, setStudents] = useState([]); // Fix: Define students state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Generate 30 students' random performance data
  const generateStudentData = () => {
    return Array.from({ length: 30 }, (_, i) => ({
      rollNumber: `STU${(i + 1).toString().padStart(2, "0")}`, // STU01, STU02...
      gradedAssignments: Math.floor(Math.random() * 6) + 5, // Random between 5-10
      performance: Math.floor(Math.random() * 41) + 60, // Random between 60-100%
    }));
  };

  // Fetch courses from API
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/courses/"
        );
        setCourses(response.data); // Expecting an array of course objects with a "title" field
      } catch (err) {
        setError("Failed to load courses. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  // Handle course click
  const handleCourseClick = (course) => {
    setSelectedCourse(course);
    setStudents(generateStudentData()); // Fix: Generate students when course is clicked
  };

  // Close dialog
  const closeDialog = () => {
    setSelectedCourse(null);
  };

  return (
    <div className="min-h-screen ml-16 flex flex-col items-left p-6 m-14">
      <h1 className="text-4xl font-bold mb-6">My Courses</h1>

      {/* Display loading or error message */}
      {loading && <p>Loading courses...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-10">
        {courses.map((course, index) => (
          <div
            key={index}
            onClick={() => handleCourseClick(course)}
            className="bg-orange-200 p-6 rounded-lg text-center text-2xl shadow-xl font-semibold w-80 h-120 flex items-center justify-center cursor-pointer hover:bg-orange-300 transition-all duration-200"
          >
            {course.title}
          </div>
        ))}
      </div>

      {/* Dialog Box */}
      {selectedCourse && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-3/4 max-h-[80vh] overflow-y-auto relative">
            {/* Close Button */}
            <button
              onClick={closeDialog}
              className="mt-4 absolute top-2 right-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-red-500"
            >
              Close
            </button>

            <h2 className="text-2xl font-bold mb-4 text-center">
              {selectedCourse.title} - Student Performance
            </h2>

            <table className="min-w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border border-gray-400 px-4 py-2">
                    Roll Number
                  </th>
                  <th className="border border-gray-400 px-4 py-2">
                    GAs Submitted
                  </th>
                  <th className="border border-gray-400 px-4 py-2">
                    Overall Performance (%)
                  </th>
                </tr>
              </thead>
              <tbody>
                {students.map((student, index) => (
                  <tr key={index} className="text-center">
                    <td className="border border-gray-400 px-4 py-2">
                      {student.rollNumber}
                    </td>
                    <td className="border border-gray-400 px-4 py-2">
                      {student.gradedAssignments}
                    </td>
                    <td className="border border-gray-400 px-4 py-2">
                      {student.performance}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default InstructorCoursePage;