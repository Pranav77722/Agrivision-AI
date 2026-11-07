import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { useTheme } from '../../src/hooks/useTheme';
import { ThemeMode } from '../../src/store/themeStore';

export default function ThemeSettingsScreen() {
  const { t } = useTranslation(['profile', 'common']);
  const theme = useTheme();
  const router = useRouter();

  const options: { mode: ThemeMode; label: string; icon: keyof typeof Ionicons.glyphMap }[] = [
    { mode: 'light', label: t('profile:themeLight'), icon: 'sunny-outline' },
    { mode: 'dark', label: t('profile:themeDark'), icon: 'moon-outline' },
    { mode: 'system', label: t('profile:themeSystem'), icon: 'phone-portrait-outline' },
  ];

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('profile:theme')}
        title={t('profile:theme')}
        onBack={() => router.back()}
      />

      <View style={styles.content}>
        <Card>
          {options.map((opt, idx) => {
            const isSelected = theme.mode === opt.mode;
            return (
              <TouchableOpacity
                key={opt.mode}
                activeOpacity={0.7}
                style={[
                  styles.optionRow,
                  idx < options.length - 1 && {
                    borderBottomWidth: 1,
                    borderBottomColor: theme.colors.border,
                  },
                ]}
                onPress={() => theme.setThemeMode(opt.mode)}
              >
                <View style={styles.left}>
                  <Ionicons name={opt.icon} size={22} color={theme.colors.primary} />
                  <Text style={[styles.label, { color: theme.colors.textPrimary }]}>
                    {opt.label}
                  </Text>
                </View>

                {isSelected && (
                  <Ionicons name="checkmark-circle" size={24} color={theme.colors.primary} />
                )}
              </TouchableOpacity>
            );
          })}
        </Card>
      </View>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  content: {
    padding: 16,
  },
  optionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
  },
  left: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  label: {
    fontSize: 15,
    fontWeight: '600',
  },
});

