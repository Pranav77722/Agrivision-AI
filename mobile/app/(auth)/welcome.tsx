import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  FlatList,
  TouchableOpacity,
  NativeSyntheticEvent,
  NativeScrollEvent,
  Image,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Button } from '../../src/components/ui/Button';
import { LanguageSelector } from '../../src/components/common/LanguageSelector';
import { useTheme } from '../../src/hooks/useTheme';

const { width } = Dimensions.get('window');

export default function WelcomeScreen() {
  const { t } = useTranslation(['onboarding', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const [activeIndex, setActiveIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);

  const slides = [
    {
      id: '1',
      icon: 'leaf' as const,
      iconColor: '#16A34A',
      title: t('onboarding:slide1Title'),
      desc: t('onboarding:slide1Desc'),
    },
    {
      id: '2',
      icon: 'shield-half' as const,
      iconColor: '#DC2626',
      title: t('onboarding:slide2Title'),
      desc: t('onboarding:slide2Desc'),
    },
    {
      id: '3',
      icon: 'trending-up' as const,
      iconColor: '#2563EB',
      title: t('onboarding:slide3Title'),
      desc: t('onboarding:slide3Desc'),
    },
  ];

  const handleScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const slideIndex = Math.round(event.nativeEvent.contentOffset.x / width);
    setActiveIndex(slideIndex);
  };

  const handleNext = () => {
    if (activeIndex < slides.length - 1) {
      flatListRef.current?.scrollToIndex({ index: activeIndex + 1, animated: true });
    } else {
      router.push('/(auth)/login' as any);
    }
  };

  return (
    <SafeArea style={styles.safeArea}>
      <View style={styles.header}>
        <View style={styles.logoRow}>
          <Image
            source={require('../../assets/logo.png')}
            style={styles.headerLogo}
            resizeMode="contain"
          />
          <Text style={[styles.brandName, { color: theme.colors.primary }]}>
            {t('common:appName')}
          </Text>
        </View>

        <LanguageSelector compact />
      </View>

      <FlatList
        ref={flatListRef}
        data={slides}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onMomentumScrollEnd={handleScroll}
        renderItem={({ item }) => (
          <View style={[styles.slide, { width }]}>
            <View
              style={[
                styles.illustrationCircle,
                {
                  backgroundColor: theme.isDark ? '#1A2F25' : '#DCFCE7',
                  borderColor: theme.isDark ? '#234E35' : '#BBF7D0',
                },
              ]}
            >
              <Ionicons name={item.icon} size={72} color={item.iconColor} />
            </View>
            <Text style={[styles.slideTitle, { color: theme.colors.textPrimary }]}>
              {item.title}
            </Text>
            <Text style={[styles.slideDesc, { color: theme.colors.textSecondary }]}>
              {item.desc}
            </Text>
          </View>
        )}
        keyExtractor={(item) => item.id}
      />

      {/* Pagination dots */}
      <View style={styles.pagination}>
        {slides.map((_, index) => (
          <View
            key={index}
            style={[
              styles.dot,
              {
                backgroundColor:
                  activeIndex === index ? theme.colors.primary : theme.colors.border,
                width: activeIndex === index ? 24 : 8,
              },
            ]}
          />
        ))}
      </View>

      <View style={[styles.footer, { paddingHorizontal: theme.spacing.xl }]}>
        <Button
          size="lg"
          title={activeIndex === slides.length - 1 ? t('onboarding:getStarted') : t('common:next')}
          variant="primary"
          onPress={handleNext}
        />

        <View style={styles.loginRow}>
          <Text style={[styles.accountPrompt, { color: theme.colors.textSecondary }]}>
            {t('onboarding:alreadyHaveAccount')}
          </Text>
          <TouchableOpacity onPress={() => router.push('/(auth)/login' as any)}>
            <Text style={[styles.loginLink, { color: theme.colors.primary }]}>
              {' '}{t('onboarding:loginHere')}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerLogo: {
    width: 36,
    height: 36,
    borderRadius: 8,
  },
  brandName: {
    fontSize: 18,
    fontWeight: '800',
    letterSpacing: -0.3,
  },
  slide: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  illustrationCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 32,
  },
  slideTitle: {
    fontSize: 24,
    fontWeight: '800',
    textAlign: 'center',
    marginBottom: 12,
    lineHeight: 30,
  },
  slideDesc: {
    fontSize: 15,
    textAlign: 'center',
    lineHeight: 22,
    maxWidth: 300,
  },
  pagination: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 16,
    gap: 6,
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  footer: {
    paddingBottom: 24,
    gap: 14,
  },
  loginRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  accountPrompt: {
    fontSize: 14,
  },
  loginLink: {
    fontSize: 14,
    fontWeight: '700',
  },
});
