import React, { createContext, useState, useContext, useEffect } from 'react';
import enTranslations from '../public/locales/en/common.json';
import bgTranslations from '../public/locales/bg/common.json';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Import translation files directly to ensure they work with SSG
const translations = {
  en: enTranslations,
  bg: bgTranslations
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [loading, setLoading] = useState(false);

  // Initialize language from localStorage on client-side
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedLanguage = localStorage.getItem('language') || 'en';
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  // Switch language
  const switchLanguage = (newLanguage) => {
    if (newLanguage === currentLanguage) return;
    
    setCurrentLanguage(newLanguage);
    
    // Save to localStorage if in browser environment
    if (typeof window !== 'undefined') {
      localStorage.setItem('language', newLanguage);
    }
  };

  // Translation function - supports nested keys like 'nav.home' and arrays
  const t = (key, options = {}) => {
    const keys = key.split('.');
    let value = translations[currentLanguage];
    
    if (!value) {
      value = translations['en']; // fallback to English
    }
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Try fallback to English if not found in current language
        let fallbackValue = translations['en'];
        for (const fk of keys) {
          if (fallbackValue && typeof fallbackValue === 'object' && fk in fallbackValue) {
            fallbackValue = fallbackValue[fk];
          } else {
            return options.fallback || key;
          }
        }
        return typeof fallbackValue === 'string' ? fallbackValue : (options.fallback || key);
      }
    }
    
    // If returnObjects is true, return arrays/objects as-is
    if (options.returnObjects && (Array.isArray(value) || typeof value === 'object')) {
      return value;
    }
    
    return typeof value === 'string' ? value : (options.fallback || key);
  };

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        switchLanguage,
        t,
        loading
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};