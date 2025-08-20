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

      <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', fontFamily: 'Arial, sans-serif' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          {/* Hero Section */}
          <section style={{ textAlign: 'center', paddingTop: '80px', paddingBottom: '80px', color: 'white' }}>
            <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '16px', margin: 0 }}>
              Peter Stoyanov
            </h1>
            <p style={{ fontSize: '1.5rem', marginBottom: '32px' }}>
              Communication & Leadership Coach
            </p>
            <p style={{ fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 40px auto', lineHeight: '1.6' }}>
              Transform your communication skills and unlock your leadership potential 
              with over 20 years of professional coaching experience.
            </p>
          </section>

          {/* Services */}
          <section style={{ paddingBottom: '80px' }}>
            <h2 style={{ fontSize: '2rem', textAlign: 'center', marginBottom: '48px', color: 'white' }}>
              Professional Coaching Services
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                <h3 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '16px', color: '#2c5282' }}>
                  Individual Coaching
                </h3>
                <p style={{ color: '#4a5568', lineHeight: '1.6' }}>
                  Personal development for communication excellence and leadership presence.
                </p>
              </div>
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                <h3 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '16px', color: '#2c5282' }}>
                  Corporate Training
                </h3>
                <p style={{ color: '#4a5568', lineHeight: '1.6' }}>
                  Team workshops and organizational communication development programs.
                </p>
              </div>
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                <h3 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '16px', color: '#2c5282' }}>
                  Leadership Development
                </h3>
                <p style={{ color: '#4a5568', lineHeight: '1.6' }}>
                  Build confidence, presence, and communication skills for effective leadership.
                </p>
              </div>
            </div>
          </section>

          {/* CTA */}
          <section style={{ textAlign: 'center', paddingBottom: '80px' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '32px', color: 'white' }}>
              Get Started Today
            </h2>
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <a 
                href="/guides/exersises-for-breathing-voice-and-speaking.pdf"
                style={{ 
                  background: 'linear-gradient(135deg, #38a169 0%, #2f855a 100%)',
                  color: 'white',
                  padding: '15px 30px',
                  textDecoration: 'none',
                  borderRadius: '8px',
                  fontWeight: '600',
                  fontSize: '1.1rem',
                  display: 'inline-block',
                  transition: 'transform 0.2s'
                }}
                onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
              >
                Download Free Voice Guide
              </a>
              <a 
                href="mailto:peterstoyanov83@gmail.com"
                style={{ 
                  background: 'linear-gradient(135deg, #2c5282 0%, #2a4365 100%)',
                  color: 'white',
                  padding: '15px 30px',
                  textDecoration: 'none',
                  borderRadius: '8px',
                  fontWeight: '600',
                  fontSize: '1.1rem',
                  display: 'inline-block',
                  transition: 'transform 0.2s'
                }}
                onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
              >
                Contact Me
              </a>
            </div>
          </section>
        </div>

        {/* Footer */}
        <footer style={{ background: 'rgba(0,0,0,0.2)', color: 'white', padding: '32px 0', textAlign: 'center' }}>
          <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
            <p style={{ marginBottom: '8px' }}>© 2024 Peter Stoyanov Coaching</p>
            <p style={{ color: 'rgba(255,255,255,0.8)', margin: 0 }}>
              Professional Communication & Leadership Development
            </p>
          </div>
        </footer>
      </div>
    </>
  );
}