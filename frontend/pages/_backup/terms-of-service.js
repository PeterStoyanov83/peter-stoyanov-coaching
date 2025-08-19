import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Scale, FileText, Users, Copyright, AlertTriangle, XCircle, Gavel, Mail } from 'lucide-react';

export default function TermsOfService() {
  const { t } = useTranslation('common');

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('termsOfService.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('termsOfService.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-10 left-10 w-72 h-72 bg-blue-300/8 rounded-full blur-xl animate-float"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-purple-300/8 rounded-full blur-xl animate-float-delayed"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto text-center">
              <div className="mb-8 animate-fade-in-up">
                <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-indigo-500 rounded-full flex items-center justify-center mx-auto shadow-2xl">
                  <Scale className="w-12 h-12 text-white" strokeWidth={2} />
                </div>
              </div>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span className="bg-gradient-to-r from-purple-300 via-indigo-300 to-blue-300 bg-clip-text text-transparent">
                  {t('termsOfService.title')}
                </span>
              </h1>
              
              <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                {t('termsOfService.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Content Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              
              {/* Last Updated */}
              <div className="bg-purple-50 border border-purple-200 rounded-2xl p-6 mb-12">
                <p className="text-purple-800 font-semibold">
                  <strong>{t('termsOfService.lastUpdated')}:</strong> {new Date().toLocaleDateString('bg-BG')}
                </p>
              </div>

              {/* Acceptance of Terms */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <FileText className="w-8 h-8 mr-3 text-purple-600" strokeWidth={2} />
                  {t('termsOfService.acceptance.title')}
                </h2>
                <div className="prose prose-lg max-w-none">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.acceptance.content')}
                  </p>
                </div>
              </div>

              {/* Description of Services */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <Users className="w-8 h-8 mr-3 text-purple-600" strokeWidth={2} />
                  {t('termsOfService.services.title')}
                </h2>
                <div className="bg-gray-50 rounded-2xl p-6">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.services.content')}
                  </p>
                </div>
              </div>

              {/* User Obligations */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <Users className="w-8 h-8 mr-3 text-purple-600" strokeWidth={2} />
                  {t('termsOfService.userObligations.title')}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="bg-blue-50 rounded-xl p-4">
                      <div className="flex items-start">
                        <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <p className="text-gray-700">{t('termsOfService.userObligations.respectful')}</p>
                      </div>
                    </div>
                    <div className="bg-green-50 rounded-xl p-4">
                      <div className="flex items-start">
                        <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <p className="text-gray-700">{t('termsOfService.userObligations.accurate')}</p>
                      </div>
                    </div>
                    <div className="bg-purple-50 rounded-xl p-4">
                      <div className="flex items-start">
                        <span className="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <p className="text-gray-700">{t('termsOfService.userObligations.confidential')}</p>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="bg-yellow-50 rounded-xl p-4">
                      <div className="flex items-start">
                        <span className="w-2 h-2 bg-yellow-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <p className="text-gray-700">{t('termsOfService.userObligations.payment')}</p>
                      </div>
                    </div>
                    <div className="bg-red-50 rounded-xl p-4">
                      <div className="flex items-start">
                        <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <p className="text-gray-700">{t('termsOfService.userObligations.prohibited')}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Intellectual Property */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <Copyright className="w-8 h-8 mr-3 text-purple-600" strokeWidth={2} />
                  {t('termsOfService.intellectualProperty.title')}
                </h2>
                <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-200">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.intellectualProperty.content')}
                  </p>
                </div>
              </div>

              {/* Limitation of Liability */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <AlertTriangle className="w-8 h-8 mr-3 text-orange-600" strokeWidth={2} />
                  {t('termsOfService.limitation.title')}
                </h2>
                <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.limitation.content')}
                  </p>
                </div>
              </div>

              {/* Termination */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <XCircle className="w-8 h-8 mr-3 text-red-600" strokeWidth={2} />
                  {t('termsOfService.termination.title')}
                </h2>
                <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.termination.content')}
                  </p>
                </div>
              </div>

              {/* Governing Law */}
              <div className="mb-12">
                <h2 className="text-3xl font-black mb-6 text-gray-900 flex items-center">
                  <Gavel className="w-8 h-8 mr-3 text-blue-600" strokeWidth={2} />
                  {t('termsOfService.governingLaw.title')}
                </h2>
                <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.governingLaw.content')}
                  </p>
                </div>
              </div>

              {/* Contact Information */}
              <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-8 text-white">
                <h2 className="text-3xl font-black mb-6 flex items-center">
                  <Mail className="w-8 h-8 mr-3" strokeWidth={2} />
                  {t('termsOfService.contact.title')}
                </h2>
                <div className="bg-white/10 rounded-xl p-4">
                  <p className="text-purple-100 leading-relaxed">
                    {t('termsOfService.contact.content')}
                  </p>
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