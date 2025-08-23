import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function TermsOfService() {
  const { t } = useTranslation();

  return (
    <>
      <Head>
        <title>{t('termsOfService.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('termsOfService.description')} />
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
                {t('termsOfService.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('termsOfService.subtitle')}
              </p>
              <p className="text-sm text-indigo-300">
                {t('termsOfService.lastUpdated')}: January 2025
              </p>
            </div>
          </div>
        </section>

        {/* Content */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto prose prose-lg">
              
              {/* Acceptance */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.acceptance.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed">
                  {t('termsOfService.acceptance.content')}
                </p>
              </div>

              {/* Services */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.services.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed">
                  {t('termsOfService.services.content')}
                </p>
              </div>

              {/* User Obligations */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.userObligations.title')}
                </h2>
                <ul className="list-disc pl-6 text-gray-600 space-y-2">
                  <li>{t('termsOfService.userObligations.respectful')}</li>
                  <li>{t('termsOfService.userObligations.accurate')}</li>
                  <li>{t('termsOfService.userObligations.confidential')}</li>
                  <li>{t('termsOfService.userObligations.payment')}</li>
                  <li>{t('termsOfService.userObligations.prohibited')}</li>
                </ul>
              </div>

              {/* Intellectual Property */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.intellectualProperty.title')}
                </h2>
                <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-400">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.intellectualProperty.content')}
                  </p>
                </div>
              </div>

              {/* Limitation of Liability */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.limitation.title')}
                </h2>
                <div className="bg-red-50 p-6 rounded-lg border-l-4 border-red-400">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.limitation.content')}
                  </p>
                </div>
              </div>

              {/* Termination */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.termination.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed">
                  {t('termsOfService.termination.content')}
                </p>
              </div>

              {/* Governing Law */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.governingLaw.title')}
                </h2>
                <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
                  <p className="text-gray-700 leading-relaxed">
                    {t('termsOfService.governingLaw.content')}
                  </p>
                </div>
              </div>

              {/* Contact */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('termsOfService.contact.title')}
                </h2>
                <div className="bg-indigo-50 p-6 rounded-lg">
                  <p className="text-gray-600">
                    {t('termsOfService.contact.content')}
                  </p>
                  <a href="mailto:peterstoyanov83@gmail.com" className="text-indigo-600 hover:text-indigo-800 font-semibold">
                    peterstoyanov83@gmail.com
                  </a>
                </div>
              </div>

            </div>
          </div>
        </section>

        <Footer />
        <BackToTop />
      </div>
    </>
  );
}