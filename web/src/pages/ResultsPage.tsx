// web/src/pages/ResultsPage.tsx
import React from "react";
import { exportCsv } from "../services/api";

export default function ResultsPage({
  result,
  onReset,
}: {
  result: any;
  onReset: () => void;
}) {
  const { totals, transactions, metadata } = result;

  const onExport = async () => {
    const blob = await exportCsv(transactions);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "moneylens_transactions.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <section style={{ marginBottom: 16 }}>
        <h2 style={{ margin: "8px 0" }}>Totals</h2>
        <ul>
          <li>Inflow: {totals.inflow}</li>
          <li>Outflow: {totals.outflow}</li>
          <li>Net: {totals.net}</li>
          <li>Total flow: {totals.flow_volume}</li>
        </ul>
      </section>

      <section style={{ marginBottom: 16 }}>
        <h3 style={{ margin: "8px 0" }}>Metadata</h3>
        <pre style={{ background: "#f6f6f6", padding: 12, overflow: "auto" }}>
{JSON.stringify(metadata, null, 2)}
        </pre>
      </section>

      <section>
        <h3 style={{ margin: "8px 0" }}>
          Transactions ({transactions.length})
        </h3>
        <div style={{ maxHeight: 360, overflow: "auto", border: "1px solid #ddd" }}>
          <table width="100%" cellPadding={6}>
            <thead>
              <tr>
                <th align="left">Date</th>
                <th align="left">Description</th>
                <th align="right">Amount</th>
                <th align="left">Type</th>
                <th align="right">Balance</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t: any, idx: number) => (
                <tr key={idx}>
                  <td>{t.date}</td>
                  <td>{t.description}</td>
                  <td align="right">{t.amount}</td>
                  <td>{t.type}</td>
                  <td align="right">{t.balance ?? ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: 12 }}>
          <button onClick={onExport}>Export CSV</button>{" "}
          <button onClick={onReset}>Parse another</button>
        </div>
      </section>
    </div>
  );
}
