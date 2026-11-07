import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Badge } from '../../src/components/ui/Badge';
import { ProgressBar } from '../../src/components/ui/ProgressBar';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';
import { formatConfidence } from '../../src/utils/formatters';

export default function EnsembleScreen() {
  const { t } = useTranslation(['ensemble', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis) || INITIAL_DEMO_DIAGNOSES[0];
  const ensemble = currentDiagnosis.ensemble;

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={ensemble.consensusClass}
        title={t('ensemble:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Consensus Decision Hero Card */}
        <Card
          subtitle={t('ensemble:votingStrategy')}
          title={t('ensemble:consensusDecision')}
          style={[styles.heroCard, { backgroundColor: theme.isDark ? '#052E16' : '#DCFCE7' }]}
        >
          <View style={styles.consensusHeader}>
            <View>
              <Text style={[styles.consensusClass, { color: theme.colors.primary }]}>
                {ensemble.consensusClass}
              </Text>
              <Text style={[styles.confidenceTag, { color: theme.colors.textSecondary }]}>
                Consensus Confidence: {formatConfidence(ensemble.consensusConfidence)}
              </Text>
            </View>
            <Badge
              icon={<Ionicons name="shield-checkmark" size={14} color="#16A34A" />}
              label={t('ensemble:agreementHigh')}
              variant="success"
            />
          </View>
        </Card>

        {/* Individual Models Breakdown */}
        <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
          {t('ensemble:modelsHeader')}
        </Text>

        {ensemble.models.map((model, index) => {
          const descKey =
            model.modelName.includes('ResNet')
              ? 'resnetDesc'
              : model.modelName.includes('EfficientNet')
              ? 'efficientnetDesc'
              : 'vitDesc';

          return (
            <Card key={index} style={styles.modelCard}>
              <View style={styles.modelHeader}>
                <View style={styles.modelTitleRow}>
                  <Ionicons name="hardware-chip-outline" size={20} color={theme.colors.primary} />
                  <Text style={[styles.modelName, { color: theme.colors.textPrimary }]}>
                    {model.modelName}
                  </Text>
                </View>
                <Badge
                  label={`Weight: ${(model.weight * 100).toFixed(0)}%`}
                  variant="info"
                />
              </View>

              <Text style={[styles.modelDesc, { color: theme.colors.textSecondary }]}>
                {t(`ensemble:${descKey}` as any, { defaultValue: 'Deep feature extractor' })}
              </Text>

              <View style={styles.predRow}>
                <Text style={[styles.predClass, { color: theme.colors.textPrimary }]}>
                  {model.predictedClass}
                </Text>
                <Text style={[styles.predScore, { color: theme.colors.primary }]}>
                  {formatConfidence(model.confidence)}
                </Text>
              </View>

              <ProgressBar
                color={theme.colors.secondary}
                height={8}
                progress={model.confidence}
              />
            </Card>
          );
        })}
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
  heroCard: {
    marginBottom: 20,
    borderWidth: 1.5,
  },
  consensusHeader: {
    gap: 12,
  },
  consensusClass: {
    fontSize: 22,
    fontWeight: '800',
  },
  confidenceTag: {
    fontSize: 13,
    marginTop: 4,
    fontWeight: '600',
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 12,
  },
  modelCard: {
    marginVertical: 6,
  },
  modelHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  modelTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  modelName: {
    fontSize: 16,
    fontWeight: '700',
  },
  modelDesc: {
    fontSize: 12,
    lineHeight: 18,
    marginBottom: 12,
  },
  predRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  predClass: {
    fontSize: 14,
    fontWeight: '600',
  },
  predScore: {
    fontSize: 14,
    fontWeight: '800',
  },
});
