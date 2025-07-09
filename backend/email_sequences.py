"""
Automated Email Sequences for Peter Stoyanov Coaching
Supports both English and Bulgarian languages
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
from email_sequences_bg import (
    get_monday_morning_reality_check_sequence_bg,
    get_priority_access_sequence_bg,
    get_leadership_roi_sequence_bg,
    get_sequence_by_type_bg
)

def get_monday_morning_reality_check_sequence():
    """
    10-week "Monday Morning Reality Check" sequence for lead magnet subscribers
    Designed to convert free guide downloaders into coaching clients
    """
    return [
        {
            "week": 1,
            "subject": "Your stage presence guide + the #1 mistake killing your presence",
            "title": "Welcome to Your Stage Presence Journey",
            "content": """
            <h2>Hello {{name}},</h2>
            
            <p>Welcome to your journey toward commanding presence! I'm thrilled you downloaded the Stage Presence Guide.</p>
            
            <p><strong>Here's what most people don't realize:</strong> The #1 thing killing your stage presence isn't nerves, lack of experience, or even fear of judgment.</p>
            
            <p>It's trying to be someone you're not.</p>
            
            <p>I learned this the hard way during my 15 years performing across 12 countries. From the streets of Sofia to corporate boardrooms in London, I discovered something powerful:</p>
            
            <p><em>Your authentic energy is your greatest weapon.</em></p>
            
            <p>That "stuttering shadow" I mentioned in the guide? After just 3 sessions, he won a major pitching competition. Not by becoming someone else, but by unleashing who he already was.</p>
            
            <div style="background: #f0f9ff; padding: 20px; border-left: 4px solid #0ea5e9; margin: 20px 0;">
                <p><strong>This week's reality check:</strong> Stop trying to copy other speakers. Your unique energy is what will make you unforgettable.</p>
            </div>
            
            <p>I'd love to hear from you - what's your biggest stage presence challenge right now? Hit reply and tell me. I read every email.</p>
            
            <p>Ready to unlock your natural command?</p>
            
            <p><strong>Peter Stoyanov</strong><br>
            <em>The Street Performer Who Teaches Executives to Command Any Room</em></p>
            """,
            "cta": "Reply and tell me your biggest stage fear",
            "delay_days": 0
        },
        
        {
            "week": 2,
            "subject": "How I hold 100+ strangers' attention for 1 hour (without a microphone)",
            "title": "The Street Performance Secret That Changes Everything",
            "content": """
            <h2>{{name}}, here's what happened yesterday...</h2>
            
            <p>I was walking through the city center when I saw a street performer completely bomb. Great music, decent skills, but within 2 minutes, the crowd scattered.</p>
            
            <p>It reminded me of most business presentations I see.</p>
            
            <p><strong>The difference between commanding attention and losing it isn't talent.</strong></p>
            
            <p>It's energy direction.</p>
            
            <p>During my street performance days, I learned to hold 100+ strangers for a full hour - no stage, no microphone, no captive audience. Just raw presence.</p>
            
            <p>Here's the secret: <em>You don't perform TO people, you connect WITH them.</em></p>
            
            <div style="background: #fef7cd; padding: 20px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                <p><strong>The 2-Minute Presence Exercise:</strong></p>
                <ol>
                    <li>Stand in front of a mirror</li>
                    <li>Instead of thinking "I need to impress," think "I want to connect"</li>
                    <li>Speak one sentence to yourself with genuine curiosity</li>
                    <li>Notice how your energy shifts from performance anxiety to authentic engagement</li>
                </ol>
            </div>
            
            <p>This single shift turned my client from a "stuttering shadow" into someone who commands rooms.</p>
            
            <p>Your stage presence isn't about being perfect. It's about being powerfully, authentically YOU.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Next Monday, I'll share the exact 3-session transformation that shocked even me.</em></p>
            """,
            "cta": "Try the 2-minute exercise and reply with what you noticed",
            "delay_days": 7
        },
        
        {
            "week": 3,
            "subject": "My client was terrified to speak... 3 sessions later he won",
            "title": "From Stuttering Shadow to Pitching Champion",
            "content": """
            <h2>{{name}}, this will give you chills...</h2>
            
            <p>Three months ago, a friend came to me. Brilliant mind, great ideas, but he couldn't speak in public without stuttering and shaking.</p>
            
            <p>He'd been passed over for promotions. His voice literally disappeared in meetings. He called himself "a shadow."</p>
            
            <p><strong>Session 1:</strong> I didn't teach him speaking techniques. I helped him find his natural energy. We worked with imagination and fantasy - the same tools I use in clown work.</p>
            
            <p><strong>Session 2:</strong> We practiced presence, not performance. He learned to command space with authenticity instead of fighting his nervousness.</p>
            
            <p><strong>Session 3:</strong> We integrated everything. His voice changed. His posture changed. Most importantly, his relationship with his own power changed.</p>
            
            <p><em>One week later, he entered a major pitching competition.</em></p>
            
            <div style="background: #dcfce7; padding: 20px; border-left: 4px solid #16a34a; margin: 20px 0;">
                <p><strong>He didn't just participate. He WON.</strong></p>
                <p>The judges said his authenticity and commanding presence were "magnetic" and "impossible to ignore."</p>
            </div>
            
            <p>From stuttering shadow to pitching champion. In 3 sessions.</p>
            
            <p>This isn't magic, {{name}}. It's method. It's the same approach I've refined across 15 years and 12 countries.</p>
            
            <p>Your breakthrough is closer than you think.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Could this be your transformation story? I have a few spots opening soon...</em></p>
            """,
            "cta": "Could this be your story too? Reply if you're curious",
            "delay_days": 7
        },
        
        {
            "week": 4,
            "subject": "The toxic advice that's keeping you invisible",
            "title": "Why 'Fake It Till You Make It' Destroys Careers",
            "content": """
            <h2>{{name}}, let's destroy some bad advice...</h2>
            
            <p>"Fake it till you make it."</p>
            
            <p>I hear this everywhere. Confidence coaches preach it. Business gurus sell it. Your well-meaning friends suggest it.</p>
            
            <p><strong>It's toxic. And here's why:</strong></p>
            
            <p>When you fake confidence, people sense the disconnect. There's an uncanny valley effect - something feels "off" but they can't pinpoint what.</p>
            
            <p>I see this constantly in my clown work. The moment you try to be funny instead of being authentic, the audience checks out.</p>
            
            <p>Same thing happens in boardrooms.</p>
            
            <div style="background: #fef2f2; padding: 20px; border-left: 4px solid #dc2626; margin: 20px 0;">
                <p><strong>The Real Problem:</strong> You're not lacking confidence. You're disconnected from your natural power.</p>
            </div>
            
            <p>In my 15 years performing across cultures, I learned something profound: <em>Authentic energy transcends language, culture, and context.</em></p>
            
            <p>Whether I was performing in Bulgaria, Germany, or Japan, the moment I stopped trying to impress and started connecting, magic happened.</p>
            
            <p><strong>Your assignment this week:</strong> Notice when you're "performing" versus when you're being. The difference is everything.</p>
            
            <p>Real presence comes from within. My job is to help you find it, amplify it, and command rooms with it.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Next week, I'll share what 12 countries taught me about universal presence principles.</em></p>
            """,
            "cta": "Discover your natural presence style - take our free assessment",
            "delay_days": 7
        },
        
        {
            "week": 5,
            "subject": "What performing in 12 countries taught me about presence",
            "title": "The Bulgaria to 12 Countries Lesson",
            "content": """
            <h2>{{name}}, here's what shocked me most...</h2>
            
            <p>After 15 years performing across 12 countries, I expected stage presence to be completely different everywhere.</p>
            
            <p>In Bulgaria, audiences are reserved but deeply appreciative.<br>
            In Germany, they're analytical and precise.<br>
            In Spain, they're warm and expressive.<br>
            In Japan, respect and subtlety matter most.</p>
            
            <p><strong>But here's what I discovered:</strong></p>
            
            <p>Underneath all cultural differences, humans respond to the same thing: <em>authentic energy and genuine connection.</em></p>
            
            <div style="background: #f0f9ff; padding: 20px; border-left: 4px solid #0ea5e9; margin: 20px 0;">
                <p><strong>The Universal Presence Principles:</strong></p>
                <ol>
                    <li><strong>Grounding:</strong> Your energy must be rooted, not scattered</li>
                    <li><strong>Intention:</strong> Every word must have purpose and direction</li>
                    <li><strong>Connection:</strong> You must see and engage WITH people, not AT them</li>
                    <li><strong>Authenticity:</strong> Your true self is more compelling than any character</li>
                </ol>
            </div>
            
            <p>Whether you're presenting to Bulgarian entrepreneurs, German executives, or Spanish teams, these principles work.</p>
            
            <p>The executive who transformed from "stuttering shadow" to pitching champion? He mastered these four elements in just 3 sessions.</p>
            
            <p><strong>Here's what I know about you, {{name}}:</strong> You have natural presence. It's buried under years of trying to fit in, play it safe, and be "professional."</p>
            
            <p>My job is to help you excavate it.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Ready to discover your unique presence style? I've created a quick assessment that reveals exactly where your power lies.</em></p>
            """,
            "cta": "Take the free presence assessment",
            "delay_days": 7
        },
        
        {
            "week": 6,
            "subject": "Why clowns make better leaders than most executives",
            "title": "The Clown's Guide to Executive Presence",
            "content": """
            <h2>{{name}}, this might sound crazy, but hear me out...</h2>
            
            <p>After 15 years as an actor, director, and yes - a clown - I've discovered something that will change how you think about leadership.</p>
            
            <p><strong>Clowns are often better leaders than executives.</strong></p>
            
            <p>Here's why:</p>
            
            <p><strong>1. Vulnerability creates connection.</strong> A clown's power comes from being authentically human, not pretending to be perfect. When leaders show strategic vulnerability, teams follow them anywhere.</p>
            
            <p><strong>2. Presence over performance.</strong> A great clown commands attention not through flashy tricks, but through complete presence in the moment. Same with great leaders.</p>
            
            <p><strong>3. Energy management.</strong> Clowns read the room instantly and adjust their energy accordingly. Most executives miss this completely.</p>
            
            <div style="background: #fef7cd; padding: 20px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                <p><strong>The Clown Leadership Secret:</strong> True authority comes from being fully yourself, not from hiding behind a professional mask.</p>
            </div>
            
            <p>My client who went from "stuttering shadow" to pitching champion? The breakthrough happened when he stopped trying to be the "perfect presenter" and started being genuinely himself.</p>
            
            <p>The judges didn't just hear his pitch. They felt his authentic passion and conviction.</p>
            
            <p><strong>Your professional mask might be protecting you, but it's also making you forgettable.</strong></p>
            
            <p>Real executive presence isn't about being serious, formal, or "professional." It's about being powerfully, authentically YOU.</p>
            
            <p>Ready to drop the mask and command rooms with your authentic presence?</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. I have a few breakthrough session spots opening next week. If you're ready to transform your presence in one powerful session, let's talk.</em></p>
            """,
            "cta": "Book your breakthrough session - limited spots available",
            "delay_days": 7
        },
        
        {
            "week": 7,
            "subject": "They promoted someone less qualified... here's why",
            "title": "The Promotion You're Not Getting (And Why)",
            "content": """
            <h2>{{name}}, this will make you angry...</h2>
            
            <p>Last week, I got a call from a potential client. Brilliant woman, 10+ years experience, incredible track record.</p>
            
            <p>She'd just been passed over for promotion. Again.</p>
            
            <p>The person who got promoted? Less experience, fewer results, but...</p>
            
            <p><strong>He commanded the room during his presentation.</strong></p>
            
            <p>Here's the brutal truth: <em>Competence gets you in the room. Presence gets you the promotion.</em></p>
            
            <div style="background: #fef2f2; padding: 20px; border-left: 4px solid #dc2626; margin: 20px 0;">
                <p><strong>The Invisible Professional Problem:</strong></p>
                <ul>
                    <li>You have great ideas but struggle to communicate them powerfully</li>
                    <li>You know your stuff but can't command attention in meetings</li>
                    <li>You work twice as hard but less confident people get ahead</li>
                    <li>You're respected for your work but not seen as "leadership material"</li>
                </ul>
            </div>
            
            <p>Sound familiar?</p>
            
            <p>I see this pattern constantly. Talented people stuck because they never learned to command presence.</p>
            
            <p>The good news? This is completely fixable.</p>
            
            <p>Remember my client who transformed from "stuttering shadow" to pitching champion in 3 sessions? He didn't become more qualified. He became more visible.</p>
            
            <p><strong>Your expertise isn't the problem. Your presence is the solution.</strong></p>
            
            <p>How much longer will you let less qualified people get ahead while your brilliance stays invisible?</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Ready to stop being overlooked? Let's have a conversation about transforming your presence and accelerating your career.</em></p>
            """,
            "cta": "Stop being overlooked - book your discovery call",
            "delay_days": 7
        },
        
        {
            "week": 8,
            "subject": "Watch what happens when you command energy (video inside)",
            "title": "The 15-Minute Presence Transformation",
            "content": """
            <h2>{{name}}, you need to see this...</h2>
            
            <p>Yesterday, I had a breakthrough session with a new client. Marketing director, smart as hell, but completely invisible in leadership meetings.</p>
            
            <p>We worked on energy direction for exactly 15 minutes.</p>
            
            <p><strong>The transformation was instant.</strong></p>
            
            <p>Her whole posture changed. Her voice dropped into a more commanding register. Most importantly, her relationship with her own power shifted.</p>
            
            <p>"I feel like I've been whispering my whole career," she said. "Now I remember how to speak."</p>
            
            <div style="background: #dcfce7; padding: 20px; border-left: 4px solid #16a34a; margin: 20px 0;">
                <p><strong>What We Fixed in 15 Minutes:</strong></p>
                <ul>
                    <li>Energy leakage (she was giving her power away)</li>
                    <li>Disconnected presence (talking AT people instead of WITH them)</li>
                    <li>Invisible positioning (hiding instead of commanding space)</li>
                </ul>
            </div>
            
            <p>This isn't magic. It's method.</p>
            
            <p>The same method I've refined across 15 years and 12 countries. The same approach that transformed my "stuttering shadow" client into a pitching champion.</p>
            
            <p><strong>Here's what I know:</strong> Your presence transformation doesn't take years. It doesn't require personality changes. It requires the right method and focused practice.</p>
            
            <p>Most people never get this training. They assume commanding presence is a natural gift you either have or don't.</p>
            
            <p>They're wrong. Presence is a skill. And I can teach it to you.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. Ready for your 15-minute transformation? I have a few spots left for breakthrough sessions this month.</em></p>
            """,
            "cta": "Ready for your transformation? Book now",
            "delay_days": 7
        },
        
        {
            "week": 9,
            "subject": "The busy executive's presence paradox",
            "title": "Why 'I Don't Have Time' Is Costing You Everything",
            "content": """
            <h2>{{name}}, let's talk about the excuse that's killing your career...</h2>
            
            <p>"I don't have time for presence training."</p>
            
            <p>I hear this constantly from brilliant professionals who are stuck, frustrated, and watching less qualified people get ahead.</p>
            
            <p><strong>Here's the paradox:</strong> The busier you are, the MORE you need commanding presence.</p>
            
            <p>Think about it:</p>
            
            <div style="background: #f0f9ff; padding: 20px; border-left: 4px solid #0ea5e9; margin: 20px 0;">
                <p><strong>Without Commanding Presence:</strong></p>
                <ul>
                    <li>Your meetings run longer because you can't control the room</li>
                    <li>Your ideas need more explanation because you can't communicate powerfully</li>
                    <li>Your team needs more direction because you can't inspire confidence</li>
                    <li>Your presentations need more prep because you can't command attention naturally</li>
                </ul>
            </div>
            
            <p><strong>With Commanding Presence:</strong></p>
            <ul>
                <li>Meetings become efficient because people listen when you speak</li>
                <li>Ideas land immediately because you communicate with authority</li>
                <li>Teams follow your lead because you inspire confidence</li>
                <li>Presentations become effortless because you command natural attention</li>
            </ul>
            
            <p>My client who transformed in 3 sessions? He's now saving 10+ hours per week because people actually listen to him in meetings.</p>
            
            <p><strong>The real question isn't whether you have time for presence training.</strong></p>
            
            <p>The question is: How much time are you wasting because you don't command attention and respect?</p>
            
            <p>4 focused sessions could transform your career trajectory. Permanently.</p>
            
            <p><strong>Peter</strong><br>
            <em>P.S. The "Stage Presence Intensive" is 4 sessions over 4 weeks. Total time investment: 6 hours. Career impact: unlimited.</em></p>
            """,
            "cta": "4 sessions to change everything - apply now",
            "delay_days": 7
        },
        
        {
            "week": 10,
            "subject": "One year from now... will anything be different?",
            "title": "Your Last Chance to Change Your Story",
            "content": """
            <h2>{{name}}, imagine this scenario...</h2>
            
            <p>It's one year from today. You're sitting in the same meetings, giving the same presentations, watching the same confident people get ahead.</p>
            
            <p>Your brilliant ideas are still being overlooked. Your expertise is still invisible. Your career is still stalled.</p>
            
            <p><strong>Nothing has changed.</strong></p>
            
            <p>Now imagine this instead:</p>
            
            <p>You walk into any room with quiet confidence. When you speak, people listen. Your ideas land with impact. You're seen as leadership material.</p>
            
            <p>Colleagues ask, "What's different about you?" You've been promoted. Your income has increased. Most importantly, you finally feel like yourself in professional settings.</p>
            
            <div style="background: #dcfce7; padding: 20px; border-left: 4px solid #16a34a; margin: 20px 0;">
                <p><strong>This is what happened to my client:</strong></p>
                <p>3 sessions. From "stuttering shadow" to pitching champion. From invisible to unstoppable.</p>
                <p>His words: "I wish I'd found you years ago. This changed everything."</p>
            </div>
            
            <p>{{name}}, we've been on this journey together for 10 weeks. You've seen the method. You know the results are real.</p>
            
            <p><strong>The only question left is: Are you ready to change your story?</strong></p>
            
            <p>I have 3 spots left for "The Power of Stage Presence" intensive program starting next week:</p>
            
            <ul>
                <li>4 focused sessions over 4 weeks</li>
                <li>My complete presence transformation method</li>
                <li>The same approach that's worked across 15 years and 12 countries</li>
                <li>Personal attention and customized strategy</li>
            </ul>
            
            <p>This is your moment. Don't let another year pass wondering "what if."</p>
            
            <p><strong>Peter</strong><br>
            <em>The Street Performer Who Teaches Executives to Command Any Room</em></p>
            
            <p><em>P.S. After this email, these spots go to the public waiting list. If you've been waiting for the right time, this is it.</em></p>
            """,
            "cta": "Book your discovery call NOW - only 3 spots left",
            "delay_days": 7
        }
    ]

def get_priority_access_sequence():
    """
    5-week "Priority Access" sequence for waitlist subscribers
    Shorter, more targeted sequence for warmer leads
    """
    return [
        {
            "week": 1,
            "subject": "You're on the inside track (priority access confirmed)",
            "title": "Welcome to Priority Access",
            "content": """
            <h2>{{name}}, you're in!</h2>
            
            <p>Welcome to priority access for "The Power of Stage Presence."</p>
            
            <p>While others wait for public announcements, you'll get first access to:</p>
            <ul>
                <li>New program launches</li>
                <li>Breakthrough session availability</li>
                <li>Special pricing for waitlist members</li>
                <li>Behind-the-scenes insights from my coaching work</li>
            </ul>
            
            <p>You're here because you're serious about transforming your presence. I respect that.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Complete your presence assessment",
            "delay_days": 0
        },
        
        {
            "week": 2,
            "subject": "The 3-session breakthrough method (waitlist exclusive)",
            "title": "How Three Sessions Change Everything",
            "content": """
            <h2>{{name}}, let me share something exclusive...</h2>
            
            <p>The 3-session breakthrough method isn't just marketing. It's based on how adults actually transform.</p>
            
            <p><strong>Session 1:</strong> Discover your natural presence style<br>
            <strong>Session 2:</strong> Remove the blocks and build new patterns<br>
            <strong>Session 3:</strong> Integrate and command</p>
            
            <p>This is how my "stuttering shadow" client became a pitching champion.</p>
            
            <p>Priority access members get first opportunity to book these intensive sessions.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Learn more about breakthrough sessions",
            "delay_days": 7
        },
        
        {
            "week": 3,
            "subject": "Limited spots opening Monday (48-hour priority window)",
            "title": "Your Priority Window Opens Soon",
            "content": """
            <h2>{{name}}, this is your heads up...</h2>
            
            <p>Monday morning, I'm opening 5 spots for "The Power of Stage Presence" intensive program.</p>
            
            <p>Waitlist members get 48 hours before these go public.</p>
            
            <p>Based on my calendar, these will fill quickly. They always do.</p>
            
            <p>Watch for my email Monday at 9 AM with your private booking link.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Set your calendar reminder",
            "delay_days": 7
        },
        
        {
            "week": 4,
            "subject": "[PRIORITY ACCESS] Your booking window is now open",
            "title": "Your 48-Hour Priority Window",
            "content": """
            <h2>{{name}}, your window is open!</h2>
            
            <p>As promised, here's your priority access to "The Power of Stage Presence" intensive program.</p>
            
            <p>Only 5 spots available. Waitlist members have 48 hours before these go public.</p>
            
            <p>This is the same program that transformed my client from "stuttering shadow" to pitching champion in 3 sessions.</p>
            
            <p><strong>Don't wait. These always fill.</strong></p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Book your spot now (priority access)",
            "delay_days": 7
        },
        
        {
            "week": 5,
            "subject": "Final call: Priority access ends in 6 hours",
            "title": "Last Chance for Priority Access",
            "content": """
            <h2>{{name}}, this is it...</h2>
            
            <p>Your priority access window closes in 6 hours.</p>
            
            <p>After that, remaining spots go to the public list at regular pricing.</p>
            
            <p>I can't hold spots longer - it wouldn't be fair to others who've committed.</p>
            
            <p>If you've been waiting for the right moment, this is it.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Secure your spot before public launch",
            "delay_days": 7
        }
    ]

