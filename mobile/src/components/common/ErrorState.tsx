import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../hooks/useTheme';
import { Button } from '../ui/Button';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
  style?: ViewStyle;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message, onRetry, style }) => {
  const { t } = useTranslation('common');
  const theme = useTheme();

  return (
    <View style={[styles.container, style]}>
      <View
        style={[
          styles.iconCircle,
          {
            backgroundColor: theme.isDark ? '#450A0A' : theme.colors.dangerLight,
            marginBottom: theme.spacing.base,
          },
        ]}
      >
        <Ionicons name="alert-circle-outline" size={48} color={theme.colors.danger} />
      </View>
      <Text style={[styles.title, { color: theme.colors.textPrimary }]}>{t('error')}</Text>
      <Text
        style={[
          styles.message,
          {
            color: theme.colors.textSecondary,
            marginTop: theme.spacing.xs,
            marginBottom: theme.spacing.lg,
          },
        ]}
      >
        {message || t('networkError')}
      </Text>
      {onRetry && (
        <Button
          icon={<Ionicons name="refresh" size={18} color="#FFFFFF" />}
          size="md"
          title={t('retry')}
          variant="primary"
          onPress={onRetry}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
    width: '100%',
  },
  iconCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
  },
  message: {
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
    maxWidth: 280,
  },
});

export default ErrorState;
