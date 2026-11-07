import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { useTheme } from '../../hooks/useTheme';

export type BadgeVariant = 'success' | 'warning' | 'danger' | 'info' | 'default';

interface BadgeProps {
  label: string;
  variant?: BadgeVariant;
  icon?: React.ReactNode;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Badge: React.FC<BadgeProps> = ({
  label,
  variant = 'default',
  icon,
  style,
  textStyle,
}) => {
  const theme = useTheme();

  const getBadgeColors = () => {
    switch (variant) {
      case 'success':
        return {
          bg: theme.isDark ? '#064E3B' : theme.colors.successLight,
          text: theme.isDark ? '#34D399' : theme.colors.success,
        };
      case 'warning':
        return {
          bg: theme.isDark ? '#78350F' : theme.colors.warningLight,
          text: theme.isDark ? '#FBBF24' : '#B45309',
        };
      case 'danger':
        return {
          bg: theme.isDark ? '#7F1D1D' : theme.colors.dangerLight,
          text: theme.isDark ? '#F87171' : theme.colors.danger,
        };
      case 'info':
        return {
          bg: theme.isDark ? '#1E3A8A' : '#DBEAFE',
          text: theme.isDark ? '#60A5FA' : '#1D4ED8',
        };
      default:
        return {
          bg: theme.isDark ? '#334155' : '#F1F5F9',
          text: theme.colors.textSecondary,
        };
    }
  };

  const { bg, text } = getBadgeColors();

  return (
    <View
      style={[
        styles.badge,
        {
          backgroundColor: bg,
          borderRadius: theme.borderRadius.round,
          paddingHorizontal: theme.spacing.sm,
          paddingVertical: theme.spacing.xxs,
        },
        style,
      ]}
    >
      {icon && <View style={[styles.icon, { marginRight: theme.spacing.xxs }]}>{icon}</View>}
      <Text style={[styles.text, { color: text, fontSize: theme.fontSize.xs }, textStyle]}>
        {label}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
  },
  icon: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontWeight: '700',
    textTransform: 'uppercase',
  },
});

export default Badge;
