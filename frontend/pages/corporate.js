import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import TypeformModal from '../components/TypeformModal';
import { useTranslation } from '../hooks/useTranslation';

export default function Corporate() {
  const { t } = useTranslation();
  const [isCorporateModalOpen, setIsCorporateModalOpen] = useState(false);

  return (
    <>
      <Head>
        <title>{t('corporate.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('corporate.hero.subtitle')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white">
        <Header />
        
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-indigo-900 via-indigo-800 to-purple-800 text-white py-20 pt-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                {t('corporate.hero.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('corporate.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Programs Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-center mb-16 text-gray-800">
              {t('corporate.programs.title')}
            </h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Leadership Presence</h3>
                <p className="text-gray-600 leading-relaxed">
                  Develop executive presence, confident communication, and authentic leadership style 
                  that inspires and motivates teams.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Team Communication</h3>
                <p className="text-gray-600 leading-relaxed">
                  Improve collaboration, reduce conflicts, and create a culture of open, 
                  effective communication across all levels.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Presentation Skills</h3>
                <p className="text-gray-600 leading-relaxed">
                  Master the art of compelling presentations, from structure and storytelling 
                  to delivery and audience engagement.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Change Management</h3>
                <p className="text-gray-600 leading-relaxed">
                  Navigate organizational change with clear communication strategies that 
                  build trust and reduce resistance.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Conflict Resolution</h3>
                <p className="text-gray-600 leading-relaxed">
                  Transform workplace conflicts into opportunities for growth through 
                  effective communication and mediation techniques.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Executive Coaching</h3>
                <p className="text-gray-600 leading-relaxed">
                  One-on-one coaching for C-level executives to enhance their leadership 
                  communication and strategic influence.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section with Liquid Glass Button */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold mb-6 text-gray-800">
                  {t('corporate.contact.title')}
                </h2>
                <p className="text-xl text-gray-600">
                  {t('corporate.contact.description')}
                </p>
              </div>

              <div className="bg-gradient-to-br from-indigo-50 via-white to-purple-50 rounded-2xl shadow-2xl p-12 border border-indigo-100">
                <div className="text-center space-y-8">
                  {/* Liquid Glass Typeform Button */}
                  <button
                    type="button"
                    onClick={() => setIsCorporateModalOpen(true)}
                    className="relative group overflow-hidden bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-600 hover:from-indigo-600 hover:via-purple-700 hover:to-pink-700 text-white font-bold py-5 px-10 rounded-2xl shadow-2xl transform transition-all duration-600 hover:scale-105 hover:shadow-purple-500/40 backdrop-blur-sm border border-white/20"
                  >
                    {/* Liquid glass overlay effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-white/15 via-white/8 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-800 animate-pulse"></div>
                    
                    {/* Corporate-themed glass particles */}
                    <div className="absolute inset-0 overflow-hidden rounded-2xl">
                      <div className="absolute -top-3 -left-3 w-6 h-6 bg-white/25 rounded-full animate-float delay-200"></div>
                      <div className="absolute -bottom-3 -right-3 w-4 h-4 bg-white/20 rounded-full animate-float delay-400"></div>
                      <div className="absolute top-1/4 right-1/3 w-3 h-3 bg-white/30 rounded-full animate-float delay-600"></div>
                    </div>
                    
                    {/* Button content */}
                    <div className="relative z-10 flex items-center justify-center space-x-3">
                      <svg className="w-6 h-6 transform group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      <span className="text-lg tracking-wide font-semibold">
                        Request Consultation
                      </span>
                      <div className="w-2 h-2 bg-yellow-300 rounded-full animate-pulse"></div>
                    </div>
                    
                    {/* Professional shimmer effect */}
                    <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1200 bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-12"></div>
                  </button>
                  
                  <p className="text-gray-600 max-w-2xl mx-auto leading-relaxed">
                    Ready to transform your team's communication skills? Our professional training programs are designed to create lasting impact through proven theater-based techniques.
                  </p>
                  
                  {/* Visual enhancement dots */}
                  <div className="flex justify-center space-x-2">
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse delay-300"></div>
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-pulse delay-600"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <Footer />
        <BackToTop />

        {/* Corporate Training Typeform Modal */}
        <TypeformModal
          isOpen={isCorporateModalOpen}
          onClose={() => setIsCorporateModalOpen(false)}
          typeformId="YRsIpOvV"
          title="Request Corporate Training Consultation"
          description="Tell us about your organization's needs and let's discuss how we can help your team excel."
        />
      </div>
    </>
  );
}