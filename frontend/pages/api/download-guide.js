// API endpoint for handling lead magnet downloads
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email } = req.body;

  // Basic email validation
  if (!email || !/\S+@\S+\.\S+/.test(email)) {
    return res.status(400).json({ message: 'Valid email address is required' });
  }

  try {
    // Here you would typically:
    // 1. Save the email to your database or email service (Mailchimp, ConvertKit, etc.)
    // 2. Send a welcome email with the download link
    // For now, we'll just simulate the process
    
    console.log(`New lead magnet signup: ${email}`);
    
    // In a real implementation, you might:
    // - Add to Mailchimp list
    // - Send welcome email via SendGrid/Mailgun
    // - Store in database
    // - Track analytics event
    
    // Return success response with download URL
    res.status(200).json({ 
      success: true, 
      message: 'Thank you! Your guide is ready for download.',
      downloadUrl: '/guides/5-theater-secrets-guide.pdf'
    });
    
  } catch (error) {
    console.error('Error processing lead magnet signup:', error);
    res.status(500).json({ 
      message: 'Something went wrong. Please try again.' 
    });
  }
}