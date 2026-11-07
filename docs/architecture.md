# Agrivision AI+ — Architecture Documentation

## System Overview

```
┌──────────────────────────────────────────────────────┐
│                    Mobile App                         │
│            React Native / Expo (TypeScript)           │
│                                                       │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ i18next  │ │ Zustand  │ │ TanStack │ │  Expo    │ │
│  │ (en/mr/  │ │ (State)  │ │  Query   │ │  Camera  │ │
│  │  hi)     │ │          │ │          │ │  Picker  │ │
│  └─────────┘ └──────────┘ └──────────┘ └──────────┘ │
└───────────────────────┬──────────────────────────────┘
                        │ REST API (HTTPS)
                        ▼
┌──────────────────────────────────────────────────────┐
│                   FastAPI Backend                     │
│                                                       │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │  Auth   │ │ API      │ │ Services │ │   ML     │ │
│  │  JWT    │ │ Routes   │ │          │ │ Inference│ │
│  └─────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                       │
│  ML Models:                                           │
│  ├── EfficientNetB3 (Disease Detection)               │
│  ├── VGG16, VGG19, InceptionV3, ResNet101V2 (Ensemble)│
│  ├── YOLOv8 (Pest Detection)                          │
│  ├── U-Net (Severity Segmentation)                    │
│  ├── Grad-CAM (Explainability)                        │
│  └── XGBoost / Random Forest (Yield Prediction)       │
└───────────────────────┬──────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
┌──────────────┐ ┌───────────┐ ┌──────────────┐
│  PostgreSQL  │ │ Supabase  │ │  External    │
│  (SQLAlchemy)│ │ Storage   │ │  APIs        │
│              │ │ (Images/  │ │ - Weather    │
│  Users       │ │  Reports) │ │ - BHASHINI   │
│  Diagnoses   │ │           │ │ - LLM        │
│  Predictions │ │           │ │              │
│  Knowledge   │ │           │ │              │
└──────────────┘ └───────────┘ └──────────────┘
```

## Key Design Decisions

### 1. Monorepo Structure
- `mobile/` — React Native/Expo app
- `backend/` — FastAPI Python backend
- `ml/` — ML training and evaluation (not deployed with backend)

### 2. AI/ML Architecture
- All inference runs on the backend server (not on-device)
- Models are loaded at startup with graceful degradation
- Ensemble uses weighted voting with configurable weights
- Model weights stored externally (not in Git)

### 3. Multilingual Strategy
- i18next + react-i18next for UI translations (mandatory)
- BHASHINI / IndicTrans2 for dynamic content translation
- Separate translation files per screen namespace
- Agricultural terminology dictionaries for accuracy

### 4. Authentication
- JWT-based authentication
- Phone number as primary identifier (Indian market)
- Password hashed with bcrypt
- Tokens expire after configurable period

### 5. Data Storage
- PostgreSQL for structured data via SQLAlchemy
- Supabase Storage for images and report files
- AsyncStorage for local preferences (language, theme)
- No large files in database rows

