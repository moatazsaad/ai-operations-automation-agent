// Reusable horizontal bar chart for "top N, sorted, single series" data -
// 4 of the 5 charts on this dashboard (spend, on-time rate, delayed POs,
// inventory risk) are this exact shape and only differ in data/color/title,
// so one parameterized component replaces 4 near-identical ones.
"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

interface TopNBarChartProps {
  // Each row is a plain {name, value} pair - callers reshape their raw API
  // data into this before rendering, so this component knows nothing about
  // suppliers/items/spend specifically.
  data: { name: string; value: number }[];
  color: string;
  topN?: number;
}

export function TopNBarChart({ data, color, topN = 10 }: TopNBarChartProps) {
  const sorted = [...data].sort((a, b) => b.value - a.value).slice(0, topN);

  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart
        data={sorted}
        layout="vertical"
        margin={{ top: 8, right: 16, bottom: 8, left: 8 }}
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
        <XAxis type="number" tick={{ fontSize: 12 }} />
        <YAxis
          type="category"
          dataKey="name"
          width={140}
          tick={{ fontSize: 12 }}
        />
        <Tooltip cursor={{ fill: "var(--muted)" }} />
        <Bar dataKey="value" fill={color} radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
