import React, { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";

export default function App() {
  const [result, setResult] = useState<any>(null);

  return (
    <div style={{ padding: 24, fontFamily: "system-ui, sans-serif" }}>
      <header style={{ marginBottom: 16 }}>
        <h1 style={{ margin: 0 }}>MoneyLens</h1>
        <p style={{ color: "#666", marginTop: 4 }}>Parse bank statements (PDF) and compute cash flows</p>
      </header>

      {!result ? (
        <UploadPage onParsed={setResult} />
      ) : (
        <ResultsPage result={result} onReset={() => setResult(null)} />
      )}
    </div>
  );
}
