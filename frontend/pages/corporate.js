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
                  Corporate Training
                </span>
                                <br/>
                                <span className="text-blue-200 drop-shadow-lg">
                  That Transforms Teams
                </span>
                            </h1>
                            <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-4xl mx-auto leading-relaxed font-semibold animate-fade-in-up delay-100">
                                Elevate your team's communication, leadership presence, and collaboration skills through
                                proven theater techniques and interactive workshops designed for business professionals.
                            </p>

                            {/* Stats & Image */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mt-16">
                                <div>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in-up delay-200">
                                        <div
                                            className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                                            <div
                                                className="text-4xl font-black text-yellow-300 mb-2 drop-shadow-lg">50+
                                            </div>
                                            <div className="text-white/90 font-semibold">Companies Trained</div>
                                        </div>
                                        <div
                                            className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300">
                                            <div
                                                className="text-4xl font-black text-green-300 mb-2 drop-shadow-lg">95%
                                            </div>
                                            <div className="text-white/90 font-semibold">Satisfaction Rate</div>
                                        </div>
                                        <div
                                            className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300">
                                            <div
                                                className="text-4xl font-black text-orange-300 mb-2 drop-shadow-lg">1000+
                                            </div>
                                            <div className="text-white/90 font-semibold">Professionals Trained</div>
                                        </div>
                                    </div>
                                    <blockquote
                                        className="text-xl italic text-white mt-8 p-8 bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm rounded-3xl border border-white/30 shadow-2xl font-semibold leading-relaxed animate-fade-in-up delay-300">
                                        "Theater techniques don't just improve communication—they transform how teams
                                        connect, collaborate, and lead with authentic confidence."
                                    </blockquote>
                                </div>

                                <div className="text-center">
                                    <div className="relative inline-block">
                                        <div
                                            className="w-80 h-96 rounded-3xl overflow-hidden shadow-2xl border-8 border-gradient-to-r from-yellow-400 to-pink-400 transform hover:scale-105 transition-all duration-500 animate-fade-in-up delay-200">
                                            <img
                                                src="/pictures/PeterStoyanov-powerful-2.jpg"
                                                alt="Petar Stoyanov - Executive Presence and Leadership Training"
                                                className="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                                            />
                                            <div
                                                className="absolute inset-0 bg-gradient-to-t from-purple-600/30 via-transparent to-yellow-400/20"></div>
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
                                🎯 Training Programs 🎯
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                ✨ Customized workshops that address your team's specific communication and leadership
                                challenges
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
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">Presentation
                                    Excellence</h3>
                                <p className="text-white/90 leading-relaxed">Master the art of compelling presentations
                                    using voice, body language, and storytelling techniques that captivate
                                    audiences.</p>
                            </div>

                            {/* Service 2 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Crown className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">Leadership
                                    Presence</h3>
                                <p className="text-white/90 leading-relaxed">Develop commanding presence and authentic
                                    leadership communication that inspires teams and drives results.</p>
                            </div>

                            {/* Service 3 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Users className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">Team
                                    Communication</h3>
                                <p className="text-white/90 leading-relaxed">Enhance collaboration, active listening,
                                    and conflict resolution through interactive theater-based exercises.</p>
                            </div>

                            {/* Service 4 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-300">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Video className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">Camera
                                    Confidence</h3>
                                <p className="text-white/90 leading-relaxed">Excel in video meetings, interviews, and
                                    digital presentations with professional on-camera presence and delivery.</p>
                            </div>

                            {/* Service 5 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-400">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-red-400 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:rotate-12 transition-all duration-300">
                                    <Zap className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-red-200 drop-shadow-lg">Improvisation
                                    Skills</h3>
                                <p className="text-white/90 leading-relaxed">Build quick thinking, adaptability, and
                                    creative problem-solving skills for dynamic business situations.</p>
                            </div>

                            {/* Service 6 */}
                            <div
                                className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-500">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl transform hover:scale-110 hover:-rotate-12 transition-all duration-300">
                                    <Heart className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-cyan-200 drop-shadow-lg">Stress
                                    Management</h3>
                                <p className="text-white/90 leading-relaxed">Learn breathing techniques and mindfulness
                                    practices to maintain composure and clarity under pressure.</p>
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
                                    Request a Custom Training Proposal
                                </h2>
                                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                    ✨ Let's discuss how theater-based training can transform your team's communication
                                    and performance
                                </p>
                            </div>

                            <div
                                className="bg-white/10 backdrop-blur-sm shadow-2xl rounded-3xl p-8 md:p-12 border border-white/20 relative z-10 animate-fade-in-up delay-200">
                                <div className="text-center mb-10">
                                    <h3 className="text-3xl font-black text-blue-200 drop-shadow-lg">
                                        Get Your Free Consultation
                                    </h3>
                                    <p className="text-white/90 mt-3 font-semibold">
                                        Tell us about your team's goals and we'll create a customized training program
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
                                                Company Name *
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
                                                Contact Person *
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
                                                Email Address *
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
                                                Phone Number
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
                                                Team Size *
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
                                            <label htmlFor="budget" className="block text-blue-200 font-semibold mb-2">
                                                Estimated Budget
                                            </label>
                                            <select
                                                id="budget"
                                                name="budget"
                                                value={formData.budget}
                                                onChange={handleChange}
                                                className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
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
                                        <label htmlFor="trainingGoals"
                                               className="block text-blue-200 font-semibold mb-2">
                                            Training Goals & Challenges *
                                        </label>
                                        <textarea
                                            id="trainingGoals"
                                            name="trainingGoals"
                                            value={formData.trainingGoals}
                                            onChange={handleChange}
                                            rows="4"
                                            placeholder="What communication challenges does your team face? What outcomes are you hoping to achieve?"
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
                                            Preferred Training Dates
                                        </label>
                                        <input
                                            type="text"
                                            id="preferredDates"
                                            name="preferredDates"
                                            value={formData.preferredDates}
                                            onChange={handleChange}
                                            placeholder="e.g., March 2024, flexible, ASAP"
                                            className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/60 backdrop-blur-sm focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all duration-300"
                                        />
                                    </div>

                                    {/* Additional Info */}
                                    <div className="mb-8">
                                        <label htmlFor="additionalInfo"
                                               className="block text-blue-200 font-semibold mb-2">
                                            Additional Information
                                        </label>
                                        <textarea
                                            id="additionalInfo"
                                            name="additionalInfo"
                                            value={formData.additionalInfo}
                                            onChange={handleChange}
                                            rows="3"
                                            placeholder="Any specific requirements, team dynamics, or additional context we should know about?"
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
                                                    Sending Request...
                                                </>
                                            ) : (
                                                <>
                                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor"
                                                         viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round"
                                                              strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                                                    </svg>
                                                    Request Free Consultation
                                                </>
                                            )}
                                        </button>
                                        <p className="text-sm text-blue-200/80 mt-4 font-semibold">
                                            ✨ We'll respond within 48 hours with a customized training proposal
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
                                Why Choose Play-Based Training?
                            </h2>
                            <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold animate-fade-in-up delay-100">
                                ✨ Proven techniques from the world of performance that create lasting behavioral change
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
                                <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">Experiential
                                    Learning</h3>
                                <p className="text-white/90 leading-relaxed">
                                    Learn by doing through interactive exercises that create muscle memory for confident
                                    communication.
                                </p>
                            </div>

                            {/* Benefit 2 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:-rotate-1 transition-all duration-300 animate-fade-in-up delay-100">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Lightbulb className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-green-200 drop-shadow-lg">Immediate
                                    Results</h3>
                                <p className="text-white/90 leading-relaxed">
                                    See transformation in real-time as participants break through limiting beliefs and
                                    discover their authentic presence.
                                </p>
                            </div>

                            {/* Benefit 3 */}
                            <div
                                className="text-center bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl transform hover:scale-105 hover:rotate-1 transition-all duration-300 animate-fade-in-up delay-200">
                                <div
                                    className="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
                                    <Handshake className="w-8 h-8 text-white" strokeWidth={1.5}/>
                                </div>
                                <h3 className="text-2xl font-black mb-4 text-purple-200 drop-shadow-lg">Team
                                    Bonding</h3>
                                <p className="text-white/90 leading-relaxed">
                                    Build trust and collaboration as teams work together in a safe, supportive, and
                                    energizing environment.
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