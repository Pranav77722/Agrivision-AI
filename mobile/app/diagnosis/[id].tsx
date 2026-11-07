import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { ResultCard } from '../../src/components/diagnosis/ResultCard';
import { Button } from '../../src/components/ui/Button';
import { EmptyState } from '../../src/components/common/EmptyState';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';

export default function DiagnosisDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { t } = useTranslation(['diagnosis', 'common']);
  const router = useRouter();
  const history = useDiagnosisStore((s) => s.history);
  const setCurrentDiagnosis = useDiagnosisStore((s) => s.setCurrentDiagnosis);

  const diagnosis =
    history.find((item) => item.id === id) ||
    INITIAL_DEMO_DIAGNOSES.find((item) => item.id === id) ||
    INITIAL_DEMO_DIAGNOSES[0];

  if (!diagnosis) {
    return (
      <SafeArea style={styles.safeArea}>
        <Header showBack title={t('diagnosis:resultsTitle')} />
        <EmptyState
          actionTitle={t('common:back')}
          title={t('common:error')}
          onAction={() => router.back()}
        />
      </SafeArea>
    );
  }

  const handleOpenExplainability = () => {
    setCurrentDiagnosis(diagnosis);
    router.push('/explainability' as any);
  };

  const handleOpenRecommendations = () => {
    setCurrentDiagnosis(diagnosis);
    router.push(`/recommendations/${diagnosis.id}` as any);
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={diagnosis.diseaseName}
        title={t('diagnosis:resultsTitle')}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <ResultCard diagnosis={diagnosis} />

        <View style={styles.buttonStack}>
          <Button
            icon={<Ionicons name="color-filter-outline" size={20} color="#FFFFFF" />}
            size="lg"
            title={t('diagnosis:viewExplainability')}
            variant="primary"
            onPress={handleOpenExplainability}
          />

          <Button
            icon={<Ionicons name="medkit-outline" size={20} color="#FFFFFF" />}
            size="lg"
            title={t('diagnosis:treatmentTitle')}
            variant="secondary"
            onPress={handleOpenRecommendations}
          />

          <Button
            icon={<Ionicons name="document-text-outline" size={20} color="#FFFFFF" />}
            size="lg"
            title={t('diagnosis:generateReport')}
            variant="primary"
            onPress={() => router.push('/reports' as any)}
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
  buttonStack: {
    marginTop: 18,
    gap: 12,
  },
});
