import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { useTheme } from '../../hooks/useTheme';

interface DividerProps {
  text?: string;
  style?: ViewStyle;
}

export const Divider: React.FC<DividerProps> = ({ text, style }) => {
  const theme = useTheme();

  if (text) {
    return (
      <View style={[styles.containerWithText, { marginVertical: theme.spacing.md }, style]}>
        <View style={[styles.line, { backgroundColor: theme.colors.border }]} />
        <Text
          style={[
            styles.text,
            {
              color: theme.colors.textMuted,
              paddingHorizontal: theme.spacing.sm,
              fontSize: theme.fontSize.xs,
            },
          ]}
        >
          {text}
        </Text>
        <View style={[styles.line, { backgroundColor: theme.colors.border }]} />
      </View>
    );
  }

  return (
    <View
      style={[
        styles.simpleLine,
        {
          backgroundColor: theme.colors.border,
          marginVertical: theme.spacing.sm,
        },
        style,
      ]}
    />
  );
};

const styles = StyleSheet.create({
  simpleLine: {
    height: 1,
    width: '100%',
  },
  containerWithText: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
  },
  line: {
    flex: 1,
    height: 1,
  },
  text: {
    fontWeight: '500',
    textTransform: 'uppercase',
  },
});

export default Divider;
