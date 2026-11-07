import React from 'react';
import {
  TouchableOpacity,
  Text,
  ActivityIndicator,
  StyleSheet,
  ViewStyle,
  TextStyle,
  TouchableOpacityProps,
} from 'react-native';
import { useTheme } from '../../hooks/useTheme';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon,
  iconPosition = 'left',
  style,
  textStyle,
  ...rest
}) => {
  const theme = useTheme();

  const getContainerStyles = (): ViewStyle => {
    let bg = theme.colors.primary;
    let borderColor = 'transparent';
    let borderWidth = 0;

    if (variant === 'secondary') {
      bg = theme.colors.secondary;
    } else if (variant === 'outline') {
      bg = 'transparent';
      borderColor = theme.colors.primary;
      borderWidth = 1.5;
    } else if (variant === 'danger') {
      bg = theme.colors.danger;
    } else if (variant === 'ghost') {
      bg = 'transparent';
    }

    if (disabled || loading) {
      bg = variant === 'outline' || variant === 'ghost' ? 'transparent' : theme.colors.border;
      borderColor = theme.colors.border;
    }

    let paddingVertical: number = theme.spacing.md;
    let paddingHorizontal: number = theme.spacing.lg;

    if (size === 'sm') {
      paddingVertical = theme.spacing.sm;
      paddingHorizontal = theme.spacing.md;
    } else if (size === 'lg') {
      paddingVertical = theme.spacing.base;
      paddingHorizontal = theme.spacing.xl;
    }

    return {
      backgroundColor: bg,
      borderColor,
      borderWidth,
      paddingVertical,
      paddingHorizontal,
      borderRadius: theme.borderRadius.lg,
    };
  };

  const getTextColor = (): string => {
    if (disabled || loading) {
      return theme.colors.textMuted;
    }
    if (variant === 'outline' || variant === 'ghost') {
      return theme.colors.primary;
    }
    if (variant === 'secondary') {
      return '#0F3A1E'; // High contrast dark green on bright green
    }
    return '#FFFFFF';
  };

  const textColor = getTextColor();

  return (
    <TouchableOpacity
      activeOpacity={0.8}
      disabled={disabled || loading}
      style={[styles.base, getContainerStyles(), style]}
      {...rest}
    >
      {loading ? (
        <ActivityIndicator color={textColor} size="small" />
      ) : (
        <>
          {icon && iconPosition === 'left' && <>{icon}</>}
          <Text
            style={[
              styles.text,
              {
                color: textColor,
                fontSize: size === 'sm' ? theme.fontSize.sm : size === 'lg' ? theme.fontSize.lg : theme.fontSize.base,
                marginLeft: icon && iconPosition === 'left' ? theme.spacing.sm : 0,
                marginRight: icon && iconPosition === 'right' ? theme.spacing.sm : 0,
              },
              textStyle,
            ]}
          >
            {title}
          </Text>
          {icon && iconPosition === 'right' && <>{icon}</>}
        </>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default Button;
