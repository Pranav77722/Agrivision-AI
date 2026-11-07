import React from 'react';
import { View, Text, Image, StyleSheet, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Badge } from '../../src/components/ui/Badge';
import { ProgressBar } from '../../src/components/ui/ProgressBar';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';

export default function SeverityScreen() {
  const { t } = useTranslation(['severity', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis) || INITIAL_DEMO_DIAGNOSES[0];
  const severity = currentDiagnosis.severity;

  const getUrgencyColor = (sev: string) => {
    switch (sev) {
      case 'critical':
      case 'severe':
        return theme.colors.danger;
      case 'moderate':
        return theme.colors.warning;
      default:
        return theme.colors.success;
    }
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('severity:subtitle')}
        title={t('severity:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Visual Segmentation Overview */}
        <View style={styles.imageCard}>
          <Image source={{ uri: currentDiagnosis.imageUri }} style={styles.leafImage} />
          <View style={styles.maskTag}>
            <Ionicons name="scan-outline" size={16} color="#FFFFFF" />
            <Text style={styles.maskTagText}>Semantic Mask Active</Text>
          </View>
        </View>

        {/* Damage Percentages & Urgency */}
        <Card
          subtitle={t('severity:actionWindow')}
          title={t('severity:severityClass')}
          style={styles.card}
        >
          <View style={styles.topRow}>
            <View>
              <Text style={[styles.sevClassTitle, { color: getUrgencyColor(severity.severityClass) }]}>
                {t(`severity:${severity.severityClass}` as any).toUpperCase()}
              </Text>
              <Text style={[styles.urgencyText, { color: theme.colors.textSecondary }]}>
                {t('severity:urgency')}: {severity.urgencyWindow}
              </Text>
            </View>
            <Badge
              label={`${severity.diseasedAreaPercent}% Lesions`}
              variant={severity.severityClass === 'mild' ? 'success' : 'danger'}
            />
          </View>

          <View style={styles.divider} />

          {/* Diseased Area Meter */}
          <View style={styles.metricBlock}>
            <View style={styles.metricHeader}>
              <View style={styles.labelRow}>
                <View style={[styles.colorDot, { backgroundColor: theme.colors.danger }]} />
                <Text style={[styles.metricLabel, { color: theme.colors.textPrimary }]}>
                  {t('severity:diseasedArea')}
                </Text>
              </View>
              <Text style={[styles.metricPercent, { color: theme.colors.danger }]}>
                {severity.diseasedAreaPercent}%
              </Text>
            </View>
            <ProgressBar
              color={theme.colors.danger}
              height={10}
              progress={severity.diseasedAreaPercent}
            />
          </View>

          {/* Healthy Area Meter */}
          <View style={styles.metricBlock}>
            <View style={styles.metricHeader}>
              <View style={styles.labelRow}>
                <View style={[styles.colorDot, { backgroundColor: theme.colors.success }]} />
                <Text style={[styles.metricLabel, { color: theme.colors.textPrimary }]}>
                  {t('severity:healthyArea')}
                </Text>
              </View>
              <Text style={[styles.metricPercent, { color: theme.colors.success }]}>
                {severity.healthyAreaPercent}%
              </Text>
            </View>
            <ProgressBar
              color={theme.colors.success}
              height={10}
              progress={severity.healthyAreaPercent}
            />
          </View>
        </Card>

        {/* Severity Scale Descriptions */}
        <Card title={t('severity:severityClass')} style={styles.card}>
          <View style={styles.scaleItem}>
            <Badge label="< 10%" variant="success" />
            <Text style={[styles.scaleDesc, { color: theme.colors.textSecondary }]}>
              {t('severity:mildDesc')}
            </Text>
          </View>

          <View style={styles.scaleItem}>
            <Badge label="10% - 30%" variant="warning" />
            <Text style={[styles.scaleDesc, { color: theme.colors.textSecondary }]}>
              {t('severity:moderateDesc')}
            </Text>
          </View>

          <View style={styles.scaleItem}>
            <Badge label="30% - 60%" variant="danger" />
            <Text style={[styles.scaleDesc, { color: theme.colors.textSecondary }]}>
              {t('severity:severeDesc')}
            </Text>
          </View>

          <View style={styles.scaleItem}>
            <Badge label="> 60%" variant="danger" />
            <Text style={[styles.scaleDesc, { color: theme.colors.textSecondary }]}>
              {t('severity:criticalDesc')}
            </Text>
          </View>
        </Card>

        <Button
          icon={<Ionicons name="medkit" size={20} color="#FFFFFF" />}
          size="lg"
          style={styles.actionBtn}
          title={t('common:viewDetails')}
          variant="primary"
          onPress={() => router.push(`/recommendations/${currentDiagnosis.id}` as any)}
        />
      </ScrollView>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  imageCard: {
    width: '100%',
    height: 240,
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 16,
    position: 'relative',
  },
  leafImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  maskTag: {
    position: 'absolute',
    bottom: 12,
    right: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.75)',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  maskTagText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
  },
  card: {
    marginVertical: 6,
  },
  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  sevClassTitle: {
    fontSize: 22,
    fontWeight: '800',
  },
  urgencyText: {
    fontSize: 13,
    marginTop: 4,
    fontWeight: '600',
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(150, 150, 150, 0.15)',
    marginVertical: 14,
  },
  metricBlock: {
    marginBottom: 14,
  },
  metricHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  labelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  colorDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  metricLabel: {
    fontSize: 13,
    fontWeight: '600',
  },
  metricPercent: {
    fontSize: 14,
    fontWeight: '800',
  },
  scaleItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    marginVertical: 8,
  },
  scaleDesc: {
    fontSize: 12,
    lineHeight: 18,
    flex: 1,
  },
  actionBtn: {
    marginTop: 14,
  },
});
