import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Appearance } from 'react-native';

export type ThemeMode = 'light' | 'dark' | 'system';

interface ThemeState {
  mode: ThemeMode;
  isDark: boolean;
  setThemeMode: (mode: ThemeMode) => Promise<void>;
  toggleTheme: () => Promise<void>;
  initializeTheme: () => Promise<void>;
}

const THEME_STORAGE_KEY = '@agrivision_theme_mode';

const resolveIsDark = (mode: ThemeMode): boolean => {
  if (mode === 'dark') return true;
  if (mode === 'light') return false;
  const sys = Appearance.getColorScheme();
  return sys === 'dark';
};

export const useThemeStore = create<ThemeState>((set, get) => ({
  mode: 'light',
  isDark: false,

  setThemeMode: async (mode: ThemeMode) => {
    const isDark = resolveIsDark(mode);
    set({ mode, isDark });
    try {
      await AsyncStorage.setItem(THEME_STORAGE_KEY, mode);
    } catch (err) {
      console.warn('Failed to persist theme mode:', err);
    }
  },

  toggleTheme: async () => {
    const nextMode: ThemeMode = get().isDark ? 'light' : 'dark';
    await get().setThemeMode(nextMode);
  },

  initializeTheme: async () => {
    try {
      const stored = await AsyncStorage.getItem(THEME_STORAGE_KEY);
      if (stored === 'dark' || stored === 'light' || stored === 'system') {
        set({ mode: stored as ThemeMode, isDark: resolveIsDark(stored as ThemeMode) });
      } else {
        set({ mode: 'light', isDark: false });
      }
    } catch {
      set({ mode: 'light', isDark: false });
    }
  },
}));
