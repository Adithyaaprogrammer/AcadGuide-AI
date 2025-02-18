import { AI_BOT } from "../utils/constants";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className=" min-h-screen bg-gradient-to-b from-gray-200 to-amber-200 text-white overflow-hidden">
      <main className="flex flex-col items-center justify-center min-h-screen text-center px-6">
        <div className="max-w-3xl">
          <h1 className="text-5xl font-bold mb-6 text-orange-400">
            Welcome to StudySmart AI
          </h1>
          <p className="text-lg text-black mb-8">
            Your AI-powered study companion for smarter learning.  
            Get personalized study plans, real-time assistance, and track your progress effectively.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link 
              to="/student-dashboard"
              className="px-6 py-3 bg-green-600 text-lg font-semibold rounded-full hover:bg-green-700 transition shadow-lg"
            >
              Continue as Student
            </Link>
            <Link 
              to="/instructor-dashboard"
              className="px-6 py-3 bg-green-600 text-lg font-semibold rounded-full hover:bg-green-700 transition shadow-lg"
            >
              Continue as Instructor
            </Link>
          </div>
        </div>

        <div className="mt-12 relative">
          <img src={AI_BOT} alt="AI_BOT" className="mt-10 w-52 h-44 animate-bounce"/>
        </div>
      </main>
    </div>
  );
};

export default Home;