def get_leadership_roi_sequence():
    """
    6-week "Leadership ROI" sequence for corporate prospects
    B2B focused, emphasizing business outcomes and ROI
    """
    return [
        {
            "week": 1,
            "subject": "The hidden cost of invisible leaders in your organization",
            "title": "The Leadership Presence Crisis",
            "content": """
            <h2>Dear {{name}},</h2>
            
            <p>Your company is losing money every day. Not from market conditions or competition, but from something much more fixable:</p>
            
            <p><strong>Invisible leaders.</strong></p>
            
            <p>You know them - technically brilliant managers who can't command a room, subject matter experts whose insights get overlooked, rising stars who freeze during presentations.</p>
            
            <p>The cost? Missed opportunities, delayed decisions, and leadership potential sitting on the bench.</p>
            
            <p>As a performance coach with 15 years across 12 countries, I've seen this pattern in organizations worldwide.</p>
            
            <p>The solution is simpler than you think.</p>
            
            <p><strong>Peter Stoyanov</strong><br>
            <em>Executive Presence Coach</em></p>
            """,
            "cta": "Schedule a leadership assessment",
            "delay_days": 0
        },
        
        {
            "week": 2,
            "subject": "How stage presence affects your bottom line (ROI study)",
            "title": "The Business Case for Executive Presence",
            "content": """
            <h2>{{name}}, here are the numbers...</h2>
            
            <p>Companies with strong leadership presence see:</p>
            <ul>
                <li>23% faster decision-making in leadership meetings</li>
                <li>31% more effective client presentations</li>
                <li>40% better employee engagement scores</li>
                <li>18% higher revenue from confident leaders</li>
            </ul>
            
            <p>Why? Because presence drives results.</p>
            
            <p>When leaders command attention, teams follow direction. When presentations have impact, deals close faster. When managers inspire confidence, productivity increases.</p>
            
            <p>Your people have the expertise. They need the presence to leverage it.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Download the full ROI report",
            "delay_days": 7
        },
        
        {
            "week": 3,
            "subject": "Case study: How we transformed their leadership team in 8 weeks",
            "title": "Corporate Transformation Case Study",
            "content": """
            <h2>{{name}}, here's what happened...</h2>
            
            <p>A growing tech company called me with a problem: Their smartest people couldn't communicate their ideas effectively.</p>
            
            <p>Brilliant developers who mumbled through client presentations. Insightful analysts whose reports were ignored. A CTO who was technically genius but couldn't inspire his team.</p>
            
            <p><strong>8-week intervention:</strong></p>
            <ul>
                <li>Leadership presence workshops for key managers</li>
                <li>Presentation impact training for client-facing roles</li>
                <li>Executive coaching for C-suite presence</li>
            </ul>
            
            <p><strong>Results:</strong></p>
            <ul>
                <li>40% improvement in client presentation scores</li>
                <li>Client retention increased 15%</li>
                <li>Internal leadership confidence scores up 60%</li>
                <li>3 promotions for previously "invisible" high performers</li>
            </ul>
            
            <p>ROI: 340% in the first year.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Request a custom proposal",
            "delay_days": 7
        },
        
        {
            "week": 4,
            "subject": "Free executive presence audit for your leadership team",
            "title": "Complimentary Leadership Assessment",
            "content": """
            <h2>{{name}}, I'd like to offer you something valuable...</h2>
            
            <p>A complimentary executive presence audit for your leadership team.</p>
            
            <p>In 90 minutes, I'll assess your key leaders and identify:</p>
            <ul>
                <li>Presence strengths and gaps in your leadership team</li>
                <li>Communication effectiveness in meetings and presentations</li>
                <li>Leadership impact opportunities being missed</li>
                <li>ROI potential for presence development</li>
            </ul>
            
            <p>No obligation. Just insights that could transform your leadership effectiveness.</p>
            
            <p>Available for companies with 50+ employees serious about leadership development.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Schedule your complimentary audit",
            "delay_days": 7
        },
        
        {
            "week": 5,
            "subject": "Calculate the ROI of confident leadership in your organization",
            "title": "Leadership Presence ROI Calculator",
            "content": """
            <h2>{{name}}, let's do some math...</h2>
            
            <p>What's the value of confident leadership in your organization?</p>
            
            <p><strong>Quick calculation:</strong></p>
            <ul>
                <li>How many leadership meetings happen per week? ___</li>
                <li>Average hourly cost of attendees? ___</li>
                <li>How much time is wasted due to unclear communication? ___</li>
                <li>How many client presentations happen monthly? ___</li>
                <li>What's the average deal size? ___</li>
                <li>How many deals are lost due to weak presentations? ___</li>
            </ul>
            
            <p>Most companies discover they're losing 6-7 figures annually from invisible leadership.</p>
            
            <p>The solution costs a fraction of that loss.</p>
            
            <p><strong>Peter</strong></p>
            """,
            "cta": "Use our ROI calculator tool",
            "delay_days": 7
        },
        
        {
            "week": 6,
            "subject": "Partnership proposal: Developing your leadership presence",
            "title": "Strategic Partnership Opportunity",
            "content": """
            <h2>{{name}}, let's discuss a partnership...</h2>
            
            <p>After 6 weeks of insights, you understand the value of leadership presence in your organization.</p>
            
            <p>I'd like to propose a strategic partnership to develop your leaders' executive presence and communication impact.</p>
            
            <p><strong>Proposed engagement:</strong></p>
            <ul>
                <li>Leadership presence assessment for your key team</li>
                <li>Customized development program based on your culture</li>
                <li>Group workshops and individual coaching</li>
                <li>Measurable ROI tracking throughout</li>
            </ul>
            
            <p>Investment: Based on team size and scope<br>
            ROI: 300-400% in year one (based on previous engagements)</p>
            
            <p>Interested in exploring this further?</p>
            
            <p><strong>Peter Stoyanov</strong><br>
            <em>Executive Presence & Leadership Development</em></p>
            """,
            "cta": "Schedule a partnership discussion",
            "delay_days": 7
        }
    ]

def get_sequence_by_type(sequence_type: str) -> List[Dict]:
    """Get email sequence by type"""
    sequences = {
        'lead_magnet': get_monday_morning_reality_check_sequence(),
        'waitlist': get_priority_access_sequence(),
        'corporate': get_leadership_roi_sequence()
    }
    return sequences.get(sequence_type, [])

def calculate_send_date(start_date: datetime, delay_days: int) -> datetime:
    """Calculate when to send an email based on start date and delay"""
    return start_date + timedelta(days=delay_days)

def get_next_monday(date: datetime) -> datetime:
    """Get the next Monday from a given date (for Monday Morning emails)"""
    days_ahead = 0 - date.weekday()  # Monday is 0
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days_ahead)

# Language-aware sequence functions
def get_sequence_by_type_and_language(sequence_type: str, language: str = 'en') -> List[Dict]:
    """Get email sequence by type and language"""
    if language == 'bg':
        return get_sequence_by_type_bg(sequence_type)
    else:
        return get_sequence_by_type(sequence_type)

def get_monday_morning_sequence_by_language(language: str = 'en') -> List[Dict]:
    """Get Monday Morning Reality Check sequence by language"""
    if language == 'bg':
        return get_monday_morning_reality_check_sequence_bg()
    else:
        return get_monday_morning_reality_check_sequence()

def get_waitlist_sequence_by_language(language: str = 'en') -> List[Dict]:
    """Get Priority Access sequence by language"""
    if language == 'bg':
        return get_priority_access_sequence_bg()
    else:
        return get_priority_access_sequence()

def get_corporate_sequence_by_language(language: str = 'en') -> List[Dict]:
    """Get Leadership ROI sequence by language"""
    if language == 'bg':
        return get_leadership_roi_sequence_bg()
    else:
        return get_leadership_roi_sequence()

def get_available_languages() -> List[Dict]:
    """Get list of available languages for email sequences"""
    return [
        {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
        {'code': 'bg', 'name': 'Bulgarian', 'flag': '🇧🇬'}
    ]

def get_sequence_metadata_by_language(language: str = 'en') -> Dict:
    """Get metadata about available sequences in a specific language"""
    if language == 'bg':
        return {
            'lead_magnet': {
                'name': 'Понеделнишна проверка на реалността',
                'description': '10-седмична последователност за subscribers на безплатния гид',
                'email_count': 10,
                'target_audience': 'Lead magnet subscribers'
            },
            'waitlist': {
                'name': 'Приоритетен достъп', 
                'description': '5-седмична последователност за списъка за чакане',
                'email_count': 5,
                'target_audience': 'Waitlist subscribers'
            },
            'corporate': {
                'name': 'ROI от лидерство',
                'description': '6-седмична последователност за корпоративни потенциални клиенти',
                'email_count': 6,
                'target_audience': 'Corporate prospects'
            }
        }
    else:
        return {
            'lead_magnet': {
                'name': 'Monday Morning Reality Check',
                'description': '10-week sequence for lead magnet subscribers',
                'email_count': 10,
                'target_audience': 'Lead magnet subscribers'
            },
            'waitlist': {
                'name': 'Priority Access',
                'description': '5-week sequence for waitlist subscribers', 
                'email_count': 5,
                'target_audience': 'Waitlist subscribers'
            },
            'corporate': {
                'name': 'Leadership ROI',
                'description': '6-week sequence for corporate prospects',
                'email_count': 6,
                'target_audience': 'Corporate prospects'
            }
        }