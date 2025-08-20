import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function Corporate() {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    companyName: '',
    contactPerson: '',
    email: '',
    phone: '',
    trainingGoals: '',
    additionalInfo: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage('');

    try {
      const response = await fetch('/api/corporate-inquiry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        setSubmitMessage('✅ Thank you! We\'ll get back to you within 24 hours.');
        setFormData({
          companyName: '',
          contactPerson: '',
          email: '',
          phone: '',
          trainingGoals: '',
          additionalInfo: ''
        });
      } else {
        setSubmitMessage('❌ Something went wrong. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setSubmitMessage('❌ Something went wrong. Please try again.');
    }

    setIsSubmitting(false);
  };

  return (
    <>
      <Head>
        <title>{t('corporate.title')} - Peter Stoyanov</title>
        <meta name="description" content={t('corporate.hero.subtitle')} />
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
                {t('corporate.hero.title')}
              </h1>
              <p className="text-xl md:text-2xl text-indigo-200 mb-8">
                {t('corporate.hero.subtitle')}
              </p>
            </div>
          </div>
        </section>

        {/* Programs Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-center mb-16 text-gray-800">
              {t('corporate.programs.title')}
            </h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Leadership Presence</h3>
                <p className="text-gray-600 leading-relaxed">
                  Develop executive presence, confident communication, and authentic leadership style 
                  that inspires and motivates teams.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Team Communication</h3>
                <p className="text-gray-600 leading-relaxed">
                  Improve collaboration, reduce conflicts, and create a culture of open, 
                  effective communication across all levels.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Presentation Skills</h3>
                <p className="text-gray-600 leading-relaxed">
                  Master the art of compelling presentations, from structure and storytelling 
                  to delivery and audience engagement.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Change Management</h3>
                <p className="text-gray-600 leading-relaxed">
                  Navigate organizational change with clear communication strategies that 
                  build trust and reduce resistance.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Conflict Resolution</h3>
                <p className="text-gray-600 leading-relaxed">
                  Transform workplace conflicts into opportunities for growth through 
                  effective communication and mediation techniques.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition duration-300">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-gray-800">Executive Coaching</h3>
                <p className="text-gray-600 leading-relaxed">
                  One-on-one coaching for C-level executives to enhance their leadership 
                  communication and strategic influence.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Form Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold mb-6 text-gray-800">
                  {t('corporate.contact.title')}
                </h2>
                <p className="text-xl text-gray-600">
                  {t('corporate.contact.description')}
                </p>
              </div>

              <div className="bg-white rounded-lg shadow-md p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-2">
                        Company Name *
                      </label>
                      <input
                        type="text"
                        id="companyName"
                        name="companyName"
                        value={formData.companyName}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label htmlFor="contactPerson" className="block text-sm font-medium text-gray-700 mb-2">
                        Contact Person *
                      </label>
                      <input
                        type="text"
                        id="contactPerson"
                        name="contactPerson"
                        value={formData.contactPerson}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                        Phone Number
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor="trainingGoals" className="block text-sm font-medium text-gray-700 mb-2">
                      Training Goals & Objectives *
                    </label>
                    <textarea
                      id="trainingGoals"
                      name="trainingGoals"
                      value={formData.trainingGoals}
                      onChange={handleChange}
                      required
                      rows={4}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Tell us about your team's communication challenges and what you hope to achieve..."
                    />
                  </div>

                  <div>
                    <label htmlFor="additionalInfo" className="block text-sm font-medium text-gray-700 mb-2">
                      Additional Information
                    </label>
                    <textarea
                      id="additionalInfo"
                      name="additionalInfo"
                      value={formData.additionalInfo}
                      onChange={handleChange}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Team size, preferred dates, budget considerations, etc."
                    />
                  </div>

                  <div className="text-center">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-8 rounded-lg transition duration-300 disabled:opacity-50"
                    >
                      {isSubmitting ? 'Sending...' : 'Request Consultation'}
                    </button>
                  </div>

                  {submitMessage && (
                    <div className="text-center mt-4">
                      <p className="text-sm">{submitMessage}</p>
                    </div>
                  )}
                </form>
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