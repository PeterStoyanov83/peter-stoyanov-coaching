from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
from typing import List, Optional
import markdown
import glob

from models import WaitlistRegistration, CorporateInquiry
from database import get_db, store_waitlist_registration, store_corporate_inquiry
from mailerlite import add_subscriber_to_mailerlite

app = FastAPI(title="Coaching Site API", description="API for Petar Stoyanov's coaching website")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WaitlistRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    city_country: str
    occupation: str
    why_join: str
    skills_to_improve: str

class CorporateInquiryRequest(BaseModel):
    company_name: str
    contact_person: str
    email: EmailStr
    message: str

class BlogPost(BaseModel):
    slug: str
    title: str
    content: str
    excerpt: str
    date: str
    tags: List[str] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Petar Stoyanov's Coaching API"}

@app.post("/api/register")
async def register_waitlist(
    registration: WaitlistRegistrationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    # Create model instance
    reg_model = WaitlistRegistration(
        full_name=registration.full_name,
        email=registration.email,
        city_country=registration.city_country,
        occupation=registration.occupation,
        why_join=registration.why_join,
        skills_to_improve=registration.skills_to_improve
    )
    
    # Try to add to MailerLite first
    mailer_success = False
    if os.getenv("MAILERLITE_API_KEY"):
        try:
            background_tasks.add_task(
                add_subscriber_to_mailerlite,
                registration.email,
                registration.full_name,
                {
                    "city_country": registration.city_country,
                    "occupation": registration.occupation,
                    "why_join": registration.why_join,
                    "skills_to_improve": registration.skills_to_improve
                }
            )
            mailer_success = True
        except Exception as e:
            print(f"MailerLite error: {e}")
            # Continue to SQLite fallback
    
    # Store in SQLite as fallback or if MailerLite failed
    if not mailer_success or not os.getenv("MAILERLITE_API_KEY"):
        store_waitlist_registration(db, reg_model)
    
    return {"status": "success", "message": "Registration successful"}

@app.post("/api/contact-corporate")
async def contact_corporate(
    inquiry: CorporateInquiryRequest,
    db = Depends(get_db)
):
    # Create model instance
    inq_model = CorporateInquiry(
        company_name=inquiry.company_name,
        contact_person=inquiry.contact_person,
        email=inquiry.email,
        message=inquiry.message
    )
    
    # Store in database
    store_corporate_inquiry(db, inq_model)
    
    return {"status": "success", "message": "Inquiry submitted successfully"}

@app.get("/api/posts", response_model=List[BlogPost])
def get_blog_posts(tag: Optional[str] = None):
    posts = []
    
    # Get all markdown files from the blog directory
    blog_files = glob.glob("../blog/*.md")
    
    for file_path in blog_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract metadata and content
        # This is a simple implementation - in a real app, you might want to use frontmatter
        lines = content.split("\n")
        title = lines[0].replace("# ", "")
        date = ""
        tags_list = []
        
        # Look for metadata in the first few lines
        for i, line in enumerate(lines[1:5]):
            if line.startswith("Date: "):
                date = line.replace("Date: ", "")
            elif line.startswith("Tags: "):
                tags_text = line.replace("Tags: ", "")
                tags_list = [tag.strip() for tag in tags_text.split(",")]
        
        # Generate excerpt from first paragraph
        excerpt = ""
        for line in lines:
            if line and not line.startswith("#") and not line.startswith("Date:") and not line.startswith("Tags:"):
                excerpt = line[:150] + "..." if len(line) > 150 else line
                break
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content)
        
        # Get slug from filename
        slug = os.path.basename(file_path).replace(".md", "")
        
        # Filter by tag if specified
        if tag and tag not in tags_list:
            continue
            
        posts.append(BlogPost(
            slug=slug,
            title=title,
            content=html_content,
            excerpt=excerpt,
            date=date,
            tags=tags_list
        ))
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.date, reverse=True)
    
    return posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)