module.exports = {
  i18n: {
    defaultLocale: 'bg',
    locales: ['bg', 'en'],
    localeDetection: false,
  },
  localePath: './public/locales',
  reloadOnPrerender: process.env.NODE_ENV === 'development',
};