#!/usr/bin/env python3

"""
Migration script to populate the database with hardcoded blog posts from the frontend.
This script extracts the blog content from the frontend and saves it to the backend database.
"""

import os
import sys
from datetime import datetime
from database import SessionLocal, engine
from models import BlogPost, Base

# Blog posts data extracted from frontend
BLOG_POSTS_DATA = [
    {
        "slug": "mastering-public-speaking",
        "title": "Mastering Public Speaking: 5 Theater Techniques That Work",
        "excerpt": "Learn how theater techniques can transform your public speaking skills and help you connect with any audience.",
        "content": """
        <p>Public speaking is often cited as one of the most common fears people have. Yet, with the right techniques, anyone can become a confident and engaging speaker. As an actor and coach with over 20 years of experience, I've found that theater techniques offer powerful tools for improving public speaking skills.</p>
        
        <h2>1. The Power of Breath Control</h2>
        <p>Actors understand that breath is the foundation of vocal projection and emotional control. Before going on stage, practice deep diaphragmatic breathing: inhale slowly through your nose for a count of four, hold for two, and exhale through your mouth for six. This technique calms nerves and provides the breath support needed for clear, powerful speech.</p>
        
        <h2>2. Physical Grounding</h2>
        <p>Theater performers know that stance and posture affect both how you feel and how others perceive you. Stand with your feet shoulder-width apart, weight evenly distributed. Feel your connection to the ground. This "power stance" increases confidence and projects authority to your audience.</p>
        
        <h2>3. Vocal Variety</h2>
        <p>Monotone delivery will lose your audience quickly. Practice varying your pitch, pace, and volume. Try reading the same sentence as a question, an excited statement, and a solemn declaration. This flexibility makes your speech more engaging and helps emphasize key points.</p>
        
        <h2>4. The Pause</h2>
        <p>One of the most powerful tools in theater is the strategic pause. Many speakers rush through their material, but well-placed pauses give the audience time to absorb important points and create dramatic emphasis. Don't be afraid of silence – it's often more powerful than words.</p>
        
        <h2>5. Character Work</h2>
        <p>When nervous, try thinking of your presentation as a performance. Create a slightly more confident "character" version of yourself. This mental shift can help separate personal anxiety from the task at hand, allowing you to present with greater ease.</p>
        
        <p>These theater-based techniques have helped countless professionals transform their public speaking abilities. Remember that like any skill, improvement comes with practice. Start incorporating these approaches into your presentations, and you'll soon find yourself speaking with greater confidence and impact.</p>
        """,
        "tags": ["public-speaking", "theater"],
        "language": "en",
        "is_published": True,
        "published_at": datetime(2023, 5, 15)
    },
    {
        "slug": "voice-projection-tips",
        "title": "Voice Projection Tips for Effective Communication",
        "excerpt": "Discover how to use your voice effectively to command attention and convey your message with impact.",
        "content": """
        <p>Your voice is one of your most powerful tools for communication. Whether you're speaking to a small group or addressing a large audience, how you use your voice can make the difference between engaging listeners and losing their attention.</p>
        
        <h2>Understanding Voice Projection</h2>
        <p>Voice projection isn't about shouting—it's about producing a clear, resonant sound that carries well. It involves proper breath support, vocal placement, and articulation.</p>
        
        <h2>Breath Support: The Foundation</h2>
        <p>All good voice work begins with proper breathing. Practice diaphragmatic breathing by placing your hand on your abdomen and ensuring it expands when you inhale. This provides the air support needed for strong projection.</p>
        
        <h2>Finding Resonance</h2>
        <p>To add richness to your voice, focus on creating resonance in your chest, throat, and facial cavities. Try humming at different pitches to feel where your voice resonates most naturally.</p>
        
        <h2>Articulation Exercises</h2>
        <p>Clear articulation ensures your words are understood. Practice tongue twisters daily to improve the precision of your consonants and the clarity of your vowels.</p>
        
        <h2>Varying Your Delivery</h2>
        <p>A dynamic voice keeps listeners engaged. Experiment with changing your pace, pitch, and volume to emphasize important points and create interest.</p>
        
        <h2>Practical Tips for Daily Practice</h2>
        <p>Spend 10 minutes each day on vocal exercises. Record yourself speaking and listen critically. Practice projecting to the back of a room without straining your voice.</p>
        
        <p>Remember, a well-projected voice communicates confidence and authority. With consistent practice of these techniques, you'll develop a voice that commands attention and effectively conveys your message.</p>
        """,
        "tags": ["voice", "communication"],
        "language": "en", 
        "is_published": True,
        "published_at": datetime(2023, 4, 22)
    },
    {
        "slug": "body-language-secrets",
        "title": "Body Language Secrets from Professional Actors",
        "excerpt": "Explore how professional actors use body language to enhance their performances and how you can apply these techniques.",
        "content": """
        <p>Body language is a powerful form of communication that can significantly impact how others perceive and respond to you. Professional actors spend years mastering the art of physical expression, and their techniques can be incredibly valuable for anyone looking to improve their communication skills.</p>
        
        <h2>The Foundation: Posture and Alignment</h2>
        <p>Actors know that everything starts with proper posture. Stand tall with your shoulders back, but not rigidly. Imagine a string pulling you up from the crown of your head. This aligned posture not only looks confident but actually helps you feel more confident.</p>
        
        <h2>Mirroring and Matching</h2>
        <p>One of the most powerful techniques actors use is subtle mirroring. When you slightly mirror someone's posture or gestures, you create an unconscious connection. This builds rapport and makes others feel more comfortable with you.</p>
        
        <h2>Intentional Gestures</h2>
        <p>Every movement an actor makes on stage has purpose. Apply this principle to your daily communication by making your gestures deliberate and meaningful. Avoid fidgeting or repetitive movements that can distract from your message.</p>
        
        <h2>The Power of Eye Contact</h2>
        <p>Actors understand that eyes are windows to emotion. Practice maintaining appropriate eye contact – not staring, but engaging. Look at one person for a complete thought before shifting to another.</p>
        
        <h2>Facial Expression Awareness</h2>
        <p>Your face communicates as much as your words. Practice expressing different emotions with your facial expressions. A genuine smile, raised eyebrows for emphasis, or a thoughtful expression can all enhance your message.</p>
        
        <h2>Breathing and Presence</h2>
        <p>Actors use breath work to ground themselves and project presence. Deep, controlled breathing not only calms nerves but also creates a sense of authority and calm that others find compelling.</p>
        
        <p>By incorporating these actor-tested techniques into your daily interactions, you'll develop a more commanding presence and become a more effective communicator. Remember, consistency is key – these skills improve with regular practice.</p>
        """,
        "tags": ["body-language", "acting"],
        "language": "en",
        "is_published": True,
        "published_at": datetime(2023, 3, 10)
    },
    {
        "slug": "overcoming-stage-fright",
        "title": "Overcoming Stage Fright: A Step-by-Step Guide",
        "excerpt": "Learn practical techniques to manage anxiety and perform confidently in front of any audience.",
        "content": """
        <p>Stage fright is a common experience that affects everyone from seasoned performers to first-time speakers. The key to overcoming it lies not in eliminating the nerves completely, but in learning to manage and channel them effectively.</p>
        
        <h2>Understanding Stage Fright</h2>
        <p>Stage fright is your body's natural response to a perceived threat. Your sympathetic nervous system kicks in, flooding your body with adrenaline. Understanding this physiological response is the first step to managing it.</p>
        
        <h2>Step 1: Preparation is Key</h2>
        <p>The better prepared you are, the more confident you'll feel. Know your material inside and out. Practice until you can deliver your content even when distracted. This preparation becomes your safety net.</p>
        
        <h2>Step 2: Breathing Techniques</h2>
        <p>When anxious, our breathing becomes shallow and rapid. Combat this with the 4-7-8 technique: inhale for 4 counts, hold for 7, exhale for 8. This activates your parasympathetic nervous system and promotes calm.</p>
        
        <h2>Step 3: Progressive Muscle Relaxation</h2>
        <p>Tension builds up in our muscles when we're nervous. Practice tensing and then releasing each muscle group, starting from your toes and working up to your head. This helps release physical tension.</p>
        
        <h2>Step 4: Visualization</h2>
        <p>Spend time visualizing yourself delivering a successful performance. See yourself confident, engaged, and connecting with your audience. This mental rehearsal helps program your subconscious for success.</p>
        
        <h2>Step 5: Reframe Your Mindset</h2>
        <p>Instead of viewing the audience as judges, see them as allies who want you to succeed. Remember that they're there to hear what you have to say, not to criticize you.</p>
        
        <h2>Step 6: Use Your Nervous Energy</h2>
        <p>Some nervousness can actually improve performance by keeping you sharp and focused. Channel this energy into enthusiasm and passion for your subject.</p>
        
        <p>Remember, even experienced performers get nervous. The difference is that they've learned to work with their nerves rather than against them. With practice and patience, you can develop the same confidence.</p>
        """,
        "tags": ["anxiety", "performance"],
        "language": "en",
        "is_published": True,
        "published_at": datetime(2023, 2, 18)
    },
    {
        "slug": "storytelling-for-business",
        "title": "Storytelling for Business: Engage Your Audience",
        "excerpt": "Discover how to use storytelling techniques to make your business presentations more engaging and memorable.",
        "content": """
        <p>In the world of business, facts and figures are important, but stories are what move people to action. Storytelling isn't just for entertainment – it's a powerful tool that can transform your business presentations and help you connect with your audience on a deeper level.</p>
        
        <h2>Why Stories Work in Business</h2>
        <p>Stories engage multiple areas of the brain simultaneously. While data activates only the language processing centers, stories activate the sensory cortex, motor cortex, and emotional centers. This makes your message more memorable and persuasive.</p>
        
        <h2>The Classic Story Structure</h2>
        <p>Every compelling story follows a basic structure: setup, conflict, and resolution. In business contexts, this translates to: situation, challenge, and solution. This structure keeps your audience engaged and makes your message clear.</p>
        
        <h2>Types of Business Stories</h2>
        <p>Different types of stories serve different purposes. Origin stories build credibility, customer success stories provide proof, and vision stories inspire action. Choose the right type of story for your objective.</p>
        
        <h2>Making Your Story Relevant</h2>
        <p>The best business stories are those your audience can relate to. Use characters and situations that mirror your audience's experiences. This creates emotional connection and makes your message more impactful.</p>
        
        <h2>Incorporating Sensory Details</h2>
        <p>Don't just tell your audience what happened – help them experience it. Use sensory details to make your story vivid. What did people see, hear, feel? These details make stories more engaging and memorable.</p>
        
        <h2>The Power of Vulnerability</h2>
        <p>Sharing appropriate challenges and failures makes you more relatable and trustworthy. People connect with human stories that include both struggles and triumphs.</p>
        
        <h2>Practice and Refinement</h2>
        <p>Like any skill, storytelling improves with practice. Start by collecting stories from your professional experience. Refine them by practicing with colleagues and noting what resonates with different audiences.</p>
        
        <p>Remember, every presentation is an opportunity to tell a story. Whether you're pitching a product, presenting quarterly results, or motivating a team, weaving narrative elements into your content will make you a more effective communicator.</p>
        """,
        "tags": ["storytelling", "business"],
        "language": "en",
        "is_published": True,
        "published_at": datetime(2023, 1, 25)
    },
    {
        "slug": "breathing-techniques",
        "title": "Breathing Techniques for Better Speech and Presence",
        "excerpt": "Master the art of breathing to improve your vocal quality, reduce stress, and enhance your overall presence.",
        "content": """
        <p>Breathing is the foundation of all vocal work and personal presence. Most people take breathing for granted, but learning to breathe properly can transform your voice, reduce anxiety, and dramatically improve your communication effectiveness.</p>
        
        <h2>Understanding Proper Breathing</h2>
        <p>Many people breathe shallowly, using only the upper chest. Proper breathing involves the diaphragm – the large muscle beneath your lungs. This deeper breathing provides better vocal support and helps regulate your nervous system.</p>
        
        <h2>The Diaphragmatic Breathing Technique</h2>
        <p>Place one hand on your chest and one on your abdomen. When you breathe correctly, the lower hand should move more than the upper hand. Practice this until it becomes natural.</p>
        
        <h2>Breathing for Vocal Power</h2>
        <p>Your voice is created by air passing through your vocal cords. The more steady and controlled your airflow, the better your voice will sound. Practice speaking on one breath, gradually increasing the length of your phrases.</p>
        
        <h2>Breathing for Anxiety Management</h2>
        <p>When we're nervous, our breathing becomes shallow and rapid. This can actually increase anxiety. Learning to control your breathing helps activate your body's relaxation response.</p>
        
        <h2>The 4-7-8 Technique</h2>
        <p>This powerful technique involves inhaling for 4 counts, holding for 7, and exhaling for 8. It's particularly effective for managing performance anxiety and can be done anywhere.</p>
        
        <h2>Box Breathing</h2>
        <p>Used by military professionals and athletes, box breathing involves equal counts for inhaling, holding, exhaling, and holding again. Start with 4 counts for each phase and gradually increase.</p>
        
        <h2>Breathing Exercises for Daily Practice</h2>
        <p>Spend 5-10 minutes daily practicing breathing exercises. This can be done while commuting, before important meetings, or as part of your morning routine. Consistency is more important than duration.</p>
        
        <h2>Breathing and Presence</h2>
        <p>Proper breathing doesn't just improve your voice – it enhances your overall presence. When you breathe deeply and calmly, you appear more confident and centered, which influences how others perceive and respond to you.</p>
        
        <p>Remember, breathing is both automatic and controllable. By taking conscious control of your breathing, you can improve your voice, manage stress, and project greater confidence in all your interactions.</p>
        """,
        "tags": ["breathing", "voice"],
        "language": "en",
        "is_published": True,
        "published_at": datetime(2022, 12, 12)
    }
]

def migrate_blog_posts():
    """Migrate hardcoded blog posts to the database"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if blog posts already exist
        existing_posts = db.query(BlogPost).count()
        if existing_posts > 0:
            print(f"Database already contains {existing_posts} blog posts.")
            print("Deleting existing posts and re-importing...")
            
            # Delete existing posts
            db.query(BlogPost).delete()
            db.commit()
            print("Existing blog posts deleted.")
        
        # Insert new blog posts
        for post_data in BLOG_POSTS_DATA:
            blog_post = BlogPost(**post_data)
            db.add(blog_post)
        
        db.commit()
        print(f"Successfully migrated {len(BLOG_POSTS_DATA)} blog posts to the database.")
        
        # Verify the migration
        total_posts = db.query(BlogPost).count()
        print(f"Total blog posts in database: {total_posts}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting blog post migration...")
    migrate_blog_posts()
    print("Migration completed successfully!")