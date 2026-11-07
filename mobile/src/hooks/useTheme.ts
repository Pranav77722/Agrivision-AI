import { useMemo } from 'react';
import { useThemeStore } from '../store/themeStore';
import { getTheme, AppTheme } from '../theme';

export const useTheme = (): AppTheme & {
  mode: 'light' | 'dark' | 'system';
  setThemeMode: (mode: 'light' | 'dark' | 'system') => Promise<void>;
  toggleTheme: () => Promise<void>;
} => {
  const mode = useThemeStore((s) => s.mode);
  const isDark = useThemeStore((s) => s.isDark);
  const setThemeMode = useThemeStore((s) => s.setThemeMode);
  const toggleTheme = useThemeStore((s) => s.toggleTheme);

  const theme = useMemo(() => getTheme(isDark), [isDark]);

  return {
    ...theme,
    mode,
    setThemeMode,
    toggleTheme,
  };
};

export default useTheme;
