import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
  Modal,
  Pressable,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLanguage } from '../../hooks/useLanguage';
import { useTheme } from '../../hooks/useTheme';
import { SupportedLanguage } from '../../i18n';

interface LanguageSelectorProps {
  compact?: boolean;
  variant?: 'pill' | 'segmented' | 'full';
  style?: ViewStyle;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  compact = false,
  variant,
  style,
}) => {
  const { currentLanguage, setLanguage, supportedLanguages } = useLanguage();
  const theme = useTheme();
  const [modalVisible, setModalVisible] = useState(false);

  const activeLangObj = supportedLanguages.find((l) => l.code === currentLanguage);

  const isPill = variant === 'pill' || (compact && variant !== 'full');

  const languageDetails: Record<
    SupportedLanguage,
    { badge: string; tag: string; description: string }
  > = {
    mr: {
      badge: 'मराठी',
      tag: 'महाराष्ट्र',
      description: 'शेतकऱ्यांसाठी सर्व सल्ले, रोग निदान व हवामान माहिती',
    },
    hi: {
      badge: 'हिंदी',
      tag: 'भारत',
      description: 'भारतीय किसानों के लिए फसल सलाह एवं कीट निदान',
    },
    en: {
      badge: 'EN',
      tag: 'Global',
      description: 'Smart agricultural advisory & scientific reports',
    },
  };

  const handleSelectLanguage = (code: SupportedLanguage) => {
    setLanguage(code);
    setModalVisible(false);
  };

  // 1. Compact Pill Trigger with Modal (for headers / top bar)
  if (isPill) {
    return (
      <>
        <TouchableOpacity
          accessibilityRole="button"
          accessibilityLabel="Change language"
          activeOpacity={0.75}
          style={[
            styles.triggerPill,
            {
              backgroundColor: theme.isDark ? '#1E293B' : '#DCFCE7',
              borderColor: theme.isDark ? '#334155' : '#86EFAC',
            },
            style,
          ]}
          onPress={() => setModalVisible(true)}
        >
          <Ionicons name="globe-outline" size={15} color={theme.colors.primary} />
          <Text style={[styles.triggerText, { color: theme.colors.primary }]}>
            {activeLangObj?.nativeName || 'English'}
          </Text>
          <Ionicons name="chevron-down" size={13} color={theme.colors.primary} />
        </TouchableOpacity>

        {/* Modal Sheet for Language Selection */}
        <Modal
          animationType="fade"
          transparent
          visible={modalVisible}
          onRequestClose={() => setModalVisible(false)}
        >
          <Pressable
            style={styles.modalBackdrop}
            onPress={() => setModalVisible(false)}
          >
            <View
              style={[
                styles.modalCard,
                {
                  backgroundColor: theme.isDark ? '#0F172A' : '#FFFFFF',
                  borderColor: theme.colors.border,
                },
              ]}
            >
              {/* Modal Header */}
              <View style={styles.modalHeader}>
                <View style={styles.modalTitleRow}>
                  <View
                    style={[
                      styles.modalIconWrap,
                      { backgroundColor: theme.colors.primaryLight },
                    ]}
                  >
                    <Ionicons name="language" size={20} color={theme.colors.primary} />
                  </View>
                  <View style={styles.modalTitleTextWrap}>
                    <Text
                      style={[
                        styles.modalTitle,
                        { color: theme.colors.textPrimary },
                      ]}
                    >
                      भाषा निवडा / Select Language
                    </Text>
                    <Text
                      style={[
                        styles.modalSubtitle,
                        { color: theme.colors.textSecondary },
                      ]}
                    >
                      Choose your preferred app language
                    </Text>
                  </View>
                </View>

                <TouchableOpacity
                  accessibilityRole="button"
                  accessibilityLabel="Close language selector"
                  style={[
                    styles.closeBtn,
                    { backgroundColor: theme.isDark ? '#334155' : '#F1F5F9' },
                  ]}
                  onPress={() => setModalVisible(false)}
                >
                  <Ionicons
                    name="close"
                    size={18}
                    color={theme.colors.textSecondary}
                  />
                </TouchableOpacity>
              </View>

              {/* Language Options */}
              <View style={styles.optionsList}>
                {supportedLanguages.map((lang) => {
                  const isSelected = currentLanguage === lang.code;
                  const details = languageDetails[lang.code as SupportedLanguage];

                  return (
                    <TouchableOpacity
                      key={lang.code}
                      activeOpacity={0.7}
                      style={[
                        styles.optionCard,
                        {
                          backgroundColor: isSelected
                            ? (theme.isDark ? '#064E3B' : '#DCFCE7')
                            : (theme.isDark ? '#1E293B' : '#F8FAFC'),
                          borderColor: isSelected
                            ? theme.colors.primary
                            : (theme.isDark ? '#334155' : '#E2E8F0'),
                          borderWidth: isSelected ? 1.8 : 1,
                        },
                      ]}
                      onPress={() => handleSelectLanguage(lang.code as SupportedLanguage)}
                    >
                      <View style={styles.optionLeft}>
                        <View
                          style={[
                            styles.langBadge,
                            {
                              backgroundColor: isSelected
                                ? theme.colors.primary
                                : (theme.isDark ? '#334155' : '#E2E8F0'),
                            },
                          ]}
                        >
                          <Text
                            style={[
                              styles.langBadgeText,
                              {
                                color: isSelected
                                  ? '#FFFFFF'
                                  : theme.colors.textPrimary,
                              },
                            ]}
                          >
                            {details.badge}
                          </Text>
                        </View>

                        <View style={styles.optionInfo}>
                          <View style={styles.nameRow}>
                            <Text
                              style={[
                                styles.optionNativeName,
                                {
                                  color: isSelected
                                    ? theme.colors.primary
                                    : theme.colors.textPrimary,
                                },
                              ]}
                            >
                              {lang.nativeName}
                            </Text>
                            <View
                              style={[
                                styles.tagBadge,
                                {
                                  backgroundColor: isSelected
                                    ? 'rgba(20, 83, 45, 0.12)'
                                    : 'rgba(100, 116, 139, 0.1)',
                                },
                              ]}
                            >
                              <Text
                                style={[
                                  styles.tagText,
                                  {
                                    color: isSelected
                                      ? theme.colors.primary
                                      : theme.colors.textSecondary,
                                  },
                                ]}
                              >
                                {details.tag}
                              </Text>
                            </View>
                          </View>
                          <Text
                            numberOfLines={1}
                            style={[
                              styles.optionDesc,
                              { color: theme.colors.textSecondary },
                            ]}
                          >
                            {details.description}
                          </Text>
                        </View>
                      </View>

                      <Ionicons
                        name={
                          isSelected
                            ? 'checkmark-circle'
                            : 'ellipse-outline'
                        }
                        size={22}
                        color={
                          isSelected
                            ? theme.colors.primary
                            : theme.colors.textMuted
                        }
                      />
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>
          </Pressable>
        </Modal>
      </>
    );
  }

  // 2. Full Row View (for Profile & Settings)
  return (
    <View
      style={[
        styles.fullContainer,
        {
          backgroundColor: theme.colors.surface,
          borderColor: theme.colors.border,
        },
        style,
      ]}
    >
      {supportedLanguages.map((lang, idx) => {
        const isSelected = currentLanguage === lang.code;
        const details = languageDetails[lang.code as SupportedLanguage];
        const isLast = idx === supportedLanguages.length - 1;

        return (
          <TouchableOpacity
            key={lang.code}
            activeOpacity={0.7}
            style={[
              styles.fullRow,
              {
                borderBottomColor: theme.colors.border,
                borderBottomWidth: isLast ? 0 : 1,
                backgroundColor: isSelected
                  ? theme.colors.primaryLight
                  : 'transparent',
              },
            ]}
            onPress={() => setLanguage(lang.code as SupportedLanguage)}
          >
            <View style={styles.optionLeft}>
              <View
                style={[
                  styles.langBadge,
                  {
                    backgroundColor: isSelected
                      ? theme.colors.primary
                      : theme.isDark
                      ? '#334155'
                      : '#E2E8F0',
                  },
                ]}
              >
                <Text
                  style={[
                    styles.langBadgeText,
                    {
                      color: isSelected
                        ? '#FFFFFF'
                        : theme.colors.textPrimary,
                    },
                  ]}
                >
                  {details.badge}
                </Text>
              </View>

              <View style={styles.optionInfo}>
                <Text
                  style={[
                    styles.optionNativeName,
                    {
                      color: isSelected
                        ? theme.colors.primary
                        : theme.colors.textPrimary,
                    },
                  ]}
                >
                  {lang.nativeName} ({lang.label})
                </Text>
                <Text
                  numberOfLines={1}
                  style={[styles.optionDesc, { color: theme.colors.textSecondary }]}
                >
                  {details.description}
                </Text>
              </View>
            </View>

            {isSelected ? (
              <Ionicons
                name="checkmark-circle"
                size={24}
                color={theme.colors.primary}
              />
            ) : (
              <Ionicons
                name="chevron-forward"
                size={18}
                color={theme.colors.textMuted}
              />
            )}
          </TouchableOpacity>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  // Trigger Pill
  triggerPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 11,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1.2,
  },
  triggerText: {
    fontSize: 12.5,
    fontWeight: '700',
  },

  // Modal Backdrop & Card
  modalBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalCard: {
    width: '100%',
    maxWidth: 380,
    borderRadius: 24,
    borderWidth: 1,
    padding: 20,
    overflow: 'hidden',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.25,
        shadowRadius: 20,
      },
      android: {
        elevation: 20,
      },
    }),
  },
  modalTitleTextWrap: {
    flex: 1,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 18,
  },
  modalTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  modalIconWrap: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 16,
    fontWeight: '800',
  },
  modalSubtitle: {
    fontSize: 12,
    marginTop: 2,
  },
  closeBtn: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Options List
  optionsList: {
    gap: 10,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 12,
    borderRadius: 16,
  },
  optionLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  langBadge: {
    width: 42,
    height: 42,
    borderRadius: 21,
    justifyContent: 'center',
    alignItems: 'center',
  },
  langBadgeText: {
    fontSize: 13,
    fontWeight: '800',
  },
  optionInfo: {
    flex: 1,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  optionNativeName: {
    fontSize: 15,
    fontWeight: '700',
  },
  tagBadge: {
    paddingHorizontal: 7,
    paddingVertical: 2,
    borderRadius: 10,
  },
  tagText: {
    fontSize: 10.5,
    fontWeight: '700',
  },
  optionDesc: {
    fontSize: 11.5,
    marginTop: 3,
    lineHeight: 16,
  },

  // Full Row Container
  fullContainer: {
    borderWidth: 1,
    borderRadius: 16,
    overflow: 'hidden',
  },
  fullRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 14,
  },
});

export default LanguageSelector;
