// Animates a number counting up from 0 to its real value on mount, instead
// of just popping into view. Takes a plain number and an optional formatter
// so it can render "$33,614,650.00" or "69.33%" while still animating the
// underlying number.
"use client";

import { useEffect, useRef } from "react";
import { useMotionValue, animate } from "motion/react";

interface AnimatedCounterProps {
  value: number;
  formatter?: (n: number) => string;
  className?: string;
}

export function AnimatedCounter({ value, formatter, className }: AnimatedCounterProps) {
  const spanRef = useRef<HTMLSpanElement>(null);
  // A MotionValue holds the in-progress number during the animation - it
  // lives outside React state so updating it every frame doesn't trigger a
  // React re-render each time (better animation performance).
  const motionValue = useMotionValue(0);

  useEffect(() => {
    const format = formatter ?? ((n: number) => Math.round(n).toLocaleString());

    // Write the very first frame synchronously so the number doesn't
    // flash "0" before the animation's first tick fires.
    if (spanRef.current) spanRef.current.textContent = format(0);

    const controls = animate(motionValue, value, {
      duration: 1,
      ease: "easeOut",
      onUpdate: (latest) => {
        if (spanRef.current) spanRef.current.textContent = format(latest);
      },
    });

    return () => controls.stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value]);

  return <span ref={spanRef} className={className} />;
}
