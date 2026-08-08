// Renders the plain-English insight strings from lib/derive-dashboard-text.ts
// in a 2-column grid, matching app/dashboard.py's layout.
import { Lightbulb } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

export function AiInsights({ insights }: { insights: string[] }) {
  return (
    <div className="grid sm:grid-cols-2 gap-3">
      {insights.map((insight) => (
        <Alert key={insight}>
          <Lightbulb className="h-4 w-4" />
          <AlertDescription>{insight}</AlertDescription>
        </Alert>
      ))}
    </div>
  );
}
