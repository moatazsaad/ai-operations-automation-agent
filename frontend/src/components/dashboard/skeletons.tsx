// Loading placeholders shaped like the section they stand in for, instead of
// one generic gray rectangle - so the page doesn't visibly "jump" in layout
// once real data replaces them.
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function KpiSkeletons() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {Array.from({ length: 5 }).map((_, i) => (
        <Card key={i}>
          <CardContent className="flex items-start gap-3 px-5">
            <Skeleton className="h-9 w-9 shrink-0 rounded-full" />
            <div className="w-full space-y-2">
              <Skeleton className="h-3 w-3/4" />
              <Skeleton className="h-6 w-1/2" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export function InsightSkeletons() {
  return (
    <div className="grid sm:grid-cols-2 gap-3">
      {Array.from({ length: 4 }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full rounded-lg" />
      ))}
    </div>
  );
}

export function ActionSkeletons() {
  return (
    <div className="space-y-2">
      {Array.from({ length: 4 }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full rounded-lg" />
      ))}
    </div>
  );
}

export function ChartSkeletons() {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-4 w-1/2" />
          </CardHeader>
          <CardContent>
            {/* A handful of bars at random-ish heights so it reads as "a
                chart is loading here" rather than a blank box. */}
            <div className="flex h-[280px] items-end gap-2">
              {[60, 90, 45, 75, 55, 85, 40].map((h, j) => (
                <Skeleton key={j} className="flex-1" style={{ height: `${h}%` }} />
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export function TableSkeleton() {
  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-8 w-32" />
        ))}
      </div>
      <div className="space-y-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-9 w-full" />
        ))}
      </div>
    </div>
  );
}
