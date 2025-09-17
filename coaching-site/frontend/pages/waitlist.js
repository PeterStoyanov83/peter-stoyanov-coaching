import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import TypeformModal from '../components/TypeformModal';
import { useLanguage } from '../contexts/LanguageContext';
import { Sparkles, Brain, Star, Calendar, Users, Lightbulb } from 'lucide-react';

export default function Waitlist() {
  const { t } = useLanguage();
  const [isWaitlistModalOpen, setIsWaitlistModalOpen] = useState(false);


  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('waitlist.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('waitlist.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 pt-24 pb-20 md:pt-32 md:pb-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span className="bg-gradient-to-r from-blue-300 via-teal-300 to-indigo-300 bg-clip-text text-transparent">
                  {t('waitlist.title')}
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                {t('waitlist.description')}
              </p>
              
              {/* Stats & Image */}
              <div className="flex flex-col items-center mt-20">
                <div className="w-full max-w-6xl">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 justify-items-center animate-fade-in-up delay-200">
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-yellow-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.limited')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.spotsAvailable')}</div>
                    </div>
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-green-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.early')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.birdPricing')}</div>
                    </div>
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-orange-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.exclusive')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.access')}</div>
                    </div>
                  </div>
                  <div className="col-span-full mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl animate-fade-in-up delay-300">
                    <p className="text-xl italic text-white font-semibold leading-relaxed text-center">
                      "{t('waitlist.hero.quote')}"
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Understanding Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('waitlist.understanding.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('waitlist.understanding.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-100 h-100 rounded-2xl overflow-hidden shadow-xl">
                      <img
                        src="/pictures/PeterStoyanov-preplexed.jpg"
                        alt="Peter Stoyanov - Understanding Communication Challenges"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-3xl font-black mb-8 text-white drop-shadow-lg">
                    {t('waitlist.understanding.challenges.title')}
                  </h3>
                  <div className="space-y-6">
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up">
                      <div className="w-12 h-12 bg-gradient-to-br from-red-400 to-pink-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                          <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.fear.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.fear.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-100">
                      <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.impostor.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.impostor.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-200">
                      <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.presence.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.presence.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-300">
                      <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.camera.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.camera.description')}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl animate-fade-in-up delay-400">
                    <p className="text-xl font-black text-white mb-4 drop-shadow-lg">{t('waitlist.understanding.truth.title')}</p>
                    <p className="text-white/90 leading-relaxed font-semibold">{t('waitlist.understanding.truth.description')}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

          {/* Registration Form Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="bg-white/10 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12 border border-white/20">
                <div className="text-center mb-12">
                  <div className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h2 className="text-4xl md:text-5xl font-black text-white mb-6 drop-shadow-2xl animate-fade-in-up">
                    {t('waitlist.form.title')}
                  </h2>
                  <p className="text-xl text-blue-200 font-semibold animate-fade-in-up delay-100">
                    {t('waitlist.form.subtitle')}
                  </p>
                </div>
                
                <div className="text-center">
                    <button
                      onClick={() => setIsWaitlistModalOpen(true)}
                      className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl transform transition-all duration-300 border-4 border-white/80 hover:scale-110 hover:-rotate-2 hover:shadow-3xl"
                    >
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      {t('waitlist.form.submitButton')}
                    </button>
                    <p className="text-sm text-blue-200/80 mt-6 font-semibold leading-relaxed">
                      {t('waitlist.form.privacyNote')}
                    </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('waitlist.benefits.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('waitlist.benefits.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Benefit 1 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <Star className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">
                    {t('waitlist.benefits.earlyAccess.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.earlyAccess.description')}
                  </p>
                </div>
                
                {/* Benefit 2 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <Calendar className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">
                    {t('waitlist.benefits.flexible.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.flexible.description')}
                  </p>
                </div>
                
                {/* Benefit 3 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <Users className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">
                    {t('waitlist.benefits.community.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.community.description')}
                  </p>
                </div>
                
                {/* Benefit 4 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <Lightbulb className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-cyan-200 drop-shadow-lg">
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
      </main>

      <Footer />
      <BackToTop />
      
      {/* Waitlist Registration Modal */}
      <TypeformModal
        isOpen={isWaitlistModalOpen}
        onClose={() => setIsWaitlistModalOpen(false)}
        formId="C9yyuMrs"
        title={t('waitlist.form.title')}
        description={t('waitlist.form.subtitle')}
      />
    </div>
  );
}

