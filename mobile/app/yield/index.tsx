import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { BarChart } from 'react-native-chart-kit';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Card } from '../../src/components/ui/Card';
import { Input } from '../../src/components/ui/Input';
import { Button } from '../../src/components/ui/Button';
import { Badge } from '../../src/components/ui/Badge';
import { yieldService } from '../../src/services/yieldService';
import { YieldPredictionInput, YieldPredictionResult, CropType } from '../../src/types';
import { formatCurrencyInr } from '../../src/utils/formatters';
import { useTheme } from '../../src/hooks/useTheme';

const { width } = Dimensions.get('window');
const chartWidth = width - 48;

const CROPS: CropType[] = [
  'tomato',
  'rice',
  'wheat',
  'cotton',
  'potato',
  'maize',
  'soybean',
  'sugarcane',
];

const SOILS: ('black' | 'alluvial' | 'red' | 'sandy' | 'clay')[] = [
  'black',
  'alluvial',
  'red',
  'sandy',
  'clay',
];

const SEASONS: ('kharif' | 'rabi' | 'zaid')[] = ['kharif', 'rabi', 'zaid'];

const IRRIGATIONS: ('drip' | 'sprinkler' | 'canal' | 'rainfed')[] = [
  'drip',
  'sprinkler',
  'canal',
  'rainfed',
];

