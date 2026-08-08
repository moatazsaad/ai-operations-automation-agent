// TanStack Query hooks - one per GET endpoint. Each hook gives components a
// {data, isLoading, isError} triple for free, and useQueries below lets all
// 6 requests fire in parallel instead of waiting for each other one by one.
"use client";

import { useQueries, useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";

// queryKey uniquely identifies each request in TanStack Query's cache.
export function useDashboardMetrics() {
  const results = useQueries({
    queries: [
      { queryKey: ["low-stock-items"], queryFn: api.getLowStockItems },
      { queryKey: ["delayed-purchase-orders"], queryFn: api.getDelayedPurchaseOrders },
      { queryKey: ["supplier-performance"], queryFn: api.getSupplierPerformance },
      { queryKey: ["spend-by-supplier"], queryFn: api.getSpendBySupplier },
      { queryKey: ["reorder-recommendations"], queryFn: api.getReorderRecommendations },
      { queryKey: ["top-delayed-suppliers"], queryFn: api.getTopDelayedSuppliers },
    ],
  });

  const [
    lowStockItems,
    delayedPurchaseOrders,
    supplierPerformance,
    spendBySupplier,
    reorderRecommendations,
    topDelayedSuppliers,
  ] = results;

  return {
    lowStockItems: lowStockItems.data ?? [],
    delayedPurchaseOrders: delayedPurchaseOrders.data ?? [],
    supplierPerformance: supplierPerformance.data ?? [],
    spendBySupplier: spendBySupplier.data ?? [],
    reorderRecommendations: reorderRecommendations.data ?? [],
    topDelayedSuppliers: topDelayedSuppliers.data ?? [],
    // True until every query has settled at least once.
    isLoading: results.some((r) => r.isLoading),
    // True if any single query failed.
    isError: results.some((r) => r.isError),
  };
}

// Mutation for the "Ask the AI Operations Agent" panel - a POST triggered by
// a button click, not data that loads automatically on page load.
export function useAskAgent() {
  return useMutation({
    mutationFn: (prompt: string) => api.runAgent(prompt),
  });
}

// Mutation for the "Generate Weekly Operations Report" button.
export function useGenerateReport() {
  return useMutation({
    mutationFn: () => api.generateOperationsReport(),
  });
}
