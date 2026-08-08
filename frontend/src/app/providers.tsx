// Two providers every page needs:
// - QueryClientProvider: TanStack Query's in-memory cache/state.
// - ThemeProvider (next-themes): toggles the "dark" class on <html> and
//   remembers the choice in localStorage. Both need a Client Component
//   ("use client"), so this is split out from layout.tsx, which stays a
//   Server Component.
"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  // useState (not a module-level constant) so each user session gets its own
  // QueryClient instance instead of sharing one across requests.
  const [queryClient] = useState(() => new QueryClient());

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </ThemeProvider>
  );
}
