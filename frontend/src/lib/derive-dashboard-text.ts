// Ports the exact insight/action/KPI derivation logic from app/dashboard.py
// so both UIs tell the same story from the same data. Nothing here queries
// anything - it only reshapes arrays that were already fetched.
import type {
  LowStockItem,
  DelayedPurchaseOrder,
  SupplierPerformance,
  SupplierSpend,
  ReorderRecommendation,
  TopDelayedSupplier,
} from "./types";
import { formatMoney } from "./format";

export function formatPercent(value: number): string {
  return `${value.toFixed(2)}%`;
}

interface DashboardData {
  lowStockItems: LowStockItem[];
  delayedPurchaseOrders: DelayedPurchaseOrder[];
  supplierPerformance: SupplierPerformance[];
  spendBySupplier: SupplierSpend[];
  reorderRecommendations: ReorderRecommendation[];
  topDelayedSuppliers: TopDelayedSupplier[];
}

export function computeKpis(data: DashboardData) {
  const totalSpend = data.spendBySupplier.reduce((sum, s) => sum + s.total_spend, 0);

  const avgOnTime = data.supplierPerformance.length
    ? data.supplierPerformance.reduce((sum, s) => sum + s.on_time_delivery_rate, 0) /
      data.supplierPerformance.length
    : 0;

  return {
    lowStockCount: data.lowStockItems.length,
    delayedPoCount: data.delayedPurchaseOrders.length,
    reorderCount: data.reorderRecommendations.length,
    // Raw numbers, not pre-formatted strings - KpiCards animates these with
    // AnimatedCounter, which needs the real number to count up from 0.
    totalSpend,
    avgOnTime,
  };
}

// Each SQL query behind these arrays already sorts server-side (e.g. spend
// by supplier is ORDER BY total_spend DESC), so index [0] is already "the
// top one" - no re-sorting needed here.
export function buildInsights(data: DashboardData): string[] {
  const insights: string[] = [];

  if (data.delayedPurchaseOrders.length) {
    insights.push(
      `${data.delayedPurchaseOrders.length} purchase order(s) are delayed and may need supplier follow-up.`
    );
  }

  if (data.lowStockItems.length) {
    insights.push(
      `${data.lowStockItems.length} item(s) are below reorder point and may create inventory risk.`
    );
  }

  if (data.spendBySupplier.length) {
    const topSupplier = data.spendBySupplier[0];
    insights.push(
      `${topSupplier.supplier_name} has the highest procurement spend at ${formatMoney(
        topSupplier.total_spend
      )}.`
    );
  }

  if (data.topDelayedSuppliers.length) {
    const worst = data.topDelayedSuppliers[0];
    insights.push(
      `${worst.supplier_name} is the top delayed supplier with ${worst.delayed_po_count} delayed POs, ` +
        `${worst.average_days_delayed} average days delayed, and ${worst.max_days_delayed} max days delayed.`
    );
  }

  if (data.supplierPerformance.length) {
    const riskySupplier = data.supplierPerformance[0];
    insights.push(`${riskySupplier.supplier_name} should be reviewed due to supplier performance risk.`);
  }

  if (insights.length === 0) {
    insights.push("No major procurement risks detected at this time.");
  }

  return insights;
}

export function buildActions(data: DashboardData): string[] {
  const actions: string[] = [];

  for (const item of data.reorderRecommendations) {
    actions.push(`Reorder ${item.recommended_order_quantity} units of ${item.item_name}.`);
  }

  for (const order of data.delayedPurchaseOrders) {
    actions.push(`Follow up with ${order.supplier_name} for delayed PO #${order.purchase_order_id}.`);
  }

  if (data.topDelayedSuppliers.length) {
    const worst = data.topDelayedSuppliers[0];
    actions.push(
      `Prioritize supplier review for ${worst.supplier_name} because it has ${worst.delayed_po_count} delayed POs.`
    );
  }

  if (data.supplierPerformance.length) {
    actions.push("Review supplier scorecard and prioritize suppliers with delays or low on-time rate.");
  }

  return actions;
}
