export interface ColorTheme {
  primary: string;
  primaryDark: string;
  primaryLight: string;
  secondary: string;
  secondaryLight: string;
  background: string;
  surface: string;
  surfaceElevated: string;
  border: string;
  textPrimary: string;
  textSecondary: string;
  textMuted: string;
  warning: string;
  warningLight: string;
  danger: string;
  dangerLight: string;
  success: string;
  successLight: string;
  white: string;
  black: string;
  card: string;
  shadow: string;
  tint: string;
  tabIconDefault: string;
  tabIconSelected: string;
}

export const lightColors: ColorTheme = {
  primary: '#14532D',
  primaryDark: '#0D361D',
  primaryLight: '#DCFCE7',
  secondary: '#22C55E',
  secondaryLight: '#86EFAC',
  background: '#F8FAFC',
  surface: '#FFFFFF',
  surfaceElevated: '#FFFFFF',
  border: '#E2E8F0',
  textPrimary: '#172033',
  textSecondary: '#64748B',
  textMuted: '#94A3B8',
  warning: '#F59E0B',
  warningLight: '#FEF3C7',
  danger: '#DC2626',
  dangerLight: '#FEE2E2',
  success: '#16A34A',
  successLight: '#DCFCE7',
  white: '#FFFFFF',
  black: '#000000',
  card: '#FFFFFF',
  shadow: '#000000',
  tint: '#14532D',
  tabIconDefault: '#94A3B8',
  tabIconSelected: '#14532D',
};

export const darkColors: ColorTheme = {
  primary: '#22C55E',
  primaryDark: '#16A34A',
  primaryLight: '#052E16',
  secondary: '#4ADE80',
  secondaryLight: '#86EFAC',
  background: '#0B1220',
  surface: '#1A2332',
  surfaceElevated: '#243044',
  border: '#2D3B4F',
  textPrimary: '#F1F5F9',
  textSecondary: '#94A3B8',
  textMuted: '#64748B',
  warning: '#FBBF24',
  warningLight: '#451A03',
  danger: '#EF4444',
  dangerLight: '#450A0A',
  success: '#22C55E',
  successLight: '#052E16',
  white: '#FFFFFF',
  black: '#000000',
  card: '#1A2332',
  shadow: '#000000',
  tint: '#22C55E',
  tabIconDefault: '#64748B',
  tabIconSelected: '#22C55E',
};

export const palette = {
  primaryGreen: '#14532D',
  secondaryGreen: '#22C55E',
  lightGreen: '#DCFCE7',
  darkBg: '#0B1220',
  white: '#FFFFFF',
  lightBg: '#F8FAFC',
  primaryText: '#172033',
  secondaryText: '#64748B',
  warning: '#F59E0B',
  danger: '#DC2626',
  success: '#16A34A',
};
