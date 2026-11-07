import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Share } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Badge } from '../../src/components/ui/Badge';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore, INITIAL_DEMO_DIAGNOSES } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';

type RecTab = 'organic' | 'chemical' | 'cultural' | 'safety';

export default function RecommendationsScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { t } = useTranslation(['recommendations', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const history = useDiagnosisStore((s) => s.history);

  const diagnosis =
    history.find((item) => item.id === id) ||
    INITIAL_DEMO_DIAGNOSES.find((item) => item.id === id) ||
    INITIAL_DEMO_DIAGNOSES[0];

  const [activeTab, setActiveTab] = useState<RecTab>('organic');
  const rec = diagnosis.recommendations;

  const handleShare = async () => {
    try {
      await Share.share({
        title: `Agrivision AI+ Treatment: ${diagnosis.diseaseName}`,
        message: `*Agrivision AI+ Treatment Plan*\nCrop: ${diagnosis.crop.toUpperCase()}\nCondition: ${diagnosis.diseaseName}\nDosage: ${rec.dosage}\nInterval: Every ${rec.intervalDays} days\nTiming: ${t('recommendations:morningOrEvening')}`,
      });
    } catch (e) {
      console.warn('Share error:', e);
    }
  };

  const tabs: { id: RecTab; label: string; icon: keyof typeof Ionicons.glyphMap }[] = [
    { id: 'organic', label: t('recommendations:tabs.organic'), icon: 'leaf-outline' },
    { id: 'chemical', label: t('recommendations:tabs.chemical'), icon: 'flask-outline' },
    { id: 'cultural', label: t('recommendations:tabs.cultural'), icon: 'construct-outline' },
    { id: 'safety', label: t('recommendations:tabs.safety'), icon: 'shield-outline' },
  ];

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={diagnosis.diseaseName}
        title={t('recommendations:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Prescription Overview Card */}
        <Card
          subtitle={t('recommendations:subtitle')}
          title={diagnosis.diseaseName}
          style={styles.heroCard}
        >
          <View style={styles.dosageRow}>
            <View>
              <Text style={[styles.metaLabel, { color: theme.colors.textSecondary }]}>
                {t('recommendations:dosage')}
              </Text>
              <Text style={[styles.metaVal, { color: theme.colors.textPrimary }]}>
                {rec.dosage}
              </Text>
            </View>

            <View style={{ alignItems: 'flex-end' }}>
              <Text style={[styles.metaLabel, { color: theme.colors.textSecondary }]}>
                Spray Interval
              </Text>
              <Badge label={`Every ${rec.intervalDays} Days`} variant="info" />
            </View>
          </View>
        </Card>

        {/* Segmented Tab Bar */}
        <ScrollView horizontal contentContainerStyle={styles.tabScroll} showsHorizontalScrollIndicator={false}>
          {tabs.map((tab) => {
            const isSelected = activeTab === tab.id;
            return (
              <TouchableOpacity
                key={tab.id}
                activeOpacity={0.8}
                style={[
                  styles.tabChip,
                  {
                    backgroundColor: isSelected ? theme.colors.primary : theme.colors.surface,
                    borderColor: isSelected ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setActiveTab(tab.id)}
              >
                <Ionicons
                  name={tab.icon}
                  size={16}
                  color={isSelected ? '#FFFFFF' : theme.colors.textSecondary}
                />
                <Text
                  style={[
                    styles.tabChipText,
                    { color: isSelected ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {tab.label}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>

        {/* Tab Content Display */}
        {activeTab === 'organic' && (
          <Card title={t('recommendations:organicHeader')} style={styles.contentCard}>
            {rec.organic.map((item, idx) => (
              <View key={idx} style={styles.listItem}>
                <Ionicons name="leaf" size={18} color={theme.colors.success} />
                <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>{item}</Text>
              </View>
            ))}
          </Card>
        )}

        {activeTab === 'chemical' && (
          <Card title={t('recommendations:chemicalHeader')} style={styles.contentCard}>
            {rec.chemical.map((item, idx) => (
              <View key={idx} style={styles.listItem}>
                <Ionicons name="flask" size={18} color={theme.colors.danger} />
                <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>{item}</Text>
              </View>
            ))}
          </Card>
        )}

        {activeTab === 'cultural' && (
          <Card title={t('recommendations:culturalHeader')} style={styles.contentCard}>
            {rec.cultural.map((item, idx) => (
              <View key={idx} style={styles.listItem}>
                <Ionicons name="hand-left" size={18} color={theme.colors.warning} />
                <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>{item}</Text>
              </View>
            ))}
          </Card>
        )}

        {activeTab === 'safety' && (
          <Card title={t('recommendations:safetyHeader')} style={styles.contentCard}>
            <View style={styles.listItem}>
              <Ionicons name="shield-checkmark" size={18} color={theme.colors.primary} />
              <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>
                {t('recommendations:wearMask')}
              </Text>
            </View>
            <View style={styles.listItem}>
              <Ionicons name="sunny" size={18} color={theme.colors.warning} />
              <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>
                {t('recommendations:morningOrEvening')}
              </Text>
            </View>
            {rec.safety.map((item, idx) => (
              <View key={idx} style={styles.listItem}>
                <Ionicons name="alert-circle" size={18} color={theme.colors.danger} />
                <Text style={[styles.itemText, { color: theme.colors.textPrimary }]}>{item}</Text>
              </View>
            ))}
          </Card>
        )}

        {/* Share Action */}
        <Button
          icon={<Ionicons name="logo-whatsapp" size={20} color="#FFFFFF" />}
          size="lg"
          style={styles.shareBtn}
          title={t('common:share')}
          variant="primary"
          onPress={handleShare}
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
  heroCard: {
    marginBottom: 16,
  },
  dosageRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  metaLabel: {
    fontSize: 12,
    marginBottom: 2,
  },
  metaVal: {
    fontSize: 15,
    fontWeight: '700',
  },
  tabScroll: {
    gap: 8,
    paddingBottom: 12,
  },
  tabChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 24,
    borderWidth: 1.2,
  },
  tabChipText: {
    fontSize: 13,
    fontWeight: '700',
  },
  contentCard: {
    marginVertical: 8,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    marginBottom: 14,
  },
  itemText: {
    fontSize: 14,
    lineHeight: 20,
    flex: 1,
  },
  shareBtn: {
    marginTop: 18,
  },
});

