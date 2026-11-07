import React from 'react';
import {
  ScrollView,
  View,
  StyleSheet,
  ViewStyle,
  RefreshControl,
  ScrollViewProps,
} from 'react-native';
import { useTheme } from '../../hooks/useTheme';

interface ContainerProps extends ScrollViewProps {
  children: React.ReactNode;
  scrollable?: boolean;
  padding?: boolean;
  refreshing?: boolean;
  onRefresh?: () => void;
  style?: ViewStyle;
  contentContainerStyle?: ViewStyle;
}

export const Container: React.FC<ContainerProps> = ({
  children,
  scrollable = true,
  padding = true,
  refreshing = false,
  onRefresh,
  style,
  contentContainerStyle,
  ...rest
}) => {
  const theme = useTheme();

  const containerPadding = padding ? theme.spacing.base : 0;

  if (!scrollable) {
    return (
      <View
        style={[
          styles.container,
          {
            backgroundColor: theme.colors.background,
            padding: containerPadding,
          },
          style,
        ]}
      >
        {children}
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={[
        styles.scrollContent,
        { padding: containerPadding },
        contentContainerStyle,
      ]}
      refreshControl={
        onRefresh ? (
          <RefreshControl
            colors={[theme.colors.primary]}
            refreshing={refreshing}
            tintColor={theme.colors.primary}
            onRefresh={onRefresh}
          />
        ) : undefined
      }
      showsVerticalScrollIndicator={false}
      style={[styles.container, { backgroundColor: theme.colors.background }, style]}
      {...rest}
    >
      {children}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
  },
});

export default Container;
