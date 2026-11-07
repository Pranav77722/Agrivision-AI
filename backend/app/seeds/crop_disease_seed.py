"""
Crop Disease Catalog Seed Data for Agrivision AI+.
Contains real agricultural data for Tomato, Rice, Wheat, and Cotton diseases.
"""

from typing import List, Dict, Any

CROP_DISEASES_CATALOG: List[Dict[str, Any]] = [
    # Tomato Diseases
    {
        "crop": "Tomato",
        "disease_name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "symptoms": {
            "en": "Brown to black spots with concentric rings appearing on older lower leaves first.",
            "mr": "खालच्या जुन्या पानांवर काळे-तपकिरी चक्राकार गोल डाग पडतात.",
            "hi": "निचली पत्तियों पर संकेंद्रित छल्लों वाले गहरे भूरे-काले धब्बे।"
        },
        "optimal_conditions": "Warm temperatures (24-29°C) and high humidity or frequent rainfall."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": {
            "en": "Water-soaked lesions on leaves rapidly turning purplish-black with white mildew in humid mornings.",
            "mr": "पानांवर काळसर जांभळट डाग पडतात आणि दमट हवेत पानाच्या मागे पांढरी बुरशी वाढते.",
            "hi": "पत्तियों पर जलसिक्त धब्बे जो तेजी से बैंगनी-काले हो जाते हैं।"
        },
        "optimal_conditions": "Cool (15-20°C) wet weather with prolonged leaf wetness."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva",
        "symptoms": {
            "en": "Pale green or yellowish spots on upper leaf surface with olive-green to gray velvety mold underneath.",
            "mr": "पानाच्या वरच्या बाजूला पिवळे डाग आणि खालच्या बाजूला ऑलिव्ह हिरवट-राखाडी मखमली बुरशी.",
            "hi": "पत्तियों की ऊपरी सतह पर पीले धब्बे और नीचे मखमली कवक।"
        },
        "optimal_conditions": "High relative humidity (>85%) and temperatures between 20-25°C."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "symptoms": {
            "en": "Numerous small circular spots with grayish-white centers and dark brown margins.",
            "mr": "पानांवर लहान गोल डाग ज्यांचे केंद्र पांढरे-राखाडी आणि कडा गडद तपकिरी असतात.",
            "hi": "गहरे भूरे किनारों और भूरे-सफेद केंद्र वाले छोटे गोलाकार धब्बे।"
        },
        "optimal_conditions": "Extended wet weather and moderate warmth (20-25°C)."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Spider Mites",
        "scientific_name": "Tetranychus urticae",
        "symptoms": {
            "en": "Yellow stippling or bronzing on upper leaf surface, fine webbing on leaf undersides.",
            "mr": "पानांवर पिवळे लहान ठिपके, पाने तांबूस पडणे आणि पानाच्या खाली बारीक जाळे तयार होणे.",
            "hi": "पत्तियों पर पीलापन, तांबे जैसा रंग और पत्तियों के नीचे बारीक जाला।"
        },
        "optimal_conditions": "Hot, dry, and dusty conditions (above 30°C)."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Yellow Leaf Curl Virus",
        "scientific_name": "TYLCV (Begomovirus transmitted by Whitefly)",
        "symptoms": {
            "en": "Upward curling and cupping of leaves, chlorotic margins, stunted bushy plant growth.",
            "mr": "पाने वरच्या बाजूला आकसून वाटीसारखी होतात, कडा पिवळ्या पडतात आणि झाडाची वाढ खुंटते.",
            "hi": "पत्तियों का ऊपर की ओर मुड़ना, किनारों पर पीलापन और पौधे का बौना रह जाना।"
        },
        "optimal_conditions": "High whitefly (Bemisia tabaci) populations in dry/warm seasons."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Mosaic Virus",
        "scientific_name": "ToMV (Tobamovirus)",
        "symptoms": {
            "en": "Mottling of leaves with alternating light and dark green areas, leaf distortion and blistering.",
            "mr": "पानांवर फिकट व गडद हिरव्या रंगाचे चट्टे (मोझॅक), पाने चुरगळणे व विकृत होणे.",
            "hi": "पत्तियों पर हल्के और गहरे हरे रंग के चित्तीदार धब्बे और विकृति।"
        },
        "optimal_conditions": "Easily transmitted mechanically via tools, hands, and infected seeds."
    },
    {
        "crop": "Tomato",
        "disease_name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas perforans",
        "symptoms": {
            "en": "Small water-soaked circular spots turning dark brown to black, scabby raised lesions on green fruit.",
            "mr": "पानांवर आणि फळांवर काळे-तपकिरी खडबडीत व्रण आणि डाग पडतात.",
            "hi": "पत्तियों और फलों पर छोटे पानी से भीगे भूरे-काले उभरे हुए धब्बे।"
        },
        "optimal_conditions": "Warm rainy weather (25-30°C) with splashing rain."
    },

    # Rice Diseases
    {
        "crop": "Rice",
        "disease_name": "Rice Blast",
        "scientific_name": "Magnaporthe oryzae",
        "symptoms": {
            "en": "Diamond or spindle-shaped lesions with gray centers, neck rot causing panicle collapse.",
            "mr": "पानांवर टोकदार आकाराचे डाग आणि लोंबीच्या मानेवर करपा पडून लोंबी मोडणे.",
            "hi": "पत्तियों पर तर्कुरूपी धब्बे और बालियों की गर्दन पर सड़न।"
        },
        "optimal_conditions": "High humidity (>90%), cool nights (17-20°C), and excessive nitrogen application."
    },
    {
        "crop": "Rice",
        "disease_name": "Rice Brown Spot",
        "scientific_name": "Bipolaris oryzae",
        "symptoms": {
            "en": "Small, oval, brown spots scattered over leaves with yellow halos; poorly filled grain.",
            "mr": "पानांवर गोलाकार-लंबगोलाकार तपकिरी डाग ज्यांच्याभोवती पिवळे वलय असते.",
            "hi": "पत्तियों पर पीले घेरे वाले छोटे अंडाकार भूरे धब्बे।"
        },
        "optimal_conditions": "Nutrient-deficient soils, water stress, and high humidity."
    },
    {
        "crop": "Rice",
        "disease_name": "Rice Leaf Scald",
        "scientific_name": "Microdochium oryzae",
        "symptoms": {
            "en": "Zonate lesions starting from leaf tips and margins with alternating light and dark brown bands.",
            "mr": "पानाच्या टोकाकडून करपा सुरू होऊन पानावर पट्टेदार फिकट व गडद तपकिरी वलये दिसतात.",
            "hi": "पत्तियों के सिरों से शुरू होने वाले धारीदार भूरे धब्बे।"
        },
        "optimal_conditions": "High humidity, continuous cloud cover, and heavy rainfall."
    },
    {
        "crop": "Rice",
        "disease_name": "Rice Bacterial Blight",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "symptoms": {
            "en": "Water-soaked stripes on leaf margins turning wavy yellow-white, bacterial ooze drops.",
            "mr": "पानांच्या कडांवरून पिवळसर-पांढऱ्या नागमोडी पट्ट्या तयार होतात, कडा वाळतात.",
            "hi": "पत्तियों के किनारों पर लहरदार पीले-सफेद पट्टे।"
        },
        "optimal_conditions": "Temperatures 25-34°C, strong winds with heavy rain."
    },
    {
        "crop": "Rice",
        "disease_name": "Rice Sheath Blight",
        "scientific_name": "Rhizoctonia solani",
        "symptoms": {
            "en": "Greenish-gray oval lesions on leaf sheaths near water line with irregular brownish borders.",
            "mr": "पाण्याच्या पातळीजवळ खोडाच्या पापुद्र्यावर राखाडी-हिरवट डाग आणि काळे डाग.",
            "hi": "पानी की सतह के पास तने के आवरण पर धूसर-हरे अंडाकार धब्बे।"
        },
        "optimal_conditions": "Dense crop canopy, high temperature (28-32°C), and humidity >95%."
    },

    # Wheat Diseases
    {
        "crop": "Wheat",
        "disease_name": "Wheat Rust",
        "scientific_name": "Puccinia striiformis / Puccinia triticina",
        "symptoms": {
            "en": "Bright yellow or reddish-brown powdery pustules arranged in stripes or patches on leaf blades.",
            "mr": "पानांवर पिवळ्या किंवा विटकरी रंगाच्या लहान पुळ्या (तांबेरा) रांगेत दिसतात.",
            "hi": "पत्तियों पर पीली या लाल-भूरी पाउडर जैसी धारियां या धब्बे (रतुआ)।"
        },
        "optimal_conditions": "Cool moist weather (10-15°C for stripe rust, 15-25°C for brown rust)."
    },
    {
        "crop": "Wheat",
        "disease_name": "Wheat Powdery Mildew",
        "scientific_name": "Blumeria graminis f. sp. tritici",
        "symptoms": {
            "en": "White to light gray powdery fungal patches on leaves and stems, turning yellowish.",
            "mr": "पानांवर आणि खोडावर पांढऱ्या पिठासारखी बुरशीची थर (भुरी रोग).",
            "hi": "पत्तियों और तने पर सफेद पाउडर जैसे कवक के धब्बे।"
        },
        "optimal_conditions": "Dense stands, shaded fields, temperature 15-22°C with high humidity."
    },
    {
        "crop": "Wheat",
        "disease_name": "Wheat Septoria",
        "scientific_name": "Zymoseptoria tritici",
        "symptoms": {
            "en": "Irregular necrotic brown blotches with tiny black fruiting bodies (pycnidia) inside.",
            "mr": "पानांवर तपकिरी चट्टे आणि चट्ट्यांमध्ये बारीक काळे ठिपके (बुरशीचे बीजाणू) दिसतात.",
            "hi": "पत्तियों पर अनियमित भूरे धब्बे जिनके अंदर छोटे काले दानेदार बिंदु होते हैं।"
        },
        "optimal_conditions": "Cool, wet, and windy conditions early in spring."
    },
    {
        "crop": "Wheat",
        "disease_name": "Wheat Karnal Bunt",
        "scientific_name": "Tilletia indica",
        "symptoms": {
            "en": "Partial conversion of grain kernels into black foul-smelling powdery spore masses (rotten fish odor).",
            "mr": "गव्हाच्या दाण्यांमध्ये काळी दुर्गंधीयुक्त पावडर तयार होते (सडलेल्या माशासारखा वास).",
            "hi": "गेहूं के दानों का आंशिक रूप से काले बदबूदार चूर्ण में बदलना।"
        },
        "optimal_conditions": "Cool cloudy weather (15-20°C) with showers at anthesis/heading stage."
    },

    # Cotton Diseases
    {
        "crop": "Cotton",
        "disease_name": "Cotton Bacterial Blight",
        "scientific_name": "Xanthomonas citri pv. malvacearum",
        "symptoms": {
            "en": "Angular water-soaked spots bounded by veins on leaves, black lesions on stems ('blackarm').",
            "mr": "पानांवर शिरांमधील त्रिकोणी डाग, फांद्यांवर काळे चट्टे (काळी काठी रोग).",
            "hi": "पत्तियों पर कोणीय काले धब्बे और शाखाओं पर काले घाव।"
        },
        "optimal_conditions": "Warm humid conditions (30-35°C) and splashing monsoon rains."
    },
    {
        "crop": "Cotton",
        "disease_name": "Cotton Alternaria Leaf Spot",
        "scientific_name": "Alternaria macrospora",
        "symptoms": {
            "en": "Brown circular spots with purple margins and concentric rings on older leaves; defoliation.",
            "mr": "पानांवर जांभळट कडा असलेले तपकिरी चक्राकार डाग, पाने अकाली गळणे.",
            "hi": "बैंगनी किनारों वाले गोलाकार भूरे धब्बे और पत्तियों का गिरना।"
        },
        "optimal_conditions": "Intermittent wet and dry spells with temperature between 25-30°C."
    },
    {
        "crop": "Cotton",
        "disease_name": "Cotton Grey Mildew",
        "scientific_name": "Ramularia areola",
        "symptoms": {
            "en": "Angular pale translucent lesions covered with frosty white-grey powdery growth underneath.",
            "mr": "पानाच्या खाली पांढऱ्या-राखाडी बुरशीचे डाग (दहिया रोग).",
            "hi": "पत्तियों की निचली सतह पर सफेद-धूसर पाउडर जैसी कवक (दहिया रोग)।"
        },
        "optimal_conditions": "High humidity and continuous cloudy weather late in season."
    },
    {
        "crop": "Cotton",
        "disease_name": "Cotton Root Rot",
        "scientific_name": "Rhizoctonia bataticola / Macrophomina phaseolina",
        "symptoms": {
            "en": "Sudden wilting and drooping of leaves, shredding of root bark, yellowing and plant death.",
            "mr": "झाड अचानक कोमेजून सुकणे, मुळांची साल निघणे आणि झाड मरणे (मूळ कुज).",
            "hi": "पौधे का अचानक मुरझाना और जड़ों की छाल का सड़ना।"
        },
        "optimal_conditions": "High soil temperatures (above 35°C) with dry surface soil."
    }
]
