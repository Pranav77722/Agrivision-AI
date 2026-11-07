# Agrivision AI+ — Deployment Guide

## Development Setup

### Prerequisites
- Node.js 18+ (tested with v24.16.0)
- Python 3.10+ (tested with 3.14.5)
- PostgreSQL 14+
- Git
- Docker (optional)
- Android Studio / Android SDK (for mobile build)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Agrivision-AI-Plus
cp .env.example .env
# Edit .env with your configuration
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python -m app.seeds.seed_all  # Seed database
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Mobile App Setup

```bash
cd mobile
npm install
npx expo start
# Press 'a' for Android emulator
```

### 4. ML Models Setup

```bash
# Download or train models
cd ml
python training/train_disease_classifier.py  # Requires PlantVillage dataset
python training/train_yield_model.py         # Requires agricultural data

# Or download pre-trained weights
# Place weights in ml/models/weights/
```

## Production Deployment

### Backend (Docker)

```bash
cd backend
docker build -t agrivision-backend .
docker run -d \
  --name agrivision-api \
  -p 8000:8000 \
  --env-file ../.env \
  agrivision-backend
```

### Database (Supabase)

1. Create a Supabase project
2. Copy the database URL to `.env`
3. Run migrations: `alembic upgrade head`
4. Create storage buckets: `agrivision-images`, `agrivision-reports`

### Mobile (EAS Build)

```bash
cd mobile
npx eas-cli login
npx eas build --platform android --profile production
```

### ML Models Deployment

Models are loaded by the backend at startup. Ensure:
1. All weight files are in the configured `MODEL_WEIGHTS_DIR`
2. Sufficient RAM for all models (~8GB recommended)
3. GPU available for faster inference (optional)

## Environment Variables Checklist

- [ ] DATABASE_URL
- [ ] SECRET_KEY (use a strong random string)
- [ ] SUPABASE_URL
- [ ] SUPABASE_ANON_KEY
- [ ] SUPABASE_SERVICE_KEY
- [ ] WEATHER_API_KEY
- [ ] BHASHINI_API_KEY
- [ ] LLM_PROVIDER + API_KEY
- [ ] MODEL_WEIGHTS_DIR

## Monitoring

- Backend health: `GET /api/v1/health`
- Model status: `GET /api/v1/health/models`
- API docs: `GET /docs` (Swagger UI)

