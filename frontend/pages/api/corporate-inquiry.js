export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    const {
      companyName,
      contactPerson,
      email,
      phone,
      teamSize,
      budget,
      trainingGoals,
      preferredDates,
      additionalInfo
    } = req.body;

    // Basic validation
    if (!companyName || !contactPerson || !email || !teamSize || !trainingGoals) {
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

    // For now, just log the corporate inquiry data
    // In production, you would save this to a database
    console.log('New corporate training inquiry:', {
      companyName,
      contactPerson,
      email,
      phone,
      teamSize,
      budget,
      trainingGoals,
      preferredDates,
      additionalInfo,
      submitted_at: new Date().toISOString()
    });

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Return success response
    return res.status(200).json({ 
      message: 'Corporate inquiry submitted successfully',
      data: { companyName, contactPerson, email }
    });

  } catch (error) {
    console.error('Corporate inquiry error:', error);
    return res.status(500).json({ 
      message: 'Internal server error. Please try again later.' 
    });
  }
}