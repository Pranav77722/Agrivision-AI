import i18n, { SupportedLanguage } from '../i18n';

export const translationService = {
  getLanguage: (): SupportedLanguage => {
    return (i18n.language as SupportedLanguage) || 'en';
  },

  changeLanguage: async (lang: SupportedLanguage): Promise<void> => {
    await i18n.changeLanguage(lang);
  },

  translateText: (key: string, namespace?: string, options?: Record<string, any>): string => {
    const fullKey = namespace ? `${namespace}:${key}` : key;
    return i18n.t(fullKey, options);
  },
};
