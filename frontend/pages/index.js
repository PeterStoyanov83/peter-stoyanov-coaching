import { useState, useEffect } from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';

export default function Home() {
  const { t } = useTranslation('common');
  
  // Lead magnet form state
  const [leadMagnetEmail, setLeadMagnetEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');
  const [submitError, setSubmitError] = useState('');

  // Testimonials carousel state
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  // Auto-advance testimonials
  useEffect(() => {
    if (!isAutoPlaying) return;
    
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % 10);
    }, 5000); // Change every 5 seconds

    return () => clearInterval(interval);
  }, [isAutoPlaying]);

  const nextTestimonial = () => {
    setCurrentTestimonial((prev) => (prev + 1) % 10);
    setIsAutoPlaying(false);
  };

  const prevTestimonial = () => {
    setCurrentTestimonial((prev) => (prev - 1 + 10) % 10);
    setIsAutoPlaying(false);
  };

  const goToTestimonial = (index) => {
    setCurrentTestimonial(index);
    setIsAutoPlaying(false);
  };

  const handleLeadMagnetSubmit = async (e) => {
    e.preventDefault();
    
    if (!leadMagnetEmail || !/\S+@\S+\.\S+/.test(leadMagnetEmail)) {
      setSubmitError(t('home.leadMagnet.errors.emailRequired'));
      return;
    }
    
    setIsSubmitting(true);
    setSubmitError('');
    setSubmitMessage('');
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/download-guide`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: leadMagnetEmail }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSubmitMessage(data.message);
        setLeadMagnetEmail('');
        
        // Trigger download
        const link = document.createElement('a');
        link.href = data.downloadUrl;
        link.download = '5-Theater-Secrets-Guide.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        setSubmitError(data.message || t('home.leadMagnet.errors.submitError'));
      }
    } catch (error) {
      setSubmitError(t('home.leadMagnet.errors.networkError'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('home.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('home.description')} />
      </Head>

      <Header />

      <main>
        {/* Hero Section - Custom Background */}
        <section className="relative min-h-screen flex items-center overflow-hidden">
          {/* Background Image as img element for testing */}
          <img 
            src="/pictures/hero-bg.png"
            alt="Hero Background" 
            className="absolute inset-0 w-full h-full object-cover z-0"
          />
          {/* Overlay for text readability */}
          <div className="absolute inset-0 bg-black/40 z-10"></div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-7xl mx-auto">
              <div className="text-center">
                
                <h1 className="pt-20 text-5xl md:text-6xl lg:text-7xl font-bold mb-8 leading-tight">
                  <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    {t('home.hero.title')}
                  </span>
                </h1>
                
                <p className="text-xl md:text-2xl mb-12 text-gray-300 leading-relaxed max-w-4xl mx-auto">
                  {t('home.hero.subtitle')}
                </p>
                
                <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                  <Link href="/waitlist" className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-slate-900 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-xl shadow-2xl hover:shadow-3xl transform hover:scale-105 hover:-translate-y-1 transition-all duration-300">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    {t('home.hero.cta')}
                    <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                  <Link href="/about" className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-white/10 backdrop-blur-sm border-2 border-white/20 rounded-xl shadow-xl hover:bg-white/20 transform hover:scale-105 hover:-translate-y-1 transition-all duration-300">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    {t('home.hero.meetPetar')}
                  </Link>
                </div>

                {/* Modern Stats */}
                <div className="flex justify-center">
                  <div className="grid grid-cols-2 gap-8 max-w-lg">
                    <div className="text-center bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 transform hover:scale-105 transition-all duration-300">
                      <div className="text-3xl md:text-4xl font-bold text-cyan-400 mb-2">20+</div>
                      <div className="text-gray-300 text-sm">{t('home.hero.stats.experience')}</div>
                    </div>
                    <div className="text-center bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 transform hover:scale-105 transition-all duration-300">
                      <div className="text-3xl md:text-4xl font-bold text-pink-400 mb-2">15+</div>
                      <div className="text-gray-300 text-sm">{t('home.hero.stats.countries')}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Video Introduction Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  {t('home.video.title')}
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  {t('home.video.description')}
                </p>
              </div>
              
              <div className="max-w-4xl mx-auto">
                <div className="relative w-full h-0 pb-[56.25%] rounded-2xl overflow-hidden shadow-2xl mb-12">
                  <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-indigo-600 to-purple-700 flex items-center justify-center">
                    <div className="text-center text-white">
                      <svg className="w-24 h-24 mx-auto mb-4 opacity-80" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                      <p className="text-xl font-semibold">{t('home.video.comingSoon')}</p>
                      <p className="text-indigo-200">{t('home.video.preview')}</p>
                    </div>
                  </div>
                </div>
                
                {/* Quote Section */}
                <div className="text-center">
                  <blockquote className="text-lg text-gray-700 italic leading-relaxed mb-4">
                    "{t('home.video.quote')}"
                  </blockquote>
                  <p className="text-gray-900 font-semibold text-lg">— Peter Stoyanov</p>
                  <p className="text-gray-600 mt-2">{t('home.video.credentials')}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Methodology Section - Enhanced Bold & Vibrant */}
        <section className="py-20 md:py-28 relative overflow-hidden">
          {/* Enhanced Multi-layer Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500"></div>
          <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/30 via-transparent to-yellow-400/30"></div>
          
          {/* Animated Background Elements */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-10 left-10 w-32 h-32 bg-white rounded-full mix-blend-overlay filter blur-xl animate-pulse"></div>
            <div className="absolute bottom-10 right-10 w-40 h-40 bg-yellow-300 rounded-full mix-blend-overlay filter blur-xl animate-pulse" style={{animationDelay: '1s'}}></div>
            <div className="absolute top-1/2 left-1/3 w-24 h-24 bg-pink-300 rounded-full mix-blend-overlay filter blur-xl animate-pulse" style={{animationDelay: '2s'}}></div>
          </div>
          
          {/* Pattern Overlay */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 25% 25%, white 2px, transparent 2px)',
              backgroundSize: '50px 50px'
            }}></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 text-white drop-shadow-lg">
                  {t('home.methodology.title')}
                </h2>
                <p className="text-xl md:text-2xl text-white/90 max-w-4xl mx-auto font-medium leading-relaxed drop-shadow-sm">
                  {t('home.methodology.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Method 1 - Enhanced */}
                <div className="text-center group">
                  <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-all duration-300 shadow-2xl border-2 border-white/30">
                    <svg className="w-12 h-12 text-white group-hover:text-yellow-300 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 3v3m6.364-.636l-2.12 2.12M21 12h-3m-.636 6.364l-2.12-2.12M12 21v-3m-6.364.636l2.12-2.12M3 12h3m.636-6.364l2.12 2.12" />
                      <circle cx="12" cy="12" r="6" strokeWidth={2.5} />
                      <circle cx="12" cy="12" r="2" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-2xl md:text-3xl font-black mb-4 text-white drop-shadow-lg group-hover:text-yellow-300 transition-colors duration-300">
                    {t('home.methodology.method1.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed text-lg font-medium">
                    {t('home.methodology.method1.description')}
                  </p>
                </div>
                
                {/* Method 2 - Enhanced */}
                <div className="text-center group">
                  <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-all duration-300 shadow-2xl border-2 border-white/30">
                    <svg className="w-12 h-12 text-white group-hover:text-cyan-300 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl md:text-3xl font-black mb-4 text-white drop-shadow-lg group-hover:text-cyan-300 transition-colors duration-300">
                    {t('home.methodology.method2.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed text-lg font-medium">
                    {t('home.methodology.method2.description')}
                  </p>
                </div>
                
                {/* Method 3 - Enhanced */}
                <div className="text-center group">
                  <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-all duration-300 shadow-2xl border-2 border-white/30">
                    <svg className="w-12 h-12 text-white group-hover:text-orange-300 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl md:text-3xl font-black mb-4 text-white drop-shadow-lg group-hover:text-orange-300 transition-colors duration-300">
                    {t('home.methodology.method3.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed text-lg font-medium">
                    {t('home.methodology.method3.description')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* What You'll Learn Section - Enhanced Bold & Vibrant */}
        <section className="py-20 md:py-28 relative overflow-hidden">
          {/* Dynamic Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50"></div>
          <div className="absolute inset-0 bg-gradient-to-tr from-emerald-100/50 via-transparent to-orange-100/50"></div>
          
          {/* Animated Background Shapes */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-blue-400/20 to-cyan-400/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gradient-to-r from-yellow-400/10 to-orange-400/10 rounded-full blur-2xl animate-pulse" style={{animationDelay: '4s'}}></div>
          </div>

          <div className="container mx-auto px-4 relative z-10">
            <div className="text-center mb-20">
              <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-emerald-600 bg-clip-text text-transparent drop-shadow-sm">
                {t('home.features.title')}
              </h2>
              <p className="text-xl md:text-2xl text-gray-700 max-w-4xl mx-auto font-medium leading-relaxed">
                {t('home.features.subtitle')}
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {/* Feature 1 - Stage Presence */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M7 8h10l4 8H3l4-8z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M7 8V6a2 2 0 012-2h6a2 2 0 012 2v2" />
                    <circle cx="12" cy="10" r="3" strokeWidth={2.5} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 13v6" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 19h6" />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-purple-700 transition-colors duration-300">{t('home.features.feature1.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature1.description')}</p>
              </div>

              {/* Feature 2 - Voice Techniques */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-blue-700 transition-colors duration-300">{t('home.features.feature2.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature2.description')}</p>
              </div>

              {/* Feature 3 - Body Language */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8 14v3m8-3v3" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 11h.01M15 11h.01" />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-emerald-700 transition-colors duration-300">{t('home.features.feature3.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature3.description')}</p>
              </div>

              {/* Feature 4 - Work with Camera */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-pink-500 to-pink-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="2" y="6" width="14" height="10" rx="2" strokeWidth={2.5} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M16 10l6-3v10l-6-3" />
                    <circle cx="9" cy="11" r="2" strokeWidth={2.5} />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-pink-700 transition-colors duration-300">{t('home.features.feature4.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature4.description')}</p>
              </div>

              {/* Feature 5 - Addressing Audience */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-orange-500 to-orange-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 8v4l3 3" />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-orange-700 transition-colors duration-300">{t('home.features.feature5.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature5.description')}</p>
              </div>

              {/* Feature 6 - Improvisation Skills */}
              <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-3 transition-all duration-500 border border-white/50 hover:bg-white/90">
                <div className="w-20 h-20 bg-gradient-to-br from-cyan-500 to-cyan-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-2xl md:text-3xl font-black mb-4 text-gray-900 group-hover:text-cyan-700 transition-colors duration-300">{t('home.features.feature6.title')}</h3>
                <p className="text-gray-700 leading-relaxed text-lg font-medium">{t('home.features.feature6.description')}</p>
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials Carousel Section - Enhanced Bold & Vibrant */}
        <section className="py-20 md:py-28 relative overflow-hidden">
          {/* Dynamic Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-orange-100 via-pink-100 to-purple-100"></div>
          <div className="absolute inset-0 bg-gradient-to-tl from-cyan-50/80 via-transparent to-yellow-50/80"></div>
          
          {/* Animated Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-32 -left-32 w-64 h-64 bg-gradient-to-br from-orange-300/30 to-pink-300/30 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-32 -right-32 w-80 h-80 bg-gradient-to-tr from-purple-300/30 to-cyan-300/30 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1.5s'}}></div>
            <div className="absolute top-20 right-20 w-40 h-40 bg-gradient-to-r from-yellow-300/20 to-orange-300/20 rounded-full blur-2xl animate-pulse" style={{animationDelay: '3s'}}></div>
          </div>

          <div className="container mx-auto px-4 relative z-10">
            <div className="text-center mb-20">
              <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 bg-gradient-to-r from-orange-600 via-pink-600 to-purple-600 bg-clip-text text-transparent drop-shadow-sm">
                {t('home.testimonials.title')}
              </h2>
              <p className="text-xl md:text-2xl text-gray-700 max-w-4xl mx-auto font-medium leading-relaxed">
                {t('home.testimonials.subtitle')}
              </p>
            </div>
            
            {/* Testimonials Carousel */}
            <div className="relative max-w-6xl mx-auto">
              {/* Main Carousel Container - Added extra padding for quote icons */}
              <div className="relative overflow-hidden rounded-3xl pt-8 pb-4">
                <div 
                  className="flex transition-transform duration-700 ease-in-out"
                  style={{ transform: `translateX(-${currentTestimonial * 100}%)` }}
                  onMouseEnter={() => setIsAutoPlaying(false)}
                  onMouseLeave={() => setIsAutoPlaying(true)}
                >
                  {/* Generate all 10 testimonials */}
                  {[...Array(10)].map((_, index) => {
                    const testimonialNumber = index + 1;
                    const gradientColors = [
                      'from-indigo-500 to-purple-600',
                      'from-purple-500 to-pink-600', 
                      'from-emerald-500 to-teal-600',
                      'from-orange-500 to-red-600',
                      'from-blue-500 to-cyan-600',
                      'from-pink-500 to-rose-600',
                      'from-green-500 to-emerald-600',
                      'from-yellow-500 to-orange-600',
                      'from-cyan-500 to-blue-600',
                      'from-violet-500 to-purple-600'
                    ];
                    
                    return (
                      <div key={index} className="w-full flex-shrink-0 px-8">
                        <div className="group relative bg-white/95 backdrop-blur-sm p-8 md:p-12 rounded-3xl shadow-2xl border border-white/60 max-w-5xl mx-auto mt-8">
                          {/* Decorative Quote Mark - Adjusted positioning */}
                          <div className={`absolute -top-4 -left-4 w-16 h-16 bg-gradient-to-br ${gradientColors[index]} rounded-full flex items-center justify-center shadow-xl`}>
                            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h4v10h-10z"/>
                            </svg>
                          </div>

                          <div className="flex flex-col md:flex-row items-center md:items-start gap-8">
                            {/* Avatar and Info */}
                            <div className="flex flex-col items-center md:items-start text-center md:text-left flex-shrink-0">
                              <div className={`w-24 h-24 bg-gradient-to-br ${gradientColors[index]} rounded-full flex items-center justify-center text-white font-black text-2xl shadow-xl group-hover:scale-110 transition-transform duration-300 mb-4`}>
                                {t(`home.testimonials.testimonial${testimonialNumber}.name`).split(' ').map(name => name[0]).join('')}
                              </div>
                              <h4 className="font-black text-gray-900 text-xl md:text-2xl mb-2">
                                {t(`home.testimonials.testimonial${testimonialNumber}.name`)}
                              </h4>
                              <p className="text-gray-600 font-bold text-lg">
                                {t(`home.testimonials.testimonial${testimonialNumber}.position`)}
                              </p>
                            </div>

                            {/* Testimonial Text */}
                            <div className="flex-1">
                              <p className="text-gray-800 italic leading-relaxed text-xl md:text-2xl font-medium mb-8 text-center md:text-left">
                                "{t(`home.testimonials.testimonial${testimonialNumber}.text`)}"
                              </p>
                              
                              {/* Star Rating */}
                              <div className="flex text-yellow-500 justify-center md:justify-start">
                                {[...Array(5)].map((_, i) => (
                                  <svg key={i} className="w-7 h-7 drop-shadow-sm" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                  </svg>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Navigation Arrows */}
              <button
                onClick={prevTestimonial}
                className="absolute left-4 top-1/2 -translate-y-1/2 w-14 h-14 bg-white/90 backdrop-blur-sm rounded-full shadow-xl flex items-center justify-center text-gray-700 hover:bg-white hover:scale-110 transition-all duration-300 z-10"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              
              <button
                onClick={nextTestimonial}
                className="absolute right-4 top-1/2 -translate-y-1/2 w-14 h-14 bg-white/90 backdrop-blur-sm rounded-full shadow-xl flex items-center justify-center text-gray-700 hover:bg-white hover:scale-110 transition-all duration-300 z-10"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>

              {/* Dots Indicator */}
              <div className="flex justify-center mt-12 space-x-3">
                {[...Array(10)].map((_, index) => (
                  <button
                    key={index}
                    onClick={() => goToTestimonial(index)}
                    className={`w-4 h-4 rounded-full transition-all duration-300 ${
                      currentTestimonial === index 
                        ? 'bg-gradient-to-r from-orange-500 to-pink-500 scale-125 shadow-lg' 
                        : 'bg-gray-300 hover:bg-gray-400'
                    }`}
                  />
                ))}
              </div>

              {/* Auto-play indicator */}
              <div className="text-center mt-6">
                <button
                  onClick={() => setIsAutoPlaying(!isAutoPlaying)}
                  className="text-gray-600 hover:text-gray-800 text-sm font-medium transition-colors duration-300"
                >
                  {isAutoPlaying ? '⏸️ Pause Auto-play' : '▶️ Resume Auto-play'}
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Transformation Section - Enhanced Bold & Vibrant */}
        <section className="py-20 md:py-28 relative overflow-hidden">
          {/* Multi-layer Dynamic Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-400 via-cyan-500 to-blue-600"></div>
          <div className="absolute inset-0 bg-gradient-to-tl from-purple-500/30 via-transparent to-pink-500/30"></div>
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-300/20 via-transparent to-orange-400/20"></div>
          
          {/* Animated Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-32 -left-32 w-64 h-64 bg-gradient-to-br from-green-300/30 to-blue-300/30 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-32 -right-32 w-80 h-80 bg-gradient-to-tr from-purple-300/30 to-pink-300/30 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1.5s'}}></div>
            <div className="absolute top-20 right-20 w-40 h-40 bg-gradient-to-r from-cyan-300/20 to-teal-300/20 rounded-full blur-2xl animate-pulse" style={{animationDelay: '3s'}}></div>
            <div className="absolute bottom-20 left-20 w-48 h-48 bg-gradient-to-br from-yellow-300/20 to-orange-300/20 rounded-full blur-2xl animate-pulse" style={{animationDelay: '2s'}}></div>
          </div>

          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-7xl mx-auto">
              <div className="text-center mb-20">
                <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 bg-gradient-to-r from-white via-yellow-100 to-white bg-clip-text text-transparent drop-shadow-lg">
                  {t('home.transformation.title')}
                </h2>
                <p className="text-xl md:text-2xl text-white/95 max-w-4xl mx-auto font-medium leading-relaxed">
                  {t('home.transformation.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-4 lg:gap-6 items-center">
                {/* Before - Enhanced */}
                <div className="group text-center">
                  <div className="relative inline-block mb-4">
                    <div className="w-80 h-96 rounded-3xl overflow-hidden shadow-2xl border-4 border-white/20 backdrop-blur-sm bg-white/10 p-2 transform group-hover:scale-105 transition-all duration-500">
                      <div className="w-full h-full rounded-2xl overflow-hidden">
                        <img 
                          src="/pictures/PeterStoyanov-quiet-panic.jpg" 
                          alt="Before - Communication Anxiety and Fear"
                          className="w-full h-full object-cover filter grayscale group-hover:grayscale-0 transition-all duration-500"
                        />
                      </div>
                    </div>
                    {/* Decorative Corner Element */}
                    <div className="absolute -top-6 -left-6 w-12 h-12 bg-gradient-to-br from-red-400 to-red-600 rounded-2xl rotate-45 shadow-xl opacity-90"></div>
                  </div>
                  <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/40">
                    <h3 className="text-2xl md:text-3xl font-black mb-6 bg-gradient-to-r from-red-600 to-red-800 bg-clip-text text-transparent">{t('home.transformation.before.title')}</h3>
                    <ul className="text-left space-y-4 max-w-sm mx-auto">
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.before.item1')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.before.item2')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.before.item3')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.before.item4')}</span>
                      </li>
                    </ul>
                  </div>
                </div>

                {/* SVG Journey Arrow with CSS Effects */}
                <div className="text-center flex items-center justify-center">
                  {/* Mobile Arrow */}
                  <div className="lg:hidden mb-4 mt-4">
                    <div className="relative group">
                      <img 
                        src="/arrow.svg" 
                        alt="Transformation Journey" 
                        className="w-24 h-32 mx-auto transform rotate-90 journey-arrow-mobile group-hover:scale-110 transition-all duration-500"
                      />
                      {/* Journey Enhancement Effects */}
                      <div className="absolute inset-0 journey-glow opacity-60 group-hover:opacity-90 transition-opacity duration-500"></div>
                      
                      {/* Transformation Sparkles */}
                      <div className="absolute top-4 left-1/2 w-2 h-2 bg-yellow-400 rounded-full animate-bounce transform -translate-x-1/2" style={{animationDelay: '0s'}}></div>
                      <div className="absolute top-1/2 right-2 w-2 h-2 bg-orange-400 rounded-full animate-bounce transform -translate-y-1/2" style={{animationDelay: '1s'}}></div>
                      <div className="absolute bottom-4 left-1/2 w-2 h-2 bg-emerald-400 rounded-full animate-bounce transform -translate-x-1/2" style={{animationDelay: '2s'}}></div>
                    </div>
                  </div>
                  
                  {/* Desktop Arrow */}
                  <div className="hidden lg:block">
                    <div className="relative group">
                      <img 
                        src="/arrow.svg" 
                        alt="Transformation Journey" 
                        className="w-40 h-24 mx-auto journey-arrow-desktop group-hover:scale-110 group-hover:brightness-125 transition-all duration-500"
                      />
                      
                      {/* Enhanced Glow Effect */}
                      <div className="absolute inset-0 journey-glow-desktop opacity-50 group-hover:opacity-80 transition-opacity duration-500"></div>
                      
                      {/* Flowing Energy Particles */}
                      <div className="absolute top-1/2 left-4 w-3 h-3 bg-yellow-400 rounded-full animate-ping opacity-70 transform -translate-y-1/2" style={{animationDelay: '0s'}}></div>
                      <div className="absolute top-2 left-1/3 w-2 h-2 bg-orange-400 rounded-full animate-ping opacity-70" style={{animationDelay: '1s'}}></div>
                      <div className="absolute bottom-2 left-1/2 w-2 h-2 bg-red-400 rounded-full animate-ping opacity-70 transform -translate-x-1/2" style={{animationDelay: '1.5s'}}></div>
                      <div className="absolute top-1/2 right-8 w-3 h-3 bg-emerald-400 rounded-full animate-ping opacity-70 transform -translate-y-1/2" style={{animationDelay: '2s'}}></div>
                      
                      {/* Success Aura */}
                      <div className="absolute top-0 right-2 w-1 h-1 bg-cyan-300 rounded-full animate-pulse" style={{animationDelay: '0.5s'}}></div>
                      <div className="absolute bottom-1 right-4 w-1 h-1 bg-teal-300 rounded-full animate-pulse" style={{animationDelay: '2.5s'}}></div>
                    </div>
                  </div>
                </div>

                {/* After - Enhanced */}
                <div className="group text-center">
                  <div className="relative inline-block mb-4">
                    <div className="w-80 h-96 rounded-3xl overflow-hidden shadow-2xl border-4 border-white/20 backdrop-blur-sm bg-white/10 p-2 transform group-hover:scale-105 transition-all duration-500">
                      <div className="w-full h-full rounded-2xl overflow-hidden">
                        <img 
                          src="/pictures/PeterStoyanov-I-dare-you.jpg" 
                          alt="After - Confident Communication and Presence"
                          className="w-full h-full object-cover group-hover:scale-110 transition-all duration-500"
                        />
                      </div>
                    </div>
                    {/* Decorative Corner Element */}
                    <div className="absolute -top-6 -right-6 w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-600 rounded-2xl rotate-45 shadow-xl opacity-90"></div>
                  </div>
                  <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/40">
                    <h3 className="text-2xl md:text-3xl font-black mb-6 bg-gradient-to-r from-green-600 to-emerald-700 bg-clip-text text-transparent">{t('home.transformation.after.title')}</h3>
                    <ul className="text-left space-y-4 max-w-sm mx-auto">
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.after.item1')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.after.item2')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.after.item3')}</span>
                      </li>
                      <li className="flex items-start group/item">
                        <div className="w-6 h-6 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center mr-4 mt-1 group-hover/item:scale-110 transition-transform duration-300">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <span className="text-gray-800 font-medium leading-relaxed">{t('home.transformation.after.item4')}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="text-center mt-20">
                <p className="text-2xl md:text-3xl font-black text-white mb-8 drop-shadow-lg">{t('home.transformation.cta.title')}</p>
                <Link href="/waitlist" className="group inline-flex items-center justify-center px-10 py-5 text-xl font-black text-cyan-800 bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl hover:shadow-3xl hover:bg-white transform hover:-translate-y-3 hover:scale-105 transition-all duration-300">
                  <div className="w-8 h-8 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full flex items-center justify-center mr-3 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  {t('home.transformation.cta.button')}
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Lead Magnet Section */}
        <section id="lead-magnet" className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto">
              <div className="feature-card bg-gradient-to-br from-indigo-50 to-purple-50 p-8 md:p-12 rounded-2xl shadow-xl border border-indigo-100">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                  <div>
                    <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                      <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gray-900">
                      {t('home.leadMagnetSection.title')}
                    </h2>
                    <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                      {t('home.leadMagnetSection.description')}
                    </p>
                    <ul className="space-y-3 text-gray-700 mb-8">
                      {t('home.leadMagnetSection.benefits', { returnObjects: true }).map((benefit, index) => (
                        <li key={index} className="flex items-start">
                          <svg className="w-5 h-5 text-indigo-600 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          {benefit}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="text-center lg:text-left">
                    <div className="relative inline-block mb-6">
                      <div className="w-48 h-64 bg-gradient-to-br from-indigo-600 to-purple-700 rounded-lg shadow-2xl mx-auto lg:mx-0 flex items-center justify-center">
                        <div className="text-center text-white">
                          <svg className="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                          </svg>
                          <div className="text-lg font-bold">{t('home.leadMagnetSection.guideLabel')}</div>
                          <div className="text-sm">{t('home.leadMagnetSection.pdfLabel')}</div>
                        </div>
                      </div>
                      <div className="absolute -top-2 -right-2 w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center text-gray-900 font-bold text-sm animate-pulse">
                        {t('home.leadMagnetSection.freeLabel')}
                      </div>
                    </div>
                    
                    <form onSubmit={handleLeadMagnetSubmit} className="space-y-4">
                      {submitMessage && (
                        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
                          {submitMessage}
                        </div>
                      )}
                      {submitError && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                          {submitError}
                        </div>
                      )}
                      <input
                        type="email"
                        value={leadMagnetEmail}
                        onChange={(e) => setLeadMagnetEmail(e.target.value)}
                        placeholder={t('home.leadMagnet.emailPlaceholder')}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        required
                      />
                      <button 
                        type="submit"
                        disabled={isSubmitting}
                        className={`w-full inline-flex items-center justify-center px-6 py-3 text-lg font-semibold text-white button-gradient rounded-lg shadow-lg transform transition-all duration-300 ${
                          isSubmitting ? 'opacity-70 cursor-not-allowed' : 'hover:-translate-y-1'
                        }`}
                      >
                        {isSubmitting ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            {t('home.leadMagnet.sending')}
                          </>
                        ) : (
                          <>
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                            </svg>
                            {t('home.leadMagnet.downloadButton')}
                          </>
                        )}
                      </button>
                      <p className="text-sm text-gray-500">
                        {t('home.leadMagnet.joinText')}
                      </p>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section - Enhanced Bold & Vibrant */}
        <section className="py-20 md:py-28 relative overflow-hidden">
          {/* Multi-layer Dynamic Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-600 to-orange-500"></div>
          <div className="absolute inset-0 bg-gradient-to-tl from-cyan-500/40 via-transparent to-yellow-400/40"></div>
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/30 via-transparent to-purple-600/30"></div>
          
          {/* Animated Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-32 -left-32 w-64 h-64 bg-gradient-to-br from-yellow-300/30 to-orange-300/30 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-32 -right-32 w-80 h-80 bg-gradient-to-tr from-purple-300/30 to-cyan-300/30 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1.5s'}}></div>
            <div className="absolute top-20 left-20 w-40 h-40 bg-gradient-to-r from-pink-300/20 to-purple-300/20 rounded-full blur-2xl animate-pulse" style={{animationDelay: '3s'}}></div>
            <div className="absolute bottom-20 right-20 w-48 h-48 bg-gradient-to-br from-cyan-300/20 to-indigo-300/20 rounded-full blur-2xl animate-pulse" style={{animationDelay: '2s'}}></div>
          </div>
          
          <div className="container mx-auto px-4 text-center relative z-10">
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-8 text-white drop-shadow-lg">
              {t('home.cta.title')}
            </h2>
            <p className="text-xl md:text-2xl mb-12 text-white/90 max-w-3xl mx-auto leading-relaxed font-medium">
              {t('home.cta.description')}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center max-w-2xl mx-auto">
              <Link href="/waitlist" className="group inline-flex items-center justify-center px-8 py-4 text-lg font-black text-purple-700 bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl hover:shadow-3xl hover:bg-white transform hover:-translate-y-2 hover:scale-105 transition-all duration-300">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mr-3 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                {t('home.cta.button')}
              </Link>
              <Link href="/corporate" className="group inline-flex items-center justify-center px-8 py-4 text-lg font-black text-white border-3 border-white/80 rounded-2xl backdrop-blur-sm hover:bg-white/20 hover:border-white transform hover:-translate-y-2 hover:scale-105 transition-all duration-300 shadow-xl">
                <div className="w-8 h-8 bg-gradient-to-br from-cyan-400 to-indigo-500 rounded-full flex items-center justify-center mr-3 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                {t('home.cta.corporateButton')}
              </Link>
            </div>
            
            {/* Additional Visual Elements */}
            <div className="mt-16 flex justify-center space-x-8 opacity-60">
              <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
      <BackToTop />
    </div>
  );
}

export async function getStaticProps({ locale }) {
  return {
    props: {
      ...(await serverSideTranslations(locale, ['common'])),
    },
  };
}