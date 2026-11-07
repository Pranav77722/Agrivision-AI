import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Ionicons } from '@expo/vector-icons';
import { SafeArea } from '../../src/components/layout/SafeArea';
import { Header } from '../../src/components/layout/Header';
import { assistantService } from '../../src/services/assistantService';
import { firebaseDbService } from '../../src/services/firebase';
import { ChatMessage } from '../../src/types';
import { formatDate } from '../../src/utils/formatters';
import { useTheme } from '../../src/hooks/useTheme';
import { useLanguage } from '../../src/hooks/useLanguage';

export default function AssistantScreen() {
  const { t } = useTranslation(['assistant', 'common']);
  const theme = useTheme();
  const router = useRouter();
  const { currentLanguage } = useLanguage();
  const flatListRef = useRef<FlatList>(null);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome-01',
      sender: 'assistant',
      text:
        currentLanguage === 'mr'
          ? 'नमस्कार शेतकरी बंधू! मी तुमचा अॅग्रीव्हिजन AI सल्लागार आहे. आज मी तुम्हाला कोणती माहिती देऊ?'
          : currentLanguage === 'hi'
          ? 'नमस्ते किसान साथी! मैं आपका एग्रीविज़न AI कृषि सलाहकार हूँ। आज आपकी फसल के लिए क्या सहायता कर सकता हूँ?'
          : 'Hello Farmer! I am your Agrivision AI Advisor. How can I help protect your crops today?',
      timestamp: new Date().toISOString(),
    },
  ]);

  const suggestedQuestions = [
    t('assistant:q1'),
    t('assistant:q2'),
    t('assistant:q3'),
    t('assistant:q4'),
  ];

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || loading) return;

    const userMsg: ChatMessage = {
      id: 'user-' + Date.now(),
      sender: 'user',
      text: query,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    // Save user message to Firebase
    firebaseDbService.saveChatMessage(userMsg);

    try {
      const response = await assistantService.sendMessage(query, currentLanguage);
      setMessages((prev) => [...prev, response]);
      // Save AI response to Firebase
      firebaseDbService.saveChatMessage(response);
    } catch (e) {
      console.warn('Chat send error:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true });
    }, 150);
  }, [messages, loading]);

  const languageLabel =
    currentLanguage === 'mr' ? 'मराठी' : currentLanguage === 'hi' ? 'हिंदी' : 'English';

  return (
    <SafeArea style={styles.safeArea}>
      <Header
        showBack
        rightElement={
          <View style={[styles.langBadge, { backgroundColor: theme.colors.primaryLight }]}>
            <Text style={[styles.langBadgeText, { color: theme.colors.primary }]}>
              {languageLabel}
            </Text>
          </View>
        }
        subtitle={t('assistant:languageIndicator', { lang: languageLabel })}
        title={t('assistant:title')}
        onBack={() => router.back()}
      />

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        style={styles.keyboardContainer}
      >
        <FlatList
          ref={flatListRef}
          contentContainerStyle={styles.messagesList}
          data={messages}
          keyExtractor={(item) => item.id}
          ListFooterComponent={
            loading ? (
              <View style={[styles.bubble, styles.assistantBubble, { backgroundColor: theme.colors.surface }]}>
                <Text style={[styles.typingText, { color: theme.colors.textSecondary }]}>
                  {t('assistant:aiTyping')}
                </Text>
              </View>
            ) : undefined
          }
          ListHeaderComponent={
            <View style={styles.suggestedContainer}>
              <Text style={[styles.suggestedHeader, { color: theme.colors.textSecondary }]}>
                {t('assistant:suggestedHeader')}
              </Text>
              <View style={styles.suggestedWrap}>
                {suggestedQuestions.map((q, idx) => (
                  <TouchableOpacity
                    key={idx}
                    activeOpacity={0.8}
                    style={[
                      styles.suggestedChip,
                      {
                        backgroundColor: theme.colors.surface,
                        borderColor: theme.colors.border,
                      },
                    ]}
                    onPress={() => handleSend(q)}
                  >
                    <Ionicons name="chatbubble-outline" size={14} color={theme.colors.primary} />
                    <Text
                      numberOfLines={1}
                      style={[styles.suggestedChipText, { color: theme.colors.textPrimary }]}
                    >
                      {q}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          }
          renderItem={({ item }) => {
            const isUser = item.sender === 'user';
            return (
              <View
                style={[
                  styles.bubble,
                  isUser ? styles.userBubble : styles.assistantBubble,
                  {
                    backgroundColor: isUser ? theme.colors.primary : theme.colors.surface,
                    borderColor: theme.colors.border,
                  },
                ]}
              >
                {!isUser && (
                  <View style={styles.assistantRow}>
                    <Ionicons name="sparkles" size={14} color={theme.colors.secondary} />
                    <Text style={[styles.assistantTag, { color: theme.colors.secondary }]}>
                      Kisan AI
                    </Text>
                  </View>
                )}
                <Text
                  style={[
                    styles.messageText,
                    { color: isUser ? '#FFFFFF' : theme.colors.textPrimary },
                  ]}
                >
                  {item.text}
                </Text>
                <Text
                  style={[
                    styles.timeText,
                    { color: isUser ? 'rgba(255,255,255,0.7)' : theme.colors.textMuted },
                  ]}
                >
                  {formatDate(item.timestamp, 'hh:mm a')}
                </Text>
              </View>
            );
          }}
        />

        {/* Input Bar */}
        <View
          style={[
            styles.inputBar,
            {
              backgroundColor: theme.colors.surface,
              borderTopColor: theme.colors.border,
            },
          ]}
        >
          <TouchableOpacity
            accessibilityRole="button"
            style={[styles.micBtn, { backgroundColor: theme.colors.primaryLight }]}
            onPress={() => handleSend(suggestedQuestions[0])}
          >
            <Ionicons name="mic" size={20} color={theme.colors.primary} />
          </TouchableOpacity>

          <TextInput
            placeholder={t('assistant:inputPlaceholder')}
            placeholderTextColor={theme.colors.textMuted}
            style={[
              styles.input,
              {
                color: theme.colors.textPrimary,
                backgroundColor: theme.colors.background,
                borderColor: theme.colors.border,
              },
            ]}
            value={input}
            onChangeText={setInput}
            onSubmitEditing={() => handleSend()}
          />

          <TouchableOpacity
            accessibilityRole="button"
            disabled={!input.trim() || loading}
            style={[
              styles.sendBtn,
              {
                backgroundColor: input.trim() ? theme.colors.primary : theme.colors.border,
              },
            ]}
            onPress={() => handleSend()}
          >
            <Ionicons name="send" size={18} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeArea>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
  },
  keyboardContainer: {
    flex: 1,
  },
  langBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  langBadgeText: {
    fontSize: 12,
    fontWeight: '700',
  },
  messagesList: {
    padding: 16,
    paddingBottom: 24,
  },
  suggestedContainer: {
    marginBottom: 16,
  },
  suggestedHeader: {
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  suggestedWrap: {
    gap: 6,
  },
  suggestedChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 16,
    borderWidth: 1,
  },
  suggestedChipText: {
    fontSize: 12,
    fontWeight: '600',
    flex: 1,
  },
  bubble: {
    maxWidth: '82%',
    padding: 12,
    borderRadius: 16,
    marginVertical: 4,
    borderWidth: 1,
  },
  userBubble: {
    alignSelf: 'flex-end',
    borderBottomRightRadius: 4,
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 4,
  },
  assistantRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 4,
  },
  assistantTag: {
    fontSize: 11,
    fontWeight: '800',
    textTransform: 'uppercase',
  },
  messageText: {
    fontSize: 14,
    lineHeight: 20,
  },
  timeText: {
    fontSize: 10,
    marginTop: 4,
    alignSelf: 'flex-end',
  },
  typingText: {
    fontSize: 13,
    fontStyle: 'italic',
  },
  inputBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderTopWidth: 1,
    gap: 8,
  },
  micBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    fontSize: 14,
    borderWidth: 1,
    maxHeight: 100,
  },
  sendBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
