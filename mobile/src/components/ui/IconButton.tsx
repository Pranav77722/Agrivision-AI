import React from 'react';
import {
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
  TouchableOpacityProps,
  ActivityIndicator,
} from 'react-native';
import { useTheme } from '../../hooks/useTheme';

export type IconButtonVariant = 'default' | 'primary' | 'surface' | 'ghost';

interface IconButtonProps extends TouchableOpacityProps {
  icon: React.ReactNode;
  variant?: IconButtonVariant;
  size?: number;
  loading?: boolean;
  style?: ViewStyle;
}

export const IconButton: React.FC<IconButtonProps> = ({
  icon,
  variant = 'surface',
  size = 40,
  loading = false,
  disabled = false,
  style,
  ...rest
}) => {
  const theme = useTheme();

  const getBackgroundColor = () => {
    if (variant === 'primary') return theme.colors.primary;
    if (variant === 'surface') return theme.colors.surface;
    if (variant === 'ghost') return 'transparent';
    return theme.colors.background;
  };

  return (
    <TouchableOpacity
      activeOpacity={0.7}
      disabled={disabled || loading}
      hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
      style={[
        styles.button,
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          backgroundColor: getBackgroundColor(),
          borderColor: theme.colors.border,
          borderWidth: variant === 'surface' ? 1 : 0,
        },
        variant === 'surface' ? theme.shadows.sm : undefined,
        style,
      ]}
      {...rest}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'primary' ? '#FFFFFF' : theme.colors.primary}
          size="small"
        />
      ) : (
        icon
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default IconButton;
