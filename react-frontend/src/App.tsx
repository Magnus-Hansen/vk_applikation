import { useState } from "react";
import JsonPage from "./assets/pages/JsonPage";
import HistoryPage from "./assets/pages/HistoryPage";

export default function App() {
  const [currentPage, setCurrentPage] = useState<"upload" | "history">("upload");

  return (
    <div>
      <nav style={{ padding: "10px", backgroundColor: "#333", color: "white" }}>
        <button
          onClick={() => setCurrentPage("upload")}
          style={{
            marginRight: "10px",
            padding: "8px 16px",
            backgroundColor: currentPage === "upload" ? "#555" : "#222",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Upload JSON
        </button>
        <button
        id="History"
          onClick={() => setCurrentPage("history")}
          style={{
            padding: "8px 16px",
            backgroundColor: currentPage === "history" ? "#555" : "#222",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          View History
        </button>
      </nav>

      {currentPage === "upload" ? <JsonPage /> : <HistoryPage />}
    </div>
  );
}