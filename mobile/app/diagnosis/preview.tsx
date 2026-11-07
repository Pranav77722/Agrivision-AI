import React, { useState } from 'react';
import { View, Text, Image, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Button } from '../../src/components/ui/Button';
import { useDiagnosisStore } from '../../src/store/diagnosisStore';
import { diagnosisService } from '../../src/services/diagnosisService';
import { useTheme } from '../../src/hooks/useTheme';
import { CropType } from '../../src/types';

const CROPS: CropType[] = [
  'tomato',
  'potato',
  'maize',
  'rice',
  'cotton',
  'wheat',
  'pepper',
  'apple',
  'grape',
];

export default function PreviewScreen() {
  const { t } = useTranslation(['diagnosis', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const capturedImageUri = useDiagnosisStore((s) => s.capturedImageUri);
  const selectedCrop = useDiagnosisStore((s) => s.selectedCrop);
  const setSelectedCrop = useDiagnosisStore((s) => s.setSelectedCrop);
  const addDiagnosis = useDiagnosisStore((s) => s.addDiagnosis);
  const [analyzing, setAnalyzing] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  const imageToDisplay =
    capturedImageUri ||
    'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?auto=format&fit=crop&w=600&q=80';

  const handleStartAnalysis = async () => {
    setAnalyzing(true);
    setValidationError(null);
    try {
      const result = await diagnosisService.diagnoseCrop(imageToDisplay, selectedCrop);
      await addDiagnosis(result);
      router.replace('/diagnosis/results' as any);
    } catch (err: any) {
      if (err?.name === 'NotAPlantError' || err?.isNotAPlant) {
        const msg =
          err.message ||
          t('diagnosis:notAPlantMessage', {
            defaultValue:
              'No plant or crop leaf detected. Please take a clear, well-lit photo of an affected plant leaf or crop.',
          });
        setValidationError(msg);
        Alert.alert(
          t('diagnosis:notAPlantTitle', { defaultValue: '🌱 No Plant or Leaf Detected' }),
          msg,
          [
            {
              text: t('diagnosis:retakePhoto', { defaultValue: 'Retake Photo' }),
              onPress: () => router.back(),
            },
            {
              text: t('common:dismiss', { defaultValue: 'Dismiss' }),
              style: 'cancel',
            },
          ]
        );
      } else {
        const errorMsg =
          err?.response?.data?.detail?.message ||
          err?.response?.data?.message ||
          err?.message ||
          t('common:networkError', { defaultValue: 'Could not connect to diagnosis server. Please try again.' });
        Alert.alert(
          t('common:error', { defaultValue: 'Diagnosis Notice' }),
          errorMsg
        );
      }
    } finally {
      setAnalyzing(false);
    }
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
        <TouchableOpacity
          accessibilityRole="button"
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color={theme.colors.textPrimary} />
        </TouchableOpacity>
        <Text style={[styles.headerTitle, { color: theme.colors.textPrimary }]}>
          {t('diagnosis:title')}
        </Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.imageCard}>
          <Image source={{ uri: imageToDisplay }} style={styles.previewImage} />
        </View>

        {/* Selected Crop confirmation & toggle */}
        <View style={styles.selectorSection}>
          <Text style={[styles.sectionLabel, { color: theme.colors.textPrimary }]}>
            {t('diagnosis:selectCrop')}
          </Text>
          <ScrollView
            horizontal
            contentContainerStyle={styles.cropsRow}
            showsHorizontalScrollIndicator={false}
          >
            {CROPS.map((crop) => {
              const active = selectedCrop === crop;
              return (
                <TouchableOpacity
                  key={crop}
                  activeOpacity={0.8}
                  style={[
                    styles.cropChip,
                    {
                      backgroundColor: active ? theme.colors.primary : theme.colors.surface,
                      borderColor: active ? theme.colors.primary : theme.colors.border,
                    },
                  ]}
                  onPress={() => setSelectedCrop(crop)}
                >
                  <Text
                    style={[
                      styles.cropChipText,
                      { color: active ? '#FFFFFF' : theme.colors.textPrimary },
                    ]}
                  >
                    {t(`diagnosis:crops.${crop}` as any, { defaultValue: crop })}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>

        {analyzing && (
          <View
            style={[
              styles.analyzingCard,
              { backgroundColor: theme.colors.primaryLight, borderColor: theme.colors.primary },
            ]}
          >
            <Ionicons name="sync" size={24} color={theme.colors.primary} />
            <View style={styles.analyzingTextCol}>
              <Text style={[styles.analyzingTitle, { color: theme.colors.primary }]}>
                {t('diagnosis:analyzing')}
              </Text>
              <Text style={[styles.analyzingSub, { color: theme.colors.textSecondary }]}>
                {t('diagnosis:analyzingSubtitle')}
              </Text>
            </View>
          </View>
        )}

        {validationError && (
          <View
            style={[
              styles.errorCard,
              { backgroundColor: theme.colors.dangerLight, borderColor: theme.colors.danger },
            ]}
          >
            <Ionicons name="alert-circle" size={26} color={theme.colors.danger} />
            <View style={styles.errorTextCol}>
              <Text style={[styles.errorCardTitle, { color: theme.colors.danger }]}>
                {t('diagnosis:notAPlantTitle', { defaultValue: '🌱 No Plant Detected' })}
              </Text>
              <Text style={[styles.errorCardDesc, { color: theme.colors.textPrimary }]}>
                {validationError}
              </Text>
            </View>
          </View>
        )}

        <View style={styles.actions}>
          <Button
            icon={<Ionicons name="sparkles" size={20} color="#FFFFFF" />}
            loading={analyzing}
            size="lg"
            title={t('diagnosis:resultsTitle')}
            variant="primary"
            onPress={handleStartAnalysis}
          />

          <Button
            disabled={analyzing}
            icon={<Ionicons name="camera-reverse-outline" size={20} color={theme.colors.textPrimary} />}
            size="md"
            style={styles.retakeBtn}
            title={t('diagnosis:retakePhoto')}
            variant="outline"
            onPress={() => router.back()}
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
  headerBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  imageCard: {
    width: '100%',
    height: 320,
    borderRadius: 20,
    overflow: 'hidden',
    marginBottom: 20,
    elevation: 3,
  },
  previewImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  selectorSection: {
    marginBottom: 20,
  },
  sectionLabel: {
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 10,
  },
  cropsRow: {
    gap: 8,
  },
  cropChip: {
    paddingHorizontal: 16,
    paddingVertical: 9,
    borderRadius: 20,
    borderWidth: 1.2,
  },
  cropChipText: {
    fontSize: 13,
    fontWeight: '700',
  },
  analyzingCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
    borderRadius: 14,
    borderWidth: 1,
    marginBottom: 20,
  },
  analyzingTextCol: {
    flex: 1,
  },
  analyzingTitle: {
    fontSize: 15,
    fontWeight: '700',
  },
  analyzingSub: {
    fontSize: 12,
    marginTop: 2,
    lineHeight: 16,
  },
  actions: {
    gap: 12,
  },
  errorCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    padding: 16,
    borderRadius: 14,
    borderWidth: 1.5,
    marginBottom: 20,
  },
  errorTextCol: {
    flex: 1,
  },
  errorCardTitle: {
    fontSize: 15,
    fontWeight: '800',
    marginBottom: 4,
  },
  errorCardDesc: {
    fontSize: 13,
    lineHeight: 18,
  },
  retakeBtn: {
    marginTop: 4,
  },
});
