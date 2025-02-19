import { useNavigate } from "react-router-dom";

const courses = [
  { id: 1, name: "SystemCommands" },
  { id: 2, name: "Java" },
  { id: 3, name: "Python" },
];

const CoursePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen ml-16 flex flex-col items-left p-6 m-14">
      <h1 className="text-4xl font-bold mb-6">My Current Courses</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-10">
        {courses.map((course) => (
          <div
            key={course.id}
            onClick={() => navigate(`/course/${course.name}`)}
            className="bg-orange-200 p-6 rounded-lg text-center text-2xl shadow-xl font-semibold w-80 h-100 flex items-center justify-center cursor-pointer"
          >
            {course.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoursePage;