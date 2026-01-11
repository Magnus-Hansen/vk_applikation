import { useState, useEffect } from "react";
import { validateKriterie } from "../../utils/kriterieValidation";

const API_BASE = "http://localhost:8000"; // ← change if needed

export default function JsonPage() {
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");
  const [note, setNote] = useState("");
  const [sommer, setSommer] = useState<boolean | null>(null);

  // Re-validate when season selection changes
  useEffect(() => {
    if (text && message.includes("valid")) {
      try {
        const jsonData = JSON.parse(text);
        const validation = validateKriterie(jsonData);
        if (validation.valid) {
          if (sommer === null) {
            setMessage("⚠️ JSON is valid. Please select season before sending.");
          } else {
            setMessage("✅ JSON is valid and ready to send!");
          }
        }
      } catch {
        // Keep existing error message
      }
    }
  }, [sommer, text, message]);

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

    if (sommer === null) {
      setMessage("⚠️ JSON is valid. Please select season before sending.");
    } else {
      setMessage("✅ JSON is valid and ready to send!");
    }
  };

  // Called when user clicks "Send to server"
  const handleSend = async () => {
    setMessage("");

    if (!text) {
      setMessage("No JSON loaded.");
      return;
    }

    if (sommer === null) {
      setMessage("❌ Please select season (Summer/Winter).");
      return;
    }

    let jsonData;
    try {
      const parsedData = JSON.parse(text);
      jsonData = {
        note: note,
        sommer: sommer,
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
      setMessage(`✅ Success! Created item with id: ${result.upload_id}`);
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

      <div style={{ marginTop: 15 }}>
        <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
          Season: <span style={{ color: "red" }}>*</span>
        </label>
        <label style={{ marginRight: 20, cursor: "pointer" }}>
          <input
            type="radio"
            name="season"
            checked={sommer === true}
            onChange={() => setSommer(true)}
            style={{ marginRight: "6px" }}
          />
          Summer
        </label>
        <label style={{ cursor: "pointer" }}>
          <input
            type="radio"
            name="season"
            checked={sommer === false}
            onChange={() => setSommer(false)}
            style={{ marginRight: "6px" }}
          />
          Winter
        </label>
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
                } else if (sommer === null) {
                  setMessage("⚠️ JSON is valid. Please select season before sending.");
                } else {
                  setMessage("✅ JSON is valid and ready to send!");
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
