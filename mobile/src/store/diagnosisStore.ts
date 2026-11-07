import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { DiagnosisRecord, CropType } from '../types';

interface DiagnosisState {
  currentDiagnosis: DiagnosisRecord | null;
  history: DiagnosisRecord[];
  selectedCrop: CropType;
  capturedImageUri: string | null;
  isLoading: boolean;
  error: string | null;
  setSelectedCrop: (crop: CropType) => void;
  setCapturedImageUri: (uri: string | null) => void;
  setCurrentDiagnosis: (diagnosis: DiagnosisRecord | null) => void;
  addDiagnosis: (diagnosis: DiagnosisRecord) => Promise<void>;
  removeDiagnosis: (id: string) => Promise<void>;
  initializeHistory: () => Promise<void>;
}

const HISTORY_STORAGE_KEY = '@agrivision_diagnosis_history';

export const INITIAL_DEMO_DIAGNOSES: DiagnosisRecord[] = [
  {
    id: 'diag-001',
    crop: 'tomato',
    imageUri: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?auto=format&fit=crop&w=600&q=80',
    diseaseName: 'Tomato Early Blight (Alternaria solani)',
    isHealthy: false,
    confidence: 96.4,
    severity: {
      healthyAreaPercent: 78.5,
      diseasedAreaPercent: 21.5,
      severityClass: 'moderate',
      urgencyWindow: 'Within 48 Hours',
    },
    ensemble: {
      consensusClass: 'Tomato Early Blight',
      consensusConfidence: 96.4,
      agreementRate: 100,
      isHighAgreement: true,
      models: [
        { modelName: 'ResNet-50', predictedClass: 'Early Blight', confidence: 97.1, weight: 0.35 },
        { modelName: 'EfficientNet-B4', predictedClass: 'Early Blight', confidence: 96.2, weight: 0.40 },
        { modelName: 'Vision Transformer (ViT)', predictedClass: 'Early Blight', confidence: 95.8, weight: 0.25 },
      ],
    },
    explainability: {
      heatmapUri: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?auto=format&fit=crop&w=600&q=80',
      originalImageUri: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?auto=format&fit=crop&w=600&q=80',
      focusDescription: 'High saliency around concentric brown target-board lesions with chlorotic yellow halo.',
      attentionRegions: [
        { label: 'Concentric Target Rings', score: 0.94 },
        { label: 'Marginal Chlorosis', score: 0.88 },
        { label: 'Petiole Necrosis', score: 0.72 },
      ],
    },
    symptoms: [
      'Brown circular lesions with concentric target-board rings on older leaves.',
      'Yellow chlorotic halos surrounding necrotic spots.',
      'Premature defoliation starting from the plant base.',
    ],
    recommendations: {
      organic: [
        'Spray Neem Oil (10,000 PPM) at 3 ml per liter of water.',
        'Apply Trichoderma viride bio-fungicide in soil drenching @ 5 kg/acre.',
        'Prune lower infected foliage to enhance airflow.',
      ],
      chemical: [
        'Mancozeb 75% WP @ 2.0 g/L or Chlorothalonil 75% WP @ 2.0 g/L.',
        'For high severity: Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L.',
      ],
      cultural: [
        'Avoid overhead sprinkler watering; use drip irrigation.',
        'Maintain 60 cm row-to-row spacing for sunlight penetration.',
        'Rotate crops with non-solanaceous species like corn or pulses.',
      ],
      safety: [
        'Wear protective mask and nitrile gloves while preparing spray broth.',
        'Observe 7-day pre-harvest interval before picking tomatoes.',
      ],
      dosage: '2.0 g per liter of clean water',
      intervalDays: 10,
    },
    createdAt: new Date(Date.now() - 86400000 * 2).toISOString(),
  },
  {
    id: 'diag-002',
    crop: 'rice',
    imageUri: 'https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=600&q=80',
    diseaseName: 'Rice Blast (Magnaporthe oryzae)',
    isHealthy: false,
    confidence: 94.8,
    severity: {
      healthyAreaPercent: 88.2,
      diseasedAreaPercent: 11.8,
      severityClass: 'mild',
      urgencyWindow: 'Within 48-72 Hours',
    },
    ensemble: {
      consensusClass: 'Rice Blast',
      consensusConfidence: 94.8,
      agreementRate: 100,
      isHighAgreement: true,
      models: [
        { modelName: 'ResNet-50', predictedClass: 'Rice Blast', confidence: 95.5, weight: 0.35 },
        { modelName: 'EfficientNet-B4', predictedClass: 'Rice Blast', confidence: 94.6, weight: 0.40 },
        { modelName: 'Vision Transformer (ViT)', predictedClass: 'Rice Blast', confidence: 94.1, weight: 0.25 },
      ],
    },
    explainability: {
      heatmapUri: 'https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=600&q=80',
      originalImageUri: 'https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=600&q=80',
      focusDescription: 'Attention centered along spindle-shaped lesions with gray centers and reddish-brown borders.',
      attentionRegions: [
        { label: 'Spindle-shaped Leaf Spots', score: 0.91 },
        { label: 'Necrotic Collar Point', score: 0.82 },
      ],
    },
    symptoms: [
      'Diamond/spindle-shaped lesions on leaves with white-gray centers.',
      'Brown borders that coalesce to dry out leaf blades.',
    ],
    recommendations: {
      organic: [
        'Foliar spray with Pseudomonas fluorescens @ 5 g/L.',
        'Apply fermented cow dung & butter milk extract.',
      ],
      chemical: [
        'Tricyclazole 75% WP @ 0.6 g/L of water.',
        'Isoprothiolane 40% EC @ 1.5 ml/L.',
      ],
      cultural: [
        'Avoid excessive split urea applications during damp overcast weather.',
        'Maintain proper field drainage.',
      ],
      safety: [
        'Spray during morning hours after dew has dried.',
      ],
      dosage: '0.6 g / L',
      intervalDays: 14,
    },
    createdAt: new Date(Date.now() - 86400000 * 5).toISOString(),
  },
];

