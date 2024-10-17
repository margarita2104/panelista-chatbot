import { useEffect, useState } from "react";

interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  topics?: string;
  current_job_title?: string;
  career_description?: string;
}

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    topics: "",
    current_job_title: "",
    career_description: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/users/create/")
      .then((response) => response.json())
      .then((data: User[]) => setUsers(data))
      .catch((error) => setError(error.message));
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    fetch("http://localhost:8000/users/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data: User) => {
        setUsers([...users, data]);
        setFormData({
          email: "",
          username: "",
          first_name: "",
          last_name: "",
          topics: "",
          current_job_title: "",
          career_description: "",
        });
      })
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 text-left">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Users List</h1>

        {error && <p className="text-red-500 mb-4">Error: {error}</p>}
        {loading && <p className="text-blue-500 mb-4">Loading...</p>}

        <table className="w-full mb-6">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 text-left text-gray-700">Name</th>
              {/* <th className="py-2 px-4 text-left text-gray-700">Email</th> */}
              {/* <th className="py-2 px-4 text-left text-gray-700">Username</th> */}
              <th className="py-2 px-4 text-left text-gray-700">Topics</th>
              <th className="py-2 px-4 text-left text-gray-700">
                Current Job Title
              </th>
              <th className="py-2 px-4 text-left text-gray-700">
                Career Description
              </th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-gray-200">
                <td className="py-2 px-4">
                  {user.first_name} {user.last_name}
                </td>
                {/* <td className="py-2 px-4">{user.email}</td> */}
                {/* <td className="py-2 px-4">{user.username}</td> */}
                <td className="py-2 px-4">{user.topics}</td>
                <td className="py-2 px-4">{user.current_job_title}</td>
                <td className="py-2 px-4">{user.career_description}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <h2 className="text-2xl font-semibold mb-4 text-gray-700">
          Create New User
        </h2>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6">
          <div>
            <label className="block text-gray-700">Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700">Username:</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700">First Name:</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700">Last Name:</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div className="col-span-2">
            <label className="block text-gray-700">Topics:</label>
            <textarea
              name="topics"
              value={formData.topics}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700">Current Job Title:</label>
            <input
              type="text"
              name="current_job_title"
              value={formData.current_job_title}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-gray-700">Career Description:</label>
            <textarea
              name="career_description"
              value={formData.career_description}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          <div className="col-span-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300 disabled:bg-blue-300"
            >
              {loading ? "Creating..." : "Create User"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Users;
