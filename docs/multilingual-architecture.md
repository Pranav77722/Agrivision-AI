# Agrivision AI+ — Multilingual Architecture

## Overview

Agrivision AI+ supports three languages at launch:
- **English (en)** — Default
- **Marathi (mr)** — मराठी
- **Hindi (hi)** — हिंदी

The architecture is designed to easily add: Gujarati, Kannada, Telugu, Tamil, Bengali, Punjabi.

## Architecture Layers

### Layer 1: Static UI Translations (i18next)
- Library: `i18next` + `react-i18next`
- All UI text uses translation keys via `t()` function
- 15 namespace files per language
- Bundled locally for offline access
- Language detection via `expo-localization`
- Persistence via `AsyncStorage` + backend sync

### Layer 2: Dynamic Content Translation (BHASHINI/IndicTrans2)
- Agricultural content translated via BHASHINI APIs
- Fallback to AI4Bharat IndicTrans2
- Cached translations to reduce API calls
- Provider abstraction for easy switching

### Layer 3: Agricultural Terminology Dictionary
- Curated crop name mappings (en → mr, hi)
- Disease name translations (verified by domain experts)
- Pest terminology
- Treatment/chemical names (NOT auto-translated for safety)

### Layer 4: Voice (Speech Recognition + TTS)
- BHASHINI ASR for Marathi/Hindi/English
- AI4Bharat IndicConformer as fallback ASR
- TTS for spoken AI responses
- Support for code-mixed Marathi-English, Hindi-English

### Layer 5: AI Assistant Language
- LLM generates responses in user's selected language
- System prompt instructs language + agricultural context
- Translation layer ensures consistency

## Translation File Structure

```
mobile/src/i18n/
├── index.ts           # i18next initialization
├── config.ts          # Supported languages, namespaces
├── locales/
│   ├── en/            # English translations
│   │   ├── common.json
│   │   ├── onboarding.json
│   │   ├── dashboard.json
│   │   ├── diagnosis.json
│   │   ├── ensemble.json
│   │   ├── pest.json
│   │   ├── severity.json
│   │   ├── explainability.json
│   │   ├── yield.json
│   │   ├── recommendations.json
│   │   ├── knowledge.json
│   │   ├── assistant.json
│   │   ├── reports.json
│   │   ├── archive.json
│   │   └── profile.json
│   ├── mr/            # Marathi translations (same files)
│   └── hi/            # Hindi translations (same files)
```

## Agricultural Terminology Mapping

| Internal ID | English | मराठी (Marathi) | हिंदी (Hindi) |
|-------------|---------|-----------------|---------------|
| TOMATO_EARLY_BLIGHT | Tomato Early Blight | टोमॅटोवरील अर्ली ब्लाइट | टमाटर का अर्ली ब्लाइट |
| TOMATO_LATE_BLIGHT | Tomato Late Blight | टोमॅटोवरील उशीरा करपा | टमाटर का लेट ब्लाइट |
| RICE_BLAST | Rice Blast | भाताचा करपा | धान का ब्लास्ट |
| WHEAT_RUST | Wheat Rust | गव्हावरील तांबेरा | गेहूं का रस्ट |
| COTTON_BLIGHT | Cotton Bacterial Blight | कापसावरील जिवाणूजन्य करपा | कपास का जीवाणु झुलसा |

## Language Switching Flow

```
User selects language
  → Zustand store updates currentLanguage
  → AsyncStorage persists preference
  → i18next.changeLanguage() called
  → All components using t() re-render automatically
  → API calls include Accept-Language header
  → Backend updates user.preferred_language
  → Future API responses use user's language
  → AI assistant uses selected language
```

## Safety Rules

1. **Never auto-translate pesticide dosages** — Use verified translations only
2. **Never auto-translate chemical names** — Keep scientific names alongside translations
3. **Mark machine-translated content** — Distinguish from expert-reviewed translations
4. **Test Devanagari rendering** — Verify fonts support conjunct characters
5. **Handle RTL-awareness** — Not needed for current languages, but architecture supports it

