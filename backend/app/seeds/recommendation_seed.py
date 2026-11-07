"""
Recommendation Seed Data for Agrivision AI+.
Provides treatment protocols (chemical, organic, cultural) for crop diseases and pests.
"""

from typing import List, Dict, Any

RECOMMENDATIONS_SEED: List[Dict[str, Any]] = [
    {
        "disease_key": "Tomato Early Blight",
        "chemical": {
            "en": [
                "Mancozeb 75% WP @ 2.5 g/liter of water at first symptom appearance.",
                "Azoxystrobin 23% SC @ 1 ml/liter of water as systemic curative spray.",
                "Chlorothalonil 75% WP @ 2 g/liter at 10-14 day intervals."
            ],
            "mr": [
                "मॅन्कोझेब ७५% WP २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.",
                "अझोक्सिस्ट्रोबिन २३% SC १ मिली प्रति लिटर पाण्यात मिसळून फवारावे.",
                "क्लोरोथॅलोनिल ७५% WP २ ग्रॅम प्रति लिटर १०-१४ दिवसांच्या अंतराने फवारावे."
            ],
            "hi": [
                "मैनकोजेब 75% WP को 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें।",
                "एजॉक्सीस्ट्रोबिन 23% SC 1 मिली प्रति लीटर स्प्रे करें।",
                "क्लोरोथैलोनिल 75% WP को 2 ग्राम प्रति लीटर 10-14 दिनों के अंतराल पर छिड़कें।"
            ]
        },
        "organic": {
            "en": [
                "Foliar spray of Trichoderma harzianum @ 5 g/liter.",
                "Apply 5% Neem Seed Kernel Extract (NSKE) every 7-10 days.",
                "Spray 1% Bordeaux mixture as protective foliar cover."
            ],
            "mr": [
                "ट्रायकोडर्मा हार्झियानम ५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.",
                "५% निंबोळी अर्क (NSKE) दर ७-१० दिवसांनी फवारावे.",
                "१% बोर्डो मिश्रण प्रतिबंधात्मक म्हणून फवारावे."
            ],
            "hi": [
                "ट्राइकोडर्मा हार्ज़ियानम 5 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें।",
                "5% नीम के बीज का अर्क (NSKE) हर 7-10 दिनों में छिड़कें।"
            ]
        },
        "cultural": {
            "en": [
                "Remove and burn infected lower leaves immediately.",
                "Adopt drip irrigation to avoid wet foliage.",
                "Maintain 3-year crop rotation with non-solanaceous crops."
            ],
            "mr": [
                "रोगट झालेली खालची पाने तोडून नष्ट करा.",
                "ठिबक सिंचनाचा वापर करून पाने ओली राहू देऊ नका.",
                "टोमॅटो पिकाची ३ वर्षे फेरपालट करा."
            ],
            "hi": [
                "संक्रमित निचली पत्तियों को तुरंत हटाकर नष्ट कर दें।",
                "ड्रिप सिंचाई अपनाएं ताकि पत्तियां गीली न रहें।"
            ]
        }
    },
    {
        "disease_key": "Rice Blast",
        "chemical": {
            "en": [
                "Tricyclazole 75% WP @ 0.6 g/liter at boot leaf and heading stage.",
                "Isoprothiolane 40% EC @ 1.5 ml/liter.",
                "Kasugamycin 3% SL @ 2-2.5 ml/liter."
            ],
            "mr": [
                "ट्रायसायक्लॅझोल ७५% WP ०.६ ग्रॅम प्रति लिटर पोटरी अवस्थेत फवारावे.",
                "आयसोप्रॉथिओलेन ४०% EC १.५ मिली प्रति लिटर फवारावे.",
                "कासुगामायसिन ३% SL २ ते २.५ मिली प्रति लिटर फवारावे."
            ],
            "hi": [
                "ट्राइसाइक्लाजोल 75% WP 0.6 ग्राम प्रति लीटर की दर से बालियां निकलते समय छिड़कें।",
                "कासुगामाइसिन 3% SL 2 से 2.5 मिली प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic": {
            "en": [
                "Seed treatment with Pseudomonas fluorescens @ 10 g/kg seed.",
                "Foliar spray with 10% cow urine + Hing (Asafoetida) solution."
            ],
            "mr": [
                "बियाण्यावर स्यूडोमोनास फ्लूरोसेन्स १० ग्रॅम प्रति किलो चोळावे.",
                "१०% गोमूत्र आणि हिंग द्रावणाची फवारणी करावी."
            ],
            "hi": [
                "स्यूडोमोनास फ्लोरोसेंट 10 ग्राम/किग्रा बीज से बीजोपचार करें।",
                "10% गोमूत्र + हींग के घोल का छिड़काव करें।"
            ]
        },
        "cultural": {
            "en": [
                "Avoid excess nitrogenous fertilizer (split urea into 3 applications).",
                "Ensure proper field drainage during cloudy humid periods."
            ],
            "mr": [
                "युरिया खताचा अतिरेक टाळा; हप्त्याहप्त्याने युरिया द्या.",
                "खाचरातील पाण्याचा निचरा व्यवस्थित ठेवा."
            ],
            "hi": [
                "अत्यधिक यूरिया के प्रयोग से बचें; संतुलित मात्रा दें।"
            ]
        }
    },
    {
        "disease_key": "Wheat Rust",
        "chemical": {
            "en": [
                "Propiconazole 25% EC (Tilt) @ 1 ml/liter of water at first symptom.",
                "Tebuconazole 250 EC @ 1 ml/liter."
            ],
            "mr": [
                "प्रोपिकोनाझोल २५% EC (टिल्ट) १ मिली प्रति लिटर पाण्यात मिसळून फवारावे.",
                "टेब्युकोनाझोल २५० EC १ मिली प्रति लिटर फवारावे."
            ],
            "hi": [
                "प्रोपिकोनाजोल 25% EC (टिल्ट) 1 मिली प्रति लीटर लक्षण दिखते ही छिड़कें।",
                "टेबुकोनाजोल 250 EC 1 मिली प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic": {
            "en": [
                "Sour buttermilk spray (diluted 1:10 with water).",
                "Bacillus subtilis foliar application @ 5 g/liter."
            ],
            "mr": [
                "आंबट ताक १:१० प्रमाणात पाण्यात मिसळून फवारावे.",
                "बॅसिलस सबटिलिस ५ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "खट्टी छाछ 1:10 के अनुपात में पानी में मिलाकर स्प्रे करें।"
            ]
        },
        "cultural": {
            "en": [
                "Sow rust-resistant varieties like HD-2967, PBW-550.",
                "Timely sowing before mid-November to avoid late infection."
            ],
            "mr": [
                "तांबेरा प्रतिकारक जातींची निवड करा (HD-2967).",
                "वेळेवर पेरणी करा."
            ],
            "hi": [
                "रोग प्रतिरोधी किस्मों की समय पर बुवाई करें।"
            ]
        }
    },
    {
        "disease_key": "Cotton Bacterial Blight",
        "chemical": {
            "en": [
                "Copper Oxychloride 50% WP @ 2.5 g + Streptocycline @ 0.1 g/liter of water.",
                "Kasugamycin 5% + Copper Oxychloride 45% WP @ 1.5 g/liter."
            ],
            "mr": [
                "कॉपर ऑक्सिक्लोराईड ५०% WP २.५ ग्रॅम + स्ट्रेप्टोसायक्लिन ०.१ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
                "कासुगामायसिन ५% + कॉपर ऑक्सिक्लोराईड १.५ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "कॉपर ऑक्सीक्लोराइड 50% WP 2.5 ग्राम + स्ट्रेप्टोसाइक्लिन 0.1 ग्राम प्रति लीटर छिड़कें।"
            ]
        },
        "organic": {
            "en": [
                "Spray 5% Dashparni ark at 10-day intervals.",
                "Pseudomonas fluorescens seed treatment @ 10 g/kg."
            ],
            "mr": [
                "५% दशपर्णी अर्क १० दिवसांच्या अंतराने फवारावे.",
                "स्यूडोमोनास बीजप्रक्रिया करा."
            ],
            "hi": [
                "5% दशपर्णी अर्क का नियमित छिड़काव करें।"
            ]
        },
        "cultural": {
            "en": [
                "Acid delinting of cotton seeds before planting.",
                "Burn crop residues after harvest to destroy bacterial inoculum."
            ],
            "mr": [
                "पेरणीपूर्वी बियाण्यांवर ऍसिड डीलिंटिंग करा.",
                "हंगाम संपल्यावर पिकाचे अवशेष नष्ट करा."
            ],
            "hi": [
                "बुवाई से पहले कपास के बीजों का एसिड डिलिंटिंग करें।"
            ]
        }
    }
]
