// Single source of truth for chart colors - a colorblind-safe categorical
// palette (validated for CVD-safe contrast between adjacent colors).
export const CHART_COLORS = {
  blue: "#2a78d6", // Spend by Supplier
  green: "#008300", // On-Time Delivery Rate
  magenta: "#e87ba4", // Delayed Purchase Orders
  yellow: "#eda100", // Inventory Risk
  aqua: "#1baf7a", // Average Days Delayed
  orange: "#eb6834", // Max Days Delayed
} as const;
