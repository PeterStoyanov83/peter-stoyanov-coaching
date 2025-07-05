import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useTranslation } from 'next-i18next';

export default function Header() {
  const { t, i18n } = useTranslation('common');
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  
  // Toggle language between 'bg' (Bulgarian) and 'en' (English)
  const toggleLanguage = () => {
    const newLocale = i18n.language === 'bg' ? 'en' : 'bg';
    router.push(router.pathname, router.asPath, { locale: newLocale });
  };
  
  // Handle scroll event to change header style when scrolled
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-md py-3' : 'bg-white/95 backdrop-blur-sm py-4'
    }`}>
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link href="/" className="text-xl font-bold text-indigo-600">
            Petar Stoyanov
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/" className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
              router.pathname === '/' ? 'font-semibold text-indigo-600' : ''
            }`}>
              {t('nav.home')}
            </Link>
            <Link href="/about" className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
              router.pathname === '/about' ? 'font-semibold text-indigo-600' : ''
            }`}>
              {t('nav.about')}
            </Link>
            <Link href="/corporate" className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
              router.pathname === '/corporate' ? 'font-semibold text-indigo-600' : ''
            }`}>
              {t('nav.corporate')}
            </Link>
            <Link href="/blog" className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
              router.pathname.startsWith('/blog') ? 'font-semibold text-indigo-600' : ''
            }`}>
              {t('nav.blog')}
            </Link>
            <Link href="/waitlist" className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-300">
              {t('nav.waitlist')}
            </Link>
            
            {/* Language Switcher */}
            <button 
              onClick={toggleLanguage}
              className="px-3 py-1 text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 rounded-md transition duration-300 font-medium"
            >
              {i18n.language === 'bg' ? 'EN' : 'BG'}
            </button>
          </nav>
          
          {/* Mobile Menu Button */}
          <button 
            className="md:hidden text-gray-700 focus:outline-none"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
        
        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="md:hidden mt-4 pb-4">
            <div className="flex flex-col space-y-4">
              <Link href="/" 
                className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
                  router.pathname === '/' ? 'font-semibold text-indigo-600' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.home')}
              </Link>
              <Link href="/about" 
                className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
                  router.pathname === '/about' ? 'font-semibold text-indigo-600' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.about')}
              </Link>
              <Link href="/corporate" 
                className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
                  router.pathname === '/corporate' ? 'font-semibold text-indigo-600' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.corporate')}
              </Link>
              <Link href="/blog" 
                className={`text-gray-700 hover:text-indigo-600 transition duration-300 ${
                  router.pathname.startsWith('/blog') ? 'font-semibold text-indigo-600' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.blog')}
              </Link>
              <Link href="/waitlist" 
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-300 inline-block"
                onClick={() => setIsMenuOpen(false)}
              >
                {t('nav.waitlist')}
              </Link>
              
              {/* Language Switcher */}
              <button 
                onClick={() => {
                  toggleLanguage();
                  setIsMenuOpen(false);
                }}
                className="px-3 py-1 text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 rounded-md transition duration-300 font-medium"
              >
                {i18n.language === 'bg' ? 'EN' : 'BG'}
              </button>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}