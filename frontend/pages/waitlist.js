import { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useTranslation } from '../hooks/useTranslation';

export default function Waitlist() {
  const { t } = useTranslation();
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
    
    // Clear error when the user starts typing
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
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://peter-stoyanov-backend.onrender.com';
      const response = await fetch(`${apiUrl}/api/register`, {
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
      } else if (response.status === 422) {
        // Handle validation errors from Pydantic
        const validationErrors = {};
        
        if (data.detail && Array.isArray(data.detail)) {
          data.detail.forEach(error => {
            const field = error.loc[error.loc.length - 1]; // Get the field name
            if (field === 'email' && error.type === 'value_error.email') {
              validationErrors.email = t('waitlist.form.errors.emailInvalid');
            } else if (field === 'full_name') {
              validationErrors.fullName = t('waitlist.form.errors.fullNameRequired');
            } else if (field === 'city_country') {
              validationErrors.cityCountry = t('waitlist.form.errors.cityCountryRequired');
            } else if (field === 'occupation') {
              validationErrors.occupation = t('waitlist.form.errors.occupationRequired');
            } else if (field === 'why_join') {
              validationErrors.whyJoin = t('waitlist.form.errors.whyJoinRequired');
            } else if (field === 'skills_to_improve') {
              validationErrors.skillsToImprove = t('waitlist.form.errors.skillsToImproveRequired');
            } else {
              // Generic validation error
              validationErrors.submit = error.msg || t('waitlist.form.errors.submitError');
            }
          });
        } else {
          validationErrors.submit = t('waitlist.form.errors.submitError');
        }
        
        setFormErrors(validationErrors);
        setIsSubmitting(false);
      } else {
        // Handle other API errors
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
        <title>{t('waitlist.title')} | Peter Stoyanov</title>
        <meta name="description" content={t('waitlist.description')} />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 pt-24 pb-20 md:pt-32 md:pb-32">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span className="bg-gradient-to-r from-blue-300 via-teal-300 to-indigo-300 bg-clip-text text-transparent">
                  {t('waitlist.title')}
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                {t('waitlist.description')}
              </p>
              
              {/* Stats & Image */}
              <div className="flex flex-col items-center mt-20">
                <div className="w-full max-w-6xl">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 justify-items-center animate-fade-in-up delay-200">
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-yellow-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.limited')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.spotsAvailable')}</div>
                    </div>
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-green-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.early')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.birdPricing')}</div>
                    </div>
                    <div className="text-center p-6 py-8 min-w-[200px] bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                      <div className="text-lg md:text-xl font-black text-orange-300 mb-3 drop-shadow-lg leading-tight break-words">{t('waitlist.hero.stats.exclusive')}</div>
                      <div className="text-white/90 text-xs md:text-sm font-semibold leading-relaxed">{t('waitlist.hero.stats.access')}</div>
                    </div>
                  </div>
                  <div className="col-span-full mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl animate-fade-in-up delay-300">
                    <p className="text-xl italic text-white font-semibold leading-relaxed text-center">
                      "{t('waitlist.hero.quote')}"
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Understanding Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('waitlist.understanding.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('waitlist.understanding.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-100 h-100 rounded-2xl overflow-hidden shadow-xl">
                      <img
                        src="/pictures/PeterStoyanov-preplexed.jpg"
                        alt="Peter Stoyanov - Understanding Communication Challenges"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-3xl font-black mb-8 text-white drop-shadow-lg">
                    {t('waitlist.understanding.challenges.title')}
                  </h3>
                  <div className="space-y-6">
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up">
                      <div className="w-12 h-12 bg-gradient-to-br from-red-400 to-pink-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                          <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.fear.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.fear.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-100">
                      <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.impostor.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.impostor.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-200">
                      <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.presence.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.presence.description')}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-xl animate-fade-in-up delay-300">
                      <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0 shadow-lg">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <div>
                        <h4 className="text-xl font-black text-white mb-3 drop-shadow-lg">{t('waitlist.understanding.challenges.camera.title')}</h4>
                        <p className="text-white/90 leading-relaxed">{t('waitlist.understanding.challenges.camera.description')}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl animate-fade-in-up delay-400">
                    <p className="text-xl font-black text-white mb-4 drop-shadow-lg">{t('waitlist.understanding.truth.title')}</p>
                    <p className="text-white/90 leading-relaxed font-semibold">{t('waitlist.understanding.truth.description')}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

          {/* Registration Form Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="bg-white/10 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12 border border-white/20">
                <div className="text-center mb-12">
                  <div className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h2 className="text-4xl md:text-5xl font-black text-white mb-6 drop-shadow-2xl animate-fade-in-up">
                    {t('waitlist.form.title')}
                  </h2>
                  <p className="text-xl text-blue-200 font-semibold animate-fade-in-up delay-100">
                    {t('waitlist.form.subtitle')}
                  </p>
                </div>
                
                {formErrors.submit && (
                  <div className="bg-red-500/20 border border-red-400/50 text-red-200 px-6 py-4 rounded-2xl mb-8 backdrop-blur-sm">
                    {formErrors.submit}
                  </div>
                )}
                
                <form onSubmit={handleSubmit}>
                  {/* Full Name */}
                  <div className="mb-6">
                    <label htmlFor="fullName" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.fullName')} *
                    </label>
                    <input
                      type="text"
                      id="fullName"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                        formErrors.fullName ? 'border-red-400' : ''
                      }`}
                    />
                    {formErrors.fullName && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.fullName}</p>
                    )}
                  </div>
                  
                  {/* Email */}
                  <div className="mb-6">
                    <label htmlFor="email" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.email')} *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                        formErrors.email ? 'border-red-400' : ''
                      }`}
                    />
                    {formErrors.email && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.email}</p>
                    )}
                  </div>
                  
                  {/* City & Country */}
                  <div className="mb-6">
                    <label htmlFor="cityCountry" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.cityCountry')} *
                    </label>
                    <input
                      type="text"
                      id="cityCountry"
                      name="cityCountry"
                      value={formData.cityCountry}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                        formErrors.cityCountry ? 'border-red-400' : ''
                      }`}
                    />
                    {formErrors.cityCountry && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.cityCountry}</p>
                    )}
                  </div>
                  
                  {/* Occupation */}
                  <div className="mb-6">
                    <label htmlFor="occupation" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.occupation')} *
                    </label>
                    <input
                      type="text"
                      id="occupation"
                      name="occupation"
                      value={formData.occupation}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                        formErrors.occupation ? 'border-red-400' : ''
                      }`}
                    />
                    {formErrors.occupation && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.occupation}</p>
                    )}
                  </div>
                  
                  {/* Why Join */}
                  <div className="mb-6">
                    <label htmlFor="whyJoin" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.whyJoin')} *
                    </label>
                    <textarea
                      id="whyJoin"
                      name="whyJoin"
                      value={formData.whyJoin}
                      onChange={handleChange}
                      rows="4"
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 resize-none ${
                        formErrors.whyJoin ? 'border-red-400' : ''
                      }`}
                    ></textarea>
                    {formErrors.whyJoin && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.whyJoin}</p>
                    )}
                  </div>
                  
                  {/* Skills to Improve */}
                  <div className="mb-8">
                    <label htmlFor="skillsToImprove" className="block text-blue-200 font-semibold mb-3">
                      {t('waitlist.form.skillsToImprove')} *
                    </label>
                    <textarea
                      id="skillsToImprove"
                      name="skillsToImprove"
                      value={formData.skillsToImprove}
                      onChange={handleChange}
                      rows="4"
                      className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 resize-none ${
                        formErrors.skillsToImprove ? 'border-red-400' : ''
                      }`}
                    ></textarea>
                    {formErrors.skillsToImprove && (
                      <p className="mt-2 text-sm text-red-300">{formErrors.skillsToImprove}</p>
                    )}
                  </div>
                  
                  {/* Submit Button */}
                  <div className="text-center">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className={`inline-flex items-center justify-center px-10 py-5 text-xl font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl transform transition-all duration-300 border-4 border-white/80 ${
                        isSubmitting ? 'opacity-70 cursor-not-allowed' : 'hover:scale-110 hover:-rotate-2 hover:shadow-3xl'
                      }`}
                    >
                      {isSubmitting ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          {t('waitlist.form.submitting')}
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                          {t('waitlist.form.submitButton')}
                        </>
                      )}
                    </button>
                    <p className="text-sm text-blue-200/80 mt-6 font-semibold leading-relaxed">
                      {t('waitlist.form.privacyNote')}
                    </p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                  {t('waitlist.benefits.title')}
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                  {t('waitlist.benefits.subtitle')}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Benefit 1 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                  <div className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">
                    {t('waitlist.benefits.earlyAccess.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.earlyAccess.description')}
                  </p>
                </div>
                
                {/* Benefit 2 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3a2 2 0 012-2h4a2 2 0 012 2v4m-6 0V6a2 2 0 012-2h2a2 2 0 012 2v1M8 7h8m-8 0a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V9a2 2 0 00-2-2m0 0V6a2 2 0 00-2-2H8a2 2 0 00-2 2v3" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">
                    {t('waitlist.benefits.flexible.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.flexible.description')}
                  </p>
                </div>
                
                {/* Benefit 3 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m3 5.197v1M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">
                    {t('waitlist.benefits.community.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.community.description')}
                  </p>
                </div>
                
                {/* Benefit 4 */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                  <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-cyan-200 drop-shadow-lg">
                    {t('waitlist.benefits.personalized.title')}
                  </h3>
                  <p className="text-white/90 leading-relaxed">
                    {t('waitlist.benefits.personalized.description')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
      <BackToTop />
    </div>
  );
}

