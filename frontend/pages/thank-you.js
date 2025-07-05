import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function ThankYou() {
  const { t } = useTranslation('common');
  const router = useRouter();
  const [formType, setFormType] = useState('general');

  useEffect(() => {
    const { type } = router.query;
    if (type) {
      setFormType(type);
    }
  }, [router.query]);

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('thankYou.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('thankYou.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative hero-gradient pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-30">
            <div className="absolute top-10 left-10 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
            <div className="absolute bottom-10 left-1/2 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-500"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto text-center">
              <div className="mb-8">
                <div className="w-24 h-24 button-gradient rounded-full flex items-center justify-center mx-auto shadow-xl">
                  <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8 text-gray-900 leading-tight">
                <span className="text-gradient-primary">
                  Thank You!
                </span>
              </h1>
              
              <p className="text-xl md:text-2xl mb-12 text-gray-600 max-w-3xl mx-auto leading-relaxed">
                {formType === 'corporate' 
                  ? "Your corporate training inquiry has been received. We'll prepare a customized proposal for your team."
                  : formType === 'waitlist'
                  ? "Welcome to our exclusive community! You're now on the waitlist for our transformative workshops."
                  : "Your message has been received. We'll be in touch soon to discuss your communication journey."
                }
              </p>
              
              {/* Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">24hrs</div>
                  <div className="text-gray-600">Response Time</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-indigo-600 mb-2">95%</div>
                  <div className="text-gray-600">Satisfaction Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">1000+</div>
                  <div className="text-gray-600">Lives Transformed</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Next Steps Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  What Happens Next?
                </h2>
                <p className="text-xl text-gray-600">
                  Here's your roadmap to communication transformation
                </p>
              </div>
              
              <div className="feature-card bg-gradient-to-br from-indigo-50 to-purple-50 p-8 md:p-12 rounded-2xl shadow-xl border border-indigo-100">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {/* Step 1 */}
                  <div className="text-center">
                    <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                      <span className="text-white font-bold text-xl">1</span>
                    </div>
                    <h3 className="text-xl font-bold mb-4 text-gray-900">
                      {formType === 'corporate' ? 'Proposal Review' : 'Email Confirmation'}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {formType === 'corporate' 
                        ? 'We\'ll analyze your team\'s needs and prepare a customized training proposal within 24 hours.'
                        : 'Check your email for a confirmation message with exclusive resources and next steps.'
                      }
                    </p>
                  </div>
                  
                  {/* Step 2 */}
                  <div className="text-center">
                    <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                      <span className="text-white font-bold text-xl">2</span>
                    </div>
                    <h3 className="text-xl font-bold mb-4 text-gray-900">
                      {formType === 'corporate' ? 'Strategy Call' : 'Personal Consultation'}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {formType === 'corporate'
                        ? 'We\'ll schedule a strategy call to discuss your training goals and answer any questions.'
                        : 'Receive a personal consultation to discuss your communication goals and workshop options.'
                      }
                    </p>
                  </div>
                  
                  {/* Step 3 */}
                  <div className="text-center">
                    <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                      <span className="text-white font-bold text-xl">3</span>
                    </div>
                    <h3 className="text-xl font-bold mb-4 text-gray-900">
                      {formType === 'corporate' ? 'Transform Your Team' : 'Begin Your Journey'}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {formType === 'corporate'
                        ? 'Experience the transformation as your team develops authentic communication skills and confidence.'
                        : 'Start your journey to confident communication with our proven theater-based techniques.'
                      }
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                <div className="text-center lg:text-left">
                  <div className="flex flex-col gap-4">
                    <Link href="/" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white button-gradient rounded-xl shadow-lg hover:-translate-y-1 transform transition-all duration-300">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                      </svg>
                      Return Home
                    </Link>
                    
                    <Link href="/about" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-600 rounded-xl shadow-lg hover:shadow-xl hover:bg-indigo-50 transform hover:-translate-y-1 transition-all duration-300">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Learn About Petar
                    </Link>
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl">
                      <img 
                        src="/pictures/PeterStoyanov-thinking-2.jpg" 
                        alt="Petar Stoyanov - Planning Your Communication Journey"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -bottom-4 -right-4 w-20 h-20 bg-gradient-to-br from-green-500 to-teal-600 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">🎯</div>
                        <div className="text-xs">Next</div>
                        <div className="text-xs">Steps</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Additional Resources Section */}
        <section className="py-20 md:py-28 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  While You Wait...
                </h2>
                <p className="text-xl text-gray-600">
                  Explore these resources to start your transformation journey today
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Resource 1 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg text-center">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Free Guide</h3>
                  <p className="text-gray-600 mb-6">Download "5 Theater Secrets to Command Any Room" for instant confidence tips</p>
                  <Link href="/#lead-magnet" className="inline-flex items-center text-indigo-600 font-semibold hover:text-indigo-700">
                    Get Free Guide
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
                
                {/* Resource 2 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg text-center">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">About Petar</h3>
                  <p className="text-gray-600 mb-6">Learn about Petar's 20+ year journey from actor to international communication coach</p>
                  <Link href="/about" className="inline-flex items-center text-indigo-600 font-semibold hover:text-indigo-700">
                    Read His Story
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
                
                {/* Resource 3 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg text-center">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Share & Inspire</h3>
                  <p className="text-gray-600 mb-6">Help others discover the power of confident communication by sharing your journey</p>
                  <div className="flex justify-center space-x-3">
                    <a href="https://www.linkedin.com/sharing/share-offsite/" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-blue-700 hover:bg-blue-800 rounded-full flex items-center justify-center text-white transition duration-300">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                    <a href="https://www.facebook.com/sharer/sharer.php" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center text-white transition duration-300">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/></svg>
                    </a>
                  </div>
                </div>
              </div>
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