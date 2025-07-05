import { useState } from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Home() {
  const { t } = useTranslation('common');
  
  // Lead magnet form state
  const [leadMagnetEmail, setLeadMagnetEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');
  const [submitError, setSubmitError] = useState('');

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
      const response = await fetch('/api/download-guide', {
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
        <title>{t('home.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('home.description')} />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative hero-gradient pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-30">
            <div className="absolute top-10 left-10 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
            <div className="absolute bottom-10 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-500"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-7xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center lg:text-left">
                  <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8 text-gray-900 leading-tight">
                    <span className="text-gradient-primary">
                      {t('home.hero.title')}
                    </span>
                  </h1>
                  <p className="text-xl md:text-2xl mb-12 text-gray-600 leading-relaxed">
                    <strong>{t('home.hero.subtitle')}</strong>
                  </p>
                  
                  <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-12">
                    <Link href="/waitlist" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white button-gradient rounded-xl shadow-lg">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      {t('home.hero.cta')}
                    </Link>
                    <Link href="/about" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-600 rounded-xl shadow-lg hover:shadow-xl hover:bg-indigo-50 transform hover:-translate-y-1 transition-all duration-300">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      {t('home.hero.meetPetar')}
                    </Link>
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-3 gap-6">
                    <div className="text-center lg:text-left">
                      <div className="text-3xl md:text-4xl font-bold text-indigo-600 mb-2">20+</div>
                      <div className="text-gray-600">{t('home.hero.stats.experience')}</div>
                    </div>
                    <div className="text-center lg:text-left">
                      <div className="text-3xl md:text-4xl font-bold text-purple-600 mb-2">500+</div>
                      <div className="text-gray-600">{t('home.hero.stats.students')}</div>
                    </div>
                    <div className="text-center lg:text-left">
                      <div className="text-3xl md:text-4xl font-bold text-pink-600 mb-2">15+</div>
                      <div className="text-gray-600">{t('home.hero.stats.countries')}</div>
                    </div>
                  </div>
                </div>
                
                <div className="text-center lg:text-right">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 md:w-96 md:h-[28rem] lg:w-[400px] lg:h-[500px] rounded-2xl overflow-hidden shadow-2xl transform rotate-3 hover:rotate-0 transition-transform duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-powerfull-pic.jpg" 
                        alt="Petar Stoyanov - Professional Communication Coach"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -bottom-4 -left-4 w-24 h-24 button-gradient rounded-full flex items-center justify-center text-white font-bold text-lg shadow-xl">
                      <span>Coach</span>
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
                  Watch Petar share his unique approach to stage presence and communication training.
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                <div className="lg:col-span-2">
                  <div className="relative w-full h-0 pb-[56.25%] rounded-2xl overflow-hidden shadow-2xl">
                    <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-indigo-600 to-purple-700 flex items-center justify-center">
                      <div className="text-center text-white">
                        <svg className="w-24 h-24 mx-auto mb-4 opacity-80" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M8 5v14l11-7z"/>
                        </svg>
                        <p className="text-xl font-semibold">Video Coming Soon</p>
                        <p className="text-indigo-200">Exclusive training preview</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="text-center lg:text-left">
                  <div className="relative inline-block mb-6">
                    <div className="w-64 h-80 rounded-2xl overflow-hidden shadow-xl">
                      <img 
                        src="/pictures/PeterStoyanov-nice-smile.jpg" 
                        alt="Petar Stoyanov - Warm and Approachable Coach"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                  <blockquote className="text-lg text-gray-700 italic leading-relaxed">
                    "Every person has a unique voice and presence. My role is to help you discover and amplify yours."
                  </blockquote>
                  <p className="text-gray-900 font-semibold mt-4 text-lg">— Petar Stoyanov</p>
                  <p className="text-gray-600 mt-2">Actor, Coach & Communication Expert</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Methodology Section */}
        <section className="py-20 md:py-28 button-gradient relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-xl"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-xl"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
                  Learning Through Practice
                </h2>
                <p className="text-xl text-indigo-100 max-w-3xl mx-auto">
                  Skip traditional theory. Experience immediate transformation through proven theater techniques that create lasting change.
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Method 1 */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v3m6.364-.636l-2.12 2.12M21 12h-3m-.636 6.364l-2.12-2.12M12 21v-3m-6.364.636l2.12-2.12M3 12h3m.636-6.364l2.12 2.12" />
                      <circle cx="12" cy="12" r="6" strokeWidth={2} />
                      <circle cx="12" cy="12" r="2" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-white">Feel the Change</h3>
                  <p className="text-indigo-100 leading-relaxed">
                    Experience breakthrough moments as fear transforms into confidence through hands-on exercises.
                  </p>
                </div>
                
                {/* Method 2 */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.5 14.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5 1.5.67 1.5 1.5z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12c0-2.21 1.79-4 4-4s4 1.79 4 4" />
                      <circle cx="12" cy="8" r="3" strokeWidth={2} />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 20c0-4 3-6 6-6s6 2 6 6" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-white">Discover Your Voice</h3>
                  <p className="text-indigo-100 leading-relaxed">
                    Uncover your unique communication style and authentic presence that captivates any audience.
                  </p>
                </div>
                
                {/* Method 3 */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4" />
                      <circle cx="12" cy="12" r="9" strokeWidth={2} />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12h6l3-6 3 6h6" />
                      <circle cx="12" cy="12" r="3" fill="currentColor" opacity={0.3} />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-white">Apply Immediately</h3>
                  <p className="text-indigo-100 leading-relaxed">
                    Use your new skills right away in meetings, presentations, and important conversations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* What You'll Learn Section */}
        <section className="py-20 md:py-28 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="text-center mb-20">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                {t('home.features.title')}
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Develop the skills that will transform how you communicate and connect with others.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {/* Feature 1 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10l4 8H3l4-8z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8V6a2 2 0 012-2h6a2 2 0 012 2v2" />
                    <circle cx="12" cy="10" r="3" strokeWidth={2} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 13v6" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19h6" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">{t('home.features.feature1.title')}</h3>
                <p className="text-gray-600 leading-relaxed">{t('home.features.feature1.description')}</p>
              </div>

              {/* Feature 2 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2a10 10 0 100 20 10 10 0 000-20z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v12" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10v4" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 10v4" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 8h12v8H6z" fill="currentColor" fillOpacity={0.1} />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">{t('home.features.feature2.title')}</h3>
                <p className="text-gray-600 leading-relaxed">{t('home.features.feature2.description')}</p>
              </div>

              {/* Feature 3 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 6L4 2m0 0L0 6m4-4v12" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 2L16 6m4-4l-4 4m4-4v12" />
                    <circle cx="12" cy="12" r="10" strokeWidth={1.5} opacity={0.3} />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">{t('home.features.feature3.title')}</h3>
                <p className="text-gray-600 leading-relaxed">{t('home.features.feature3.description')}</p>
              </div>

              {/* Feature 4 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="2" y="6" width="14" height="10" rx="2" strokeWidth={2} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 10l6-3v10l-6-3" />
                    <circle cx="9" cy="11" r="2" strokeWidth={2} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 18h2m4 0h2" />
                    <rect x="4" y="4" width="2" height="2" rx="1" fill="currentColor" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Camera Presence</h3>
                <p className="text-gray-600 leading-relaxed">Excel in video meetings, interviews, and digital presentations with commanding on-camera confidence.</p>
              </div>

              {/* Feature 5 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8L5 6" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8L19 6" />
                    <circle cx="12" cy="12" r="1" fill="currentColor" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Interview Mastery</h3>
                <p className="text-gray-600 leading-relaxed">Conquer job interviews, media appearances, and high-stakes conversations with authentic confidence.</p>
              </div>

              {/* Feature 6 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    <circle cx="12" cy="12" r="4" strokeWidth={1.5} opacity={0.3} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v8M8 12h8" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Improvisation Skills</h3>
                <p className="text-gray-600 leading-relaxed">Build quick thinking and adaptability for any speaking situation.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-20">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                {t('home.testimonials.title')}
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Hear from students who have transformed their communication skills.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {/* Testimonial 1 */}
              <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-8 rounded-2xl shadow-lg">
                <div className="flex items-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl mr-4">
                    MP
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-lg">{t('home.testimonials.testimonial1.name')}</h4>
                    <p className="text-gray-600">{t('home.testimonials.testimonial1.position')}</p>
                  </div>
                </div>
                <p className="text-gray-700 italic leading-relaxed">"{t('home.testimonials.testimonial1.text')}"</p>
                <div className="flex text-yellow-400 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
              </div>

              {/* Testimonial 2 */}
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-8 rounded-2xl shadow-lg">
                <div className="flex items-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full flex items-center justify-center text-white font-bold text-xl mr-4">
                    GN
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-lg">{t('home.testimonials.testimonial2.name')}</h4>
                    <p className="text-gray-600">{t('home.testimonials.testimonial2.position')}</p>
                  </div>
                </div>
                <p className="text-gray-700 italic leading-relaxed">"{t('home.testimonials.testimonial2.text')}"</p>
                <div className="flex text-yellow-400 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
              </div>

              {/* Testimonial 3 */}
              <div className="bg-gradient-to-br from-green-50 to-teal-50 p-8 rounded-2xl shadow-lg">
                <div className="flex items-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center text-white font-bold text-xl mr-4">
                    AS
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-lg">Anna Stefanova</h4>
                    <p className="text-gray-600">Marketing Director</p>
                  </div>
                </div>
                <p className="text-gray-700 italic leading-relaxed">"The workshop gave me tools I use daily. My presentations are now engaging and confident."</p>
                <div className="flex text-yellow-400 mt-4">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Transformation Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-gray-50 to-indigo-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  From Fear to Fearless
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Experience the journey from communication anxiety to confident presence
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                {/* Before */}
                <div className="text-center">
                  <div className="relative inline-block mb-8">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl filter grayscale hover:grayscale-0 transition-all duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-quiet-panic.jpg" 
                        alt="Before - Communication Anxiety and Fear"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -top-4 -left-4 w-16 h-16 bg-red-500 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      😰
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">Before: Silent Struggle</h3>
                  <ul className="text-left text-gray-600 space-y-2 max-w-sm mx-auto">
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-red-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Racing heart before speaking
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-red-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Avoiding important conversations
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-red-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Feeling invisible in meetings
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-red-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Self-doubt and overthinking
                    </li>
                  </ul>
                </div>

                {/* Arrow */}
                <div className="text-center lg:hidden">
                  <svg className="w-12 h-12 mx-auto text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </div>
                <div className="hidden lg:block text-center">
                  <svg className="w-12 h-12 mx-auto text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </div>

                {/* After */}
                <div className="text-center">
                  <div className="relative inline-block mb-8">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl transform hover:scale-105 transition-transform duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-I-dare-you.jpg" 
                        alt="After - Confident Communication and Presence"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -top-4 -right-4 w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      🎯
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">After: Commanding Presence</h3>
                  <ul className="text-left text-gray-600 space-y-2 max-w-sm mx-auto">
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-green-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Speaking with calm confidence
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-green-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Leading important discussions
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-green-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Commanding attention naturally
                    </li>
                    <li className="flex items-start">
                      <svg className="w-5 h-5 text-green-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Authentic self-expression
                    </li>
                  </ul>
                </div>
              </div>
              
              <div className="text-center mt-16">
                <p className="text-2xl font-semibold text-gray-900 mb-6">Ready for Your Transformation?</p>
                <Link href="/waitlist" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white button-gradient rounded-xl shadow-lg hover:-translate-y-1 transform transition-all duration-300">
                  Start Your Journey
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
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
                      Free Download: "5 Theater Secrets to Command Any Room"
                    </h2>
                    <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                      Discover the professional techniques actors use to captivate audiences and eliminate stage fright. 
                      These proven methods will transform your presence in meetings, presentations, and conversations.
                    </p>
                    <ul className="space-y-3 text-gray-700 mb-8">
                      <li className="flex items-start">
                        <svg className="w-5 h-5 text-indigo-600 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Instantly calm your nerves before any important conversation
                      </li>
                      <li className="flex items-start">
                        <svg className="w-5 h-5 text-indigo-600 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Use voice and posture to project unshakeable confidence
                      </li>
                      <li className="flex items-start">
                        <svg className="w-5 h-5 text-indigo-600 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Master the art of authentic storytelling that engages audiences
                      </li>
                      <li className="flex items-start">
                        <svg className="w-5 h-5 text-indigo-600 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Quick exercises to improve your on-camera presence
                      </li>
                    </ul>
                  </div>
                  
                  <div className="text-center lg:text-left">
                    <div className="relative inline-block mb-6">
                      <div className="w-48 h-64 bg-gradient-to-br from-indigo-600 to-purple-700 rounded-lg shadow-2xl mx-auto lg:mx-0 flex items-center justify-center">
                        <div className="text-center text-white">
                          <svg className="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                          </svg>
                          <div className="text-lg font-bold">FREE GUIDE</div>
                          <div className="text-sm">PDF Download</div>
                        </div>
                      </div>
                      <div className="absolute -top-2 -right-2 w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center text-gray-900 font-bold text-sm animate-pulse">
                        FREE
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

        {/* CTA Section */}
        <section className="py-20 md:py-28 button-gradient relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-xl"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-xl"></div>
          </div>
          
          <div className="container mx-auto px-4 text-center relative z-10">
            <h2 className="text-4xl md:text-5xl font-bold mb-8 text-white">
              {t('home.cta.title')}
            </h2>
            <p className="text-xl md:text-2xl mb-12 text-indigo-100 max-w-3xl mx-auto leading-relaxed">
              {t('home.cta.description')}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/waitlist" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-indigo-600 bg-white rounded-xl shadow-lg hover:bg-gray-100 transition-all duration-300">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                {t('home.cta.button')}
              </Link>
              <Link href="/corporate" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white border-2 border-white rounded-xl hover:bg-white hover:text-indigo-600 transform hover:-translate-y-1 transition-all duration-300">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                Corporate Training
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
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