// web/src/pages/UploadPage.tsx
import React, { useState } from "react";
import { parsePdf } from "../services/api";

type Mode = "auto" | "text" | "ocr";

export default function UploadPage({ onParsed }: { onParsed: (r: any) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<Mode>("auto");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setErr(null);
    try {
      const data = await parsePdf(file, mode);
      onParsed(data);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || "Failed to parse PDF";
      setErr(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit}>
      <div style={{ margin: "12px 0" }}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      <div style={{ margin: "12px 0" }}>
        <label>
          Mode:{" "}
          <select value={mode} onChange={(e) => setMode(e.target.value as Mode)}>
            <option value="auto">auto</option>
            <option value="text">text</option>
            <option value="ocr">ocr</option>
          </select>
        </label>
      </div>

      <button type="submit" disabled={!file || loading}>
        {loading ? "Parsing..." : "Parse PDF"}
      </button>

      {err && (
        <div style={{ color: "crimson", marginTop: 12 }}>
          {err}
        </div>
      )}

      <p style={{ color: "#666", marginTop: 12, fontSize: 13 }}>
        Tip: For large scanned PDFs, try “ocr” mode; for digital statements, “text” is faster.
      </p>
    </form>
  );
}
