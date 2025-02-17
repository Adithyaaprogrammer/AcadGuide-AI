import { PROFILE } from "../utils/constants";

const Navbar = () => {
  const user = { regNo: "25F3001702", name: "John Doe" };
  
  return (
    <div className="flex justify-between bg-orange-400 p-4 items-center">
      <h1 className="text-2xl text-black font-medium font-sans">StudySmart AI</h1>

      {user ? (
        <div className="flex items-center space-x-2">
          <span className="text-black font-medium mx-5 text-lg">{user.regNo}</span>
          <img src={PROFILE} alt="Profile" className="w-10 h-10 rounded-full" />
        </div>
      ) : (
        <span className="text-black font-medium">Not Logged In</span>
      )}
    </div>
  );
};

export default Navbar;
