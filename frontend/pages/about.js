import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function About() {
  const { t } = useTranslation();

  return (
    <>
      <Head>
        <title>{t('about.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('about.hero.subtitle')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen">
        <Header />
        
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-indigo-900 via-indigo-800 to-purple-800 text-white py-20 pt-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                {t('about.hero.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('about.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* About Content */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              
              {/* Journey Section */}
              <div className="mb-16">
                <h2 className="text-3xl font-bold mb-8 text-gray-800">
                  {t('about.journey.title')}
                </h2>
                <div className="grid md:grid-cols-2 gap-12 items-center">
                  <div>
                    <p className="text-lg text-gray-600 leading-relaxed mb-6">
                      {t('about.journey.description')}
                    </p>
                    <p className="text-lg text-gray-600 leading-relaxed mb-6">
                      With over two decades of experience spanning theater, education, and corporate training, 
                      I've discovered that the most powerful leaders are those who can communicate their vision 
                      with clarity, passion, and authenticity.
                    </p>
                    <p className="text-lg text-gray-600 leading-relaxed">
                      My unique background as a professional actor and director gives me insights into the 
                      psychology of presence, the power of storytelling, and the art of connecting with any audience.
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-64 h-64 mx-auto bg-gray-200 rounded-full overflow-hidden">
                      <img 
                        src="/pictures/PeterStoyanov-straight-look-in-your-eyes.jpg" 
                        alt="Peter Stoyanov"
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                      <div className="w-full h-full bg-indigo-100 hidden items-center justify-center">
                        <span className="text-indigo-600 text-lg font-medium">Peter Stoyanov</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Expertise Section */}
              <div className="mb-16">
                <h2 className="text-3xl font-bold mb-8 text-gray-800">
                  {t('about.expertise.title')}
                </h2>
                <div className="grid md:grid-cols-3 gap-8">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m0 0V1a1 1 0 011-1h2a1 1 0 011 1v18a1 1 0 01-1 1H4a1 1 0 01-1-1V4a1 1 0 011-1h2a1 1 0 011-1V2z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Theater & Performance</h3>
                    <p className="text-gray-600">20+ years on stage teaching presence and authentic expression</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V2a2 2 0 012 2v16a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2V0z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Corporate Training</h3>
                    <p className="text-gray-600">Executive coaching and team development across industries</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Leadership Psychology</h3>
                    <p className="text-gray-600">Deep understanding of influence, motivation, and human dynamics</p>
                  </div>
                </div>
              </div>

              {/* Approach Section */}
              <div className="bg-gray-50 rounded-lg p-8">
                <h2 className="text-3xl font-bold mb-6 text-gray-800">
                  {t('about.approach.title')}
                </h2>
                <div className="grid md:grid-cols-2 gap-8">
                  <div>
                    <h3 className="text-xl font-semibold mb-4 text-indigo-600">Authentic Connection</h3>
                    <p className="text-gray-600 leading-relaxed">
                      I believe that true leadership isn't about putting on a performance—it's about finding 
                      your authentic voice and learning to share it with confidence and clarity.
                    </p>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-4 text-indigo-600">Practical Skills</h3>
                    <p className="text-gray-600 leading-relaxed">
                      Every session focuses on actionable techniques you can implement immediately, 
                      from body language and vocal presence to strategic storytelling.
                    </p>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-4 text-indigo-600">Personalized Growth</h3>
                    <p className="text-gray-600 leading-relaxed">
                      I tailor every program to your specific goals, industry, and communication style, 
                      ensuring maximum relevance and impact.
                    </p>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-4 text-indigo-600">Measurable Results</h3>
                    <p className="text-gray-600 leading-relaxed">
                      Together, we'll track your progress and celebrate measurable improvements in 
                      confidence, influence, and leadership effectiveness.
                    </p>
                  </div>
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