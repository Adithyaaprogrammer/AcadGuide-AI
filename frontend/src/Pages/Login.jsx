import { Link } from "react-router-dom";

const Login = () => {
  return (
    <div className="w-full flex justify-center items-center my-auto">
      <div className="relative w-[400px] h-[450px] bg-transparent border-2 border-black/50 rounded-[20px] backdrop-blur-md flex justify-center items-center">
        <div>
          <form className="flex flex-col items-center">
            <h2 className="text-4xl text-black text-center mb-6">Login</h2>
          
            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <div className="relative">
                <input 
                  type="text" 
                  required
                  className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[35px] py-0 text-black peer"
                />
                <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                  Email
                </label>
              </div>
            </div>

            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <div className="relative">
                <input 
                  type="password" 
                  required
                  className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[35px] py-0 text-black peer"
                />
                <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                  Password
                </label>
              </div>
            </div>

            {/* <div className="-mt-4 mb-4 text-sm text-black w-[310px] flex justify-between">
              <a href="#" className="hover:underline text-gray-700">
                Forgot Password?
              </a>
            </div> */}

            <button className="w-[310px] h-10 rounded-full bg-black border-none outline-none cursor-pointer text-base font-semibold mb-6 text-white">
              Login
            </button>

            <div className="text-sm text-black text-center">
              <p>
                Don&apos;t have an account ?{' '}
                <Link to="/signup" className="font-semibold hover:underline text-black">
                  Signup
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;