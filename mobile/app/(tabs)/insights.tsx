import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { useTranslation } from 'react-i18next';
import { LineChart, BarChart, ProgressChart } from 'react-native-chart-kit';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Container } from '../../src/components/layout/Container';
import { Card } from '../../src/components/ui/Card';
import { useTheme } from '../../src/hooks/useTheme';

const { width } = Dimensions.get('window');
const chartWidth = width - 48;

export default function InsightsScreen() {
  const { t } = useTranslation(['dashboard', 'yield', 'common']);
  const theme = useTheme();

  const chartConfig = {
    backgroundGradientFrom: theme.colors.surface,
    backgroundGradientTo: theme.colors.surface,
    color: (opacity = 1) =>
      theme.isDark ? `rgba(34, 197, 94, ${opacity})` : `rgba(20, 83, 45, ${opacity})`,
    labelColor: (opacity = 1) =>
      theme.isDark ? `rgba(241, 245, 249, ${opacity})` : `rgba(23, 32, 51, ${opacity})`,
    strokeWidth: 2.5,
    barPercentage: 0.6,
    decimalPlaces: 0,
    propsForDots: {
      r: '5',
      strokeWidth: '2',
      stroke: theme.colors.primary,
    },
  };

  const trendData = {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
    datasets: [
      {
        data: [72, 85, 91, 88, 96],
        color: (opacity = 1) => `rgba(22, 163, 74, ${opacity})`,
        strokeWidth: 2.5,
      },
    ],
  };

  const diseaseDistributionData = {
    labels: ['Early Blight', 'Rust', 'Blast', 'Aphids', 'Mildew'],
    datasets: [
      {
        data: [12, 8, 6, 4, 3],
      },
    ],
  };

  const cropHealthRatios = {
    labels: ['Healthy', 'Mild', 'Severe'],
    data: [0.82, 0.14, 0.04],
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
        <Text style={[styles.title, { color: theme.colors.textPrimary }]}>
          Farm Analytics & Insights
        </Text>
        <Text style={[styles.subtitle, { color: theme.colors.textSecondary }]}>
          Deep learning diagnostic trendlines and crop output statistics
        </Text>
      </View>

      <Container contentContainerStyle={styles.containerContent}>
        {/* Overall Health Score Card */}
        <Card
          subtitle="Plot Health Index"
          title="Overall Plot Health Index"
          style={styles.card}
        >
          <View style={styles.ratioRow}>
            <View style={styles.scoreBox}>
              <Text style={[styles.scoreNumber, { color: theme.colors.success }]}>94.2%</Text>
              <Text style={[styles.scoreDesc, { color: theme.colors.textSecondary }]}>
                Optimal Foliage Health
              </Text>
            </View>
            <ProgressChart
              chartConfig={{
                ...chartConfig,
                color: (opacity = 1) => `rgba(22, 163, 74, ${opacity})`,
              }}
              data={cropHealthRatios}
              height={120}
              hideLegend={false}
              radius={28}
              strokeWidth={8}
              width={chartWidth * 0.55}
            />
          </View>
        </Card>

        {/* 5-Month Diagnostic Accuracy Trend */}
        <Card
          subtitle="Model Confidence History"
          title="Diagnostic Accuracy Trend (%)"
          style={styles.card}
        >
          <LineChart
            bezier
            chartConfig={chartConfig}
            data={trendData}
            height={190}
            style={styles.chart}
            width={chartWidth}
          />
        </Card>

        {/* Top Detected Pathogens / Pests */}
        <Card
          subtitle="Observed Incident Counts"
          title="Top Detected Pests & Pathogens"
          style={styles.card}
        >
          <BarChart
            chartConfig={chartConfig}
            data={diseaseDistributionData}
            height={200}
            showValuesOnTopOfBars
            style={styles.chart}
            width={chartWidth}
            yAxisLabel=""
            yAxisSuffix=""
          />
        </Card>

        {/* Seasonal Agriculture Calendar */}
        <Card
          subtitle="Upcoming Agricultural Tasks"
          title="Seasonal Operations Calendar"
          style={styles.card}
        >
          <View style={styles.calendarItem}>
            <View style={[styles.dateBadge, { backgroundColor: theme.colors.primaryLight }]}>
              <Text style={[styles.dateMonth, { color: theme.colors.primary }]}>NOV</Text>
              <Text style={[styles.dateDay, { color: theme.colors.primary }]}>10</Text>
            </View>
            <View style={styles.taskContent}>
              <Text style={[styles.taskTitle, { color: theme.colors.textPrimary }]}>
                Wheat Rabi Sowing & Seed Priming
              </Text>
              <Text style={[styles.taskDesc, { color: theme.colors.textSecondary }]}>
                Treat seed with Azotobacter & PSB culture before line sowing.
              </Text>
            </View>
          </View>

          <View style={styles.calendarItem}>
            <View style={[styles.dateBadge, { backgroundColor: theme.colors.warningLight }]}>
              <Text style={[styles.dateMonth, { color: '#B45309' }]}>NOV</Text>
              <Text style={[styles.dateDay, { color: '#B45309' }]}>18</Text>
            </View>
            <View style={styles.taskContent}>
              <Text style={[styles.taskTitle, { color: theme.colors.textPrimary }]}>
                Tomato Preventive Mancozeb Spray
              </Text>
              <Text style={[styles.taskDesc, { color: theme.colors.textSecondary }]}>
                Anticipated morning fog increases early blight vulnerability.
              </Text>
            </View>
          </View>
        </Card>
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
  title: {
    fontSize: 22,
    fontWeight: '800',
  },
  subtitle: {
    fontSize: 13,
    marginTop: 4,
    lineHeight: 18,
  },
  containerContent: {
    paddingBottom: 110,
  },
  card: {
    marginVertical: 10,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  ratioRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  scoreBox: {
    flex: 1,
  },
  scoreNumber: {
    fontSize: 32,
    fontWeight: '800',
  },
  scoreDesc: {
    fontSize: 13,
    marginTop: 4,
  },
  calendarItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  dateBadge: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dateMonth: {
    fontSize: 10,
    fontWeight: '800',
  },
  dateDay: {
    fontSize: 18,
    fontWeight: '800',
    marginTop: -2,
  },
  taskContent: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '700',
  },
  taskDesc: {
    fontSize: 12,
    marginTop: 2,
    lineHeight: 16,
  },
});
