# Agrivision AI+ — Database Schema

## Entity Relationship Diagram

### users
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() |
| full_name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NULLABLE |
| phone | VARCHAR(20) | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| preferred_language | VARCHAR(5) | DEFAULT 'en' |
| preferred_theme | VARCHAR(10) | DEFAULT 'light' |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### farmer_profiles
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id, UNIQUE |
| village | VARCHAR(255) | |
| district | VARCHAR(255) | |
| state | VARCHAR(255) | DEFAULT 'Maharashtra' |
| farm_area_hectares | FLOAT | |
| primary_crops | JSONB | |
| soil_type | VARCHAR(100) | |
| irrigation_type | VARCHAR(100) | |
| profile_photo_url | VARCHAR(500) | |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### diagnoses
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id, NOT NULL |
| image_url | VARCHAR(500) | NOT NULL |
| crop_type | VARCHAR(100) | NOT NULL |
| predicted_disease | VARCHAR(255) | |
| confidence | FLOAT | |
| severity | VARCHAR(50) | |
| severity_percentage | FLOAT | |
| ensemble_results | JSONB | |
| pest_detections | JSONB | |
| explainability_url | VARCHAR(500) | |
| recommendations | JSONB | |
| model_version | VARCHAR(50) | |
| inference_time_ms | FLOAT | |
| language | VARCHAR(5) | DEFAULT 'en' |
| status | VARCHAR(20) | DEFAULT 'pending' |
| created_at | TIMESTAMP | DEFAULT NOW() |

Indexes: user_id, created_at DESC, crop_type

### yield_predictions
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| crop | VARCHAR(100) | NOT NULL |
| district | VARCHAR(255) | NOT NULL |
| season | VARCHAR(50) | NOT NULL |
| area_hectares | FLOAT | NOT NULL |
| soil_type | VARCHAR(100) | |
| irrigation | BOOLEAN | DEFAULT FALSE |
| predicted_yield_kg_per_hectare | FLOAT | |
| predicted_total_production_kg | FLOAT | |
| prediction_range_low | FLOAT | |
| prediction_range_high | FLOAT | |
| risk_factors | JSONB | |
| influencing_factors | JSONB | |
| created_at | TIMESTAMP | DEFAULT NOW() |

### conversations
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| title | VARCHAR(255) | |
| language | VARCHAR(5) | DEFAULT 'en' |
| created_at | TIMESTAMP | DEFAULT NOW() |

### messages
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| conversation_id | UUID | FK → conversations.id |
| role | VARCHAR(20) | NOT NULL (user/assistant) |
| content | TEXT | NOT NULL |
| audio_url | VARCHAR(500) | NULLABLE |
| created_at | TIMESTAMP | DEFAULT NOW() |

### knowledge_articles
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| category | VARCHAR(100) | NOT NULL |
| title_en | VARCHAR(500) | NOT NULL |
| title_mr | VARCHAR(500) | |
| title_hi | VARCHAR(500) | |
| content_en | TEXT | NOT NULL |
| content_mr | TEXT | |
| content_hi | TEXT | |
| tags | JSONB | |
| is_published | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | DEFAULT NOW() |

### reports
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| diagnosis_id | UUID | FK → diagnoses.id |
| report_url | VARCHAR(500) | NOT NULL |
| language | VARCHAR(5) | DEFAULT 'en' |
| generated_at | TIMESTAMP | DEFAULT NOW() |

### notifications
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| title | VARCHAR(255) | NOT NULL |
| message | TEXT | |
| type | VARCHAR(50) | |
| is_read | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |

### model_versions
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| model_name | VARCHAR(100) | NOT NULL |
| version | VARCHAR(50) | NOT NULL |
| accuracy | FLOAT | |
| f1_score | FLOAT | |
| weights_path | VARCHAR(500) | |
| is_active | BOOLEAN | DEFAULT TRUE |
| trained_at | TIMESTAMP | |
| created_at | TIMESTAMP | DEFAULT NOW() |

