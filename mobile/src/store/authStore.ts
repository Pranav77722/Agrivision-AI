import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserProfile } from '../types';

interface AuthStoreState {
  user: UserProfile | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string, refreshToken: string, user: UserProfile) => Promise<void>;
  register: (token: string, refreshToken: string, user: UserProfile) => Promise<void>;
  updateProfile: (user: Partial<UserProfile>) => Promise<void>;
  logout: () => Promise<void>;
  initializeAuth: () => Promise<void>;
}

const TOKEN_KEY = '@agrivision_auth_token';
const REFRESH_TOKEN_KEY = '@agrivision_refresh_token';
const USER_KEY = '@agrivision_user_profile';

const DEFAULT_DEMO_USER: UserProfile = {
  id: 'farmer_01',
  fullName: 'Pranav Khaire',
  phoneNumber: '+91 98765 43210',
  email: 'khairepranav124@gmail.com',
  village: 'Gunjalwadi',
  district: 'Sangamner, Ahilyanagar',
  state: 'Maharashtra',
  totalAcres: 5.0,
  primaryCrops: ['tomato', 'wheat', 'soybean'],
  createdAt: new Date().toISOString(),
};

export const useAuthStore = create<AuthStoreState>((set, get) => ({
  user: DEFAULT_DEMO_USER,
  token: 'mock_jwt_token_agrivision',
  refreshToken: 'mock_refresh_token_agrivision',
  isAuthenticated: true,
  isLoading: false,

  login: async (token, refreshToken, user) => {
    try {
      await AsyncStorage.multiSet([
        [TOKEN_KEY, token],
        [REFRESH_TOKEN_KEY, refreshToken],
        [USER_KEY, JSON.stringify(user)],
      ]);
      set({ user, token, refreshToken, isAuthenticated: true });
    } catch (error) {
      console.error('Failed to save auth state to AsyncStorage:', error);
    }
  },

  register: async (token, refreshToken, user) => {
    try {
      await AsyncStorage.multiSet([
        [TOKEN_KEY, token],
        [REFRESH_TOKEN_KEY, refreshToken],
        [USER_KEY, JSON.stringify(user)],
      ]);
      set({ user, token, refreshToken, isAuthenticated: true });
    } catch (error) {
      console.error('Failed to persist registration:', error);
    }
  },

  updateProfile: async (partialUser) => {
    const current = get().user;
    if (!current) return;
    const updated = { ...current, ...partialUser };
    await AsyncStorage.setItem(USER_KEY, JSON.stringify(updated));
    set({ user: updated });
  },

  logout: async () => {
    try {
      await AsyncStorage.multiRemove([TOKEN_KEY, REFRESH_TOKEN_KEY, USER_KEY]);
      set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  },

  initializeAuth: async () => {
    set({ isLoading: true });
    try {
      const items = await AsyncStorage.multiGet([TOKEN_KEY, REFRESH_TOKEN_KEY, USER_KEY]);
      const token = items[0][1];
      const refreshToken = items[1][1];
      const userStr = items[2][1];

      if (token && userStr) {
        set({
          token,
          refreshToken,
          user: JSON.parse(userStr),
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        // Fallback demo user for immediate seamless testing
        set({
          token: 'mock_jwt_token_agrivision',
          refreshToken: 'mock_refresh_token_agrivision',
          user: DEFAULT_DEMO_USER,
          isAuthenticated: true,
          isLoading: false,
        });
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
      set({ isLoading: false });
    }
  },
}));
