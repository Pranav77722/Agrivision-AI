import { Platform, ViewStyle } from 'react-native';

export interface ShadowStyle {
  sm: ViewStyle;
  md: ViewStyle;
  lg: ViewStyle;
}

export const getShadows = (isDark: boolean): ShadowStyle => {
  const shadowColor = isDark ? '#000000' : '#0F172A';
  const shadowOpacity = isDark ? 0.4 : 0.08;

  if (Platform.OS === 'android') {
    return {
      sm: { elevation: 2 },
      md: { elevation: 4 },
      lg: { elevation: 8 },
    };
  }

  return {
    sm: {
      shadowColor,
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity,
      shadowRadius: 2,
    },
    md: {
      shadowColor,
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: shadowOpacity * 1.2,
      shadowRadius: 6,
    },
    lg: {
      shadowColor,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: shadowOpacity * 1.5,
      shadowRadius: 12,
    },
  };
};
