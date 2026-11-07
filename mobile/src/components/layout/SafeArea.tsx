import React from 'react';
import { StyleSheet, ViewStyle } from 'react-native';
import { SafeAreaView, SafeAreaViewProps } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { useTheme } from '../../hooks/useTheme';

interface CustomSafeAreaProps extends SafeAreaViewProps {
  children: React.ReactNode;
  style?: ViewStyle;
}

export const SafeArea: React.FC<CustomSafeAreaProps> = ({ children, style, ...rest }) => {
  const theme = useTheme();

  return (
    <SafeAreaView
      edges={['top', 'left', 'right']}
      style={[
        styles.safeArea,
        { backgroundColor: theme.colors.background },
        style,
      ]}
      {...rest}
    >
      <StatusBar style={theme.isDark ? 'light' : 'dark'} />
      {children}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
});

export default SafeArea;
