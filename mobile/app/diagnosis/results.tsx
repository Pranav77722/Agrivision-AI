import React, { useState } from 'react';
import { View, Text, StyleSheet, Alert, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { ResultCard } from '../../src/components/diagnosis/ResultCard';
import { Card } from '../../src/components/ui/Card';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';

export default function DiagnosisResultsScreen() {
  const { t } = useTranslation(['diagnosis', 'common', 'recommendations']);
  const theme = useTheme();
  const router = useRouter();
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis) || INITIAL_DEMO_DIAGNOSES[0];
  const [saved, setSaved] = useState(false);

  const handleSaveToHistory = () => {
    setSaved(true);
    Alert.alert(t('common:success'), t('diagnosis:savedSuccessfully'));
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={currentDiagnosis.diseaseName}
        title={t('diagnosis:resultsTitle')}
        onBack={() => router.replace('/(tabs)' as any)}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Main Result Card */}
        <ResultCard diagnosis={currentDiagnosis} />

        {/* Deep Dive Action Navigation Cards */}
        <View style={styles.deepDiveGrid}>
          {/* Explainability Grad-CAM Button */}
          <Card
            subtitle="Grad-CAM heatmaps showing lesion hotspots"
            title={t('diagnosis:viewExplainability')}
            style={styles.actionCard}
            onPress={() => router.push('/explainability' as any)}
          >
            <View style={styles.cardRow}>
              <View style={[styles.iconCircle, { backgroundColor: '#FEE2E2' }]}>
                <Ionicons name="color-filter-outline" size={24} color="#DC2626" />
              </View>
              <Text style={[styles.arrowText, { color: theme.colors.primary }]}>
                {t('common:viewDetails')} →
              </Text>
            </View>
          </Card>

          {/* Ensemble Voting Comparison */}
          <Card
            subtitle="ResNet-50, EfficientNet-B4 & ViT consensus"
            title="Ensemble Model Consensus"
            style={styles.actionCard}
            onPress={() => router.push('/ensemble' as any)}
          >
            <View style={styles.cardRow}>
              <View style={[styles.iconCircle, { backgroundColor: '#DCFCE7' }]}>
                <Ionicons name="git-network-outline" size={24} color="#16A34A" />
              </View>
              <Text style={[styles.arrowText, { color: theme.colors.primary }]}>
                {t('common:viewDetails')} →
              </Text>
            </View>
          </Card>

          {/* Severity & Damage Quantification */}
          <Card
            subtitle="Leaf damage percentage & urgency classification"
            title="Severity Estimation"
            style={styles.actionCard}
            onPress={() => router.push('/severity' as any)}
          >
            <View style={styles.cardRow}>
              <View style={[styles.iconCircle, { backgroundColor: '#FEF3C7' }]}>
                <Ionicons name="pie-chart-outline" size={24} color="#D97706" />
              </View>
              <Text style={[styles.arrowText, { color: theme.colors.primary }]}>
                {t('common:viewDetails')} →
              </Text>
            </View>
          </Card>

          {/* Full IPM Recommendations Detail */}
          <Card
            subtitle="Organic, chemical sprays, and dosage instructions"
            title={t('diagnosis:treatmentTitle')}
            style={styles.actionCard}
            onPress={() => router.push(`/recommendations/${currentDiagnosis.id}` as any)}
          >
            <View style={styles.cardRow}>
              <View style={[styles.iconCircle, { backgroundColor: '#DBEAFE' }]}>
                <Ionicons name="medkit-outline" size={24} color="#2563EB" />
              </View>
              <Text style={[styles.arrowText, { color: theme.colors.primary }]}>
                {t('common:viewDetails')} →
              </Text>
            </View>
          </Card>
        </View>

        {/* Primary Screen Actions */}
        <View style={styles.buttonStack}>
          <Button
            icon={<Ionicons name="document-text" size={20} color="#FFFFFF" />}
            size="lg"
            title={t('diagnosis:generateReport')}
            variant="primary"
            onPress={() => router.push('/reports' as any)}
          />

          <Button
            disabled={saved}
            icon={
              <Ionicons
                name={saved ? 'checkmark-circle' : 'bookmark-outline'}
                size={20}
                color={saved ? theme.colors.textMuted : theme.colors.primary}
              />
            }
            size="lg"
            title={saved ? t('diagnosis:savedSuccessfully') : t('diagnosis:saveToHistory')}
            variant="outline"
            onPress={handleSaveToHistory}
          />
        </View>
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
  deepDiveGrid: {
    marginVertical: 14,
    gap: 10,
  },
  actionCard: {
    paddingVertical: 12,
  },
  cardRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  iconCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  arrowText: {
    fontSize: 13,
    fontWeight: '700',
  },
  buttonStack: {
    marginTop: 10,
    gap: 12,
  },
});
