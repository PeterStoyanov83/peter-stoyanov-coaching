const { i18n } = require('./next-i18next.config');

module.exports = {
  i18n,
  reactStrictMode: true,
  
  // GitHub Pages configuration
  output: 'export',
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/coaching-site' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/coaching-site' : '',
  
  // Image optimization (disabled for static export)
  images: {
    unoptimized: true,
  },
};