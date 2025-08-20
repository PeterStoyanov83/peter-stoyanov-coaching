/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/peter-stoyanov-coaching' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/peter-stoyanov-coaching' : '',
  images: {
    unoptimized: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // i18n for static export - we'll handle this manually
  // Note: Static export doesn't support automatic i18n, so we'll build separate pages
}

module.exports = nextConfig