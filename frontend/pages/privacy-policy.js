import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function PrivacyPolicy() {
  const { t } = useTranslation();

  return (
    <>
      <Head>
        <title>{t('privacyPolicy.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('privacyPolicy.description')} />
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
                {t('privacyPolicy.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('privacyPolicy.subtitle')}
              </p>
              <p className="text-sm text-indigo-300">
                {t('privacyPolicy.lastUpdated')}: January 2025
              </p>
            </div>
          </div>
        </section>

        {/* Content */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto prose prose-lg">
              
              {/* Introduction */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.introduction.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed mb-4">
                  {t('privacyPolicy.introduction.content1')}
                </p>
                <p className="text-gray-600 leading-relaxed">
                  {t('privacyPolicy.introduction.content2')}
                </p>
              </div>

              {/* Data Controller */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.dataController.title')}
                </h2>
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-gray-600 mb-2">
                    <strong>{t('privacyPolicy.dataController.name')}:</strong> Peter Stoyanov
                  </p>
                  <p className="text-gray-600 mb-2">
                    <strong>{t('privacyPolicy.dataController.address')}:</strong> Sofia, Bulgaria
                  </p>
                  <p className="text-gray-600">
                    <strong>{t('privacyPolicy.dataController.email')}:</strong> peterstoyanov83@gmail.com
                  </p>
                </div>
              </div>

              {/* Data Collection */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.dataCollection.title')}
                </h2>
                
                <h3 className="text-2xl font-semibold mb-4 text-gray-700">
                  {t('privacyPolicy.dataCollection.personal.title')}
                </h3>
                <ul className="list-disc pl-6 text-gray-600 mb-6">
                  <li>{t('privacyPolicy.dataCollection.personal.name')}</li>
                  <li>{t('privacyPolicy.dataCollection.personal.email')}</li>
                  <li>{t('privacyPolicy.dataCollection.personal.phone')}</li>
                  <li>{t('privacyPolicy.dataCollection.personal.company')}</li>
                  <li>{t('privacyPolicy.dataCollection.personal.location')}</li>
                  <li>{t('privacyPolicy.dataCollection.personal.occupation')}</li>
                </ul>

                <h3 className="text-2xl font-semibold mb-4 text-gray-700">
                  {t('privacyPolicy.dataCollection.technical.title')}
                </h3>
                <ul className="list-disc pl-6 text-gray-600">
                  <li>{t('privacyPolicy.dataCollection.technical.ip')}</li>
                  <li>{t('privacyPolicy.dataCollection.technical.browser')}</li>
                  <li>{t('privacyPolicy.dataCollection.technical.device')}</li>
                  <li>{t('privacyPolicy.dataCollection.technical.usage')}</li>
                  <li>{t('privacyPolicy.dataCollection.technical.cookies')}</li>
                </ul>
              </div>

              {/* Legal Basis */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.legalBasis.title')}
                </h2>
                
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3 text-gray-700">
                    {t('privacyPolicy.legalBasis.consent.title')}
                  </h3>
                  <p className="text-gray-600">
                    {t('privacyPolicy.legalBasis.consent.description')}
                  </p>
                </div>

                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3 text-gray-700">
                    {t('privacyPolicy.legalBasis.contract.title')}
                  </h3>
                  <p className="text-gray-600">
                    {t('privacyPolicy.legalBasis.contract.description')}
                  </p>
                </div>

                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3 text-gray-700">
                    {t('privacyPolicy.legalBasis.legitimate.title')}
                  </h3>
                  <p className="text-gray-600">
                    {t('privacyPolicy.legalBasis.legitimate.description')}
                  </p>
                </div>
              </div>

              {/* Data Usage */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.dataUsage.title')}
                </h2>
                <ul className="list-disc pl-6 text-gray-600">
                  <li>{t('privacyPolicy.dataUsage.communication')}</li>
                  <li>{t('privacyPolicy.dataUsage.services')}</li>
                  <li>{t('privacyPolicy.dataUsage.marketing')}</li>
                  <li>{t('privacyPolicy.dataUsage.analytics')}</li>
                  <li>{t('privacyPolicy.dataUsage.legal')}</li>
                </ul>
              </div>

              {/* Rights */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.rights.title')}
                </h2>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-blue-800">
                      {t('privacyPolicy.rights.access.title')}
                    </h3>
                    <p className="text-blue-700 text-sm">
                      {t('privacyPolicy.rights.access.description')}
                    </p>
                  </div>

                  <div className="bg-green-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-green-800">
                      {t('privacyPolicy.rights.rectification.title')}
                    </h3>
                    <p className="text-green-700 text-sm">
                      {t('privacyPolicy.rights.rectification.description')}
                    </p>
                  </div>

                  <div className="bg-red-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-red-800">
                      {t('privacyPolicy.rights.erasure.title')}
                    </h3>
                    <p className="text-red-700 text-sm">
                      {t('privacyPolicy.rights.erasure.description')}
                    </p>
                  </div>

                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-purple-800">
                      {t('privacyPolicy.rights.portability.title')}
                    </h3>
                    <p className="text-purple-700 text-sm">
                      {t('privacyPolicy.rights.portability.description')}
                    </p>
                  </div>

                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-yellow-800">
                      {t('privacyPolicy.rights.objection.title')}
                    </h3>
                    <p className="text-yellow-700 text-sm">
                      {t('privacyPolicy.rights.objection.description')}
                    </p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-2 text-gray-800">
                      {t('privacyPolicy.rights.complaint.title')}
                    </h3>
                    <p className="text-gray-700 text-sm">
                      {t('privacyPolicy.rights.complaint.description')}
                    </p>
                  </div>
                </div>
              </div>

              {/* Contact */}
              <div className="mb-12">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('privacyPolicy.contact.title')}
                </h2>
                <p className="text-gray-600 mb-4">
                  {t('privacyPolicy.contact.description')}
                </p>
                <div className="bg-indigo-50 p-6 rounded-lg">
                  <p className="text-indigo-800 mb-2">
                    <strong>{t('privacyPolicy.contact.email')}:</strong> peterstoyanov83@gmail.com
                  </p>
                  <p className="text-indigo-800">
                    <strong>{t('privacyPolicy.contact.response')}:</strong> {t('privacyPolicy.contact.responseTime')}
                  </p>
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