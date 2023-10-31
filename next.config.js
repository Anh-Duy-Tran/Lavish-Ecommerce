/** @type {import('next').NextConfig} */
const nextConfig = {
  compiler: {
    // Enables the styled-components SWC transform
    styledComponents: true,
  },
  images: {
    domains: ["images.ctfassets.net"],
  },
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig;
