import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import i18n, { SupportedLanguage, LANGUAGE_STORAGE_KEY } from '../i18n';

interface LanguageState {
  currentLanguage: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => Promise<void>;
  initializeLanguage: () => Promise<void>;
}

export const useLanguageStore = create<LanguageState>((set) => ({
  currentLanguage: (i18n.language as SupportedLanguage) || 'en',

  setLanguage: async (lang: SupportedLanguage) => {
    try {
      await i18n.changeLanguage(lang);
      await AsyncStorage.setItem(LANGUAGE_STORAGE_KEY, lang);
      set({ currentLanguage: lang });
    } catch (error) {
      console.error('Failed to change language:', error);
    }
  },

  initializeLanguage: async () => {
    try {
      const stored = await AsyncStorage.getItem(LANGUAGE_STORAGE_KEY);
      if (stored && ['en', 'mr', 'hi'].includes(stored)) {
        await i18n.changeLanguage(stored);
        set({ currentLanguage: stored as SupportedLanguage });
      }
    } catch (err) {
      console.warn('Could not initialize language from storage:', err);
    }
  },
}));
