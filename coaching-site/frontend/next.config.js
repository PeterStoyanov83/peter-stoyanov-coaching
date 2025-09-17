module.exports = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // Removed assetPrefix and basePath for Cloudflare Pages deployment with custom domain
};