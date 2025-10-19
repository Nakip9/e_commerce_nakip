import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const LANGUAGE_KEY = 'nakip_language';

export function LanguageSwitcher() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const saved = localStorage.getItem(LANGUAGE_KEY);
    if (saved && saved !== i18n.language) {
      i18n.changeLanguage(saved);
      document.documentElement.lang = saved;
      document.documentElement.dir = saved === 'ar' ? 'rtl' : 'ltr';
    }
  }, [i18n]);

  const toggleLanguage = () => {
    const next = i18n.language === 'ar' ? 'en' : 'ar';
    i18n.changeLanguage(next);
    localStorage.setItem(LANGUAGE_KEY, next);
    document.documentElement.lang = next;
    document.documentElement.dir = next === 'ar' ? 'rtl' : 'ltr';
  };

  return (
    <button type="button" className="language-switcher" onClick={toggleLanguage}>
      {i18n.language === 'ar' ? 'English' : 'العربية'}
    </button>
  );
}
