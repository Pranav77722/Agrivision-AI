import React from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity } from 'react-native';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { DiagnosisRecord } from '../../types';
import { useTheme } from '../../hooks/useTheme';
import { Badge } from '../ui/Badge';
import { formatDate, formatConfidence } from '../../utils/formatters';

interface DiagnosisCardProps {
  item: DiagnosisRecord;
  onPress: () => void;
}

export const DiagnosisCard: React.FC<DiagnosisCardProps> = ({ item, onPress }) => {
  const { t } = useTranslation('diagnosis');
  const theme = useTheme();

  const getSeverityBadgeVariant = (sev: string) => {
    switch (sev) {
      case 'mild':
        return 'success';
      case 'moderate':
        return 'warning';
      case 'severe':
      case 'critical':
        return 'danger';
      default:
        return 'info';
    }
  };

  return (
    <TouchableOpacity
      activeOpacity={0.85}
      style={[
        styles.card,
        {
          backgroundColor: theme.colors.surface,
          borderColor: theme.colors.border,
        },
        theme.shadows.sm,
      ]}
      onPress={onPress}
    >
      <Image source={{ uri: item.imageUri }} style={styles.image} />

      <View style={styles.content}>
        <View style={styles.topRow}>
          <Text
            numberOfLines={1}
            style={[styles.cropName, { color: theme.colors.primary }]}
          >
            {t(`crops.${item.crop}` as any, { defaultValue: item.crop }).toUpperCase()}
          </Text>
          <Badge
            label={item.severity.severityClass.toUpperCase()}
            variant={getSeverityBadgeVariant(item.severity.severityClass) as any}
          />
        </View>

        <Text
          numberOfLines={2}
          style={[styles.diseaseName, { color: theme.colors.textPrimary }]}
        >
          {item.diseaseName}
        </Text>

        <View style={styles.bottomRow}>
          <View style={styles.accuracyTag}>
            <Ionicons name="shield-checkmark" size={14} color={theme.colors.success} />
            <Text style={[styles.confidence, { color: theme.colors.textSecondary }]}>
              {formatConfidence(item.confidence)}
            </Text>
          </View>

          <Text style={[styles.date, { color: theme.colors.textMuted }]}>
            {formatDate(item.createdAt, 'dd MMM')}
          </Text>
        </View>
      </View>

      <Ionicons
        color={theme.colors.textMuted}
        name="chevron-forward"
        size={20}
        style={styles.chevron}
      />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 16,
    borderWidth: 1,
    padding: 12,
    marginVertical: 6,
  },
  image: {
    width: 72,
    height: 72,
    borderRadius: 12,
    backgroundColor: '#E2E8F0',
  },
  content: {
    flex: 1,
    marginLeft: 12,
    justifyContent: 'center',
  },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  cropName: {
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  diseaseName: {
    fontSize: 14,
    fontWeight: '700',
    lineHeight: 18,
    marginBottom: 6,
  },
  bottomRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  accuracyTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  confidence: {
    fontSize: 12,
    fontWeight: '600',
  },
  date: {
    fontSize: 11,
  },
  chevron: {
    marginLeft: 6,
  },
});

export default DiagnosisCard;
