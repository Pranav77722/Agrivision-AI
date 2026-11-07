import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../ui/Card';

interface StatsCardProps {
  healthyCount: number;
  atRiskCount: number;
  criticalCount: number;
  totalScans: number;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  healthyCount = 14,
  atRiskCount = 3,
  criticalCount = 1,
  totalScans = 18,
}) => {
  const { t } = useTranslation('dashboard');
  const theme = useTheme();

  return (
    <Card
      subtitle={t('farmStatus')}
      title={t('cropHealthSummary')}
    >
      <View style={styles.statsRow}>
        <View style={styles.statBox}>
          <Text style={[styles.statValue, { color: theme.colors.success }]}>
            {healthyCount}
          </Text>
          <Text style={[styles.statLabel, { color: theme.colors.textSecondary }]}>
            {t('healthyCrops')}
          </Text>
        </View>

        <View style={[styles.verticalDivider, { backgroundColor: theme.colors.border }]} />

        <View style={styles.statBox}>
          <Text style={[styles.statValue, { color: theme.colors.warning }]}>
            {atRiskCount}
          </Text>
          <Text style={[styles.statLabel, { color: theme.colors.textSecondary }]}>
            {t('atRisk')}
          </Text>
        </View>

        <View style={[styles.verticalDivider, { backgroundColor: theme.colors.border }]} />

        <View style={styles.statBox}>
          <Text style={[styles.statValue, { color: theme.colors.danger }]}>
            {criticalCount}
          </Text>
          <Text style={[styles.statLabel, { color: theme.colors.textSecondary }]}>
            {t('critical')}
          </Text>
        </View>

        <View style={[styles.verticalDivider, { backgroundColor: theme.colors.border }]} />

        <View style={styles.statBox}>
          <Text style={[styles.statValue, { color: theme.colors.primary }]}>
            {totalScans}
          </Text>
          <Text style={[styles.statLabel, { color: theme.colors.textSecondary }]}>
            {t('totalScans')}
          </Text>
        </View>
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 4,
  },
  statBox: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: 22,
    fontWeight: '800',
  },
  statLabel: {
    fontSize: 11,
    marginTop: 4,
    fontWeight: '600',
  },
  verticalDivider: {
    width: 1,
    height: 36,
  },
});

export default StatsCard;
