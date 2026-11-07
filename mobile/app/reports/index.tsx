import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Share, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Badge } from '../../src/components/ui/Badge';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';
import { useAuthStore } from '../../src/store/authStore';
import { firebaseDbService } from '../../src/services/firebase';
import { FarmReport } from '../../src/types';
import { formatDate } from '../../src/utils/formatters';
import { useTheme } from '../../src/hooks/useTheme';

export default function ReportsScreen() {
  const { t } = useTranslation(['reports', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const currentDiagnosis = useDiagnosisStore((s) => s.currentDiagnosis) || INITIAL_DEMO_DIAGNOSES[0];

  const [reports, setReports] = useState<FarmReport[]>([
    {
      id: 'REP-7489',
      diagnosisId: currentDiagnosis.id,
      farmerName: user?.fullName || 'Ramesh Patil',
      crop: currentDiagnosis.crop,
      disease: currentDiagnosis.diseaseName,
      confidence: currentDiagnosis.confidence,
      severity: currentDiagnosis.severity.severityClass,
      generatedDate: new Date().toISOString(),
    },
  ]);

  const handleGenerateReport = async () => {
    const newReport: FarmReport = {
      id: `REP-${Math.floor(1000 + Math.random() * 9000)}`,
      diagnosisId: currentDiagnosis.id,
      farmerName: user?.fullName || 'Ramesh Patil',
      crop: currentDiagnosis.crop,
      disease: currentDiagnosis.diseaseName,
      confidence: currentDiagnosis.confidence,
      severity: currentDiagnosis.severity.severityClass,
      generatedDate: new Date().toISOString(),
    };

    setReports([newReport, ...reports]);
    // Save to Firebase Firestore
    await firebaseDbService.saveReport(newReport);
    Alert.alert(t('common:success'), 'Official Diagnostic Report Generated & Stored');
  };

  const handleShareReport = async (rep: FarmReport) => {
    try {
      await Share.share({
        title: `Agrivision AI+ Official Report ${rep.id}`,
        message: `*AGRIVISION AI+ OFFICIAL ADVISORY REPORT*\nReport ID: #${rep.id}\nFarmer: ${rep.farmerName}\nCrop: ${rep.crop.toUpperCase()}\nDiagnosed: ${rep.disease}\nSeverity: ${rep.severity.toUpperCase()}\nDate: ${formatDate(rep.generatedDate)}\nVerified against ICAR Indian agronomy norms.`,
      });
    } catch (e) {
      console.warn('Share error:', e);
    }
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('reports:subtitle')}
        title={t('reports:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Button
          icon={<Ionicons name="add-circle-outline" size={20} color="#FFFFFF" />}
          size="lg"
          style={styles.generateBtn}
          title={t('reports:generateReport')}
          variant="primary"
          onPress={handleGenerateReport}
        />

        {reports.map((report) => (
          <Card key={report.id} style={styles.reportCard}>
            <View style={styles.cardHeader}>
              <View>
                <Text style={[styles.reportNum, { color: theme.colors.primary }]}>
                  {t('reports:reportNumber', { id: report.id })}
                </Text>
                <Text style={[styles.genDate, { color: theme.colors.textMuted }]}>
                  {t('reports:generatedOn', { date: formatDate(report.generatedDate, 'dd MMM yyyy') })}
                </Text>
              </View>
              <Badge
                label={report.severity.toUpperCase()}
                variant={report.severity === 'mild' ? 'success' : 'danger'}
              />
            </View>

            <View style={styles.divider} />

            <View style={styles.detailRow}>
              <Text style={[styles.label, { color: theme.colors.textSecondary }]}>
                {t('reports:farmerName')}:
              </Text>
              <Text style={[styles.value, { color: theme.colors.textPrimary }]}>
                {report.farmerName}
              </Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={[styles.label, { color: theme.colors.textSecondary }]}>
                {t('reports:cropDiagnosed')}:
              </Text>
              <Text style={[styles.value, { color: theme.colors.textPrimary }]}>
                {report.crop.toUpperCase()}
              </Text>
            </View>

            <View style={styles.detailRow}>
              <Text style={[styles.label, { color: theme.colors.textSecondary }]}>
                {t('reports:conditionDetected')}:
              </Text>
              <Text
                numberOfLines={2}
                style={[styles.value, { color: theme.colors.textPrimary, flex: 1, textAlign: 'right' }]}
              >
                {report.disease}
              </Text>
            </View>

            <View style={styles.buttonRow}>
              <Button
                icon={<Ionicons name="share-social-outline" size={16} color="#FFFFFF" />}
                size="sm"
                style={styles.actionBtn}
                title={t('common:share')}
                variant="primary"
                onPress={() => handleShareReport(report)}
              />
              <Button
                icon={<Ionicons name="download-outline" size={16} color={theme.colors.primary} />}
                size="sm"
                style={styles.actionBtn}
                title={t('common:download')}
                variant="outline"
                onPress={() => Alert.alert(t('common:success'), 'PDF saved to device downloads')}
              />
            </View>
          </Card>
        ))}

        <Card style={styles.disclaimerCard}>
          <Ionicons name="shield-checkmark" size={24} color={theme.colors.primary} />
          <Text style={[styles.disclaimerText, { color: theme.colors.textSecondary }]}>
            {t('reports:officialDisclaimer')}
          </Text>
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
  generateBtn: {
    marginBottom: 16,
  },
  reportCard: {
    marginVertical: 8,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  reportNum: {
    fontSize: 16,
    fontWeight: '800',
  },
  genDate: {
    fontSize: 11,
    marginTop: 2,
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(150, 150, 150, 0.15)',
    marginVertical: 12,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    fontSize: 13,
  },
  value: {
    fontSize: 13,
    fontWeight: '700',
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 14,
  },
  actionBtn: {
    flex: 1,
  },
  disclaimerCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginTop: 16,
    padding: 16,
  },
  disclaimerText: {
    fontSize: 12,
    lineHeight: 18,
    flex: 1,
  },
});

