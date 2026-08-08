// Shows the first 8 recommended actions inline. If there are more, a
// "view all" dialog holds the rest.
"use client";

import { CheckCircle2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const VISIBLE_ACTION_COUNT = 8;

export function RecommendedActions({ actions }: { actions: string[] }) {
  if (actions.length === 0) {
    return (
      <p className="rounded-lg border bg-card px-4 py-3 text-sm text-muted-foreground">
        No urgent action required.
      </p>
    );
  }

  const visibleActions = actions.slice(0, VISIBLE_ACTION_COUNT);
  const remainingCount = actions.length - visibleActions.length;

  return (
    <div className="space-y-2">
      {visibleActions.map((action) => (
        <ActionRow key={action} text={action} />
      ))}

      {remainingCount > 0 && (
        <Dialog>
          <DialogTrigger render={<Button variant="outline" size="sm" className="mt-1" />}>
            View all {actions.length} recommended actions
          </DialogTrigger>
          <DialogContent className="max-h-[70vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>All recommended actions ({actions.length})</DialogTitle>
            </DialogHeader>
            <div className="space-y-2">
              {actions.map((action) => (
                <ActionRow key={action} text={action} />
              ))}
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}

function ActionRow({ text }: { text: string }) {
  return (
    <div className="flex items-start gap-2 rounded-lg border bg-card px-4 py-3 text-sm">
      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-[#008300]" />
      <span>{text}</span>
    </div>
  );
}
