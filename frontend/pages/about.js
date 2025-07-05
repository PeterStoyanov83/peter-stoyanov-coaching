import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import Link from 'next/link';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function About() {
  const { t } = useTranslation('common');

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('about.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('about.content')} />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="pt-20">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-20 md:py-28">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                {/* Content */}
                <div className="order-2 lg:order-1">
                  <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-8 text-gray-900">
                    Meet <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Petar Stoyanov</span>
                  </h1>
                  <div className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
                    Actor • Clown • Coach • Director
                  </div>
                  <p className="text-lg text-gray-700 mb-8 leading-relaxed">
                    {t('about.content')}
                  </p>
                  
                  {/* Quick Stats */}
                  <div className="grid grid-cols-2 gap-6 mb-8">
                    <div className="text-center p-4 bg-white rounded-xl shadow-md">
                      <div className="text-3xl font-bold text-indigo-600 mb-2">20+</div>
                      <div className="text-gray-600 text-sm">Years Experience</div>
                    </div>
                    <div className="text-center p-4 bg-white rounded-xl shadow-md">
                      <div className="text-3xl font-bold text-purple-600 mb-2">15+</div>
                      <div className="text-gray-600 text-sm">Countries</div>
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-4">
                    <Link href="/waitlist" className="inline-flex items-center justify-center px-6 py-3 text-lg font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300">
                      Join a Workshop
                    </Link>
                    <Link href="/corporate" className="inline-flex items-center justify-center px-6 py-3 text-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-600 rounded-xl shadow-lg hover:shadow-xl hover:bg-indigo-50 transform hover:-translate-y-1 transition-all duration-300">
                      Corporate Training
                    </Link>
                  </div>
                </div>

                {/* Photo */}
                <div className="order-1 lg:order-2">
                  <div className="relative">
                    <div className="w-full h-96 lg:h-[500px] rounded-2xl shadow-2xl overflow-hidden">
                      <img 
                        src="/pictures/PeterStoyanov-straight-look-black-and-white.jpg" 
                        alt="Petar Stoyanov - Professional Communication Coach and Actor"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    
                    {/* Decorative elements */}
                    <div className="absolute -top-4 -right-4 w-24 h-24 bg-yellow-300 rounded-full opacity-30 animate-pulse"></div>
                    <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-pink-300 rounded-full opacity-40 animate-pulse delay-1000"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Background & Experience */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
                My Journey
              </h2>
              
              <div className="space-y-12">
                {/* Theater & Performance */}
                <div className="flex flex-col md:flex-row gap-8 items-start">
                  <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-pink-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m0 0V1a1 1 0 011-1h2a1 1 0 011 1v2m0 0v14a2 2 0 01-2 2H5a2 2 0 01-2-2V4m4 0V2a1 1 0 011-1h4a1 1 0 011 1v2M9 12l2 2 4-4" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-gray-900">Theater & Clowning</h3>
                    <p className="text-gray-700 leading-relaxed">
                      My journey began on the stage, where I discovered the transformative power of performance. 
                      Through years of theater and clowning, I learned that authenticity and vulnerability are 
                      the keys to genuine connection with an audience.
                    </p>
                  </div>
                </div>

                {/* International Work */}
                <div className="flex flex-col md:flex-row gap-8 items-start">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-gray-900">International Experience</h3>
                    <p className="text-gray-700 leading-relaxed">
                      Over two decades, I've worked across 15+ countries, collaborating with diverse audiences 
                      and understanding how communication transcends cultural boundaries. This global perspective 
                      shapes my unique approach to coaching.
                    </p>
                  </div>
                </div>

                {/* Coaching Method */}
                <div className="flex flex-col md:flex-row gap-8 items-start">
                  <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-teal-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold mb-4 text-gray-900">Unique Methodology</h3>
                    <p className="text-gray-700 leading-relaxed">
                      My coaching combines theater techniques, voice work, breathing exercises, and mindfulness. 
                      Unlike traditional public speaking training, I focus on discovering your authentic voice 
                      and presence through play and exploration.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Philosophy */}
        <section className="py-20 md:py-28 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
                My Philosophy
              </h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="order-2 lg:order-1">
                  <div className="bg-white p-8 md:p-10 rounded-2xl shadow-xl">
                    <blockquote className="text-2xl md:text-3xl text-gray-700 italic leading-relaxed mb-8">
                      "Every person has a unique voice and presence. My role is not to change who you are, 
                      but to help you discover and amplify your authentic self."
                    </blockquote>
                    <p className="text-lg text-gray-600 leading-relaxed mb-6">
                      I believe that confidence comes from authenticity, not from pretending to be someone else. 
                      Through my workshops, you'll learn to embrace your natural communication style while 
                      developing the skills to express yourself powerfully and clearly.
                    </p>
                    <p className="text-lg text-gray-600 leading-relaxed">
                      My approach combines theater techniques with practical business applications, 
                      creating a safe space where vulnerability becomes strength and fear transforms into confidence.
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
                    <div className="absolute -bottom-4 -right-4 w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">💭</div>
                        <div className="text-xs">Deep</div>
                        <div className="text-xs">Work</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Approach */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
                My Approach
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {/* Play-based Learning */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12c0 1.657 1.343 3 3 3s3-1.343 3-3-1.343-3-3-3-3 1.343-3 3z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9l1.5 1.5M15 9l-1.5 1.5M9 15l1.5-1.5M15 15l-1.5-1.5" />
                      <circle cx="9" cy="9" r="1" fill="currentColor" />
                      <circle cx="15" cy="9" r="1" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Play-Based Learning</h3>
                  <p className="text-gray-600">Learning through joy and exploration, not fear and pressure.</p>
                </div>

                {/* Body Awareness */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-teal-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      <circle cx="12" cy="8" r="3" strokeWidth={2} />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14v7" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17h6" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Body Awareness</h3>
                  <p className="text-gray-600">Understanding how your body communicates and using it as a tool.</p>
                </div>

                {/* Voice & Breath */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 1C8 1 5 4 5 8c0 2.5 1 4.5 2.5 6 1 1 2.5 1.5 4.5 1.5s3.5-.5 4.5-1.5C17.5 12.5 19 10.5 19 8c0-4-3-7-7-7z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 18c0-2 2-4 4-4s4 2 4 4" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 21c0-3 3-6 6-6s6 3 6 6" />
                      <circle cx="12" cy="8" r="2" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Voice & Breath</h3>
                  <p className="text-gray-600">Developing vocal power and breathing techniques for confidence.</p>
                </div>

                {/* Mindful Presence */}
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <circle cx="12" cy="12" r="3" strokeWidth={2} />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 1v6M12 17v6M4.22 4.22l4.24 4.24M15.54 15.54l4.24 4.24M1 12h6M17 12h6M4.22 19.78l4.24-4.24M15.54 8.46l4.24-4.24" />
                      <circle cx="12" cy="12" r="1" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-4 text-gray-900">Mindful Presence</h3>
                  <p className="text-gray-600">Being fully present and authentic in every interaction.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Let's Work Together */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl">
                      <img 
                        src="/pictures/PeterStoyanov-well-here-we-are.jpg" 
                        alt="Petar Stoyanov - Ready to Welcome and Work Together"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -top-4 -left-4 w-24 h-24 bg-gradient-to-br from-green-500 to-teal-600 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">🤝</div>
                        <div className="text-xs">Let's</div>
                        <div className="text-xs">Begin</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h2 className="text-4xl md:text-5xl font-bold mb-8 text-gray-900">
                    Let's Work Together
                  </h2>
                  <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                    Whether you're looking to overcome speaking anxiety, enhance your leadership presence, 
                    or transform your team's communication skills, I'm here to guide you on that journey.
                  </p>
                  <div className="space-y-6">
                    <div className="flex items-start">
                      <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                        <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Individual Coaching</h3>
                        <p className="text-gray-600">Personalized sessions focused on your specific communication goals and challenges.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                        <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Group Workshops</h3>
                        <p className="text-gray-600">Dynamic group sessions where participants learn together and support each other's growth.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start">
                      <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                        <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Corporate Training</h3>
                        <p className="text-gray-600">Customized programs designed to enhance your team's communication and leadership skills.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Social Links & CTA */}
        <section className="py-20 md:py-28 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-8 text-white">
              Ready to Transform Your Communication?
            </h2>
            <p className="text-xl text-indigo-100 mb-12 max-w-3xl mx-auto">
              Join hundreds of students who have discovered their authentic voice and confident presence.
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
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/waitlist" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-indigo-600 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300">
                Join a Workshop
              </Link>
              <Link href="/corporate" className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white border-2 border-white rounded-xl hover:bg-white hover:text-indigo-600 transform hover:-translate-y-1 transition-all duration-300">
                Corporate Training
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