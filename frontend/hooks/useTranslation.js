import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

// Translation data
const translations = {
  bg: {
    // Navigation
    'nav.home': 'Начало',
    'nav.about': 'За мен',
    'nav.corporate': 'Корпоративни',
    'nav.blog': 'Блог',
    'nav.waitlist': 'Запишете се',
    
    // Home page
    'home.title': 'Професионален коучинг за комуникация и лидерство',
    'home.description': 'Преобразете уменията си за комуникация и отключете лидерския си потенциал с над 20 години професионален опит в коучинг.',
    'home.hero.title': 'Професионален коучинг за комуникация и лидерство',
    'home.hero.subtitle': 'Превърнете страха си в сила. Преобразете присъствието си. Станете лидера, който сте призвани да бъдете.',
    'home.hero.cta': 'Започнете трансформацията си',
    'home.hero.meetPetar': 'Запознайте се с Петър',
    'home.hero.stats.experience': 'години опит',
    'home.hero.stats.countries': 'страни',
    
    // Video section
    'home.video.title': 'Запознайте се с Петър Стоянов',
    'home.video.description': 'Открийте историята зад методологията и научете как мога да ви помогна да постигнете целите си за комуникация.',
    'home.video.comingSoon': 'Видеото идва скоро',
    'home.video.preview': 'Предварителен преглед на личния ми подход',
    'home.video.quote': 'Комуникацията не е само за думите - тя е за създаване на връзка и оставяне на впечатление.',
    'home.video.credentials': 'Експерт по комуникация и лидерство',
    
    // Methodology section
    'home.methodology.title': 'Моята уникална методология',
    'home.methodology.subtitle': 'Проверен подход, базиран на десетилетия опит в театъра, коучинга и корпоративния свят',
    'home.methodology.method1.title': 'Присъствие в момента',
    'home.methodology.method1.description': 'Научете се да заповядвате вниманието чрез истинско присъствие и осъзнатост на момента.',
    'home.methodology.method2.title': 'Гласов контрол',
    'home.methodology.method2.description': 'Овладейте силата на гласа си - от проекция до тон и темпо.',
    'home.methodology.method3.title': 'Енергия и действие',
    'home.methodology.method3.description': 'Трансформирайте нервността в енергия, която привлича и вдъхновява аудиторията.',
    
    // Features section
    'home.features.title': 'Какво ще научите',
    'home.features.subtitle': 'Цялостна програма за развитие на комуникационните и лидерски умения',
    'home.features.feature1.title': 'Сценично присъствие',
    'home.features.feature1.description': 'Изградете магнетично присъствие, което привлича и задържа вниманието.',
    'home.features.feature2.title': 'Гласови техники',
    'home.features.feature2.description': 'Овладейте проекция, артикулация и вокален контрол за максимално въздействие.',
    'home.features.feature3.title': 'Език на тялото',
    'home.features.feature3.description': 'Научете се да използвате позата, жестовете и движението си убедително.',
    'home.features.feature4.title': 'Работа с камера',
    'home.features.feature4.description': 'Станете естествени и убедителни във виртуални среди и видео комуникация.',
    'home.features.feature5.title': 'Обръщение към аудитория',
    'home.features.feature5.description': 'Изградете връзка със зрителите и управлявайте енергията на групата.',
    'home.features.feature6.title': 'Импровизационни умения',
    'home.features.feature6.description': 'Развийте способността да мислите бързо и да се адаптирате в неочаквани ситуации.',
    
    // Testimonials section - adding all 10 testimonials
    'home.testimonials.title': 'Какво споделят клиентите ми',
    'home.testimonials.subtitle': 'Истински истории за трансформация от хора, които са преминали този път',
    'home.testimonials.testimonial1.name': 'Мария Георгиева',
    'home.testimonials.testimonial1.position': 'Изпълнителен директор, ТехСофт България',
    'home.testimonials.testimonial1.text': 'Работата с Петър промени не само начина, по който презентирам, но и цялото ми самочувствие като лидер. За 6 месеца станах по-убедителна и уверена в себе си.',
    'home.testimonials.testimonial2.name': 'Димитър Петров',
    'home.testimonials.testimonial2.position': 'Мениджър продажби, ГлобалКорп',
    'home.testimonials.testimonial2.text': 'Страхувах се от публичното говорене цял живот. Сега водя презентации пред стотици хора и се чувствам естествено и уверено.',
    'home.testimonials.testimonial3.name': 'Елена Стоева',
    'home.testimonials.testimonial3.position': 'Основател, Инова Консулт',
    'home.testimonials.testimonial3.text': 'Техниките на Петър ми помогнаха да намеря своя автентичен глас като предприемач. Клиентите ме възприемат като по-сериозен партньор.',
    'home.testimonials.testimonial4.name': 'Александър Иванов',
    'home.testimonials.testimonial4.position': 'Старши програмист, ТехГигант',
    'home.testimonials.testimonial4.text': 'Като интроверт мислех, че никога няма да мога да презентирам добре. Методите на Петър ми показаха, че мога да съм убедителен по свой начин.',
    'home.testimonials.testimonial5.name': 'Виолета Димитрова',
    'home.testimonials.testimonial5.position': 'HR директор, МегаКомпани',
    'home.testimonials.testimonial5.text': 'Обучението промени не само професионалния ми живот, но и личните ми отношения. Комуникирам по-ясно и с повече емпатия.',
    'home.testimonials.testimonial6.name': 'Георги Николов',
    'home.testimonials.testimonial6.position': 'Стартъп основател',
    'home.testimonials.testimonial6.text': 'Благодарение на Петър успях да привлека инвеститори за стартъпа си. Презентационните ми умения се подобриха драстично.',
    'home.testimonials.testimonial7.name': 'Надя Павлова',
    'home.testimonials.testimonial7.position': 'Медицински представител',
    'home.testimonials.testimonial7.text': 'Научих се да объркам лекарите със страст и експертиза. Продажбите ми се увеличиха с 40% след обучението.',
    'home.testimonials.testimonial8.name': 'Стефан Михайлов',
    'home.testimonials.testimonial8.position': 'Мениджър проекти, БигТех',
    'home.testimonials.testimonial8.text': 'Сега мога да водя трудни разговори с клиенти без да се притеснявам. Уверността ми като лидер се увеличи значително.',
    'home.testimonials.testimonial9.name': 'Цветелина Атанасова',
    'home.testimonials.testimonial9.position': 'Консултант по маркетинг',
    'home.testimonials.testimonial9.text': 'Работата с Петър ми даде инструментите да се изразявам по-ясно и убедително пред клиентите. Бизнесът ми се подобри.',
    'home.testimonials.testimonial10.name': 'Борис Христов',
    'home.testimonials.testimonial10.position': 'Финансов анализатор',
    'home.testimonials.testimonial10.text': 'Никога не съм си мислил, че мога да държа презентация без да треперя. Сега това е естествена част от работата ми.',
    
    // Transformation section
    'home.transformation.title': 'Вашата трансформация',
    'home.transformation.subtitle': 'От страх и несигурност към увереност и харизма',
    'home.transformation.before.title': 'ПРЕДИ',
    'home.transformation.before.item1': 'Страх от публичното говорене',
    'home.transformation.before.item2': 'Нервност пред камера',
    'home.transformation.before.item3': 'Липса на присъствие',
    'home.transformation.before.item4': 'Неуверена комуникация',
    'home.transformation.after.title': 'СЛЕД',
    'home.transformation.after.item1': 'Уверено публично говорене',
    'home.transformation.after.item2': 'Естественост пред камера',
    'home.transformation.after.item3': 'Силно присъствие и харизма',
    'home.transformation.after.item4': 'Ясна и убедителна комуникация',
    'home.transformation.cta.title': 'Готови ли сте за вашата трансформация?',
    'home.transformation.cta.button': 'Започнете своето пътешествие',
    
    // Lead magnet section
    'home.leadMagnetSection.title': 'Изтеглете безплатното ръководство',
    'home.leadMagnetSection.description': 'Получете достъп до моето ексклузивно ръководство с практически упражнения за подобряване на дишането, гласа и говоренето.',
    'home.leadMagnetSection.benefits': [
      'Техники за контрол на дишането',
      'Гласови упражнения за яснота',
      'Практически съвети за говорене',
      'Методи за преодоляване на треми'
    ],
    'home.leadMagnetSection.guideLabel': 'Ръководство',
    'home.leadMagnetSection.pdfLabel': 'PDF Формат',
    'home.leadMagnetSection.freeLabel': 'БЕЗПЛАТНО',
    
    // Lead magnet form
    'home.leadMagnet.emailPlaceholder': 'Въведете вашия имейл адрес',
    'home.leadMagnet.downloadButton': 'Изтеглете безплатно',
    'home.leadMagnet.sending': 'Изпращане...',
    'home.leadMagnet.joinText': 'Присъединете се към хиляди професионалисти, които вече подобряват уменията си',
    'home.leadMagnet.errors.emailRequired': 'Моля, въведете валиден имейл адрес',
    'home.leadMagnet.errors.submitError': 'Възникна грешка при изпращането',
    'home.leadMagnet.errors.networkError': 'Грешка в мрежата. Моля, опитайте отново.',
    
    // CTA section
    'home.cta.title': 'Готови ли сте да започнете?',
    'home.cta.description': 'Присъединете се към стотиците професионалисти, които вече преобразиха уменията си за комуникация и лидерство.',
    'home.cta.button': 'Запишете се сега',
    'home.cta.corporateButton': 'Корпоративно обучение',
    
    // Services
    'services.title': 'Професионални коучинг услуги',
    'services.individual.title': 'Индивидуален коучинг',
    'services.individual.description': 'Личностно развитие за съвършенство в комуникацията и лидерско присъствие.',
    'services.corporate.title': 'Корпоративно обучение',
    'services.corporate.description': 'Семинари за екипи и програми за развитие на организационната комуникация.',
    'services.leadership.title': 'Развитие на лидерството',
    'services.leadership.description': 'Изградете увереност, присъствие и комуникационни умения за ефективно лидерство.',
    
    // Footer
    'footer.description': 'Трансформиране на комуникацията чрез театрални техники, работа с дишането и автентично присъствие.',
    'footer.contact': 'Контакт',
    'footer.followUs': 'Последвай ни',
    'footer.newsletter': 'Бюлетин',
    'footer.newsletterDescription': 'Бъди в крак новините от нас.',
    'footer.subscribe': 'Абонирай се',
    'footer.allRightsReserved': 'Всички права запазени',
    'footer.privacyPolicy': 'Политика за поверителност',
    'footer.termsOfService': 'Условия за ползване',
    'footer.copyright': '© 2024 Peter Stoyanov Coaching',
    'footer.tagline': 'Професионално развитие на комуникацията и лидерството',
    
    // Contact
    'contact.title': 'Свържете се с Peter Stoyanov',
    'contact.ready': 'Готови ли сте да преобразите уменията си за комуникация и лидерство?',
    'contact.email': 'Имейл',
    'contact.services': 'Услуги',
    'contact.approach': 'За моя подход',
    'contact.back': '← Обратно към началото',
    
    // About
    'about.title': 'За мен',
    'about.hero.title': 'Здравейте, аз съм Peter Stoyanov',
    'about.hero.subtitle': 'Коуч за комуникация и лидерство с над 20 години опит',
    'about.journey.title': 'Моето пътешествие',
    'about.journey.description': 'От театралната сцена до корпоративните стаи за съвещания, моят път ме е научил, че истинското лидерство започва с автентична комуникация.',
    'about.expertise.title': 'Моята експертиза',
    'about.approach.title': 'Моят подход',
    
    // Corporate
    'corporate.title': 'Корпоративно обучение',
    'corporate.hero.title': 'Преобразете вашия екип чрез мощна комуникация',
    'corporate.hero.subtitle': 'Персонализирани програми за обучение, които изграждат увереност и подобряват резултатите',
    'corporate.programs.title': 'Програми за обучение',
    'corporate.contact.title': 'Започнете днес',
    'corporate.contact.description': 'Свържете се с нас за персонализирана консултация и предложение за вашата организация.',
    
    // Waitlist
    'waitlist.title': 'Станете част от бъдещето на комуникацията',
    'waitlist.description': 'Ексклузивен курс за присъствие и комуникационни умения',
    'waitlist.hero.stats.limited': 'Ограничени места',
    'waitlist.hero.stats.spotsAvailable': 'Само 20 места налични',
    'waitlist.hero.stats.early': 'Ранен достъп',
    'waitlist.hero.stats.birdPricing': 'Специална цена за първите',
    'waitlist.hero.stats.exclusive': 'Ексклузивен достъп',
    'waitlist.hero.stats.access': 'Премиум материали и ресурси',
    'waitlist.hero.quote': 'Комуникацията е мост между това, което мислим, и това, което другите разбират',
    'waitlist.understanding.title': 'Разбирам предизвикателствата ви',
    'waitlist.understanding.subtitle': 'От личен опит знам колко трудно може да бъде да се изгради увереност в комуникацията',
    'waitlist.understanding.challenges.title': 'Общи предизвикателства:',
    'waitlist.understanding.challenges.fear.title': 'Страх от публично говорене',
    'waitlist.understanding.challenges.fear.description': 'Тревожност и нервност при представяне пред аудитория',
    'waitlist.understanding.challenges.impostor.title': 'Синдром на самозванеца',
    'waitlist.understanding.challenges.impostor.description': 'Чувство, че не заслужавате да бъдете чути или уважавани',
    'waitlist.understanding.challenges.presence.title': 'Липса на присъствие',
    'waitlist.understanding.challenges.presence.description': 'Трудности в привличането и задържането на вниманието на аудиторията',
    'waitlist.understanding.challenges.camera.title': 'Неудобство пред камера',
    'waitlist.understanding.challenges.camera.description': 'Скованост и неестественост при видео комуникация',
    'waitlist.understanding.truth.title': 'Истината е:',
    'waitlist.understanding.truth.description': 'Всички тези предизвикателства могат да бъдат преодолени с правилните техники и практика.',
    'waitlist.form.title': 'Запишете се в списъка за очакване',
    'waitlist.form.subtitle': 'Получете ранен достъп и специални условия',
    'waitlist.form.fullName': 'Име и фамилия',
    'waitlist.form.email': 'Имейл адрес',
    'waitlist.form.cityCountry': 'Град, страна',
    'waitlist.form.occupation': 'Професия/позиция',
    'waitlist.form.whyJoin': 'Защо искате да се присъедините към курса?',
    'waitlist.form.skillsToImprove': 'Кои умения искате да подобрите?',
    'waitlist.form.submitButton': 'Запишете ме в списъка',
    'waitlist.form.submitting': 'Записване...',
    'waitlist.form.privacyNote': 'Вашата информация е защитена и няма да бъде споделена с трети страни.',
    'waitlist.form.errors.fullNameRequired': 'Моля, въведете вашето име',
    'waitlist.form.errors.emailRequired': 'Моля, въведете вашия имейл',
    'waitlist.form.errors.emailInvalid': 'Моля, въведете валиден имейл адрес',
    'waitlist.form.errors.cityCountryRequired': 'Моля, въведете вашия град и страна',
    'waitlist.form.errors.occupationRequired': 'Моля, въведете вашата професия',
    'waitlist.form.errors.whyJoinRequired': 'Моля, опишете защо искате да се присъедините',
    'waitlist.form.errors.skillsToImproveRequired': 'Моля, опишете уменията, които искате да подобрите',
    'waitlist.form.errors.submitError': 'Възникна грешка. Моля, опитайте отново.',
    'waitlist.form.errors.networkError': 'Грешка в мрежата. Проверете интернет връзката си.',
    'waitlist.benefits.title': 'Какво ще получите като член на списъка',
    'waitlist.benefits.subtitle': 'Ексклузивни предимства за ранните записани участници',
    'waitlist.benefits.earlyAccess.title': 'Ранен достъп',
    'waitlist.benefits.earlyAccess.description': 'Бъдете първите, които ще получат достъп до курса',
    'waitlist.benefits.flexible.title': 'Гъвкаво обучение',
    'waitlist.benefits.flexible.description': 'Учете в собственото си темпо с достъп 24/7',
    'waitlist.benefits.community.title': 'Общност',
    'waitlist.benefits.community.description': 'Присъединете се към мрежа от мотивирани професионалисти',
    'waitlist.benefits.personalized.title': 'Персонализиран подход',
    'waitlist.benefits.personalized.description': 'Получете обратна връзка и съвети, адаптирани за вашите нужди',
    
    // Thank You
    'thankYou.title': 'Благодарим ви!',
    'thankYou.description': 'Успешно се записахте в програмата на Peter Stoyanov',
    'thankYou.success.title': 'Поздравления!',
    'thankYou.success.subtitle': 'Успешно се записахте',
    'thankYou.success.message': 'Благодарим ви за доверието! Ще получите потвърждение на имейла си скоро.',
    'thankYou.actions.returnHome': 'Върнете се в началото',
    'thankYou.actions.learnAbout': 'Научете повече за Peter',
    'thankYou.resources.title': 'Какво следва?',
    'thankYou.resources.subtitle': 'Докато чакате, ето какво можете да правите',
    'thankYou.resources.freeGuide.title': 'Безплатно ръководство',
    'thankYou.resources.freeGuide.description': 'Изтеглете безплатното ни ръководство за подобряване на комуникационните умения',
    'thankYou.resources.aboutPetar.title': 'За Peter Stoyanov',
    'thankYou.resources.aboutPetar.description': 'Научете повече за опита и подхода на Peter в коучинга',
    'thankYou.resources.shareInspire.title': 'Споделете и вдъхновете',
    'thankYou.resources.shareInspire.description': 'Помогнете на други да открият възможността за развитие'
  },
  en: {
    // Navigation  
    'nav.home': 'Home',
    'nav.about': 'About',
    'nav.corporate': 'Corporate',
    'nav.blog': 'Blog',
    'nav.waitlist': 'Join Waitlist',
    
    // Home page
    'home.title': 'Professional Communication & Leadership Coaching',
    'home.description': 'Transform your communication skills and unlock your leadership potential with over 20 years of professional coaching experience.',
    'home.hero.title': 'Professional Communication & Leadership Coaching',
    'home.hero.subtitle': 'Turn your fear into strength. Transform your presence. Become the leader you were meant to be.',
    'home.hero.cta': 'Start Your Transformation',
    'home.hero.meetPetar': 'Meet Peter',
    'home.hero.stats.experience': 'years experience',
    'home.hero.stats.countries': 'countries',
    
    // Video section
    'home.video.title': 'Meet Peter Stoyanov',
    'home.video.description': 'Discover the story behind the methodology and learn how I can help you achieve your communication goals.',
    'home.video.comingSoon': 'Video Coming Soon',
    'home.video.preview': 'Preview of my personal approach',
    'home.video.quote': 'Communication is not just about words - it\'s about creating connection and making an impact.',
    'home.video.credentials': 'Communication & Leadership Expert',
    
    // Methodology section
    'home.methodology.title': 'My Unique Methodology',
    'home.methodology.subtitle': 'A proven approach based on decades of experience in theater, coaching, and the corporate world',
    'home.methodology.method1.title': 'Present Moment Awareness',
    'home.methodology.method1.description': 'Learn to command attention through genuine presence and mindful awareness.',
    'home.methodology.method2.title': 'Voice Mastery',
    'home.methodology.method2.description': 'Master the power of your voice - from projection to tone and tempo.',
    'home.methodology.method3.title': 'Energy and Action',
    'home.methodology.method3.description': 'Transform nervousness into energy that captivates and inspires your audience.',
    
    // Features section
    'home.features.title': 'What You\'ll Learn',
    'home.features.subtitle': 'Comprehensive program for developing communication and leadership skills',
    'home.features.feature1.title': 'Stage Presence',
    'home.features.feature1.description': 'Build magnetic presence that attracts and holds attention.',
    'home.features.feature2.title': 'Voice Techniques',
    'home.features.feature2.description': 'Master projection, articulation, and vocal control for maximum impact.',
    'home.features.feature3.title': 'Body Language',
    'home.features.feature3.description': 'Learn to use your posture, gestures, and movement persuasively.',
    'home.features.feature4.title': 'Camera Work',
    'home.features.feature4.description': 'Become natural and compelling in virtual environments and video communication.',
    'home.features.feature5.title': 'Audience Address',
    'home.features.feature5.description': 'Build connection with viewers and manage group energy.',
    'home.features.feature6.title': 'Improvisation Skills',
    'home.features.feature6.description': 'Develop the ability to think quickly and adapt in unexpected situations.',
    
    // Testimonials section - adding all 10 testimonials
    'home.testimonials.title': 'What My Clients Say',
    'home.testimonials.subtitle': 'Real transformation stories from people who have walked this path',
    'home.testimonials.testimonial1.name': 'Maria Georgieva',
    'home.testimonials.testimonial1.position': 'CEO, TechSoft Bulgaria',
    'home.testimonials.testimonial1.text': 'Working with Peter changed not only how I present, but my entire confidence as a leader. In 6 months I became more persuasive and self-assured.',
    'home.testimonials.testimonial2.name': 'Dimitar Petrov',
    'home.testimonials.testimonial2.position': 'Sales Manager, GlobalCorp',
    'home.testimonials.testimonial2.text': 'I was afraid of public speaking my whole life. Now I lead presentations to hundreds of people and feel natural and confident.',
    'home.testimonials.testimonial3.name': 'Elena Stoeva',
    'home.testimonials.testimonial3.position': 'Founder, Innova Consult',
    'home.testimonials.testimonial3.text': 'Peter\'s techniques helped me find my authentic voice as an entrepreneur. Clients perceive me as a more serious partner.',
    'home.testimonials.testimonial4.name': 'Alexander Ivanov',
    'home.testimonials.testimonial4.position': 'Senior Developer, TechGiant',
    'home.testimonials.testimonial4.text': 'As an introvert I thought I would never be able to present well. Peter\'s methods showed me I can be persuasive in my own way.',
    'home.testimonials.testimonial5.name': 'Violeta Dimitrova',
    'home.testimonials.testimonial5.position': 'HR Director, MegaCompany',
    'home.testimonials.testimonial5.text': 'The training changed not only my professional life, but my personal relationships. I communicate more clearly and with more empathy.',
    'home.testimonials.testimonial6.name': 'Georgi Nikolov',
    'home.testimonials.testimonial6.position': 'Startup Founder',
    'home.testimonials.testimonial6.text': 'Thanks to Peter I was able to attract investors for my startup. My presentation skills improved dramatically.',
    'home.testimonials.testimonial7.name': 'Nadya Pavlova',
    'home.testimonials.testimonial7.position': 'Medical Representative',
    'home.testimonials.testimonial7.text': 'I learned to engage doctors with passion and expertise. My sales increased by 40% after the training.',
    'home.testimonials.testimonial8.name': 'Stefan Mihaylov',
    'home.testimonials.testimonial8.position': 'Project Manager, BigTech',
    'home.testimonials.testimonial8.text': 'Now I can lead difficult conversations with clients without worrying. My confidence as a leader increased significantly.',
    'home.testimonials.testimonial9.name': 'Tsvetelina Atanasova',
    'home.testimonials.testimonial9.position': 'Marketing Consultant',
    'home.testimonials.testimonial9.text': 'Working with Peter gave me the tools to express myself more clearly and persuasively to clients. My business improved.',
    'home.testimonials.testimonial10.name': 'Boris Hristov',
    'home.testimonials.testimonial10.position': 'Financial Analyst',
    'home.testimonials.testimonial10.text': 'I never thought I could hold a presentation without shaking. Now it\'s a natural part of my work.',
    
    // Transformation section
    'home.transformation.title': 'Your Transformation',
    'home.transformation.subtitle': 'From fear and insecurity to confidence and charisma',
    'home.transformation.before.title': 'BEFORE',
    'home.transformation.before.item1': 'Fear of public speaking',
    'home.transformation.before.item2': 'Nervousness on camera',
    'home.transformation.before.item3': 'Lack of presence',
    'home.transformation.before.item4': 'Uncertain communication',
    'home.transformation.after.title': 'AFTER',
    'home.transformation.after.item1': 'Confident public speaking',
    'home.transformation.after.item2': 'Natural on camera',
    'home.transformation.after.item3': 'Strong presence and charisma',
    'home.transformation.after.item4': 'Clear and persuasive communication',
    'home.transformation.cta.title': 'Are you ready for your transformation?',
    'home.transformation.cta.button': 'Start Your Journey',
    
    // Lead magnet section
    'home.leadMagnetSection.title': 'Download the Free Guide',
    'home.leadMagnetSection.description': 'Get access to my exclusive guide with practical exercises for improving breathing, voice, and speaking.',
    'home.leadMagnetSection.benefits': [
      'Breathing control techniques',
      'Voice exercises for clarity',
      'Practical speaking tips',
      'Methods for overcoming stage fright'
    ],
    'home.leadMagnetSection.guideLabel': 'Guide',
    'home.leadMagnetSection.pdfLabel': 'PDF Format',
    'home.leadMagnetSection.freeLabel': 'FREE',
    
    // Lead magnet form
    'home.leadMagnet.emailPlaceholder': 'Enter your email address',
    'home.leadMagnet.downloadButton': 'Download Free',
    'home.leadMagnet.sending': 'Sending...',
    'home.leadMagnet.joinText': 'Join thousands of professionals already improving their skills',
    'home.leadMagnet.errors.emailRequired': 'Please enter a valid email address',
    'home.leadMagnet.errors.submitError': 'An error occurred during submission',
    'home.leadMagnet.errors.networkError': 'Network error. Please try again.',
    
    // CTA section
    'home.cta.title': 'Ready to Get Started?',
    'home.cta.description': 'Join hundreds of professionals who have already transformed their communication and leadership skills.',
    'home.cta.button': 'Enroll Now',
    'home.cta.corporateButton': 'Corporate Training',
    
    // Services
    'services.title': 'Professional Coaching Services',
    'services.individual.title': 'Individual Coaching',
    'services.individual.description': 'Personal development for communication excellence and leadership presence.',
    'services.corporate.title': 'Corporate Training',
    'services.corporate.description': 'Team workshops and organizational communication development programs.',
    'services.leadership.title': 'Leadership Development',
    'services.leadership.description': 'Build confidence, presence, and communication skills for effective leadership.',
    
    // Footer
    'footer.description': 'Transforming communication through theater techniques, breath work, and authentic presence.',
    'footer.contact': 'Contact',
    'footer.followUs': 'Follow Us',
    'footer.newsletter': 'Newsletter',
    'footer.newsletterDescription': 'Stay updated.',
    'footer.subscribe': 'Subscribe',
    'footer.allRightsReserved': 'All Rights Reserved',
    'footer.privacyPolicy': 'Privacy Policy',
    'footer.termsOfService': 'Terms of Service',
    'footer.copyright': '© 2024 Peter Stoyanov Coaching',
    'footer.tagline': 'Professional Communication & Leadership Development',
    
    // Contact
    'contact.title': 'Contact Peter Stoyanov',
    'contact.ready': 'Ready to transform your communication and leadership skills?',
    'contact.email': 'Email',
    'contact.services': 'Services',
    'contact.approach': 'About My Approach',
    'contact.back': '← Back to Home',
    
    // About
    'about.title': 'About Me',
    'about.hero.title': 'Hello, I\'m Peter Stoyanov',
    'about.hero.subtitle': 'Communication & Leadership Coach with 20+ years of experience',
    'about.journey.title': 'My Journey',
    'about.journey.description': 'From the theater stage to corporate boardrooms, my path has taught me that true leadership begins with authentic communication.',
    'about.expertise.title': 'My Expertise',
    'about.approach.title': 'My Approach',
    
    // Corporate
    'corporate.title': 'Corporate Training',
    'corporate.hero.title': 'Transform Your Team Through Powerful Communication',
    'corporate.hero.subtitle': 'Customized training programs that build confidence and improve results',
    'corporate.programs.title': 'Training Programs',
    'corporate.contact.title': 'Get Started Today',
    'corporate.contact.description': 'Contact us for a personalized consultation and proposal for your organization.',
    
    // Waitlist
    'waitlist.title': 'Become Part of Communication\'s Future',
    'waitlist.description': 'Exclusive course for presence and communication skills',
    'waitlist.hero.stats.limited': 'Limited Spots',
    'waitlist.hero.stats.spotsAvailable': 'Only 20 spots available',
    'waitlist.hero.stats.early': 'Early Access',
    'waitlist.hero.stats.birdPricing': 'Special pricing for early birds',
    'waitlist.hero.stats.exclusive': 'Exclusive Access',
    'waitlist.hero.stats.access': 'Premium materials and resources',
    'waitlist.hero.quote': 'Communication is the bridge between what we think and what others understand',
    'waitlist.understanding.title': 'I Understand Your Challenges',
    'waitlist.understanding.subtitle': 'From personal experience, I know how difficult it can be to build confidence in communication',
    'waitlist.understanding.challenges.title': 'Common Challenges:',
    'waitlist.understanding.challenges.fear.title': 'Fear of Public Speaking',
    'waitlist.understanding.challenges.fear.description': 'Anxiety and nervousness when presenting to an audience',
    'waitlist.understanding.challenges.impostor.title': 'Impostor Syndrome',
    'waitlist.understanding.challenges.impostor.description': 'Feeling like you don\'t deserve to be heard or respected',
    'waitlist.understanding.challenges.presence.title': 'Lack of Presence',
    'waitlist.understanding.challenges.presence.description': 'Difficulty in capturing and maintaining audience attention',
    'waitlist.understanding.challenges.camera.title': 'Camera Discomfort',
    'waitlist.understanding.challenges.camera.description': 'Stiffness and unnaturalness in video communication',
    'waitlist.understanding.truth.title': 'The Truth Is:',
    'waitlist.understanding.truth.description': 'All these challenges can be overcome with the right techniques and practice.',
    'waitlist.form.title': 'Join the Waitlist',
    'waitlist.form.subtitle': 'Get early access and special conditions',
    'waitlist.form.fullName': 'Full Name',
    'waitlist.form.email': 'Email Address',
    'waitlist.form.cityCountry': 'City, Country',
    'waitlist.form.occupation': 'Profession/Position',
    'waitlist.form.whyJoin': 'Why do you want to join the course?',
    'waitlist.form.skillsToImprove': 'What skills do you want to improve?',
    'waitlist.form.submitButton': 'Add Me to the List',
    'waitlist.form.submitting': 'Submitting...',
    'waitlist.form.privacyNote': 'Your information is protected and will not be shared with third parties.',
    'waitlist.form.errors.fullNameRequired': 'Please enter your name',
    'waitlist.form.errors.emailRequired': 'Please enter your email',
    'waitlist.form.errors.emailInvalid': 'Please enter a valid email address',
    'waitlist.form.errors.cityCountryRequired': 'Please enter your city and country',
    'waitlist.form.errors.occupationRequired': 'Please enter your profession',
    'waitlist.form.errors.whyJoinRequired': 'Please describe why you want to join',
    'waitlist.form.errors.skillsToImproveRequired': 'Please describe the skills you want to improve',
    'waitlist.form.errors.submitError': 'An error occurred. Please try again.',
    'waitlist.form.errors.networkError': 'Network error. Please check your internet connection.',
    'waitlist.benefits.title': 'What You\'ll Get as a Member',
    'waitlist.benefits.subtitle': 'Exclusive benefits for early registered participants',
    'waitlist.benefits.earlyAccess.title': 'Early Access',
    'waitlist.benefits.earlyAccess.description': 'Be the first to get access to the course',
    'waitlist.benefits.flexible.title': 'Flexible Learning',
    'waitlist.benefits.flexible.description': 'Learn at your own pace with 24/7 access',
    'waitlist.benefits.community.title': 'Community',
    'waitlist.benefits.community.description': 'Join a network of motivated professionals',
    'waitlist.benefits.personalized.title': 'Personalized Approach',
    'waitlist.benefits.personalized.description': 'Get feedback and advice tailored to your needs',
    
    // Thank You
    'thankYou.title': 'Thank You!',
    'thankYou.description': 'Successfully registered for Peter Stoyanov\'s program',
    'thankYou.success.title': 'Congratulations!',
    'thankYou.success.subtitle': 'Successfully registered',
    'thankYou.success.message': 'Thank you for your trust! You will receive confirmation in your email soon.',
    'thankYou.actions.returnHome': 'Return Home',
    'thankYou.actions.learnAbout': 'Learn About Peter',
    'thankYou.resources.title': 'What\'s Next?',
    'thankYou.resources.subtitle': 'While you wait, here\'s what you can do',
    'thankYou.resources.freeGuide.title': 'Free Guide',
    'thankYou.resources.freeGuide.description': 'Download our free guide to improving communication skills',
    'thankYou.resources.aboutPetar.title': 'About Peter Stoyanov',
    'thankYou.resources.aboutPetar.description': 'Learn more about Peter\'s experience and coaching approach',
    'thankYou.resources.shareInspire.title': 'Share and Inspire',
    'thankYou.resources.shareInspire.description': 'Help others discover the opportunity for growth'
  }
};

export function useTranslation() {
  const router = useRouter();
  const [locale, setLocale] = useState('bg'); // Default to Bulgarian

  useEffect(() => {
    // Get locale from URL or localStorage
    const urlLocale = router.query.lang || localStorage.getItem('locale') || 'bg';
    setLocale(urlLocale);
  }, [router.query.lang]);

  const t = (key) => {
    return translations[locale]?.[key] || translations['en'][key] || key;
  };

  const changeLanguage = (newLocale) => {
    setLocale(newLocale);
    localStorage.setItem('locale', newLocale);
    
    // Update URL
    const newQuery = { ...router.query, lang: newLocale };
    router.push({
      pathname: router.pathname,
      query: newQuery
    }, undefined, { shallow: true });
  };

  return {
    t,
    i18n: {
      language: locale,
      changeLanguage
    }
  };
}