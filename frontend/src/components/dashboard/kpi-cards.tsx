// The 5 headline numbers at the top of the dashboard. Each card gets a
// colored icon chip (so the eye can tell them apart at a glance, not just by
// reading the label) and an AnimatedCounter that counts up to its value
// instead of just appearing.
"use client";

import { motion } from "motion/react";
import { Card, CardContent } from "@/components/ui/card";
import { AnimatedCounter } from "./animated-counter";
import { formatMoney } from "@/lib/format";
import { formatPercent } from "@/lib/derive-dashboard-text";
import { CHART_COLORS } from "@/lib/colors";
import { Package, Clock, RotateCcw, DollarSign, TrendingUp } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface KpiCardsProps {
  lowStockCount: number;
  delayedPoCount: number;
  reorderCount: number;
  totalSpend: number;
  avgOnTime: number;
}

interface KpiDefinition {
  label: string;
  value: number;
  formatter?: (n: number) => string;
  icon: LucideIcon;
  color: string;
}

function buildKpiList(props: KpiCardsProps): KpiDefinition[] {
  return [
    { label: "Low-Stock Items", value: props.lowStockCount, icon: Package, color: CHART_COLORS.yellow },
    { label: "Delayed POs", value: props.delayedPoCount, icon: Clock, color: CHART_COLORS.magenta },
    {
      label: "Reorder Recommendations",
      value: props.reorderCount,
      icon: RotateCcw,
      color: CHART_COLORS.blue,
    },
    {
      label: "Total Procurement Spend",
      value: props.totalSpend,
      formatter: formatMoney,
      icon: DollarSign,
      color: CHART_COLORS.green,
    },
    {
      label: "Avg Delivered On-Time",
      value: props.avgOnTime,
      formatter: formatPercent,
      icon: TrendingUp,
      color: CHART_COLORS.aqua,
    },
  ];
}

// Parent + child variants make the 5 cards fade/slide in one after another
// instead of all popping in at once.
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};
const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0 },
};

export function KpiCards(props: KpiCardsProps) {
  const kpis = buildKpiList(props);

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4"
    >
      {kpis.map((kpi) => (
        <motion.div key={kpi.label} variants={item} whileHover={{ y: -3 }}>
          <Card className="h-full transition-shadow hover:shadow-md">
            <CardContent className="flex items-start gap-3 px-5">
              <div
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full"
                style={{ backgroundColor: `${kpi.color}1a`, color: kpi.color }}
              >
                <kpi.icon className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  {kpi.label}
                </p>
                <p className="mt-1 text-2xl font-bold">
                  <AnimatedCounter value={kpi.value} formatter={kpi.formatter} />
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </motion.div>
  );
}
