import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Image,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Input } from '../../src/components/ui/Input';
import { Button } from '../../src/components/ui/Button';
import { LanguageSelector } from '../../src/components/common/LanguageSelector';
import { loginSchema, LoginFormData } from '../../src/utils/validators';
import { useAuthStore } from '../../src/store/authStore';
import { authService } from '../../src/services/authService';
import { useTheme } from '../../src/hooks/useTheme';

export default function LoginScreen() {
  const { t } = useTranslation(['onboarding', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const loginToStore = useAuthStore((s) => s.login);
  const [loading, setLoading] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      phoneOrEmail: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setLoading(true);
    setAuthError(null);
    try {
      const response = await authService.login({
        phoneOrEmail: data.phoneOrEmail.trim(),
        password: data.password,
      });
      await loginToStore(response.accessToken, response.refreshToken, response.user);
      router.replace('/(tabs)');
    } catch (err: any) {
      setAuthError(err?.response?.data?.detail || t('common:networkError'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeArea style={styles.safeArea}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        style={styles.keyboardView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.topBar}>
            <TouchableOpacity
              accessibilityRole="button"
              hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              onPress={() => router.back()}
            >
              <Ionicons name="arrow-back" size={24} color={theme.colors.textPrimary} />
            </TouchableOpacity>

            <LanguageSelector compact />
          </View>

          <View style={styles.header}>
            <Image
              source={require('../../assets/logo.png')}
              style={styles.loginLogo}
              resizeMode="contain"
            />
            <Text style={[styles.title, { color: theme.colors.textPrimary }]}>
              {t('onboarding:loginTitle')}
            </Text>
            <Text style={[styles.subtitle, { color: theme.colors.textSecondary }]}>
              {t('onboarding:loginSubtitle')}
            </Text>
          </View>

          {authError && (
            <View style={[styles.errorBox, { backgroundColor: theme.colors.dangerLight }]}>
              <Ionicons name="alert-circle" size={18} color={theme.colors.danger} />
              <Text style={[styles.errorText, { color: theme.colors.danger }]}>
                {authError}
              </Text>
            </View>
          )}

          <View style={styles.form}>
            <Controller
              control={control}
              name="phoneOrEmail"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  autoCapitalize="none"
                  error={errors.phoneOrEmail?.message}
                  label={t('onboarding:phoneOrEmail')}
                  leftIcon={
                    <Ionicons
                      name="person-outline"
                      size={20}
                      color={theme.colors.textSecondary}
                    />
                  }
                  placeholder="Email or Mobile (+91...)"
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <Controller
              control={control}
              name="password"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  error={errors.password?.message}
                  label={t('onboarding:password')}
                  leftIcon={
                    <Ionicons
                      name="lock-closed-outline"
                      size={20}
                      color={theme.colors.textSecondary}
                    />
                  }
                  placeholder="••••••••"
                  secureTextEntry
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <TouchableOpacity
              style={styles.forgotPassword}
              onPress={() => router.push('/(auth)/forgot-password' as any)}
            >
              <Text style={[styles.forgotText, { color: theme.colors.primary }]}>
                {t('onboarding:forgotPassword')}
              </Text>
            </TouchableOpacity>

            <Button
              loading={loading}
              size="lg"
              style={styles.submitBtn}
              title={t('onboarding:loginButton')}
              variant="primary"
              onPress={() => handleSubmit(onSubmit)()}
            />

            <View style={styles.registerRow}>
              <Text style={[styles.noAccountText, { color: theme.colors.textSecondary }]}>
                {t('onboarding:dontHaveAccount')}
              </Text>
              <TouchableOpacity onPress={() => router.push('/(auth)/register' as any)}>
                <Text style={[styles.registerLink, { color: theme.colors.primary }]}>
                  {' '}{t('onboarding:registerNow')}
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 24,
    paddingBottom: 32,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
  },
  header: {
    marginTop: 16,
    marginBottom: 28,
  },
  loginLogo: {
    width: 68,
    height: 68,
    borderRadius: 16,
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
  errorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderRadius: 10,
    marginBottom: 16,
    gap: 8,
  },
  errorText: {
    fontSize: 13,
    fontWeight: '600',
    flex: 1,
  },
  form: {
    width: '100%',
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginBottom: 24,
    marginTop: -4,
  },
  forgotText: {
    fontSize: 13,
    fontWeight: '600',
  },
  submitBtn: {
    marginBottom: 20,
  },
  registerRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  noAccountText: {
    fontSize: 14,
  },
  registerLink: {
    fontSize: 14,
    fontWeight: '700',
  },
});
