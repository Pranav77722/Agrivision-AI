import React from 'react';
import { View, Text, StyleSheet, StyleProp, ViewStyle, TextStyle, TouchableOpacity } from 'react-native';
import { useTheme } from '../../hooks/useTheme';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
  contentStyle?: StyleProp<ViewStyle>;
  headerStyle?: StyleProp<ViewStyle>;
  titleStyle?: StyleProp<TextStyle>;
  elevated?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  action,
  onPress,
  style,
  contentStyle,
  headerStyle,
  titleStyle,
  elevated = true,
}) => {
  const theme = useTheme();

  const ContainerComponent = onPress ? TouchableOpacity : View;

  return (
    <ContainerComponent
      activeOpacity={onPress ? 0.85 : 1}
      onPress={onPress}
      style={[
        styles.card,
        {
          backgroundColor: theme.colors.surface,
          borderColor: theme.colors.border,
          borderRadius: theme.borderRadius.xl,
        },
        elevated ? theme.shadows.sm : undefined,
        style as any,
      ]}
    >
      {(title || subtitle || action) && (
        <View
          style={[
            styles.header,
            {
              borderBottomColor: theme.colors.border,
              paddingHorizontal: theme.spacing.base,
              paddingTop: theme.spacing.base,
              paddingBottom: theme.spacing.sm,
            },
            headerStyle,
          ]}
        >
          <View style={styles.headerText}>
            {title && (
              <Text style={[styles.title, { color: theme.colors.textPrimary }, titleStyle]}>
                {title}
              </Text>
            )}
            {subtitle && (
              <Text
                style={[
                  styles.subtitle,
                  { color: theme.colors.textSecondary, marginTop: theme.spacing.xxs },
                ]}
              >
                {subtitle}
              </Text>
            )}
          </View>
          {action && <View style={styles.action}>{action}</View>}
        </View>
      )}
      <View style={[styles.content, { padding: theme.spacing.base }, contentStyle]}>
        {children}
      </View>
    </ContainerComponent>
  );
};

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    overflow: 'hidden',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerText: {
    flex: 1,
  },
  title: {
    fontSize: 17,
    fontWeight: '700',
  },
  subtitle: {
    fontSize: 13,
  },
  action: {
    marginLeft: 8,
  },
  content: {
    width: '100%',
  },
});

export default Card;
