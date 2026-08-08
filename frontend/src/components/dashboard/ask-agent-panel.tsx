// "Ask the AI Operations Agent" panel. Sends the typed question to the
// existing POST /run-agent endpoint (unchanged backend logic).
"use client";

import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, Sparkles } from "lucide-react";
import { useAskAgent } from "@/hooks/use-metrics";

const SUGGESTED_QUESTIONS = [
  "Show me delayed purchase orders",
  "Show me top delayed suppliers by average days delayed",
  "Show me low stock items",
  "Give me reorder recommendations",
  "Generate weekly operations report",
];

export function AskAgentPanel() {
  const [prompt, setPrompt] = useState("");
  const { mutate, data, isPending, isError, error } = useAskAgent();

  function handleAsk() {
    if (!prompt.trim()) return;
    mutate(prompt);
  }

  return (
    <div className="grid md:grid-cols-3 gap-4">
      <div className="md:col-span-2 space-y-3">
        <label htmlFor="agent-prompt" className="text-sm font-medium">
          Ask a procurement, inventory, supplier, sales, or reporting question:
        </label>
        <Textarea
          id="agent-prompt"
          placeholder="Example: Show me top delayed suppliers by average days delayed"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="min-h-[120px]"
        />
        <Button onClick={handleAsk} disabled={isPending}>
          {isPending ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Asking...
            </>
          ) : (
            "Ask Agent"
          )}
        </Button>

        {isError && (
          <Alert variant="destructive">
            <AlertDescription>Could not reach the AI agent: {error.message}</AlertDescription>
          </Alert>
        )}

        {data && (
          <Card>
            <CardContent className="flex gap-2 pt-4 text-sm">
              <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-[#2a78d6]" />
              <p className="whitespace-pre-wrap">{data.response}</p>
            </CardContent>
          </Card>
        )}
      </div>

      <div>
        <p className="mb-2 text-sm font-medium">Suggested demo questions</p>
        <pre className="whitespace-pre-wrap rounded-lg border bg-muted/40 p-3 text-xs">
          {SUGGESTED_QUESTIONS.join("\n")}
        </pre>
      </div>
    </div>
  );
}
