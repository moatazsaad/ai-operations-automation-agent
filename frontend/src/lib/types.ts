// These types mirror the Pydantic response models in
// app/routers/metrics.py exactly, field for field. If a backend field is
// ever renamed, TypeScript will flag every place in the frontend that still
// expects the old name.

export interface LowStockItem {
  item_name: string;
  category: string;
  current_stock: number;
  reorder_point: number;
}

export interface DelayedPurchaseOrder {
  purchase_order_id: number;
  supplier_name: string;
  item_name: string;
  expected_delivery_date: string;
  status: string;
}

export interface SupplierPerformance {
  supplier_name: string;
  total_purchase_orders: number;
  delayed_purchase_orders: number;
  delivered_purchase_orders: number;
  on_time_deliveries: number;
  total_spend: number;
  on_time_delivery_rate: number;
}

export interface SupplierSpend {
  supplier_name: string;
  total_spend: number;
}

export interface ReorderRecommendation {
  item_name: string;
  category: string;
  current_stock: number;
  reorder_point: number;
  safety_stock: number;
  recommended_order_quantity: number;
}

export interface TopDelayedSupplier {
  supplier_name: string;
  delayed_po_count: number;
  average_days_delayed: number;
  max_days_delayed: number;
}

// Shape of the POST /run-agent response (app/main.py's AgentRequest/response).
export interface RunAgentResponse {
  response: string;
}

// Shape of the POST /generate-operations-report response.
export interface GenerateReportResponse {
  message: string;
  markdown_path: string;
  pdf_path: string;
}
