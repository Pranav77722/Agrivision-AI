import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Input } from '../../src/components/ui/Input';
import { Button } from '../../src/components/ui/Button';
import { registerSchema, RegisterFormData } from '../../src/utils/validators';
import { useAuthStore } from '../../src/store/authStore';
import { authService } from '../../src/services/authService';
import { useTheme } from '../../src/hooks/useTheme';

export default function RegisterScreen() {
  const { t } = useTranslation(['onboarding', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const registerToStore = useAuthStore((s) => s.register);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [acres, setAcres] = useState('5');
  const [selectedCrops, setSelectedCrops] = useState<string[]>(['Tomato', 'Soybean']);

  const cropOptions = ['Tomato', 'Soybean', 'Onion', 'Wheat', 'Sugarcane', 'Cotton', 'Pomegranate', 'Maize'];

  const toggleCrop = (crop: string) => {
    if (selectedCrops.includes(crop)) {
      if (selectedCrops.length > 1) {
        setSelectedCrops(selectedCrops.filter((c) => c !== crop));
      }
    } else {
      setSelectedCrops([...selectedCrops, crop]);
    }
  };

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      fullName: '',
      phoneNumber: '',
      email: '',
      password: '',
      confirmPassword: '',
      village: 'Gunjalwadi',
      district: 'Sangamner, Ahilyanagar',
      state: 'Maharashtra',
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const response = await authService.register({
        fullName: data.fullName,
        phoneNumber: data.phoneNumber,
        email: data.email || undefined,
        password: data.password,
        village: data.village || 'Gunjalwadi',
        district: data.district || 'Sangamner, Ahilyanagar',
        state: data.state || 'Maharashtra',
        totalAcres: parseFloat(acres) || 5,
        primaryCrops: selectedCrops,
      });
      await registerToStore(response.accessToken, response.refreshToken, response.user);
      router.replace('/(tabs)');
    } catch {
      setErrorMsg(t('common:networkError'));
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
          <TouchableOpacity
            accessibilityRole="button"
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            style={styles.backBtn}
            onPress={() => router.back()}
          >
            <Ionicons name="arrow-back" size={24} color={theme.colors.textPrimary} />
          </TouchableOpacity>

          <View style={styles.header}>
            <Text style={[styles.title, { color: theme.colors.textPrimary }]}>
              {t('onboarding:registerTitle')}
            </Text>
            <Text style={[styles.subtitle, { color: theme.colors.textSecondary }]}>
              {t('onboarding:registerSubtitle')}
            </Text>
          </View>

          {errorMsg && (
            <View style={[styles.errorBox, { backgroundColor: theme.colors.dangerLight }]}>
              <Ionicons name="alert-circle" size={18} color={theme.colors.danger} />
              <Text style={[styles.errorText, { color: theme.colors.danger }]}>{errorMsg}</Text>
            </View>
          )}

          <View style={styles.form}>
            <Controller
              control={control}
              name="fullName"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  error={errors.fullName?.message}
                  label={t('onboarding:fullName')}
                  leftIcon={
                    <Ionicons name="person-outline" size={20} color={theme.colors.textSecondary} />
                  }
                  placeholder="e.g. Ramesh Patil"
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <Controller
              control={control}
              name="phoneNumber"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  error={errors.phoneNumber?.message}
                  keyboardType="phone-pad"
                  label={t('onboarding:phoneNumber')}
                  leftIcon={
                    <Ionicons name="call-outline" size={20} color={theme.colors.textSecondary} />
                  }
                  placeholder="+91 98765 43210"
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <Controller
              control={control}
              name="email"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  autoCapitalize="none"
                  error={errors.email?.message}
                  keyboardType="email-address"
                  label={t('onboarding:emailOptional')}
                  leftIcon={
                    <Ionicons name="mail-outline" size={20} color={theme.colors.textSecondary} />
                  }
                  placeholder="farmer@example.com"
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <Controller
              control={control}
              name="village"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  error={errors.village?.message}
                  label={t('onboarding:village')}
                  leftIcon={
                    <Ionicons name="home-outline" size={20} color={theme.colors.textSecondary} />
                  }
                  placeholder="e.g. Baramati"
                  value={value}
                  onBlur={onBlur}
                  onChangeText={onChange}
                />
              )}
            />

            <View style={styles.row}>
              <View style={styles.halfCol}>
                <Controller
                  control={control}
                  name="district"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <Input
                      error={errors.district?.message}
                      label={t('onboarding:district')}
                      placeholder="e.g. Pune"
                      value={value}
                      onBlur={onBlur}
                      onChangeText={onChange}
                    />
                  )}
                />
              </View>

              <View style={styles.halfCol}>
                <Controller
                  control={control}
                  name="state"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <Input
                      error={errors.state?.message}
                      label={t('onboarding:state')}
                      placeholder="Maharashtra"
                      value={value}
                      onBlur={onBlur}
                      onChangeText={onChange}
                    />
                  )}
                />
              </View>
            </View>

            {/* Farm Land & Crops Section */}
            <View style={{ marginBottom: 16 }}>
              <Input
                keyboardType="numeric"
                label="Farm Land Area (Acres)"
                leftIcon={
                  <Ionicons name="leaf-outline" size={20} color={theme.colors.textSecondary} />
                }
                placeholder="e.g. 5"
                value={acres}
                onChangeText={setAcres}
              />

              <Text style={{ fontSize: 13, fontWeight: '600', color: theme.colors.textPrimary, marginBottom: 8, marginTop: 4 }}>
                Primary Crops Grown
              </Text>
              <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
                {cropOptions.map((crop) => {
                  const isSel = selectedCrops.includes(crop);
                  return (
                    <TouchableOpacity
                      key={crop}
                      activeOpacity={0.8}
                      onPress={() => toggleCrop(crop)}
                      style={{
                        paddingHorizontal: 12,
                        paddingVertical: 6,
                        borderRadius: 20,
                        backgroundColor: isSel ? theme.colors.primary : theme.colors.surface,
                        borderWidth: 1,
                        borderColor: isSel ? theme.colors.primary : theme.colors.border,
                      }}
                    >
                      <Text
                        style={{
                          fontSize: 12,
                          fontWeight: '600',
                          color: isSel ? '#FFFFFF' : theme.colors.textSecondary,
                        }}
                      >
                        {isSel ? '✓ ' : ''}{crop}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

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

            <Controller
              control={control}
              name="confirmPassword"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  error={errors.confirmPassword?.message}
                  label={t('onboarding:confirmPassword')}
                  leftIcon={
                    <Ionicons
                      name="shield-checkmark-outline"
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

            <Button
              loading={loading}
              size="lg"
              style={styles.submitBtn}
              title={t('onboarding:registerButton')}
              variant="primary"
              onPress={() => handleSubmit(onSubmit)()}
            />

            <View style={styles.loginRow}>
              <Text style={[styles.haveAccountText, { color: theme.colors.textSecondary }]}>
                {t('onboarding:alreadyHaveAccount')}
              </Text>
              <TouchableOpacity onPress={() => router.push('/(auth)/login' as any)}>
                <Text style={[styles.loginLink, { color: theme.colors.primary }]}>
                  {' '}{t('onboarding:loginHere')}
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
    paddingBottom: 40,
  },
  backBtn: {
    paddingVertical: 12,
  },
  header: {
    marginTop: 8,
    marginBottom: 24,
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
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  halfCol: {
    flex: 1,
  },
  submitBtn: {
    marginTop: 8,
    marginBottom: 16,
  },
  loginRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  haveAccountText: {
    fontSize: 14,
  },
  loginLink: {
    fontSize: 14,
    fontWeight: '700',
  },
});
