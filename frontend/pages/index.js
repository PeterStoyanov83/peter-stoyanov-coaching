import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>Peter Stoyanov - Communication & Leadership Coach</title>
        <meta name="description" content="Professional coaching for communication and leadership development" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <div className="max-w-6xl mx-auto px-4 py-20 text-center">
            <h1 className="text-5xl font-bold mb-4">Peter Stoyanov</h1>
            <p className="text-xl mb-8">Communication & Leadership Coach</p>
            <p className="text-lg max-w-2xl mx-auto">
              Transform your communication skills and unlock your leadership potential 
              with over 20 years of professional coaching experience.
            </p>
          </div>
        </section>

        {/* Services */}
        <section className="py-16">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
              Professional Coaching Services
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold mb-4 text-blue-600">Individual Coaching</h3>
                <p className="text-gray-600">
                  Personal development for communication excellence and leadership presence.
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold mb-4 text-blue-600">Corporate Training</h3>
                <p className="text-gray-600">
                  Team workshops and organizational communication development programs.
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold mb-4 text-blue-600">Leadership Development</h3>
                <p className="text-gray-600">
                  Build confidence, presence, and communication skills for effective leadership.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-gray-100 py-16">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-8 text-gray-800">Get Started Today</h2>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="/guides/exersises-for-breathing-voice-and-speaking.pdf"
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition"
              >
                Download Free Voice Guide
              </a>
              <a 
                href="mailto:peterstoyanov83@gmail.com"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition"
              >
                Contact Me
              </a>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-800 text-white py-8">
          <div className="max-w-6xl mx-auto px-4 text-center">
            <p className="mb-2">© 2024 Peter Stoyanov Coaching</p>
            <p className="text-gray-400">Professional Communication & Leadership Development</p>
          </div>
        </footer>
      </div>
    </>
  );
}