export default function YieldPredictionScreen() {
  const { t } = useTranslation(['yield', 'diagnosis', 'common']);
  const theme = useTheme();
  const router = useRouter();

  const [form, setForm] = useState<YieldPredictionInput>({
    crop: 'tomato',
    district: 'Pune',
    areaAcres: 3,
    soilType: 'black',
    season: 'rabi',
    irrigation: 'drip',
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<YieldPredictionResult | null>(null);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await yieldService.predictYield(form);
      setResult(res);
    } catch (err) {
      console.warn('Yield prediction failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const chartConfig = {
    backgroundGradientFrom: theme.colors.surface,
    backgroundGradientTo: theme.colors.surface,
    color: (opacity = 1) =>
      theme.isDark ? `rgba(34, 197, 94, ${opacity})` : `rgba(20, 83, 45, ${opacity})`,
    labelColor: (opacity = 1) =>
      theme.isDark ? `rgba(241, 245, 249, ${opacity})` : `rgba(23, 32, 51, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.65,
    decimalPlaces: 0,
  };

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('yield:subtitle')}
        title={t('yield:title')}
        onBack={() => router.back()}
      />

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Form Input Card */}
        <Card title={t('yield:title')} style={styles.formCard}>
          {/* Crop Selector */}
          <Text style={[styles.fieldLabel, { color: theme.colors.textPrimary }]}>
            {t('yield:cropLabel')}
          </Text>
          <ScrollView horizontal contentContainerStyle={styles.chipRow} showsHorizontalScrollIndicator={false}>
            {CROPS.map((c) => (
              <TouchableOpacity
                key={c}
                activeOpacity={0.8}
                style={[
                  styles.chip,
                  {
                    backgroundColor: form.crop === c ? theme.colors.primary : theme.colors.surface,
                    borderColor: form.crop === c ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setForm({ ...form, crop: c })}
              >
                <Text
                  style={[
                    styles.chipText,
                    { color: form.crop === c ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {t(`diagnosis:crops.${c}` as any, { defaultValue: c })}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {/* District Input */}
          <Input
            containerStyle={styles.inputSpacing}
            label={t('yield:districtLabel')}
            placeholder="e.g. Pune, Nashik, Aurangabad"
            value={form.district}
            onChangeText={(v) => setForm({ ...form, district: v })}
          />

          {/* Area Input */}
          <Input
            containerStyle={styles.inputSpacing}
            keyboardType="numeric"
            label={t('yield:areaLabel')}
            placeholder="3.5"
            value={String(form.areaAcres)}
            onChangeText={(v) => setForm({ ...form, areaAcres: parseFloat(v) || 1 })}
          />

          {/* Soil Type */}
          <Text style={[styles.fieldLabel, { color: theme.colors.textPrimary }]}>
            {t('yield:soilLabel')}
          </Text>
          <ScrollView horizontal contentContainerStyle={styles.chipRow} showsHorizontalScrollIndicator={false}>
            {SOILS.map((soil) => (
              <TouchableOpacity
                key={soil}
                activeOpacity={0.8}
                style={[
                  styles.chip,
                  {
                    backgroundColor: form.soilType === soil ? theme.colors.primary : theme.colors.surface,
                    borderColor: form.soilType === soil ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setForm({ ...form, soilType: soil })}
              >
                <Text
                  style={[
                    styles.chipText,
                    { color: form.soilType === soil ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {t(`yield:soils.${soil}` as any)}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {/* Season */}
          <Text style={[styles.fieldLabel, { color: theme.colors.textPrimary }]}>
            {t('yield:seasonLabel')}
          </Text>
          <ScrollView horizontal contentContainerStyle={styles.chipRow} showsHorizontalScrollIndicator={false}>
            {SEASONS.map((s) => (
              <TouchableOpacity
                key={s}
                activeOpacity={0.8}
                style={[
                  styles.chip,
                  {
                    backgroundColor: form.season === s ? theme.colors.primary : theme.colors.surface,
                    borderColor: form.season === s ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setForm({ ...form, season: s })}
              >
                <Text
                  style={[
                    styles.chipText,
                    { color: form.season === s ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {t(`yield:seasons.${s}` as any)}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {/* Irrigation Source */}
          <Text style={[styles.fieldLabel, { color: theme.colors.textPrimary }]}>
            {t('yield:irrigationLabel')}
          </Text>
          <ScrollView horizontal contentContainerStyle={styles.chipRow} showsHorizontalScrollIndicator={false}>
            {IRRIGATIONS.map((irr) => (
              <TouchableOpacity
                key={irr}
                activeOpacity={0.8}
                style={[
                  styles.chip,
                  {
                    backgroundColor: form.irrigation === irr ? theme.colors.primary : theme.colors.surface,
                    borderColor: form.irrigation === irr ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setForm({ ...form, irrigation: irr })}
              >
                <Text
                  style={[
                    styles.chipText,
                    { color: form.irrigation === irr ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {t(`yield:irrigations.${irr}` as any)}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <Button
            icon={<Ionicons name="calculator-outline" size={20} color="#FFFFFF" />}
            loading={loading}
            size="lg"
            style={styles.predictBtn}
            title={t('yield:predictButton')}
            variant="primary"
            onPress={handlePredict}
          />
        </Card>

        {/* Prediction Results */}
        {result && (
          <View style={styles.resultsWrapper}>
            {/* Output Hero Card */}
            <Card
              subtitle={t('yield:totalExpected', { total: result.totalEstimatedYield })}
              title={t('yield:resultsHeader')}
              style={[styles.heroResult, { backgroundColor: theme.isDark ? '#052E16' : '#DCFCE7' }]}
            >
              <View style={styles.yieldMetricRow}>
                <View>
                  <Text style={[styles.yieldNumber, { color: theme.colors.primary }]}>
                    {result.estimatedYieldPerAcre}
                  </Text>
                  <Text style={[styles.yieldUnit, { color: theme.colors.textSecondary }]}>
                    {t('yield:yieldUnit')}
                  </Text>
                </View>

                <View style={styles.revenueBox}>
                  <Text style={[styles.revLabel, { color: theme.colors.textSecondary }]}>
                    Projected Revenue
                  </Text>
                  <Text style={[styles.revValue, { color: theme.colors.primary }]}>
                    {formatCurrencyInr(result.projectedRevenueInr)}
                  </Text>
                </View>
              </View>

              <View style={styles.rangeBadgeRow}>
                <Badge
                  label={`Expected Range: ${result.rangeMin} - ${result.rangeMax} Qtl`}
                  variant="success"
                />
              </View>
            </Card>

            {/* Historical Benchmarks Comparison Chart */}
            <Card subtitle="Your Plot vs Historical Regional Average" title="Comparative Performance" style={styles.formCard}>
              <BarChart
                chartConfig={chartConfig}
                data={{
                  labels: ['District Avg', 'Your Forecast', 'Optimal High'],
                  datasets: [
                    {
                      data: [
                        result.historicalAveragePerAcre,
                        result.estimatedYieldPerAcre,
                        Math.round(result.estimatedYieldPerAcre * 1.15),
                      ],
                    },
                  ],
                }}
                height={200}
                showValuesOnTopOfBars
                style={styles.chart}
                width={chartWidth}
                yAxisLabel=""
                yAxisSuffix=""
              />
            </Card>

            {/* Risk Factors List */}
            <Card title={t('yield:riskFactorsHeader')} style={styles.formCard}>
              {result.riskFactors.map((risk, idx) => (
                <View key={idx} style={styles.riskRow}>
                  <Ionicons name="warning-outline" size={18} color={theme.colors.warning} />
                  <Text style={[styles.riskText, { color: theme.colors.textSecondary }]}>
                    {risk}
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
  formCard: {
    marginBottom: 16,
  },
  fieldLabel: {
    fontSize: 14,
    fontWeight: '700',
    marginTop: 10,
    marginBottom: 8,
  },
  chipRow: {
    gap: 8,
    paddingBottom: 6,
  },
  chip: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1.2,
  },
  chipText: {
    fontSize: 12,
    fontWeight: '700',
  },
  inputSpacing: {
    marginTop: 12,
    marginBottom: 4,
  },
  predictBtn: {
    marginTop: 20,
  },
  resultsWrapper: {
    gap: 12,
  },
  heroResult: {
    borderWidth: 1.5,
  },
  yieldMetricRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 8,
  },
  yieldNumber: {
    fontSize: 36,
    fontWeight: '900',
  },
  yieldUnit: {
    fontSize: 13,
    fontWeight: '600',
  },
  revenueBox: {
    alignItems: 'flex-end',
  },
  revLabel: {
    fontSize: 12,
  },
  revValue: {
    fontSize: 20,
    fontWeight: '800',
  },
  rangeBadgeRow: {
    marginTop: 8,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 12,
  },
  riskRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    marginBottom: 10,
  },
  riskText: {
    fontSize: 13,
    lineHeight: 18,
    flex: 1,
  },
});

