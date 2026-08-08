// One typed function per FastAPI endpoint. Every function fetches JSON and
// throws if the request failed, so TanStack Query can turn that into an
// error state the UI can show - nothing here should ever return silently
// broken data.
import type {
  LowStockItem,
  DelayedPurchaseOrder,
  SupplierPerformance,
  SupplierSpend,
  ReorderRecommendation,
  TopDelayedSupplier,
  RunAgentResponse,
  GenerateReportResponse,
} from "./types";

// Read at call time (not module load time) so tests/tools can override it,
// but in practice this is baked in at build time since it's a NEXT_PUBLIC_ var.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

// Sent with every request so the backend can tell "this came from our own
// frontend" apart from a random request. Since this is a NEXT_PUBLIC_ var, it
// ends up in the public JS bundle - it stops casual/automated abuse of the
// AI agent and report endpoints, but isn't a true secret a determined person
// couldn't find by reading the network tab.
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "";

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "X-API-Key": API_KEY },
  });
  if (!res.ok) {
    throw new Error(`GET ${path} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function postJSON<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    throw new Error(`POST ${path} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getLowStockItems: () => getJSON<LowStockItem[]>("/api/metrics/low-stock-items"),
  getDelayedPurchaseOrders: () =>
    getJSON<DelayedPurchaseOrder[]>("/api/metrics/delayed-purchase-orders"),
  getSupplierPerformance: () =>
    getJSON<SupplierPerformance[]>("/api/metrics/supplier-performance"),
  getSpendBySupplier: () => getJSON<SupplierSpend[]>("/api/metrics/spend-by-supplier"),
  getReorderRecommendations: () =>
    getJSON<ReorderRecommendation[]>("/api/metrics/reorder-recommendations"),
  getTopDelayedSuppliers: () =>
    getJSON<TopDelayedSupplier[]>("/api/metrics/top-delayed-suppliers"),

  runAgent: (prompt: string) => postJSON<RunAgentResponse>("/run-agent", { prompt }),
  generateOperationsReport: () =>
    postJSON<GenerateReportResponse>("/generate-operations-report"),
};

// The backend returns a server-side path like "reports/weekly_operations_report_....pdf" -
// this turns that into a URL the browser can actually load, via the
// GET /reports/{filename} endpoint (only the filename matters, not the
// leading "reports/" folder part).
export function reportFileUrl(serverPath: string): string {
  const filename = serverPath.split("/").pop();
  return `${API_BASE_URL}/reports/${filename}`;
}
