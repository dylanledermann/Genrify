import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  turbopack: {
    root: path.join(__dirname, '..'),
  },
};

module.exports = {
  experimental: {
    serverActions: true,
  },
}

export default nextConfig;
