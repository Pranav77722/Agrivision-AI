import React, { useState } from 'react';
import { View, Text, Image, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
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

export default function ExplainabilityScreen() {
  const { t } = useTranslation(['explainability', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis) || INITIAL_DEMO_DIAGNOSES[0];
  const explainability = currentDiagnosis.explainability;
  const [viewMode, setViewMode] = useState<'heatmap' | 'original'>('heatmap');

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={currentDiagnosis.diseaseName}
        title={t('explainability:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Toggle Mode Segmented Control */}
        <View
          style={[
            styles.toggleContainer,
            { backgroundColor: theme.colors.surface, borderColor: theme.colors.border },
          ]}
        >
          <TouchableOpacity
            style={[
              styles.toggleTab,
              viewMode === 'heatmap' && { backgroundColor: theme.colors.primary },
            ]}
            onPress={() => setViewMode('heatmap')}
          >
            <Text
              style={[
                styles.toggleText,
                { color: viewMode === 'heatmap' ? '#FFFFFF' : theme.colors.textSecondary },
              ]}
            >
              {t('explainability:gradCamView')}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.toggleTab,
              viewMode === 'original' && { backgroundColor: theme.colors.primary },
            ]}
            onPress={() => setViewMode('original')}
          >
            <Text
              style={[
                styles.toggleText,
                { color: viewMode === 'original' ? '#FFFFFF' : theme.colors.textSecondary },
              ]}
            >
              {t('explainability:originalImage')}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Heatmap Visual Display */}
        <View style={styles.imageCard}>
          <Image
            source={{
              uri:
                viewMode === 'heatmap'
                  ? explainability.heatmapUri
                  : explainability.originalImageUri,
            }}
            style={styles.leafImage}
          />
          {viewMode === 'heatmap' && (
            <View style={styles.heatmapLegend}>
              <View style={[styles.legendBox, { backgroundColor: '#EF4444' }]} />
              <Text style={styles.legendText}>{t('explainability:redZone')}</Text>
            </View>
          )}
        </View>

        {/* Model Explanation Card */}
        <Card
          subtitle={t('explainability:verifiedByAgronomist')}
          title={t('explainability:whatAiSaw')}
          style={styles.card}
        >
          <Text style={[styles.focusDesc, { color: theme.colors.textPrimary }]}>
            {explainability.focusDescription}
          </Text>

          <Text style={[styles.generalDesc, { color: theme.colors.textSecondary }]}>
            {t('explainability:explanationDesc')}
          </Text>

          <View style={styles.colorKeyRow}>
            <View style={styles.colorKeyItem}>
              <View style={[styles.colorChip, { backgroundColor: '#EF4444' }]} />
              <Text style={[styles.colorKeyText, { color: theme.colors.textSecondary }]}>
                {t('explainability:redZone')}
              </Text>
            </View>

            <View style={styles.colorKeyItem}>
              <View style={[styles.colorChip, { backgroundColor: '#F59E0B' }]} />
              <Text style={[styles.colorKeyText, { color: theme.colors.textSecondary }]}>
                {t('explainability:yellowZone')}
              </Text>
            </View>

            <View style={styles.colorKeyItem}>
              <View style={[styles.colorChip, { backgroundColor: '#3B82F6' }]} />
              <Text style={[styles.colorKeyText, { color: theme.colors.textSecondary }]}>
                {t('explainability:blueZone')}
              </Text>
            </View>
          </View>
        </Card>

        {/* Attention Region Breakdown */}
        <Card title={t('explainability:modelConfidence')} style={styles.card}>
          {explainability.attentionRegions.map((region, idx) => (
            <View key={idx} style={styles.regionRow}>
              <View style={styles.regionHeader}>
                <Text style={[styles.regionLabel, { color: theme.colors.textPrimary }]}>
                  {region.label}
                </Text>
                <Badge
                  label={`${Math.round(region.score * 100)}%`}
                  variant="success"
                />
              </View>
              <ProgressBar
                color={theme.colors.secondary}
                height={6}
                progress={region.score * 100}
              />
            </View>
          ))}
        </Card>
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
  toggleContainer: {
    flexDirection: 'row',
    padding: 4,
    borderRadius: 24,
    borderWidth: 1,
    marginBottom: 16,
  },
  toggleTab: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 20,
    alignItems: 'center',
  },
  toggleText: {
    fontSize: 13,
    fontWeight: '700',
  },
  imageCard: {
    width: '100%',
    height: 280,
    borderRadius: 20,
    overflow: 'hidden',
    marginBottom: 16,
    position: 'relative',
  },
  leafImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  heatmapLegend: {
    position: 'absolute',
    bottom: 12,
    left: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.75)',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  legendBox: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  legendText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  card: {
    marginVertical: 6,
  },
  focusDesc: {
    fontSize: 15,
    fontWeight: '700',
    lineHeight: 22,
    marginBottom: 10,
  },
  generalDesc: {
    fontSize: 13,
    lineHeight: 20,
    marginBottom: 16,
  },
  colorKeyRow: {
    gap: 8,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: 'rgba(150, 150, 150, 0.15)',
  },
  colorKeyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  colorChip: {
    width: 14,
    height: 14,
    borderRadius: 7,
  },
  colorKeyText: {
    fontSize: 12,
    fontWeight: '600',
  },
  regionRow: {
    marginBottom: 12,
  },
  regionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  regionLabel: {
    fontSize: 14,
    fontWeight: '600',
  },
});
