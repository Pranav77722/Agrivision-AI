import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet, ViewStyle } from 'react-native';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../hooks/useTheme';

interface LoadingSpinnerProps {
  message?: string;
  size?: 'small' | 'large';
  fullScreen?: boolean;
  style?: ViewStyle;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message,
  size = 'large',
  fullScreen = false,
  style,
}) => {
  const { t } = useTranslation('common');
  const theme = useTheme();

  return (
    <View
      style={[
        styles.container,
        fullScreen && styles.fullScreen,
        { backgroundColor: fullScreen ? theme.colors.background : 'transparent' },
        style,
      ]}
    >
      <ActivityIndicator color={theme.colors.primary} size={size} />
      <Text
        style={[
          styles.text,
          {
            color: theme.colors.textSecondary,
            fontSize: theme.fontSize.base,
            marginTop: theme.spacing.md,
          },
        ]}
      >
        {message || t('loading')}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  fullScreen: {
    flex: 1,
  },
  text: {
    fontWeight: '500',
  },
});

export default LoadingSpinner;
