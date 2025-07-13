import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="bg">
      <Head>
        {/* Critical CSS inline for hero section */}
        <style dangerouslySetInnerHTML={{
          __html: `
            /* Critical CSS for above-the-fold content */
            .hero-critical {
              position: relative;
              min-height: 100vh;
              display: flex;
              align-items: center;
              overflow: hidden;
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .hero-bg {
              position: absolute;
              inset: 0;
              width: 100%;
              height: 100%;
              object-fit: cover;
              z-index: 0;
            }
            .hero-overlay {
              position: absolute;
              inset: 0;
              background: rgba(0, 0, 0, 0.4);
              z-index: 10;
            }
            .hero-content {
              position: relative;
              z-index: 10;
              text-align: center;
              color: white;
              padding: 1rem;
            }
            .hero-title {
              font-size: clamp(2rem, 5vw, 4rem);
              font-weight: 700;
              margin-bottom: 1.5rem;
              line-height: 1.2;
            }
            .hero-subtitle {
              font-size: clamp(1rem, 2.5vw, 1.5rem);
              margin-bottom: 2rem;
              opacity: 0.9;
              max-width: 800px;
              margin-left: auto;
              margin-right: auto;
            }
            .hero-cta {
              display: inline-flex;
              align-items: center;
              justify-content: center;
              padding: 1rem 2rem;
              font-size: 1.125rem;
              font-weight: 600;
              background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
              color: white;
              text-decoration: none;
              border-radius: 0.75rem;
              transition: transform 0.2s;
            }
            .hero-cta:hover {
              transform: translateY(-2px);
            }
            /* Font display optimization */
            @font-face {
              font-family: 'system-ui';
              font-display: swap;
            }
          `
        }} />
        
        {/* SEO Meta Description */}
        <meta name="description" content="Петър Стоянов – Тренинг за сценично присъствие и увереност. Преодолей страха от сцената и говори с харизма." />
        
        {/* Favicons */}
        <link rel="apple-touch-icon" sizes="180x180" href="/favicons/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicons/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicons/favicon-16x16.png" />
        <link rel="manifest" href="/favicons/site.webmanifest" />
        <link rel="shortcut icon" href="/favicons/favicon.ico" />
        
        {/* DNS Prefetch for external resources */}
        <link rel="dns-prefetch" href="//fonts.googleapis.com" />
        
        {/* Preload critical hero image */}
        <link rel="preload" as="image" href="/pictures/hero-bg.webp" type="image/webp" />
        <link rel="preload" as="image" href="/pictures/hero-bg.png" type="image/png" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}