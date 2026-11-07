import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../src/store/authStore';
import { useTheme } from '../src/hooks/useTheme';

export default function IndexScreen() {
  const router = useRouter();
  const theme = useTheme();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isLoading = useAuthStore((s) => s.isLoading);

  useEffect(() => {
    if (!isLoading) {
      const timer = setTimeout(() => {
        if (isAuthenticated) {
          router.replace('/(tabs)');
        } else {
          router.replace('/(auth)/welcome');
        }
      }, 700);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, isLoading, router]);

  return (
    <View style={[styles.container, { backgroundColor: theme.isDark ? '#0B1220' : '#FFFFFF' }]}>
      <Image
        source={require('../assets/logo.png')}
        style={styles.logo}
        resizeMode="contain"
      />
      <Text style={[styles.appName, { color: theme.colors.primary }]}>
        Agrivision AI+
      </Text>
      <Text style={[styles.tagline, { color: theme.colors.textSecondary }]}>
        Smart Farming with AI • कृषी क्रांती
      </Text>
      <View style={styles.loaderWrap}>
        <ActivityIndicator color={theme.colors.primary} size="small" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  logo: {
    width: 140,
    height: 140,
    borderRadius: 28,
    marginBottom: 16,
  },
  appName: {
    fontSize: 26,
    fontWeight: '900',
    letterSpacing: -0.5,
  },
  tagline: {
    fontSize: 13,
    fontWeight: '600',
    marginTop: 6,
  },
  loaderWrap: {
    marginTop: 28,
  },
});
