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
    'contact.back': '← Обратно към началото'
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
    'contact.back': '← Back to Home'
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