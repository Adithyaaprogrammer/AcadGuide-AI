
const courses = [
  { id: 1, name: "Data Structures and Algorithms" },
  { id: 2, name: "Web Development" },
  { id: 3, name: "Machine Learning" },
  { id: 4, name: "Cloud Computing" },
];

const CoursePage = () => {
  return (
    <div className="min-h-screen ml-16 bg-gray-100 flex flex-col items-left p-6 m-14">
      <h1 className="text-4xl font-bold mb-6">My Current Courses</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-10">
        {courses.map((course) => (
          <div
            key={course.id}
            className="bg-orange-200 p-6 rounded-lg text-center text-2xl shadow-xl font-semibold w-80 h-100 flex items-center justify-center"
          >
            {course.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoursePage;