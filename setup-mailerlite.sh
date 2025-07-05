#!/bin/bash

echo "🎯 MailerLite Setup for Coaching Site"
echo "======================================"
echo ""

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created"
fi

echo ""
echo "📋 Setup Instructions:"
echo ""
echo "1. 🌐 Go to MailerLite:"
echo "   https://app.mailerlite.com/integrations/api"
echo ""
echo "2. 🔑 Generate new API token"
echo ""
echo "3. 📝 Edit your .env file:"
echo "   nano .env"
echo ""
echo "4. 🔧 Replace 'your_mailerlite_api_key_here' with your actual API key"
echo ""
echo "5. 🚀 Start your application:"
echo "   docker-compose up"
echo ""
echo "📁 Your .env file location: $(pwd)/.env"
echo ""
echo "🎉 After setup, your lead magnet will:"
echo "   ✅ Store emails in database"
echo "   ✅ Add subscribers to MailerLite"
echo "   ✅ Enable email marketing campaigns"
echo ""

# Check if MailerLite API key is set
if [ -f ".env" ]; then
    if grep -q "your_mailerlite_api_key_here" .env; then
        echo "⚠️  REMINDER: Don't forget to update your API key in .env!"
    else
        echo "✅ API key appears to be configured in .env"
    fi
fi