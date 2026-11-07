import { lightColors, darkColors, ColorTheme, palette } from './colors';
import { spacing, borderRadius, Spacing, BorderRadius } from './spacing';
import { typography, fontSize, fontWeight } from './typography';
import { getShadows, ShadowStyle } from './shadows';

export interface AppTheme {
  isDark: boolean;
  colors: ColorTheme;
  spacing: Spacing;
  borderRadius: BorderRadius;
  typography: typeof typography;
  fontSize: typeof fontSize;
  fontWeight: typeof fontWeight;
  shadows: ShadowStyle;
}

export const getTheme = (isDark: boolean): AppTheme => ({
  isDark,
  colors: isDark ? darkColors : lightColors,
  spacing,
  borderRadius,
  typography,
  fontSize,
  fontWeight,
  shadows: getShadows(isDark),
});

export { lightColors, darkColors, palette, spacing, borderRadius, typography, fontSize, fontWeight, getShadows };
