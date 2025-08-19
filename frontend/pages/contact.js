import Head from 'next/head';

export default function Contact() {
  return (
    <>
      <Head>
        <title>Contact - Peter Stoyanov Coaching</title>
        <meta name="description" content="Get in touch with Peter Stoyanov for professional coaching services" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4 text-gray-800">Contact Peter Stoyanov</h1>
            <p className="text-lg text-gray-600">
              Ready to transform your communication and leadership skills?
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h2 className="text-2xl font-semibold mb-4 text-gray-800">Get In Touch</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-gray-700">Email</h3>
                    <a 
                      href="mailto:peterstoyanov83@gmail.com" 
                      className="text-blue-600 hover:text-blue-800"
                    >
                      peterstoyanov83@gmail.com
                    </a>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-gray-700">Services</h3>
                    <ul className="text-gray-600 space-y-1">
                      <li>• Individual Coaching Sessions</li>
                      <li>• Corporate Training Programs</li>
                      <li>• Leadership Development</li>
                      <li>• Communication Workshops</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div>
                <h2 className="text-2xl font-semibold mb-4 text-gray-800">About My Approach</h2>
                <p className="text-gray-600 mb-4">
                  With over 20 years of experience in theater, communication, and leadership 
                  development, I bring a unique combination of artistic insight and professional 
                  expertise to every coaching session.
                </p>
                <p className="text-gray-600">
                  Whether you're looking to improve your public speaking, develop executive 
                  presence, or build team communication skills, I tailor my approach to meet 
                  your specific needs and goals.
                </p>
              </div>
            </div>
          </div>

          <div className="text-center mt-12">
            <a 
              href="/"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              ← Back to Home
            </a>
          </div>
        </div>
      </div>
    </>
  );
}