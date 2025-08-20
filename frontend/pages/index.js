import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function Home() {
  const { t } = useTranslation();
  
  // Lead magnet form state
  const [leadMagnetEmail, setLeadMagnetEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const handleLeadMagnetSubmit = async (e) => {
    e.preventDefault();
    if (!leadMagnetEmail) return;

    setIsSubmitting(true);
    setSubmitMessage('');

    try {
      const response = await fetch('/api/download-guide', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: leadMagnetEmail }),
      });

      const data = await response.json();

      if (data.success) {
        setSubmitMessage('✅ Check your email for the guide download link!');
        setLeadMagnetEmail('');
        
        // Open download link if available
        if (data.downloadUrl) {
          window.open(data.downloadUrl, '_blank');
        }
      } else {
        setSubmitMessage('❌ Something went wrong. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setSubmitMessage('❌ Something went wrong. Please try again.');
    }

    setIsSubmitting(false);
  };

  return (
    <>
      <Head>
        <title>Peter Stoyanov - {t('home.hero.subtitle')}</title>
        <meta name="description" content={t('home.hero.description')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen">
        <Header />
        
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-indigo-900 via-indigo-800 to-purple-800 text-white py-20 pt-32 overflow-hidden">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="relative container mx-auto px-4 text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              {t('home.hero.title')}
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-indigo-100 max-w-3xl mx-auto">
              {t('home.hero.description')}
            </p>
            
            {/* Lead Magnet Form */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 max-w-md mx-auto mb-8">
              <h3 className="text-lg font-semibold mb-4">🎭 Free Voice & Presence Guide</h3>
              <form onSubmit={handleLeadMagnetSubmit} className="space-y-4">
                <input
                  type="email"
                  value={leadMagnetEmail}
                  onChange={(e) => setLeadMagnetEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full px-4 py-2 rounded-lg text-gray-800 placeholder-gray-500"
                  required
                />
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300 disabled:opacity-50"
                >
                  {isSubmitting ? 'Sending...' : t('home.cta.primary')}
                </button>
              </form>
              {submitMessage && (
                <p className="mt-3 text-sm">{submitMessage}</p>
              )}
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/contact"
                className="bg-white text-indigo-900 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition duration-300"
              >
                {t('home.cta.secondary')}
              </Link>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-center mb-16 text-gray-800">
              {t('services.title')}
            </h2>
            
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">
                  {t('services.individual.title')}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {t('services.individual.description')}
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">
                  {t('services.corporate.title')}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {t('services.corporate.description')}
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">
                  {t('services.leadership.title')}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {t('services.leadership.description')}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-indigo-900 text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-8">
              Ready to Transform Your Leadership?
            </h2>
            <p className="text-xl mb-8 text-indigo-200 max-w-2xl mx-auto">
              Join hundreds of professionals who have unlocked their potential through proven communication strategies.
            </p>
            <Link 
              href="/contact"
              className="bg-white text-indigo-900 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition duration-300 inline-block"
            >
              Get Started Today
            </Link>
          </div>
        </section>

        <Footer />
        <BackToTop />
      </div>
    </>
  );
}