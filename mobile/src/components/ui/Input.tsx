import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ViewStyle,
  TextStyle,
  TextInputProps,
  TouchableOpacity,
} from 'react-native';
import { useTheme } from '../../hooks/useTheme';

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  containerStyle?: ViewStyle;
  inputStyle?: TextStyle;
  labelStyle?: TextStyle;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  hint,
  leftIcon,
  rightIcon,
  containerStyle,
  inputStyle,
  labelStyle,
  secureTextEntry,
  ...rest
}) => {
  const theme = useTheme();
  const [isFocused, setIsFocused] = useState(false);
  const [isPasswordVisible, setIsPasswordVisible] = useState(!secureTextEntry);

  const hasError = Boolean(error);

  return (
    <View style={[styles.container, containerStyle]}>
      {label && (
        <Text
          style={[
            styles.label,
            {
              color: hasError
                ? theme.colors.danger
                : isFocused
                ? theme.colors.primary
                : theme.colors.textPrimary,
              marginBottom: theme.spacing.xs,
            },
            labelStyle,
          ]}
        >
          {label}
        </Text>
      )}

      <View
        style={[
          styles.inputWrapper,
          {
            backgroundColor: theme.colors.surface,
            borderColor: hasError
              ? theme.colors.danger
              : isFocused
              ? theme.colors.primary
              : theme.colors.border,
            borderRadius: theme.borderRadius.lg,
            paddingHorizontal: theme.spacing.md,
          },
        ]}
      >
        {leftIcon && <View style={[styles.iconWrapper, { marginRight: theme.spacing.sm }]}>{leftIcon}</View>}

        <TextInput
          placeholderTextColor={theme.colors.textMuted}
          secureTextEntry={secureTextEntry && !isPasswordVisible}
          style={[
            styles.input,
            {
              color: theme.colors.textPrimary,
              fontSize: theme.fontSize.base,
              paddingVertical: theme.spacing.md,
            },
            inputStyle,
          ]}
          onBlur={() => setIsFocused(false)}
          onFocus={() => setIsFocused(true)}
          {...rest}
        />

        {rightIcon ? (
          <View style={[styles.iconWrapper, { marginLeft: theme.spacing.sm }]}>{rightIcon}</View>
        ) : null}
      </View>

      {error ? (
        <Text style={[styles.error, { color: theme.colors.danger, marginTop: theme.spacing.xxs }]}>
          {error}
        </Text>
      ) : hint ? (
        <Text
          style={[styles.hint, { color: theme.colors.textSecondary, marginTop: theme.spacing.xxs }]}
        >
          {hint}
        </Text>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1.2,
    minHeight: 48,
  },
  input: {
    flex: 1,
    padding: 0,
  },
  iconWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  error: {
    fontSize: 12,
  },
  hint: {
    fontSize: 12,
  },
});

export default Input;
