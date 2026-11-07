import React, { useState, useMemo } from 'react';
import { View, Text, StyleSheet, Alert, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { Container } from '../../src/components/layout/Container';
import { Input } from '../../src/components/ui/Input';
import { DiagnosisCard } from '../../src/components/diagnosis/DiagnosisCard';
import { EmptyState } from '../../src/components/common/EmptyState';
import { useDiagnosisStore } from '../../src/store/diagnosisStore';
import { useTheme } from '../../src/hooks/useTheme';

export default function ArchiveScreen() {
  const { t } = useTranslation(['archive', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const history = useDiagnosisStore((s) => s.history);
  const removeDiagnosis = useDiagnosisStore((s) => s.removeDiagnosis);

  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<'all' | 'infected' | 'resolved'>('all');

  const filteredHistory = useMemo(() => {
    return history.filter((item) => {
      const matchesQuery =
        query.trim() === '' ||
        item.diseaseName.toLowerCase().includes(query.toLowerCase()) ||
        item.crop.toLowerCase().includes(query.toLowerCase());

      const matchesFilter =
        filter === 'all' ||
        (filter === 'infected' && !item.isHealthy) ||
        (filter === 'resolved' && item.isHealthy);

      return matchesQuery && matchesFilter;
    });
  }, [history, query, filter]);

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        subtitle={t('archive:subtitle')}
        title={t('archive:title')}
        onBack={() => router.back()}
      />

      <Container contentContainerStyle={styles.containerContent}>
        <Input
          containerStyle={styles.searchInput}
          leftIcon={<Ionicons name="search" size={20} color={theme.colors.textSecondary} />}
          placeholder={t('archive:searchArchive')}
          value={query}
          onChangeText={setQuery}
        />

        {/* Filter Chips */}
        <View style={styles.filterRow}>
          <TouchableOpacity
            style={[
              styles.chip,
              {
                backgroundColor: filter === 'all' ? theme.colors.primary : theme.colors.surface,
                borderColor: filter === 'all' ? theme.colors.primary : theme.colors.border,
              },
            ]}
            onPress={() => setFilter('all')}
          >
            <Text
              style={[
                styles.chipText,
                { color: filter === 'all' ? '#FFFFFF' : theme.colors.textPrimary },
              ]}
            >
              {t('archive:filterAll')}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.chip,
              {
                backgroundColor: filter === 'infected' ? theme.colors.primary : theme.colors.surface,
                borderColor: filter === 'infected' ? theme.colors.primary : theme.colors.border,
              },
            ]}
            onPress={() => setFilter('infected')}
          >
            <Text
              style={[
                styles.chipText,
                { color: filter === 'infected' ? '#FFFFFF' : theme.colors.textPrimary },
              ]}
            >
              {t('archive:filterActive')}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.chip,
              {
                backgroundColor: filter === 'resolved' ? theme.colors.primary : theme.colors.surface,
                borderColor: filter === 'resolved' ? theme.colors.primary : theme.colors.border,
              },
            ]}
            onPress={() => setFilter('resolved')}
          >
            <Text
              style={[
                styles.chipText,
                { color: filter === 'resolved' ? '#FFFFFF' : theme.colors.textPrimary },
              ]}
            >
              {t('archive:filterResolved')}
            </Text>
          </TouchableOpacity>
        </View>

        {filteredHistory.length === 0 ? (
          <EmptyState
            description={t('archive:emptyArchiveDesc')}
            icon="archive-outline"
            title={t('archive:emptyArchiveTitle')}
          />
        ) : (
          filteredHistory.map((item) => (
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
  containerContent: {
    paddingBottom: 40,
  },
  searchInput: {
    marginTop: 8,
    marginBottom: 8,
  },
  filterRow: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 14,
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
});

