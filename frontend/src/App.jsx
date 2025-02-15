import {Outlet, RouterProvider, createBrowserRouter} from 'react-router-dom';

//components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

//pages
import Login from './pages/Login';
import Signup from './pages/Signup';
import StudentDashboard from './pages/StudentDashboard';

const AppLayout = () => {
  return (
    <div className='flex flex-col min-h-screen bg-gray-100'>
      <Navbar />
      <Outlet />
      <Footer />
    </div>
  );
}

const App = () => {

  const appRouter = createBrowserRouter([
    {
      path:"/",
      element: <AppLayout />,
      children: [
        {
          path: '/',
          element: <Login />,
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
          path: '/student-dashboard',
          element: <StudentDashboard />,
        },
      ]
    }
  ]);

  return <RouterProvider router={appRouter} />;
}

export default App;
