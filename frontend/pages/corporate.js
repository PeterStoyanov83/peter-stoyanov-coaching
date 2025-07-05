import { useState } from 'react';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Corporate() {
  const { t } = useTranslation('common');
  const router = useRouter();
  const [formData, setFormData] = useState({
    companyName: '',
    contactPerson: '',
    email: '',
    phone: '',
    teamSize: '',
    trainingGoals: '',
    preferredDates: '',
    budget: '',
    additionalInfo: ''
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
    
    if (!formData.companyName.trim()) {
      errors.companyName = t('corporate.form.errors.companyNameRequired');
    }
    
    if (!formData.contactPerson.trim()) {
      errors.contactPerson = t('corporate.form.errors.contactPersonRequired');
    }
    
    if (!formData.email.trim()) {
      errors.email = t('corporate.form.errors.emailRequired');
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = t('corporate.form.errors.emailInvalid');
    }
    
    if (!formData.teamSize.trim()) {
      errors.teamSize = t('corporate.form.errors.teamSizeRequired');
    }
    
    if (!formData.trainingGoals.trim()) {
      errors.trainingGoals = t('corporate.form.errors.trainingGoalsRequired');
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
      const response = await fetch('/api/corporate-inquiry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Redirect to thank you page
        router.push('/thank-you?type=corporate');
      } else {
        // Handle API error
        setFormErrors({
          submit: data.message || t('corporate.form.errors.submitError')
        });
        setIsSubmitting(false);
      }
    } catch (error) {
      // Handle network error
      setFormErrors({
        submit: t('corporate.form.errors.networkError')
      });
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>{t('corporate.title')} | Petar Stoyanov</title>
        <meta name="description" content={t('corporate.description')} />
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
            <div className="max-w-5xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8 text-gray-900 leading-tight">
                <span className="text-gradient-primary">
                  Corporate Training
                </span>
                <br />
                <span className="text-gray-800">
                  That Transforms Teams
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-12 text-gray-600 max-w-4xl mx-auto leading-relaxed">
                Elevate your team's communication, leadership presence, and collaboration skills through 
                proven theater techniques and interactive workshops designed for business professionals.
              </p>
              
              {/* Stats & Image */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                <div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center p-6 bg-white bg-opacity-20 rounded-2xl">
                      <div className="text-3xl font-bold text-indigo-600 mb-2">50+</div>
                      <div className="text-gray-600">Companies Trained</div>
                    </div>
                    <div className="text-center p-6 bg-white bg-opacity-20 rounded-2xl">
                      <div className="text-3xl font-bold text-purple-600 mb-2">95%</div>
                      <div className="text-gray-600">Satisfaction Rate</div>
                    </div>
                    <div className="text-center p-6 bg-white bg-opacity-20 rounded-2xl">
                      <div className="text-3xl font-bold text-pink-600 mb-2">1000+</div>
                      <div className="text-gray-600">Professionals Trained</div>
                    </div>
                  </div>
                  <blockquote className="text-lg italic text-gray-700 mt-8 p-6 bg-white bg-opacity-10 rounded-xl">
                    "Theater techniques don't just improve communication—they transform how teams connect, collaborate, and lead with authentic confidence."
                  </blockquote>
                </div>
                
                <div className="text-center">
                  <div className="relative inline-block">
                    <div className="w-80 h-96 rounded-2xl overflow-hidden shadow-2xl">
                      <img 
                        src="/pictures/PeterStoyanov-powerful-2.jpg" 
                        alt="Petar Stoyanov - Executive Presence and Leadership Training"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="absolute -bottom-4 -right-4 w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-xl">
                      <div className="text-center">
                        <div className="text-2xl">💼</div>
                        <div className="text-xs text-gray-600">Business</div>
                        <div className="text-xs text-gray-600">Leader</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-20">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                Training Programs
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Customized workshops that address your team's specific communication and leadership challenges
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {/* Service 1 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="3" y="4" width="18" height="12" rx="2" strokeWidth={2} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 21l4-7 4 7" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18h12" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8l3 2 2-3 3 2" />
                    <circle cx="8" cy="9" r="1" fill="currentColor" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Presentation Excellence</h3>
                <p className="text-gray-600 leading-relaxed">Master the art of compelling presentations using voice, body language, and storytelling techniques that captivate audiences.</p>
              </div>

              {/* Service 2 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100-4m0 4v2m0-6V4" />
                    <circle cx="12" cy="8" r="3" strokeWidth={2} />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14h8l2 6H6l2-6z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 12h4" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Leadership Presence</h3>
                <p className="text-gray-600 leading-relaxed">Develop commanding presence and authentic leadership communication that inspires teams and drives results.</p>
              </div>

              {/* Service 3 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Team Communication</h3>
                <p className="text-gray-600 leading-relaxed">Enhance collaboration, active listening, and conflict resolution through interactive theater-based exercises.</p>
              </div>

              {/* Service 4 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Camera Confidence</h3>
                <p className="text-gray-600 leading-relaxed">Excel in video meetings, interviews, and digital presentations with professional on-camera presence and delivery.</p>
              </div>

              {/* Service 5 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Improvisation Skills</h3>
                <p className="text-gray-600 leading-relaxed">Build quick thinking, adaptability, and creative problem-solving skills for dynamic business situations.</p>
              </div>

              {/* Service 6 */}
              <div className="feature-card bg-white p-8 rounded-2xl shadow-lg">
                <div className="feature-icon w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Stress Management</h3>
                <p className="text-gray-600 leading-relaxed">Learn breathing techniques and mindfulness practices to maintain composure and clarity under pressure.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Inquiry Form Section */}
        <section className="py-20 md:py-28 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                  Request a Custom Training Proposal
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Let's discuss how theater-based training can transform your team's communication and performance
                </p>
              </div>
              
              <div className="feature-card bg-white shadow-xl rounded-2xl p-8 md:p-12 border border-gray-100">
                <div className="text-center mb-10">
                  <div className="w-16 h-16 button-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900">
                    Get Your Free Consultation
                  </h3>
                  <p className="text-gray-600 mt-3">
                    Tell us about your team's goals and we'll create a customized training program
                  </p>
                </div>
                
                {formErrors.submit && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                    {formErrors.submit}
                  </div>
                )}
                
                <form onSubmit={handleSubmit}>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    {/* Company Name */}
                    <div>
                      <label htmlFor="companyName" className="block text-gray-700 font-medium mb-2">
                        Company Name *
                      </label>
                      <input
                        type="text"
                        id="companyName"
                        name="companyName"
                        value={formData.companyName}
                        onChange={handleChange}
                        className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                          formErrors.companyName ? 'border-red-500' : 'border-gray-300'
                        }`}
                      />
                      {formErrors.companyName && (
                        <p className="mt-1 text-sm text-red-600">{formErrors.companyName}</p>
                      )}
                    </div>
                    
                    {/* Contact Person */}
                    <div>
                      <label htmlFor="contactPerson" className="block text-gray-700 font-medium mb-2">
                        Contact Person *
                      </label>
                      <input
                        type="text"
                        id="contactPerson"
                        name="contactPerson"
                        value={formData.contactPerson}
                        onChange={handleChange}
                        className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                          formErrors.contactPerson ? 'border-red-500' : 'border-gray-300'
                        }`}
                      />
                      {formErrors.contactPerson && (
                        <p className="mt-1 text-sm text-red-600">{formErrors.contactPerson}</p>
                      )}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    {/* Email */}
                    <div>
                      <label htmlFor="email" className="block text-gray-700 font-medium mb-2">
                        Email Address *
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
                    
                    {/* Phone */}
                    <div>
                      <label htmlFor="phone" className="block text-gray-700 font-medium mb-2">
                        Phone Number
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    {/* Team Size */}
                    <div>
                      <label htmlFor="teamSize" className="block text-gray-700 font-medium mb-2">
                        Team Size *
                      </label>
                      <select
                        id="teamSize"
                        name="teamSize"
                        value={formData.teamSize}
                        onChange={handleChange}
                        className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                          formErrors.teamSize ? 'border-red-500' : 'border-gray-300'
                        }`}
                      >
                        <option value="">Select team size</option>
                        <option value="5-15">5-15 people</option>
                        <option value="16-30">16-30 people</option>
                        <option value="31-50">31-50 people</option>
                        <option value="51-100">51-100 people</option>
                        <option value="100+">100+ people</option>
                      </select>
                      {formErrors.teamSize && (
                        <p className="mt-1 text-sm text-red-600">{formErrors.teamSize}</p>
                      )}
                    </div>
                    
                    {/* Budget */}
                    <div>
                      <label htmlFor="budget" className="block text-gray-700 font-medium mb-2">
                        Estimated Budget
                      </label>
                      <select
                        id="budget"
                        name="budget"
                        value={formData.budget}
                        onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value="">Select budget range</option>
                        <option value="under-5k">Under €5,000</option>
                        <option value="5k-10k">€5,000 - €10,000</option>
                        <option value="10k-20k">€10,000 - €20,000</option>
                        <option value="20k+">€20,000+</option>
                        <option value="discuss">Let's discuss</option>
                      </select>
                    </div>
                  </div>
                  
                  {/* Training Goals */}
                  <div className="mb-6">
                    <label htmlFor="trainingGoals" className="block text-gray-700 font-medium mb-2">
                      Training Goals & Challenges *
                    </label>
                    <textarea
                      id="trainingGoals"
                      name="trainingGoals"
                      value={formData.trainingGoals}
                      onChange={handleChange}
                      rows="4"
                      placeholder="What communication challenges does your team face? What outcomes are you hoping to achieve?"
                      className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                        formErrors.trainingGoals ? 'border-red-500' : 'border-gray-300'
                      }`}
                    ></textarea>
                    {formErrors.trainingGoals && (
                      <p className="mt-1 text-sm text-red-600">{formErrors.trainingGoals}</p>
                    )}
                  </div>
                  
                  {/* Preferred Dates */}
                  <div className="mb-6">
                    <label htmlFor="preferredDates" className="block text-gray-700 font-medium mb-2">
                      Preferred Training Dates
                    </label>
                    <input
                      type="text"
                      id="preferredDates"
                      name="preferredDates"
                      value={formData.preferredDates}
                      onChange={handleChange}
                      placeholder="e.g., March 2024, flexible, ASAP"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                  
                  {/* Additional Info */}
                  <div className="mb-8">
                    <label htmlFor="additionalInfo" className="block text-gray-700 font-medium mb-2">
                      Additional Information
                    </label>
                    <textarea
                      id="additionalInfo"
                      name="additionalInfo"
                      value={formData.additionalInfo}
                      onChange={handleChange}
                      rows="3"
                      placeholder="Any specific requirements, team dynamics, or additional context we should know about?"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    ></textarea>
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
                          Sending Request...
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                          </svg>
                          Request Free Consultation
                        </>
                      )}
                    </button>
                    <p className="text-sm text-gray-500 mt-4">
                      We'll respond within 24 hours with a customized training proposal
                    </p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 md:py-28 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">
                Why Choose Theater-Based Training?
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Proven techniques from the world of performance that create lasting behavioral change
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {/* Benefit 1 */}
              <div className="text-center">
                <div className="w-20 h-20 button-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Experiential Learning</h3>
                <p className="text-gray-600 leading-relaxed">
                  Learn by doing through interactive exercises that create muscle memory for confident communication.
                </p>
              </div>
              
              {/* Benefit 2 */}
              <div className="text-center">
                <div className="w-20 h-20 button-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Immediate Results</h3>
                <p className="text-gray-600 leading-relaxed">
                  See transformation in real-time as participants break through limiting beliefs and discover their authentic presence.
                </p>
              </div>
              
              {/* Benefit 3 */}
              <div className="text-center">
                <div className="w-20 h-20 button-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900">Team Bonding</h3>
                <p className="text-gray-600 leading-relaxed">
                  Build trust and collaboration as teams work together in a safe, supportive, and energizing environment.
                </p>
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