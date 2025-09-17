import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useLanguage } from '../contexts/LanguageContext';
import { Gamepad2, User, Mic, Circle, Star, Rocket, Drama, Globe, Brain, Building2, Sparkles } from 'lucide-react';

export default function About() {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('about.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('about.content')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main className="pt-20">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 py-16 md:py-24 lg:py-32">
          <div className="container mx-auto px-4">
            <div className="max-w-7xl mx-auto">
              {/* Main Content Layout */}
              <div className="text-center mb-12 lg:mb-16">
                <h1 className="text-4xl md:text-5xl lg:text-7xl xl:text-8xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('about.hero.title')}
                </h1>
                <div className="text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black mb-8 animate-fade-in-up delay-100">
                  <span className="bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent drop-shadow-lg">
                    {t('about.hero.name')}
                  </span>
                </div>
                <div className="text-xl md:text-2xl lg:text-3xl text-blue-100 mb-12 leading-relaxed font-medium max-w-4xl mx-auto animate-fade-in-up delay-200">
                  {t('about.hero.subtitle')}
                </div>
              </div>

              {/* Optimized Layout - Photo, Content & CTAs */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16">
                {/* Photo - Left Side */}
                <div className="flex justify-center lg:justify-end animate-fade-in-up delay-300">
                  <div className="relative">
                    <div className="w-100 h-100 lg:w-100 lg:h-100 rounded-3xl shadow-2xl overflow-hidden border-4 border-yellow-400 transform hover:scale-105 transition-all duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-straight-look-in-your-eyes.jpg"
                        alt="Peter Stoyanov - Professional Communication Coach and Actor"
                        className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                      />
                    </div>
                    {/* Decorative glow effect */}
                    <div className="absolute -inset-4 bg-gradient-to-r from-yellow-400/20 to-orange-400/20 rounded-3xl blur-2xl -z-10"></div>
                  </div>
                </div>

                {/* Content & CTAs - Right Side */}
                <div className="space-y-8 animate-fade-in-up delay-400">
                  {/* Description */}
                  <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 lg:p-8 border border-white/20 shadow-2xl">
                    <p className="text-lg lg:text-xl text-white/95 leading-relaxed font-medium">
                      {t('about.content')}
                    </p>
                  </div>

                  {/* CTA Buttons - Integrated */}
                  <div className="space-y-4">
                    <div className="flex flex-col sm:flex-row gap-4">
                      <Link href="/waitlist" className="flex-1 inline-flex items-center justify-center px-6 py-3 text-base font-semibold text-slate-900 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 border border-white/30">
                        {t('about.hero.cta.workshop')}
                      </Link>
                      <Link href="/corporate" className="flex-1 inline-flex items-center justify-center px-6 py-3 text-base font-semibold text-white bg-gradient-to-r from-indigo-600 to-blue-600 border border-yellow-400/50 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                        {t('about.hero.cta.corporate')}
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Background & Experience */}
        <section className="py-20 md:py-28 relative overflow-hidden " style={{backgroundImage: 'url(/pictures/maps.png)', backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat'}}>
          {/* Gradient overlay on top of the map image */}
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/50 via-purple-900/50 to-blue-800/80"></div>
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
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-black text-center mb-16 text-white drop-shadow-2xl animate-fade-in-up">
                 {t('about.philosophy.title')}
              </h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="order-2 lg:order-1 animate-fade-in-up">
                  <div className="bg-gradient-to-br from-white via-yellow-50 to-orange-50 p-8 md:p-10 rounded-3xl shadow-2xl border-4 border-yellow-400/50 transform hover:scale-105 transition-all duration-500">
                    <blockquote className="text-2xl md:text-3xl bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent font-black italic leading-relaxed mb-8 drop-shadow-sm">
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
                    <div className="w-full h-full rounded-2xl overflow-hidden shadow-xl border-4 border-yellow-400 transform hover:scale-105 transition-transform duration-500">
                      <img 
                        src="/pictures/transformation.png"
                        alt="Peter Stoyanov - Thoughtful and Contemplative Approach"
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
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 transition-all duration-300">
                    <Gamepad2 className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-yellow-200 drop-shadow-lg">{t('about.approach.playBased.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.playBased.description')}</p>
                </div>

                {/* Body Awareness */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up delay-100">
                  <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 transition-all duration-300">
                    <User className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('about.approach.bodyAwareness.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.bodyAwareness.description')}</p>
                </div>

                {/* Voice & Breath */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up delay-200">
                  <div className="w-20 h-20 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 transition-all duration-300">
                    <Mic className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-yellow-200 drop-shadow-lg">{t('about.approach.voiceBreath.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.voiceBreath.description')}</p>
                </div>

                {/* Mindful Presence */}
                <div className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/8 shadow-2xl transform hover:scale-105 transition-all duration-300 animate-fade-in-up delay-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-indigo-600 to-blue-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl transform hover:scale-110 transition-all duration-300">
                    <Circle className="w-8 h-8 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('about.approach.mindfulPresence.title')}</h3>
                  <p className="text-white/90 leading-relaxed">{t('about.approach.mindfulPresence.description')}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Let's Work Together - Optimized */}
        <section className="py-16 md:py-24 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4">
            <div className="max-w-7xl mx-auto">
              {/* Section Header */}
              <div className="text-center mb-16 animate-fade-in-up">
                <h2 className="text-4xl md:text-5xl lg:text-6xl font-black mb-6 text-white drop-shadow-2xl">
                  {t('about.workTogether.title')}
                </h2>
                <p className="text-xl md:text-2xl text-blue-200 leading-relaxed font-medium max-w-3xl mx-auto">
                  {t('about.workTogether.description')}
                </p>
              </div>

              {/* Main Content Layout */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12 items-stretch">
                {/* Photo Section */}
                <div className="lg:col-span-1 flex justify-center animate-fade-in-up delay-200">
                  <div className="relative">
                    <div className="w-80 h-96 lg:w-full lg:h-full min-h-[480px] rounded-3xl overflow-hidden shadow-2xl border-4 border-yellow-400 transform hover:scale-105 transition-all duration-500">
                      <img 
                        src="/pictures/PeterStoyanov-well-here-we-are.jpg" 
                        alt="Peter Stoyanov - Ready to Welcome and Work Together"
                        className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-indigo-600/20 via-transparent to-yellow-400/5"></div>
                    </div>
                    {/* Decorative glow */}
                    <div className="absolute -inset-4 bg-gradient-to-r from-yellow-400/15 to-orange-400/15 rounded-3xl blur-2xl -z-10"></div>
                  </div>
                </div>
                
                {/* Services Grid */}
                <div className="lg:col-span-2 flex flex-col animate-fade-in-up delay-300">
                  <div className="grid grid-cols-1 gap-6 h-full">
                    {/* Individual Coaching */}
                    <div className="bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-md rounded-2xl p-6 lg:p-8 border border-white/10 shadow-xl hover:shadow-2xl transform hover:scale-102 transition-all duration-300 flex-1">
                      <div className="flex items-start gap-6 h-full">
                        <div className="w-16 h-16 lg:w-18 lg:h-18 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                          <div className="text-2xl lg:text-3xl">👤</div>
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl lg:text-2xl font-black text-yellow-200 mb-3 drop-shadow-lg">
                            {t('about.workTogether.individual.title')}
                          </h3>
                          <p className="text-white/90 leading-relaxed text-base lg:text-lg">
                            {t('about.workTogether.individual.description')}
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    {/* Group Workshops */}
                    <div className="bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-md rounded-2xl p-6 lg:p-8 border border-white/10 shadow-xl hover:shadow-2xl transform hover:scale-102 transition-all duration-300 flex-1">
                      <div className="flex items-start gap-6 h-full">
                        <div className="w-16 h-16 lg:w-18 lg:h-18 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                          <div className="text-2xl lg:text-3xl">👥</div>
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl lg:text-2xl font-black text-blue-200 mb-3 drop-shadow-lg">
                            {t('about.workTogether.group.title')}
                          </h3>
                          <p className="text-white/90 leading-relaxed text-base lg:text-lg">
                            {t('about.workTogether.group.description')}
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    {/* Corporate Training */}
                    <div className="bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-md rounded-2xl p-6 lg:p-8 border border-white/10 shadow-xl hover:shadow-2xl transform hover:scale-102 transition-all duration-300 flex-1">
                      <div className="flex items-start gap-6 h-full">
                        <div className="w-16 h-16 lg:w-18 lg:h-18 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                          <Building2 className="w-7 h-7 lg:w-8 lg:h-8 text-white" strokeWidth={1.5} />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl lg:text-2xl font-black text-yellow-200 mb-3 drop-shadow-lg">
                            {t('about.workTogether.corporate.title')}
                          </h3>
                          <p className="text-white/90 leading-relaxed text-base lg:text-lg">
                            {t('about.workTogether.corporate.description')}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Call to Action */}
              <div className="text-center pt-16 mt-12 animate-fade-in-up delay-400">
                <div className="bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-md rounded-2xl p-8 border border-white/10 shadow-xl max-w-2xl mx-auto">
                  <p className="text-lg text-blue-100 mb-6 font-medium">
                    Ready to transform your communication skills?
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link href="/waitlist" className="px-6 py-3 text-base font-semibold text-slate-900 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 border border-white/30">
                      Join Workshop
                    </Link>
                    <Link href="/corporate" className="px-6 py-3 text-base font-semibold text-white bg-gradient-to-r from-indigo-600 to-blue-600 border border-yellow-400/50 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                      Corporate Training
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Social Links & CTA */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl md:text-6xl font-black mb-8 text-white drop-shadow-2xl animate-fade-in-up">
              {t('about.cta.title')}
            </h2>
            <p className="text-xl md:text-2xl text-blue-200 mb-12 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
              {t('about.cta.description')}
            </p>
            
            {/* Social Links */}
            <div className="flex justify-center space-x-6 mb-12">
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-gradient-to-br from-indigo-500/20 to-blue-600/20 rounded-full flex items-center justify-center text-white hover:from-indigo-400/30 hover:to-blue-500/30 transition-all duration-300 shadow-lg">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
                </svg>
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-gradient-to-br from-yellow-400/20 to-orange-500/20 rounded-full flex items-center justify-center text-white hover:from-yellow-300/30 hover:to-orange-400/30 transition-all duration-300 shadow-lg">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-gradient-to-br from-indigo-600/20 to-blue-700/20 rounded-full flex items-center justify-center text-white hover:from-indigo-500/30 hover:to-blue-600/30 transition-all duration-300 shadow-lg">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center animate-fade-in-up delay-200">
              <Link href="/waitlist" className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-slate-900 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 hover:-rotate-2 transition-all duration-300 border-4 border-white/80">
                {t('about.cta.workshop')}
              </Link>
              <Link href="/corporate" className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-white bg-gradient-to-r from-indigo-600 to-blue-600 border-4 border-yellow-400 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 hover:rotate-2 transition-all duration-300">
                {t('about.cta.corporate')}
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
      <BackToTop />
    </div>
  );
}

