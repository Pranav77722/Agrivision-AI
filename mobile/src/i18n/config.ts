import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import * as Localization from 'expo-localization';
import AsyncStorage from '@react-native-async-storage/async-storage';

// English
import enCommon from './locales/en/common.json';
import enOnboarding from './locales/en/onboarding.json';
import enDashboard from './locales/en/dashboard.json';
import enDiagnosis from './locales/en/diagnosis.json';
import enEnsemble from './locales/en/ensemble.json';
import enPest from './locales/en/pest.json';
import enSeverity from './locales/en/severity.json';
import enExplainability from './locales/en/explainability.json';
import enYield from './locales/en/yield.json';
import enRecommendations from './locales/en/recommendations.json';
import enKnowledge from './locales/en/knowledge.json';
import enAssistant from './locales/en/assistant.json';
import enReports from './locales/en/reports.json';
import enArchive from './locales/en/archive.json';
import enProfile from './locales/en/profile.json';

// Marathi
import mrCommon from './locales/mr/common.json';
import mrOnboarding from './locales/mr/onboarding.json';
import mrDashboard from './locales/mr/dashboard.json';
import mrDiagnosis from './locales/mr/diagnosis.json';
import mrEnsemble from './locales/mr/ensemble.json';
import mrPest from './locales/mr/pest.json';
import mrSeverity from './locales/mr/severity.json';
import mrExplainability from './locales/mr/explainability.json';
import mrYield from './locales/mr/yield.json';
import mrRecommendations from './locales/mr/recommendations.json';
import mrKnowledge from './locales/mr/knowledge.json';
import mrAssistant from './locales/mr/assistant.json';
import mrReports from './locales/mr/reports.json';
import mrArchive from './locales/mr/archive.json';
import mrProfile from './locales/mr/profile.json';

// Hindi
import hiCommon from './locales/hi/common.json';
import hiOnboarding from './locales/hi/onboarding.json';
import hiDashboard from './locales/hi/dashboard.json';
import hiDiagnosis from './locales/hi/diagnosis.json';
import hiEnsemble from './locales/hi/ensemble.json';
import hiPest from './locales/hi/pest.json';
import hiSeverity from './locales/hi/severity.json';
import hiExplainability from './locales/hi/explainability.json';
import hiYield from './locales/hi/yield.json';
import hiRecommendations from './locales/hi/recommendations.json';
import hiKnowledge from './locales/hi/knowledge.json';
import hiAssistant from './locales/hi/assistant.json';
import hiReports from './locales/hi/reports.json';
import hiArchive from './locales/hi/archive.json';
import hiProfile from './locales/hi/profile.json';

export const LANGUAGE_STORAGE_KEY = '@agrivision_language';

export const resources = {
  en: {
    common: enCommon,
    onboarding: enOnboarding,
    dashboard: enDashboard,
    diagnosis: enDiagnosis,
    ensemble: enEnsemble,
    pest: enPest,
    severity: enSeverity,
    explainability: enExplainability,
    yield: enYield,
    recommendations: enRecommendations,
    knowledge: enKnowledge,
    assistant: enAssistant,
    reports: enReports,
    archive: enArchive,
    profile: enProfile,
  },
  mr: {
    common: mrCommon,
    onboarding: mrOnboarding,
    dashboard: mrDashboard,
    diagnosis: mrDiagnosis,
    ensemble: mrEnsemble,
    pest: mrPest,
    severity: mrSeverity,
    explainability: mrExplainability,
    yield: mrYield,
    recommendations: mrRecommendations,
    knowledge: mrKnowledge,
    assistant: mrAssistant,
    reports: mrReports,
    archive: mrArchive,
    profile: mrProfile,
  },
  hi: {
    common: hiCommon,
    onboarding: hiOnboarding,
    dashboard: hiDashboard,
    diagnosis: hiDiagnosis,
    ensemble: hiEnsemble,
    pest: hiPest,
    severity: hiSeverity,
    explainability: hiExplainability,
    yield: hiYield,
    recommendations: hiRecommendations,
    knowledge: hiKnowledge,
    assistant: hiAssistant,
    reports: hiReports,
    archive: hiArchive,
    profile: hiProfile,
  },
} as const;

export type SupportedLanguage = 'en' | 'mr' | 'hi';

export const SUPPORTED_LANGUAGES: { code: SupportedLanguage; label: string; nativeName: string }[] = [
  { code: 'en', label: 'English', nativeName: 'English' },
  { code: 'mr', label: 'Marathi', nativeName: 'मराठी' },
  { code: 'hi', label: 'Hindi', nativeName: 'हिंदी' },
];

export const initI18n = async (): Promise<typeof i18n> => {
  let defaultLang: SupportedLanguage = 'en';

  try {
    const savedLang = await AsyncStorage.getItem(LANGUAGE_STORAGE_KEY);
    if (savedLang && ['en', 'mr', 'hi'].includes(savedLang)) {
      defaultLang = savedLang as SupportedLanguage;
    } else {
      const deviceLocales = Localization.getLocales();
      const deviceLang = deviceLocales?.[0]?.languageCode;
      if (deviceLang === 'mr' || deviceLang === 'hi') {
        defaultLang = deviceLang;
      }
    }
  } catch (error) {
    console.warn('Error fetching language from storage:', error);
  }

  if (!i18n.isInitialized) {
    await i18n
      .use(initReactI18next)
      .init({
        compatibilityJSON: 'v4',
        resources,
        lng: defaultLang,
        fallbackLng: 'en',
        ns: [
          'common',
          'onboarding',
          'dashboard',
          'diagnosis',
          'ensemble',
          'pest',
          'severity',
          'explainability',
          'yield',
          'recommendations',
          'knowledge',
          'assistant',
          'reports',
          'archive',
          'profile',
        ],
        defaultNS: 'common',
        interpolation: {
          escapeValue: false,
        },
      });
  }

  return i18n;
};

export default i18n;
