import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [userPrompt, setUserPrompt] = useState<string>("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserPrompt(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await axios.post("http://localhost:8000/chatbot/", {
        user_prompt: userPrompt,
      });
      setResponse(result.data.chatbot_response);
    } catch (err) {
      setError(
        "An error occurred while fetching the response. Please try again."
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderSpeakers = (response: string) => {
    const lines = response.split("\n").filter(line => line.trim() !== "");

    // Identify if there's reasoning in the first lines
    const reasoningIndex = lines.findIndex(line =>
      line.toLowerCase().includes("i couldn't find")
    );
    const reasoningText =
      reasoningIndex !== -1 ? lines[reasoningIndex] : null;

    // Filter out reasoning from the speaker lines
    const speakerLines = lines.slice(reasoningIndex + 1);

    return (
      <>
        {/* Render reasoning if it exists */}
        {reasoningText && (
          <div className="p-4 mb-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700">
            <p>{reasoningText}</p>
          </div>
        )}

        {/* Render speakers */}
        {speakerLines.map((line, index) => {
          if (line.startsWith("- ")) {
            const [name, expertise, bio] = [
              line.split(" - ")[0].replace("- ", ""),
              speakerLines[index + 1]?.replace("  Expertise: ", ""),
              speakerLines[index + 2]?.replace("  Bio: ", ""),
            ];

            return (
              <div
                key={index}
                className="p-4 border rounded-lg shadow-md mb-4 bg-gray-50"
              >
                <h3 className="text-lg font-bold text-gray-800">{name}</h3>
                <p className="text-sm text-gray-600">
                  <strong>Expertise:</strong> {expertise}
                </p>
                <p className="text-sm text-gray-600">
                  <strong>Bio:</strong> {bio}
                </p>
              </div>
            );
          }
          return null;
        })}
      </>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 text-left">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Chatbot</h1>

        <form onSubmit={handleSubmit} className="mb-6">
          <input
            type="text"
            value={userPrompt}
            onChange={handleInputChange}
            placeholder="What kind of speaker are you looking for?"
            required
            className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none mb-4"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300 disabled:bg-blue-300"
          >
            {loading ? "Submitting..." : "Submit"}
          </button>
        </form>

        {error && <p className="text-red-500 mb-4">{error}</p>}
        {loading && <p className="text-blue-500 mb-4">Loading...</p>}
        {response && (
          <div
            style={{
              marginTop: "20px",
              border: "1px solid #ccc",
              padding: "10px",
            }}
          >
            <h2 className="text-2xl font-semibold mb-2">Suggested Speakers:</h2>
            {renderSpeakers(response)}
          </div>
        )}
      </div>
    </div>
  );
};

export default Chatbot;
