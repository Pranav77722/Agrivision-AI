import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, Switch, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Container } from '../../src/components/layout/Container';
import { Card } from '../../src/components/ui/Card';
import { Avatar } from '../../src/components/ui/Avatar';
import { Button } from '../../src/components/ui/Button';
import { Divider } from '../../src/components/ui/Divider';
import { LanguageSelector } from '../../src/components/common/LanguageSelector';
import { useAuthStore } from '../../src/store/authStore';
import { useTheme } from '../../src/hooks/useTheme';

export default function ProfileTabScreen() {
  const { t } = useTranslation(['profile', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  const handleLogout = () => {
    Alert.alert(t('profile:logout'), t('profile:logoutConfirm'), [
      { text: t('common:cancel'), style: 'cancel' },
      {
        text: t('profile:logout'),
        style: 'destructive',
        onPress: async () => {
          await logout();
          router.replace('/(auth)/welcome' as any);
        },
      },
    ]);
  };

  return (
    <SafeArea style={styles.safeArea}>
      <View
        style={[
          styles.headerBar,
          {
            backgroundColor: theme.colors.surface,
            borderBottomColor: theme.colors.border,
          },
        ]}
      >
        <Text style={[styles.screenTitle, { color: theme.colors.textPrimary }]}>
          {t('profile:title')}
        </Text>
        <Text style={[styles.screenSubtitle, { color: theme.colors.textSecondary }]}>
          {t('profile:subtitle')}
        </Text>
      </View>

      <Container contentContainerStyle={styles.containerContent}>
        {/* User Card */}
        <Card style={styles.userCard}>
          <View style={styles.userRow}>
            <Avatar name={user?.fullName || 'Kisan'} size={60} />
            <View style={styles.userInfo}>
              <Text style={[styles.userName, { color: theme.colors.textPrimary }]}>
                {user?.fullName || 'Ramesh Patil'}
              </Text>
              <Text style={[styles.userPhone, { color: theme.colors.textSecondary }]}>
                {user?.phoneNumber || '+91 98765 43210'}
              </Text>
              <Text style={[styles.userLocation, { color: theme.colors.primary }]}>
                {user?.village ? `${user.village}, ${user.district}, ${user.state}` : 'Pune, Maharashtra'}
              </Text>
            </View>
          </View>
        </Card>

        {/* Farm Details Card */}
        <Card title={t('profile:farmDetailsHeader')} style={styles.card}>
          <View style={styles.detailRow}>
            <Text style={[styles.detailLabel, { color: theme.colors.textSecondary }]}>
              {t('profile:totalAcres')}
            </Text>
            <Text style={[styles.detailValue, { color: theme.colors.textPrimary }]}>
              {t('profile:acresUnit', { count: user?.totalAcres || 5 })}
            </Text>
          </View>
          <Divider />
          <View style={styles.detailRow}>
            <Text style={[styles.detailLabel, { color: theme.colors.textSecondary }]}>
              {t('profile:primaryCrops')}
            </Text>
            <Text style={[styles.detailValue, { color: theme.colors.textPrimary }]}>
              {user?.primaryCrops && user.primaryCrops.length > 0
                ? user.primaryCrops.join(', ')
                : 'Tomato, Soybean, Wheat'}
            </Text>
          </View>
        </Card>

        {/* Language Selection Card */}
        <Card subtitle={t('profile:languageSubtitle')} title={t('profile:language')} style={styles.card}>
          <LanguageSelector />
        </Card>

        {/* App Preferences (Theme & Notifications) */}
        <Card title={t('profile:appPreferencesHeader')} style={styles.card}>
          <View style={styles.prefRow}>
            <View style={styles.prefLeft}>
              <Ionicons
                name={theme.isDark ? 'moon' : 'sunny'}
                size={22}
                color={theme.colors.primary}
              />
              <View>
                <Text style={[styles.prefTitle, { color: theme.colors.textPrimary }]}>
                  {theme.isDark ? t('profile:themeDark') : t('profile:themeLight')}
                </Text>
                <Text style={[styles.prefSub, { color: theme.colors.textSecondary }]}>
                  {t('profile:theme')}
                </Text>
              </View>
            </View>
            <Switch
              thumbColor="#FFFFFF"
              trackColor={{ false: '#CBD5E1', true: theme.colors.primary }}
              value={theme.isDark}
              onValueChange={theme.toggleTheme}
            />
          </View>

          <Divider />

          <View style={styles.prefRow}>
            <View style={styles.prefLeft}>
              <Ionicons name="notifications-outline" size={22} color={theme.colors.primary} />
              <View>
                <Text style={[styles.prefTitle, { color: theme.colors.textPrimary }]}>
                  {t('profile:notifications')}
                </Text>
                <Text style={[styles.prefSub, { color: theme.colors.textSecondary }]}>
                  {t('profile:notificationsSubtitle')}
                </Text>
              </View>
            </View>
            <Switch
              thumbColor="#FFFFFF"
              trackColor={{ false: '#CBD5E1', true: theme.colors.primary }}
              value={notificationsEnabled}
              onValueChange={setNotificationsEnabled}
            />
          </View>
        </Card>

        {/* Navigation Quick Links (Reports, Archive, AI Assistant) */}
        <Card style={styles.card}>
          <TouchableOpacity
            style={styles.navLink}
            onPress={() => router.push('/archive' as any)}
          >
            <View style={styles.linkLeft}>
              <Ionicons name="time-outline" size={20} color={theme.colors.textPrimary} />
              <Text style={[styles.linkText, { color: theme.colors.textPrimary }]}>
                {t('profile:farmDetailsHeader')} Archive
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={theme.colors.textMuted} />
          </TouchableOpacity>

          <Divider />

          <TouchableOpacity
            style={styles.navLink}
            onPress={() => router.push('/reports' as any)}
          >
            <View style={styles.linkLeft}>
              <Ionicons name="document-text-outline" size={20} color={theme.colors.textPrimary} />
              <Text style={[styles.linkText, { color: theme.colors.textPrimary }]}>
                {t('common:download')} Reports
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={theme.colors.textMuted} />
          </TouchableOpacity>
        </Card>

        {/* Logout Button */}
        <Button
          icon={<Ionicons name="log-out-outline" size={20} color="#FFFFFF" />}
          size="lg"
          style={styles.logoutBtn}
          title={t('profile:logout')}
          variant="danger"
          onPress={handleLogout}
        />

        {/* About App Card with Logo */}
        <Card style={styles.aboutCard}>
          <View style={styles.aboutRow}>
            <Image
              source={require('../../assets/logo.png')}
              style={styles.aboutLogo}
              resizeMode="contain"
            />
            <View style={styles.aboutContent}>
              <Text style={[styles.aboutTitle, { color: theme.colors.textPrimary }]}>
                Agrivision AI+
              </Text>
              <Text style={[styles.aboutTagline, { color: theme.colors.primary }]}>
                Smart Farming with AI
              </Text>
              <Text style={[styles.aboutDesc, { color: theme.colors.textSecondary }]}>
                AI-driven crop diagnosis, pest detection & yield analytics for Indian farmers.
              </Text>
            </View>
          </View>
        </Card>

        {/* App Version Info */}
        <Text style={[styles.versionText, { color: theme.colors.textMuted }]}>
          {t('profile:appVersion', { version: '1.0.0 (Build 42)' })}
        </Text>
      </Container>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  headerBar: {
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  screenTitle: {
    fontSize: 22,
    fontWeight: '800',
  },
  screenSubtitle: {
    fontSize: 13,
    marginTop: 4,
    lineHeight: 18,
  },
  containerContent: {
    paddingBottom: 110,
  },
  userCard: {
    marginVertical: 10,
  },
  userRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    fontSize: 18,
    fontWeight: '800',
  },
  userPhone: {
    fontSize: 13,
    marginTop: 2,
  },
  userLocation: {
    fontSize: 12,
    fontWeight: '600',
    marginTop: 4,
  },
  card: {
    marginVertical: 8,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 4,
  },
  detailLabel: {
    fontSize: 14,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '700',
  },
  prefRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 6,
  },
  prefLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  prefTitle: {
    fontSize: 15,
    fontWeight: '700',
  },
  prefSub: {
    fontSize: 12,
    marginTop: 2,
  },
  navLink: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  linkLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  linkText: {
    fontSize: 14,
    fontWeight: '600',
  },
  logoutBtn: {
    marginTop: 16,
    marginBottom: 16,
  },
  aboutCard: {
    marginVertical: 12,
    padding: 16,
  },
  aboutRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  aboutLogo: {
    width: 60,
    height: 60,
    borderRadius: 14,
  },
  aboutContent: {
    flex: 1,
  },
  aboutTitle: {
    fontSize: 16,
    fontWeight: '800',
  },
  aboutTagline: {
    fontSize: 12,
    fontWeight: '700',
    marginTop: 2,
  },
  aboutDesc: {
    fontSize: 11.5,
    marginTop: 4,
    lineHeight: 16,
  },
  versionText: {
    textAlign: 'center',
    fontSize: 12,
    marginBottom: 8,
  },
});
