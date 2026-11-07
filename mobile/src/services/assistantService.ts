import apiClient from './api';
import { ChatMessage } from '../types';

export const assistantService = {
  sendMessage: async (prompt: string, language: string): Promise<ChatMessage> => {
    try {
      const res = await apiClient.post<ChatMessage>('/assistant/chat', { prompt, language });
      return res.data;
    } catch {
      // Realistic localized AI advisory responses
      let reply = '';
      const lower = prompt.toLowerCase();

      if (language === 'mr') {
        if (lower.includes('टोमॅटो') || lower.includes('करपा') || lower.includes('tomato')) {
          reply =
            'टोमॅटोवरील अर्ली ब्लाइट (करपा) रोगासाठी १०,००० PPM निंबोळी अर्क ३ मिली/लिटर किंवा मॅन्कोझेब ७५ WP २ ग्रॅम/लिटर पाण्यात मिसळून फवारावे. झाडाची खालची सुकलेली पाने काढून टाकावीत जेणेकरून रोगाचा फैलाव थांबेल.';
        } else if (lower.includes('खत') || lower.includes('fertilizer')) {
          reply =
            'पिकाच्या फुटवे फुटण्याच्या अवस्थेत नत्र (युरिया) आणि स्फुरद यांचा समतोल ठेवा. जमिनीच्या प्रकारानुसार सूक्ष्म अन्नद्रव्ये आणि १९:१९:१९ विद्राव्य खताची फवारणी करावी.';
        } else {
          reply =
            'तुमच्या पिकाची स्थिती आणि लक्षणे लक्षात घेता, शेतात पाण्याचा निचरा योग्य ठेवा आणि सकाळी लवकर प्रतिबंधात्मक जैविक बुरशीनाशकाची फवारणी करा.';
        }
      } else if (language === 'hi') {
        if (lower.includes('टमाटर') || lower.includes('झुलसा') || lower.includes('tomato')) {
          reply =
            'टमाटर में अगेती झुलसा (Early Blight) के लिए मैंकोज़ेब 75 WP @ 2 ग्राम प्रति लीटर पानी का छिड़काव करें। जैविक उपचार के लिए नीम तेल 10,000 PPM 3 मिली/लीटर और ट्राइकोडर्मा विरिडी का प्रयोग बहुत लाभकारी है।';
        } else if (lower.includes('गेहूं') || lower.includes('खाद') || lower.includes('wheat')) {
          reply =
            'गेहूं में कल्ले फूटते समय (20-25 दिन पर) पहली सिंचाई के बाद प्रति एकड़ 30-35 किग्रा यूरिया और जिंक सल्फेट दें। इससे पौधे मजबूत होते हैं और पैदावार बढ़ती है।';
        } else {
          reply =
            'फसल सुरक्षा के लिए खेत में समय पर खरपतवार निकालें और कीटों की निगरानी के लिए पीले चिपचिपे ट्रैप लगाएं। आवश्यकता पड़ने पर अनुशंसित मात्रा में ही छिड़काव करें।';
        }
      } else {
        if (lower.includes('tomato') || lower.includes('blight')) {
          reply =
            'For Tomato Early Blight, apply Mancozeb 75 WP @ 2.0 g/L or Azoxystrobin @ 1 ml/L. Organically, spray 10,000 PPM Neem Oil @ 3 ml/L and prune lower infected leaves to prevent soil splash.';
        } else if (lower.includes('fertilizer') || lower.includes('wheat')) {
          reply =
            'For wheat at crown root initiation and tillering, apply 30-35 kg/acre Urea following the first irrigation. Supplement with Zinc Sulphate 33% @ 5 kg/acre for vigorous vegetative growth.';
        } else {
          reply =
            'Ensure adequate field drainage and apply balanced NPK nutrients based on soil test recommendations. Use IPM sticky traps to monitor early pest populations.';
        }
      }

      return {
        id: 'msg-' + Date.now(),
        sender: 'assistant',
        text: reply,
        timestamp: new Date().toISOString(),
      };
    }
  },
};
