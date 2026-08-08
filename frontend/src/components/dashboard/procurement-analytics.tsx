// The 5-chart analytics section: 2x2 grid of top-10 horizontal bars, plus
// one full-width grouped bar chart underneath. Mirrors the layout in
// app/dashboard.py's "Procurement Analytics" section.
import { motion } from "motion/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TopNBarChart } from "./charts/top-n-bar-chart";
import { DelaySeverityChart } from "./charts/delay-severity-chart";
import { CHART_COLORS } from "@/lib/colors";
import type {
  SupplierSpend,
  SupplierPerformance,
  ReorderRecommendation,
  TopDelayedSupplier,
} from "@/lib/types";

interface ProcurementAnalyticsProps {
  spendBySupplier: SupplierSpend[];
  supplierPerformance: SupplierPerformance[];
  reorderRecommendations: ReorderRecommendation[];
  topDelayedSuppliers: TopDelayedSupplier[];
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <motion.div whileHover={{ y: -3 }} className="h-full">
      <Card className="h-full transition-shadow hover:shadow-md">
        <CardHeader>
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
        </CardHeader>
        <CardContent>{children}</CardContent>
      </Card>
    </motion.div>
  );
}

export function ProcurementAnalytics({
  spendBySupplier,
  supplierPerformance,
  reorderRecommendations,
  topDelayedSuppliers,
}: ProcurementAnalyticsProps) {
  return (
    <div className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <ChartCard title="Spend by Supplier (Top 10)">
          <TopNBarChart
            data={spendBySupplier.map((s) => ({ name: s.supplier_name, value: s.total_spend }))}
            color={CHART_COLORS.blue}
          />
        </ChartCard>

        <ChartCard title="Delivered PO On-Time Rate by Supplier (Top 10)">
          <TopNBarChart
            data={supplierPerformance.map((s) => ({
              name: s.supplier_name,
              value: s.on_time_delivery_rate,
            }))}
            color={CHART_COLORS.green}
          />
        </ChartCard>

        <ChartCard title="Delayed Purchase Orders by Supplier (Top 10)">
          <TopNBarChart
            data={supplierPerformance.map((s) => ({
              name: s.supplier_name,
              value: s.delayed_purchase_orders,
            }))}
            color={CHART_COLORS.magenta}
          />
        </ChartCard>

        <ChartCard title="Inventory Risk by Item (Top 10)">
          <TopNBarChart
            data={reorderRecommendations.map((r) => ({
              name: r.item_name,
              value: r.recommended_order_quantity,
            }))}
            color={CHART_COLORS.yellow}
          />
        </ChartCard>
      </div>

      <ChartCard title="Top Delayed Suppliers: Average vs Max Days Delayed">
        <DelaySeverityChart data={topDelayedSuppliers} />
      </ChartCard>
    </div>
  );
}
