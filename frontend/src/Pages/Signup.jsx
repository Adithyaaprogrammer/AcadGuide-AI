import { useState } from "react";
import { Link } from "react-router-dom";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    role: "",
  });

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch("http://localhost:7777/users/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Signup failed");
      }

      alert("Signup successful!");
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="w-full flex justify-center items-center mt-24">
      <div className="relative w-[400px] h-[550px] bg-transparent border-2 border-black/50 rounded-[20px] backdrop-blur-md flex justify-center items-center">
        <div>
          <form className="flex flex-col items-center" onSubmit={handleSubmit}>
            <h2 className="text-4xl text-black text-center mb-6">Signup</h2>

            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <input
                type="text"
                name="username"
                required
                value={formData.username}
                onChange={handleChange}
                className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[10px] text-black peer"
              />
              <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                Name
              </label>
            </div>

            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <select
                name="role"
                required
                value={formData.role}
                onChange={handleChange}
                className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[10px] text-black appearance-none peer"
              >
                <option value="" disabled selected></option>
                <option value="student">Student</option>
                <option value="instructor">Instructor</option>
              </select>
              <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                Role ▼
              </label>
            </div>

            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <input
                type="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[10px] text-black peer"
              />
              <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                Email
              </label>
            </div>

            <div className="relative w-[310px] mb-8 border-b-2 border-black">
              <input
                type="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full h-[50px] bg-transparent border-none outline-none text-base px-[10px] text-black peer"
              />
              <label className="absolute left-1 top-1/2 -translate-y-1/2 text-black text-base pointer-events-none transition-all duration-500 peer-focus:-top-1 peer-focus:text-md peer-valid:-top-1 peer-valid:text-md">
                Password
              </label>
            </div>

            <button
              type="submit"
              className="w-[310px] h-10 rounded-full bg-black border-none outline-none cursor-pointer text-base font-semibold mb-6 text-white"
            >
              Signup
            </button>

            <div className="text-sm text-black text-center">
              <p>
                Already have an account?{" "}
                <Link to="/login" className="font-semibold hover:underline text-black">
                  Login
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Signup;
