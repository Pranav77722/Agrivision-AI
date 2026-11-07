export interface UserProfile {
  id: string;
  fullName: string;
  phoneNumber: string;
  email?: string;
  village: string;
  district: string;
  state: string;
  totalAcres: number;
  primaryCrops: string[];
  createdAt: string;
}

export interface AuthState {
  user: UserProfile | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export type CropType =
  | 'tomato'
  | 'rice'
  | 'wheat'
  | 'cotton'
  | 'potato'
  | 'maize'
  | 'soybean'
  | 'sugarcane';

export type SeverityClass = 'healthy' | 'mild' | 'moderate' | 'severe' | 'critical';

export interface TreatmentRecommendation {
  organic: string[];
  chemical: string[];
  cultural: string[];
  safety: string[];
  dosage: string;
  intervalDays: number;
}

export interface IndividualModelPrediction {
  modelName: string;
  predictedClass: string;
  confidence: number;
  weight: number;
}

export interface EnsembleResult {
  consensusClass: string;
  consensusConfidence: number;
  agreementRate: number;
  isHighAgreement: boolean;
  models: IndividualModelPrediction[];
}

export interface SeverityResult {
  healthyAreaPercent: number;
  diseasedAreaPercent: number;
  severityClass: SeverityClass;
  urgencyWindow: string;
  maskOverlayUri?: string;
}

export interface ExplainabilityResult {
  heatmapUri: string;
  originalImageUri: string;
  focusDescription: string;
  attentionRegions: { label: string; score: number }[];
}

export interface DiagnosisRecord {
  id: string;
  crop: CropType;
  imageUri: string;
  diseaseName: string;
  isHealthy: boolean;
  confidence: number;
  severity: SeverityResult;
  ensemble: EnsembleResult;
  explainability: ExplainabilityResult;
  symptoms: string[];
  recommendations: TreatmentRecommendation;
  createdAt: string;
  notes?: string;
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  confidence: number;
}

export interface PestDetectionResult {
  id: string;
  imageUri: string;
  totalPests: number;
  species: string;
  threatLevel: 'low' | 'moderate' | 'high';
  boundingBoxes: BoundingBox[];
  organicControl: string[];
  chemicalControl: string[];
  biologicalControl: string[];
  detectedAt: string;
}

export interface YieldPredictionInput {
  crop: CropType;
  district: string;
  areaAcres: number;
  soilType: 'black' | 'alluvial' | 'red' | 'sandy' | 'clay';
  season: 'kharif' | 'rabi' | 'zaid';
  irrigation: 'drip' | 'sprinkler' | 'canal' | 'rainfed';
}

export interface YieldPredictionResult {
  estimatedYieldPerAcre: number;
  totalEstimatedYield: number;
  rangeMin: number;
  rangeMax: number;
  unit: string;
  riskFactors: string[];
  projectedRevenueInr: number;
  historicalAveragePerAcre: number;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  audioUri?: string;
  timestamp: string;
  status?: 'sending' | 'sent' | 'error';
}

export interface KnowledgeArticle {
  id: string;
  category: 'diseases' | 'pests' | 'soil' | 'fertilizers' | 'weather' | 'schemes' | string;
  title: string;
  summary: string;
  content: string;
  readTimeMinutes: number;
  cropTarget?: CropType | string;
  imageUrl?: string;
  isBookmarked: boolean;
  publishedAt: string;
  sourceName?: string;
  sourceUrl?: string;
  sourceAuthority?: string;
}

export interface FarmReport {
  id: string;
  diagnosisId: string;
  farmerName: string;
  crop: CropType;
  disease: string;
  confidence: number;
  severity: SeverityClass;
  pdfUri?: string;
  generatedDate: string;
}

export interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
  rainfallMm: number;
  condition: string;
  icon: string;
  updatedAt: string;
}
