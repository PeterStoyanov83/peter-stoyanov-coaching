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
    'home.hero.title': 'Освободете своя потенциал за лидерство',
    'home.hero.subtitle': 'Професионално обучение за комуникация и лидерство',
    'home.hero.description': 'Преобразете уменията си за комуникация и отключете лидерския си потенциал с над 20 години професионален опит в коучинг.',
    'home.cta.primary': 'Изтеглете безплатно ръководство',
    'home.cta.secondary': 'Свържете се с мен',
    
    // Services
    'services.title': 'Професионални коучинг услуги',
    'services.individual.title': 'Индивидуален коучинг',
    'services.individual.description': 'Личностно развитие за съвършенство в комуникацията и лидерско присъствие.',
    'services.corporate.title': 'Корпоративно обучение',
    'services.corporate.description': 'Семинари за екипи и програми за развитие на организационната комуникация.',
    'services.leadership.title': 'Развитие на лидерството',
    'services.leadership.description': 'Изградете увереност, присъствие и комуникационни умения за ефективно лидерство.',
    
    // Footer
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
    'home.hero.title': 'Unlock Your Leadership Potential',
    'home.hero.subtitle': 'Professional Coaching for Communication & Leadership',
    'home.hero.description': 'Transform your communication skills and unlock your leadership potential with over 20 years of professional coaching experience.',
    'home.cta.primary': 'Download Free Guide',
    'home.cta.secondary': 'Contact Me',
    
    // Services
    'services.title': 'Professional Coaching Services',
    'services.individual.title': 'Individual Coaching',
    'services.individual.description': 'Personal development for communication excellence and leadership presence.',
    'services.corporate.title': 'Corporate Training',
    'services.corporate.description': 'Team workshops and organizational communication development programs.',
    'services.leadership.title': 'Leadership Development',
    'services.leadership.description': 'Build confidence, presence, and communication skills for effective leadership.',
    
    // Footer
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