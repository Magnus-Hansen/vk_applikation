import { useState } from "react";
import { validateKriterie } from "../../utils/kriterieValidation";

const API_BASE = "http://localhost:8000"; // ← change if needed

export default function JsonPage() {
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");
  const [note, setNote] = useState("");

  // Called when a file is uploaded
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const contents = await file.text();
    setText(contents);
    setMessage(""); // clear messages

    // Validate immediately on upload
    let jsonData;
    try {
      jsonData = JSON.parse(contents);
    } catch {
      setMessage("❌ Invalid JSON syntax.");
      return;
    }

    const validation = validateKriterie(jsonData);
    if (!validation.valid) {
      setMessage(`❌ Validation errors:\n${validation.errors.join('\n')}`);
      return;
    }

    setMessage("✅ JSON is valid!");
  };

  // Called when user clicks "Send to server"
  const handleSend = async () => {
    setMessage("");

    if (!text) {
      setMessage("No JSON loaded.");
      return;
    }

    let jsonData;
    try {
      const parsedData = JSON.parse(text);
      jsonData = {
        note: note,
        kriterier: parsedData
      };
      //jsonData = JSON.parse(text);
    } catch {
      setMessage("❌ Invalid JSON.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData)
      });

      if (!res.ok) {
        const err = await res.text();
        setMessage(`❌ Server error: ${res.status}: ${err}`);
        return;
      }

      const result = await res.json();
      setMessage(`✅ Success! Created item with id: ${result.id}`);
    } catch (err) {
      setMessage("❌ Network error: " + String(err));
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Upload JSON File</h1>

      <input
        type="file"
        accept="application/json"
        onChange={handleFileChange}
      />

      <div style={{ marginTop: 20 }}>
        <label htmlFor="note-input">Note (optional): </label>
        <input
          id="note-input"
          type="text"
          placeholder="Add a note about this upload"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          style={{
            width: "100%",
            padding: "8px",
            marginTop: "5px",
            fontSize: "14px"
          }}
        />
      </div>

      {text && (
        <>
          <h2>Edit JSON</h2>
          <textarea
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              setMessage(""); // Clear validation message when editing
            }}
            onBlur={() => {
              // Re-validate when user stops editing
              try {
                const jsonData = JSON.parse(text);
                const validation = validateKriterie(jsonData);
                if (!validation.valid) {
                  setMessage(`❌ Validation errors:\n${validation.errors.join('\n')}`);
                } else {
                  setMessage("✅ JSON is valid!");
                }
              } catch {
                setMessage("❌ Invalid JSON syntax.");
              }
            }}
            style={{
              width: "100%",
              minHeight: "300px",
              fontFamily: "monospace",
              fontSize: "14px",
              padding: "10px"
            }}
          />

          <button onClick={handleSend} style={{ marginTop: 20 }}>
            Send to server (POST)
          </button>
        </>
      )}

      {message && (
        <p style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>{message}</p>
      )}
    </div>
  );
}
