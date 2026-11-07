import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Input } from '../../src/components/ui/Input';
import { Button } from '../../src/components/ui/Button';
import { useTheme } from '../../src/hooks/useTheme';

export default function ForgotPasswordScreen() {
  const { t } = useTranslation(['onboarding', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const [identifier, setIdentifier] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSendCode = () => {
    if (!identifier.trim()) {
      Alert.alert(t('common:error'), t('common:requiredField'));
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSent(true);
    }, 1200);
  };

  return (
    <SafeArea style={styles.safeArea}>
      <View style={styles.container}>
        <TouchableOpacity
          accessibilityRole="button"
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          style={styles.backBtn}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color={theme.colors.textPrimary} />
        </TouchableOpacity>

        <View style={styles.header}>
          <View style={[styles.iconBox, { backgroundColor: theme.colors.primaryLight }]}>
            <Ionicons name="key-outline" size={32} color={theme.colors.primary} />
          </View>
          <Text style={[styles.title, { color: theme.colors.textPrimary }]}>
            {t('onboarding:forgotPasswordTitle')}
          </Text>
          <Text style={[styles.subtitle, { color: theme.colors.textSecondary }]}>
            {t('onboarding:forgotPasswordSubtitle')}
          </Text>
        </View>

        {sent ? (
          <View style={[styles.successBox, { backgroundColor: theme.colors.successLight }]}>
            <Ionicons name="checkmark-circle" size={24} color={theme.colors.success} />
            <Text style={[styles.successText, { color: theme.colors.primary }]}>
              {t('common:success')} - OTP Code sent!
            </Text>
            <Button
              size="md"
              style={styles.backToLogin}
              title={t('onboarding:loginButton')}
              variant="primary"
              onPress={() => router.replace('/(auth)/login' as any)}
            />
          </View>
        ) : (
          <View style={styles.form}>
            <Input
              autoCapitalize="none"
              label={t('onboarding:phoneOrEmail')}
              leftIcon={
                <Ionicons name="call-outline" size={20} color={theme.colors.textSecondary} />
              }
              placeholder="+91 98765 43210"
              value={identifier}
              onChangeText={setIdentifier}
            />

            <Button
              loading={loading}
              size="lg"
              style={styles.submitBtn}
              title={t('onboarding:sendResetCode')}
              variant="primary"
              onPress={handleSendCode}
            />
          </View>
        )}
      </View>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  container: {
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  backBtn: {
    paddingVertical: 8,
  },
  header: {
    marginTop: 16,
    marginBottom: 28,
  },
  iconBox: {
    width: 60,
    height: 60,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: '800',
    marginBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    lineHeight: 20,
  },
  form: {
    width: '100%',
  },
  submitBtn: {
    marginTop: 16,
  },
  successBox: {
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    gap: 12,
  },
  successText: {
    fontSize: 15,
    fontWeight: '700',
    textAlign: 'center',
  },
  backToLogin: {
    marginTop: 8,
    width: '100%',
  },
});
