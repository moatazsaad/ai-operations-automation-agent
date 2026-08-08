import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Build a plain folder of HTML/CSS/JS instead of a Node server - this is
  // what lets the app be hosted on S3 + CloudFront instead of needing a
  // server to run.
  output: "export",

  // Image Optimization needs a server to resize images on the fly, which a
  // static export doesn't have. This app has no images to optimize, but
  // turning it off avoids a build error if one is ever added.
  images: { unoptimized: true },

  // Makes every route export as folder/index.html (e.g. /about/index.html)
  // instead of /about.html, which is easier to serve correctly from S3.
  trailingSlash: true,
};

export default nextConfig;
