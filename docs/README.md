# Coaching Site for Peter Stoyanov

A full-stack web application for a communication and stage presence coaching program led by Peter Stoyanov — an experienced actor, clown, and trainer with 20+ years of international work.

## 🚀 Features

- **Multilingual Support**: Bulgarian and English
- **Responsive Design**: Fully mobile-optimized
- **Waitlist Registration**: Collect leads for upcoming workshops
- **Corporate Inquiries**: Form for business training requests
- **Blog System**: Markdown-based content management
- **MailerLite Integration**: Email collection with SQLite fallback

## 🛠️ Tech Stack

### Frontend
- **Next.js**: React framework for server-rendered applications
- **TailwindCSS**: Utility-first CSS framework
- **next-i18next**: Internationalization support

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **MailerLite API**: Email marketing integration

### Infrastructure
- **Docker**: Containerization for consistent development and deployment
- **SQLite**: Lightweight database for storage

## 📁 Project Structure

```
coaching-site/
├── backend/
│   ├── main.py                # FastAPI application and endpoints
│   ├── models.py              # Data models
│   ├── mailerlite.py          # MailerLite API integration
│   ├── database.py            # Database connection and functions
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container configuration
│
├── frontend/
│   ├── pages/                 # Next.js pages
│   ├── components/            # Reusable React components
│   ├── public/                # Static assets
│   │   └── locales/           # Translation files
│   ├── styles/                # CSS styles
│   ├── i18n/                  # Internationalization config
│   └── Dockerfile             # Frontend container configuration
│
├── blog/                      # Markdown blog posts
│
├── docker-compose.yml         # Docker services configuration
├── .env.example               # Environment variables template
└── README.md                  # Project documentation
```

## 🚦 Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.9+ (for local development)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/coaching-site.git
   cd coaching-site
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```
   
3. Edit the `.env` file with your configuration values.

4. Start the application:
   ```bash
   docker-compose up -d
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 Blog Management

Blog posts are written in Markdown format and stored in the `blog/` directory. Each post should include:

```markdown
# Title of the Post

Date: YYYY-MM-DD
Tags: tag1, tag2, tag3

Content of the post...
```

## 🌐 Internationalization

The site supports Bulgarian (default) and English. Translation files are located in:

```
frontend/public/locales/bg/common.json
frontend/public/locales/en/common.json
```

## 📧 MailerLite Integration

To use MailerLite for email collection:

1. Sign up for a MailerLite account
2. Get your API key from the MailerLite dashboard
3. Add the API key to your `.env` file

If no API key is provided, the system will fall back to storing registrations in SQLite.

## 🔒 Security Notes

- The `.env` file contains sensitive information and should not be committed to version control
- In production, set up proper CORS configuration in the backend
- Consider using a more robust database for production (PostgreSQL, MySQL)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Peter Stoyanov - Communication Coach and Trainer