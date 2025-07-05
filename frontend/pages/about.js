import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Gamepad2, User, Mic, Circle, Star, Rocket, Drama, Globe, Brain, Building2, Sparkles } from 'lucide-react';

export default function About() {
  const { t } = useTranslation('common');

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('about.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('about.content')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main className="pt-20">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 py-20 md:py-28 overflow-hidden">

          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                {/* Content */}
                <div className="order-2 lg:order-1">
                  <h1 className="text-4xl md:text-5xl lg:text-6xl font-black mb-8 text-white drop-shadow-lg animate-fade-in-up">
                    {t('about.hero.title')} <span className="bg-gradient-to-r from-yellow-300 to-green-300 bg-clip-text text-transparent animate-pulse">{t('about.hero.name')}</span>
                  </h1>
                  <div className="text-xl md:text-2xl text-blue-100 mb-8 leading-relaxed font-semibold animate-fade-in-up delay-100">
                    {t('about.hero.subtitle')}
                  </div>
                  <p className="text-lg text-white/90 mb-8 leading-relaxed bg-black/8 p-6 rounded-2xl backdrop-blur-sm animate-fade-in-up delay-200">
                    {t('about.content')}
                  </p>
                  
                  {/* Quick Stats */}
                  <div className="grid grid-cols-2 gap-6 mb-8 animate-fade-in-up delay-300">
                    <div className="text-center p-6 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-2xl shadow-2xl transform hover:scale-105 transition-all duration-300 hover:rotate-1">
                      <div className="text-4xl font-black text-white mb-2 drop-shadow-lg">20+</div>
                      <div className="text-white/90 text-sm font-semibold">{t('about.hero.stats.experience')}</div>
                    </div>
                    <div className="text-center p-6 bg-gradient-to-br from-rose-400 to-pink-500 rounded-2xl shadow-2xl transform hover:scale-105 transition-all duration-300 hover:-rotate-1">
                      <div className="text-4xl font-black text-white mb-2 drop-shadow-lg">15+</div>
                      <div className="text-white/90 text-sm font-semibold">{t('about.hero.stats.countries')}</div>
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-4 animate-fade-in-up delay-400">
                    <Link href="/waitlist" className="inline-flex items-center justify-center px-8 py-4 text-lg font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-300 to-yellow-500 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 hover:-rotate-1 transition-all duration-300 border-4 border-white/50">
                      {t('about.hero.cta.workshop')}
                    </Link>
                    <Link href="/corporate" className="inline-flex items-center justify-center px-8 py-4 text-lg font-black text-white bg-gradient-to-r from-green-500 to-emerald-600 border-4 border-yellow-300 rounded-2xl shadow-2xl hover:shadow-3xl hover:bg-gradient-to-r hover:from-emerald-600 hover:to-green-500 transform hover:scale-110 hover:rotate-1 transition-all duration-300">
                      {t('about.hero.cta.corporate')}
                    </Link>
                  </div>
                </div>

                {/* Photo */}
                <div className="order-1 lg:order-2 ">
                  <div className="relative">
                    <div className="w-full h-96 lg:h-[500px] rounded-3xl shadow-2xl overflow-hidden border-8 border-gradient-to-r from-yellow-400 to-pink-400 transform hover:scale-105 transition-all duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-straight-look-black-and-white.jpg" 
                        alt="Petar Stoyanov - Professional Communication Coach and Actor"
                        className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Background & Experience */}
        <section className="py-20 md:py-28 relative overflow-hidden" style={{backgroundImage: 'url(/maps.png)', backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat'}}>
          {/* Gradient overlay on top of the map image */}
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/50 via-purple-900/50 to-pink-900/60"></div>
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/8 via-purple-600/8 to-pink-600/8"></div>
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-black text-center mb-16 bg-gradient-to-r from-yellow-400/60 via-orange-400 to-pink-400 bg-clip-text text-transparent drop-shadow-lg">
                {t('about.journey.title')}
              </h2>
              
              <div className="space-y-12">
                {/* Theater & Performance */}
                <div className="flex flex-col md:flex-row gap-8 items-start group animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-br from-red-500 via-pink-500 to-rose-600 rounded-3xl flex items-center justify-center flex-shrink-0 shadow-2xl transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                    <Drama className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <div className="bg-white/30 backdrop-blur-md  rounded-2xl p-6 border border-white/8 shadow-2xl">
                    <h3 className="text-3xl font-black mb-4 text-yellow-300 drop-shadow-lg"> {t('about.journey.theater.title')}</h3>
                    <p className="text-white/90 leading-relaxed text-lg">
                      {t('about.journey.theater.description')}
                    </p>
                  </div>
                </div>

                {/* International Work */}
                <div className="flex flex-col md:flex-row gap-8 items-start group animate-fade-in-up delay-100">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-500 via-cyan-500 to-teal-600 rounded-3xl flex items-center justify-center flex-shrink-0 shadow-2xl transform group-hover:scale-110 group-hover:-rotate-12 transition-all duration-500">
                    <Globe className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/8 shadow-2xl">
                    <h3 className="text-3xl font-black mb-4 text-cyan-300 drop-shadow-lg"> {t('about.journey.international.title')}</h3>
                    <p className="text-white/90 leading-relaxed text-lg">
                      {t('about.journey.international.description')}
                    </p>
                  </div>
                </div>

                {/* Coaching Method */}
                <div className="flex flex-col md:flex-row gap-8 items-start group animate-fade-in-up delay-200">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-500 via-emerald-500 to-teal-600 rounded-3xl flex items-center justify-center flex-shrink-0 shadow-2xl transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                    <Brain className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-6 border border-white/8 shadow-2xl">
                    <h3 className="text-3xl font-black mb-4 text-green-300 drop-shadow-lg">{t('about.journey.methodology.title')}</h3>
                    <p className="text-white/90 leading-relaxed text-lg">
                      {t('about.journey.methodology.description')}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Philosophy */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">
          <div className="absolute inset-0">
            <div className="absolute top-1/3 left-1/3 w-72 h-72 bg-yellow-300/8 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-1/3 right-1/3 w-96 h-96 bg-purple-300/8 rounded-full blur-3xl animate-float-delayed"></div>
          </div>
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-black text-center mb-16 text-white drop-shadow-2xl animate-fade-in-up">
                 {t('about.philosophy.title')}
              </h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="order-2 lg:order-1 animate-fade-in-up">
                  <div className="bg-gradient-to-br from-white via-yellow-50 to-orange-50 p-8 md:p-10 rounded-3xl shadow-2xl border-4 border-yellow-300/50 transform hover:scale-105 transition-all duration-500">
                    <blockquote className="text-2xl md:text-3xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent font-black italic leading-relaxed mb-8 drop-shadow-sm">
                      "{t('about.philosophy.quote')}"
                    </blockquote>
                    <p className="text-lg text-gray-800 leading-relaxed mb-6 font-semibold">
                      {t('about.philosophy.belief')}
                    </p>
                    <p className="text-lg text-gray-700 leading-relaxed">
                      {t('about.philosophy.approach')}
                    </p>
                  </div>
                </div>
                
                <div className="order-1 lg:order-2 text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl transform hover:scale-105 transition-transform duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-thinking.jpg" 
                        alt="Petar Stoyanov - Thoughtful and Contemplative Approach"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Approach */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">

          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-black text-center mb-16 text-white drop-shadow-2xl animate-fade-in-up">
                {t('about.approach.title')}
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {/* Play-based Learning */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <Gamepad2 className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('about.approach.playBased.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.playBased.description')}</p>
                </div>

                {/* Body Awareness */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <User className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-green-200 drop-shadow-lg">{t('about.approach.bodyAwareness.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.bodyAwareness.description')}</p>
                </div>

                {/* Voice & Breath */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <Mic className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('about.approach.voiceBreath.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.voiceBreath.description')}</p>
                </div>

                {/* Mindful Presence */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <Circle className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('about.approach.mindfulPresence.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.mindfulPresence.description')}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Let's Work Together */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 relative overflow-hidden">
          {/* Floating Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-1/4 right-1/4 w-80 h-80 bg-gradient-to-br from-yellow-300/8 to-orange-400/8 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-green-300/8 to-teal-400/8 rounded-full blur-3xl animate-float-delayed"></div>
            <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-gradient-to-br from-cyan-300/8 to-blue-400/8 rounded-full blur-3xl animate-float-slow"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center animate-fade-in-up">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-3xl overflow-hidden shadow-2xl border-8 border-gradient-to-r from-yellow-400 to-pink-400 transform hover:scale-105 transition-all duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-well-here-we-are.jpg" 
                        alt="Petar Stoyanov - Ready to Welcome and Work Together"
                        className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-purple-600/30 via-transparent to-yellow-400/8"></div>
                    </div>

                  </div>
                </div>
                
                <div className="animate-fade-in-up delay-100">
                  <h2 className="text-4xl md:text-5xl font-black mb-8 text-white drop-shadow-2xl">
                    {t('about.workTogether.title')}
                  </h2>
                  <p className="text-xl text-blue-200 mb-8 leading-relaxed font-semibold">
                    {t('about.workTogether.description')}
                  </p>
                  <div className="space-y-6">
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/8 shadow-xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center mr-6 flex-shrink-0 shadow-lg">
                        <div className="text-2xl"> 👤 </div>
                      </div>
                      <div>
                        <h3 className="text-xl font-black text-blue-200 mb-3 drop-shadow-lg">{t('about.workTogether.individual.title')}</h3>
                        <p className="text-white/90 leading-relaxed">{t('about.workTogether.individual.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/8 shadow-xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300">
                      <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center mr-6 flex-shrink-0 shadow-lg">
                        <div className="text-2xl">👥</div>
                      </div>
                      <div>
                        <h3 className="text-xl font-black text-purple-200 mb-3 drop-shadow-lg">{t('about.workTogether.group.title')}</h3>
                        <p className="text-white/90 leading-relaxed">{t('about.workTogether.group.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/8 shadow-xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center mr-6 flex-shrink-0 shadow-lg">
                        <Building2 className="w-6 h-6 text-white" strokeWidth={1.5} />
                      </div>
                      <div>
                        <h3 className="text-xl font-black text-green-200 mb-3 drop-shadow-lg">{t('about.workTogether.corporate.title')}</h3>
                        <p className="text-white/90 leading-relaxed">{t('about.workTogether.corporate.description')}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Social Links & CTA */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 relative overflow-hidden">
          <div className="absolute inset-0">
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-yellow-400/8 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-cyan-400/8 rounded-full blur-3xl animate-float-delayed"></div>
            <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-green-400/8 rounded-full blur-3xl animate-float-slow"></div>
          </div>
          <div className="container mx-auto px-4 text-center relative z-10">
            <h2 className="text-4xl md:text-6xl font-black mb-8 text-white drop-shadow-2xl animate-fade-in-up">
              {t('about.cta.title')}
            </h2>
            <p className="text-xl md:text-2xl text-blue-200 mb-12 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
              {t('about.cta.description')}
            </p>
            
            {/* Social Links */}
            <div className="flex justify-center space-x-6 mb-12">
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white hover:bg-opacity-30 transition-all duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
                </svg>
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white hover:bg-opacity-30 transition-all duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white hover:bg-opacity-30 transition-all duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center animate-fade-in-up delay-200">
              <Link href="/waitlist" className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 hover:-rotate-2 transition-all duration-300 border-4 border-white/80">
                {t('about.cta.workshop')}
              </Link>
              <Link href="/corporate" className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-white bg-gradient-to-r from-green-500 to-emerald-600 border-4 border-yellow-400 rounded-2xl shadow-2xl hover:shadow-3xl hover:bg-gradient-to-r hover:from-emerald-600 hover:to-green-500 transform hover:scale-110 hover:rotate-2 transition-all duration-300">
                {t('about.cta.corporate')}
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