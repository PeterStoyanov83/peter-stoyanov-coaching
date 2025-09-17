import { useLanguage } from '../contexts/LanguageContext';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { CheckCircle, Clock, Heart, Users, BookOpen, User, Share2, Home, Target, Linkedin, Facebook } from 'lucide-react';

export default function ThankYou() {
  const { t } = useLanguage();
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
        <title>{t('thankYou.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('thankYou.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-10 left-10 w-72 h-72 bg-blue-300/8 rounded-full blur-xl animate-float"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-green-300/8 rounded-full blur-xl animate-float-delayed"></div>
            <div className="absolute bottom-10 left-1/2 w-72 h-72 bg-purple-300/8 rounded-full blur-xl animate-float-slow"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto text-center">
              <div className="mb-8 animate-fade-in-up">
                <div className="w-24 h-24 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mx-auto shadow-2xl transform hover:scale-110 transition-all duration-300">
                  <CheckCircle className="w-12 h-12 text-white" strokeWidth={2} />
                </div>
              </div>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span className="bg-gradient-to-r from-green-300 via-teal-300 to-blue-300 bg-clip-text text-transparent">
                  {t('thankYou.title')}
                </span>
              </h1>
              
              <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                {formType === 'corporate' 
                  ? t('thankYou.messages.corporate')
                  : formType === 'waitlist'
                  ? t('thankYou.messages.waitlist')
                  : t('thankYou.messages.general')
                }
              </p>
              
              {/* Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto animate-fade-in-up delay-200">
                <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                  <div className="text-3xl font-black text-yellow-300 mb-3 drop-shadow-lg">24hrs</div>
                  <div className="text-blue-100/90 font-semibold">{t('thankYou.stats.responseTime')}</div>
                </div>
                <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300">
                  <div className="text-3xl font-black text-green-300 mb-3 drop-shadow-lg">95%</div>
                  <div className="text-blue-100/90 font-semibold">{t('thankYou.stats.satisfactionRate')}</div>
                </div>
                <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                  <div className="text-3xl font-black text-purple-300 mb-3 drop-shadow-lg">1000+</div>
                  <div className="text-blue-100/90 font-semibold">{t('thankYou.stats.livesTransformed')}</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Next Steps Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">
          {/* Floating Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-1/4 right-1/4 w-80 h-80 bg-gradient-to-br from-blue-300/8 to-teal-400/8 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-indigo-300/8 to-purple-400/8 rounded-full blur-3xl animate-float-delayed"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('thankYou.nextSteps.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('thankYou.nextSteps.subtitle')}
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm p-8 md:p-12 rounded-3xl shadow-2xl border border-white/20 animate-fade-in-up delay-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {/* Step 1 */}
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                      <span className="text-white font-black text-xl">1</span>
                    </div>
                    <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">
                      {formType === 'corporate' ? t('thankYou.nextSteps.step1.corporate') : t('thankYou.nextSteps.step1.general')}
                    </h3>
                    <p className="text-white/90 leading-relaxed">
                      {formType === 'corporate' 
                        ? t('thankYou.nextSteps.step1.corporateDesc')
                        : t('thankYou.nextSteps.step1.generalDesc')
                      }
                    </p>
                  </div>
                  
                  {/* Step 2 */}
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                      <span className="text-white font-black text-xl">2</span>
                    </div>
                    <h3 className="text-xl font-black mb-4 text-green-200 drop-shadow-lg">
                      {formType === 'corporate' ? t('thankYou.nextSteps.step2.corporate') : t('thankYou.nextSteps.step2.general')}
                    </h3>
                    <p className="text-white/90 leading-relaxed">
                      {formType === 'corporate'
                        ? t('thankYou.nextSteps.step2.corporateDesc')
                        : t('thankYou.nextSteps.step2.generalDesc')
                      }
                    </p>
                  </div>
                  
                  {/* Step 3 */}
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                      <span className="text-white font-black text-xl">3</span>
                    </div>
                    <h3 className="text-xl font-black mb-4 text-purple-200 drop-shadow-lg">
                      {formType === 'corporate' ? t('thankYou.nextSteps.step3.corporate') : t('thankYou.nextSteps.step3.general')}
                    </h3>
                    <p className="text-white/90 leading-relaxed">
                      {formType === 'corporate'
                        ? t('thankYou.nextSteps.step3.corporateDesc')
                        : t('thankYou.nextSteps.step3.generalDesc')
                      }
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                <div className="text-center lg:text-left">
                  <div className="flex flex-col gap-4">
                    <Link href="/" className="inline-flex items-center justify-center px-8 py-4 text-lg font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl transform transition-all duration-300 border-4 border-white/80 hover:scale-110 hover:-rotate-2 hover:shadow-3xl">
                      <Home className="w-5 h-5 mr-2" strokeWidth={2} />
                      {t('thankYou.actions.returnHome')}
                    </Link>
                    
                    <Link href="/about" className="inline-flex items-center justify-center px-8 py-4 text-lg font-black text-white bg-white/10 backdrop-blur-sm border-2 border-white/30 rounded-2xl shadow-2xl hover:bg-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <User className="w-5 h-5 mr-2" strokeWidth={2} />
                      {t('thankYou.actions.learnAbout')}
                    </Link>
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-100 h-200 rounded-3xl overflow-hidden shadow-2xl border-8 border-white">
                      <img 
                        src="/pictures/PeterStoyanov-nice-smile.jpg"
                        alt="Peter Stoyanov - Planning Your Communication Journey"
                        className="w-full h-full object-cover"
                      />
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Additional Resources Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 relative overflow-hidden">
          {/* Floating Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-1/3 left-1/3 w-72 h-72 bg-yellow-300/8 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-1/3 right-1/3 w-96 h-96 bg-purple-300/8 rounded-full blur-3xl animate-float-delayed"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('thankYou.resources.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('thankYou.resources.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Resource 1 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 text-center transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                  <div className="w-16 h-16 bg-gradient-to-br from-slate-600 to-blue-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <BookOpen className="w-8 h-8 text-white" strokeWidth={2} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('thankYou.resources.freeGuide.title')}</h3>
                  <p className="text-white/90 mb-6 leading-relaxed">{t('thankYou.resources.freeGuide.description')}</p>
                  <Link href="/#lead-magnet" className="inline-flex items-center text-yellow-300 font-black hover:text-yellow-200 transform hover:scale-105 transition-all duration-300">
                    {t('thankYou.resources.freeGuide.action')}
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
                
                {/* Resource 2 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 text-center transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <User className="w-8 h-8 text-white" strokeWidth={2} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('thankYou.resources.aboutPetar.title')}</h3>
                  <p className="text-white/90 mb-6 leading-relaxed">{t('thankYou.resources.aboutPetar.description')}</p>
                  <Link href="/about" className="inline-flex items-center text-purple-300 font-black hover:text-purple-200 transform hover:scale-105 transition-all duration-300">
                    {t('thankYou.resources.aboutPetar.action')}
                    <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
                
                {/* Resource 3 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 text-center transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                  <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <Share2 className="w-8 h-8 text-white" strokeWidth={2} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-cyan-200 drop-shadow-lg">{t('thankYou.resources.shareInspire.title')}</h3>
                  <p className="text-white/90 mb-6 leading-relaxed">{t('thankYou.resources.shareInspire.description')}</p>
                  <div className="flex justify-center space-x-3">
                    <a href="https://www.linkedin.com/sharing/share-offsite/" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center text-white transition duration-300 transform hover:scale-110">
                      <Linkedin className="w-5 h-5" strokeWidth={2} />
                    </a>
                    <a href="https://www.facebook.com/sharer/sharer.php" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-blue-500 hover:bg-blue-600 rounded-full flex items-center justify-center text-white transition duration-300 transform hover:scale-110">
                      <Facebook className="w-5 h-5" strokeWidth={2} />
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

