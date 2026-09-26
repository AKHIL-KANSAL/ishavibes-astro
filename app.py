import streamlit as st
import datetime
import calendar
import requests
import base64
import time
from geopy.geocoders import Nominatim
from supabase import create_client

geolocator = Nominatim(user_agent="vedic_astro_portal_full")
st.set_page_config(
    page_title="Vedic Astro Portal | Multilingual", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PORTAL FACELIFT: CUSTOM PALETTE & MODERN WEB STYLING ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Poppins:wght@300;400;500;600&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
    
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1250px !important;
        margin: 0 auto !important;
    }
    
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #AC5633 !important;
        color: #FFFFFF !important;
    }
    
    label, p, span, div {
        color: #FFFFFF !important;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif;
        color: #FFFFFF !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.4);
    }
    
    .portal-header {
        text-align: left;
        padding: 5px 0 10px 0;
    }
    .portal-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 1px;
        line-height: 1.1;
    }
    .portal-subtitle {
        font-size: 0.92rem;
        color: #F3E5AB;
        margin-top: 4px;
    }
    
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        background: rgba(82, 34, 14, 0.7);
        padding: 10px;
        border-radius: 12px;
        border: 1.5px solid #CB8C2F;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stRadio"] label {
        background: rgba(203, 140, 47, 0.25) !important;
        border: 1px solid #CB8C2F !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: #B8860B !important;
        transform: translateY(-2px);
    }
    
    div.stForm, div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"], .stExpander {
        background-color: rgba(203, 140, 47, 0.22) !important;
        border: 1.5px solid #CB8C2F !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(6px);
    }
    
    .stTextInput input, 
    .stSelectbox [data-baseweb="select"], 
    .stSelectbox div[data-baseweb="select"] > div, 
    textarea {
        background-color: #78381D !important;
        color: #F3E5AB !important;
        border: 1.5px solid #CB8C2F !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] * {
        color: #F3E5AB !important;
    }
    
    .stSelectbox svg { 
        fill: #D4AF37 !important; 
    }
    
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] * {
        background-color: #3D180A !important;
        color: #D4AF37 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] ul[role="listbox"] {
        background-color: #3D180A !important;
        border: 1.5px solid #CB8C2F !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6) !important;
    }
    
    div[data-baseweb="popover"] li[role="option"] {
        background-color: #3D180A !important;
        color: #D4AF37 !important;
        padding: 10px 14px !important;
    }

    div[data-baseweb="popover"] li[role="option"] * {
        background-color: transparent !important;
        color: #D4AF37 !important;
    }
    
    div[data-baseweb="popover"] li[role="option"]:hover,
    div[data-baseweb="popover"] li[role="option"]:hover *,
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"],
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"] * {
        background-color: #B8860B !important;
        color: #FFFFFF !important;
    }
    
    .stButton button, div.stFormSubmitButton button {
        background: linear-gradient(135deg, #B8860B 0%, #8A6405 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
    }
    .stButton button:hover, div.stFormSubmitButton button:hover {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }
    
    .badge-shubh {
        background-color: #27ae60;
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-ashubh {
        background-color: #c0392b;
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-neutral {
        background-color: #CB8C2F;
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- REUSABLE DROPDOWN DATE & TIME PICKERS ---
def render_date_dropdowns(label, default_date, key_prefix):
    st.markdown(f"**{label}**")
    c_day, c_month, c_year = st.columns(3)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    with c_day:
        day = st.selectbox("Day", list(range(1, 32)), index=default_date.day - 1, key=f"{key_prefix}_day")
    with c_month:
        month_idx = default_date.month - 1
        month_str = st.selectbox("Month", months, index=month_idx, key=f"{key_prefix}_month")
        month = months.index(month_str) + 1
    with c_year:
        years = list(range(2026, 1919, -1))
        year_default_idx = years.index(default_date.year) if default_date.year in years else 0
        year = st.selectbox("Year", years, index=year_default_idx, key=f"{key_prefix}_year")
        
    max_days = calendar.monthrange(year, month)[1]
    valid_day = min(day, max_days)
    return datetime.date(year, month, valid_day)

def render_time_dropdowns(label, default_time, key_prefix):
    st.markdown(f"**{label}**")
    c_hr, c_min, c_ampm = st.columns(3)
    
    def_hr_12 = default_time.hour % 12
    if def_hr_12 == 0: def_hr_12 = 12
    def_ampm_idx = 0 if default_time.hour < 12 else 1
    
    with c_hr:
        hour_12 = st.selectbox("Hour", list(range(1, 13)), index=def_hr_12 - 1, key=f"{key_prefix}_hr")
    with c_min:
        minute = st.selectbox("Minute", [f"{m:02d}" for m in range(60)], index=default_time.minute, key=f"{key_prefix}_min")
    with c_ampm:
        ampm = st.selectbox("AM/PM", ["AM", "PM"], index=def_ampm_idx, key=f"{key_prefix}_ampm")
        
    h24 = hour_12 % 12
    if ampm == "PM":
        h24 += 12
    return datetime.time(h24, int(minute))

# --- INITIALIZE DATABASE CONNECTION ---
def init_supabase():
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        url = url.replace("/rest/v1/", "").replace("/rest/v1", "").rstrip("/")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

supabase = init_supabase()

# --- SUPABASE RULEBOOK DATABASE FETCHERS ---
def fetch_detailed_interpretation(supabase_client, domain, identifier):
    if not supabase_client:
        return None
    try:
        response = (
            supabase_client.table("detailed_interpretations")
            .select("*")
            .eq("domain", domain)
            .eq("identifier", identifier.lower())
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception:
        pass
    return None

def fetch_rulebook_predictions(supabase_client):
    if not supabase_client:
        return []
    try:
        response = supabase_client.table("rules").select("*").eq("is_active", True).execute()
        if response.data:
            rules_list = []
            for r in response.data:
                rules_list.append({
                    "Name": r.get("title"),
                    "Description": r.get("prediction"),
                    "Nature": "Good" if r.get("effect") == "positive" else ("Bad" if r.get("effect") == "negative" else "Neutral"),
                    "Category": r.get("category")
                })
            return rules_list
    except Exception:
        pass
    return []

def fetch_custom_rudraksha_recommendation(supabase_client, ascendant_sign, running_dasha_name):
    if not supabase_client:
        return None
    try:
        response = supabase_client.table("rudraksha_rules").select("*").eq("is_active", True).execute()
        if response.data:
            rules = response.data
            for r in rules:
                if r["target_ascendant"].lower() == ascendant_sign.lower() and r["target_maha_dasha"].lower() in running_dasha_name.lower():
                    return r
            for r in rules:
                if r["target_ascendant"].lower() == ascendant_sign.lower() and r["target_maha_dasha"].lower() == "all":
                    return r
            for r in rules:
                if r["target_ascendant"].lower() == "all" and r["target_maha_dasha"].lower() in running_dasha_name.lower():
                    return r
    except Exception:
        pass
    return None

def fetch_12_month_forecast(supabase_client, sign_name):
    if not supabase_client:
        return []
    try:
        response = (
            supabase_client.table("monthly_predictions")
            .select("*")
            .eq("zodiac_sign", sign_name.capitalize())
            .order("month_number")
            .execute()
        )
        if response.data:
            return response.data
    except Exception:
        pass
    return []

if "autofill" not in st.session_state:
    st.session_state.autofill = {}
af = st.session_state.autofill

if "planet_cache" not in st.session_state:
    st.session_state.planet_cache = {}

if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- MULTI-LANGUAGE UI DICTIONARY ---
TRANSLATIONS = {
    "English": {
        "pages": ["☀️ Panchang & Daily", "⭐ Kundli & Life Report", "🤖 Deepti Ji (Expert)", "💘 Matchmaking", "⏱️ Muhurtha & Prashna", "🔮 Cosmic Tools", "💾 Saved Profiles", "📿 Lucky Rudraksha"],
        "subtitle": "Authentic Daily Panchang, Astrological Readings & Planetary Transits",
        "sunrise": "Sunrise", "sunset": "Sunset", "tithi": "Tithi (Lunar Day)", "nakshatra": "Nakshatra (Birth Star)",
        "yoga": "Yoga", "vaara": "Vaara (Day)", "daily_title": "Daily Rashifal | Cosmic Outlook",
        "full_name": "Full Name", "city": "City of Birth", "save_btn": "Save to Database",
        "generate_btn": "Generate Complete Horoscope", "lucky_col_label": "Lucky Color"
    },
    "हिन्दी": {
        "pages": ["☀️ पंचांग व दैनिक", "⭐ कुंडली व जीवन रिपोर्ट", "🤖 दीप्ति जी (विशेषज्ञ)", "💘 गुण मिलान", "⏱️ मुहूर्त व प्रश्न", "🔮 वैदिक टूल्स", "💾 सहेजे गए प्रोफाइल", "📿 लकी रुद्राक्ष"],
        "subtitle": "प्रामाणिक दैनिक पंचांग, जन्मकुंडली विश्लेषण एवं ग्रह गोचर",
        "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "tithi": "तिथि", "nakshatra": "नक्षत्र",
        "yoga": "योग", "vaara": "वार (दिन)", "daily_title": "दैनिक राशिफल | आज का भविष्यफल",
        "full_name": "पूरा नाम", "city": "जन्म स्थान / शहर", "save_btn": "प्रोफाइल सहेजें",
        "generate_btn": "संपूर्ण कुंडली प्राप्त करें", "lucky_col_label": "शुभ रंग"
    },
    "தமிழ்": {
        "pages": ["☀️ பஞ்சாங்கம் & பலன்", "⭐ ஜாதகம் & அறிக்கை", "🤖 தீப்தி ஜி", "💘 திருமண பொருத்தம்", "⏱️ முகூர்த்தம் & பிரசன்னம்", "🔮 ஜோதிட கருவிகள்", "💾 சேமிக்கப்பட்டவை", "📿 லக்கி ருத்ராட்சம்"],
        "subtitle": "துல்லியமான பஞ்சாங்கம், ஜாதக பலன்கள் மற்றும் கிரக நிலைகள்",
        "sunrise": "சூரிய உதயம்", "sunset": "சூரிய அஸ்தமனம்", "tithi": "திதி", "nakshatra": "நட்சத்திரம்",
        "yoga": "யோகம்", "vaara": "வாரம்", "daily_title": "தினசரி ராசிபலன்",
        "full_name": "முழு பெயர்", "city": "பிறந்த ஊர்", "save_btn": "சேமிக்கவும்",
        "generate_btn": "முழு ஜாதகம் கணிக்கவும்", "lucky_col_label": "அதிர்ஷ்ட நிறம்"
    },
    "తెలుగు": {
        "pages": ["☀️ పంచాంగం & దినఫలాలు", "⭐ జాతకం & నివేదిక", "🤖 దీప్తి జీ", "💘 జాతక పొంతన", "⏱️ ముహూర్తం & ప్రశ్న", "🔮 జ్యోతిష్య సాధనాలు", "💾 సేవ్ చేసిన ప్రొఫైల్స్", "📿 లక్కీ రుద్రాక్ష"],
        "subtitle": "ప్రామాణిక దిన పంచాంగం, జాతక ఫలితాలు & గోచార స్థితి",
        "sunrise": "సూర్యోదయం", "sunset": "సూర్యాస్తమయం", "tithi": "తిథి", "nakshatra": "నక్షత్రం",
        "yoga": "యోగం", "vaara": "వారం", "daily_title": "దినఫలాలు | రాశి ఫలితాలు",
        "full_name": "పూర్తి పేరు", "city": "పుట్టిన నగరం", "save_btn": "సేవ్ చేయండి",
        "generate_btn": "పూర్తి జాతకం పొందండి", "lucky_col_label": "అదృష్ట రంగు"
    },
    "ಕನ್ನಡ": {
        "pages": ["☀️ ಪಂಚಾಂಗ & ಭವಿಷ್ಯ", "⭐ ಜಾತಕ & ವರದಿ", "🤖 ದೀಪ್ತಿ ಜಿ", "💘 ಗುಣ ಮಿಲನ", "⏱️ ಮುಹೂರ್ತ & ಪ್ರಶ್ನೆ", "🔮 ಜ್ಯೋತಿಷ್ಯ ಪರಿಕರಗಳು", "💾 ಉಳಿಸಿದ ಪ್ರೊಫೈಲ್‌ಗಳು", "📿 ಲಕ್ಕಿ ರುದ್ರಾಕ್ಷಿ"],
        "subtitle": "ದೈನಂದಿನ ಪಂಚಾಂಗ, ಜಾತಕ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಗ್ರಹಗಳ ಚಲನೆ",
        "sunrise": "ಸೂರ್ಯೋದಯ", "sunset": "ಸೂರ್ಯಾಸ್ತ", "tithi": "ತಿಥಿ", "nakshatra": "ನಕ್ಷತ್ರ",
        "yoga": "ಯೋಗ", "vaara": "ವಾರ", "daily_title": "ದಿನ ಭವಿಷ್ಯ | ರಾಶಿ ಫಲ",
        "full_name": "ಪೂರ್ಣ ಹೆಸರು", "city": "ಜನನ ನಗರ", "save_btn": "ಉಳಿಸಿ",
        "generate_btn": "ಸಂಪೂರ್ಣ ಜಾತಕ ಪಡೆಯಿರಿ", "lucky_col_label": "ಅದೃಷ್ಟದ ಬಣ್ಣ"
    },
    "മലയാളം": {
        "pages": ["☀️ പഞ്ചാംഗം & ഫലം", "⭐ ജാതകം & റിപ്പോർട്ട്", "🤖 ദീപ്തി ജി", "💘 പൊരുത്തം", "⏱️ മുഹൂർത്തം & പ്രശ്നം", "🔮 ജ്യോതിഷ ഉപകരണങ്ങൾ", "💾 പ്രൊഫൈലുകൾ", "📿 ലക്കി രുദ്രാക്ഷം"],
        "subtitle": "ദൈനംദിന പഞ്ചാംഗം, ജാതക വിശകലനം, ഗ്രഹനിലകൾ",
        "sunrise": "സൂര്യോദയം", "sunset": "സൂര്യാസ്തമയം", "tithi": "തിഥി", "nakshatra": "നക്ഷത്രം",
        "yoga": "യോഗം", "vaara": "ദിവസം", "daily_title": "പ്രതിദിന രാശിഫലം",
        "full_name": "പൂർണ്ണമായ പേര്", "city": "ജനിച്ച സ്ഥലം", "save_btn": "സേവ് ചെയ്യുക",
        "generate_btn": "ജാതകം പ്രവചിക്കുക", "lucky_col_label": "ഭാഗ്യ നിറം"
    },
    "ગુજરાતી": {
        "pages": ["☀️ પંચાંગ અને રાશિફળ", "⭐ કુંડળી અને રિપોર્ટ", "🤖 દીપ્તિ જી", "💘 ગુણ મિલન", "⏱️ મુહૂર્ત અને પ્રશ્ન", "🔮 જ્યોતિષ ટૂલ્સ", "💾 સાચવેલી પ્રોફાઇલ", "📿 લકી રુદ્રાક્ષ"],
        "subtitle": "વિશ્વાસપાત્ર દૈનિક પંચાંગ, જ્યોતિષ ગણતરીઓ અને રાશિફળ",
        "sunrise": "સૂર્યોદય", "sunset": "સૂર્યાસ્ત", "tithi": "તિથિ", "nakshatra": "નક્ષત્ર",
        "yoga": "યોગ", "vaara": "વાર", "daily_title": "દૈનિક રાશિફળ",
        "full_name": "પૂરું નામ", "city": "જન્મ સ્થળ / શહેર", "save_btn": "સાચવો",
        "generate_btn": "સંપૂર્ણ કુંડળી મેળવો", "lucky_col_label": "શુભ રંગ"
    },
    "मराठी": {
        "pages": ["☀️ पंचांग व राशीभविष्य", "⭐ कुंडली व संपूर्ण अहवाल", "🤖 दीप्ती जी", "💘 गुण मिलन", "⏱️ मुहूर्त व प्रश्न", "🔮 ज्योतिष टूल्स", "💾 सेव्ह केलेल्या प्रोफाइल्स", "📿 लकी रुद्राक्ष"],
        "subtitle": "अचूक दैनिक पंचांग, जन्मकुंडली विश्लेषण आणि ग्रहभ्रमण",
        "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "tithi": "तिथी", "nakshatra": "नक्षत्र",
        "yoga": "योग", "vaara": "वार (दिवस)", "daily_title": "दैनिक राशीभविष्य",
        "full_name": "पूर्ण नाव", "city": "जन्म गाव / शहर", "save_btn": "प्रोफाइल सेव्ह करा",
        "generate_btn": "संपूर्ण कुंडली अहवाल मिळवा", "lucky_col_label": "शुभ रंग"
    },
    "বাংলা": {
        "pages": ["☀️ পঞ্জিকা ও রাশিফল", "⭐ কোষ্ঠী ও জীবন রিপোর্ট", "🤖 দীপ্তি জী", "💘 যোটক বিচার", "⏱️ মুহূর্ত ও প্রশ্ন", "🔮 জ্যোতিষ টুলস", "💾 সংরক্ষিত প্রোফাইল", "📿 লাকি রুদ্রাক্ষ"],
        "subtitle": "নির্ভুল দৈনিক পঞ্জিকা, জন্মকুণ্ডলী বিচার ও জ্যোতিষ পরামর্শ",
        "sunrise": "সূর্যোদয়", "sunset": "সূর্যাস্ত", "tithi": "তিথি", "nakshatra": "নক্ষত্র",
        "yoga": "যোগ", "vaara": "বার (দিন)", "daily_title": "আজকের রাশিফল",
        "full_name": "পুরো নাম", "city": "জন্মস্থান / শহর", "save_btn": "সংরক্ষণ করুন",
        "generate_btn": "সম্পূর্ণ কোষ্ঠী গণনা করুন", "lucky_col_label": "শুভ রং"
    }
}

# --- TOP BRAND HEADER WITH LANGUAGE SELECTOR ---
top_hdr_col, top_lang_col = st.columns([4.2, 1.4])
with top_hdr_col:
    st.markdown(
        f"""
        <div class="portal-header">
            <div class="portal-title">🔱 VEDIC ASTRO PORTAL</div>
            <div class="portal-subtitle">{TRANSLATIONS[st.session_state.lang]['subtitle']}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with top_lang_col:
    languages = list(TRANSLATIONS.keys())
    cur_idx = languages.index(st.session_state.lang) if st.session_state.lang in languages else 0
    selected_lang = st.selectbox("🌐 Language / भाषा", languages, index=cur_idx, key="global_lang_dropdown")
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

current_lang = st.session_state.lang
ui = TRANSLATIONS[current_lang]

# --- DYNAMIC MULTI-LANGUAGE NAVIGATION BAR ---
localized_tabs = ui["pages"]
english_tabs = TRANSLATIONS["English"]["pages"]
tab_map = dict(zip(localized_tabs, english_tabs))

selected_tab_localized = st.radio(
    "Navigation Menu", 
    localized_tabs, 
    horizontal=True, 
    label_visibility="collapsed",
    key=f"nav_menu_{current_lang}"
)
selected_tab = tab_map.get(selected_tab_localized, "☀️ Panchang & Daily")
st.write("")

# --- ISHA VIBES REMEDIES DATABASE ---
def get_remedies(ascendant_sign):
    remedies = {
        "Aries": {"gem": "Certified Red Coral (Moonga)", "gem_img": "https://via.placeholder.com/150/8B0000/FFFFFF?text=Red+Coral", "gem_url": "https://ishavibes.com/products/red-coral", "rudraksha": "3 Mukhi Nepali Rudraksha", "planet": "Mars"},
        "Taurus": {"gem": "Natural White Zircon / Opal", "gem_img": "https://via.placeholder.com/150/F5F5F5/000000?text=Opal", "gem_url": "https://ishavibes.com/products/opal", "rudraksha": "6 Mukhi Nepali Rudraksha", "planet": "Venus"},
        "Gemini": {"gem": "Colombian Emerald (Panna)", "gem_img": "https://via.placeholder.com/150/008000/FFFFFF?text=Emerald", "gem_url": "https://ishavibes.com/products/emerald", "rudraksha": "4 Mukhi Nepali Rudraksha", "planet": "Mercury"},
        "Cancer": {"gem": "Natural Pearl (Moti)", "gem_img": "https://via.placeholder.com/150/FFFAF0/000000?text=Pearl", "gem_url": "https://ishavibes.com/products/pearl", "rudraksha": "2 Mukhi Rudraksha", "planet": "Moon"},
        "Leo": {"gem": "Burmese Ruby (Manik)", "gem_img": "https://via.placeholder.com/150/DC143C/FFFFFF?text=Ruby", "gem_url": "https://ishavibes.com/products/ruby", "rudraksha": "12 Mukhi Surya Rudraksha", "planet": "Sun"},
        "Virgo": {"gem": "Colombian Emerald (Panna)", "gem_img": "https://via.placeholder.com/150/008000/FFFFFF?text=Emerald", "gem_url": "https://ishavibes.com/products/emerald", "rudraksha": "4 Mukhi Nepali Rudraksha", "planet": "Mercury"},
        "Libra": {"gem": "Natural White Zircon / Opal", "gem_img": "https://via.placeholder.com/150/F5F5F5/000000?text=Opal", "gem_url": "https://ishavibes.com/products/opal", "rudraksha": "6 Mukhi Nepali Rudraksha", "planet": "Venus"},
        "Scorpio": {"gem": "Certified Red Coral (Moonga)", "gem_img": "https://via.placeholder.com/150/8B0000/FFFFFF?text=Red+Coral", "gem_url": "https://ishavibes.com/products/red-coral", "rudraksha": "3 Mukhi Nepali Rudraksha", "planet": "Mars"},
        "Sagittarius": {"gem": "Yellow Sapphire (Pukhraj)", "gem_img": "https://via.placeholder.com/150/FFD700/000000?text=Yellow+Sapphire", "gem_url": "https://ishavibes.com/products/yellow-sapphire", "rudraksha": "5 Mukhi Nepali Rudraksha", "planet": "Jupiter"},
        "Capricorn": {"gem": "Blue Sapphire (Neelam)", "gem_img": "https://via.placeholder.com/150/00008B/FFFFFF?text=Blue+Sapphire", "gem_url": "https://ishavibes.com/products/blue-sapphire", "rudraksha": "7 Mukhi Nepali Rudraksha", "planet": "Saturn"},
        "Aquarius": {"gem": "Blue Sapphire (Neelam)", "gem_img": "https://via.placeholder.com/150/00008B/FFFFFF?text=Blue+Sapphire", "gem_url": "https://ishavibes.com/products/blue-sapphire", "rudraksha": "7 Mukhi Nepali Rudraksha", "planet": "Saturn"},
        "Pisces": {"gem": "Yellow Sapphire (Pukhraj)", "gem_img": "https://via.placeholder.com/150/FFD700/000000?text=Yellow+Sapphire", "gem_url": "https://ishavibes.com/products/yellow-sapphire", "rudraksha": "5 Mukhi Nepali Rudraksha", "planet": "Jupiter"}
    }
    for sign in remedies:
        if sign.lower() in str(ascendant_sign).lower(): return remedies[sign]
    return {"gem": "Sphatik Crystal Mala", "gem_img": "https://via.placeholder.com/150/FFFFFF/000000?text=Sphatik", "gem_url": "https://ishavibes.com/products/sphatik-mala", "rudraksha": "5 Mukhi Rudraksha", "planet": "Unknown"}

# --- VEDASTRO MATH & API CALLS ---
def fetch_vedastro(method_path, safe_city, time_str, dd, mm, yyyy):
    url = f"https://api.vedastro.org/api/Calculate/{method_path}/Location/{safe_city}/Time/{time_str}/{dd}/{mm}/{yyyy}/%2B05:30/Ayanamsa/RAMAN"
    try:
        with requests.Session() as s:
            response = s.get(url, timeout=25)
            if response.status_code == 200:
                data = response.json()
                if data.get("Status") == "Pass":
                    payload = data.get("Payload")
                    if isinstance(payload, str): return payload
                    if isinstance(payload, dict):
                        if "Name" in payload: return str(payload["Name"])
                        for key, value in payload.items():
                            if isinstance(value, str): return value
                            if isinstance(value, dict) and "Name" in value: return str(value["Name"])
                    return str(payload)
    except Exception: 
        pass
    return "Data Not Found"

def get_live_daily_panchang(city_name, target_date):
    time_str = "06:00"
    dd, mm, yyyy = target_date.strftime("%d"), target_date.strftime("%m"), target_date.strftime("%Y")
    location = geolocator.geocode(city_name)
    safe_city = location.address.split(",")[0].strip().replace(" ", "%20") if location else "New%20Delhi"
    
    sunrise = fetch_vedastro("Sunrise", safe_city, time_str, dd, mm, yyyy)
    sunset = fetch_vedastro("Sunset", safe_city, time_str, dd, mm, yyyy)
    tithi = fetch_vedastro("Tithi", safe_city, time_str, dd, mm, yyyy)
    nakshatra = fetch_vedastro("PlanetConstellation/PlanetName/Moon", safe_city, time_str, dd, mm, yyyy)
    yoga = fetch_vedastro("NithyaYoga", safe_city, time_str, dd, mm, yyyy)
    
    return {
        "sunrise": sunrise if sunrise != "Data Not Found" else "06:15 AM (Est)",
        "sunset": sunset if sunset != "Data Not Found" else "06:30 PM (Est)",
        "tithi": tithi if tithi != "Data Not Found" else "Shukla Paksha",
        "nakshatra": nakshatra if nakshatra != "Data Not Found" else "Ashwini",
        "yoga": yoga if yoga != "Data Not Found" else "Siddhi"
    }

def fetch_chart_svg(chart_type, safe_city, time_str, dd, mm, yyyy):
    url = f"https://api.vedastro.org/api/Calculate/{chart_type}/Location/{safe_city}/Time/{time_str}/{dd}/{mm}/{yyyy}/%2B05:30/Ayanamsa/RAMAN"
    try:
        with requests.Session() as s:
            response = s.get(url, timeout=30)
            if response.status_code == 200:
                text_data = response.text
                if "<svg" in text_data:
                    if text_data.strip().startswith("{"): return response.json().get("Payload", "")
                    return text_data
    except Exception: 
        pass
    return None

def generate_80_year_timeline(birth_date, nakshatra_name):
    lords = [
        ("Ketu", 7, "Introspection, spiritual growth, sudden breakthroughs, and detachment."),
        ("Venus", 20, "Luxuries, relationships, creative arts, comfort, and financial gains."),
        ("Sun", 6, "Career growth, authority, vitality, government connections, and reputation."),
        ("Moon", 10, "Emotional peace, travel, public dealings, motherly care, and mind balance."),
        ("Mars", 7, "Energy, property acquisition, technical pursuits, drive, and physical vitality."),
        ("Rahu", 18, "Ambition, foreign travels, sudden material expansion, and unconventional success."),
        ("Jupiter", 16, "Wisdom, higher education, expansion, and prosperity."),
        ("Saturn", 19, "Discipline, hard work, karmic balancing, long-term career foundations."),
        ("Mercury", 17, "Intellect, business ventures, communication skills, and commercial success.")
    ]
    nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Satabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    clean_nak = "Ashwini"
    for n in nakshatras:
        if n.lower() in nakshatra_name.lower():
            clean_nak = n
            break
    start_idx = (nakshatras.index(clean_nak) // 3) % 9
    ordered_lords = lords[start_idx:] + lords[:start_idx]
    
    timeline = []
    current_age = 0
    birth_year = birth_date.year
    
    for planet, duration, theme in ordered_lords:
        if current_age >= 80: break
        end_age = min(current_age + duration, 80)
        start_cal_year = birth_year + current_age
        end_cal_year = birth_year + end_age
        timeline.append({
            "Planet": planet,
            "Period": f"{planet} Maha Dasha", 
            "Start_Age": current_age,
            "End_Age": end_age, 
            "Start_Year": start_cal_year,
            "End_Year": end_cal_year, 
            "Theme": theme
        })
        current_age = end_age
    return timeline

# ==========================================
# VIEW 1: PANCHANG TODAY & 12-RASHI GRID (HOME)
# ==========================================
if selected_tab == "☀️ Panchang & Daily":
    today_date = datetime.date.today()
    
    col_hdr, col_city = st.columns([2, 1])
    with col_hdr:
        st.markdown(f"### 🗓️ {today_date.strftime('%d %B %Y')}")
    with col_city:
        p_city = st.text_input(f"📍 {ui['city']}", value=af.get("city", "Roorkee"), key="panch_city")

    with st.spinner(f"📡 Fetching Live Planetary Data for {p_city}..."):
        live_panchang = get_live_daily_panchang(p_city, today_date)
    
    st.markdown("### 🌅 Surya Timings")
    c1, c2 = st.columns(2)
    c1.metric(f"☀️ {ui['sunrise']}", live_panchang["sunrise"])
    c2.metric(f"🌇 {ui['sunset']}", live_panchang["sunset"])
    
    st.divider()
    
    st.subheader(f"📜 Today's Cosmic Alignments (Live)")
    with st.container(border=True):
        st.markdown(f"**{ui['tithi']}:** {live_panchang['tithi']}")
        st.markdown("---")
        st.markdown(f"**{ui['nakshatra']}:** {live_panchang['nakshatra']}")
        st.markdown("---")
        st.markdown(f"**{ui['yoga']}:** {live_panchang['yoga']}")

    st.divider()
    
    # --- DYNAMIC MULTILINGUAL RASHIFAL ENGINE ---
    st.header(f"🔮 {ui['daily_title']} ({today_date.strftime('%d %b %Y')})")
    
    rashi_meta = [
        ("Aries", "मेष", "Crimson Red", "लाल", "Energetic momentum favors bold initiatives. Direct your drive toward key milestones.", "आज ऊर्जा और पराक्रम में वृद्धि होगी। महत्वपूर्ण निर्णय लेने के लिए दिन शुभ है।"),
        ("Taurus", "वृषभ", "Emerald Green", "हरा", "Financial stability and tactical patience yield steady progress. Avoid impulse spending.", "आर्थिक स्थिरता बनी रहेगी। धैर्य से काम लें और अनावश्यक खर्चों से बचें।"),
        ("Gemini", "मिथुन", "Canary Yellow", "पीला", "Analytical acuity and negotiations are highlighted. Ensure clarity in communication.", "बुद्धि और बातचीत से बिगड़े काम बनेंगे। नई योजनाओं पर ध्यान केंद्रित करें।"),
        ("Cancer", "कर्क", "Pearl White", "सफेद", "Intuitive clarity guides domestic harmony. Guard against emotional fatigue.", "पारिवारिक सुख में वृद्धि होगी। अपनी भावनाओं पर नियंत्रण रखें और शांति बनाए रखें।"),
        ("Leo", "सिंह", "Royal Gold", "सुनहरा", "Natural authority commands respect in professional dealings. Lead with poise.", "कार्यक्षेत्र में मान-सम्मान बढ़ेगा। नेतृत्व क्षमता का पूरा लाभ मिलेगा।"),
        ("Virgo", "कन्या", "Forest Green", "गहरा हरा", "Precision planning resolves complex bottlenecks. Prioritize physical wellbeing.", "योजनाबद्ध तरीके से काम करने से सफलता मिलेगी। स्वास्थ्य के प्रति सचेत रहें।"),
        ("Libra", "तुला", "Pastel Pink", "गुलाबी", "Diplomatic balance restores equilibrium in partnerships. Fair compromises succeed.", "साझेदारी और रिश्तों में सामंजस्य रहेगा। कला और सौंदर्य में रुचि बढ़ेगी।"),
        ("Scorpio", "वृश्चिक", "Deep Maroon", "मैरून", "Strategic determination penetrates obstacles. Focus on confidential, deep work.", "गूढ़ विषयों और गोपनीय योजनाओं में सफलता मिलेगी। एकाग्रता बनाए रखें।"),
        ("Sagittarius", "धनु", "Bright Saffron", "केसरिया", "Expansive foresight supports learning and commercial strategy. Stay grounded.", "भाग्य का साथ मिलेगा। धर्म और ज्ञान के क्षेत्र में रुचि बढ़ेगी।"),
        ("Capricorn", "मकर", "Navy Blue", "नीला", "Methodical perseverance brings recognition from superiors. Build enduring structures.", "कड़ी मेहनत का फल मिलेगा। कार्यक्षेत्र में वरिष्ठों का सहयोग प्राप्त होगा।"),
        ("Aquarius", "कुंभ", "Electric Cyan", "हल्का नीला", "Innovative networking unlocks progressive opportunities. Collaborate with peers.", "नए विचार और संपर्क लाभदायक सिद्ध होंगे। मित्रों का सहयोग मिलेगा।"),
        ("Pisces", "मीन", "Sea Green", "समुद्री हरा", "Creative empathy and spiritual reflections balance demands. Trust inner instincts.", "आत्मिक शांति और रचनात्मक कार्यों में सफलता मिलेगी। अपने अंतर्मन की सुनें।")
    ]
    
    today_str = today_date.strftime("%Y-%m-%d")
    today_nakshatra = live_panchang.get("nakshatra", "Shubh Star")
    
    # 3-column responsive grid with native Hindi & English rendering
    for i in range(0, 12, 3):
        cols = st.columns(3)
        for j in range(3):
            eng_name, hi_name, eng_col, hi_col, eng_pred, hi_pred = rashi_meta[i+j]
            with cols[j]:
                with st.container(border=True):
                    if current_lang == "हिन्दी":
                        st.subheader(f"✨ {hi_name} ({eng_name})")
                        st.write(f"{hi_pred} आज {today_nakshatra} नक्षत्र के प्रभाव से कार्य में सफलता मिलेगी।")
                        st.info(f"**{ui['lucky_col_label']}:** {hi_col}")
                    else:
                        st.subheader(f"✨ {eng_name}")
                        st.write(f"{eng_pred} Influenced positively by today's {today_nakshatra} alignment.")
                        st.info(f"**{ui['lucky_col_label']}:** {eng_col}")

# ==========================================
# VIEW 2: KUNDLI & LIFE REPORT
# ==========================================
elif selected_tab == "⭐ Kundli & Life Report":
    st.title(f"⭐ {ui['pages'][1]}")
    chart_style = st.radio("Select Chart Style", ["North Indian", "South Indian"], horizontal=True)
    
    with st.form("birth_details_form"):
        name = st.text_input(ui["full_name"], value=af.get("name", ""))
        birth_date = render_date_dropdowns("Date of Birth", af.get("dob", datetime.date(1995, 1, 1)), "horo_b")
        birth_time = render_time_dropdowns("Time of Birth", af.get("tob", datetime.time(10, 0)), "horo_b")
        city = st.text_input(ui["city"], value=af.get("city", ""))
        submitted = st.form_submit_button(ui["generate_btn"])

    if submitted and name and city:
        location = geolocator.geocode(city)
        if location:
            safe_city = location.address.split(",")[0].strip().replace(" ", "%20")
            time_str = birth_time.strftime("%H:%M")
            dd, mm, yyyy = birth_date.strftime("%d"), birth_date.strftime("%m"), birth_date.strftime("%Y")
            
            with st.spinner("Computing planetary coordinates via VedAstro & Supabase..."):
                try:
                    sun_sign = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Sun", safe_city, time_str, dd, mm, yyyy)
                    moon_sign = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_city, time_str, dd, mm, yyyy)
                    ascendant = fetch_vedastro("HouseSignName/HouseName/House1", safe_city, time_str, dd, mm, yyyy)
                    nakshatra = fetch_vedastro("PlanetConstellation/PlanetName/Moon", safe_city, time_str, dd, mm, yyyy)
                    method_name = "NorthIndianChart" if chart_style == "North Indian" else "SouthIndianChart"
                    d1_svg = fetch_chart_svg(method_name, safe_city, time_str, dd, mm, yyyy)
                    remedy = get_remedies(ascendant)

                    st.session_state.generated_report_data = {
                        "name": name, "ascendant": ascendant, "moon_sign": moon_sign,
                        "nakshatra": nakshatra, "sun_sign": sun_sign, "d1_svg": d1_svg,
                        "remedy": remedy, "birth_date": birth_date
                    }
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")

    if "generated_report_data" in st.session_state:
        rep = st.session_state.generated_report_data
        name, ascendant, moon_sign = rep["name"], rep["ascendant"], rep["moon_sign"]
        nakshatra, sun_sign, d1_svg = rep["nakshatra"], rep["sun_sign"], rep["d1_svg"]
        remedy, birth_date = rep["remedy"], rep["birth_date"]

        st.divider()
        st.header(f"🔮 {name}'s General Astro Data")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Ascendant (Lagna)", ascendant)
        col_b.metric("Moon Sign (Rasi)", moon_sign)
        col_c.metric("Birth Star (Nakshatra)", nakshatra)
        
        if d1_svg:
            st.divider()
            st.subheader("D1 Birth Chart")
            b64_d1 = base64.b64encode(d1_svg.encode('utf-8')).decode('utf-8')
            st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/svg+xml;base64,{b64_d1}" style="max-width: 100%; height: auto; border-radius: 8px;"></div>', unsafe_allow_html=True)

        st.divider()
        st.header("📜 80-Year Vimshottari Dasha Lifecycle & Remedies")
        timeline_data = generate_80_year_timeline(birth_date, nakshatra)
        
        for item in timeline_data:
            planet_name = item['Planet'].lower()
            with st.expander(f"✨ {item['Period']} (Age {item['Start_Age']} to {item['End_Age']} | Years: {item['Start_Year']} - {item['End_Year']})"):
                st.write(f"**Core Planetary Theme:** {item['Theme']}")
                if supabase:
                    planet_db_info = fetch_detailed_interpretation(supabase, "planet", planet_name)
                    if planet_db_info:
                        st.markdown(f"**🌟 What to Expect:** {planet_db_info.get('interactive_summary', '')}")
                        st.info(f"**📿 Recommended Remedy for this Phase:** {planet_db_info.get('remedial_guidance', '')}")

# ==========================================
# VIEW 3: DEEPTI JI (DATABASE-DRIVEN ADVISOR)
# ==========================================
elif selected_tab == "🤖 Deepti Ji (Expert)":
    st.title(f"🤖 {ui['pages'][2]}")
    st.write("Consult Deepti Ji using direct answers retrieved from your Supabase astrological rulebook database.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form("profile_lock_form"):
        st.subheader("Step 1: Set Your Birth Profile for Consultation")
        p_name = st.text_input(ui["full_name"], value=af.get("name", ""))
        p_date = render_date_dropdowns("Date of Birth", af.get("dob", datetime.date(1995, 1, 1)), "ai_astro")
        p_time = render_time_dropdowns("Time of Birth", af.get("tob", datetime.time(10, 0)), "ai_astro")
        p_city = st.text_input(ui["city"], value=af.get("city", ""))
        profile_submitted = st.form_submit_button("Lock Profile & Start Consultation")

    if profile_submitted and p_name and p_city:
        loc = geolocator.geocode(p_city)
        if loc:
            safe_c = loc.address.split(",")[0].strip().replace(" ", "%20")
            time_s = p_time.strftime("%H:%M")
            dd_s, mm_s, yyyy_s = p_date.strftime("%d"), p_date.strftime("%m"), p_date.strftime("%Y")
            with st.spinner("Reviewing your chart..."):
                asc = fetch_vedastro("HouseSignName/HouseName/House1", safe_c, time_s, dd_s, mm_s, yyyy_s)
                moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                consult_preds = fetch_rulebook_predictions(supabase)
            st.session_state.profile = {"name": p_name, "ascendant": asc, "moon": moon, "preds": consult_preds}
            st.session_state.messages = []
            st.success(f"Profile locked! Lagna: {asc}. Deepti Ji is ready!")

    if "profile" in st.session_state:
        st.divider()
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_query := st.chat_input("Ask Deepti Ji about career, marriage, or financial stability..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            prof = st.session_state.profile
            with st.chat_message("assistant"):
                query_lower = user_query.lower()
                matched_rule = next((r for r in prof['preds'] if any(kw in r['Name'].lower() or kw in r['Description'].lower() for kw in query_lower.split() if len(kw) > 3)), None)
                
                if matched_rule:
                    resp_text = f"Namaste {prof['name']}! Consulting your chart under {prof['ascendant']} Lagna:\n\n**{matched_rule['Name']}**\n> {matched_rule['Description']}"
                else:
                    resp_text = f"Namaste {prof['name']}! Based on your {prof['ascendant']} Ascendant, your chart exhibits balanced planetary stability. Focus on disciplined, structured actions."
                st.markdown(resp_text)
            st.session_state.messages.append({"role": "assistant", "content": resp_text})

# ==========================================
# VIEW 4: LUCKY RUDRAKSHA REPORT
# ==========================================
elif selected_tab == "📿 Lucky Rudraksha":
    st.title("📿 Lucky Rudraksha Report")
    st.write("Unlock Your Destiny with personalized Rudraksha recommendations based on your planetary alignments.")
    
    with st.form("rudraksha_form"):
        st.subheader("Enter Details for Your Custom Report")
        c1, c2 = st.columns(2)
        with c1:
            r_name = st.text_input(ui["full_name"], value=af.get("name", "AKHIL"))
            r_city = st.text_input(ui["city"], value=af.get("city", "ROORKEE, UTTARAKHAND"))
        with c2:
            r_date = render_date_dropdowns("Date of Birth", af.get("dob", datetime.date(1981, 1, 13)), "rud_d")
            r_time = render_time_dropdowns("Time of Birth", af.get("tob", datetime.time(20, 10)), "rud_t")
        
        submitted = st.form_submit_button("Generate Lucky Rudraksha Report")
        
    if submitted:
        loc = geolocator.geocode(r_city)
        safe_c = loc.address.split(",")[0].strip().replace(" ", "%20") if loc else "Roorkee"
        time_s = r_time.strftime("%H:%M")
        dd_s, mm_s, yyyy_s = r_date.strftime("%d"), r_date.strftime("%m"), r_date.strftime("%Y")
        
        with st.spinner("Analyzing your birth chart for personalized recommendations..."):
            r_asc = fetch_vedastro("HouseSignName/HouseName/House1", safe_c, time_s, dd_s, mm_s, yyyy_s)
            r_moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
            personal_remedy = get_remedies(r_asc)
            
        st.divider()
        st.markdown(f'''
            <div style="background-color: #3D180A; padding: 20px; border-radius: 10px; border: 2px solid #CB8C2F; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                <h2 style="text-align: center; color: #D4AF37; margin-bottom: 0px;">LUCKY RUDRAKSHA REPORT</h2>
                <h4 style="text-align: center; color: #F3E5AB; margin-top: 5px;">Unlock Your Destiny</h4>
                <hr style="border-color: #CB8C2F;">
                <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                    <div style="min-width: 200px;">
                        <p><strong>Name:</strong> {r_name}</p>
                        <p><strong>Date of Birth:</strong> {r_date.strftime("%d %B %Y")}</p>
                        <p><strong>Time of Birth:</strong> {r_time.strftime("%I:%M %p")}</p>
                        <p><strong>Place of Birth:</strong> {r_city}</p>
                    </div>
                    <div style="min-width: 200px;">
                        <p><strong>Ascendant (Lagna):</strong> {r_asc}</p>
                        <p><strong>Moon Sign (Rasi):</strong> {r_moon}</p>
                        <p><strong>Ruling Planet:</strong> {personal_remedy.get('planet', 'Mars')}</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.write("")
        st.header(f"🌟 Your Primary Life Rudraksha (For {r_asc} Lagna)")
        st.success(f"**✨ Recommended: {personal_remedy['rudraksha']}**")
        st.write(f"Because your ruling planet is **{personal_remedy['planet']}**, this is your foundational bead for life success and clearing karmic blockages.")
        
        st.divider()
        st.header("❤️ Relationship & Emotional Balance")
        st.info("**✨ Recommended for Love Balance: 2 Mukhi Rudraksha**")
        st.write("The 2 Mukhi is the bead of union (Ardhanarishvara), balancing emotions, forgiveness, and relationships.")

        st.divider()
        st.header("🧠 Mental Fatigue & Anxiety")
        st.info("**✨ Recommended for Health Balance: Nirakar Rudraksha**")
        st.write("Brings deep serenity, dispels anxiety, and keeps mental energy light and centered.")
        
        st.divider()
        st.header("🛡️ Care Instructions")
        m1, m2, m3, m4 = st.columns(4)
        m1.success("🚿 Remove before bathing")
        m2.success("💪 Remove before gym")
        m3.success("🧴 Oil once a month (Almond Oil)")
        m4.error("❌ Never wash with soap")
        
        st.divider()
        st.markdown("<p style='text-align: center; color: #F3E5AB;'><em>Report curated by the experts at ishavibes.com</em></p>", unsafe_allow_html=True)
        
        st.html(
            """
            <div style="text-align: center; margin-top: 10px;">
                <button onclick="window.parent.print()" style="background: linear-gradient(135deg, #B8860B 0%, #8A6405 100%); color: #FFFFFF; font-family: 'Poppins', sans-serif; font-weight: 600; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.4); padding: 0.8rem 1.5rem; cursor: pointer; font-size: 16px;">
                    🖨️ Download / Print as PDF
                </button>
            </div>
            """
        )

# ==========================================
# VIEW 5, 6, 7: PLACEHOLDER ROUTING
# ==========================================
elif selected_tab in ["💘 Matchmaking", "⏱️ Muhurtha & Prashna", "🔮 Cosmic Tools", "💾 Saved Profiles"]:
    st.title(f"{selected_tab}")
    st.info(f"The module for {selected_tab} is active and ready for data entry.")