import { useState } from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Waitlist() {
  const { t } = useTranslation('common');
  const router = useRouter();
  
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    cityCountry: '',
    occupation: '',
    whyJoin: '',
    skillsToImprove: ''
  });
  
  const [formErrors, setFormErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.fullName.trim()) {
      errors.fullName = t('waitlist.form.errors.fullNameRequired');
    }
    
    if (!formData.email.trim()) {
      errors.email = t('waitlist.form.errors.emailRequired');
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = t('waitlist.form.errors.emailInvalid');
    }
    
    if (!formData.cityCountry.trim()) {
      errors.cityCountry = t('waitlist.form.errors.cityCountryRequired');
    }
    
    if (!formData.occupation.trim()) {
      errors.occupation = t('waitlist.form.errors.occupationRequired');
    }
    
    if (!formData.whyJoin.trim()) {
      errors.whyJoin = t('waitlist.form.errors.whyJoinRequired');
    }
    
    if (!formData.skillsToImprove.trim()) {
      errors.skillsToImprove = t('waitlist.form.errors.skillsToImproveRequired');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: formData.fullName,
          email: formData.email,
          city_country: formData.cityCountry,
          occupation: formData.occupation,
          why_join: formData.whyJoin,
          skills_to_improve: formData.skillsToImprove
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Redirect to thank you page
        router.push('/thank-you');
      } else {
        // Handle API error
        setFormErrors({
          submit: data.message || t('waitlist.form.errors.submitError')
        });
        setIsSubmitting(false);
      }
    } catch (error) {
      // Handle network error
      setFormErrors({
        submit: t('waitlist.form.errors.networkError')
      });
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('waitlist.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('waitlist.description')} />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative hero-gradient pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-30">
            <div className="absolute top-10 left-10 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
            <div className="absolute bottom-10 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-500"></div>
          </div>
          
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8 text-gray-900 leading-tight">
                <span className="text-gradient-primary">
                  {t('waitlist.title')}
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-12 text-gray-600 max-w-3xl mx-auto leading-relaxed">
                {t('waitlist.description')}
              </p>
              
              {/* Stats & Image */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                <div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center p-4 bg-white bg-opacity-20 rounded-xl">
                      <div className="text-2xl font-bold text-indigo-600 mb-2">{t('waitlist.hero.stats.limited')}</div>
                      <div className="text-gray-600 text-sm">{t('waitlist.hero.stats.spotsAvailable')}</div>
                    </div>
                    <div className="text-center p-4 bg-white bg-opacity-20 rounded-xl">
                      <div className="text-2xl font-bold text-purple-600 mb-2">{t('waitlist.hero.stats.early')}</div>
                      <div className="text-gray-600 text-sm">{t('waitlist.hero.stats.birdPricing')}</div>
                    </div>
                    <div className="text-center p-4 bg-white bg-opacity-20 rounded-xl">
                      <div className="text-2xl font-bold text-pink-600 mb-2">{t('waitlist.hero.stats.exclusive')}</div>
                      <div className="text-gray-600 text-sm">{t('waitlist.hero.stats.access')}</div>
                    </div>
                  </div>
                  <div className="mt-8 p-6 bg-white bg-opacity-10 rounded-xl">
                    <p className="text-lg italic text-gray-700">
                      {t('waitlist.hero.quote')}
                    </p>
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-2xl">
                      <img 
                        src="/pictures/PeterStoyanov-dreaming.jpg" 
                        alt="Petar Stoyanov - Inspiring Vision and Aspirational Coaching"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -top-4 -right-4 w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">✨</div>
                        <div className="text-xs">Your</div>
                        <div className="text-xs">Future</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Understanding Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-gray-50 to-indigo-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  {t('waitlist.understanding.title')}
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  {t('waitlist.understanding.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-xl">
                      <img 
                        src="/pictures/PeterStoyanov-preplexed.jpg" 
                        alt="Petar Stoyanov - Understanding Communication Challenges"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">🤔</div>
                        <div className="text-xs">I Get</div>
                        <div className="text-xs">It</div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-3xl font-bold mb-8 text-gray-900">
                    {t('waitlist.understanding.challenges.title')}
                  </h3>
                  <div className="space-y-6">
                    <div className="flex items-start">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0 mt-1">
                        <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">{t('waitlist.understanding.challenges.fear.title')}</h4>
                        <p className="text-gray-600">{t('waitlist.understanding.challenges.fear.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0 mt-1">
                        <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">Impostor Syndrome</h4>
                        <p className="text-gray-600">Feeling like you don't belong in the room, despite your qualifications and achievements.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0 mt-1">
                        <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">Lack of Executive Presence</h4>
                        <p className="text-gray-600">Struggling to command attention and respect in high-stakes business situations.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-4 flex-shrink-0 mt-1">
                        <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 mb-2">Camera Anxiety</h4>
                        <p className="text-gray-600">Freezing up in video calls, virtual presentations, or when being recorded.</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-8 p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl">
                    <p className="text-lg font-semibold text-gray-900 mb-2">Here's the truth:</p>
                    <p className="text-gray-700">These challenges don't reflect your worth or potential. They're simply skills that can be learned and obstacles that can be overcome with the right approach.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Registration Form Section */}
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              <div className="feature-card bg-white shadow-xl rounded-2xl p-8 md:p-12 border border-gray-100">
                <div className="text-center mb-10">
                  <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h2 className="text-3xl font-bold text-gray-900">
                    Complete Your Registration
                  </h2>
                  <p className="text-gray-600 mt-3">
                    Join our exclusive community of aspiring speakers and performers
                  </p>
                </div>
                
                {formErrors.submit && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                    {formErrors.submit}
                  </div>
                )}
                
                <form onSubmit={handleSubmit}>
                  {/* Full Name */}
                  <div className="mb-6">
                    <label htmlFor="fullName" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.fullName')} *
                    </label>
                    <input
                      type="text"
                      id="fullName"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.fullName ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {formErrors.fullName && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.fullName}</p>
                    )}
                  </div>
                  
                  {/* Email */}
                  <div className="mb-6">
                    <label htmlFor="email" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.email')} *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.email ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {formErrors.email && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>
                    )}
                  </div>
                  
                  {/* City & Country */}
                  <div className="mb-6">
                    <label htmlFor="cityCountry" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.cityCountry')} *
                    </label>
                    <input
                      type="text"
                      id="cityCountry"
                      name="cityCountry"
                      value={formData.cityCountry}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.cityCountry ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {formErrors.cityCountry && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.cityCountry}</p>
                    )}
                  </div>
                  
                  {/* Occupation */}
                  <div className="mb-6">
                    <label htmlFor="occupation" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.occupation')} *
                    </label>
                    <input
                      type="text"
                      id="occupation"
                      name="occupation"
                      value={formData.occupation}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.occupation ? 'border-red-500' : 'border-gray-300'
                      }`}
                    />
                    {formErrors.occupation && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.occupation}</p>
                    )}
                  </div>
                  
                  {/* Why Join */}
                  <div className="mb-6">
                    <label htmlFor="whyJoin" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.whyJoin')} *
                    </label>
                    <textarea
                      id="whyJoin"
                      name="whyJoin"
                      value={formData.whyJoin}
                      onChange={handleChange}
                      rows="4"
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.whyJoin ? 'border-red-500' : 'border-gray-300'
                      }`}
                    ></textarea>
                    {formErrors.whyJoin && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.whyJoin}</p>
                    )}
                  </div>
                  
                  {/* Skills to Improve */}
                  <div className="mb-8">
                    <label htmlFor="skillsToImprove" className="block text-gray-700 font-medium mb-2">
                      {t('waitlist.form.skillsToImprove')} *
                    </label>
                    <textarea
                      id="skillsToImprove"
                      name="skillsToImprove"
                      value={formData.skillsToImprove}
                      onChange={handleChange}
                      rows="4"
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.skillsToImprove ? 'border-red-500' : 'border-gray-300'
                      }`}
                    ></textarea>
                    {formErrors.skillsToImprove && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.skillsToImprove}</p>
                    )}
                  </div>
                  
                  {/* Submit Button */}
                  <div className="text-center">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className={`inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white button-gradient rounded-xl shadow-lg transform transition-all duration-300 ${
                        isSubmitting ? 'opacity-70 cursor-not-allowed' : 'hover:-translate-y-1'
                      }`}
                    >
                      {isSubmitting ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Submitting...
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                          Join Waitlist
                        </>
                      )}
                    </button>
                    <p className="text-sm text-gray-500 mt-4">
                      By joining, you agree to receive updates about our workshops and coaching programs.
                    </p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 md:py-28 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  Why Join Our Community?
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Gain exclusive access to transformative workshops and connect with like-minded individuals
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Benefit 1 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                      <circle cx="12" cy="12" r="2" fill="currentColor" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">
                    Early Access Benefits
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Be the first to know about new workshops, get priority booking, and receive exclusive early-bird pricing discounts.
                  </p>
                </div>
                
                {/* Benefit 2 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <rect x="3" y="4" width="18" height="15" rx="2" strokeWidth={2} />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 2v4M16 2v4" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14h.01M12 14h.01M16 14h.01M8 17h.01M12 17h.01M16 17h.01" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">
                    Flexible Scheduling
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Choose from multiple time slots and formats that fit your lifestyle, including weekend intensives and evening sessions.
                  </p>
                </div>
                
                {/* Benefit 3 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">
                    Community Network
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Connect with other aspiring speakers and performers, share experiences, and build lasting professional relationships.
                  </p>
                </div>
                
                {/* Benefit 4 */}
                <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                  <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2C8.13 2 5 5.13 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.87-3.13-7-7-7z" />
                      <circle cx="12" cy="9" r="2" fill="currentColor" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 20h8" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 22h4" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-900">
                    Personalized Guidance
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    Receive tailored coaching based on your specific goals, whether for business presentations, public speaking, or performance.
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