export const useDiagnosisStore = create<DiagnosisState>((set, get) => ({
  currentDiagnosis: INITIAL_DEMO_DIAGNOSES[0],
  history: INITIAL_DEMO_DIAGNOSES,
  selectedCrop: 'tomato',
  capturedImageUri: null,
  isLoading: false,
  error: null,

  setSelectedCrop: (crop) => set({ selectedCrop: crop }),
  setCapturedImageUri: (uri) => set({ capturedImageUri: uri }),
  setCurrentDiagnosis: (diagnosis) => set({ currentDiagnosis: diagnosis }),

  addDiagnosis: async (diagnosis) => {
    const updated = [diagnosis, ...get().history];
    set({ history: updated, currentDiagnosis: diagnosis });
    try {
      await AsyncStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(updated));
    } catch (err) {
      console.warn('Failed to save diagnosis history to storage:', err);
    }
  },

  removeDiagnosis: async (id) => {
    const updated = get().history.filter((item) => item.id !== id);
    set({ history: updated });
    try {
      await AsyncStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(updated));
    } catch (err) {
      console.warn('Failed to remove diagnosis from storage:', err);
    }
  },

  initializeHistory: async () => {
    try {
      const stored = await AsyncStorage.getItem(HISTORY_STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          set({ history: parsed, currentDiagnosis: parsed[0] });
          return;
        }
      }
      // If nothing stored, initialize with demo diagnoses and persist
      await AsyncStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(INITIAL_DEMO_DIAGNOSES));
      set({ history: INITIAL_DEMO_DIAGNOSES, currentDiagnosis: INITIAL_DEMO_DIAGNOSES[0] });
    } catch (err) {
      console.warn('Error reading diagnosis history:', err);
    }
  },
}));
