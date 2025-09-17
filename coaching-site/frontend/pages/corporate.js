import {useState} from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import TypeformModal from '../components/TypeformModal';
import { useLanguage } from '../contexts/LanguageContext';
import {
    Presentation,
    Crown,
    Users,
    Video,
    Zap,
    Heart,
    Building2,
    Mail,
    GraduationCap,
    Lightbulb,
    Handshake
} from 'lucide-react';

export default function Corporate() {
    const {t} = useLanguage();
    const [isCorporateModalOpen, setIsCorporateModalOpen] = useState(false);


    return (
        <div className="min-h-screen bg-white">
            <Head>
                <title>{t('corporate.title')} | Peter Stoyanov</title>
                <meta name="description" content={t('corporate.description')}/>
                <link rel="icon" href="/favicons/favicon.ico"/>
            </Head>

            <Header/>

            <main>
                {/* Hero Section */}
                <section
                    className="relative pt-24 pb-20 md:pt-32 md:pb-32 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
                    <div className="container mx-auto px-4">
                        <div className="max-w-5xl mx-auto text-center">
                            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span
                    className="bg-gradient-to-r from-blue-300 via-teal-300 to-indigo-300 bg-clip-text text-transparent">
                  {t('corporate.hero.title')}
                </span>
                                <br/>
                                <span className="text-blue-200 drop-shadow-lg">
                  {t('corporate.hero.subtitle')}
                </span>
                            </h1>
                            <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-4xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                                {t('corporate.hero.description')}
                            </p>

                            {/* Stats & Image */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                                <div>
                                    <blockquote
                                        className="text-xl italic text-white mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl font-semibold leading-relaxed animate-fade-in-up delay-300">
                                        "{t('corporate.hero.quote')}"
                                    </blockquote>
                                </div>

                                <div className="text-center">
                                    <div className="relative inline-block">
                                        <div
                                            className="h-90 w-80 rounded-3xl overflow-hidden shadow-2xl border-8 border-white">
                                            <img
                                                src="/pictures/PeterStoyanov-straight-look-in-your-eyes.jpg"
                                                alt="Peter Stoyanov - Executive Presence and Leadership Training"
                                                className="w-full h-full object-cover"
                                            />
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Services Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
                    <div className="container mx-auto px-4">
                        <div className="text-center mb-20 relative z-10">
                            <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                {t('corporate.services.title')}
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                {t('corporate.services.subtitle')}
                            </p>
                        </div>

                        <div
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto relative z-10">
                            {/* Service 1 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Presentation className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.services.presentation.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.presentation.description')}</p>
                            </div>

                            {/* Service 2 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Crown className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('corporate.services.leadership.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.leadership.description')}</p>
                            </div>

                            {/* Service 3 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Users className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">{t('corporate.services.communication.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.communication.description')}</p>
                            </div>

                            {/* Service 4 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Video className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.services.camera.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.camera.description')}</p>
                            </div>

                            {/* Service 5 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-400">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-red-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Zap className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-red-200 drop-shadow-lg">{t('corporate.services.improvisation.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.improvisation.description')}</p>
                            </div>

                            {/* Service 6 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-500">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Heart className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-cyan-200 drop-shadow-lg">{t('corporate.services.stress.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.stress.description')}</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Inquiry Form Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
                    <div className="container mx-auto px-4">
                        <div className="max-w-4xl mx-auto">
                            <div className="text-center mb-16 relative z-10">
                                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                    {t('corporate.form.title')}
                                </h2>
                                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                    {t('corporate.form.subtitle')}
                                </p>
                            </div>

                            <div
                                className="bg-white/10 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12 border border-white/20 relative z-10 animate-fade-in-up delay-200">
                                <div className="text-center mb-10">
                                    <h3 className="text-3xl font-black text-blue-200 drop-shadow-lg">
                                        {t('corporate.form.consultationTitle')}
                                    </h3>
                                    <p className="text-white/90 mt-3 font-semibold">
                                        {t('corporate.form.consultationSubtitle')}
                                    </p>
                                </div>

                                <div className="text-center">
                                    <button
                                        onClick={() => setIsCorporateModalOpen(true)}
                                        className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl transform transition-all duration-300 border-4 border-white/80 hover:-translate-y-2 hover:scale-105 hover:shadow-3xl hover:rotate-2"
                                    >
                                        <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                                        </svg>
                                        {t('corporate.form.submitButton')}
                                    </button>
                                    <p className="text-sm text-blue-200/80 mt-4 font-semibold">
                                        {t('corporate.form.responseNote')}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Benefits Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
                    <div className="container mx-auto px-4">
                        <div className="text-center mb-16 relative z-10">
                            <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                {t('corporate.benefits.title')}
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                {t('corporate.benefits.subtitle')}
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto relative z-10">
                            {/* Benefit 1 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <GraduationCap className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.benefits.experiential.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.experiential.description')}
                                </p>
                            </div>

                            {/* Benefit 2 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Lightbulb className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">{t('corporate.benefits.immediate.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.immediate.description')}
                                </p>
                            </div>

                            {/* Benefit 3 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Handshake className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('corporate.benefits.teamBonding.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.teamBonding.description')}
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            <Footer/>
            <BackToTop/>
            
            {/* Corporate Inquiry Modal */}
            <TypeformModal
                isOpen={isCorporateModalOpen}
                onClose={() => setIsCorporateModalOpen(false)}
                formId="YRsIpOvV"
                title={t('corporate.form.title')}
                description={t('corporate.form.subtitle')}
            />
        </div>
    );
}

