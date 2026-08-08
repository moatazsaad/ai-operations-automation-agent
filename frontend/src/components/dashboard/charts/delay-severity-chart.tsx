// The one grouped chart on the dashboard: average vs. max days delayed,
// per supplier, shown as two bars side by side instead of two separate
// charts you'd otherwise have to mentally cross-reference.
"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import type { TopDelayedSupplier } from "@/lib/types";
import { CHART_COLORS } from "@/lib/colors";

export function DelaySeverityChart({ data }: { data: TopDelayedSupplier[] }) {
  const chartData = data.map((s) => ({
    name: s.supplier_name,
    "Average Days Delayed": s.average_days_delayed,
    "Max Days Delayed": s.max_days_delayed,
  }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={chartData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip cursor={{ fill: "var(--muted)" }} />
        <Legend />
        <Bar dataKey="Average Days Delayed" fill={CHART_COLORS.aqua} radius={[4, 4, 0, 0]} />
        <Bar dataKey="Max Days Delayed" fill={CHART_COLORS.orange} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
