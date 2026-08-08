// Light/dark toggle button. next-themes only knows the real theme after the
// component mounts in the browser (it reads localStorage), so before that we
// render a plain disabled placeholder - this avoids a server/client mismatch
// where the icon would flash from wrong-to-right on first load.
"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // This is the standard next-themes pattern for detecting "we're now
  // running in the browser, past the first render" - there's no external
  // system to subscribe to here, just a one-time flag flip, so the newer
  // "no setState in effect" lint rule is a false positive on this exact case.
  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => setMounted(true), []);

  if (!mounted) {
    return <Button variant="outline" size="icon" disabled className="opacity-0" />;
  }

  const isDark = resolvedTheme === "dark";

  return (
    <Button
      variant="outline"
      size="icon"
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      onClick={() => setTheme(isDark ? "light" : "dark")}
    >
      {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
}
