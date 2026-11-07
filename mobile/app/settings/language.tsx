import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { LanguageSelector } from '../../src/components/common/LanguageSelector';

export default function LanguageSettingsScreen() {
  const { t } = useTranslation(['profile', 'common']);
  const router = useRouter();

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('profile:languageSubtitle')}
        title={t('profile:language')}
        onBack={() => router.back()}
      />
      <View style={styles.content}>
        <Card>
          <LanguageSelector />
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
});

