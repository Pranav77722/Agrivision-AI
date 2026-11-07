import React, { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { I18nextProvider } from 'react-i18next';
import i18n, { initI18n } from '../src/i18n';
import { useThemeStore } from '../src/store/themeStore';
import { useLanguageStore } from '../src/store/languageStore';
import { useDiagnosisStore } from '../src/store/diagnosisStore';
import { useAuthStore } from '../src/store/authStore';
import { useTheme } from '../src/hooks/useTheme';

SplashScreen.preventAutoHideAsync().catch(() => {});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 1000 * 60 * 5,
    },
  },
});

function RootNavigation() {
  const theme = useTheme();

  return (
    <>
      <StatusBar style={theme.isDark ? 'light' : 'dark'} />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: theme.colors.background },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="diagnosis/camera" options={{ animation: 'fade' }} />
        <Stack.Screen name="diagnosis/preview" />
        <Stack.Screen name="diagnosis/results" />
        <Stack.Screen name="diagnosis/[id]" />
        <Stack.Screen name="ensemble/index" />
        <Stack.Screen name="pest/index" />
        <Stack.Screen name="severity/index" />
        <Stack.Screen name="explainability/index" />
        <Stack.Screen name="yield/index" />
        <Stack.Screen name="recommendations/[id]" />
        <Stack.Screen name="assistant/index" />
        <Stack.Screen name="reports/index" />
        <Stack.Screen name="archive/index" />
        <Stack.Screen name="settings/language" />
        <Stack.Screen name="settings/theme" />
      </Stack>
    </>
  );
}

export default function RootLayout() {
  const [appIsReady, setAppIsReady] = useState(false);
  const initializeTheme = useThemeStore((s) => s.initializeTheme);
  const initializeLanguage = useLanguageStore((s) => s.initializeLanguage);
  const initializeHistory = useDiagnosisStore((s) => s.initializeHistory);
  const initializeAuth = useAuthStore((s) => s.initializeAuth);

  useEffect(() => {
    async function prepare() {
      try {
        await Promise.all([
          initI18n(),
          initializeTheme(),
          initializeLanguage(),
          initializeHistory(),
          initializeAuth(),
        ]);
      } catch (e) {
        console.warn('Initialization error:', e);
      } finally {
        setAppIsReady(true);
        await SplashScreen.hideAsync().catch(() => {});
      }
    }
    prepare();
  }, [initializeTheme, initializeLanguage, initializeHistory, initializeAuth]);

  if (!appIsReady) {
    return null;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <I18nextProvider i18n={i18n}>
          <RootNavigation />
        </I18nextProvider>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}
