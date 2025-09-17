import React, { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { exportCsv } from "../services/api";
import { fmtCurrency, fmtDate } from "../styles/format";

export default function ResultsPage({ result, onReset }: { result: any; onReset: () => void }) {
  const [metaOpen, setMetaOpen] = useState(false);
  if (!result) return null;
  const { totals, transactions, metadata } = result;

  const stats = [
    { label: "Inflow", value: fmtCurrency(totals.inflow), hue: "from-emerald-500 to-teal-500" },
    { label: "Outflow", value: fmtCurrency(totals.outflow), hue: "from-rose-500 to-orange-500" },
    { label: "Net", value: fmtCurrency(totals.net), hue: "from-indigo-500 to-violet-500" },
    { label: "Flow", value: fmtCurrency(totals.flow_volume), hue: "from-cyan-500 to-blue-500" },
  ];

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
    <DashboardLayout title="Results">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((s) => (
          <div key={s.label} className="card overflow-hidden">
            <div className={`h-1.5 bg-gradient-to-r ${s.hue}`} />
            <div className="card-pad">
              <div className="card-title">{s.label}</div>
              <div className="stat mt-1">{s.value}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="mb-6">
        <button className="btn" onClick={() => setMetaOpen((v) => !v)}>
          {metaOpen ? "Hide metadata" : "Show metadata"}
        </button>
        {metaOpen && (
          <div className="card card-pad mt-3">
            <pre className="prose prose-zinc text-xs overflow-auto">{JSON.stringify(metadata, null, 2)}</pre>
          </div>
        )}
      </div>

      <div className="card overflow-hidden">
        <div className="card-pad border-b border-zinc-200 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-zinc-800">
            Transactions <span className="opacity-60">({transactions.length})</span>
          </h3>
          <div className="flex items-center gap-2">
            <button className="btn" onClick={onReset}>Parse another</button>
            <button className="btn btn-primary" onClick={onExport}>Export CSV</button>
          </div>
        </div>
        <div className="max-h-[420px] overflow-auto">
          <table className="table">
            <thead>
              <tr>
                <th className="th">Date</th>
                <th className="th">Description</th>
                <th className="th text-right">Amount</th>
                <th className="th">Type</th>
                <th className="th text-right">Balance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200">
              {transactions.map((t: any, idx: number) => (
                <tr key={`${t.date}-${t.amount}-${idx}`} className="odd:bg-white even:bg-zinc-50 hover:bg-zinc-100/60">
                  <td className="td whitespace-nowrap">{fmtDate(t.date)}</td>
                  <td className="td">{t.description}</td>
                  <td className="td text-right tabular-nums">{fmtCurrency(t.amount)}</td>
                  <td className="td">{t.type}</td>
                  <td className="td text-right tabular-nums">{t.balance != null ? fmtCurrency(t.balance) : ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </DashboardLayout>
  );
}
