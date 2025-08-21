import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import TypeformModal from '../components/TypeformModal';
import { useTranslation } from '../hooks/useTranslation';

export default function Waitlist() {
  const { t } = useTranslation();
  const [isWaitlistModalOpen, setIsWaitlistModalOpen] = useState(false);

  return (
    <>
      <Head>
        <title>{t('waitlist.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('waitlist.description')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white">
        <Header />
        
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 overflow-hidden pt-20">
          {/* Animated Background Elements */}
          <div className="absolute inset-0">
            <div className="absolute top-20 left-20 w-40 h-40 bg-cyan-400/20 rounded-full blur-xl animate-pulse"></div>
            <div className="absolute bottom-20 right-20 w-60 h-60 bg-purple-400/20 rounded-full blur-2xl animate-pulse delay-300"></div>
            <div className="absolute top-1/2 left-1/2 w-80 h-80 bg-pink-400/10 rounded-full blur-3xl animate-pulse delay-600"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto text-center">
              
              {/* Hero Content */}
              <div className="mb-12">
                <h1 className="text-5xl md:text-6xl font-black text-white mb-6 drop-shadow-2xl">
                  {t('waitlist.form.title')}
                </h1>
                <p className="text-xl md:text-2xl text-indigo-200 mb-8 max-w-3xl mx-auto">
                  {t('waitlist.form.subtitle')}
                </p>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-8 mb-12">
                <div className="text-center">
                  <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                    <div className="text-3xl font-black text-yellow-300 mb-2">
                      {t('waitlist.hero.stats.limited')}
                    </div>
                    <div className="text-white/80 font-semibold">
                      {t('waitlist.hero.stats.spotsAvailable')}
                    </div>
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                    <div className="text-3xl font-black text-green-300 mb-2">
                      {t('waitlist.hero.stats.early')}
                    </div>
                    <div className="text-white/80 font-semibold">
                      {t('waitlist.hero.stats.birdPricing')}
                    </div>
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                    <div className="text-3xl font-black text-cyan-300 mb-2">
                      {t('waitlist.hero.stats.exclusive')}
                    </div>
                    <div className="text-white/80 font-semibold">
                      {t('waitlist.hero.stats.access')}
                    </div>
                  </div>
                </div>
              </div>

              {/* Liquid Glass Typeform Button */}
              <div className="space-y-8">
                <button
                  type="button"
                  onClick={() => setIsWaitlistModalOpen(true)}
                  className="relative group overflow-hidden bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 hover:from-cyan-500 hover:via-blue-600 hover:to-purple-700 text-white font-black py-6 px-12 rounded-3xl shadow-2xl transform transition-all duration-700 hover:scale-110 hover:shadow-cyan-500/50 backdrop-blur-lg border border-white/30"
                >
                  {/* Liquid glass overlay effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-1000 animate-pulse"></div>
                  
                  {/* Floating glass particles */}
                  <div className="absolute inset-0 overflow-hidden rounded-3xl">
                    <div className="absolute -top-6 -left-6 w-12 h-12 bg-white/30 rounded-full animate-bounce delay-100"></div>
                    <div className="absolute -bottom-6 -right-6 w-8 h-8 bg-white/25 rounded-full animate-bounce delay-300"></div>
                    <div className="absolute top-1/3 left-1/3 w-6 h-6 bg-white/20 rounded-full animate-bounce delay-500"></div>
                    <div className="absolute bottom-1/3 right-1/4 w-4 h-4 bg-white/30 rounded-full animate-bounce delay-700"></div>
                  </div>
                  
                  {/* Button content */}
                  <div className="relative z-10 flex items-center justify-center space-x-4">
                    <svg className="w-8 h-8 transform group-hover:rotate-180 transition-transform duration-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                    <span className="text-2xl tracking-wide">
                      {t('waitlist.form.submitButton')}
                    </span>
                    <div className="w-3 h-3 bg-yellow-300 rounded-full animate-bounce"></div>
                  </div>
                  
                  {/* Advanced shimmer effect */}
                  <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1500 bg-gradient-to-r from-transparent via-white/40 to-transparent skew-x-12 delay-200"></div>
                </button>
                
                <p className="text-lg text-indigo-200/90 font-semibold leading-relaxed max-w-md mx-auto">
                  {t('waitlist.form.privacyNote')}
                </p>
                
                {/* Visual enhancement */}
                <div className="flex justify-center space-x-2 mt-8">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-300"></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse delay-600"></div>
                </div>
              </div>

              {/* Quote */}
              <div className="mt-16 max-w-2xl mx-auto">
                <blockquote className="text-xl md:text-2xl text-white/90 italic font-light leading-relaxed">
                  "{t('waitlist.hero.quote')}"
                </blockquote>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl">
                  {t('waitlist.benefits.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold">
                  {t('waitlist.benefits.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Benefit 1 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 transition-all duration-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-yellow-200">
                    {t('waitlist.benefits.earlyAccess.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.earlyAccess.description')}
                  </p>
                </div>
                
                {/* Benefit 2 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 transition-all duration-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0V6a2 2 0 012-2h2a2 2 0 012 2v1M8 7h8m-8 0a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V9a2 2 0 00-2-2m0 0V6a2 2 0 00-2-2H8a2 2 0 00-2 2v3" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-green-200">
                    {t('waitlist.benefits.flexible.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.flexible.description')}
                  </p>
                </div>
                
                {/* Benefit 3 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 transition-all duration-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m3 5.197v1M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-purple-200">
                    {t('waitlist.benefits.community.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.community.description')}
                  </p>
                </div>
                
                {/* Benefit 4 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 transition-all duration-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-cyan-200">
                    {t('waitlist.benefits.personalized.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.personalized.description')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <Footer />
        <BackToTop />

        {/* Waitlist Typeform Modal */}
        <TypeformModal
          isOpen={isWaitlistModalOpen}
          onClose={() => setIsWaitlistModalOpen(false)}
          typeformId="YRsIpOvV"
          title="Join the Stage Presence Waitlist"
          description="Secure your spot for early access to our transformational program with exclusive benefits."
        />
      </div>
    </>
  );
}