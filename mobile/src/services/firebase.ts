import { initializeApp, getApps, getApp } from 'firebase/app';
import {
  initializeAuth,
  getAuth,
  signInWithCredential,
  GoogleAuthProvider,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User as FirebaseUser,
} from 'firebase/auth';
// @ts-ignore
import { getReactNativePersistence } from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  getFirestore,
  collection,
  doc,
  setDoc,
  getDocs,
  getDoc,
  query,
  orderBy,
  limit,
} from 'firebase/firestore';
import { DiagnosisRecord, UserProfile, ChatMessage, FarmReport } from '../types';

const firebaseConfig = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY || '',
  authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN || 'agrivision-4223d.firebaseapp.com',
  projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID || 'agrivision-4223d',
  storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET || 'agrivision-4223d.firebasestorage.app',
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID || '',
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
export const db = getFirestore(app);

// Initialize Firebase Auth with AsyncStorage persistence for React Native
let authInstance: any;
try {
  authInstance = initializeAuth(app, {
    persistence: getReactNativePersistence(AsyncStorage),
  });
} catch {
  authInstance = getAuth(app);
}
export const auth = authInstance;

// Firestore Collections
export const COLLECTIONS = {
  DIAGNOSES: 'diagnoses',
  USERS: 'users',
  CHATS: 'chats',
  REPORTS: 'reports',
} as const;

export const firebaseAuthService = {
  // Sign in using Google ID token via Firebase GoogleAuthProvider
  signInWithGoogleToken: async (idToken: string): Promise<FirebaseUser | null> => {
    try {
      const credential = GoogleAuthProvider.credential(idToken);
      const userCredential = await signInWithCredential(auth, credential);
      return userCredential.user;
    } catch (e) {
      console.warn('Firebase Google credential sign in error (falling back to mock user):', e);
      return null;
    }
  },

  // Email and password sign-in
  loginWithEmail: async (email: string, pass: string): Promise<FirebaseUser> => {
    const userCredential = await signInWithEmailAndPassword(auth, email, pass);
    return userCredential.user;
  },

  // Email and password registration
  registerWithEmail: async (email: string, pass: string): Promise<FirebaseUser> => {
    const userCredential = await createUserWithEmailAndPassword(auth, email, pass);
    return userCredential.user;
  },

  // Sign out
  logout: async (): Promise<void> => {
    await signOut(auth);
  },

  // Get current authenticated user
  getCurrentUser: (): FirebaseUser | null => {
    return auth.currentUser;
  },

  // Subscribe to auth state changes
  onAuthChange: (callback: (user: FirebaseUser | null) => void) => {
    return onAuthStateChanged(auth, callback);
  },
};

export const firebaseDbService = {
  // Save or update Diagnosis in Firestore
  saveDiagnosis: async (diagnosis: DiagnosisRecord): Promise<void> => {
    try {
      const docRef = doc(db, COLLECTIONS.DIAGNOSES, diagnosis.id);
      await setDoc(docRef, {
        ...diagnosis,
        updatedAt: new Date().toISOString(),
      });
    } catch (e) {
      console.warn('Firebase saveDiagnosis fallback (offline/mock):', e);
    }
  },

  // Fetch recent diagnoses
  getDiagnoses: async (count = 20): Promise<DiagnosisRecord[]> => {
    try {
      const q = query(
        collection(db, COLLECTIONS.DIAGNOSES),
        orderBy('createdAt', 'desc'),
        limit(count)
      );
      const snapshot = await getDocs(q);
      const records: DiagnosisRecord[] = [];
      snapshot.forEach((d) => {
        records.push(d.data() as DiagnosisRecord);
      });
      return records;
    } catch (e) {
      console.warn('Firebase getDiagnoses fallback:', e);
      return [];
    }
  },

  // Save User Profile in Firestore
  saveUserProfile: async (user: UserProfile): Promise<void> => {
    try {
      const docRef = doc(db, COLLECTIONS.USERS, user.id);
      // Fire-and-forget or fast timeout so offline/mock does not hang UI
      Promise.race([
        setDoc(docRef, user, { merge: true }),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Firestore timeout')), 1200)),
      ]).catch((e) => console.warn('Firebase saveUserProfile notice:', e?.message || e));
    } catch (e) {
      console.warn('Firebase saveUserProfile fallback:', e);
    }
  },

  // Save Chat Message in Firestore
  saveChatMessage: async (message: ChatMessage): Promise<void> => {
    try {
      const docRef = doc(db, COLLECTIONS.CHATS, message.id);
      await setDoc(docRef, message);
    } catch (e) {
      console.warn('Firebase saveChatMessage fallback:', e);
    }
  },

  // Save Farm Report in Firestore
  saveReport: async (report: FarmReport): Promise<void> => {
    try {
      const docRef = doc(db, COLLECTIONS.REPORTS, report.id);
      await setDoc(docRef, report);
    } catch (e) {
      console.warn('Firebase saveReport fallback:', e);
    }
  },
};

export default firebaseDbService;
