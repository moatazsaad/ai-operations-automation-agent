// Wraps every section on the page: a heading with a leading icon + colored
// accent bar, plus a fade/slide-in animation that plays once when the
// section scrolls into view (not just once on initial page load) - kept as
// one component so every section animates and is titled consistently.
"use client";

import { motion } from "motion/react";
import type { LucideIcon } from "lucide-react";

interface SectionProps {
  icon: LucideIcon;
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function Section({ icon: Icon, title, children, className }: SectionProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className={`space-y-4 ${className ?? ""}`}
    >
      <h2 className="flex items-center gap-2 border-l-4 border-[#2a78d6] pl-3 text-xl font-bold">
        <Icon className="h-5 w-5 text-[#2a78d6]" />
        {title}
      </h2>
      {children}
    </motion.section>
  );
}
