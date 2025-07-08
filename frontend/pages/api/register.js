export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const {
      full_name,
      email,
      city_country,
      occupation,
      why_join,
      skills_to_improve
    } = req.body;

    // Basic validation
    if (!full_name || !email || !city_country || !occupation || !why_join || !skills_to_improve) {
      return res.status(400).json({ 
        message: 'All required fields must be filled out' 
      });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ 
        message: 'Please provide a valid email address' 
      });
    }

    // For now, just log the registration data
    // In production, you would save this to a database
    console.log('New waitlist registration:', {
      full_name,
      email,
      city_country,
      occupation,
      why_join,
      skills_to_improve,
      registered_at: new Date().toISOString()
    });

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Return success response
    return res.status(200).json({ 
      message: 'Registration successful',
      data: { full_name, email }
    });

  } catch (error) {
    console.error('Registration error:', error);
    return res.status(500).json({ 
      message: 'Internal server error. Please try again later.' 
    });
  }
}