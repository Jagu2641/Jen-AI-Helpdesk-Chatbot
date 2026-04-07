import { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setUploadMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadMessage("Uploading...");

      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setUploadMessage(`Upload successful: ${data.filename}`);
    } catch (error) {
      setUploadMessage(`Upload failed: ${error.message}`);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setAnswer("");
      setSources([]);

      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setAnswer(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-2">JEN-AI Helpdesk Chatbot</h1>
        <p className="text-slate-300 mb-8">
          Upload a document and ask questions about it using RAG.
        </p>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Upload Document</h2>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full mb-4 text-sm text-slate-300"
          />
          <button
            onClick={handleUpload}
            className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded-xl"
          >
            Upload
          </button>

          {uploadMessage && (
            <p className="mt-4 text-sm text-slate-300">{uploadMessage}</p>
          )}
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h2 className="text-2xl font-semibold mb-4">Ask a Question</h2>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something about the uploaded document..."
            className="w-full h-32 rounded-xl bg-slate-800 border border-slate-700 p-4 text-white mb-4"
          />
          <button
            onClick={handleAsk}
            className="bg-green-600 hover:bg-green-700 px-5 py-2 rounded-xl"
          >
            Ask
          </button>

          {loading && <p className="mt-4 text-slate-300">Thinking...</p>}

          {answer && (
            <div className="mt-6">
              <h3 className="text-xl font-semibold mb-2">Answer</h3>
              <div className="bg-slate-800 p-4 rounded-xl whitespace-pre-wrap">
                {answer}
              </div>
            </div>
          )}

          {sources.length > 0 && (
            <div className="mt-6">
              <h3 className="text-xl font-semibold mb-3">Sources</h3>
              <div className="space-y-4">
                {sources.map((source, index) => (
                  <div
                    key={index}
                    className="bg-slate-800 p-4 rounded-xl border border-slate-700"
                  >
                    <p className="text-sm text-slate-200 mb-2 whitespace-pre-wrap">
                      {source.text}
                    </p>
                    <p className="text-xs text-slate-400">
                      Source: {source.metadata?.source} | Chunk:{" "}
                      {source.metadata?.chunk_index}
                    </p>
                    {source.score !== undefined && (
                      <p className="text-xs text-slate-500 mt-1">
                        Score: {source.score}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}