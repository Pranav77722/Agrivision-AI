# Agrivision AI+ — Model Documentation

## Model Inventory

### 1. EfficientNetB3 — Primary Disease Classifier

| Property | Value |
|----------|-------|
| Architecture | EfficientNetB3 |
| Framework | TensorFlow / Keras |
| Input Size | 300 × 300 × 3 |
| Output | 38 classes (PlantVillage) |
| Transfer Learning | ImageNet pretrained backbone |
| Custom Head | GlobalAveragePooling2D → Dense(256, ReLU) → Dropout(0.3) → Dense(38, Softmax) |
| Training Dataset | PlantVillage (54,305 images) |
| Validation Dataset | PlantDoc (2,598 images) |
| Weights File | `efficientnetb3_disease.h5` |

### 2. Ensemble Models

#### VGG16
| Property | Value |
|----------|-------|
| Input Size | 224 × 224 × 3 |
| Preprocessing | VGG-specific (BGR, mean subtraction) |
| Ensemble Weight | 0.20 |

#### VGG19
| Property | Value |
|----------|-------|
| Input Size | 224 × 224 × 3 |
| Preprocessing | VGG-specific (BGR, mean subtraction) |
| Ensemble Weight | 0.20 |

#### InceptionV3
| Property | Value |
|----------|-------|
| Input Size | 299 × 299 × 3 |
| Preprocessing | Inception-specific (scale to [-1, 1]) |
| Ensemble Weight | 0.30 |

#### ResNet101V2
| Property | Value |
|----------|-------|
| Input Size | 224 × 224 × 3 |
| Preprocessing | ResNet V2 (scale to [-1, 1]) |
| Ensemble Weight | 0.30 |

### 3. YOLOv8 — Pest Detection

| Property | Value |
|----------|-------|
| Architecture | YOLOv8m / YOLO11 |
| Framework | PyTorch / Ultralytics |
| Input Size | 640 × 640 |
| Task | Object Detection |
| Training Dataset | IP102 (75,222 images, 102 pest classes) |
| Confidence Threshold | 0.25 |
| IoU Threshold | 0.45 |
| Weights File | `yolov8_pest.pt` |

### 4. U-Net — Disease Severity Segmentation

| Property | Value |
|----------|-------|
| Architecture | U-Net (encoder-decoder) |
| Framework | TensorFlow / Keras |
| Input Size | 256 × 256 × 3 |
| Output | 256 × 256 × 1 (binary mask) |
| Classes | Healthy tissue / Diseased tissue |
| Loss | Dice Loss + Binary Cross-Entropy |
| Weights File | `unet_severity.h5` |

### 5. Grad-CAM — Explainability

| Property | Value |
|----------|-------|
| Method | Gradient-weighted Class Activation Mapping |
| Compatible Models | EfficientNetB3, VGG16, VGG19, InceptionV3, ResNet101V2 |
| Output | Heatmap overlay showing regions influencing prediction |
| Implementation | Custom (not a separate model) |

### 6. XGBoost — Yield Prediction

| Property | Value |
|----------|-------|
| Architecture | XGBRegressor |
| Framework | XGBoost + Scikit-learn |
| Features | crop, district, season, area, soil_type, irrigation, rainfall, temperature |
| Output | Predicted yield (kg/hectare) |
| Fallback | Random Forest Regressor |
| Training Data | Indian district-level agricultural statistics |
| Weights File | `xgboost_yield.joblib` |

## Required Datasets

| Dataset | Purpose | Source | License |
|---------|---------|--------|---------|
| PlantVillage | Disease classification training | Kaggle / Penn State | Open (CC BY-SA) |
| PlantDoc | Disease classification validation | IIT Bombay | Research use |
| IP102 | Pest detection | Paper: Wu et al. 2019 | Research use |
| Indian Agri Stats | Yield prediction | data.gov.in / ICAR | Open Government |

## Model Weight Locations

All model weights should be placed in: `ml/models/weights/`

```
ml/models/weights/
├── efficientnetb3_disease.h5
├── vgg16_disease.h5
├── vgg19_disease.h5
├── inceptionv3_disease.h5
├── resnet101v2_disease.h5
├── yolov8_pest.pt
├── unet_severity.h5
└── xgboost_yield.joblib
```

> ⚠️ These files are NOT included in the Git repository due to their size.
> They must be downloaded or trained separately using the scripts in `ml/training/`.

