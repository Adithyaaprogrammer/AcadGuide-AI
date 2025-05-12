import {Outlet, RouterProvider, createBrowserRouter} from 'react-router-dom';

//components
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
// import Footer from './components/Footer';
import AIButton from './components/AIButton';

//pages
import Login from './pages/Login';
import Signup from './pages/Signup';
import StudentDashboard from './pages/StudentDashboard';
import InstructorDashboard from './pages/InstructorDashboard';
import InstructorCoursePage from './pages/InstructorCoursePage';
import CoursePage from './Pages/CoursePage';
import AIAgent from './Pages/AIAgent';
import Home from './Pages/Home';
import SpecificCoursePage from './Pages/SpecificCoursePage';
import StudentAIModal from './components/StudentAIModal';
import InstructorAIModal from './components/InstructorAIModal';

const AppLayout = () => {
  return (
    <div className="flex flex-col h-screen overflow-hidden bg-gray-100">
      <Navbar />
      <div className="flex flex-row flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex-1 overflow-hidden">
          <Outlet />
        </div>
      </div>
      <AIButton />
      <StudentAIModal />
      <InstructorAIModal />
      {/* <Footer /> */}
    </div>
  );
};



const App = () => {

  const appRouter = createBrowserRouter([
    {
      path:"/",
      element: <AppLayout />,
      children: [
        {
          path: '/',
          element: <Home />,
        },
        {
          path: '/login',
          element: <Login />,
        },
        {
          path: '/signup',
          element: <Signup />,
        },
        {
          path: '/home',
          element: <Home />,
        },
        {
          path: '/student-dashboard',
          element: <StudentDashboard />,
        },
        {
          path: '/course-page',
          element: <CoursePage />,
        },
        {
          path: '/instructor-dashboard',
          element: <InstructorDashboard />,
        },
        {
          path: '/instructor-course-page',
          element: <InstructorCoursePage />,
        },
        {
          path: '/ai-agent',
          element: <AIAgent />,
        },
        {
          path: '/course/:name',
          element: <SpecificCoursePage />,
        },        
      ]
    }
  ]);

  return <RouterProvider router={appRouter} />;
}

export default App;
