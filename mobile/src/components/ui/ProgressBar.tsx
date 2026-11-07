import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { useTheme } from '../../hooks/useTheme';

interface ProgressBarProps {
  progress: number; // 0 to 100
  height?: number;
  color?: string;
  trackColor?: string;
  style?: ViewStyle;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  height = 8,
  color,
  trackColor,
  style,
}) => {
  const theme = useTheme();

  const clamped = Math.min(100, Math.max(0, progress));
  const fillColor = color || theme.colors.secondary;
  const barTrack = trackColor || (theme.isDark ? '#334155' : '#E2E8F0');

  return (
    <View
      style={[
        styles.track,
        {
          height,
          backgroundColor: barTrack,
          borderRadius: height / 2,
        },
        style,
      ]}
    >
      <View
        style={[
          styles.fill,
          {
            width: `${clamped}%`,
            height,
            backgroundColor: fillColor,
            borderRadius: height / 2,
          },
        ]}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  track: {
    width: '100%',
    overflow: 'hidden',
  },
  fill: {
    height: '100%',
  },
});

export default ProgressBar;
