// The 6-tab detailed data section, mirroring app/dashboard.py's tab order.
"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataTable } from "./data-table";
import type {
  LowStockItem,
  DelayedPurchaseOrder,
  SupplierPerformance,
  SupplierSpend,
  ReorderRecommendation,
  TopDelayedSupplier,
} from "@/lib/types";

interface DetailedDataTabsProps {
  reorderRecommendations: ReorderRecommendation[];
  lowStockItems: LowStockItem[];
  delayedPurchaseOrders: DelayedPurchaseOrder[];
  supplierPerformance: SupplierPerformance[];
  spendBySupplier: SupplierSpend[];
  topDelayedSuppliers: TopDelayedSupplier[];
}

export function DetailedDataTabs(props: DetailedDataTabsProps) {
  return (
    <Tabs defaultValue="reorder">
      <TabsList className="flex-wrap h-auto">
        <TabsTrigger value="reorder">Reorder Recommendations</TabsTrigger>
        <TabsTrigger value="low-stock">Low Stock</TabsTrigger>
        <TabsTrigger value="delayed-pos">Delayed POs</TabsTrigger>
        <TabsTrigger value="supplier-performance">Supplier Performance</TabsTrigger>
        <TabsTrigger value="spend">Spend by Supplier</TabsTrigger>
        <TabsTrigger value="top-delayed">Top Delayed Suppliers</TabsTrigger>
      </TabsList>

      <TabsContent value="reorder" className="mt-4">
        <DataTable rows={props.reorderRecommendations} emptyMessage="No reorder recommendations." />
      </TabsContent>
      <TabsContent value="low-stock" className="mt-4">
        <DataTable rows={props.lowStockItems} emptyMessage="No low-stock items." />
      </TabsContent>
      <TabsContent value="delayed-pos" className="mt-4">
        <DataTable rows={props.delayedPurchaseOrders} emptyMessage="No delayed purchase orders." />
      </TabsContent>
      <TabsContent value="supplier-performance" className="mt-4">
        <DataTable rows={props.supplierPerformance} emptyMessage="No supplier performance data." />
      </TabsContent>
      <TabsContent value="spend" className="mt-4">
        <DataTable rows={props.spendBySupplier} emptyMessage="No spend data." />
      </TabsContent>
      <TabsContent value="top-delayed" className="mt-4">
        <DataTable rows={props.topDelayedSuppliers} emptyMessage="No delayed supplier severity data." />
      </TabsContent>
    </Tabs>
  );
}
