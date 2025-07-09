#!/usr/bin/env python3
"""
Create Bulgarian versions of existing English blog posts
Run this after you've translated your content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, create_blog_post, get_blog_posts

# Sample Bulgarian translations (you should replace with your actual translations)
bulgarian_translations = {
    "mastering-public-speaking": {
        "title": "Овладяване на публичното говорене: 5 театрални техники, които работят",
        "slug": "ovladyavane-publichno-govorene",
        "excerpt": "Научете как театралните техники могат да трансформират уменията ви за публично говорене и да ви помогнат да се свържете с всяка аудитория.",
        "content": """<p>Публичното говорене се нарежда сред най-големите страхове за повечето хора, често надминавайки дори страха от смърт. Но какво ще кажете, ако ви кажа, че същите техники, които професионалните актьори използват за пленяване на аудиториите, могат да трансформират способностите ви за говорене?</p>

<p>Като работя с актьори и бизнес професионалисти от над две десетилетия, открих, че театралните техники са невероятно мощни инструменти за публично говорене. Ето пет доказани метода, които ще революционизират начина, по който комуникирате.</p>

<h2>1. Силата на контрола на дишането</h2>
<p>В театъра дишането е живот. Всеки ред, всяка емоция, всеки момент на присъствие започва с правилно дишане. Същият принцип важи и за публичното говорене.</p>

<p><strong>Техника:</strong> Преди да говорите, направете три дълбоки диафрагмални вдишвания. Поставете една ръка на гърдите, една на корема. Ръката на корема трябва да се издига повече от тази на гърдите.</p>

<p><strong>Защо работи:</strong> Правилното дишане успокоява нервната ви система, дава ви гласова сила и създава естествена пауза, която привлича внимание.</p>

<h2>2. Физическо заземяване</h2>
<p>Актьорите се учат да се заземяват физически преди да стъпят на сцената. Това създава присъствие и увереност, които аудиторията може да почувства.</p>

<p><strong>Техника:</strong> Застанете с крака на ширина рамене, почувствайте връзката си със земята и си представете корени, простиращи се от краката ви в земята. Това не е само метафорично—действително променя стойката и енергията ви.</p>

<p><strong>Защо работи:</strong> Физическото заземяване намалява нервната енергия и проектира увереност. Когато се чувствате стабилни, аудиторията също усеща вашата стабилност.</p>

<h2>3. Гласово разнообразие</h2>
<p>Монотонното говорене е враг на ангажираността. Актьорите използват гласа си като музикален инструмент, създавайки ритъм, мелодия и динамика.</p>

<p><strong>Техника:</strong> Упражнявайте да казвате едно и също изречение с различни емоции—радост, тъга, вълнение, любопитство. Забележете как темпото, височината и силата на гласа ви се променят естествено.</p>

<p><strong>Защо работи:</strong> Гласовото разнообразие поддържа аудиторията ангажирана и й помага да остане свързана с вашето съобщение през цялата презентация.</p>

<h2>4. Силата на паузата</h2>
<p>В театъра тишината е също толкова важна, колкото и думите. Добре поставена пауза може да бъде по-мощна от всяка дума, която изговорите.</p>

<p><strong>Техника:</strong> След важна точка направете пауза от три пълни секунди. Пребройте ги: "Една Мисисипи, две Мисисипи, три Мисисипи." Ще ви се струва по-дълго отколкото на аудиторията ви.</p>

<p><strong>Защо работи:</strong> Паузите дават на аудиторията време да усвои информацията, създават очакване и демонстрират вашата увереност и контрол.</p>

<h2>5. Работа с характер</h2>
<p>Това не означава да станете някой друг—означава да намерите най-добрата, най-уверена версия на себе си за говорската ситуация.</p>

<p><strong>Техника:</strong> Преди да говорите, запитайте се: "Какво би направила най-уверената версия на мен точно сега?" Нагласете стойката, дишането и енергията си да отговарят на тази визия.</p>

<p><strong>Защо работи:</strong> Тази техника ви помага да влезете в по-силна версия на себе си, намалявайки тревожността и увеличавайки автентичността.</p>

<p>Започнете с една техника наведнъж, упражнявайте я последователно и постепенно добавяйте останалите. Дори професионалните актьори се вълнуват. Разликата е, че те са се научили да работят с тревожността си, а не срещу нея.</p>""",
        "tags": ["публично-говорене", "театър", "комуникация", "увереност"]
    }
    # Add more translations here as you create them
}

def create_bulgarian_versions():
    """Create Bulgarian versions of existing English posts"""
    print("Creating Bulgarian versions of blog posts...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get all English posts
        english_posts = get_blog_posts(db, language='en', published_only=False)
        
        created_count = 0
        for post in english_posts:
            if post.slug in bulgarian_translations:
                translation = bulgarian_translations[post.slug]
                
                # Create Bulgarian version
                bg_post_data = {
                    "title": translation["title"],
                    "slug": translation["slug"],
                    "excerpt": translation["excerpt"],
                    "content": translation["content"],
                    "featured_image": post.featured_image,  # Same image
                    "tags": translation.get("tags", post.tags),
                    "language": "bg",
                    "is_published": post.is_published  # Same publish status
                }
                
                try:
                    created_post = create_blog_post(db, bg_post_data)
                    print(f"✓ Created Bulgarian version: {created_post.title}")
                    created_count += 1
                except Exception as e:
                    print(f"✗ Failed to create Bulgarian version of '{post.title}': {e}")
            else:
                print(f"⚠ No translation found for: {post.title} (slug: {post.slug})")
                
        print(f"\nCreation complete! {created_count} Bulgarian posts created.")
        print(f"\nTo add more translations, edit the bulgarian_translations dictionary in this script.")
        
    except Exception as e:
        print(f"Creation failed: {e}")
        
    finally:
        db.close()

if __name__ == "__main__":
    create_bulgarian_versions()