import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { DiagnosisRecord } from '../../types';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { ProgressBar } from '../ui/ProgressBar';
import { formatConfidence } from '../../utils/formatters';

interface ResultCardProps {
  diagnosis: DiagnosisRecord;
}

export const ResultCard: React.FC<ResultCardProps> = ({ diagnosis }) => {
  const { t } = useTranslation('diagnosis');
  const theme = useTheme();

  return (
    <Card style={styles.card}>
      <View style={styles.imageContainer}>
        <Image source={{ uri: diagnosis.imageUri }} style={styles.image} />
        <View style={styles.badgeOverlay}>
          <Badge
            label={diagnosis.severity.severityClass.toUpperCase()}
            variant={diagnosis.severity.severityClass === 'mild' ? 'success' : 'danger'}
          />
        </View>
      </View>

      <View style={styles.details}>
        <Text style={[styles.cropLabel, { color: theme.colors.primary }]}>
          {t(`crops.${diagnosis.crop}` as any, { defaultValue: diagnosis.crop }).toUpperCase()}
        </Text>
        <Text style={[styles.diseaseTitle, { color: theme.colors.textPrimary }]}>
          {diagnosis.diseaseName}
        </Text>

        <View style={styles.confidenceSection}>
          <View style={styles.confidenceRow}>
            <Text style={[styles.confidenceLabel, { color: theme.colors.textSecondary }]}>
              {t('confidence')}
            </Text>
            <Text style={[styles.confidenceValue, { color: theme.colors.primary }]}>
              {formatConfidence(diagnosis.confidence)}
            </Text>
          </View>
          <ProgressBar
            color={theme.colors.secondary}
            height={8}
            progress={diagnosis.confidence > 1 ? diagnosis.confidence / 100 : diagnosis.confidence}
          />
        </View>

        <View style={styles.section}>
          <Text style={[styles.sectionHeader, { color: theme.colors.textPrimary }]}>
            {t('symptomsTitle')}
          </Text>
          {diagnosis.symptoms.map((symptom, index) => (
            <View key={index} style={styles.bulletRow}>
              <Ionicons name="ellipse" size={6} color={theme.colors.warning} style={styles.bulletIcon} />
              <Text style={[styles.symptomText, { color: theme.colors.textSecondary }]}>
                {symptom}
              </Text>
            </View>
          ))}
        </View>
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 0,
    overflow: 'hidden',
  },
  imageContainer: {
    width: '100%',
    height: 220,
    position: 'relative',
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  badgeOverlay: {
    position: 'absolute',
    top: 14,
    right: 14,
  },
  details: {
    padding: 16,
  },
  cropLabel: {
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  diseaseTitle: {
    fontSize: 20,
    fontWeight: '800',
    lineHeight: 26,
    marginBottom: 12,
  },
  confidenceSection: {
    marginBottom: 16,
  },
  confidenceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  confidenceLabel: {
    fontSize: 13,
    fontWeight: '600',
  },
  confidenceValue: {
    fontSize: 14,
    fontWeight: '800',
  },
  section: {
    marginTop: 8,
  },
  sectionHeader: {
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  bulletRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 6,
  },
  bulletIcon: {
    marginTop: 6,
    marginRight: 8,
  },
  symptomText: {
    fontSize: 13,
    lineHeight: 18,
    flex: 1,
  },
});

export default ResultCard;
