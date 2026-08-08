// The single dashboard page - fetches all metrics and derives the
// insights/actions/KPIs shown across the sections below.
"use client";

import { Package, Bot, BarChart3, Lightbulb, CheckCircle2, LineChart, FolderOpen, FileText } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { ThemeToggle } from "@/components/theme-toggle";
import { useDashboardMetrics } from "@/hooks/use-metrics";
import { computeKpis, buildInsights, buildActions } from "@/lib/derive-dashboard-text";
import { KpiCards } from "@/components/dashboard/kpi-cards";
import { AiInsights } from "@/components/dashboard/ai-insights";
import { RecommendedActions } from "@/components/dashboard/recommended-actions";
import { ProcurementAnalytics } from "@/components/dashboard/procurement-analytics";
import { DetailedDataTabs } from "@/components/dashboard/detailed-data-tabs";
import { AskAgentPanel } from "@/components/dashboard/ask-agent-panel";
import { GenerateReportButton } from "@/components/dashboard/generate-report-button";
import { Section } from "@/components/dashboard/section";
import {
  KpiSkeletons,
  InsightSkeletons,
  ActionSkeletons,
  ChartSkeletons,
  TableSkeleton,
} from "@/components/dashboard/skeletons";

export default function DashboardPage() {
  const metrics = useDashboardMetrics();

  return (
    <div className="mx-auto w-full max-w-7xl flex-1 space-y-8 px-6 py-8">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="flex items-center gap-2 text-3xl font-extrabold tracking-tight">
            <Package className="h-7 w-7 text-[#2a78d6]" />
            AI Procurement Control Tower
          </h1>
          <p className="mt-1 text-muted-foreground">
            Real-time supplier performance, inventory risk, and spend visibility - powered by an AI
            operations agent.
          </p>
        </div>
        <ThemeToggle />
      </div>
      <Separator />

      <Section icon={Bot} title="Ask the AI Operations Agent">
        <AskAgentPanel />
      </Section>
      <Separator />

      {metrics.isError && (
        <p className="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          Could not load data from the API. Confirm the backend is running and reachable.
        </p>
      )}

      <Section icon={BarChart3} title="Executive Overview">
        {metrics.isLoading ? <KpiSkeletons /> : <KpiCards {...computeKpis(metrics)} />}
      </Section>
      <Separator />

      <Section icon={Lightbulb} title="AI Insights">
        {metrics.isLoading ? <InsightSkeletons /> : <AiInsights insights={buildInsights(metrics)} />}
      </Section>
      <Separator />

      <Section icon={CheckCircle2} title="Recommended Actions">
        {metrics.isLoading ? (
          <ActionSkeletons />
        ) : (
          <RecommendedActions actions={buildActions(metrics)} />
        )}
      </Section>
      <Separator />

      <Section icon={LineChart} title="Procurement Analytics">
        {metrics.isLoading ? (
          <ChartSkeletons />
        ) : (
          <ProcurementAnalytics
            spendBySupplier={metrics.spendBySupplier}
            supplierPerformance={metrics.supplierPerformance}
            reorderRecommendations={metrics.reorderRecommendations}
            topDelayedSuppliers={metrics.topDelayedSuppliers}
          />
        )}
      </Section>
      <Separator />

      <Section icon={FolderOpen} title="Detailed Procurement Data">
        {metrics.isLoading ? (
          <TableSkeleton />
        ) : (
          <DetailedDataTabs
            reorderRecommendations={metrics.reorderRecommendations}
            lowStockItems={metrics.lowStockItems}
            delayedPurchaseOrders={metrics.delayedPurchaseOrders}
            supplierPerformance={metrics.supplierPerformance}
            spendBySupplier={metrics.spendBySupplier}
            topDelayedSuppliers={metrics.topDelayedSuppliers}
          />
        )}
      </Section>
      <Separator />

      <Section icon={FileText} title="Executive Report Generation" className="pb-8">
        <GenerateReportButton />
      </Section>
    </div>
  );
}
