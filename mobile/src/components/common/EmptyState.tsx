import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../../hooks/useTheme';
import { Button } from '../ui/Button';

interface EmptyStateProps {
  icon?: keyof typeof Ionicons.glyphMap;
  title: string;
  description?: string;
  actionTitle?: string;
  onAction?: () => void;
  style?: ViewStyle;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon = 'leaf-outline',
  title,
  description,
  actionTitle,
  onAction,
  style,
}) => {
  const theme = useTheme();

  return (
    <View style={[styles.container, style]}>
      <View
        style={[
          styles.iconCircle,
          {
            backgroundColor: theme.colors.primaryLight,
            marginBottom: theme.spacing.base,
          },
        ]}
      >
        <Ionicons name={icon} size={48} color={theme.colors.primary} />
      </View>
      <Text
        style={[
          styles.title,
          {
            color: theme.colors.textPrimary,
            marginBottom: theme.spacing.xs,
          },
        ]}
      >
        {title}
      </Text>
      {description && (
        <Text
          style={[
            styles.description,
            {
              color: theme.colors.textSecondary,
              marginBottom: actionTitle ? theme.spacing.lg : 0,
            },
          ]}
        >
          {description}
        </Text>
      )}
      {actionTitle && onAction && (
        <Button
          size="md"
          title={actionTitle}
          variant="primary"
          onPress={onAction}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
    width: '100%',
  },
  iconCircle: {
    width: 88,
    height: 88,
    borderRadius: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    textAlign: 'center',
  },
  description: {
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
    maxWidth: 280,
  },
});

export default EmptyState;
