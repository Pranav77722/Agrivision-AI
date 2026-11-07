import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Container } from '../../src/components/layout/Container';
import { WeatherCard } from '../../src/components/dashboard/WeatherCard';
import { QuickActions } from '../../src/components/dashboard/QuickActions';
import { StatsCard } from '../../src/components/dashboard/StatsCard';
import { DiagnosisCard } from '../../src/components/diagnosis/DiagnosisCard';
import { Card } from '../../src/components/ui/Card';
import { LanguageSelector } from '../../src/components/common/LanguageSelector';
import { weatherService, LiveWeatherData } from '../../src/services/weatherService';
import { useAuthStore } from '../../src/store/authStore';
import { useDiagnosisStore } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';

export default function DashboardScreen() {
  const { t } = useTranslation(['dashboard', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const history = useDiagnosisStore((s) => s.history);
  const [refreshing, setRefreshing] = useState(false);
  const [weatherData, setWeatherData] = useState<LiveWeatherData | null>(null);
  const [deviceLocationName, setDeviceLocationName] = useState<string>(user?.district || 'Pune');

  const farmerName = user?.fullName || 'Kisan';

  React.useEffect(() => {
    let isMounted = true;
    const loadRealWeather = async () => {
      try {
        const data = await weatherService.fetchLiveWeather(undefined, undefined, user?.district);
        if (isMounted) {
          setWeatherData(data);
          if (data.location) {
            setDeviceLocationName(data.location);
          }
        }
      } catch (e) {
        console.warn('Real weather load failed:', e);
      }
    };
    loadRealWeather();
    return () => {
      isMounted = false;
    };
  }, [user?.district]);

  const onRefresh = async () => {
    setRefreshing(true);
    try {
      const data = await weatherService.fetchLiveWeather(undefined, undefined, user?.district);
      setWeatherData(data);
      if (data.location) {
        setDeviceLocationName(data.location);
      }
    } catch {}
    setRefreshing(false);
  };

  // Dynamic stats calculated from real scan history
  const totalScans = history.length;
  const criticalCount = history.filter(
    (h) => h.severity?.severityClass === 'severe' || h.severity?.severityClass === 'critical'
  ).length;
  const atRiskCount = history.filter(
    (h) => h.severity?.severityClass === 'moderate'
  ).length;
  const healthyCount = history.filter(
    (h) => h.isHealthy || h.severity?.severityClass === 'mild'
  ).length;

  return (
    <SafeArea style={styles.safeArea}>
      {/* Header bar */}
      <View
        style={[
          styles.headerBar,
          {
            backgroundColor: theme.colors.surface,
            borderBottomColor: theme.colors.border,
          },
        ]}
      >
        <View style={styles.userRow}>
          <Image
            source={require('../../assets/logo.png')}
            style={[
              styles.headerLogo,
              {
                borderColor: theme.isDark ? '#334155' : '#86EFAC',
              },
            ]}
            resizeMode="contain"
          />
          <View style={styles.userInfo}>
            <Text
              numberOfLines={1}
              style={[styles.greeting, { color: theme.colors.textPrimary }]}
            >
              {t('dashboard:greeting', { name: farmerName })}
            </Text>
            <View style={styles.locationRow}>
              <Ionicons name="location-sharp" size={12} color={theme.colors.primary} />
              <Text
                numberOfLines={1}
                style={[styles.villageSub, { color: theme.colors.textSecondary }]}
              >
                {weatherData?.fullHierarchy || (deviceLocationName ? `${deviceLocationName}, Sangamner • Ahilyanagar` : 'Gunjalwadi, Sangamner • Ahilyanagar')}
              </Text>
            </View>
          </View>
        </View>

        <View style={styles.headerRight}>
          <LanguageSelector compact />
          <TouchableOpacity
            accessibilityRole="button"
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            style={[styles.iconBtn, { backgroundColor: theme.colors.background }]}
            onPress={() => router.push('/reports' as any)}
          >
            <Ionicons name="notifications-outline" size={20} color={theme.colors.textPrimary} />
            <View style={styles.notifDot} />
          </TouchableOpacity>
        </View>
      </View>

      <Container
        contentContainerStyle={styles.contentContainer}
        refreshing={refreshing}
        onRefresh={onRefresh}
      >
        {/* Weather Card with Live Open-Meteo & GPS Data */}
        <WeatherCard
          locationName={weatherData?.formattedLocation || deviceLocationName || 'Gunjalwadi, Sangamner'}
          district={weatherData?.formattedLocation || deviceLocationName || 'Gunjalwadi, Sangamner'}
          hierarchy={weatherData?.district ? `${weatherData.district}, Maharashtra` : 'Ahilyanagar, Maharashtra'}
          temperature={weatherData?.temperature}
          temperatureMax={weatherData?.temperatureMax}
          temperatureMin={weatherData?.temperatureMin}
          humidity={weatherData?.humidity}
          windSpeed={weatherData?.windSpeed}
          rainfall={weatherData?.rainfall}
          condition={weatherData?.weatherCondition}
          icon={weatherData?.weatherIcon}
          isLiveGps={weatherData?.isLiveGps}
          updatedAt={weatherData?.updatedAt}
          sprayingNote={weatherData?.sprayingNote}
          onRefresh={onRefresh}
        />

        {/* Quick Actions Grid */}
        <QuickActions />

        {/* Health Summary Stats */}
        <StatsCard
          atRiskCount={atRiskCount}
          criticalCount={criticalCount}
          healthyCount={healthyCount}
          totalScans={totalScans}
        />

        {/* Dynamic Seasonal & Agronomic Advisory Card */}
        <Card
          subtitle={
            weatherData?.temperature
              ? `Real-time Field Advisory • ${weatherData.temperature}°C, ${weatherData.humidity}% RH`
              : 'Rabi Season Advisory'
          }
          title="Agronomic Field Insights"
          style={styles.seasonalCard}
        >
          <View style={styles.seasonalRow}>
            <Ionicons name="bulb-outline" size={24} color="#F59E0B" />
            <Text style={[styles.seasonalText, { color: theme.colors.textPrimary }]}>
              {weatherData?.sprayingNote
                ? `${weatherData.sprayingNote} Based on live humidity (${weatherData.humidity}%), maintain routine morning inspection for fungal spores.`
                : t('dashboard:seasonalAdvice')}
            </Text>
          </View>
        </Card>

        {/* Recent Diagnoses Section */}
        <View style={styles.sectionHeader}>
          <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
            {t('dashboard:recentDiagnoses')}
          </Text>
          <TouchableOpacity onPress={() => router.push('/archive' as any)}>
            <Text style={[styles.viewAllText, { color: theme.colors.primary }]}>
              {t('dashboard:viewAllScans')}
            </Text>
          </TouchableOpacity>
        </View>

        {history.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Ionicons name="leaf-outline" size={36} color={theme.colors.textMuted} />
            <Text style={[styles.emptyText, { color: theme.colors.textSecondary }]}>
              {t('dashboard:noDiagnosesYet')}
            </Text>
          </Card>
        ) : (
          history.slice(0, 3).map((item) => (
            <DiagnosisCard
              key={item.id}
              item={item}
              onPress={() => router.push(`/diagnosis/${item.id}` as any)}
            />
          ))
        )}
      </Container>
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
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  userRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    flex: 1,
    marginRight: 8,
  },
  userInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    marginTop: 2,
  },
  headerLogo: {
    width: 40,
    height: 40,
    borderRadius: 10,
    borderWidth: 1.2,
    backgroundColor: '#FFFFFF',
  },
  greeting: {
    fontSize: 15.5,
    fontWeight: '800',
    letterSpacing: -0.2,
  },
  villageSub: {
    fontSize: 11.5,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  iconBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  notifDot: {
    position: 'absolute',
    top: 7,
    right: 8,
    width: 7,
    height: 7,
    borderRadius: 3.5,
    backgroundColor: '#DC2626',
  },
  contentContainer: {
    paddingBottom: 110,
  },
  seasonalCard: {
    marginVertical: 10,
  },
  seasonalRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    paddingVertical: 4,
  },
  seasonalText: {
    fontSize: 13,
    lineHeight: 20,
    flex: 1,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 14,
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: '700',
  },
  viewAllText: {
    fontSize: 13,
    fontWeight: '700',
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
