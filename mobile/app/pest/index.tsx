import React, { useState } from 'react';
import { View, Text, Image, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Badge } from '../../src/components/ui/Badge';
import { Button } from '../../src/components/ui/Button';
import { pestService } from '../../src/services/pestService';
import { PestDetectionResult } from '../../src/types';
import { pickImageFromGallery } from '../../src/utils/imageUtils';
import { useTheme } from '../../src/hooks/useTheme';

export default function PestDetectionScreen() {
  const { t } = useTranslation(['pest', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [showBoxes, setShowBoxes] = useState(true);
  const [result, setResult] = useState<PestDetectionResult | null>(null);

  const handleScanPest = async () => {
    try {
      const picked = await pickImageFromGallery();
      const imageUri =
        picked?.uri ||
        'https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=600&q=80';
      setLoading(true);
      const res = await pestService.detectPests(imageUri);
      setResult(res);
    } catch {
      Alert.alert(t('common:error'), t('common:networkError'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('pest:subtitle')}
        title={t('pest:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Upload Action Card */}
        <Card style={styles.uploadCard}>
          <Ionicons name="bug" size={48} color={theme.colors.danger} />
          <Text style={[styles.uploadPrompt, { color: theme.colors.textPrimary }]}>
            {t('pest:uploadPrompt')}
          </Text>
          <Button
            icon={<Ionicons name="scan" size={20} color="#FFFFFF" />}
            loading={loading}
            size="lg"
            title={t('pest:detectPests')}
            variant="primary"
            onPress={handleScanPest}
          />
        </Card>

        {result && (
          <View style={styles.resultsContainer}>
            {/* Visual with Bounding Boxes */}
            <View style={styles.imageWrapper}>
              <Image source={{ uri: result.imageUri }} style={styles.detectedImage} />
              {showBoxes &&
                result.boundingBoxes.map((box, idx) => (
                  <View
                    key={idx}
                    style={[
                      styles.boundingBox,
                      {
                        left: `${box.x}%`,
                        top: `${box.y}%`,
                        width: `${box.width}%`,
                        height: `${box.height}%`,
                      },
                    ]}
                  >
                    <View style={styles.boxTag}>
                      <Text style={styles.boxTagText}>{box.label}</Text>
                    </View>
                  </View>
                ))}
            </View>

            <View style={styles.toggleRow}>
              <TouchableOpacity
                style={styles.toggleBtn}
                onPress={() => setShowBoxes(!showBoxes)}
              >
                <Ionicons
                  name={showBoxes ? 'eye' : 'eye-off'}
                  size={18}
                  color={theme.colors.primary}
                />
                <Text style={[styles.toggleText, { color: theme.colors.primary }]}>
                  {t('pest:boundingBoxToggle')}
                </Text>
              </TouchableOpacity>
            </View>

            {/* Species Identification Card */}
            <Card
              subtitle={t('pest:threatHigh')}
              title={t('pest:pestDetectedCount', { count: result.totalPests })}
              style={styles.infoCard}
            >
              <View style={styles.pestRow}>
                <View>
                  <Text style={[styles.pestSpecies, { color: theme.colors.textPrimary }]}>
                    {result.species}
                  </Text>
                  <Text style={[styles.pestCount, { color: theme.colors.textSecondary }]}>
                    {t('pest:count')}: {result.totalPests}
                  </Text>
                </View>
                <Badge label={result.threatLevel.toUpperCase()} variant="danger" />
              </View>
            </Card>

            {/* Organic Solutions */}
            <Card title={t('pest:organicControl')} style={styles.controlCard}>
              {result.organicControl.map((sol, i) => (
                <View key={i} style={styles.bulletRow}>
                  <Ionicons name="checkmark-circle" size={16} color={theme.colors.success} />
                  <Text style={[styles.controlText, { color: theme.colors.textSecondary }]}>
                    {sol}
                  </Text>
                </View>
              ))}
            </Card>

            {/* Chemical Sprays */}
            <Card title={t('pest:chemicalControl')} style={styles.controlCard}>
              {result.chemicalControl.map((sol, i) => (
                <View key={i} style={styles.bulletRow}>
                  <Ionicons name="flask-outline" size={16} color={theme.colors.danger} />
                  <Text style={[styles.controlText, { color: theme.colors.textSecondary }]}>
                    {sol}
                  </Text>
                </View>
              ))}
            </Card>

            {/* Biological Control */}
            <Card title={t('pest:biologicalControl')} style={styles.controlCard}>
              {result.biologicalControl.map((sol, i) => (
                <View key={i} style={styles.bulletRow}>
                  <Ionicons name="shield-outline" size={16} color={theme.colors.primary} />
                  <Text style={[styles.controlText, { color: theme.colors.textSecondary }]}>
                    {sol}
                  </Text>
                </View>
              ))}
            </Card>
          </View>
        )}
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
  uploadCard: {
    alignItems: 'center',
    padding: 24,
    gap: 12,
    marginBottom: 16,
  },
  uploadPrompt: {
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 8,
  },
  resultsContainer: {
    gap: 12,
  },
  imageWrapper: {
    width: '100%',
    height: 260,
    borderRadius: 16,
    overflow: 'hidden',
    position: 'relative',
  },
  detectedImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  boundingBox: {
    position: 'absolute',
    borderWidth: 2.5,
    borderColor: '#DC2626',
    backgroundColor: 'rgba(220, 38, 38, 0.15)',
  },
  boxTag: {
    position: 'absolute',
    top: -20,
    left: 0,
    backgroundColor: '#DC2626',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  boxTagText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '700',
  },
  toggleRow: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginBottom: 6,
  },
  toggleBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  toggleText: {
    fontSize: 13,
    fontWeight: '700',
  },
  infoCard: {
    marginVertical: 4,
  },
  pestRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  pestSpecies: {
    fontSize: 18,
    fontWeight: '800',
  },
  pestCount: {
    fontSize: 13,
    marginTop: 2,
  },
  controlCard: {
    marginVertical: 4,
  },
  bulletRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    marginBottom: 8,
  },
  controlText: {
    fontSize: 13,
    lineHeight: 18,
    flex: 1,
  },
});
