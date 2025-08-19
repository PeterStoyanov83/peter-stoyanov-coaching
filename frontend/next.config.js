const { i18n } = require('./next-i18next.config');

module.exports = {
  i18n,
  reactStrictMode: true,
  
  // GitHub Pages configuration
  output: 'export',
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/peter-stoyanov-coaching' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/peter-stoyanov-coaching' : '',
  
  // Image optimization (disabled for static export)
  images: {
    unoptimized: true,
  },
};