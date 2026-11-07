import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../ui/Card';

export interface WeatherCardProps {
  locationName?: string;
  district?: string;
  hierarchy?: string;
  temperature?: number;
  temperatureMax?: number;
  temperatureMin?: number;
  humidity?: number;
  windSpeed?: number;
  rainfall?: number;
  condition?: string;
  icon?: 'sunny' | 'partly-sunny' | 'cloudy' | 'rainy' | 'thunderstorm';
  isLiveGps?: boolean;
  updatedAt?: string;
  sprayingNote?: string;
  onRefresh?: () => void;
}

export const WeatherCard: React.FC<WeatherCardProps> = ({
  locationName,
  district = 'Gunjalwadi, Sangamner',
  hierarchy,
  temperature = 29,
  temperatureMax,
  temperatureMin,
  humidity = 28,
  windSpeed = 12,
  rainfall = 0,
  condition = 'Clear Sky',
  icon = 'sunny',
  isLiveGps = true,
  updatedAt,
  sprayingNote,
  onRefresh,
}) => {
  const { t } = useTranslation('dashboard');
  const theme = useTheme();

  const displayLocation = locationName || district;

  const renderWeatherIcon = () => {
    switch (icon) {
      case 'sunny':
        return <Ionicons name="sunny" size={34} color="#F59E0B" />;
      case 'cloudy':
        return <Ionicons name="cloudy" size={34} color={theme.isDark ? '#94A3B8' : '#64748B'} />;
      case 'rainy':
        return <Ionicons name="rainy" size={34} color="#3B82F6" />;
      case 'thunderstorm':
        return <Ionicons name="thunderstorm" size={34} color="#6366F1" />;
      case 'partly-sunny':
      default:
        return <Ionicons name="partly-sunny" size={34} color="#F59E0B" />;
    }
  };

  return (
    <Card
      style={[
        styles.card,
        {
          backgroundColor: theme.isDark ? '#142838' : '#ECFDF5',
          borderColor: theme.isDark ? '#1E3A52' : '#A7F3D0',
        },
      ]}
    >
      <View style={styles.topRow}>
        <View style={styles.locationContainer}>
          <View style={styles.badgeRow}>
            <Ionicons name="location" size={13} color={theme.colors.primary} />
            <Text numberOfLines={1} style={[styles.district, { color: theme.colors.primary }]}>
              {displayLocation}
            </Text>
            {isLiveGps && (
              <View style={styles.liveGpsBadge}>
                <View style={styles.liveGpsDot} />
                <Text style={styles.liveGpsText}>Live GPS</Text>
              </View>
            )}
          </View>
          <Text style={[styles.title, { color: theme.colors.textPrimary }]}>
            {t('weatherTitle', { defaultValue: 'Hyper-local Weather' })}
          </Text>
          <Text numberOfLines={1} style={[styles.conditionText, { color: theme.colors.textSecondary }]}>
            {hierarchy ? `${hierarchy} • ` : ''}{condition} {updatedAt ? `• ${updatedAt}` : ''}
          </Text>
        </View>

        <View style={styles.tempBadge}>
          {renderWeatherIcon()}
          <View>
            <Text style={[styles.tempText, { color: theme.colors.textPrimary }]}>
              {temperature}°C
            </Text>
            {temperatureMax !== undefined && temperatureMin !== undefined && (
              <Text style={[styles.tempRange, { color: theme.colors.textSecondary }]}>
                {temperatureMax}° / {temperatureMin}°
              </Text>
            )}
          </View>
        </View>
      </View>

      <View style={[styles.divider, { backgroundColor: theme.isDark ? '#1E3A52' : '#D1FAE5' }]} />

      <View style={styles.metricsRow}>
        <View style={styles.metricItem}>
          <Ionicons name="water-outline" size={18} color="#0EA5E9" />
          <Text style={[styles.metricLabel, { color: theme.colors.textSecondary }]}>
            {t('humidity', { defaultValue: 'Humidity' })}
          </Text>
          <Text style={[styles.metricValue, { color: theme.colors.textPrimary }]}>
            {humidity}%
          </Text>
        </View>

        <View style={styles.metricItem}>
          <Ionicons name="speedometer-outline" size={18} color="#6366F1" />
          <Text style={[styles.metricLabel, { color: theme.colors.textSecondary }]}>
            {t('windSpeed', { defaultValue: 'Wind' })}
          </Text>
          <Text style={[styles.metricValue, { color: theme.colors.textPrimary }]}>
            {windSpeed} km/h
          </Text>
        </View>

        <View style={styles.metricItem}>
          <Ionicons name="rainy-outline" size={18} color="#3B82F6" />
          <Text style={[styles.metricLabel, { color: theme.colors.textSecondary }]}>
            {t('rainfall', { defaultValue: 'Rainfall' })}
          </Text>
          <Text style={[styles.metricValue, { color: theme.colors.textPrimary }]}>
            {rainfall} mm
          </Text>
        </View>
      </View>

      {/* Spraying & Agricultural Advisory Pill */}
      {sprayingNote && (
        <View
          style={[
            styles.advisoryRow,
            {
              backgroundColor: theme.isDark ? 'rgba(6, 78, 59, 0.4)' : '#DCFCE7',
              borderColor: theme.isDark ? '#065F46' : '#86EFAC',
            },
          ]}
        >
          <Ionicons name="checkmark-circle" size={15} color="#15803D" />
          <Text
            numberOfLines={2}
            style={[styles.advisoryText, { color: theme.isDark ? '#86EFAC' : '#14532D' }]}
          >
            {sprayingNote}
          </Text>
        </View>
      )}
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
  },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  locationContainer: {
    flex: 1,
  },
  badgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
    gap: 5,
  },
  district: {
    fontSize: 11.5,
    fontWeight: '800',
    textTransform: 'uppercase',
    letterSpacing: 0.3,
  },
  liveGpsBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(22, 163, 74, 0.15)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  liveGpsDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#16A34A',
  },
  liveGpsText: {
    fontSize: 9.5,
    fontWeight: '700',
    color: '#15803D',
  },
  title: {
    fontSize: 16,
    fontWeight: '800',
  },
  conditionText: {
    fontSize: 11.5,
    marginTop: 2,
  },
  tempBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  tempText: {
    fontSize: 26,
    fontWeight: '800',
    lineHeight: 30,
  },
  tempRange: {
    fontSize: 10.5,
    fontWeight: '600',
  },
  divider: {
    height: 1,
    marginVertical: 12,
  },
  metricsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metricItem: {
    alignItems: 'center',
    flex: 1,
    gap: 2,
  },
  metricLabel: {
    fontSize: 11,
    fontWeight: '500',
  },
  metricValue: {
    fontSize: 14,
    fontWeight: '700',
  },
  advisoryRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 12,
    paddingHorizontal: 10,
    paddingVertical: 8,
    borderRadius: 10,
    borderWidth: 1,
  },
  advisoryText: {
    fontSize: 11.5,
    flex: 1,
    lineHeight: 16,
    fontWeight: '600',
  },
});

export default WeatherCard;
