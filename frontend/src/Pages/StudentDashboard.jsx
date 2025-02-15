import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from "recharts";
// import aiImage from "./ai_assist.png";
// import profile from "./profile.jpg";
// import pro1 from "./pro1.png";

const Dashboard = () => {
  const gaData = [
    { name: "You", python: 2, java: 3, system: 4 },
    { name: "Your Peers", python: 4, java: 4, system: 5 },
  ];

  const pieData = {
    python: [
      { name: "You", value: 3, color: "#FFD700", head: "Python for Data Science" },
      { name: "Your Peers", value: 97, color: "#DC006A", head: "Python for Data Science" },
    ],
    java: [
      { name: "You", value: 5, color: "#FFD700", head: "Programming in Java" },
      { name: "Your Peers", value: 95, color: "#DC006A", head: "Programming in Java" },
    ],
    system: [
      { name: "You", value: 12, color: "#FFD700", head: "System Commands" },
      { name: "Your Peers", value: 88, color: "#DC006A", head: "System Commands" },
    ],
  };

  return (
    <div className="font-sans m-0 p-0 flex">
      <div className="flex-grow pl-24 pt-28 ml-24">
        <h1 className="text-2xl font-bold text-left mb-4 ml-3">Current Courses</h1>
        <div className="flex justify-start items-start gap-5">
          <div className="mx-10 mb-8">
            <div className="flex gap-16 items-center justify-center">
              {Object.entries(pieData).slice(0, 3).map(([key, data]) => (
                <div key={key} className="bg-orange-200 p-10 h-72 shadow-md text-center flex-1 max-w-md">
                  <div className="pie-chart">
                    <h2 className="text-lg font-bold">{data[0].head}</h2>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Top Navigation */}
        <nav className="fixed top-0 left-0 w-full bg-white p-4 h-10 z-50">
          <div className="flex gap-4">
            {[...Array(4)].map((_, index) => (
              <div key={index} className="w-4 h-4 rounded-full bg-orange-400" />
            ))}
          </div>
        </nav>

        {/* Secondary Navigation */}
        <nav className="fixed top-9 left-0 w-full bg-orange-400 p-1 flex justify-between items-center z-40">
          <h1 className="ml-6 text-black">StudySmart AI</h1>
          <h4 className="flex items-center gap-2">
            25J1223334
            {/* <img src={pro1} alt="" className="w-6 h-px" />
            <img src={profile} alt="" className="h-6" />
            <img src={pro1} alt="" className="h-6" /> */}
          </h4>
        </nav>

        {/* Sidebar */}
        <nav className="fixed left-0 top-10 w-36 h-full bg-orange-200 p-5 flex flex-col items-center overflow-y-auto z-30">
          <ul className="list-none p-0 mt-20 w-full">
            {['COURSES', 'PROJECTS', 'QUERIES', 'DOCUMENTS', 'CERTIFICATES'].map((item) => (
              <li key={item} className="my-4 text-left">
                <a href={`#${item.toLowerCase()}`} className="text-black no-underline text-sm font-bold block p-3 rounded hover:bg-orange-600 transition-colors">
                  {item}
                </a>
              </li>
            ))}
          </ul>
          
          <div className="text-center mt-5">
            {/* <div className="relative">
              <img src={aiImage} alt="AI Assistant" className="w-28 h-auto animate-bounce" />
            </div> */}
            <h1 className="text-lg font-bold mt-4">AI ASSISTANT</h1>
          </div>
        </nav>

        {/* Main Content */}
        <div className="flex justify-start items-start gap-5">
          {/* Charts Section */}
          <div className="mx-10 mb-8">
            <h3 className="text-2xl font-bold text-left mb-4">LET&apos;S COMPETE!</h3>
            <h3 className="bg-orange-400 p-3 text-2xl shadow-md text-center mb-0">Number of GAs submitted</h3>
            <div className="bg-orange-200 p-10 h-72 shadow-md text-center">
              <div className="flex justify-center items-center">
                <BarChart width={400} height={300} data={gaData}>
                  <XAxis dataKey="name" tick={{ fill: "black" }} />
                  <YAxis tick={{ fill: "black" }} />
                  <Tooltip />
                  <Legend wrapperStyle={{ marginTop: "20px" }} />
                  <Bar dataKey="python" fill="#DC006A" name="Python for Data Science" />
                  <Bar dataKey="java" fill="#00BF63" name="Programming in Java" />
                  <Bar dataKey="system" fill="#2289E6" name="System Commands" />
                </BarChart>
              </div>
            </div>
          </div>

          <div className="mx-10 mb-8">
            <h3 className="text-2xl font-bold text-center mb-4">Number of videos watched</h3>
            <div className="flex gap-16 items-center justify-center">
              {Object.entries(pieData).slice(0, 2).map(([key, data]) => (
                <div key={key} className="bg-orange-200 p-10 h-72 shadow-md text-center">
                  <div className="pie-chart">
                    <h2 className="text-lg font-bold">{data[0].head}</h2>
                    <PieChart width={200} height={200}>
                      <Pie data={data} dataKey="value" cx="56%" cy="50%" outerRadius={80}>
                        {data.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-start items-start gap-5 mt-8">
              {Object.entries(pieData).slice(2, 3).map(([key, data]) => (
                <div key={key} className="bg-orange-200 p-8 h-72 shadow-md text-center">
                  <div className="pie-chart">
                    <h2 className="text-lg font-bold">{data[0].head}</h2>
                    <PieChart width={200} height={200}>
                      <Pie data={data} dataKey="value" cx="56%" cy="50%" outerRadius={80}>
                        {data.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;