// "Generate Weekly Operations Report" button. Calls the existing POST
// /generate-operations-report endpoint (unchanged backend logic), then shows
// the actual generated PDF inline on the page via GET /reports/{filename}.
"use client";

import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle2, FileText } from "lucide-react";
import { useGenerateReport } from "@/hooks/use-metrics";
import { reportFileUrl } from "@/lib/api";

export function GenerateReportButton() {
  const { mutate, data, isPending, isError, error } = useGenerateReport();

  return (
    <div className="space-y-3">
      <Button onClick={() => mutate()} disabled={isPending}>
        {isPending ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" /> Generating...
          </>
        ) : (
          <>
            <FileText className="h-4 w-4" /> Generate Weekly Operations Report
          </>
        )}
      </Button>

      {isError && (
        <p className="text-sm text-destructive">Failed to generate report: {error.message}</p>
      )}

      {data && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm font-medium text-[#008300]">
            <CheckCircle2 className="h-4 w-4" />
            {data.message}
          </div>
          {/* Embeds the actual PDF right on the page - no extra click needed */}
          <iframe
            src={reportFileUrl(data.pdf_path)}
            title="Weekly Operations Report"
            className="h-[800px] w-full rounded-lg border"
          />
        </div>
      )}
    </div>
  );
}
