// web/src/services/api.ts
import axios from "axios";

// In production (nginx), /api proxies to the api service; in dev, Vite proxy maps /api -> http://localhost:8000 [web:49][web:67].
const base = import.meta.env.VITE_API_BASE || "/api"; // e.g., "/api" or "http://localhost:8000" [web:49][web:67]

export async function parsePdf(file: File, mode: "auto" | "text" | "ocr" = "auto") {
  const form = new FormData();
  form.append("file", file);
  form.append("mode", mode);
  const res = await axios.post(`${base}/parse/pdf`, form, {
    headers: { "Content-Type": "multipart/form-data" },
    maxBodyLength: Infinity, // allow large PDFs [web:49]
  });
  return res.data;
}

export async function exportCsv(transactions: any[]) {
  const res = await axios.post(`${base}/export/csv`, { transactions }, { responseType: "blob" });
  return res.data;
}
