// web/src/utils/format.ts
export function fmtCurrency(n: number, currency = "INR", locale = "en-IN") {
  try {
    return new Intl.NumberFormat(locale, { style: "currency", currency }).format(n);
  } catch {
    return n.toFixed(2);
  }
}

export function fmtDate(s: string) {
  // s may already be ISO; attempt to render nicely
  const d = new Date(s);
  return isNaN(d.getTime()) ? s : d.toISOString().slice(0, 10);
}
