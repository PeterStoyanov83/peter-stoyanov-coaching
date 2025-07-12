"""
Professional email templates with improved deliverability
"""

def create_professional_email_template(content: str, preheader: str = "", unsubscribe_link: str = "") -> str:
    """
    Create a professional email template with proper formatting for deliverability
    
    Args:
        content: Main email content (HTML)
        preheader: Preview text that appears in inbox
        unsubscribe_link: Unsubscribe URL
    
    Returns:
        Formatted HTML email template
    """
    
    return f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title>Peter Stoyanov - Executive Presence Coach</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style>
        table, td, div, h1, h2, h3, h4, h5, h6, p {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #1e3a8a;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            padding: 30px 20px;
            line-height: 1.6;
            color: #333333;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
        }}
        .cta-button {{
            display: inline-block;
            background-color: #10b981;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
        }}
        .preheader {{
            display: none;
            max-height: 0;
            overflow: hidden;
        }}
        @media only screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
            }}
            .content {{
                padding: 20px 15px !important;
            }}
        }}
    </style>
</head>
<body style="margin:0;padding:0;word-spacing:normal;background-color:#f4f4f4;">
    <div class="preheader">{preheader}</div>
    
    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#f4f4f4;">
        <tr>
            <td align="center" style="padding:0;">
                <table role="presentation" class="email-container" style="width:600px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                    
                    <!-- Header -->
                    <tr>
                        <td class="header">
                            <h1 style="font-size:24px;margin:0;color:white;">Peter Stoyanov</h1>
                            <p style="margin:5px 0 0 0;font-size:14px;opacity:0.9;">Executive Presence & Leadership Coach</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td class="content">
                            {content}
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td class="footer">
                            <p style="margin:0 0 10px 0;"><strong>Peter Stoyanov</strong><br>
                            Executive Presence & Leadership Coach<br>
                            <a href="https://peterstoyanov-pepe.com" style="color:#1e3a8a;">peterstoyanov-pepe.com</a></p>
                            
                            <p style="margin:10px 0;">
                                <a href="mailto:peter@peterstoyanov-pepe.com" style="color:#666666;text-decoration:none;">peter@peterstoyanov-pepe.com</a>
                            </p>
                            
                            <p style="margin:15px 0 0 0;font-size:11px;color:#999999;">
                                You received this email because you subscribed to Peter Stoyanov's coaching insights.<br>
                                <a href="{unsubscribe_link}" style="color:#999999;">Unsubscribe</a> | 
                                <a href="https://peterstoyanov-pepe.com/privacy-policy" style="color:#999999;">Privacy Policy</a>
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def create_welcome_email_content(name: str = "there") -> dict:
    """Create the welcome email content with proper formatting"""
    
    preheader = "Your Stage Presence transformation starts right now - access your guide inside"
    
    content = f"""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; margin-bottom: 30px; border-radius: 10px;">
        <h2 style="margin: 0; color: white; font-size: 28px;">🎉 Thank You for Downloading!</h2>
        <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Your Stage Presence transformation starts right now</p>
    </div>
    
    <h2 style="color: #1e3a8a; margin-bottom: 20px;">Hello {name},</h2>
    
    <p style="margin-bottom: 15px;"><strong>First things first - THANK YOU!</strong> 🙏</p>
    
    <p style="margin-bottom: 15px;">You just took the first step toward commanding presence, and I'm absolutely thrilled to be part of your journey. Your "5 Theater Secrets" guide should be in your downloads folder right now.</p>
    
    <div style="background: #fef7cd; padding: 20px; border-left: 4px solid #f59e0b; margin: 20px 0; border-radius: 0 8px 8px 0;">
        <p style="margin: 0;"><strong>📥 Can't find your guide?</strong> <a href="https://peterstoyanov-pepe.com/guides/5-theater-secrets-guide.pdf" style="color: #f59e0b; font-weight: bold;">Download it again here</a>.</p>
    </div>
    
    <p style="margin-bottom: 15px;"><strong>Here's what most people don't realize:</strong> The #1 thing killing your stage presence isn't nerves, lack of experience, or even fear of judgment.</p>
    
    <p style="margin-bottom: 15px;">It's trying to be someone you're not.</p>
    
    <p style="margin-bottom: 15px;">I learned this the hard way during my 15 years performing across 12 countries. From the streets of Sofia to corporate boardrooms in London, I discovered something powerful:</p>
    
    <p style="margin-bottom: 20px; font-style: italic; font-size: 18px; color: #1e3a8a;">Your authentic energy is your greatest weapon.</p>
    
    <div style="background: #f0f9ff; padding: 20px; border-left: 4px solid #0ea5e9; margin: 20px 0; border-radius: 0 8px 8px 0;">
        <p style="margin: 0;"><strong>Your first reality check:</strong> Stop trying to copy other speakers. Your unique energy is what will make you unforgettable.</p>
    </div>
    
    <p style="margin-bottom: 15px;">Over the next 10 weeks, I'll be sharing the exact methods I use with executives and leaders worldwide. Every Monday, you'll get practical insights that you can use immediately.</p>
    
    <p style="margin-bottom: 15px;">But right now, I'd love to hear from you - what's your biggest stage presence challenge? Hit reply and tell me. I read every email personally.</p>
    
    <p style="margin-bottom: 20px;">Ready to unlock your natural command?</p>
    
    <div style="margin: 30px 0; text-align: center;">
        <a href="mailto:peter@peterstoyanov-pepe.com?subject=My biggest stage presence challenge" class="cta-button" style="display: inline-block; background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Reply: Share Your Challenge</a>
    </div>
    
    <p style="margin-top: 30px; color: #666666; font-style: italic;">P.S. Keep an eye out for my next email this Monday - I'll share how I hold 100+ strangers' attention for 1 hour without a microphone.</p>
    """
    
    return {
        "subject": "🎭 Thank you + Your Stage Presence Guide is here!",
        "preheader": preheader,
        "content": content
    }