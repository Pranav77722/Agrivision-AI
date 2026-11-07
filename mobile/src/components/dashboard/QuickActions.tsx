import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../../hooks/useTheme';

export const QuickActions: React.FC = () => {
  const { t } = useTranslation('dashboard');
  const theme = useTheme();
  const router = useRouter();

  const actions = [
    {
      title: t('scanCrop'),
      icon: 'camera' as const,
      color: '#16A34A',
      bgColor: theme.isDark ? '#064E3B' : '#DCFCE7',
      onPress: () => router.push('/diagnosis/camera' as any),
    },
    {
      title: t('pestCheck'),
      icon: 'bug' as const,
      color: '#DC2626',
      bgColor: theme.isDark ? '#7F1D1D' : '#FEE2E2',
      onPress: () => router.push('/pest' as any),
    },
    {
      title: t('yieldPredict'),
      icon: 'trending-up' as const,
      color: '#2563EB',
      bgColor: theme.isDark ? '#1E3A8A' : '#DBEAFE',
      onPress: () => router.push('/yield' as any),
    },
    {
      title: t('aiAssistant'),
      icon: 'chatbubble-ellipses' as const,
      color: '#7C3AED',
      bgColor: theme.isDark ? '#4C1D95' : '#F3E8FF',
      onPress: () => router.push('/assistant' as any),
    },
  ];

  return (
    <View style={styles.container}>
      <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
        {t('quickActionsTitle')}
      </Text>
      <View style={styles.grid}>
        {actions.map((item, index) => (
          <TouchableOpacity
            key={index}
            activeOpacity={0.8}
            style={[
              styles.actionCard,
              {
                backgroundColor: theme.colors.surface,
                borderColor: theme.colors.border,
              },
              theme.shadows.sm,
            ]}
            onPress={item.onPress}
          >
            <View style={[styles.iconContainer, { backgroundColor: item.bgColor }]}>
              <Ionicons name={item.icon} size={24} color={item.color} />
            </View>
            <Text
              numberOfLines={2}
              style={[styles.actionLabel, { color: theme.colors.textPrimary }]}
            >
              {item.title}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 12,
  },
  grid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  actionCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 6,
    borderRadius: 14,
    borderWidth: 1,
  },
  iconContainer: {
    width: 46,
    height: 46,
    borderRadius: 23,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  actionLabel: {
    fontSize: 12,
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default QuickActions;
