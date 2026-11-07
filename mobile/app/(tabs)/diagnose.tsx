import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Container } from '../../src/components/layout/Container';
import { Card } from '../../src/components/ui/Card';
import { Button } from '../../src/components/ui/Button';
import { DiagnosisCard } from '../../src/components/diagnosis/DiagnosisCard';
import { useDiagnosisStore } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';
import { CropType } from '../../src/types';
import { pickImageFromGallery } from '../../src/utils/imageUtils';

const CROP_SPECIES: { id: CropType; icon: keyof typeof Ionicons.glyphMap }[] = [
  { id: 'tomato', icon: 'nutrition-outline' },
  { id: 'rice', icon: 'water-outline' },
  { id: 'wheat', icon: 'leaf-outline' },
  { id: 'cotton', icon: 'cloud-outline' },
  { id: 'potato', icon: 'globe-outline' },
  { id: 'maize', icon: 'sunny-outline' },
  { id: 'soybean', icon: 'flower-outline' },
  { id: 'sugarcane', icon: 'sparkles-outline' },
];

export default function DiagnoseTabScreen() {
  const { t } = useTranslation(['diagnosis', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const selectedCrop = useDiagnosisStore((s) => s.selectedCrop);
  const setSelectedCrop = useDiagnosisStore((s) => s.setSelectedCrop);
  const setCapturedImageUri = useDiagnosisStore((s) => s.setCapturedImageUri);
  const history = useDiagnosisStore((s) => s.history);

  const handlePickGallery = async () => {
    try {
      const result = await pickImageFromGallery();
      if (result) {
        setCapturedImageUri(result.uri);
        router.push('/diagnosis/preview' as any);
      }
    } catch {
      Alert.alert(t('common:error'), t('diagnosis:cameraPermission'));
    }
  };

  const handleOpenCamera = () => {
    router.push('/diagnosis/camera' as any);
  };

  return (
    <SafeArea style={styles.safeArea}>
      <View
        style={[
          styles.headerBar,
          {
            backgroundColor: theme.colors.surface,
            borderBottomColor: theme.colors.border,
          },
        ]}
      >
        <Text style={[styles.screenTitle, { color: theme.colors.textPrimary }]}>
          {t('diagnosis:title')}
        </Text>
        <Text style={[styles.screenSubtitle, { color: theme.colors.textSecondary }]}>
          {t('diagnosis:subtitle')}
        </Text>
      </View>

      <Container contentContainerStyle={styles.containerContent}>
        {/* Action Buttons: Camera & Gallery */}
        <View style={styles.actionRow}>
          <Button
            icon={<Ionicons name="camera" size={20} color="#FFFFFF" />}
            size="lg"
            style={styles.actionBtn}
            title={t('diagnosis:capturePhoto')}
            variant="primary"
            onPress={handleOpenCamera}
          />
          <Button
            icon={<Ionicons name="images-outline" size={20} color={theme.colors.primary} />}
            size="lg"
            style={styles.actionBtn}
            title={t('diagnosis:selectGallery')}
            variant="outline"
            onPress={handlePickGallery}
          />
        </View>

        {/* Crop Selector Horizontal Chips */}
        <View style={styles.cropSection}>
          <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
            {t('diagnosis:selectCrop')}
          </Text>
          <ScrollView
            horizontal
            contentContainerStyle={styles.cropScroll}
            showsHorizontalScrollIndicator={false}
          >
            {CROP_SPECIES.map((crop) => {
              const isSelected = selectedCrop === crop.id;
              return (
                <TouchableOpacity
                  key={crop.id}
                  activeOpacity={0.8}
                  style={[
                    styles.cropChip,
                    {
                      backgroundColor: isSelected ? theme.colors.primary : theme.colors.surface,
                      borderColor: isSelected ? theme.colors.primary : theme.colors.border,
                    },
                  ]}
                  onPress={() => setSelectedCrop(crop.id)}
                >
                  <Ionicons
                    name={crop.icon}
                    size={16}
                    color={isSelected ? '#FFFFFF' : theme.colors.textSecondary}
                  />
                  <Text
                    style={[
                      styles.cropChipText,
                      { color: isSelected ? '#FFFFFF' : theme.colors.textPrimary },
                    ]}
                  >
                    {t(`diagnosis:crops.${crop.id}` as any, { defaultValue: crop.id })}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>

        {/* Photography Tips Card */}
        <Card subtitle={t('diagnosis:tipsTitle')} title={t('diagnosis:tipsTitle')} style={styles.tipsCard}>
          <View style={styles.tipItem}>
            <Ionicons name="checkmark-circle" size={18} color={theme.colors.success} />
            <Text style={[styles.tipText, { color: theme.colors.textSecondary }]}>
              {t('diagnosis:tip1')}
            </Text>
          </View>
          <View style={styles.tipItem}>
            <Ionicons name="checkmark-circle" size={18} color={theme.colors.success} />
            <Text style={[styles.tipText, { color: theme.colors.textSecondary }]}>
              {t('diagnosis:tip2')}
            </Text>
          </View>
          <View style={styles.tipItem}>
            <Ionicons name="checkmark-circle" size={18} color={theme.colors.success} />
            <Text style={[styles.tipText, { color: theme.colors.textSecondary }]}>
              {t('diagnosis:tip3')}
            </Text>
          </View>
        </Card>

        {/* Recent Scans */}
        <View style={styles.recentSection}>
          <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
            {t('dashboard:recentDiagnoses')}
          </Text>
          {history.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Ionicons name="leaf-outline" size={36} color={theme.colors.textMuted} />
              <Text style={[styles.emptyText, { color: theme.colors.textSecondary }]}>
                {t('dashboard:noDiagnosesYet')}
              </Text>
            </Card>
          ) : (
            history.map((record) => (
              <DiagnosisCard
                key={record.id}
                item={record}
                onPress={() => router.push(`/diagnosis/${record.id}` as any)}
              />
            ))
          )}
        </View>
      </Container>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  headerBar: {
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  screenTitle: {
    fontSize: 22,
    fontWeight: '800',
  },
  screenSubtitle: {
    fontSize: 13,
    marginTop: 4,
    lineHeight: 18,
  },
  containerContent: {
    paddingBottom: 110,
  },
  actionRow: {
    gap: 12,
    marginVertical: 14,
  },
  actionBtn: {
    width: '100%',
  },
  cropSection: {
    marginVertical: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 10,
  },
  cropScroll: {
    gap: 8,
    paddingVertical: 4,
  },
  cropChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 24,
    borderWidth: 1.2,
  },
  cropChipText: {
    fontSize: 13,
    fontWeight: '700',
  },
  tipsCard: {
    marginVertical: 14,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    marginBottom: 8,
  },
  tipText: {
    fontSize: 13,
    lineHeight: 18,
    flex: 1,
  },
  recentSection: {
    marginTop: 8,
  },
  emptyCard: {
    alignItems: 'center',
    padding: 24,
    gap: 8,
  },
  emptyText: {
    fontSize: 13,
    textAlign: 'center',
  },
});
