import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# Comprehensive agricultural disease recommendation knowledge base
DISEASE_RECOMMENDATIONS: Dict[str, Dict[str, Any]] = {
    # Tomato Diseases
    "Tomato Early Blight": {
        "crop": "Tomato",
        "disease_name": "Tomato Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": {
            "en": "Dark brown to black spots with concentric rings ('bullseye') on older lower leaves.",
            "mr": "जुन्या खालच्या पानांवर काळे-तपकिरी रंगाचे चक्राकार डाग पडतात.",
            "hi": "पुरानी निचली पत्तियों पर संकेंद्रित छल्लों वाले गहरे भूरे से काले धब्बे।"
        },
        "chemical_control": {
            "en": [
                "Spray Mancozeb 75% WP @ 2.5 g/liter of water.",
                "Spray Azoxystrobin 23% SC @ 1 ml/liter of water at first symptom appearance.",
                "Chlorothalonil 75% WP @ 2 g/liter at 10-14 day intervals."
            ],
            "mr": [
                "मॅन्कोझेब ७५% WP २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.",
                "अझोक्सिस्ट्रोबिन २३% SC १ मिली प्रति लिटर पाण्यात मिसळून फवारावे.",
                "क्लोरोथॅलोनिल ७५% WP २ ग्रॅम प्रति लिटर १०-१४ दिवसांच्या अंतराने फवारावे."
            ],
            "hi": [
                "मैनकोजेब 75% WP को 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें।",
                "एजॉक्सीस्ट्रोबिन 23% SC को 1 मिली प्रति लीटर पानी में मिलाकर स्प्रे करें।",
                "क्लोरोथैलोनिल 75% WP को 2 ग्राम प्रति लीटर 10-14 दिनों के अंतराल पर छिड़कें।"
            ]
        },
        "organic_control": {
            "en": [
                "Foliar spray of Trichoderma harzianum @ 5 g/liter of water.",
                "Apply 5% Neem Seed Kernel Extract (NSKE) every 7-10 days.",
                "Apply copper hydroxide or Bordeaux mixture (1%) as protective spray."
            ],
            "mr": [
                "ट्रायकोडर्मा हार्झियानम ५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.",
                "५% निंबोळी अर्क (NSKE) दर ७-१० दिवसांनी फवारावे.",
                "१% बोर्डो मिश्रण किंवा कॉपर हायड्रॉक्साइड प्रतिबंधात्मक म्हणून फवारावे."
            ],
            "hi": [
                "ट्राइकोडर्मा हार्ज़ियानम 5 ग्राम प्रति लीटर पानी में मिलाकर पर्णीय छिड़काव करें।",
                "5% नीम के बीज का अर्क (NSKE) हर 7-10 दिनों में छिड़कें।",
                "1% बोर्डो मिश्रण या कॉपर हाइड्रॉक्साइड का छिड़काव करें।"
            ]
        },
        "cultural_practices": {
            "en": [
                "Remove and burn infected lower leaves immediately.",
                "Avoid overhead sprinkler irrigation; prefer drip irrigation.",
                "Practice 2-3 years crop rotation with non-solanaceous crops.",
                "Mulch soil around plants with straw to prevent fungal spore splashing."
            ],
            "mr": [
                "रोगट झालेली खालची पाने तोडून नष्ट करा.",
                "तुषार सिंचन टाळावे आणि ठिबक सिंचनाचा वापर करावा.",
                "टोमॅटो पिकाची २-३ वर्षे फेरपालट करा.",
                "मातीतून बुरशीचे बीजाणू उडू नयेत म्हणून आच्छादन (मल्चिंग) वापरा."
            ],
            "hi": [
                "संक्रमित निचली पत्तियों को तुरंत हटाकर नष्ट कर दें।",
                "फव्वारा सिंचाई से बचें और ड्रिप सिंचाई अपनाएं।",
                "2-3 साल तक गैर-सोलेनेसी फसलों के साथ फसल चक्र अपनाएं।",
                "फंगल बीजाणुओं को उछलने से रोकने के लिए पुआल की मल्चिंग करें।"
            ]
        }
    },

    "Tomato Late Blight": {
        "crop": "Tomato",
        "disease_name": "Tomato Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": {
            "en": "Water-soaked irregular spots on leaves that turn brown-black with white fuzzy growth underneath during humid conditions.",
            "mr": "पानांवर पाण्यासारखे तपकिरी-काळे डाग पडतात आणि दमट हवामानात पानाच्या मागे पांढरी बुरशी दिसते.",
            "hi": "पत्तियों पर पानी से भीगे अनियमित धब्बे जो नम मौसम में नीचे सफेद फफूंद के साथ भूरे-काले हो जाते हैं।"
        },
        "chemical_control": {
            "en": [
                "Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2.5 g/liter of water.",
                "Dimethomorph 50% WP @ 1 g/liter + Mancozeb 2 g/liter.",
                "Cymoxanil 8% + Mancozeb 64% WP @ 2.5 g/liter."
            ],
            "mr": [
                "मेटॅलॅक्सिल ८% + मॅन्कोझेब ६४% WP (रिडोमिल) २.५ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
                "डायमेथोमॉर्फ ५०% WP १ ग्रॅम + मॅन्कोझेब २ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
                "सायमॉक्सॅनिल ८% + मॅन्कोझेब ६४% WP २.५ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "मेटालैक्सिल 8% + मैनकोजेब 64% WP (रिडोमिल) 2.5 ग्राम प्रति लीटर छिड़कें।",
                "डाइमेथोमॉर्फ 50% WP 1 ग्राम + मैनकोजेब 2 ग्राम प्रति लीटर स्प्रे करें।",
                "साइमोक्सानिल 8% + मैनकोजेब 64% WP 2.5 ग्राम प्रति लीटर छिड़कें।"
            ]
        },
        "organic_control": {
            "en": [
                "Bordeaux mixture (1%) preventive spray before rains.",
                "Pseudomonas fluorescens @ 5 g/liter foliar spray.",
                "Garlic + Chili extract spray as organic fungicidal barrier."
            ],
            "mr": [
                "पावसाळ्यापूर्वी १% बोर्डो मिश्रणाची फवारणी करा.",
                "स्यूडोमोनास फ्लूरोसेन्स ५ ग्रॅम प्रति लिटर फवारावे.",
                "लसूण आणि मिरची अर्क प्रतिबंधक म्हणून वापरा."
            ],
            "hi": [
                "बारिश से पहले 1% बोर्डो मिश्रण का छिड़काव करें।",
                "स्यूडोमोनास फ्लोरोसेंट 5 ग्राम प्रति लीटर स्प्रे करें।",
                "लहसुन-मिर्च अर्क का जैविक कवकनाशी स्प्रे करें।"
            ]
        },
        "cultural_practices": {
            "en": [
                "Ensure proper plant spacing for air circulation.",
                "Destroy all volunteer tomato and potato plants nearby.",
                "Never leave wet foliage overnight."
            ],
            "mr": [
                "हवा खेळती राहण्यासाठी दोन झाडांमध्ये योग्य अंतर ठेवा.",
                "शेतातील जुनी टोमॅटो किंवा बटाटा झाडे नष्ट करा.",
                "संध्याकाळी उशिरा पाणी देणे टाळा."
            ],
            "hi": [
                "हवा के संचार के लिए पौधों के बीच उचित दूरी रखें।",
                "आसपास के पुराने टमाटर व आलू के पौधे नष्ट करें।",
                "शाम के समय पत्तियों को गीला रखने से बचें।"
            ]
        }
    },

    "Rice Blast": {
        "crop": "Rice",
        "disease_name": "Rice Blast",
        "pathogen": "Magnaporthe oryzae (Fungus)",
        "symptoms": {
            "en": "Spindle-shaped elliptical lesions with gray/whitish centers and dark reddish-brown borders on leaves and neck rot on panicles.",
            "mr": "पानांवर दोन्ही टोकांना टोकदार (चाकूच्या आकाराचे) मध्यभागी राखाडी आणि कडेला तपकिरी डाग पडतात, तसेच मानेवर करपा येतो.",
            "hi": "पत्तियों पर धुरी के आकार के धब्बे जिनका केंद्र धूसर और किनारे गहरे लाल-भूरे होते हैं।"
        },
        "chemical_control": {
            "en": [
                "Spray Tricyclazole 75% WP @ 0.6 g/liter at boot leaf and heading stage.",
                "Isoprothiolane 40% EC @ 1.5 ml/liter.",
                "Kasugamycin 3% SL @ 2-2.5 ml/liter."
            ],
            "mr": [
                "ट्रायसायक्लॅझोल ७५% WP ०.६ ग्रॅम प्रति लिटर पोटरी आणि लोंबी बाहेर पडताना फवारावे.",
                "आयसोप्रॉथिओलेन ४०% EC १.५ मिली प्रति लिटर फवारावे.",
                "कासुगामायसिन ३% SL २ ते २.५ मिली प्रति लिटर फवारावे."
            ],
            "hi": [
                "ट्राइसाइक्लाजोल 75% WP को 0.6 ग्राम प्रति लीटर की दर से बालियां निकलते समय छिड़कें।",
                "आइसोप्रोपियोलेन 40% EC 1.5 मिली प्रति लीटर स्प्रे करें।",
                "कासुगामाइसिन 3% SL 2 से 2.5 मिली प्रति लीटर छिड़कें।"
            ]
        },
        "organic_control": {
            "en": [
                "Seed treatment with Pseudomonas fluorescens @ 10 g/kg seed.",
                "Spray 10% cow urine + Asafoetida (Hing) solution.",
                "Apply silica fertilizer to strengthen plant cell walls."
            ],
            "mr": [
                "बियाण्यावर स्यूडोमोनास फ्लूरोसेन्स १० ग्रॅम प्रति किलो चोळावे.",
                "१०% गोमूत्र आणि हिंग द्रावणाची फवारणी करावी.",
                "सिलिका खताचा वापर करून पेशी मजबूत करा."
            ],
            "hi": [
                "स्यूडोमोनास फ्लोरोसेंट 10 ग्राम/किग्रा बीज से बीजोपचार करें।",
                "10% गोमूत्र + हींग के घोल का छिड़काव करें।",
                "सिलिका युक्त उर्वरकों का प्रयोग करें।"
            ]
        },
        "cultural_practices": {
            "en": [
                "Avoid excess nitrogenous fertilizer (split urea application).",
                "Maintain standing water in field during high humidity periods.",
                "Use blast-resistant varieties like IR64, Sahbhagi Dhan."
            ],
            "mr": [
                "युरिया खताचा अतिरेक टाळा; हप्त्याहप्त्याने युरिया द्या.",
                "दमट हवामानात खाचरात पाणी साठवून ठेवा.",
                "रोगप्रतिकारक जातींचा वापर करा."
            ],
            "hi": [
                "अत्यधिक यूरिया के प्रयोग से बचें; संतुलित मात्रा दें।",
                "खेत में उचित जल स्तर बनाए रखें।",
                "रोग प्रतिरोधी किस्मों की बुवाई करें।"
            ]
        }
    },

    "Wheat Rust": {
        "crop": "Wheat",
        "disease_name": "Wheat Rust (Stripe / Brown / Stem)",
        "pathogen": "Puccinia spp. (Fungus)",
        "symptoms": {
            "en": "Yellowish-orange or brownish pustules forming stripes or scattered spots on leaves, powdery spore release.",
            "mr": "गव्हाच्या पानांवर पिवळसर-केशरी किंवा तपकिरी रंगाचे लहान पुरळ (तांबेरा) पट्ट्यांच्या रूपात दिसतात.",
            "hi": "गेहूं की पत्तियों पर पीले-नारंगी या भूरे रंग के धब्बे/धारियां (गेरुआ/रतुआ) दिखाई देती हैं।"
        },
        "chemical_control": {
            "en": [
                "Spray Propiconazole 25% EC (Tilt) @ 1 ml/liter at first sign of pustules.",
                "Tebuconazole 250 EC @ 1 ml/liter.",
                "Mancozeb 75% WP @ 2 g/liter preventive spray."
            ],
            "mr": [
                "प्रोपिकोनाझोल २५% EC (टिल्ट) १ मिली प्रति लिटर पाण्यात मिसळून तातडीने फवारावे.",
                "टेब्युकोनाझोल २५० EC १ मिली प्रति लिटर फवारावे.",
                "मॅन्कोझेब ७५% WP २ ग्रॅम प्रति लिटर प्रतिबंधात्मक फवारावे."
            ],
            "hi": [
                "प्रोपिकोनाजोल 25% EC (टिल्ट) 1 मिली प्रति लीटर लक्षण दिखते ही छिड़कें।",
                "टेबुकोनाजोल 250 EC 1 मिली प्रति लीटर स्प्रे करें।",
                "मैनकोजेब 75% WP 2 ग्राम प्रति लीटर छिड़कें।"
            ]
        },
        "organic_control": {
            "en": [
                "Foliar spray of fermented butter milk (sour chaas) diluted 1:10 with water.",
                "Application of bio-agent Bacillus subtilis @ 5 g/liter."
            ],
            "mr": [
                "आंबट ताक १:१० प्रमाणात पाण्यात मिसळून फवारावे.",
                "बॅसिलस सबटिलिस ५ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "खट्टी छाछ 1:10 के अनुपात में पानी में मिलाकर स्प्रे करें।",
                "बैसिलस सबटिलिस 5 ग्राम प्रति लीटर छिड़कें।"
            ]
        },
        "cultural_practices": {
            "en": [
                "Sow timely before mid-November to escape late rust build-up.",
                "Plant rust-resistant cultivars (HD-2967, PBW-550, GW-322).",
                "Eradicate wild grasses and alternate hosts on field borders."
            ],
            "mr": [
                "वेळेवर पेरणी करा (नोव्हेंबर मध्यापूर्वी).",
                "तांबेरा प्रतिकारक जातींची निवड करा.",
                "बांधावरील तण व पर्यायी यजमान गवत काढून टाका."
            ],
            "hi": [
                "नवंबर के मध्य से पहले समय पर बुवाई करें।",
                "रोग प्रतिरोधी किस्मों का चयन करें।",
                "खेत की मेड़ों से खरपतवार साफ रखें।"
            ]
        }
    },

    "Cotton Bacterial Blight": {
        "crop": "Cotton",
        "disease_name": "Cotton Bacterial Blight (Blackarm / Angular Leaf Spot)",
        "pathogen": "Xanthomonas citri pv. malvacearum",
        "symptoms": {
            "en": "Angular water-soaked spots bounded by leaf veinlets, black lesions on stems (blackarm), and rotting bolls.",
            "mr": "पानांवर शिरांमुळे त्रिकोणी-चौकोनी काळे डाग, फांद्यांवर काळे चट्टे (काळी काठी रोग) आणि बोंड सडणे.",
            "hi": "पत्तियों की शिराओं के बीच कोणीय पानी से भीगे काले धब्बे और तने पर काले घाव।"
        },
        "chemical_control": {
            "en": [
                "Spray Copper Oxychloride 50% WP @ 2.5 g + Streptocycline @ 0.1 g/liter.",
                "Kasugamycin 5% + Copper Oxychloride 45% WP @ 1.5 g/liter."
            ],
            "mr": [
                "कॉपर ऑक्सिक्लोराईड ५०% WP २.५ ग्रॅम + स्ट्रेप्टोसायक्लिन ०.१ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
                "कासुगामायसिन ५% + कॉपर ऑक्सिक्लोराईड १.५ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "कॉपर ऑक्सीक्लोराइड 50% WP 2.5 ग्राम + स्ट्रेप्टोसाइक्लिन 0.1 ग्राम प्रति लीटर छिड़कें।",
                "कासुगामाइसिन + कॉपर ऑक्सीक्लोराइड 1.5 ग्राम प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic_control": {
            "en": [
                "Seed treatment with cow dung slurry + Pseudomonas fluorescens.",
                "Spray 5% Dashparni ark at 10-day intervals."
            ],
            "mr": [
                "स्यूडोमोनास आणि शेण स्लरीने बीजप्रक्रिया करा.",
                "५% दशपर्णी अर्क १० दिवसांच्या अंतराने फवारावे."
            ],
            "hi": [
                "स्यूडोमोनास फ्लोरोसेंट से बीज शोधन करें।",
                "5% दशपर्णी अर्क का नियमित छिड़काव करें।"
            ]
        },
        "cultural_practices": {
            "en": [
                "Acid delinting of cotton seeds before planting.",
                "Avoid sprinkler irrigation to prevent bacterial splash.",
                "Burn cotton crop residues after harvest."
            ],
            "mr": [
                "पेरणीपूर्वी बियाण्यांवर ऍसिड डीलिंटिंग करा.",
                "पाणी तुषाराने न देता सरी-वरंबा पद्धतीने द्या.",
                "हंगाम संपल्यावर पिकाचे अवशेष जाळून नष्ट करा."
            ],
            "hi": [
                "बुवाई से पहले कपास के बीजों का एसिड डिलिंटिंग करें।",
                "फसल अवशेषों को खेत से बाहर निकालकर नष्ट करें।"
            ]
        }
    },

    "Potato Early Blight": {
        "crop": "Potato",
        "disease_name": "Potato Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": {
            "en": "Brown-black concentric rings forming target spot patterns on lower potato foliage.",
            "mr": "बटाट्याच्या खालच्या पानांवर काळे-तपकिरी चक्राकार डाग पडतात.",
            "hi": "आलू की निचली पत्तियों पर संकेंद्रित छल्लों वाले गहरे भूरे-काले धब्बे।"
        },
        "chemical_control": {
            "en": [
                "Mancozeb 75% WP @ 2.5 g/L or Chlorothalonil 75% WP @ 2 g/L.",
                "Azoxystrobin 23% SC @ 1 ml/L at onset of lesions."
            ],
            "mr": [
                "मॅन्कोझेब ७५% WP २.५ ग्रॅम किंवा क्लोरोथॅलोनिल २ ग्रॅम/लिटर फवारावे.",
                "अझोक्सिस्ट्रोबिन २३% SC १ मिली/लिटर पाण्यात मिसळून फवारावे."
            ],
            "hi": [
                "मैनकोजेब 75% WP को 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें।",
                "एजॉक्सीस्ट्रोबिन 23% SC को 1 मिली प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic_control": {
            "en": ["Trichoderma harzianum @ 5 g/L", "5% Neem Seed Kernel Extract (NSKE)."],
            "mr": ["ट्रायकोडर्मा ५ ग्रॅम/लिटर", "५% निंबोळी अर्क फवारावे."],
            "hi": ["ट्राइकोडर्मा 5 ग्राम प्रति लीटर", "5% नीम अर्क का छिड़काव करें।"]
        },
        "cultural_practices": {
            "en": ["Avoid overhead irrigation", "Practice 2-year crop rotation with cereals."],
            "mr": ["तुषार सिंचन टाळा", "तृणधान्यांसोबत फेरपालट करा."],
            "hi": ["फव्वारा सिंचाई से बचें", "अनाज फसलों के साथ फसल चक्र अपनाएं।"]
        }
    },

    "Potato Late Blight": {
        "crop": "Potato",
        "disease_name": "Potato Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": {
            "en": "Water-soaked dark lesions spreading rapidly across foliage with white downy mildew under humid weather.",
            "mr": "पानांवर काळे-तपकिरी पाणावलेले डाग वेगाने पसरतात आणि पानाच्या खाली पांढरी बुरशी दिसते.",
            "hi": "पत्तियों पर पानी से भीगे काले-भूरे धब्बे जो नम मौसम में तेजी से फैलते हैं।"
        },
        "chemical_control": {
            "en": [
                "Dimethomorph 50% WP @ 1 g/L + Mancozeb @ 2 g/L.",
                "Cymoxanil 8% + Mancozeb 64% WP @ 2.5 g/L."
            ],
            "mr": [
                "डायमेथोमॉर्फ १ ग्रॅम + मॅन्कोझेब २ ग्रॅम/लिटर फवारावे.",
                "सायमॉक्सॅनिल + मॅन्कोझेब २.५ ग्रॅम/लिटर फवारावे."
            ],
            "hi": [
                "डाइमेथोमॉर्फ 1 ग्राम + मैनकोजेब 2 ग्राम प्रति लीटर छिड़कें।",
                "साइमोक्सानिल + मैनकोजेब 2.5 ग्राम प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic_control": {
            "en": ["1% Bordeaux mixture preventive spray", "Pseudomonas fluorescens @ 5 g/L."],
            "mr": ["१% बोर्डो मिश्रण प्रतिबंधात्मक फवारणी", "स्यूडोमोनास ५ ग्रॅम/लिटर."],
            "hi": ["1% बोर्डो मिश्रण का छिड़काव", "स्यूडोमोनास 5 ग्राम/लीटर छिड़कें।"]
        },
        "cultural_practices": {
            "en": ["Hill up ridges to protect tubers", "Destroy infected volunteer tubers."],
            "mr": ["बटाटे उघडे पडू नयेत म्हणून मातीची भर लावा", "रोगट अवशेष नष्ट करा."],
            "hi": ["कंदों को ढकने के लिए मिट्टी चढ़ाएं", "संक्रमित पौधों को नष्ट करें।"]
        }
    },

    "Corn Common Rust": {
        "crop": "Corn",
        "disease_name": "Corn Common Rust",
        "pathogen": "Puccinia sorghi (Fungus)",
        "symptoms": {
            "en": "Golden-brown to cinnamon-brown pustules scattered over both upper and lower leaf surfaces.",
            "mr": "मक्याच्या दोन्ही बाजूंच्या पानांवर तांबूस-तपकिरी रंगाचे बारीक फोड (तांबेरा) दिसतात.",
            "hi": "मक्का की पत्तियों पर दालचीनी जैसे भूरे रंग के उभरे हुए फफोले।"
        },
        "chemical_control": {
            "en": ["Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L.", "Mancozeb 75% WP @ 2.5 g/L."],
            "mr": ["अझोक्सिस्ट्रोबिन + डायफेनोकोनाझोल १ मिली/लिटर फवारावे.", "मॅन्कोझेब २.५ ग्रॅम/लिटर फवारावे."],
            "hi": ["एजॉक्सीस्ट्रोबिन + डाइफेनोकोनाजोल 1 मिली/लीटर स्प्रे करें।", "मैनकोजेब 2.5 ग्राम/लीटर छिड़कें।"]
        },
        "organic_control": {
            "en": ["Foliar spray with Bacillus subtilis @ 5 g/L.", "Neem oil 10,000 ppm @ 3 ml/L."],
            "mr": ["बॅसिलस सबटिलिस ५ ग्रॅम/लिटर", "कडुनिंब तेल ३ मिली/लिटर."],
            "hi": ["बैसिलस सबटिलिस 5 ग्राम/लीटर", "नीम तेल 3 मिली/लीटर छिड़कें।"]
        },
        "cultural_practices": {
            "en": ["Plant resistant corn hybrids", "Early sowing to avoid cool humid rust peaks."],
            "mr": ["रोगप्रतिकारक संकरित जातींची लागवड करा", "हंगामाच्या सुरुवातीला पेरणी करा."],
            "hi": ["रोग प्रतिरोधी संकरित किस्मों का चयन करें", "समय पर बुवाई करें।"]
        }
    },

    "Pepper Bacterial Spot": {
        "crop": "Pepper",
        "disease_name": "Pepper Bacterial Spot",
        "pathogen": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": {
            "en": "Small circular to irregular dark brown spots with prominent yellow chlorotic halos on foliage.",
            "mr": "मिरचीच्या पानांवर पिवळी कडा असलेले बारीक काळे-तपकिरी डाग पडतात.",
            "hi": "मिर्च की पत्तियों पर पीले घेरे वाले छोटे गहरे भूरे धब्बे।"
        },
        "chemical_control": {
            "en": ["Copper Hydroxide 53.8% DF @ 2 g/L + Streptocycline @ 0.1 g/L."],
            "mr": ["कॉपर हायड्रॉक्साइड २ ग्रॅम + स्ट्रेप्टोसायक्लिन ०.१ ग्रॅम/लिटर फवारावे."],
            "hi": ["कॉपर हाइड्रॉक्साइड 2 ग्राम + स्ट्रेप्टोसाइक्लिन 0.1 ग्राम/लीटर छिड़कें।"]
        },
        "organic_control": {
            "en": ["Seed treatment with hot water (50°C for 25 min)", "Pseudomonas fluorescens @ 5 g/L."],
            "mr": ["स्यूडोमोनास ५ ग्रॅम/लिटर", "५% दशपर्णी अर्क फवारावे."],
            "hi": ["गर्म पानी से बीजोपचार", "स्यूडोमोनास 5 ग्राम/लीटर स्प्रे करें।"]
        },
        "cultural_practices": {
            "en": ["Ensure disease-free nursery seedlings", "Avoid touching wet foliage in morning."],
            "mr": ["निरोगी रोपे वापरा", "सकाळी दवात काम करणे टाळा."],
            "hi": ["स्वस्थ पौध का रोपण करें", "गीली पत्तियों को छूने से बचें।"]
        }
    }
}

# Pest management database
PEST_RECOMMENDATIONS: Dict[str, Dict[str, Any]] = {
    "Aphids": {
        "pest_name": "Aphids (Mawa / Lahi)",
        "damage": {
            "en": "Clusters of tiny green/black insects sucking sap under leaves, leading to leaf curl and sooty mold.",
            "mr": "पानांच्या खालच्या बाजूला बारीक काळे किंवा हिरवे किडे रस शोषतात, ज्यामुळे पाने आकसतात.",
            "hi": "पत्तियों के नीचे छोटे हरे/काले कीड़ों का समूह रस चूसता है।"
        },
        "chemical_control": {
            "en": [
                "Imidacloprid 17.8% SL @ 0.5 ml/liter of water.",
                "Thiamethoxam 25% WG @ 0.3 g/liter.",
                "Acetamiprid 20% SP @ 0.4 g/liter."
            ],
            "mr": [
                "इमिडाक्लोप्रिड १७.८% SL ०.५ मिली प्रति लिटर पाण्यात फवारावे.",
                "थायमेथोक्सम २५% WG ०.३ ग्रॅम प्रति लिटर फवारावे.",
                "एसिटामिप्रिड २०% SP ०.४ ग्रॅम प्रति लिटर फवारावे."
            ],
            "hi": [
                "इमिडाक्लोप्रिड 17.8% SL 0.5 मिली प्रति लीटर छिड़कें।",
                "थियामेथोक्सम 25% WG 0.3 ग्राम प्रति लीटर स्प्रे करें।",
                "एसिटामिप्रिड 20% SP 0.4 ग्राम प्रति लीटर छिड़कें।"
            ]
        },
        "organic_control": {
            "en": [
                "Neem oil 10,000 ppm @ 2-3 ml/liter with soap solution.",
                "Install yellow sticky traps @ 10-15 traps per acre.",
                "Release ladybird beetles (Coccinellids) biological predators."
            ],
            "mr": [
                "१०,००० पीपीएम कडुनिंब तेल २-३ मिली साबणाच्या पाण्यात मिसळून फवारावे.",
                "एकरला १०-१५ पिवळे चिकट सापळे लावा.",
                "लेडीबर्ड भुंगेरे (नैसर्गिक मित्रकीटक) जतन करा."
            ],
            "hi": [
                "नीम का तेल 2-3 मिली साबुन के पानी के साथ मिलाकर छिड़कें।",
                "प्रति एकड़ 10-15 पीले चिपचिपे जाल (Yellow Sticky Traps) लगाएं।"
            ]
        }
    },

    "Whitefly": {
        "pest_name": "Whitefly",
        "damage": {
            "en": "Small white fluttering flies under leaves; transmits Yellow Leaf Curl Virus.",
            "mr": "पानांमागे पांढरी माशी; ही पिवळा पान विषाणू (Yellow Leaf Curl) पसरवते.",
            "hi": "पत्तियों के नीचे सफेद मक्खियां; यह पत्ती मरोड़ विषाणु फैलाती है।"
        },
        "chemical_control": {
            "en": [
                "Diafenthiuron 50% WP @ 1.2 g/liter.",
                "Pyriproxyfen 10% EC @ 1.5 ml/liter.",
                "Spiromesifen 22.9% SC @ 1 ml/liter."
            ],
            "mr": [
                "डायफेन्थियुरॉन ५०% WP १.२ ग्रॅम प्रति लिटर पाण्यात फवारावे.",
                "पायरीप्रॉक्सीफेन १०% EC १.५ मिली प्रति लिटर फवारावे.",
                "स्पिरोमेसिफेन २२.९% SC १ मिली प्रति लिटर फवारावे."
            ],
            "hi": [
                "डायफेंथियूरॉन 50% WP 1.2 ग्राम प्रति लीटर छिड़कें।",
                "पायरीप्रॉक्सीफेन 10% EC 1.5 मिली प्रति लीटर स्प्रे करें।"
            ]
        },
        "organic_control": {
            "en": [
                "Yellow sticky traps @ 20 traps/acre.",
                "Spray Verticillium lecanii bio-fungicide @ 5 g/liter.",
                "Neem oil 3 ml/liter."
            ],
            "mr": [
                "एकरला २० पिवळे चिकट सापळे लावा.",
                "व्हर्टिसिलियम लेकानी बुरशीजन्य कीटकनाशक ५ ग्रॅम प्रति लिटर फवारावे.",
                "कडुनिंब तेल ३ मिली प्रति लिटर फवारावे."
            ],
            "hi": [
                "20 पीले चिपचिपे जाल प्रति एकड़ लगाएं।",
                "वर्टिसिलियम लेकेनी जैविक कीटनाशक 5 ग्राम प्रति लीटर छिड़कें।"
            ]
        }
    }
}


class RecommendationService:
    @staticmethod
    def get_disease_recommendations(disease_name: str, language: str = "en") -> Dict[str, Any]:
        """Fetch tailored disease recommendations in requested language."""
        lang = language if language in ["en", "mr", "hi"] else "en"

        # Search matching disease
        matched_key = None
        for key in DISEASE_RECOMMENDATIONS.keys():
            if disease_name.lower() in key.lower() or key.lower() in disease_name.lower():
                matched_key = key
                break

        if matched_key:
            data = DISEASE_RECOMMENDATIONS[matched_key]
            return {
                "crop": data["crop"],
                "disease_name": data["disease_name"],
                "pathogen": data["pathogen"],
                "symptoms": data["symptoms"].get(lang, data["symptoms"]["en"]),
                "chemical_control": data["chemical_control"].get(lang, data["chemical_control"]["en"]),
                "organic_control": data["organic_control"].get(lang, data["organic_control"]["en"]),
                "cultural_practices": data["cultural_practices"].get(lang, data["cultural_practices"]["en"]),
                "precautions": "Always wear protective gear while applying pesticides. Never spray against wind direction."
            }

        # Healthy foliage branch
        if "healthy" in disease_name.lower():
            crop_name = disease_name.replace("healthy", "").replace("Healthy", "").replace("Leaf", "").strip() or "Crop"
            return {
                "crop": crop_name,
                "disease_name": f"{crop_name} Healthy Foliage",
                "pathogen": "None (Crop in Good Health)",
                "symptoms": {
                    "en": "Foliage exhibits vibrant chlorophyll color, intact lamina, and normal cellular structure with no active disease lesions.",
                    "mr": "पानांवर कोणताही रोगाचा प्रादुर्भाव नाही, पाने निरोगी आणि जोमदार आहेत.",
                    "hi": "पत्तियों पर किसी रोग के लक्षण नहीं हैं, पत्तियां स्वस्थ और मजबूत हैं।"
                }.get(lang, "Foliage exhibits vibrant chlorophyll color with no active disease lesions."),
                "chemical_control": {
                    "en": ["No chemical fungicide or pesticide required. Crop is in good health."],
                    "mr": ["कोणतेही रासायनिक बुरशीनाशक फवारण्याची गरज नाही. पीक निरोगी आहे."],
                    "hi": ["किसी रासायनिक कवकनाशी या कीटनाशक की आवश्यकता नहीं है। फसल स्वस्थ है।"]
                }.get(lang, ["No chemical fungicide or pesticide required."]),
                "organic_control": {
                    "en": [
                        "Preventive foliar spray of 5% Neem Seed Kernel Extract (NSKE) to sustain natural defenses.",
                        "Foliar micronutrient or sea-weed extract spray @ 2 ml/L to enhance photosynthetic vigor."
                    ],
                    "mr": [
                        "रोगप्रतिकारशक्ती टिकवण्यासाठी ५% निंबोळी अर्क (NSKE) फवारावे.",
                        "पानांच्या वाढीसाठी सूक्ष्म अन्नद्रव्ये किंवा सेंद्रिय टॉनिक २ मिली/लिटर फवारावे."
                    ],
                    "hi": [
                        "पौधों की प्राकृतिक प्रतिरक्षा बनाए रखने के लिए 5% नीम अर्क का छिड़काव करें।",
                        "पोषक तत्वों की आपूर्ति के लिए सूक्ष्म पोषक तत्व या सीवीड अर्क 2 मिली/लीटर स्प्रे करें।"
                    ]
                }.get(lang, ["Preventive foliar spray of 5% Neem Seed Kernel Extract (NSKE)."]),
                "cultural_practices": {
                    "en": [
                        "Continue balanced irrigation without waterlogging.",
                        "Maintain recommended N-P-K nutrient schedule.",
                        "Keep field borders clean of weeds."
                    ],
                    "mr": [
                        "ठिबक सिंचनाद्वारे वेळेवर पाणी द्या आणि पाण्याचा निचरा व्यवस्थित ठेवा.",
                        "योग्य खत व्यवस्थापन (NPK) चालू ठेवा.",
                        "शेतातील तण काढून स्वच्छता ठेवा."
                    ],
                    "hi": [
                        "उचित सिंचाई जारी रखें और जलभराव से बचें।",
                        "अनुशंसित खाद एवं पोषक तत्व प्रबंधन जारी रखें।",
                        "खेत को खरपतवार मुक्त रखें।"
                    ]
                }.get(lang, ["Continue balanced irrigation and nutrient management."]),
                "precautions": "Avoid unneeded chemical sprays to preserve beneficial insects and natural predators."
            }

        # Generic fallback
        return {
            "crop": "General Crop",
            "disease_name": disease_name,
            "pathogen": "Identified Plant Stress / Pathogen",
            "symptoms": f"Visible leaf abnormalities identified as {disease_name}.",
            "chemical_control": [
                "Apply broad-spectrum protective fungicide (Mancozeb 75% WP @ 2.5 g/L).",
                "Consult local Krishi Vigyan Kendra (KVK) for specialized prescription."
            ],
            "organic_control": [
                "Foliar spray with 5% Neem Seed Kernel Extract (NSKE).",
                "Apply Trichoderma viride @ 5 g/L of water."
            ],
            "cultural_practices": [
                "Prune and destroy severely infected plant parts.",
                "Ensure balanced N-P-K nutrition and avoid waterlogging."
            ],
            "precautions": "Avoid application in rainy or extremely windy conditions."
        }

    @staticmethod
    def get_pest_recommendations(pest_name: str, language: str = "en") -> Dict[str, Any]:
        """Fetch pest control recommendations."""
        lang = language if language in ["en", "mr", "hi"] else "en"

        matched_key = None
        for key in PEST_RECOMMENDATIONS.keys():
            if pest_name.lower() in key.lower() or key.lower() in pest_name.lower():
                matched_key = key
                break

        if matched_key:
            data = PEST_RECOMMENDATIONS[matched_key]
            return {
                "pest_name": data["pest_name"],
                "damage": data["damage"].get(lang, data["damage"]["en"]),
                "chemical_control": data["chemical_control"].get(lang, data["chemical_control"]["en"]),
                "organic_control": data["organic_control"].get(lang, data["organic_control"]["en"]),
            }

        return {
            "pest_name": pest_name,
            "damage": "Pest activity causing feeding marks or leaf damage.",
            "chemical_control": ["Apply recommended broad-spectrum insecticide as per label guidelines."],
            "organic_control": ["Install sticky traps and spray Neem oil (5 ml/L)."]
        }
