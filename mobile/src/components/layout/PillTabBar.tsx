import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLanguage } from '../../hooks/useLanguage';
import { useTheme } from '../../hooks/useTheme';

export interface PillTabBarProps {
  state: any;
  descriptors: any;
  emitter?: any;
  navigateToTab?: (routeKey: string) => void;
  navigation?: any;
  insets: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
}

const TAB_ICONS: Record<string, { active: keyof typeof Ionicons.glyphMap; inactive: keyof typeof Ionicons.glyphMap }> = {
  index: { active: 'home', inactive: 'home-outline' },
  diagnose: { active: 'scan-circle', inactive: 'scan-circle-outline' },
  insights: { active: 'bar-chart', inactive: 'bar-chart-outline' },
  knowledge: { active: 'book', inactive: 'book-outline' },
  profile: { active: 'person', inactive: 'person-outline' },
};

// Clean, short 1-word tab labels per language to prevent any text clipping on mobile screens
const TAB_LABELS: Record<'en' | 'mr' | 'hi', Record<string, string>> = {
  en: {
    index: 'Home',
    diagnose: 'Diagnose',
    insights: 'Insights',
    knowledge: 'Learn',
    profile: 'Profile',
  },
  mr: {
    index: 'होम',
    diagnose: 'निदान',
    insights: 'माहिती',
    knowledge: 'ज्ञान',
    profile: 'प्रोफाइल',
  },
  hi: {
    index: 'होम',
    diagnose: 'जांच',
    insights: 'डेटा',
    knowledge: 'ज्ञान',
    profile: 'प्रोफाइल',
  },
};

export const PillTabBar: React.FC<PillTabBarProps> = ({
  state,
  descriptors,
  emitter,
  navigateToTab,
  navigation,
  insets,
}) => {
  const theme = useTheme();
  const { currentLanguage } = useLanguage();

  const [barWidth, setBarWidth] = useState(0);
  const slideAnim = useRef(new Animated.Value(0)).current;

  const routes = state?.routes || [];
  const numTabs = routes.length;
  const paddingH = 6;
  const tabWidth = barWidth > 0 && numTabs > 0 ? (barWidth - paddingH * 2) / numTabs : 0;

  useEffect(() => {
    if (tabWidth > 0 && state?.index !== undefined) {
      Animated.spring(slideAnim, {
        toValue: state.index * tabWidth,
        tension: 72,
        friction: 9,
        useNativeDriver: true,
      }).start();
    }
  }, [state?.index, tabWidth]);

  const langKey = (currentLanguage === 'mr' || currentLanguage === 'hi') ? currentLanguage : 'en';

  const getLabel = (route: any) => {
    return TAB_LABELS[langKey]?.[route.name] || route.name;
  };

  const bottomInset = Math.max(
    Platform.OS === 'ios' ? 24 : 16,
    (insets?.bottom || 0) + (Platform.OS === 'android' ? 8 : 4)
  );

  return (
    <View
      pointerEvents="box-none"
      style={[
        styles.outerContainer,
        {
          bottom: bottomInset,
        },
      ]}
    >
      <View
        onLayout={(e) => {
          const w = e.nativeEvent.layout.width;
          if (w > 0 && w !== barWidth) {
            setBarWidth(w);
          }
        }}
        style={[
          styles.pillContainer,
          {
            backgroundColor: theme.isDark ? '#0F172A' : '#FFFFFF',
            borderColor: theme.isDark ? 'rgba(51, 65, 85, 0.8)' : 'rgba(226, 232, 240, 0.95)',
          },
        ]}
      >
        {/* Sliding Pill Indicator */}
        {tabWidth > 0 && (
          <Animated.View
            style={[
              styles.slidingPill,
              {
                width: tabWidth,
                backgroundColor: theme.colors.primary,
                transform: [{ translateX: slideAnim }],
              },
            ]}
          />
        )}

        {/* Tab Items */}
        {routes.map((route: any, index: number) => {
          const isFocused = state.index === index;
          const iconPair = TAB_ICONS[route.name] || { active: 'ellipse', inactive: 'ellipse-outline' };
          const iconName = isFocused ? iconPair.active : iconPair.inactive;
          const label = getLabel(route);

          const onPress = () => {
            let event = { defaultPrevented: false };
            if (emitter?.emit) {
              event = emitter.emit({
                type: 'tabPress',
                target: route.key,
                canPreventDefault: true,
              });
            } else if (navigation?.emit) {
              event = navigation.emit({
                type: 'tabPress',
                target: route.key,
                canPreventDefault: true,
              });
            }

            if (!isFocused && !event?.defaultPrevented) {
              if (typeof navigateToTab === 'function') {
                navigateToTab(route.key);
              } else if (navigation && typeof navigation.navigate === 'function') {
                navigation.navigate(route.name);
              }
            }
          };

          const onLongPress = () => {
            if (emitter?.emit) {
              emitter.emit({
                type: 'tabLongPress',
                target: route.key,
              });
            } else if (navigation?.emit) {
              navigation.emit({
                type: 'tabLongPress',
                target: route.key,
              });
            }
          };

          const activeColor = '#FFFFFF';
          const inactiveColor = theme.isDark ? '#94A3B8' : '#64748B';
          const itemColor = isFocused ? activeColor : inactiveColor;

          return (
            <TouchableOpacity
              key={route.key || route.name}
              accessibilityRole="button"
              accessibilityState={isFocused ? { selected: true } : {}}
              accessibilityLabel={`${label}, tab`}
              activeOpacity={0.75}
              style={styles.tabItem}
              onPress={onPress}
              onLongPress={onLongPress}
            >
              <Ionicons
                name={iconName}
                size={isFocused ? 21 : 19}
                color={itemColor}
                style={isFocused ? styles.activeIcon : undefined}
              />
              <Text
                numberOfLines={1}
                style={[
                  styles.tabLabel,
                  {
                    color: itemColor,
                    fontWeight: isFocused ? '700' : '500',
                  },
                ]}
              >
                {label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  outerContainer: {
    position: 'absolute',
    left: 14,
    right: 14,
    zIndex: 999,
  },
  pillContainer: {
    height: 66,
    borderRadius: 33,
    borderWidth: 1.5,
    flexDirection: 'row',
    alignItems: 'center',
    padding: 6,
    ...Platform.select({
      ios: {
        shadowColor: '#000000',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.14,
        shadowRadius: 18,
      },
      android: {
        elevation: 14,
      },
    }),
  },
  slidingPill: {
    position: 'absolute',
    top: 5,
    bottom: 5,
    left: 6,
    borderRadius: 27,
    ...Platform.select({
      ios: {
        shadowColor: '#14532D',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.35,
        shadowRadius: 8,
      },
      android: {
        elevation: 6,
      },
    }),
  },
  tabItem: {
    flex: 1,
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 2,
    paddingVertical: 2,
    gap: 2,
  },
  activeIcon: {
    transform: [{ scale: 1.05 }],
  },
  tabLabel: {
    fontSize: 11,
    letterSpacing: -0.2,
  },
});

export default PillTabBar;
