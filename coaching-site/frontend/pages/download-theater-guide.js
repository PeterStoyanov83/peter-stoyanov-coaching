import { useState, useEffect } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import BackToTop from '../components/BackToTop';
import { useLanguage } from '../contexts/LanguageContext';
import { Download, CheckCircle, Mail, Calendar, Star, ArrowRight } from 'lucide-react';

export default function DownloadTheaterGuide() {
  const { t } = useLanguage();
  const [downloadStarted, setDownloadStarted] = useState(false);

  // Auto-download the guide when page loads
  useEffect(() => {
    const timer = setTimeout(() => {
      handleDownload();
    }, 2000); // 2 second delay for user to see the page

    return () => clearTimeout(timer);
  }, []);

  const handleDownload = () => {
    setDownloadStarted(true);
    // Trigger download of the PDF guide
    const link = document.createElement('a');
    link.href = '/guides/The Complete Theater Secrets Guide.pdf';
    link.download = 'The_Complete_Theater_Secrets_Guide_Peter_Stoyanov.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-white">
      <Head>
        <title>Download Your Theater Secrets Guide | Peter Stoyanov</title>
        <meta name="description" content="Download your free guide to commanding any room with confidence" />
        <link rel="icon" href="/favicons/favicon.ico" />
      </Head>

      <Header />

      <main className="pt-20 pb-16">
        {/* Hero Section */}
        <section className="py-20 md:py-32 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-xl">
                <CheckCircle className="w-10 h-10 text-white" strokeWidth={2} />
              </div>

              <h1 className="text-4xl md:text-6xl font-black mb-8 text-white leading-tight drop-shadow-2xl">
                <span className="bg-gradient-to-r from-green-300 via-emerald-300 to-teal-300 bg-clip-text text-transparent">
                  Success!
                </span>
                <br />
                <span className="text-blue-200 text-3xl md:text-4xl">
                  Your Guide is Ready
                </span>
              </h1>

              <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed font-semibold">
                The Theater Secrets Guide is downloading automatically. Check your downloads folder in a moment!
              </p>

              {/* Download Button */}
              <div className="mb-12">
                <button
                  onClick={handleDownload}
                  className="inline-flex items-center justify-center px-10 py-5 text-xl font-black text-purple-900 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 rounded-2xl shadow-2xl transform transition-all duration-300 border-4 border-white/80 hover:scale-110 hover:-rotate-2 hover:shadow-3xl"
                >
                  <Download className="w-6 h-6 mr-3" />
                  {downloadStarted ? 'Download Again' : 'Download Now'}
                </button>
              </div>

              {/* What's Next Section */}
              <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl">
                <h2 className="text-2xl font-black text-white mb-6">What Happens Next?</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <Mail className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-blue-200 mb-2">Check Your Email</h3>
                    <p className="text-white/90 text-sm">
                      I'll send you additional tips and insights over the next few weeks
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <Star className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-green-200 mb-2">Start Practicing</h3>
                    <p className="text-white/90 text-sm">
                      Begin with the 30-day mastery plan in your guide
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <Calendar className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-purple-200 mb-2">Ready for More?</h3>
                    <p className="text-white/90 text-sm">
                      Watch for my coaching program announcement
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Next Steps Section */}
        <section className="py-20 md:py-28 bg-gradient-to-br from-slate-600 via-blue-700 to-indigo-800">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-4xl md:text-5xl font-black mb-6 text-white drop-shadow-2xl">
                  Ready to Accelerate Your Progress?
                </h2>
                <p className="text-xl text-blue-200 max-w-3xl mx-auto font-semibold">
                  The guide gives you the foundation. Personal coaching builds the transformation.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Self-Study Path */}
                <div className="bg-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border border-white/20 transform hover:scale-105 transition-all duration-300">
                  <h3 className="text-2xl font-black mb-4 text-blue-200 drop-shadow-lg">
                    Self-Study Path
                  </h3>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-green-300 mr-2 mt-0.5 flex-shrink-0" />
                      Follow the 30-day mastery plan
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-green-300 mr-2 mt-0.5 flex-shrink-0" />
                      Practice the 10 theater secrets daily
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-green-300 mr-2 mt-0.5 flex-shrink-0" />
                      Implement techniques in real situations
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-green-300 mr-2 mt-0.5 flex-shrink-0" />
                      Watch for weekly tips in your email
                    </li>
                  </ul>
                  <div className="text-center">
                    <div className="text-3xl font-black text-green-300 mb-2">FREE</div>
                    <p className="text-white/80 text-sm">Perfect for motivated self-learners</p>
                  </div>
                </div>

                {/* Coaching Path */}
                <div className="bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm p-8 rounded-3xl shadow-2xl border-2 border-yellow-400/50 transform hover:scale-105 transition-all duration-300 relative">
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 px-4 py-2 rounded-full text-sm font-black">
                      MOST POPULAR
                    </span>
                  </div>
                  <h3 className="text-2xl font-black mb-4 text-yellow-200 drop-shadow-lg">
                    Personal Coaching
                  </h3>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" />
                      One-on-one guidance from Peter
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" />
                      Customized techniques for your challenges
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" />
                      Real-time feedback and adjustments
                    </li>
                    <li className="flex items-start text-white/90">
                      <ArrowRight className="w-5 h-5 text-yellow-300 mr-2 mt-0.5 flex-shrink-0" />
                      Faster, lasting transformation
                    </li>
                  </ul>
                  <div className="text-center">
                    <div className="text-sm text-white/80 mb-2">Starting at</div>
                    <div className="text-3xl font-black text-yellow-300 mb-4">Contact for Pricing</div>
                    <button className="w-full bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 font-black py-3 px-6 rounded-xl hover:from-yellow-300 hover:to-orange-300 transition-all duration-300">
                      Learn More
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Social Proof Section */}
        <section className="py-20 bg-gradient-to-br from-slate-700 via-blue-800 to-indigo-900">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-black mb-12 text-white drop-shadow-2xl">
                Join Hundreds of Professionals Who've Transformed Their Communication
              </h2>

              <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl">
                <blockquote className="text-xl italic text-white mb-6 leading-relaxed">
                  "Peter's theater-based approach completely changed how I show up in meetings. I went from avoiding speaking up to leading presentations with confidence. The techniques in his guide were just the beginning - now I actually enjoy public speaking!"
                </blockquote>
                <div className="flex items-center justify-center">
                  <div className="text-center">
                    <div className="font-bold text-blue-200">Sarah M.</div>
                    <div className="text-white/80 text-sm">Marketing Director, Fortune 500</div>
                  </div>
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