// Ports app/dashboard.py's clean_column_names(): turns a raw field name like
// "purchase_order_id" into "Purchase Order ID" for table headers.
export function cleanColumnName(key: string): string {
  const titled = key
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");

  return titled.replace(/\bPo\b/g, "PO").replace(/\bId\b/g, "ID").replace(/\bUrl\b/g, "URL");
}
