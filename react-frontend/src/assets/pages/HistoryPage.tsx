import { useState, useEffect } from "react";
import { validateKriterie } from "../../utils/kriterieValidation";

const API_BASE = "http://localhost:8000";

interface Dkhype {
  "1.1": number | null;
  "5": number | null;
  "20": number | null;
  "50": number | null;
}

interface Vandstand {
  varsel: number | null;
  "1.1": number | null;
  "2": number | null;
  "5": number | null;
  "10": number | null;
}

interface Kriterie {
  id: number;  // This is the upload_id
  station_id: string;
  dkhype: Dkhype | null;
  vandstand: Vandstand | null;
}

interface Upload {
  id: number;
  Datetime: string;
  note: string;
}

interface GroupedUpload {
  upload_id: number;
  date: string;
  note: string;
  count: number;
}

export default function HistoryPage() {
  const [allData, setAllData] = useState<Kriterie[]>([]);
  const [uploads, setUploads] = useState<GroupedUpload[]>([]);
  const [selectedUpload, setSelectedUpload] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editModal, setEditModal] = useState<Kriterie | null>(null);
  const [saving, setSaving] = useState(false);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  // Fetch all data on mount
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    setError("");
    try {
      // Fetch both uploads metadata and criteria data
      const [uploadsRes, criteriaRes] = await Promise.all([
        fetch(`${API_BASE}/uploads`),
        fetch(`${API_BASE}/all`)
      ]);

      if (!uploadsRes.ok) throw new Error(`Uploads error: ${uploadsRes.status}`);
      if (!criteriaRes.ok) throw new Error(`Criteria error: ${criteriaRes.status}`);
      
      const uploadsData: Upload[] = await uploadsRes.json();
      const criteriaData: Kriterie[] = await criteriaRes.json();
      
      setAllData(criteriaData);

      // Create a map of upload metadata
      const uploadMap = new Map<number, Upload>();
      uploadsData.forEach((upload) => {
        uploadMap.set(upload.id, upload);
      });

      // Count criteria per upload and combine with upload metadata
      const countMap = new Map<number, number>();
      criteriaData.forEach((item) => {
        countMap.set(item.id, (countMap.get(item.id) || 0) + 1);
      });

      const uploadsList: GroupedUpload[] = Array.from(uploadMap.values()).map((upload) => ({
        upload_id: upload.id,
        date: upload.Datetime || "Unknown",
        note: upload.note || "",
        count: countMap.get(upload.id) || 0,
      })).sort((a, b) => b.upload_id - a.upload_id);

      setUploads(uploadsList);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch history");
    } finally {
      setLoading(false);
    }
  };

  const filteredData = selectedUpload
    ? allData.filter((item) => item.id === selectedUpload)
    : [];

  const selectedUploadInfo = uploads.find((u) => u.upload_id === selectedUpload);
  const isLatestUpload = selectedUpload === uploads[0]?.upload_id;

  const handleSave = async () => {
    if (!editModal) return;

    // Validate before saving
    const validation = validateKriterie(editModal);
    if (!validation.valid) {
      setValidationErrors(validation.errors);
      return;
    }

    setSaving(true);
    setError("");
    setValidationErrors([]);
    
    try {
      const response = await fetch(`${API_BASE}/varsling`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: editModal.id,
          station_id: editModal.station_id,
          dkhype: editModal.dkhype,
          vandstand: editModal.vandstand,
        }),
      });

      if (!response.ok) throw new Error(`Update failed: ${response.status}`);

      setAllData(prev => 
        prev.map(item => 
          item.station_id === editModal.station_id && item.id === editModal.id
            ? editModal
            : item
        )
      );

      setEditModal(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save changes");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Upload History</h1>

      {loading && <p>Loading history...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <>
          <div style={{ marginBottom: "20px" }}>
            <h2>All Uploads ({uploads.length})</h2>
            <table style={{ borderCollapse: "collapse", width: "100%" }}>
              <thead>
                <tr style={{ backgroundColor: "#f0f0f0" }}>
                  <th style={{ border: "1px solid #ccc", padding: "8px", color: "#000" }}>Upload ID</th>
                  <th style={{ border: "1px solid #ccc", padding: "8px", color: "#000" }}>Date</th>
                  <th style={{ border: "1px solid #ccc", padding: "8px", color: "#000" }}>Note</th>
                  <th style={{ border: "1px solid #ccc", padding: "8px", color: "#000" }}>Records</th>
                  <th style={{ border: "1px solid #ccc", padding: "8px", color: "#000" }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {uploads.map((upload) => (
                  <tr key={upload.upload_id}>
                    <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                      {upload.upload_id}
                    </td>
                    <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                      {upload.date}
                    </td>
                    <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                      {upload.note || "—"}
                    </td>
                    <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                      {upload.count}
                    </td>
                    <td style={{ border: "1px solid #ccc", padding: "8px" }}>
                      <button onClick={() => setSelectedUpload(upload.upload_id)}>
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedUpload && (
            <div>
              <h2>
                Upload #{selectedUpload} - Details ({filteredData.length} records)
                {isLatestUpload && <span style={{ color: "green", fontSize: "14px", marginLeft: "10px" }}>✓ Latest (Editable)</span>}
              </h2>
              {selectedUploadInfo && (
                <div style={{ marginBottom: "10px", padding: "10px", backgroundColor: "#f9f9f9", border: "1px solid #ddd", color: "#000" }}>
                  <strong>Date:</strong> {selectedUploadInfo.date} | <strong>Note:</strong> {selectedUploadInfo.note || "No note"}
                </div>
              )}
              <button onClick={() => setSelectedUpload(null)} style={{ marginBottom: "10px" }}>
                ← Back to All Uploads
              </button>
              <div style={{ maxHeight: "400px", overflow: "auto" }}>
                <table style={{ borderCollapse: "collapse", width: "100%", fontSize: "12px" }}>
                  <thead>
                    <tr style={{ backgroundColor: "#f0f0f0" }}>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Station ID</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>DKHype 1.1</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>DKHype 5</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>DKHype 20</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>DKHype 50</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Varsel</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Vandstand 1.1</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Vandstand 2</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Vandstand 5</th>
                      <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Vandstand 10</th>
                      {isLatestUpload && <th style={{ border: "1px solid #ccc", padding: "4px", color: "#000" }}>Actions</th>}
                    </tr>
                  </thead>
                  <tbody>
                    {filteredData.map((item, idx) => (
                      <tr key={idx}>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.station_id}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.dkhype?.["1.1"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.dkhype?.["5"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.dkhype?.["20"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.dkhype?.["50"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.vandstand?.varsel ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.vandstand?.["1.1"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.vandstand?.["2"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.vandstand?.["5"] ?? "—"}
                        </td>
                        <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                          {item.vandstand?.["10"] ?? "—"}
                        </td>
                        {isLatestUpload && (
                          <td style={{ border: "1px solid #ccc", padding: "4px" }}>
                            <button 
                              onClick={() => setEditModal(JSON.parse(JSON.stringify(item)))}
                              style={{ padding: "2px 8px", fontSize: "11px" }}
                            >
                              Edit
                            </button>
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {editModal && (
            <div style={{
              position: "fixed",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: "rgba(0,0,0,0.5)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 1000
            }}>
              <div style={{
                backgroundColor: "white",
                color: "#000",
                padding: "20px",
                borderRadius: "8px",
                maxWidth: "500px",
                width: "90%"
              }}>
                <h3>Edit Station {editModal.station_id}</h3>
                
                {validationErrors.length > 0 && (
                  <div style={{ 
                    backgroundColor: "#ffebee", 
                    border: "1px solid #f44336", 
                    padding: "10px", 
                    marginBottom: "15px",
                    borderRadius: "4px"
                  }}>
                    <strong style={{ color: "#c62828" }}>Validation Errors:</strong>
                    <ul style={{ margin: "5px 0", paddingLeft: "20px" }}>
                      {validationErrors.map((err, idx) => (
                        <li key={idx} style={{ color: "#c62828" }}>{err}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>DKHype 1.1:</label>
                  <input
                    type="number"
                    value={editModal.dkhype?.["1.1"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      dkhype: { ...editModal.dkhype!, "1.1": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>DKHype 5:</label>
                  <input
                    type="number"
                    value={editModal.dkhype?.["5"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      dkhype: { ...editModal.dkhype!, "5": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>DKHype 20:</label>
                  <input
                    type="number"
                    value={editModal.dkhype?.["20"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      dkhype: { ...editModal.dkhype!, "20": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>DKHype 50:</label>
                  <input
                    type="number"
                    value={editModal.dkhype?.["50"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      dkhype: { ...editModal.dkhype!, "50": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>Varsel:</label>
                  <input
                    type="number"
                    value={editModal.vandstand?.varsel ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      vandstand: { ...editModal.vandstand!, varsel: e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>Vandstand 1.1:</label>
                  <input
                    type="number"
                    value={editModal.vandstand?.["1.1"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      vandstand: { ...editModal.vandstand!, "1.1": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>Vandstand 2:</label>
                  <input
                    type="number"
                    value={editModal.vandstand?.["2"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      vandstand: { ...editModal.vandstand!, "2": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>Vandstand 5:</label>
                  <input
                    type="number"
                    value={editModal.vandstand?.["5"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      vandstand: { ...editModal.vandstand!, "5": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ marginBottom: "15px" }}>
                  <label style={{ display: "block", marginBottom: "5px" }}>Vandstand 10:</label>
                  <input
                    type="number"
                    value={editModal.vandstand?.["10"] ?? ""}
                    onChange={(e) => setEditModal({
                      ...editModal,
                      vandstand: { ...editModal.vandstand!, "10": e.target.value ? parseFloat(e.target.value) : null }
                    })}
                    style={{ width: "100%", padding: "5px" }}
                  />
                </div>
                <div style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                  <button 
                    onClick={() => {
                      setEditModal(null);
                      setValidationErrors([]);
                    }}
                    disabled={saving}
                    style={{ padding: "8px 16px" }}
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={handleSave}
                    disabled={saving}
                    style={{ padding: "8px 16px", backgroundColor: "#4CAF50", color: "white", border: "none", cursor: "pointer" }}
                  >
                    {saving ? "Saving..." : "Save"}
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
