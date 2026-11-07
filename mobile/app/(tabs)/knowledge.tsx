import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Modal,
  Linking,
  Platform,
} from 'react-native';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Container } from '../../src/components/layout/Container';
import { Card } from '../../src/components/ui/Card';
import { Input } from '../../src/components/ui/Input';
import { Badge } from '../../src/components/ui/Badge';
import { Button } from '../../src/components/ui/Button';
import { knowledgeService, REAL_KNOWLEDGE_ARTICLES } from '../../src/services/knowledgeService';
import { KnowledgeArticle } from '../../src/types';
import { useTheme } from '../../src/hooks/useTheme';

export default function KnowledgeTabScreen() {
  const { t } = useTranslation(['knowledge', 'common']);
  const theme = useTheme();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [articles, setArticles] = useState<KnowledgeArticle[]>(REAL_KNOWLEDGE_ARTICLES);
  const [refreshing, setRefreshing] = useState(false);
  const [activeArticle, setActiveArticle] = useState<KnowledgeArticle | null>(null);

  const categories = [
    { id: 'all', label: t('common:viewAll', { defaultValue: 'All Guides' }), icon: 'apps-outline' as const },
    { id: 'diseases', label: t('knowledge:categoryDiseases', { defaultValue: 'Diseases' }), icon: 'leaf-outline' as const },
    { id: 'pests', label: t('knowledge:categoryPests', { defaultValue: 'Pests' }), icon: 'bug-outline' as const },
    { id: 'fertilizers', label: t('knowledge:categoryFertilizers', { defaultValue: 'Fertilizers' }), icon: 'flask-outline' as const },
    { id: 'water', label: 'Irrigation', icon: 'water-outline' as const },
    { id: 'schemes', label: 'Govt Schemes', icon: 'ribbon-outline' as const },
  ];

  const loadArticles = async () => {
    try {
      const data = await knowledgeService.getArticles(selectedCategory, searchQuery);
      setArticles(data);
    } catch {
      setArticles(REAL_KNOWLEDGE_ARTICLES);
    }
  };

  useEffect(() => {
    loadArticles();
  }, [selectedCategory]);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadArticles();
    setRefreshing(false);
  };

  const filteredArticles = useMemo(() => {
    if (!searchQuery.trim()) return articles;
    const q = searchQuery.toLowerCase().trim();
    return articles.filter(
      (art) =>
        art.title.toLowerCase().includes(q) ||
        art.summary.toLowerCase().includes(q) ||
        art.content.toLowerCase().includes(q)
    );
  }, [articles, searchQuery]);

  const toggleBookmark = (id: string) => {
    setArticles((prev) =>
      prev.map((a) => (a.id === id ? { ...a, isBookmarked: !a.isBookmarked } : a))
    );
  };

  const handleOpenSource = (url?: string) => {
    if (url) {
      Linking.openURL(url).catch((err) => {
        console.warn('Could not open external URL:', err);
      });
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
        <View>
          <Text style={[styles.screenTitle, { color: theme.colors.textPrimary }]}>
            {t('knowledge:title', { defaultValue: 'Agricultural Knowledge Base' })}
          </Text>
          <Text style={[styles.screenSubtitle, { color: theme.colors.textSecondary }]}>
            Verified research guides from ICAR, KVK & Krishi Vibhag
          </Text>
        </View>
      </View>

      <Container
        contentContainerStyle={styles.containerContent}
        refreshing={refreshing}
        onRefresh={onRefresh}
      >
        {/* Search Bar */}
        <Input
          containerStyle={styles.searchInput}
          leftIcon={<Ionicons name="search" size={20} color={theme.colors.textSecondary} />}
          placeholder={t('knowledge:searchPlaceholder', { defaultValue: 'Search pests, diseases, fertilizers...' })}
          value={searchQuery}
          onChangeText={setSearchQuery}
        />

        {/* Category Horizontal Filter */}
        <ScrollView
          horizontal
          contentContainerStyle={styles.categoryScroll}
          showsHorizontalScrollIndicator={false}
        >
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat.id;
            return (
              <TouchableOpacity
                key={cat.id}
                activeOpacity={0.8}
                style={[
                  styles.categoryChip,
                  {
                    backgroundColor: isSelected ? theme.colors.primary : theme.colors.surface,
                    borderColor: isSelected ? theme.colors.primary : theme.colors.border,
                  },
                ]}
                onPress={() => setSelectedCategory(cat.id)}
              >
                <Ionicons
                  name={cat.icon}
                  size={16}
                  color={isSelected ? '#FFFFFF' : theme.colors.textSecondary}
                />
                <Text
                  style={[
                    styles.categoryChipText,
                    { color: isSelected ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {cat.label}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>

        {/* Section Header */}
        <View style={styles.sectionHeader}>
          <Text style={[styles.sectionTitle, { color: theme.colors.textPrimary }]}>
            {t('knowledge:featuredArticles', { defaultValue: 'Verified Agronomic Guides' })}
          </Text>
          <Text style={[styles.articleCount, { color: theme.colors.textSecondary }]}>
            {filteredArticles.length} guides
          </Text>
        </View>

        {filteredArticles.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Ionicons name="document-text-outline" size={40} color={theme.colors.textMuted} />
            <Text style={[styles.emptyText, { color: theme.colors.textSecondary }]}>
              {t('knowledge:noBookmarks', { defaultValue: 'No articles found matching your query.' })}
            </Text>
          </Card>
        ) : (
          filteredArticles.map((article) => (
            <TouchableOpacity
              key={article.id}
              activeOpacity={0.88}
              onPress={() => setActiveArticle(article)}
            >
              <Card style={styles.articleCard}>
                <View style={styles.articleHeader}>
                  <View style={styles.badgeRow}>
                    <Badge
                      label={article.category.toUpperCase()}
                      variant="info"
                    />
                    {article.sourceAuthority && (
                      <View
                        style={[
                          styles.authorityPill,
                          {
                            backgroundColor: theme.isDark ? '#064E3B' : '#DCFCE7',
                            borderColor: theme.isDark ? '#065F46' : '#86EFAC',
                          },
                        ]}
                      >
                        <Ionicons name="shield-checkmark" size={11} color="#15803D" />
                        <Text
                          numberOfLines={1}
                          style={[styles.authorityText, { color: '#15803D' }]}
                        >
                          {article.sourceAuthority}
                        </Text>
                      </View>
                    )}
                  </View>

                  <TouchableOpacity
                    hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                    onPress={() => toggleBookmark(article.id)}
                  >
                    <Ionicons
                      name={article.isBookmarked ? 'bookmark' : 'bookmark-outline'}
                      size={22}
                      color={article.isBookmarked ? theme.colors.primary : theme.colors.textMuted}
                    />
                  </TouchableOpacity>
                </View>

                <Text style={[styles.articleTitle, { color: theme.colors.textPrimary }]}>
                  {article.title}
                </Text>
                <Text
                  numberOfLines={3}
                  style={[styles.articleSummary, { color: theme.colors.textSecondary }]}>
                  {article.summary}
                </Text>

                <View style={styles.articleFooter}>
                  <View style={styles.readTimeRow}>
                    <Ionicons name="time-outline" size={14} color={theme.colors.textMuted} />
                    <Text style={[styles.readTimeText, { color: theme.colors.textMuted }]}>
                      {t('knowledge:readTime', { minutes: article.readTimeMinutes, defaultValue: `${article.readTimeMinutes} min read` })}
                    </Text>
                    {article.sourceName && (
                      <Text
                        numberOfLines={1}
                        style={[styles.sourceNameText, { color: theme.colors.textMuted }]}
                      >
                        • {article.sourceName}
                      </Text>
                    )}
                  </View>
                  <Text style={[styles.readLink, { color: theme.colors.primary }]}>
                    Read Guide →
                  </Text>
                </View>
              </Card>
            </TouchableOpacity>
          ))
        )}
      </Container>

      {/* Full Article Reader Modal */}
      <Modal
        animationType="slide"
        transparent
        visible={!!activeArticle}
        onRequestClose={() => setActiveArticle(null)}
      >
        <View style={styles.readerBackdrop}>
          <View
            style={[
              styles.readerModal,
              {
                backgroundColor: theme.colors.surface,
                borderColor: theme.colors.border,
              },
            ]}
          >
            {/* Modal Header */}
            <View style={styles.readerHeader}>
              <View style={styles.readerHeaderBadgeRow}>
                <Badge label={activeArticle?.category.toUpperCase() || 'GUIDE'} variant="info" />
                {activeArticle?.sourceAuthority && (
                  <View style={styles.readerAuthPill}>
                    <Ionicons name="shield-checkmark" size={12} color="#15803D" />
                    <Text numberOfLines={1} style={styles.readerAuthText}>
                      {activeArticle.sourceAuthority}
                    </Text>
                  </View>
                )}
              </View>

              <TouchableOpacity
                style={[
                  styles.closeBtn,
                  { backgroundColor: theme.isDark ? '#334155' : '#F1F5F9' },
                ]}
                onPress={() => setActiveArticle(null)}
              >
                <Ionicons name="close" size={20} color={theme.colors.textSecondary} />
              </TouchableOpacity>
            </View>

            {/* Scrollable Article Content */}
            <ScrollView
              contentContainerStyle={styles.readerScroll}
              showsVerticalScrollIndicator={true}
            >
              <Text style={[styles.readerTitle, { color: theme.colors.textPrimary }]}>
                {activeArticle?.title}
              </Text>

              {/* Source Card */}
              {activeArticle?.sourceName && (
                <View
                  style={[
                    styles.sourceCard,
                    {
                      backgroundColor: theme.isDark ? '#1E293B' : '#F0FDF4',
                      borderColor: theme.isDark ? '#334155' : '#BBF7D0',
                    },
                  ]}
                >
                  <View style={styles.sourceCardHeader}>
                    <Ionicons name="globe-outline" size={16} color={theme.colors.primary} />
                    <Text style={[styles.sourceCardTitle, { color: theme.colors.primary }]}>
                      Official Research Source
                    </Text>
                  </View>
                  <Text style={[styles.sourceCardName, { color: theme.colors.textPrimary }]}>
                    {activeArticle.sourceName}
                  </Text>
                  {activeArticle.sourceUrl && (
                    <TouchableOpacity
                      activeOpacity={0.7}
                      style={styles.openWebBtn}
                      onPress={() => handleOpenSource(activeArticle.sourceUrl)}
                    >
                      <Ionicons name="open-outline" size={14} color="#15803D" />
                      <Text style={styles.openWebText}>Open Official Portal ↗</Text>
                    </TouchableOpacity>
                  )}
                </View>
              )}

              {/* Body Content */}
              <Text style={[styles.readerBody, { color: theme.colors.textPrimary }]}>
                {activeArticle?.content}
              </Text>

              {/* Official Website Button */}
              {activeArticle?.sourceUrl && (
                <Button
                  icon={<Ionicons name="globe" size={18} color="#FFFFFF" />}
                  style={styles.officialBtn}
                  title="Visit Official Website / Portal ↗"
                  onPress={() => handleOpenSource(activeArticle.sourceUrl)}
                />
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>
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
    fontSize: 20,
    fontWeight: '800',
    letterSpacing: -0.3,
  },
  screenSubtitle: {
    fontSize: 12.5,
    marginTop: 3,
    lineHeight: 17,
  },
  containerContent: {
    paddingBottom: 110,
  },
  searchInput: {
    marginTop: 12,
    marginBottom: 8,
  },
  categoryScroll: {
    gap: 8,
    paddingVertical: 4,
    paddingBottom: 8,
  },
  categoryChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 13,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
  },
  categoryChipText: {
    fontSize: 12.5,
    fontWeight: '700',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 14,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '800',
  },
  articleCount: {
    fontSize: 12,
    fontWeight: '600',
  },
  articleCard: {
    marginBottom: 12,
    padding: 16,
  },
  articleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  badgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    flex: 1,
    flexWrap: 'wrap',
  },
  authorityPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
    borderWidth: 1,
    maxWidth: '75%',
  },
  authorityText: {
    fontSize: 10.5,
    fontWeight: '700',
  },
  articleTitle: {
    fontSize: 16,
    fontWeight: '800',
    lineHeight: 22,
    marginBottom: 6,
  },
  articleSummary: {
    fontSize: 13,
    lineHeight: 19,
    marginBottom: 12,
  },
  articleFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: 'rgba(150, 150, 150, 0.12)',
  },
  readTimeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    flex: 1,
  },
  readTimeText: {
    fontSize: 11.5,
  },
  sourceNameText: {
    fontSize: 11.5,
    flex: 1,
  },
  readLink: {
    fontSize: 12.5,
    fontWeight: '700',
  },
  emptyCard: {
    alignItems: 'center',
    padding: 32,
    gap: 8,
  },
  emptyText: {
    fontSize: 13,
    textAlign: 'center',
  },

  // Reader Modal Styles
  readerBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    justifyContent: 'flex-end',
  },
  readerModal: {
    height: '88%',
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    borderWidth: 1,
    paddingHorizontal: 20,
    paddingTop: 16,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -8 },
        shadowOpacity: 0.2,
        shadowRadius: 16,
      },
      android: {
        elevation: 20,
      },
    }),
  },
  readerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingBottom: 14,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(150, 150, 150, 0.15)',
  },
  readerHeaderBadgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    flex: 1,
  },
  readerAuthPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#DCFCE7',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 8,
  },
  readerAuthText: {
    fontSize: 10.5,
    fontWeight: '700',
    color: '#15803D',
  },
  closeBtn: {
    width: 34,
    height: 34,
    borderRadius: 17,
    justifyContent: 'center',
    alignItems: 'center',
  },
  readerScroll: {
    paddingVertical: 18,
    paddingBottom: 40,
  },
  readerTitle: {
    fontSize: 20,
    fontWeight: '900',
    lineHeight: 28,
    marginBottom: 14,
  },
  sourceCard: {
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    marginBottom: 18,
  },
  sourceCardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 4,
  },
  sourceCardTitle: {
    fontSize: 11.5,
    fontWeight: '800',
    textTransform: 'uppercase',
  },
  sourceCardName: {
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 8,
  },
  openWebBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  openWebText: {
    fontSize: 12.5,
    fontWeight: '700',
    color: '#15803D',
  },
  readerBody: {
    fontSize: 14.5,
    lineHeight: 24,
    marginBottom: 24,
  },
  officialBtn: {
    width: '100%',
    marginBottom: 20,
  },
});
