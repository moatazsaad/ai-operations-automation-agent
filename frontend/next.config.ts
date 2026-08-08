import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Build a plain folder of HTML/CSS/JS instead of a Node server - this is
  // what lets Nginx serve it directly with no server process needed.
  output: "export",

  // Image Optimization needs a server to resize images on the fly, which a
  // static export doesn't have. This app has no images to optimize, but
  // turning it off avoids a build error if one is ever added.
  images: { unoptimized: true },

  // Makes every route export as folder/index.html (e.g. /about/index.html)
  // instead of /about.html, which is easier to serve correctly from Nginx.
  trailingSlash: true,

  // Stops `next dev` from regenerating AGENTS.md/CLAUDE.md in this folder.
  agentRules: false,
};

export default nextConfig;
