import { useLanguage } from '../contexts/LanguageContext';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import {Shield, Eye, Lock, UserCheck, FileText, Mail} from 'lucide-react';

export default function PrivacyPolicy() {
    const {t} = useLanguage();

    return (
        <div className="min-h-screen bg-white">
            <Head>
                <title>{t('privacyPolicy.title')} | Peter Stoyanov</title>
                <meta name="description" content={t('privacyPolicy.description')}/>
                <link rel="icon" href="/favicons/favicon.ico"/>
            </Head>

            <Header/>

            <main>
                {/* Hero Section */}
                <section
                    className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
                    <div className="absolute inset-0 overflow-hidden">
                        <div
                            className="absolute top-10 left-10 w-72 h-72 bg-blue-300/8 rounded-full blur-xl animate-float"></div>
                        <div
                            className="absolute top-40 right-10 w-72 h-72 bg-purple-300/8 rounded-full blur-xl animate-float-delayed"></div>
                    </div>

                    <div className="container mx-auto px-4 relative z-10">
                        <div className="max-w-4xl mx-auto text-center">
                            <div className="mb-8 animate-fade-in-up">
                                <div
                                    className="w-24 h-24 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center mx-auto shadow-2xl">
                                    <Shield className="w-12 h-12 text-white" strokeWidth={2}/>
                                </div>
                            </div>

                            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span
                    className="bg-gradient-to-r from-blue-300 via-teal-300 to-indigo-300 bg-clip-text text-transparent">
                  {t('privacyPolicy.title')}
                </span>
                            </h1>

                            <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                                {t('privacyPolicy.subtitle')}
                            </p>
                        </div>
                    </div>
                </section>

                {/* Content Section */}
                <section className="py-20 md:py-28 bg-white">
                    <div className="container mx-auto px-4">
                        <div className="max-w-4xl mx-auto">

                            {/* Last Updated */}
                            <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6 mb-12">
                                <p className="text-blue-800 font-semibold">
                                    <strong>{t('privacyPolicy.lastUpdated')}:</strong> {new Date().toLocaleDateString('bg-BG')}
                                </p>
                            </div>

                            {/* Introduction */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                                    <FileText className="w-8 h-8 mr-3 text-blue-600" strokeWidth={2}/>
                                    {t('privacyPolicy.introduction.title')}
                                </h2>
                                <div className="prose prose-lg max-w-none">
                                    <p className="text-gray-700 leading-relaxed mb-4">
                                        {t('privacyPolicy.introduction.content1')}
                                    </p>
                                    <p className="text-gray-700 leading-relaxed">
                                        {t('privacyPolicy.introduction.content2')}
                                    </p>
                                </div>
                            </div>

                            {/* Data Controller */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                                    <UserCheck className="w-8 h-8 mr-3 text-blue-600" strokeWidth={2}/>
                                    {t('privacyPolicy.dataController.title')}
                                </h2>
                                <div className="bg-gray-50 rounded-2xl p-6">
                                    <p className="text-gray-700 leading-relaxed mb-4">
                                        <strong>{t('privacyPolicy.dataController.name')}:</strong> Петър Стоянов (Peter
                                        Stoyanov)
                                    </p>
                                    <p className="text-gray-700 leading-relaxed mb-4">
                                        <strong>{t('privacyPolicy.dataController.address')}:</strong> София, България
                                    </p>
                                    <p className="text-gray-700 leading-relaxed">
                                        <strong>{t('privacyPolicy.dataController.email')}:</strong>
                                        <a href="mailto:peterstoyanov83@gmail.com"
                                           className="text-blue-600 hover:text-blue-700 ml-2">
                                            peterstoyanov83@gmail.com
                                        </a>
                                    </p>
                                </div>
                            </div>

                            {/* Data Collection */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                                    <Eye className="w-8 h-8 mr-3 text-blue-600" strokeWidth={2}/>
                                    {t('privacyPolicy.dataCollection.title')}
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="bg-blue-50 rounded-2xl p-6">
                                        <h3 className="text-xl font-black mb-4 text-blue-900">{t('privacyPolicy.dataCollection.personal.title')}</h3>
                                        <ul className="space-y-2 text-gray-700">
                                            <li>• {t('privacyPolicy.dataCollection.personal.name')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.personal.email')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.personal.phone')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.personal.company')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.personal.location')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.personal.occupation')}</li>
                                        </ul>
                                    </div>
                                    <div className="bg-green-50 rounded-2xl p-6">
                                        <h3 className="text-xl font-black mb-4 text-green-900">{t('privacyPolicy.dataCollection.technical.title')}</h3>
                                        <ul className="space-y-2 text-gray-700">
                                            <li>• {t('privacyPolicy.dataCollection.technical.ip')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.technical.browser')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.technical.device')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.technical.usage')}</li>
                                            <li>• {t('privacyPolicy.dataCollection.technical.cookies')}</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            {/* Legal Basis */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                                    <Lock className="w-8 h-8 mr-3 text-blue-600" strokeWidth={2}/>
                                    {t('privacyPolicy.legalBasis.title')}
                                </h2>
                                <div className="space-y-6">
                                    <div className="border-l-4 border-blue-500 pl-6">
                                        <h3 className="text-xl font-black mb-2 text-gray-900">{t('privacyPolicy.legalBasis.consent.title')}</h3>
                                        <p className="text-gray-700 leading-relaxed">{t('privacyPolicy.legalBasis.consent.description')}</p>
                                    </div>
                                    <div className="border-l-4 border-green-500 pl-6">
                                        <h3 className="text-xl font-black mb-2 text-gray-900">{t('privacyPolicy.legalBasis.contract.title')}</h3>
                                        <p className="text-gray-700 leading-relaxed">{t('privacyPolicy.legalBasis.contract.description')}</p>
                                    </div>
                                    <div className="border-l-4 border-purple-500 pl-6">
                                        <h3 className="text-xl font-black mb-2 text-gray-900">{t('privacyPolicy.legalBasis.legitimate.title')}</h3>
                                        <p className="text-gray-700 leading-relaxed">{t('privacyPolicy.legalBasis.legitimate.description')}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Data Usage */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900">
                                    {t('privacyPolicy.dataUsage.title')}
                                </h2>
                                <div className="bg-gray-50 rounded-2xl p-6">
                                    <ul className="space-y-3 text-gray-700">
                                        <li className="flex items-start">
                                            <span
                                                className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                            {t('privacyPolicy.dataUsage.communication')}
                                        </li>
                                        <li className="flex items-start">
                                            <span
                                                className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                            {t('privacyPolicy.dataUsage.services')}
                                        </li>
                                        <li className="flex items-start">
                                            <span
                                                className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                            {t('privacyPolicy.dataUsage.marketing')}
                                        </li>
                                        <li className="flex items-start">
                                            <span
                                                className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                            {t('privacyPolicy.dataUsage.analytics')}
                                        </li>
                                        <li className="flex items-start">
                                            <span
                                                className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                            {t('privacyPolicy.dataUsage.legal')}
                                        </li>
                                    </ul>
                                </div>
                            </div>

                            {/* Your Rights */}
                            <div className="mb-12">
                                <h2 className="text-3xl font-black mb-6 text-gray-900">
                                    {t('privacyPolicy.rights.title')}
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-4">
                                        <div className="bg-blue-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-blue-900">{t('privacyPolicy.rights.access.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.access.description')}</p>
                                        </div>
                                        <div className="bg-green-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-green-900">{t('privacyPolicy.rights.rectification.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.rectification.description')}</p>
                                        </div>
                                        <div className="bg-purple-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-purple-900">{t('privacyPolicy.rights.erasure.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.erasure.description')}</p>
                                        </div>
                                    </div>
                                    <div className="space-y-4">
                                        <div className="bg-orange-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-orange-900">{t('privacyPolicy.rights.portability.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.portability.description')}</p>
                                        </div>
                                        <div className="bg-red-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-red-900">{t('privacyPolicy.rights.objection.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.objection.description')}</p>
                                        </div>
                                        <div className="bg-indigo-50 rounded-xl p-4">
                                            <h3 className="text-lg font-black mb-2 text-indigo-900">{t('privacyPolicy.rights.complaint.title')}</h3>
                                            <p className="text-sm text-gray-700">{t('privacyPolicy.rights.complaint.description')}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Contact Information */}
                            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white">
                                <h2 className="text-3xl font-black mb-6 flex items-center">
                                    <Mail className="w-8 h-8 mr-3" strokeWidth={2}/>
                                    {t('privacyPolicy.contact.title')}
                                </h2>
                                <p className="text-blue-100 mb-4 leading-relaxed">
                                    {t('privacyPolicy.contact.description')}
                                </p>
                                <div className="bg-white/10 rounded-xl p-4">
                                    <p className="mb-2">
                                        <strong>{t('privacyPolicy.contact.email')}:</strong>
                                        <a href="mailto:peterstoyanov83@gmail.com"
                                           className="text-blue-200 hover:text-white ml-2">
                                            peterstoyanov83@gmail.com
                                        </a>
                                    </p>
                                    <p>
                                        <strong>{t('privacyPolicy.contact.response')}:</strong> {t('privacyPolicy.contact.responseTime')}
                                    </p>
                                </div>
                            </div>

                        </div>
                    </div>
                </section>
            </main>

            <Footer/>
        </div>
    );
}

