import {useState} from 'react';
import {useTranslation} from 'next-i18next';
import {serverSideTranslations} from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import {useRouter} from 'next/router';
import Header from '../components/Header';
import Footer from '../components/Footer';
import {
    Presentation,
    Crown,
    Users,
    Video,
    Zap,
    Heart,
    Building2,
    Mail,
    GraduationCap,
    Lightbulb,
    Handshake
} from 'lucide-react';

export default function Corporate() {
    const {t} = useTranslation('common');
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
        const {name, value} = e.target;
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
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/api/corporate-inquiry`, {
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
                <title>{t('corporate.title')} | Peter Stoyanov</title>
                <meta name="description" content={t('corporate.description')}/>
                <link rel="icon" href="/favicons/favicon.ico"/>
            </Head>

            <Header/>

            <main>
                {/* Hero Section */}
                <section
                    className="relative pt-24 pb-20 md:pt-32 md:pb-32 overflow-hidden bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
                    {/* Vibrant Background decoration */}
                    <div className="absolute inset-0 overflow-hidden">
                        <div
                            className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-blue-300/8 to-teal-400/8 rounded-full blur-3xl animate-float"></div>
                        <div
                            className="absolute top-3/4 right-1/4 w-80 h-80 bg-gradient-to-br from-slate-300/8 to-blue-400/8 rounded-full blur-3xl animate-float-delayed"></div>
                        <div
                            className="absolute top-1/2 left-1/2 w-72 h-72 bg-gradient-to-br from-indigo-300/8 to-purple-400/8 rounded-full blur-3xl animate-float-slow"></div>
                    </div>

                    <div className="container mx-auto px-4 relative z-10">
                        <div className="max-w-5xl mx-auto text-center">
                            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black mb-8 text-white leading-tight drop-shadow-2xl animate-fade-in-up">
                <span
                    className="bg-gradient-to-r from-blue-300 via-teal-300 to-indigo-300 bg-clip-text text-transparent">
                  {t('corporate.hero.title')}
                </span>
                                <br/>
                                <span className="text-blue-200 drop-shadow-lg">
                  {t('corporate.hero.subtitle')}
                </span>
                            </h1>
                            <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-4xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                                {t('corporate.hero.description')}
                            </p>

                            {/* Stats & Image */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                                <div>
                                    <blockquote
                                        className="text-xl italic text-white mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl font-semibold leading-relaxed animate-fade-in-up delay-300">
                                        "{t('corporate.hero.quote')}"
                                    </blockquote>
                                </div>

                                <div className="text-center">
                                    <div className="relative inline-block">
                                        <div
                                            className="h-90 w-80 rounded-3xl overflow-hidden shadow-2xl border-8 border-white">
                                            <img
                                                src="/pictures/PeterStoyanov-straight-look-in-your-eyes.jpg"
                                                alt="Peter Stoyanov - Executive Presence and Leadership Training"
                                                className="w-full h-full object-cover"
                                            />
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Services Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">
                    {/* Floating Background Elements */}
                    <div className="absolute inset-0 overflow-hidden">
                        <div
                            className="absolute top-1/4 right-1/4 w-80 h-80 bg-gradient-to-br from-blue-300/8 to-teal-400/8 rounded-full blur-3xl animate-float"></div>
                        <div
                            className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-indigo-300/8 to-purple-400/8 rounded-full blur-3xl animate-float-delayed"></div>
                    </div>
                    <div className="container mx-auto px-4">
                        <div className="text-center mb-20 relative z-10">
                            <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                {t('corporate.services.title')}
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                {t('corporate.services.subtitle')}
                            </p>
                        </div>

                        <div
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto relative z-10">
                            {/* Service 1 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Presentation className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.services.presentation.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.presentation.description')}</p>
                            </div>

                            {/* Service 2 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Crown className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('corporate.services.leadership.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.leadership.description')}</p>
                            </div>

                            {/* Service 3 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Users className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">{t('corporate.services.communication.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.communication.description')}</p>
                            </div>

                            {/* Service 4 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Video className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.services.camera.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.camera.description')}</p>
                            </div>

                            {/* Service 5 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-400">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-red-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Zap className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-red-200 drop-shadow-lg">{t('corporate.services.improvisation.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.improvisation.description')}</p>
                            </div>

                            {/* Service 6 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-500">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Heart className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-cyan-200 drop-shadow-lg">{t('corporate.services.stress.title')}</h3>
                                <p className="text-white/90 leading-relaxed">{t('corporate.services.stress.description')}</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Inquiry Form Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900 relative overflow-hidden">
                    {/* Floating Background Elements */}
                    <div className="absolute inset-0 overflow-hidden">
                        <div
                            className="absolute top-1/4 left-1/4 w-80 h-80 bg-gradient-to-br from-blue-300/8 to-teal-400/8 rounded-full blur-3xl animate-float"></div>
                        <div
                            className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-br from-slate-300/8 to-blue-400/8 rounded-full blur-3xl animate-float-delayed"></div>
                    </div>
                    <div className="container mx-auto px-4">
                        <div className="max-w-4xl mx-auto">
                            <div className="text-center mb-16 relative z-10">
                                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                    {t('corporate.form.title')}
                                </h2>
                                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                    {t('corporate.form.subtitle')}
                                </p>
                            </div>

                            <div
                                className="bg-white/10 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12 border border-white/20 relative z-10 animate-fade-in-up delay-200">
                                <div className="text-center mb-10">
                                    <h3 className="text-3xl font-black text-blue-200 drop-shadow-lg">
                                        {t('corporate.form.consultationTitle')}
                                    </h3>
                                    <p className="text-white/90 mt-3 font-semibold">
                                        {t('corporate.form.consultationSubtitle')}
                                    </p>
                                </div>

                                {formErrors.submit && (
                                    <div
                                        className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                                        {formErrors.submit}
                                    </div>
                                )}

                                <form onSubmit={handleSubmit}>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                        {/* Company Name */}
                                        <div>
                                            <label htmlFor="companyName"
                                                   className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.companyName')} *
                                            </label>
                                            <input
                                                type="text"
                                                id="companyName"
                                                name="companyName"
                                                value={formData.companyName}
                                                onChange={handleChange}
                                                className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                                                    formErrors.companyName ? 'border-red-400' : ''
                                                }`}
                                            />
                                            {formErrors.companyName && (
                                                <p className="mt-1 text-sm text-red-600">{formErrors.companyName}</p>
                                            )}
                                        </div>

                                        {/* Contact Person */}
                                        <div>
                                            <label htmlFor="contactPerson"
                                                   className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.contactPerson')} *
                                            </label>
                                            <input
                                                type="text"
                                                id="contactPerson"
                                                name="contactPerson"
                                                value={formData.contactPerson}
                                                onChange={handleChange}
                                                className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                                                    formErrors.contactPerson ? 'border-red-400' : ''
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
                                            <label htmlFor="email" className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.email')} *
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
                                                <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>
                                            )}
                                        </div>

                                        {/* Phone */}
                                        <div>
                                            <label htmlFor="phone" className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.phone')}
                                            </label>
                                            <input
                                                type="tel"
                                                id="phone"
                                                name="phone"
                                                value={formData.phone}
                                                onChange={handleChange}
                                                className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                        {/* Team Size */}
                                        <div>
                                            <label htmlFor="teamSize"
                                                   className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.teamSize')} *
                                            </label>
                                            <select
                                                id="teamSize"
                                                name="teamSize"
                                                value={formData.teamSize}
                                                onChange={handleChange}
                                                className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                                                    formErrors.teamSize ? 'border-red-400' : ''
                                                }`}
                                            >
                                                <option value="">{t('corporate.form.teamSizeOptions.placeholder')}</option>
                                                <option value="5-15">{t('corporate.form.teamSizeOptions.small')}</option>
                                                <option value="16-30">{t('corporate.form.teamSizeOptions.medium')}</option>
                                                <option value="31-50">{t('corporate.form.teamSizeOptions.large')}</option>
                                                <option value="51-100">{t('corporate.form.teamSizeOptions.xlarge')}</option>
                                                <option value="100+">{t('corporate.form.teamSizeOptions.enterprise')}</option>
                                            </select>
                                            {formErrors.teamSize && (
                                                <p className="mt-1 text-sm text-red-600">{formErrors.teamSize}</p>
                                            )}
                                        </div>

                                        {/* Budget */}
                                        <div>
                                            <label htmlFor="budget" className="block text-blue-200 font-semibold mb-2">
                                                {t('corporate.form.budget')}
                                            </label>
                                            <select
                                                id="budget"
                                                name="budget"
                                                value={formData.budget}
                                                onChange={handleChange}
                                                className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                                            >
                                                <option value="">{t('corporate.form.budgetOptions.placeholder')}</option>
                                                <option value="under-5k">{t('corporate.form.budgetOptions.under5k')}</option>
                                                <option value="5k-10k">{t('corporate.form.budgetOptions.5k10k')}</option>
                                                <option value="10k-20k">{t('corporate.form.budgetOptions.10k20k')}</option>
                                                <option value="20k+">{t('corporate.form.budgetOptions.20kplus')}</option>
                                                <option value="discuss">{t('corporate.form.budgetOptions.discuss')}</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/* Training Goals */}
                                    <div className="mb-6">
                                        <label htmlFor="trainingGoals"
                                               className="block text-blue-200 font-semibold mb-2">
                                            {t('corporate.form.trainingGoals')} *
                                        </label>
                                        <textarea
                                            id="trainingGoals"
                                            name="trainingGoals"
                                            value={formData.trainingGoals}
                                            onChange={handleChange}
                                            rows="4"
                                            placeholder={t('corporate.form.trainingGoalsPlaceholder')}
                                            className={`w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300 ${
                                                formErrors.trainingGoals ? 'border-red-400' : ''
                                            }`}
                                        ></textarea>
                                        {formErrors.trainingGoals && (
                                            <p className="mt-1 text-sm text-red-600">{formErrors.trainingGoals}</p>
                                        )}
                                    </div>

                                    {/* Preferred Dates */}
                                    <div className="mb-6">
                                        <label htmlFor="preferredDates"
                                               className="block text-blue-200 font-semibold mb-2">
                                            {t('corporate.form.preferredDates')}
                                        </label>
                                        <input
                                            type="text"
                                            id="preferredDates"
                                            name="preferredDates"
                                            value={formData.preferredDates}
                                            onChange={handleChange}
                                            placeholder={t('corporate.form.preferredDatesPlaceholder')}
                                            className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                                        />
                                    </div>

                                    {/* Additional Info */}
                                    <div className="mb-8">
                                        <label htmlFor="additionalInfo"
                                               className="block text-blue-200 font-semibold mb-2">
                                            {t('corporate.form.additionalInfo')}
                                        </label>
                                        <textarea
                                            id="additionalInfo"
                                            name="additionalInfo"
                                            value={formData.additionalInfo}
                                            onChange={handleChange}
                                            rows="3"
                                            placeholder={t('corporate.form.additionalInfoPlaceholder')}
                                            className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                                        ></textarea>
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
                                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                                         fill="none" viewBox="0 0 24 24">
                                                        <circle className="opacity-25" cx="12" cy="12" r="10"
                                                                stroke="currentColor" strokeWidth="4"></circle>
                                                        <path className="opacity-75" fill="currentColor"
                                                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                    </svg>
                                                    {t('corporate.form.submitting')}
                                                </>
                                            ) : (
                                                <>
                                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor"
                                                         viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round"
                                                              strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                                                    </svg>
                                                    {t('corporate.form.submitButton')}
                                                </>
                                            )}
                                        </button>
                                        <p className="text-sm text-blue-200/80 mt-4 font-semibold">
                                            {t('corporate.form.responseNote')}
                                        </p>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Benefits Section */}
                <section
                    className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800 relative overflow-hidden">
                    {/* Floating Background Elements */}
                    <div className="absolute inset-0 overflow-hidden">
                        <div
                            className="absolute top-1/3 left-1/3 w-72 h-72 bg-yellow-300/20 rounded-full blur-3xl animate-float"></div>
                        <div
                            className="absolute bottom-1/3 right-1/3 w-96 h-96 bg-purple-300/20 rounded-full blur-3xl animate-float-delayed"></div>
                    </div>
                    <div className="container mx-auto px-4">
                        <div className="text-center mb-16 relative z-10">
                            <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl animate-fade-in-up">
                                {t('corporate.benefits.title')}
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                {t('corporate.benefits.subtitle')}
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto relative z-10">
                            {/* Benefit 1 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-slate-600 to-blue-700 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <GraduationCap className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">{t('corporate.benefits.experiential.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.experiential.description')}
                                </p>
                            </div>

                            {/* Benefit 2 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Lightbulb className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">{t('corporate.benefits.immediate.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.immediate.description')}
                                </p>
                            </div>

                            {/* Benefit 3 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Handshake className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">{t('corporate.benefits.teamBonding.title')}</h3>
                                <p className="text-white/90 leading-relaxed">
                                    {t('corporate.benefits.teamBonding.description')}
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            <Footer/>
        </div>
    );
}

export async function getStaticProps({locale}) {
    return {
        props: {
            ...(await serverSideTranslations(locale, ['common'])),
        },
    };
}