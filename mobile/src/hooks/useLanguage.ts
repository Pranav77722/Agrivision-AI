import { useTranslation } from 'react-i18next';
import { useLanguageStore } from '../store/languageStore';
import { SupportedLanguage, SUPPORTED_LANGUAGES } from '../i18n';

export const useLanguage = () => {
  const { t, i18n } = useTranslation();
  const currentLanguage = useLanguageStore((s) => s.currentLanguage);
  const setLanguage = useLanguageStore((s) => s.setLanguage);

  return {
    t,
    i18n,
    currentLanguage,
    setLanguage,
    supportedLanguages: SUPPORTED_LANGUAGES,
    isMarathi: currentLanguage === 'mr',
    isHindi: currentLanguage === 'hi',
    isEnglish: currentLanguage === 'en',
  };
};

export default useLanguage;
