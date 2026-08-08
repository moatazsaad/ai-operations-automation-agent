// Renders any array of flat objects as an HTML table, deriving columns from
// the keys of the first row - so each of the 6 tabs just passes its array,
// no per-tab column list to keep in sync by hand.
import { cleanColumnName } from "@/lib/clean-column-name";

export function DataTable<T extends object>({
  rows,
  emptyMessage,
}: {
  rows: T[];
  emptyMessage: string;
}) {
  if (rows.length === 0) {
    return <p className="px-1 py-4 text-sm text-muted-foreground">{emptyMessage}</p>;
  }

  // Cast to a plain string-keyed record just for reading field values below -
  // the object shape itself is still whatever T is, this only affects how we
  // index into it since T has no index signature of its own.
  const rowsAsRecords = rows as Record<string, unknown>[];
  const columns = Object.keys(rowsAsRecords[0]);

  return (
    <div className="overflow-x-auto rounded-lg border">
      <table className="w-full text-sm">
        <thead className="bg-muted/50">
          <tr>
            {columns.map((col) => (
              <th key={col} className="px-3 py-2 text-left font-medium">
                {cleanColumnName(col)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rowsAsRecords.map((row, i) => (
            <tr key={i} className="border-t">
              {columns.map((col) => (
                <td key={col} className="px-3 py-2">
                  {String(row[col])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
