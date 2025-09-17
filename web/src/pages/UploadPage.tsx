import React, { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";

export default function UploadPage({ onParsed }: { onParsed: (result: any) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState("auto");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    
    const formData = new FormData();
    formData.append("file", file);
    formData.append("mode", mode);

    try {
      const response = await fetch("/api/parse", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      onParsed(result);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout title="MoneyLens">
      <div className="card card-pad max-w-2xl mx-auto">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-zinc-900 mb-2">Parse bank statements (PDF) and compute cash flows</h2>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-2">Select File</label>
            <div className="relative">
              <input
                type="file"
                accept=".pdf,image/*"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full text-sm text-zinc-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-zinc-50 file:text-zinc-700 hover:file:bg-zinc-100"
              />
            </div>
            {file && (
              <p className="mt-2 text-sm text-zinc-600">Selected: {file.name}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-2">Mode</label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="block w-full rounded-md border-zinc-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="auto">auto</option>
              <option value="ocr">ocr</option>
              <option value="text">text</option>
            </select>
          </div>

          <button
            onClick={handleSubmit}
            disabled={!file || loading}
            className="btn btn-primary w-full justify-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Parse PDF"}
          </button>

          <div className="text-sm text-zinc-500">
            <p>Tip: For large scanned PDFs, try "ocr" mode; for digital statements, "text" is faster.</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
