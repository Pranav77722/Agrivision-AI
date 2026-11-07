"""
Knowledge Base Articles Seed Data for Agrivision AI+.
Provides rich agricultural articles in English, Marathi, and Hindi.
"""

from typing import List, Dict, Any

KNOWLEDGE_ARTICLES_SEED: List[Dict[str, Any]] = [
    {
        "category": "Disease Management",
        "title_en": "Integrated Management of Tomato Early & Late Blight",
        "title_mr": "टोमॅटो पिकातील लवकर व उशिरा येणारा करपा रोग व्यवस्थापन",
        "title_hi": "टमाटर में अगेती और पछेती झुलसा का एकीकृत प्रबंधन",
        "content_en": (
            "Tomato blights are devastating fungal diseases caused by Alternaria solani (Early Blight) "
            "and Phytophthora infestans (Late Blight). Early blight forms concentric rings on leaves, "
            "while late blight causes dark water-soaked lesions that spread rapidly during cloudy, humid weather.\n\n"
            "Key Management Steps:\n"
            "1. Preventative Spraying: Apply Mancozeb 75% WP @ 2.5 g/liter before heavy rains.\n"
            "2. Systemic Control: Spray Metalaxyl + Mancozeb (Ridomil) @ 2 g/liter when symptoms appear.\n"
            "3. Bio-control: Trichoderma harzianum @ 5 g/liter and 5% Neem extract.\n"
            "4. Cultural: Prune infected lower leaves and maintain drip irrigation."
        ),
        "content_mr": (
            "टोमॅटो पिकावर करपा हा अत्यंत नुकसानकारक रोग आहे. लवकर येणारा करपा (Early Blight) आल्टरनेरिया बुरशीमुळे "
            "आणि उशिरा येणारा करपा (Late Blight) फायटोप्थोरा बुरशीमुळे होतो. ढगाळ व दमट हवामानात हा रोग वेगाने पसरतो.\n\n"
            "महत्त्वाचे उपाय:\n"
            "१. प्रतिबंधात्मक फवारणी: मॅन्कोझेब ७५% WP २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.\n"
            "२. बुरशीनाशक उपचार: प्रादुर्भाव दिसताच मेटॅलॅक्सिल + मॅन्कोझेब (रिडोमिल) २ ग्रॅम प्रति लिटर फवारावे.\n"
            "३. सेंद्रिय उपाय: ट्रायकोडर्मा ५ ग्रॅम किंवा ५% निंबोळी अर्क फवारावा.\n"
            "४. मशागती पद्धती: खालची रोगट पाने तोडून नष्ट करा आणि ठिबक सिंचनाचा वापर करा."
        ),
        "content_hi": (
            "टमाटर का झुलसा रोग अल्टरनेरिया और फाइटोफ्थोरा कवक के कारण होता है। नम और बादलों वाले मौसम में यह रोग "
            "पत्तियों और फलों को गंभीर नुकसान पहुंचाता है।\n\n"
            "प्रबंधन के मुख्य उपाय:\n"
            "1. रोकथाम: मैनकोजेब 75% WP को 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़कें।\n"
            "2. नियंत्रण: रिडोमिल (मेटालैक्सिल + मैनकोजेब) 2 ग्राम प्रति लीटर पानी में स्प्रे करें।\n"
            "3. जैविक उपचार: 5% नीम के बीज का अर्क और ट्राइकोडर्मा का छिड़काव करें।\n"
            "4. ड्रिप सिंचाई अपनाएं और संक्रमित पत्तियों को खेत से दूर नष्ट करें।"
        ),
        "tags": ["Tomato", "Blight", "Fungicide", "Plant Pathology", "Organic Farming"],
        "is_published": True
    },
    {
        "category": "Soil & Fertilizers",
        "title_en": "Balanced NPK Fertilization and Soil Health Optimization",
        "title_mr": "संतुलित खत व्यवस्थापन आणि जमिनीचे आरोग्य संवर्धन",
        "title_hi": "संतुलित उर्वरक प्रबंधन और मृदा स्वास्थ्य सुधार",
        "content_en": (
            "Over-reliance on chemical nitrogen (Urea) leads to soil acidification, micronutrient imbalance, "
            "and increased crop susceptibility to sucking pests and leaf blights.\n\n"
            "Best Practices for Soil Fertility:\n"
            "1. Soil Testing: Test soil every 2 years to determine exact pH, organic carbon, and NPK levels.\n"
            "2. Split Application: Never apply the full nitrogen dose at sowing; split into basal, vegetative, and flowering stages.\n"
            "3. Organic Carbon: Add 5 tonnes of well-rotted FYM or vermicompost per hectare.\n"
            "4. Biofertilizers: Incorporate Azotobacter, Rhizobium, and Phosphate Solubilizing Bacteria (PSB)."
        ),
        "content_mr": (
            "केवळ युरियाचा अतिरेक केल्याने जमिनीचा पोत बिघडतो, पिकाची रोगप्रतिकारशक्ती कमी होते आणि रस शोषणाऱ्या "
            "किडींचा प्रादुर्भाव वाढतो.\n\n"
            "जमिनीच्या सुपीकतेसाठी मार्गदर्शक तत्त्वे:\n"
            "१. माती परीक्षण: दर दोन वर्षांनी माती परीक्षण करून खतांची योग्य मात्रा ठरवा.\n"
            "२. खतांचे हप्ते: युरिया एकाच वेळी न देता पेरणी, वाढीची अवस्था आणि फुलोऱ्यात विभागून द्या.\n"
            "३. सेंद्रिय खते: दरवर्षी एकरी ५ टन चांगले कुजलेले शेणखत किंवा गांडूळ खत द्या.\n"
            "४. जिवाणू संवर्धक: अझोटोबॅक्टर, रायझोबियम आणि पीएसबी (PSB) चा वापर करा."
        ),
        "content_hi": (
            "केवल यूरिया का अत्यधिक उपयोग मिट्टी की संरचना को बिगाड़ता है और कीट-रोगों को आकर्षित करता है।\n\n"
            "उर्वरक प्रबंधन के नियम:\n"
            "1. मृदा परीक्षण: हर 2 साल में मिट्टी की जांच कराएं।\n"
            "2. संतुलित मात्रा: नाइट्रोजन को 3 भागों में बांटकर दें (बुवाई, वानस्पतिक बढ़वार, और फूल आते समय)।\n"
            "3. जीवांश कार्बन: प्रति हेक्टेयर 5 टन गोबर की खाद या केंचुआ खाद डालें।\n"
            "4. जैव उर्वरक: पीएसबी (PSB) और एजोटोबैक्टर का उपयोग करें।"
        ),
        "tags": ["Soil Health", "Fertilizers", "NPK", "Organic Carbon", "Vermicompost"],
        "is_published": True
    },
    {
        "category": "Pest Management",
        "title_en": "Pink Bollworm and Sucking Pest Management in Cotton",
        "title_mr": "कपाशीवरील गुलाबी बोंडअळी व रस शोषणाऱ्या किडींचे एकात्मिक नियंत्रण",
        "title_hi": "कपास में गुलाबी सुंडी और रस चूसक कीटों का नियंत्रण",
        "content_en": (
            "Pink bollworm (Pectinophora gossypiella) enters cotton bolls undetected and damages lint and seeds. "
            "Sucking pests like aphids, thrips, and whiteflies damage early foliage.\n\n"
            "Integrated Management Protocol:\n"
            "1. Pheromone Traps: Install 5 pheromone traps per acre at 45 days after sowing for moth monitoring.\n"
            "2. Biocontrol: Release Trichogramma egg parasitoids @ 60,000 per acre.\n"
            "3. Spraying: If trap catches exceed 8 moths/day, spray Profenofos 50% EC @ 2 ml/liter or Emamectin Benzoate 5% SG @ 0.5 g/liter.\n"
            "4. Sticky Traps: Use yellow and blue sticky traps for whiteflies and thrips."
        ),
        "content_mr": (
            "गुलाबी बोंडअळी कपाशीच्या बोंडात शिरून रुई व सरकीचे प्रचंड नुकसान करते. तसेच मावा, तुडतुडे व पांढरी माशी पानांतील रस शोषतात.\n\n"
            "एकात्मिक कीड व्यवस्थापन:\n"
            "१. कामगंध सापळे: पेरणीनंतर ४५ दिवसांनी एकरी ५ कामगंध सापळे (Pheromone Traps) लावा.\n"
            "२. जैविक नियंत्रण: ट्रायकोकार्ड्स (Trichogramma) चा वापर करा.\n"
            "३. रासायनिक फवारणी: आर्थिक नुकसान पातळी ओलांडल्यास प्रोफेनोफॉस ५०% EC २ मिली किंवा इमामेक्टिन बेन्झोएट ०.५ ग्रॅम प्रति लिटर फवारावे.\n"
            "४. चिकट सापळे: पांढरी माशी व थ्रिप्ससाठी पिवळे व निळे चिकट सापळे लावा."
        ),
        "content_hi": (
            "गुलाबी सुंडी कपास के टिंडों के अंदर जाकर रुई और बीज को नुकसान पहुंचाती है।\n\n"
            "नियंत्रण उपाय:\n"
            "1. फेरोमोन ट्रैप: बुवाई के 45 दिन बाद प्रति एकड़ 5 फेरोमोन ट्रैप लगाएं।\n"
            "2. परजीवी कीट: ट्राइकोग्रामा के कार्ड खेत में लगाएं।\n"
            "3. कीटनाशक स्प्रे: प्रोफेनोफॉस 50% EC 2 मिली या इमामेक्टिन बेंजोएट 0.5 ग्राम प्रति लीटर पानी में छिड़कें।\n"
            "4. पीले और नीले चिपचिपे जाल लगाएं।"
        ),
        "tags": ["Cotton", "Pink Bollworm", "Pheromone Traps", "Pest Management"],
        "is_published": True
    },
    {
        "category": "Water & Irrigation",
        "title_en": "Smart Micro-Irrigation & Drip Scheduling for Cash Crops",
        "title_mr": "नगदी पिकांसाठी ठिबक सिंचन आणि पाण्याचे काटेकोर नियोजन",
        "title_hi": "नकदी फसलों के लिए स्मार्ट ड्रिप सिंचाई और जल प्रबंधन",
        "content_en": (
            "Drip irrigation saves 40-60% water compared to furrow irrigation and increases yield by 20-30% "
            "through direct delivery to the active root zone.\n\n"
            "Key Scheduling Rules:\n"
            "1. Fertigation: Soluble NPK fertilizers (19:19:19, 0:52:34) can be applied directly via venturi.\n"
            "2. Operating Pressure: Maintain lateral line pressure at 1.0 to 1.2 kg/cm².\n"
            "3. Acid Treatment: Perform regular flushing and dilute hydrochloric acid treatment (pH 5.5) to clear dripper clogging from hard water."
        ),
        "content_mr": (
            "पारंपारिक पद्धतीपेक्षा ठिबक सिंचनामुळे ४० ते ६० टक्के पाण्याची बचत होते आणि पिकाचे उत्पादन २० ते ३० टक्क्यांनी वाढते.\n\n"
            "महत्त्वाचे नियम:\n"
            "१. व्हेंचुरीद्वारे खत देणे (फर्टिगेशन): विद्राव्य खते थेट मुळांशी पोहोचतात.\n"
            "२. पाण्याचा दाब: लॅटरल नळ्यांमध्ये १.० ते १.२ किलोग्रॅम दाब ठेवावा.\n"
            "३. ड्रीपर स्वच्छता: क्षार साचल्यास ऍसिड ट्रीटमेंट देऊन ड्रीपर मोकळे करावेत."
        ),
        "content_hi": (
            "ड्रिप सिंचाई से 40-60% पानी की बचत होती है और पैदावार में उल्लेखनीय वृद्धि होती है।\n\n"
            "मुख्य बिंदु:\n"
            "1. वेंचुरी द्वारा घुलनशील उर्वरक (फर्टिगेशन) दें।\n"
            "2. नियमित रूप से पाइपों की फ्लशिंग करें ताकि ड्रिपर चोक न हों।"
        ),
        "tags": ["Irrigation", "Drip", "Water Conservation", "Fertigation"],
        "is_published": True
    }
]
