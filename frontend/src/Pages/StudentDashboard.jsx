import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from "recharts";

const Dashboard = () => {
  const gaData = [
    { name: "You", python: 2, java: 3, system: 4, dsa: 5 },
    { name: "Your Peers", python: 4, java: 4, system: 5, dsa: 3 },
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
    dsa: [
      { name: "You", value: 12, color: "#FFD700", head: "Data Structures and Algorithms" },
      { name: "Your Peers", value: 88, color: "#DC006A", head: "Data Structures and Algorithms" },
    ],
  };

  return (
    <div className="ml-16 container mx-auto my-auto px-4 py-6">
      <div className="grid grid-cols-2 gap-8">

        <div className="space-y-4">
            <h3 className="text-2xl font-bold text-center mb-10">Number of GAs submitted</h3>
            <div className="bg-orange-200 p-6 rounded-lg shadow-lg">
              <BarChart width={450} height={520} data={gaData} className="mx-auto">
                <XAxis dataKey="name" tick={{ fill: "black" }} />
                <YAxis tick={{ fill: "black" }} />
                <Tooltip />
                <Legend wrapperStyle={{ marginTop: "20px" }} />
                <Bar dataKey="python" fill="#DC006A" name="Python for Data Science" />
                <Bar dataKey="java" fill="#00BF63" name="Programming in Java" />
                <Bar dataKey="system" fill="#2289E6" name="System Commands" />
                <Bar dataKey="dsa" fill="#FEB172" name="Data Structures and Algorithms" />
              </BarChart>
            </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-2xl font-bold text-center mb-10">Number of videos watched</h3>
          <div className="grid grid-cols-2 gap-6">
            {Object.entries(pieData).slice(0, 2).map(([key, data]) => (
              <div key={key} className="bg-orange-200 p-4 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">{data[0].head}</h2>
                <div className="flex justify-center">
                  <PieChart width={200} height={200}>
                    <Pie data={data} dataKey="value" cx="50%" cy="50%" outerRadius={80}>
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

          <div className="flex justify-center gap-6">
            {Object.entries(pieData).slice(2, 4).map(([key, data]) => (
              <div key={key} className="bg-orange-200 p-4 rounded-lg shadow-lg w-1/2">
                <h2 className="text-lg font-bold mb-4">{data[0].head}</h2>
                <div className="flex justify-center">
                  <PieChart width={200} height={200}>
                    <Pie data={data} dataKey="value" cx="50%" cy="50%" outerRadius={80}>
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
  );
};

export default Dashboard;