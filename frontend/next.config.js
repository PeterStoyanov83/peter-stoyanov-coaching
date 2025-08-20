// const { i18n } = require('./next-i18next.config');

module.exports = {
  // i18n, // Disabled for static export
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

  // Webpack configuration to exclude backup files
  webpack: (config, { isServer }) => {
    // Exclude backup files from build
    config.module.rules.push({
      test: /\.(js|jsx|ts|tsx)$/,
      exclude: [
        /node_modules/,
        /pages\/_backup/,
        /pages\/.*\.backup\./,
        /_backup/
      ]
    });
    
    return config;
  },

  // Page extensions
  pageExtensions: ['js', 'jsx', 'ts', 'tsx'].filter(ext => !ext.includes('backup')),
};