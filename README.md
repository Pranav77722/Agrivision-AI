# 🌾 Agrivision AI+

**AI-Powered Smart Agriculture Platform for Indian Farmers**

Agrivision AI+ is an intelligent agriculture platform that uses artificial intelligence, machine learning, computer vision, and multilingual technology to help farmers make better farming decisions.

## 🚀 Features

- **Crop Disease Detection** — EfficientNetB3-powered disease classification
- **Ensemble AI Classification** — VGG16, VGG19, InceptionV3, ResNet101V2 ensemble
- **Pest Detection** — YOLOv8/YOLO11 real-time pest detection
- **Disease Severity** — U-Net/DeepLabV3+ segmentation-based severity estimation
- **Explainable AI** — Grad-CAM visualization of model decisions
- **Yield Prediction** — XGBoost/Random Forest crop yield forecasting
- **Smart Recommendations** — AI-driven agricultural advice
- **AI Assistant** — Multilingual conversational farming assistant
- **Multilingual** — English, Marathi (मराठी), Hindi (हिंदी) with BHASHINI/IndicTrans2
- **Voice Interaction** — Speech-to-text and text-to-speech in Indian languages
- **Reports** — Downloadable PDF reports with Devanagari support

## 🏗️ Architecture

```
Agrivision-AI-Plus/
├── mobile/          # React Native / Expo app (TypeScript)
├── backend/         # FastAPI Python backend
├── ml/              # ML training, evaluation, datasets
├── docs/            # Documentation
└── scripts/         # Utility scripts
```

## 📱 Mobile App (React Native + Expo)

```bash
cd mobile
npm install
npx expo start
```

## 🖥️ Backend (FastAPI + Python)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧠 ML Models

| Feature | Model | Framework |
|---------|-------|-----------|
| Disease Detection | EfficientNetB3 | TensorFlow/Keras |
| Ensemble Classification | VGG16, VGG19, InceptionV3, ResNet101V2 | TensorFlow/Keras |
| Pest Detection | YOLOv8 / YOLO11 | PyTorch/Ultralytics |
| Severity Estimation | U-Net / DeepLabV3+ | TensorFlow/Keras |
| Explainability | Grad-CAM | TensorFlow |
| Yield Prediction | XGBoost / Random Forest | Scikit-learn |

## 🌐 Supported Languages

- English (en)
- मराठी - Marathi (mr)
- हिंदी - Hindi (hi)

## 📋 Requirements

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Docker (optional)

## 📄 License

Proprietary — Agrivision AI+
