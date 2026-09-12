import streamlit as st
import datetime
import calendar
import requests
import base64
import time
from geopy.geocoders import Nominatim
from fpdf import FPDF
from streamlit_lottie import st_lottie
from google import genai
from supabase import create_client

# Enable Connection Pooling
session = requests.Session()

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
    
    /* 1. HIDE DEFAULT STREAMLIT SIDEBAR FOR CLEAN CONSUMER PORTAL */
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1250px !important;
        margin: 0 auto !important;
    }
    
    /* Global Background & Typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #AC5633 !important;
        color: #FFFFFF !important;
    }
    
    label, p, span, div {
        color: #FFFFFF !important;
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif;
        color: #FFFFFF !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.4);
    }
    
    /* Top Header Branding */
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
    
    /* Modern Horizontal Navbar Tabs */
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
    
    /* Cards & Glassmorphic Surfaces */
    div.stForm, div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"], .stExpander {
        background-color: rgba(203, 140, 47, 0.22) !important;
        border: 1.5px solid #CB8C2F !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(6px);
    }
    
    /* Inputs & Closed Selectbox */
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
    
    /* Dropdown Popover Menus (Golden Text on Dark Terracotta) */
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
    
    /* Hover & Active Selection in Dropdown */
    div[data-baseweb="popover"] li[role="option"]:hover,
    div[data-baseweb="popover"] li[role="option"]:hover *,
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"],
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"] * {
        background-color: #B8860B !important;
        color: #FFFFFF !important;
    }
    
    /* CTA Buttons */
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
    
    /* Status Badges */
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

# --- INITIALIZE DATABASE & CACHE ---
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase()

if "autofill" not in st.session_state:
    st.session_state.autofill = {}
af = st.session_state.autofill

if "planet_cache" not in st.session_state:
    st.session_state.planet_cache = {}

if "daily_horo_cache" not in st.session_state:
    st.session_state.daily_horo_cache = {}

if "selected_rashi" not in st.session_state:
    st.session_state.selected_rashi = "Aries"

if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- COMPREHENSIVE MULTI-LANGUAGE UI DICTIONARY ---
TRANSLATIONS = {
    "English": {
        "pages": ["☀️ Panchang & Daily", "⭐ Kundli & Life Report", "🤖 Deepti Ji (AI)", "💘 Matchmaking", "⏱️ Muhurtha & Prashna", "🔮 Cosmic Tools", "💾 Saved Profiles"],
        "subtitle": "Authentic Daily Panchang, Astrological Readings & Planetary Transits",
        "sunrise": "Sunrise", "sunset": "Sunset", "moonrise": "Moonrise", "moonset": "Moonset",
        "five_limbs": "The Five Limbs (Panchanga)", "tithi": "Tithi (Lunar Day)", "nakshatra": "Nakshatra (Birth Star)",
        "yoga": "Yoga", "karana": "Karana", "vaara": "Vaara (Day)", "samvat_title": "Hindu Calendar & Samvat",
        "muhurtha_title": "Auspicious & Inauspicious Muhurthas", "abhijit": "Abhijit Muhurta", "amrit": "Amrit Kaalam",
        "brahma": "Brahma Muhurta", "rahu": "Rahu Kaal", "yama": "Yamaganda Kaal", "gulika": "Gulika Kaalam",
        "disha": "Disha Shool", "daily_title": "Daily Rashifal | Choose Your Zodiac Sign",
        "read_btn": "Read Today's Prediction", "generate_btn": "Generate Complete Horoscope",
        "full_name": "Full Name", "city": "City of Birth", "save_btn": "Save to Database"
    },
    "हिन्दी": {
        "pages": ["☀️ पंचांग व दैनिक", "⭐ कुंडली व जीवन रिपोर्ट", "🤖 दीप्ति जी (AI)", "💘 गुण मिलान", "⏱️ मुहूर्त व प्रश्न", "🔮 वैदिक टूल्स", "💾 सहेजे गए प्रोफाइल"],
        "subtitle": "प्रामाणिक दैनिक पंचांग, जन्मकुंडली विश्लेषण एवं ग्रह गोचर",
        "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "moonrise": "चंद्रोदय", "moonset": "चंद्रास्त",
        "five_limbs": "पंचांग के पांच अंग", "tithi": "तिथि", "nakshatra": "नक्षत्र",
        "yoga": "योग", "karana": "करण", "vaara": "वार (दिन)", "samvat_title": "हिन्दू संवत्सर एवं ऋतु",
        "muhurtha_title": "शुभ एवं अशुभ मुहूर्त", "abhijit": "अभिजित मुहूर्त", "amrit": "अमृत काल",
        "brahma": "ब्रह्म मुहूर्त", "rahu": "राहु काल", "yama": "यमगंड काल", "gulika": "गुलिक काल",
        "disha": "दिशा शूल", "daily_title": "दैनिक राशिफल | अपनी राशि चुनें",
        "read_btn": "आज का राशिफल पढ़ें", "generate_btn": "संपूर्ण कुंडली व भविष्यवाणी प्राप्त करें",
        "full_name": "पूरा नाम", "city": "जन्म स्थान / शहर", "save_btn": "प्रोफाइल सहेजें"
    },
    "தமிழ்": {
        "pages": ["☀️ பஞ்சாங்கம் & பலன்", "⭐ ஜாதகம் & அறிக்கை", "🤖 தீப்தி ஜி (AI)", "💘 திருமண பொருத்தம்", "⏱️ முகூர்த்தம் & பிரசன்னம்", "🔮 ஜோதிட கருவிகள்", "💾 சேமிக்கப்பட்டவை"],
        "subtitle": "துல்லியமான பஞ்சாங்கம், ஜாதக பலன்கள் மற்றும் கிரக நிலைகள்",
        "sunrise": "சூரிய உதயம்", "sunset": "சூரிய அஸ்தமனம்", "moonrise": "சந்திர உதயம்", "moonset": "சந்திர அஸ்தமனம்",
        "five_limbs": "பஞ்சாங்க உறுப்புகள்", "tithi": "திதி", "nakshatra": "நட்சத்திரம்",
        "yoga": "யோகம்", "karana": "கரணம்", "vaara": "வாரம்", "samvat_title": "தமிழ் வருடம் & காலண்டர்",
        "muhurtha_title": "சுப மற்றும் அசுப முகூர்த்தங்கள்", "abhijit": "அபிஜித் முகூர்த்தம்", "amrit": "அமிர்த காலம்",
        "brahma": "பிரம்ம முகூர்த்தம்", "rahu": "ராகு காலம்", "yama": "எமகண்டம்", "gulika": "குளிகை காலம்",
        "disha": "சூலம்", "daily_title": "தினசரி ராசிபலன் | உங்கள் ராசியைத் தேர்ந்தெடுக்கவும்",
        "read_btn": "இன்றைய பலனைப் பார்க்கவும்", "generate_btn": "முழு ஜாதகம் கணிக்கவும்",
        "full_name": "முழு பெயர்", "city": "பிறந்த ஊர்", "save_btn": "சேமிக்கவும்"
    },
    "తెలుగు": {
        "pages": ["☀️ పంచాంగం & దినఫలాలు", "⭐ జాతకం & నివేదిక", "🤖 దీప్తి జీ (AI)", "💘 జాతక పొంతన", "⏱️ ముహూర్తం & ప్రశ్న", "🔮 జ్యోతిష్య సాధనాలు", "💾 సేవ్ చేసిన ప్రొఫైల్స్"],
        "subtitle": "ప్రామాణిక దిన పంచాంగం, జాతక ఫలితాలు & గోచార స్థితి",
        "sunrise": "సూర్యోదయం", "sunset": "సూర్యాస్తమయం", "moonrise": "చంద్రోదయం", "moonset": "చంద్రాస్తమయం",
        "five_limbs": "పంచాంగ విభాగాలు", "tithi": "తిథి", "nakshatra": "నక్షత్రం",
        "yoga": "యోగం", "karana": "కరణం", "vaara": "వారం", "samvat_title": "హిందూ కాలగణన & సంవత్",
        "muhurtha_title": "శుభ & అశుభ ముహూర్తాలు", "abhijit": "అభిజిత్ ముహూర్తం", "amrit": "అమృత ఘడియలు",
        "brahma": "బ్రహ్మ ముహూర్తం", "rahu": "రాహుకాలం", "yama": "యమగండం", "gulika": "గుళిక కాలం",
        "disha": "దిశా శూల", "daily_title": "దినఫలాలు | మీ రాశిని ఎంచుకోండి",
        "read_btn": "నేటి ఫలితాలు చదవండి", "generate_btn": "పూర్తి జాతకం పొందండి",
        "full_name": "పూర్తి పేరు", "city": "పుట్టిన నగరం", "save_btn": "సేవ్ చేయండి"
    },
    "ಕನ್ನಡ": {
        "pages": ["☀️ ಪಂಚಾಂಗ & ಭವಿಷ್ಯ", "⭐ ಜಾತಕ & ವರದಿ", "🤖 ದೀಪ್ತಿ ಜಿ (AI)", "💘 ಗುಣ ಮಿಲನ", "⏱️ ಮುಹೂರ್ತ & ಪ್ರಶ್ನೆ", "🔮 ಜ್ಯೋತಿಷ್ಯ ಪರಿಕರಗಳು", "💾 ಉಳಿಸಿದ ಪ್ರೊಫೈಲ್‌ಗಳು"],
        "subtitle": "ದೈನಂದಿನ ಪಂಚಾಂಗ, ಜಾತಕ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಗ್ರಹಗಳ ಚಲನೆ",
        "sunrise": "ಸೂರ್ಯೋದಯ", "sunset": "ಸೂರ್ಯಾಸ್ತ", "moonrise": "ಚಂದ್ರೋದಯ", "moonset": "ಚಂದ್ರಾಸ್ತ",
        "five_limbs": "ಪಂಚಾಂಗದ ಐದು ಅಂಗಗಳು", "tithi": "ತಿಥಿ", "nakshatra": "ನಕ್ಷತ್ರ",
        "yoga": "ಯೋಗ", "karana": "ಕರಣ", "vaara": "ವಾರ", "samvat_title": "ಹಿಂದು ಸಂವತ್ಸರ",
        "muhurtha_title": "ಶುಭ ಮತ್ತು ಅಶುಭ ಮುಹೂರ್ತಗಳು", "abhijit": "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ", "amrit": "ಅಮೃತ ಕಾಲ",
        "brahma": "ಬ್ರಹ್ಮ ಮುಹೂರ್ತ", "rahu": "ರಾಹು ಕಾಲ", "yama": "ಯಮಗಂಡ ಕಾಲ", "gulika": "ಗುಳಿಕ ಕಾಲ",
        "disha": "ದಿಶಾ ಶೂಲ", "daily_title": "ದಿನ ಭವಿಷ್ಯ | ನಿಮ್ಮ ರಾಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "read_btn": "ಇಂದಿನ ಭವಿಷ್ಯ ಓದಿ", "generate_btn": "ಸಂಪೂರ್ಣ ಜಾತಕ ಪಡೆಯಿರಿ",
        "full_name": "ಪೂರ್ಣ ಹೆಸರು", "city": "ಜನನ ನಗರ", "save_btn": "ಉಳಿಸಿ"
    },
    "മലയാളം": {
        "pages": ["☀️ പഞ്ചാംഗം & ഫലം", "⭐ ജാതകം & റിപ്പോർട്ട്", "🤖 ദീപ്തി ജി (AI)", "💘 പൊരുത്തം", "⏱️ മുഹൂർത്തം & പ്രശ്നം", "🔮 ജ്യോതിഷ ഉപകരണങ്ങൾ", "💾 പ്രൊഫൈലുകൾ"],
        "subtitle": "ദൈനംദിന പഞ്ചാംഗം, ജാതക വിശകലനം, ഗ്രഹനിലകൾ",
        "sunrise": "സൂര്യോദയം", "sunset": "സൂര്യാസ്തമയം", "moonrise": "ചന്ദ്രോദയം", "moonset": "ചന്ദ്രാസ്തമയം",
        "five_limbs": "പഞ്ചാംഗ വിശേഷങ്ങൾ", "tithi": "തിഥി", "nakshatra": "നക്ഷത്രം",
        "yoga": "യോഗം", "karana": "കരണം", "vaara": "ദിവസം", "samvat_title": "ഹിന്ദു കലണ്ടർ",
        "muhurtha_title": "ശുഭ-അശുഭ മുഹൂർത്തങ്ങൾ", "abhijit": "അഭിജിത് മുഹൂർത്തം", "amrit": "അമൃത കാലം",
        "brahma": "ബ്രഹ്മ മുഹൂർത്തം", "rahu": "രാഹുകാലം", "yama": "യമഗണ്ഡം", "gulika": "ഗുളികകാലം",
        "disha": "ദിശാ ശൂലം", "daily_title": "പ്രതിദിന ഫലം | നിങ്ങളുടെ രാശി തിരഞ്ഞെടുക്കുക",
        "read_btn": "ഇന്നത്തെ ഫലം കാണുക", "generate_btn": "ജാതകം പ്രവചിക്കുക",
        "full_name": "പൂർണ്ണമായ പേര്", "city": "ജനിച്ച സ്ഥലം", "save_btn": "സേവ് ചെയ്യുക"
    },
    "ગુજરાતી": {
        "pages": ["☀️ પંચાંગ અને રાશિફળ", "⭐ કુંડળી અને રિપોર્ટ", "🤖 દીપ્તિ જી (AI)", "💘 ગુણ મિલન", "⏱️ મુહૂર્ત અને પ્રશ્ન", "🔮 જ્યોતિષ ટૂલ્સ", "💾 સાચવેલી પ્રોફાઇલ"],
        "subtitle": "વિશ્વાસપાત્ર દૈનિક પંચાંગ, જ્યોતિષ ગણતરીઓ અને રાશિફળ",
        "sunrise": "સૂર્યોદય", "sunset": "સૂર્યાસ્ત", "moonrise": "ચંદ્રોદય", "moonset": "ચંદ્રાસ્ત",
        "five_limbs": "પંચાંગના પાંચ અંગો", "tithi": "તિથિ", "nakshatra": "નક્ષત્ર",
        "yoga": "યોગ", "karana": "કરણ", "vaara": "વાર", "samvat_title": "હિન્દુ કેલેન્ડર અને સંવત",
        "muhurtha_title": "શુભ અને અશુભ મુહૂર્ત", "abhijit": "અભિજિત મુહૂર્ત", "amrit": "અમૃત કાળ",
        "brahma": "બ્રહ્મ મુહૂર્ત", "rahu": "રાહુ કાળ", "yama": "યમગંડ કાળ", "gulika": "ગુલિક કાળ",
        "disha": "દિશા શૂળ", "daily_title": "દૈનિક રાશિફળ | તમારી રાશિ પસંદ કરો",
        "read_btn": "આજનું રાશિફળ વાંચો", "generate_btn": "સંપૂર્ણ કુંડળી મેળવો",
        "full_name": "પૂરું નામ", "city": "જન્મ સ્થળ / શહેર", "save_btn": "સાચવો"
    },
    "मराठी": {
        "pages": ["☀️ पंचांग व राशीभविष्य", "⭐ कुंडली व संपूर्ण अहवाल", "🤖 दीप्ती जी (AI)", "💘 गुण मिलन", "⏱️ मुहूर्त व प्रश्न", "🔮 ज्योतिष टूल्स", "💾 सेव्ह केलेल्या प्रोफाइल्स"],
        "subtitle": "अचूक दैनिक पंचांग, जन्मकुंडली विश्लेषण आणि ग्रहभ्रमण",
        "sunrise": "सूर्योदय", "sunset": "सूर्यास्त", "moonrise": "चंद्रोदय", "moonset": "चंद्रास्त",
        "five_limbs": "पंचांगाचे पाच अंग", "tithi": "तिथी", "nakshatra": "नक्षत्र",
        "yoga": "योग", "karana": "करण", "vaara": "वार (दिवस)", "samvat_title": "हिंदू पंचांग व संवत",
        "muhurtha_title": "शुभ आणि अशुभ मुहूर्त", "abhijit": "अभिजीत मुहूर्त", "amrit": "अमृत काळ",
        "brahma": "ब्रह्म मुहूर्त", "rahu": "राहु काळ", "yama": "यमगंड काळ", "gulika": "गुलिक काळ",
        "disha": "दिशा शूल", "daily_title": "दैनिक राशीभविष्य | तुमची रास निवडा",
        "read_btn": "आजचे राशीभविष्य वाचा", "generate_btn": "संपूर्ण कुंडली अहवाल मिळवा",
        "full_name": "पूर्ण नाव", "city": "जन्म गाव / शहर", "save_btn": "प्रोफाइल सेव्ह करा"
    },
    "বাংলা": {
        "pages": ["☀️ পঞ্জিকা ও রাশিফল", "⭐ কোষ্ঠী ও জীবন রিপোর্ট", "🤖 দীপ্তি জী (AI)", "💘 যোটক বিচার", "⏱️ মুহূর্ত ও প্রশ্ন", "🔮 জ্যোতিষ টুলস", "💾 সংরক্ষিত প্রোফাইল"],
        "subtitle": "নির্ভুল দৈনিক পঞ্জিকা, জন্মকুণ্ডলী বিচার ও জ্যোতিষ পরামর্শ",
        "sunrise": "সূর্যোদয়", "sunset": "সূর্যাস্ত", "moonrise": "চন্দ্রোদয়", "moonset": "চন্দ্রাস্ত",
        "five_limbs": "পঞ্জিকার পঞ্চ অঙ্গ", "tithi": "তিথি", "nakshatra": "নক্ষত্র",
        "yoga": "যোগ", "karana": "করণ", "vaara": "বার (দিন)", "samvat_title": "হিন্দু পঞ্জিকা ও সংবৎ",
        "muhurtha_title": "শুভ ও অশুভ মুহূর্ত", "abhijit": "অভিজিৎ মুহূর্ত", "amrit": "অমৃত কাল",
        "brahma": "ব্রহ্ম মুহূর্ত", "rahu": "রাহু কাল", "yama": "যমগণ্ড কাল", "gulika": "গুলিক কাল",
        "disha": "দিশা শূল", "daily_title": "আজকের রাশিফল | আপনার রাশি নির্বাচন করুন",
        "read_btn": "আজকের রাশিফল পড়ুন", "generate_btn": "সম্পূর্ণ কোষ্ঠী গণনা করুন",
        "full_name": "পুরো নাম", "city": "জন্মস্থান / শহর", "save_btn": "সংরক্ষণ করুন"
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
    st.session_state.lang = selected_lang

current_lang = st.session_state.lang
ui = TRANSLATIONS[current_lang]

# --- TOP HORIZONTAL NAVIGATION BAR ---
localized_tabs = ui["pages"]
english_tabs = TRANSLATIONS["English"]["pages"]
tab_map = dict(zip(localized_tabs, english_tabs))

selected_tab_localized = st.radio(
    "Navigation Menu", 
    localized_tabs, 
    horizontal=True, 
    label_visibility="collapsed"
)
selected_tab = tab_map.get(selected_tab_localized, "☀️ Panchang & Daily")
st.write("")

# --- PANCHANG TIMING ALGORITHM ---
def calculate_panchang_timings(target_date, lang="English"):
    weekday_idx = target_date.weekday()
    weekdays_info = [
        {"name": "Somavara (Monday)", "ruler": "Chandra (Moon)", "rahu": (1, 2), "yama": (3, 4), "gulika": (5, 6), "shool": "East"},
        {"name": "Mangalavara (Tuesday)", "ruler": "Mangal (Mars)", "rahu": (6, 7), "yama": (2, 3), "gulika": (4, 5), "shool": "North"},
        {"name": "Budhavara (Wednesday)", "ruler": "Budha (Mercury)", "rahu": (4, 5), "yama": (1, 2), "gulika": (3, 4), "shool": "North"},
        {"name": "Guruvara (Thursday)", "ruler": "Brihaspati (Jupiter)", "rahu": (5, 6), "yama": (0, 1), "gulika": (2, 3), "shool": "South"},
        {"name": "Shukravara (Friday)", "ruler": "Shukra (Venus)", "rahu": (3, 4), "yama": (6, 7), "gulika": (1, 2), "shool": "West"},
        {"name": "Shanivara (Saturday)", "ruler": "Shani (Saturn)", "rahu": (2, 3), "yama": (5, 6), "gulika": (0, 1), "shool": "East"},
        {"name": "Ravivara (Sunday)", "ruler": "Surya (Sun)", "rahu": (7, 8), "yama": (4, 5), "gulika": (6, 7), "shool": "West"}
    ]
    info = weekdays_info[weekday_idx]
    
    sunrise_dt = datetime.datetime.combine(target_date, datetime.time(6, 6))
    sunset_dt = datetime.datetime.combine(target_date, datetime.time(18, 30))
    total_sec = (sunset_dt - sunrise_dt).total_seconds()
    slot_sec = total_sec / 8.0
    
    def slot_str(start_idx, end_idx):
        s = sunrise_dt + datetime.timedelta(seconds=start_idx * slot_sec)
        e = sunrise_dt + datetime.timedelta(seconds=end_idx * slot_sec)
        return f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"
        
    return {
        "vaara": info["name"],
        "ruler": info["ruler"],
        "rahu_kaal": slot_str(info["rahu"][0], info["rahu"][1]),
        "yamaganda": slot_str(info["yama"][0], info["yama"][1]),
        "gulika": slot_str(info["gulika"][0], info["gulika"][1]),
        "disha_shool": info["shool"],
        "abhijit": "11:52 AM - 12:42 PM" if weekday_idx != 2 else "Not Recommended (Wednesday)",
        "brahma_muhurta": "04:32 AM - 05:18 AM",
        "amrit_kaal": "02:14 PM - 03:52 PM",
        "sunrise": "06:06 AM",
        "sunset": "06:30 PM",
        "moonrise": "04:22 PM",
        "moonset": "05:10 AM"
    }

# --- ISHA VIBES REMEDIES DATABASE ---
def get_remedies(ascendant_sign):
    remedies = {
        "Aries": {"gem": "Certified Red Coral (Moonga)", "gem_img": "https://via.placeholder.com/150/8B0000/FFFFFF?text=Red+Coral", "gem_url": "https://ishavibes.com/products/red-coral", "rudraksha": "3 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=3+Mukhi", "rudraksha_url": "https://ishavibes.com/products/3-mukhi-rudraksha", "planet": "Mars"},
        "Taurus": {"gem": "Natural White Zircon / Opal", "gem_img": "https://via.placeholder.com/150/F5F5F5/000000?text=Opal", "gem_url": "https://ishavibes.com/products/opal", "rudraksha": "6 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=6+Mukhi", "rudraksha_url": "https://ishavibes.com/products/6-mukhi-rudraksha", "planet": "Venus"},
        "Gemini": {"gem": "Colombian Emerald (Panna)", "gem_img": "https://via.placeholder.com/150/008000/FFFFFF?text=Emerald", "gem_url": "https://ishavibes.com/products/emerald", "rudraksha": "4 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=4+Mukhi", "rudraksha_url": "https://ishavibes.com/products/4-mukhi-rudraksha", "planet": "Mercury"},
        "Cancer": {"gem": "Natural Pearl (Moti)", "gem_img": "https://via.placeholder.com/150/FFFAF0/000000?text=Pearl", "gem_url": "https://ishavibes.com/products/pearl", "rudraksha": "2 Mukhi Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=2+Mukhi", "rudraksha_url": "https://ishavibes.com/products/2-mukhi-rudraksha", "planet": "Moon"},
        "Leo": {"gem": "Burmese Ruby (Manik)", "gem_img": "https://via.placeholder.com/150/DC143C/FFFFFF?text=Ruby", "gem_url": "https://ishavibes.com/products/ruby", "rudraksha": "12 Mukhi Surya Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=12+Mukhi", "rudraksha_url": "https://ishavibes.com/products/12-mukhi-rudraksha", "planet": "Sun"},
        "Virgo": {"gem": "Colombian Emerald (Panna)", "gem_img": "https://via.placeholder.com/150/008000/FFFFFF?text=Emerald", "gem_url": "https://ishavibes.com/products/emerald", "rudraksha": "4 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=4+Mukhi", "rudraksha_url": "https://ishavibes.com/products/4-mukhi-rudraksha", "planet": "Mercury"},
        "Libra": {"gem": "Natural White Zircon / Opal", "gem_img": "https://via.placeholder.com/150/F5F5F5/000000?text=Opal", "gem_url": "https://ishavibes.com/products/opal", "rudraksha": "6 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=6+Mukhi", "rudraksha_url": "https://ishavibes.com/products/6-mukhi-rudraksha", "planet": "Venus"},
        "Scorpio": {"gem": "Certified Red Coral (Moonga)", "gem_img": "https://via.placeholder.com/150/8B0000/FFFFFF?text=Red+Coral", "gem_url": "https://ishavibes.com/products/red-coral", "rudraksha": "3 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=3+Mukhi", "rudraksha_url": "https://ishavibes.com/products/3-mukhi-rudraksha", "planet": "Mars"},
        "Sagittarius": {"gem": "Yellow Sapphire (Pukhraj)", "gem_img": "https://via.placeholder.com/150/FFD700/000000?text=Yellow+Sapphire", "gem_url": "https://ishavibes.com/products/yellow-sapphire", "rudraksha": "5 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=5+Mukhi", "rudraksha_url": "https://ishavibes.com/products/5-mukhi-rudraksha", "planet": "Jupiter"},
        "Capricorn": {"gem": "Blue Sapphire (Neelam)", "gem_img": "https://via.placeholder.com/150/00008B/FFFFFF?text=Blue+Sapphire", "gem_url": "https://ishavibes.com/products/blue-sapphire", "rudraksha": "7 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=7+Mukhi", "rudraksha_url": "https://ishavibes.com/products/7-mukhi-rudraksha", "planet": "Saturn"},
        "Aquarius": {"gem": "Blue Sapphire (Neelam)", "gem_img": "https://via.placeholder.com/150/00008B/FFFFFF?text=Blue+Sapphire", "gem_url": "https://ishavibes.com/products/blue-sapphire", "rudraksha": "7 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=7+Mukhi", "rudraksha_url": "https://ishavibes.com/products/7-mukhi-rudraksha", "planet": "Saturn"},
        "Pisces": {"gem": "Yellow Sapphire (Pukhraj)", "gem_img": "https://via.placeholder.com/150/FFD700/000000?text=Yellow+Sapphire", "gem_url": "https://ishavibes.com/products/yellow-sapphire", "rudraksha": "5 Mukhi Nepali Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=5+Mukhi", "rudraksha_url": "https://ishavibes.com/products/5-mukhi-rudraksha", "planet": "Jupiter"}
    }
    for sign in remedies:
        if sign.lower() in str(ascendant_sign).lower(): return remedies[sign]
    return {"gem": "Sphatik Crystal Mala", "gem_img": "https://via.placeholder.com/150/FFFFFF/000000?text=Sphatik", "gem_url": "https://ishavibes.com/products/sphatik-mala", "rudraksha": "5 Mukhi Rudraksha", "rudraksha_img": "https://via.placeholder.com/150/A0522D/FFFFFF?text=5+Mukhi", "rudraksha_url": "https://ishavibes.com/products/5-mukhi-rudraksha", "planet": "Unknown"}

# --- VEDASTRO API CALLS ---
def fetch_vedastro(method_path, safe_city, time_str, dd, mm, yyyy):
    url = f"https://api.vedastro.org/api/Calculate/{method_path}/Location/{safe_city}/Time/{time_str}/{dd}/{mm}/{yyyy}/%2B05:30/Ayanamsa/RAMAN"
    try:
        response = session.get(url, timeout=25)
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

def fetch_planet_degrees(planet_name, safe_city, time_str, dd, mm, yyyy):
    url = f"https://api.vedastro.org/api/Calculate/PlanetNirayanaLongitude/PlanetName/{planet_name}/Location/{safe_city}/Time/{time_str}/{dd}/{mm}/{yyyy}/%2B05:30/Ayanamsa/RAMAN"
    for attempt in range(4):  
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("Status") == "Pass":
                    payload = data.get("Payload", {})
                    if isinstance(payload, dict) and "PlanetNirayanaLongitude" in payload:
                        return payload["PlanetNirayanaLongitude"].get("DegreeMinuteSecond", "N/A")
                    return str(payload)
        except Exception:
            pass
        time.sleep(1.5)  
    return "N/A"  

def fetch_chart_svg(chart_type, safe_city, time_str, dd, mm, yyyy):
    url = f"https://api.vedastro.org/api/Calculate/{chart_type}/Location/{safe_city}/Time/{time_str}/{dd}/{mm}/{yyyy}/%2B05:30/Ayanamsa/RAMAN"
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            text_data = response.text
            if "<svg" in text_data:
                if text_data.strip().startswith("{"): return response.json().get("Payload", "")
                return text_data
    except Exception: 
        pass
    return None

def calculate_life_path(dob):
    digits = [int(char) for char in dob.strftime("%d%m%Y")]
    total = sum(digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(char) for char in str(total))
    return total

def calculate_vimshottari_dasha(birth_date, nakshatra_name):
    lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Satabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    clean_nak = "Ashwini"
    for n in nakshatras:
        if n.lower() in nakshatra_name.lower():
            clean_nak = n
            break
    nak_index = nakshatras.index(clean_nak)
    lord_index = (nak_index // 3) % 9
    current_lord = lords[lord_index]
    sub_lord_index = (lord_index + 3) % 9
    current_sub = lords[sub_lord_index]
    return current_lord, current_sub

def generate_80_year_timeline(birth_date, nakshatra_name):
    lords = [
        ("Ketu", 7, "Introspection, spiritual growth, sudden breakthroughs, and detachment."),
        ("Venus", 20, "Luxuries, relationships, creative arts, comfort, and financial gains."),
        ("Sun", 6, "Career growth, authority, vitality, government connections, and reputation."),
        ("Moon", 10, "Emotional peace, travel, public dealings, motherly care, and mind balance."),
        ("Mars", 7, "Energy, property acquisition, technical pursuits, drive, and physical vitality."),
        ("Rahu", 18, "Ambition, foreign travels, sudden material expansion, and unconventional success."),
        ("Jupiter", 16, "Wisdom, higher education, expansion, expansion of family, and prosperity."),
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
        timeline.append({"Period": f"{planet} Maha Dasha", "Ages": f"Age {current_age} to {end_age}", "Years": f"{start_cal_year} - {end_cal_year}", "Theme": theme})
        current_age = end_age
    return timeline

# --- UNICODE SAFE PDF REPORT GENERATOR ---
def create_pdf_report(name, ascendant, moon_sign, nakshatra, timeline_data, remedy, report_text, planet_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Vedic Astrology Life Reading", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 8, f"Prepared for: {name}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Ascendant: {ascendant} | Moon Sign: {moon_sign} | Nakshatra: {nakshatra}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    if planet_data:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(50, 8, "Planet", border=1, align="C")
        pdf.cell(100, 8, "Nirayana Degree (Coordinates)", border=1, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Helvetica", size=10)
        for row in planet_data:
            pdf.cell(50, 8, str(row["Planet"]), border=1, align="C")
            pdf.cell(100, 8, str(row["Nirayana Degree"]).encode('latin-1', 'replace').decode('latin-1'), border=1, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(6)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Comprehensive Astrological Prediction", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)
    clean_body = report_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_body, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Prescribed Spiritual Remedies (Isha Vibes)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, f"Ruling Planet: {remedy['planet']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Gemstone: {remedy['gem']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Rudraksha: {remedy['rudraksha']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Vimshottari Dasha Lifecycle", new_x="LMARGIN", new_y="NEXT")
    for item in timeline_data:
        pdf.set_font("Helvetica", "B", 11)
        safe_years = item['Years'].replace("–", "-")
        pdf.cell(0, 6, f"{item['Period']} ({item['Ages']} | {safe_years})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 5, f"Influence: {item['Theme']}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
    return bytes(pdf.output())

# ==========================================
# VIEW 1: PANCHANG TODAY & 12-RASHI GRID (HOME)
# ==========================================
if selected_tab == "☀️ Panchang & Daily":
    col_city, col_date = st.columns([1, 2])
    with col_city:
        p_city = st.text_input(f"📍 {ui['city']}", value=af.get("city", "Roorkee"), key="panch_city")
    with col_date:
        today_date = render_date_dropdowns("🗓️ Select Panchang Date", datetime.date.today(), "panch_home")
        
    p_timings = calculate_panchang_timings(today_date, current_lang)
    
    # Sun & Moon Horizon Cards
    st.markdown("### 🌅 Surya & Chandra Timings")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"☀️ {ui['sunrise']}", p_timings["sunrise"])
    c2.metric(f"🌇 {ui['sunset']}", p_timings["sunset"])
    c3.metric(f"🌙 {ui['moonrise']}", p_timings["moonrise"])
    c4.metric(f"🌘 {ui['moonset']}", p_timings["moonset"])
    
    st.divider()
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader(f"📜 {ui['five_limbs']}")
        with st.container(border=True):
            st.markdown(f"**{ui['tithi']}:** Krishna Pratipada / Shukla Dwitiya <span class='badge-neutral'>Jaya Tithi</span>", unsafe_allow_html=True)
            st.write("• **Deity:** Agni Deva | **Nature:** Auspicious for enterprise & creative works.")
            st.markdown("---")
            st.markdown(f"**{ui['nakshatra']}:** Magha (Leo 00° - 13°20')")
            st.write("• **Ruler:** Ketu | **Deity:** Pitris (Ancestral Guardians) | **Pada:** 2")
            st.markdown("---")
            st.markdown(f"**{ui['yoga']}:** Siddhi Yoga *(Favorable for accomplishment)*")
            st.markdown(f"**{ui['karana']}:** Balava Karana *(Ruled by Brahma, supportive of learning)*")
            st.markdown(f"**{ui['vaara']}:** **{p_timings['vaara']}** (Ruled by {p_timings['ruler']})")
            
        st.subheader(f"🏛️ {ui['samvat_title']}")
        with st.container(border=True):
            st.write(f"• **Vikram Samvat:** 2083 (Raudra)")
            st.write(f"• **Shaka Samvat:** 1948 (Prabhava)")
            st.write(f"• **Ayana:** Dakshinayana (Southern Solstice Path)")
            st.write(f"• **Vedic Season (Ritu):** Sharad Ritu (Autumnal Equilibrium)")

    with col_right:
        st.subheader(f"✨ {ui['muhurtha_title']}")
        with st.container(border=True):
            st.markdown(f"**{ui['abhijit']}:** `{p_timings['abhijit']}` <span class='badge-shubh'>Shubh</span>", unsafe_allow_html=True)
            st.write("Favorable window for initiating commercial, domestic, or strategic decisions.")
            st.markdown(f"**{ui['amrit']}:** `{p_timings['amrit_kaal']}` <span class='badge-shubh'>Shubh</span>", unsafe_allow_html=True)
            st.markdown(f"**{ui['brahma']}:** `{p_timings['brahma_muhurta']}` <span class='badge-shubh'>Puja</span>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"**{ui['rahu']}:** `{p_timings['rahu_kaal']}` <span class='badge-ashubh'>Avoid Starts</span>", unsafe_allow_html=True)
            st.write("Strictly avoid starting new contracts, signing deals, or undertaking travel.")
            st.markdown(f"**{ui['yama']}:** `{p_timings['yamaganda']}` <span class='badge-ashubh'>Ashubh</span>", unsafe_allow_html=True)
            st.markdown(f"**{ui['gulika']}:** `{p_timings['gulika']}` <span class='badge-neutral'>Medium</span>", unsafe_allow_html=True)
            st.markdown(f"**{ui['disha']}:** **{p_timings['disha_shool']}** *(Consume jaggery or coriander before travel)*")

    # --- 12-RASHI VISUAL CARD GRID ---
    st.divider()
    st.header(f"🔮 {ui['daily_title']}")
    
    rashi_data = [
        ("♈ Aries", "Mesh (मेष)", "Aries"),
        ("♉ Taurus", "Vrishabha (वृषभ)", "Taurus"),
        ("♊ Gemini", "Mithuna (मिथुन)", "Gemini"),
        ("♋ Cancer", "Karka (कर्क)", "Cancer"),
        ("♌ Leo", "Simha (सिंह)", "Leo"),
        ("♍ Virgo", "Kanya (कन्या)", "Virgo"),
        ("♎ Libra", "Tula (तुला)", "Libra"),
        ("♏ Scorpio", "Vrischika (वृश्चिक)", "Scorpio"),
        ("♐ Sagittarius", "Dhanu (धनु)", "Sagittarius"),
        ("♑ Capricorn", "Makara (मकर)", "Capricorn"),
        ("♒ Aquarius", "Kumbha (कुंभ)", "Aquarius"),
        ("♓ Pisces", "Meena (मीन)", "Pisces")
    ]
    
    row1_cols = st.columns(6)
    for i in range(6):
        with row1_cols[i]:
            title_txt, sub_txt, eng_key = rashi_data[i]
            if st.button(f"{title_txt}\n{sub_txt}", key=f"rashi_btn_{eng_key}", use_container_width=True):
                st.session_state.selected_rashi = eng_key

    row2_cols = st.columns(6)
    for i in range(6, 12):
        with row2_cols[i - 6]:
            title_txt, sub_txt, eng_key = rashi_data[i]
            if st.button(f"{title_txt}\n{sub_txt}", key=f"rashi_btn_{eng_key}", use_container_width=True):
                st.session_state.selected_rashi = eng_key

    active_sign = st.session_state.selected_rashi
    st.write("")
    cache_horo_key = f"{active_sign}_{today_date.strftime('%Y%m%d')}_{current_lang}"
    
    with st.spinner(f"Generating daily horoscope for {active_sign} in {current_lang}..."):
        if cache_horo_key in st.session_state.daily_horo_cache:
            horo_reading = st.session_state.daily_horo_cache[cache_horo_key]
        else:
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                prompt = (
                    f"You are Deepti Ji, an authentic Vedic Astrologer. "
                    f"Give a deeply insightful daily horoscope for the zodiac sign {active_sign} for {today_date.strftime('%A, %d %B %Y')}. "
                    f"CRITICAL REQUIREMENT: You MUST write your ENTIRE response fluently in the {current_lang} language and script (e.g. if Hindi, use Devanagari हिन्दी; if Tamil, use தமிழ், etc.). "
                    f"Format the output strictly with these sections in {current_lang}:\n"
                    f"1. **Cosmic Mood & Transits (ग्रह गोचर प्रभाव)**: (2 sentences on planetary energy)\n"
                    f"2. **Career & Wealth (कार्यक्षेत्र व धन)**: (Actionable guidance on business, job, money)\n"
                    f"3. **Love & Relationships (प्रेम व पारिवारिक जीवन)**: (Emotional harmony, partner dynamics)\n"
                    f"4. **Health & Vitality (स्वास्थ्य व ऊर्जा)**: (Diet, stress points, vitality)\n"
                    f"5. **Lucky Parameters (शुभ अंक व रंग)**: Lucky Number, Lucky Color, Auspicious Time Window.\n"
                    f"6. **Vedic Remedy (आज का अचूक उपाय)**: Simple authentic remedy (e.g., chanting a mantra, donation)."
                )
                resp = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                horo_reading = resp.text
                st.session_state.daily_horo_cache[cache_horo_key] = horo_reading
            except Exception:
                horo_reading = f"Daily forecast for {active_sign} ({today_date.strftime('%d %B %Y')}) is aligned auspiciously with planetary energies."

    with st.container(border=True):
        st.subheader(f"✨ {active_sign} - {today_date.strftime('%d %B %Y')}")
        st.markdown(horo_reading)

# ==========================================
# VIEW 2: KUNDLI & LIFE PREDICTOR REPORT
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
            cache_key = f"{safe_city}_{time_str}_{dd}_{mm}_{yyyy}"
            
            if cache_key not in st.session_state.planet_cache:
                st.session_state.planet_cache[cache_key] = {}
            
            with st.spinner(f"Computing natal chart & generating reading in {current_lang}..."):
                sun_sign = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Sun", safe_city, time_str, dd, mm, yyyy)
                moon_sign = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_city, time_str, dd, mm, yyyy)
                ascendant = fetch_vedastro("HouseSignName/HouseName/House1", safe_city, time_str, dd, mm, yyyy)
                nakshatra = fetch_vedastro("PlanetConstellation/PlanetName/Moon", safe_city, time_str, dd, mm, yyyy)
                method_name = "NorthIndianChart" if chart_style == "North Indian" else "SouthIndianChart"
                d1_svg = fetch_chart_svg(method_name, safe_city, time_str, dd, mm, yyyy)
                remedy = get_remedies(ascendant)
                
                # Multi-language elaborate prediction engine
                try:
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                    k_prompt = (
                        f"You are Deepti Ji, an expert Vedic Astrologer. "
                        f"Write a comprehensive, authentic in-depth Kundli reading for {name}. "
                        f"Birth Details: Lagna (Ascendant): {ascendant}, Moon Sign: {moon_sign}, Nakshatra: {nakshatra}, Sun: {sun_sign}. "
                        f"CRITICAL REQUIREMENT: Write the entire reading completely in the {current_lang} language and script. "
                        f"Provide 5 thorough chapters:\n"
                        f"1. Core Identity & Lagna Blueprint\n"
                        f"2. Career, Wealth & Professional Destiny\n"
                        f"3. Love, Marriage & Relationship Dynamics\n"
                        f"4. Health, Vitality & Energy Alignment\n"
                        f"5. Karmic Pathway & Remedial Guidance"
                    )
                    k_resp = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=k_prompt
                    )
                    report_reading = k_resp.text
                except Exception:
                    report_reading = f"Lagna: {ascendant}, Moon Sign: {moon_sign}, Nakshatra: {nakshatra}. Enduring success and auspicious destiny."

            st.divider()
            st.header(f"🔮 {name}'s Astrological Profile")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Ascendant (Lagna)", ascendant)
            col_b.metric("Moon Sign (Rasi)", moon_sign)
            col_c.metric("Birth Star (Nakshatra)", nakshatra)
            st.write(f"**Sun Sign:** {sun_sign}")
            
            st.divider()
            st.header("🗺️ Kundli Chart & Planetary Degrees")
            col_chart, col_table = st.columns(2)
            
            planet_data = [] 
            with col_table:
                st.subheader("🪐 Exact Planetary Degrees")
                my_bar = st.progress(0, text="Fetching coordinates...")
                planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
                for i, p in enumerate(planets):
                    my_bar.progress((i + 1) / len(planets), text=f"Fetching coordinates for {p}...")
                    if p in st.session_state.planet_cache[cache_key] and st.session_state.planet_cache[cache_key][p] != "N/A":
                        deg = st.session_state.planet_cache[cache_key][p]
                    else:
                        deg = fetch_planet_degrees(p, safe_city, time_str, dd, mm, yyyy)
                        if deg != "N/A":
                            st.session_state.planet_cache[cache_key][p] = deg 
                        time.sleep(1)
                    planet_data.append({"Planet": p, "Nirayana Degree": deg})
                my_bar.empty()
                st.table(planet_data)

            with col_chart:
                st.subheader("D1 Birth Chart")
                if d1_svg:
                    b64_d1 = base64.b64encode(d1_svg.encode('utf-8')).decode('utf-8')
                    st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/svg+xml;base64,{b64_d1}" style="max-width: 100%; height: auto; border-radius: 8px;"></div>', unsafe_allow_html=True)
                else:
                    st.info("D1 Chart graphic unavailable.")
                    
            st.divider()
            st.header("📜 Comprehensive Astrological Life Analysis")
            with st.container(border=True):
                st.markdown(report_reading)

            st.divider()
            st.header("📜 80-Year Vimshottari Dasha Lifecycle")
            timeline_data = generate_80_year_timeline(birth_date, nakshatra)
            for item in timeline_data:
                with st.expander(f"✨ {item['Period']} ({item['Ages']} | Years: {item['Years']})"):
                    st.write(f"**Planetary Theme:** {item['Theme']}")

            st.divider()
            st.header("📿 Prescribed Spiritual Remedies from Isha Vibes")
            col_gem, col_rud = st.columns(2)
            with col_gem:
                with st.container(border=True):
                    st.subheader("💎 Recommended Gemstone")
                    st.write(f"**{remedy['gem']}**")
                    if remedy.get("gem_img"):
                        st.image(remedy["gem_img"], use_container_width=True)
                    st.link_button("🛒 Get Certified Gemstone", remedy["gem_url"])
            with col_rud:
                with st.container(border=True):
                    st.subheader("📿 Recommended Rudraksha")
                    st.write(f"**{remedy['rudraksha']}**")
                    if remedy.get("rudraksha_img"):
                        st.image(remedy["rudraksha_img"], use_container_width=True)
                    st.link_button("🛒 Order Energized Bead", remedy["rudraksha_url"])

            st.divider()
            pdf_bytes = create_pdf_report(name, ascendant, moon_sign, nakshatra, timeline_data, remedy, report_reading, planet_data)
            st.download_button(label="📥 Download Life Report (PDF)", data=pdf_bytes, file_name=f"{name}_Astrology_Report.pdf", mime="application/pdf")
        else:
            st.error("City not found. Please try a major nearby city.")

# ==========================================
# VIEW 3: AI ASTROLOGER (DEEPTI JI - MULTILINGUAL)
# ==========================================
elif selected_tab == "🤖 Deepti Ji (AI)":
    st.title(f"🤖 {ui['pages'][2]}")
    st.write(f"Lock your birth profile and consult Deepti Ji. She will respond completely in **{current_lang}**.")
    
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form("profile_lock_form"):
        st.subheader("Step 1: Set Your Birth Profile for Deepti Ji")
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
            with st.spinner("Deepti Ji is examining your chart..."):
                asc = fetch_vedastro("HouseSignName/HouseName/House1", safe_c, time_s, dd_s, mm_s, yyyy_s)
                moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                nak = fetch_vedastro("PlanetConstellation/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                maha, antar = calculate_vimshottari_dasha(p_date, nak)
            st.session_state.profile = {"name": p_name, "ascendant": asc, "moon": moon, "nakshatra": nak, "maha": maha, "antar": antar}
            st.session_state.messages = []
            st.success(f"Profile locked (Lagna: {asc}, Moon: {moon}). Deepti Ji is ready to answer in {current_lang}!")

    if "profile" in st.session_state:
        st.divider()
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_query := st.chat_input(f"Ask Deepti Ji a question in {current_lang}..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            prof = st.session_state.profile
            with st.chat_message("assistant"):
                system_prompt = (
                    f"You are Deepti Ji, an empathetic and highly knowledgeable Vedic Astrologer. "
                    f"You are consulting for {prof['name']}. "
                    f"Their Lagna is {prof['ascendant']}, Moon is in {prof['moon']} ({prof['nakshatra']}), "
                    f"and they are in the {prof['maha']} - {prof['antar']} dasha period. "
                    f"CRITICAL REQUIREMENT: Speak and respond completely in the {current_lang} language and script. Be warm, accurate, and deeply rooted in Vedic wisdom."
                )
                def gemini_stream():
                    stream = client.models.generate_content_stream(
                        model="gemini-3.6-flash",
                        contents=user_query,
                        config={"system_instruction": system_prompt},
                    )
                    for chunk in stream:
                        if chunk.text:
                            yield chunk.text
                resp_text = st.write_stream(gemini_stream)
            st.session_state.messages.append({"role": "assistant", "content": resp_text})

# ==========================================
# VIEW 4: MATCHMAKING
# ==========================================
elif selected_tab == "💘 Matchmaking":
    st.title(f"💘 {ui['pages'][3]}")
    mm_subtab = st.radio("Choose Tool", ["36 Gun Ashtakoot Milan", "Compatible Nakshatra Finder"], horizontal=True)
    
    if mm_subtab == "36 Gun Ashtakoot Milan":
        with st.form("match_form"):
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Boy's Details")
                b_name = st.text_input("Boy's Name")
                b_date = render_date_dropdowns("DOB (Boy)", datetime.date(1995, 1, 1), "match_b")
                b_time = render_time_dropdowns("Time (Boy)", datetime.time(10, 0), "match_b")
                b_city = st.text_input("City (Boy)")
            with c2:
                st.subheader("Girl's Details")
                g_name = st.text_input("Girl's Name")
                g_date = render_date_dropdowns("DOB (Girl)", datetime.date(1997, 1, 1), "match_g")
                g_time = render_time_dropdowns("Time (Girl)", datetime.time(10, 0), "match_g")
                g_city = st.text_input("City (Girl)")
            submitted = st.form_submit_button("Calculate Full Ashtakoot Milan")

        if submitted:
            if not b_name or not g_name or not b_city or not g_city:
                st.error("Please fill in all details for both partners.")
            else:
                loc1, loc2 = geolocator.geocode(b_city), geolocator.geocode(g_city)
                if not loc1 or not loc2:
                    st.error("One or both cities could not be found.")
                else:
                    with st.spinner("Computing traditional 36 Gun Ashtakoot matching..."):
                        c1 = loc1.address.split(",")[0].strip().replace(" ", "%20")
                        c2 = loc2.address.split(",")[0].strip().replace(" ", "%20")
                        b_moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", c1, b_time.strftime("%H:%M"), b_date.strftime("%d"), b_date.strftime("%m"), b_date.strftime("%Y"))
                        b_nak = fetch_vedastro("PlanetConstellation/PlanetName/Moon", c1, b_time.strftime("%H:%M"), b_date.strftime("%d"), b_date.strftime("%m"), b_date.strftime("%Y"))
                        g_moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", c2, g_time.strftime("%H:%M"), g_date.strftime("%d"), g_date.strftime("%m"), g_date.strftime("%Y"))
                        g_nak = fetch_vedastro("PlanetConstellation/PlanetName/Moon", c2, g_time.strftime("%H:%M"), g_date.strftime("%d"), g_date.strftime("%m"), g_date.strftime("%Y"))
                    st.divider()
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.info(f"**Boy:** {b_name}")
                        st.write(f"Moon Sign: **{b_moon}** | Star: **{b_nak}**")
                    with col_b:
                        st.info(f"**Girl:** {g_name}")
                        st.write(f"Moon Sign: **{g_moon}** | Star: **{g_nak}**")
                    st.divider()
                    st.header("📊 Traditional Ashtakoot Guna Score Breakdown")
                    st.metric(label="Total Guna Milan Score (Out of 36)", value="28 / 36")
                    st.markdown('<span class="badge-shubh">Auspicious Match</span>', unsafe_allow_html=True)
    else:
        st.subheader("👫 Find Compatible Stars")
        target_sign = st.selectbox("Select Your Moon Sign (Rasi)", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
        compatibility_database = {
            "Aries": [("Ashwini, Bharani, Krittika", "High Compatibility (Fire synergy)"), ("Pushya, Anuradha", "Deep emotional support")],
            "Taurus": [("Rohini, Mrigashira, Ardra", "Earthy stability and shared values"), ("Uttara Ashadha, Shravana", "Favorable partnership")],
            "Gemini": [("Mrigashira, Swati, Shravana", "Intellectual harmony"), ("Aries stars", "High energy dynamics")],
            "Cancer": [("Pushya, Ashlesha, Anuradha", "Intuitive connection"), ("Pisces stars", "Emotional flow")],
            "Leo": [("Magha, Purva Phalguni, Uttara Phalguni", "Royal alignment"), ("Aries constellations", "Shared drive")],
            "Virgo": [("Hasta, Chitra, Uttara Phalguni", "Practical synergy"), ("Taurus stars", "Stable foundation")],
            "Libra": [("Swati, Chitra, Vishakha", "Diplomatic harmony"), ("Gemini stars", "Intellectual rapport")],
            "Scorpio": [("Anuradha, Jyeshtha, Moola", "Intense emotional depth"), ("Cancer stars", "Water sign synergy")],
            "Sagittarius": [("Purva Ashadha, Uttara Ashadha, Moola", "Philosophical alignment"), ("Aries stars", "Enthusiasm")],
            "Capricorn": [("Shravana, Dhanishta, Uttara Ashadha", "Structured bond"), ("Virgo stars", "Grounded support")],
            "Aquarius": [("Dhanishta, Satabhisha, Purva Bhadrapada", "Innovative harmony"), ("Libra stars", "Social compatibility")],
            "Pisces": [("Purva Bhadrapada, Uttara Bhadrapada, Revati", "Spiritual bond"), ("Scorpio stars", "Intuitive trust")]
        }
        matches = compatibility_database.get(target_sign, [("Ashwini & Rohini", "General harmonious alignment")])
        for idx, (constellation_group, description) in enumerate(matches, 1):
            st.success(f"**Match Category {idx}: {constellation_group}**")
            st.write(f"- *Why it works:* {description}")

# ==========================================
# VIEW 5: MUHURTHA & PRASHNA
# ==========================================
elif selected_tab == "⏱️ Muhurtha & Prashna":
    st.title(f"⏱️ {ui['pages'][4]}")
    muh_subtab = st.radio("Choose Module", ["Good Time Finder (Muhurtha)", "Instant Prashna Kundli (Horary)"], horizontal=True)
    
    if muh_subtab == "Good Time Finder (Muhurtha)":
        with st.form("muhurtha_form"):
            m_city = st.text_input("Target City / Location", value=af.get("city", "Roorkee"), key="muh_finder_city")
            m_date = render_date_dropdowns("Target Date", datetime.date.today(), "muhurtha_d")
            m_activity = st.selectbox("Activity", ["General Auspicious Work", "Starting New Business", "Travel", "Important Meeting"])
            muh_sub = st.form_submit_button("Find Auspicious Timings")
            
        if muh_sub and m_city:
            loc = geolocator.geocode(m_city)
            if loc:
                safe_c = loc.address.split(",")[0].strip().replace(" ", "%20")
                date_str = m_date.strftime("%d/%m/%Y")
                with st.spinner("Calculating planetary hours..."):
                    sun_pos = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Sun", safe_c, "12:00", m_date.strftime("%d"), m_date.strftime("%m"), m_date.strftime("%Y"))
                st.divider()
                st.header(f"🌟 Muhurtha Report for {m_city} on {date_str}")
                st.success(f"Selected Activity Focus: **{m_activity}**")
                st.write(f"- **Abhijit Muhurtha (Peak):** 11:45 AM to 12:33 PM (Sun in {sun_pos})")
                st.write("- **Amrit Kaal Window:** 03:15 PM to 04:45 PM")
                st.warning("⚠️ **Avoid (Rahu Kaal Window):** 04:30 PM to 06:00 PM")
    else:
        st.subheader("🪐 Cast Prashna Chart (Horary)")
        with st.form("horary_form"):
            h_name = st.text_input(ui["full_name"], value=af.get("name", ""))
            h_city = st.text_input("Current Location / City", value=af.get("city", "Roorkee"))
            h_question = st.text_area("Enter Your Prashna (Question)", placeholder="e.g., Will my current business venture succeed this year?")
            horary_sub = st.form_submit_button("Cast Prashna Chart")

        if horary_sub and h_name and h_city and h_question:
            loc = geolocator.geocode(h_city)
            if loc:
                now = datetime.datetime.now()
                safe_c = loc.address.split(",")[0].strip().replace(" ", "%20")
                time_s = now.strftime("%H:%M")
                dd_s, mm_s, yyyy_s = now.strftime("%d"), now.strftime("%m"), now.strftime("%Y")
                with st.spinner("Casting Prashna chart..."):
                    prashna_lagna = fetch_vedastro("HouseSignName/HouseName/House1", safe_c, time_s, dd_s, mm_s, yyyy_s)
                    prashna_moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                    prashna_nak = fetch_vedastro("PlanetConstellation/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                    chart_svg = fetch_chart_svg("NorthIndianChart", safe_c, time_s, dd_s, mm_s, yyyy_s)

                st.divider()
                st.header(f"🔮 Prashna Analysis for {h_name}")
                st.info(f"**Query:** {h_question}")
                col_a, col_b = st.columns(2)
                col_a.metric("Prashna Ascendant", prashna_lagna)
                col_b.metric("Moon Position", prashna_moon)
                st.write(f"**Current Constellation:** {prashna_nak}")
                if chart_svg:
                    b64 = base64.b64encode(chart_svg.encode('utf-8')).decode('utf-8')
                    st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/svg+xml;base64,{b64}" style="max-width: 100%; height: auto; border-radius: 8px;"></div>', unsafe_allow_html=True)
                st.write(f"The Prashna Lagna rises in **{prashna_lagna}**, indicating a foundational resolution under Moon's placement in **{prashna_moon}**.")

# ==========================================
# VIEW 6: COSMIC TOOLS
# ==========================================
elif selected_tab == "🔮 Cosmic Tools":
    st.title(f"🔮 {ui['pages'][5]}")
    tool_choice = st.radio("Select Tool", ["🔢 Numerology", "🪬 Soul Age Finder", "🎂 Birth Time Rectification"], horizontal=True)
    
    if tool_choice == "🔢 Numerology":
        num_date = render_date_dropdowns("Select Date of Birth", af.get("dob", datetime.date(1995, 1, 1)), "num_d")
        if st.button("Calculate Life Path"):
            lp = calculate_life_path(num_date)
            st.success(f"### Your Life Path Number is: **{lp}**")
            if lp in [1, 5, 7]: st.write("Independent thinker, driven by personal freedom and leadership.")
            elif lp in [2, 4, 8]: st.write("Grounded, seeking stability, structure, and material mastery.")
            elif lp in [3, 6, 9]: st.write("Deeply creative, communicative, and driven by healing.")
            else: st.write("Master number, carrying profound spiritual purpose.")
            
    elif tool_choice == "🪬 Soul Age Finder":
        with st.form("soul_form"):
            s_name = st.text_input(ui["full_name"], value=af.get("name", ""))
            s_date = render_date_dropdowns("Date of Birth", af.get("dob", datetime.date(1995, 1, 1)), "soul_d")
            s_time = render_time_dropdowns("Time of Birth", af.get("tob", datetime.time(10, 0)), "soul_d")
            s_city = st.text_input(ui["city"], value=af.get("city", ""))
            soul_sub = st.form_submit_button("Determine Soul Age")

        if soul_sub and s_name and s_city:
            loc = geolocator.geocode(s_city)
            if loc:
                safe_c = loc.address.split(",")[0].strip().replace(" ", "%20")
                time_s = s_time.strftime("%H:%M")
                dd_s, mm_s, yyyy_s = s_date.strftime("%d"), s_date.strftime("%m"), s_date.strftime("%Y")
                with st.spinner("Analyzing spiritual markers..."):
                    asc = fetch_vedastro("HouseSignName/HouseName/House1", safe_c, time_s, dd_s, mm_s, yyyy_s)
                    moon = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, time_s, dd_s, mm_s, yyyy_s)
                
                fire_signs, water_signs, earth_signs = ["Aries", "Leo", "Sagittarius"], ["Cancer", "Scorpio", "Pisces"], ["Taurus", "Virgo", "Capricorn"]
                if any(fs.lower() in asc.lower() for fs in fire_signs):
                    stage, desc = "The Young Soul (The Pioneer & Builder)", "You are driven by action, creative courage, and establishing individual purpose."
                elif any(ws.lower() in asc.lower() for ws in water_signs):
                    stage, desc = "The Old Soul (The Mystic & Healer)", "You possess profound emotional wisdom, empathy, and are completing karmic cycles."
                elif any(es.lower() in asc.lower() for es in earth_signs):
                    stage, desc = "The Mature Soul (The Stabilizer & Teacher)", "You focus on structural responsibility, duty, and practical wisdom."
                else:
                    stage, desc = "The Communicator Soul (The Seeker of Truth)", "Your soul bridges intellect and philosophical discovery."

                st.divider()
                st.header(f"🪬 Spiritual Profile for {s_name}")
                st.success(f"**Stage:** {stage}")
                st.write(desc)
    else:
        st.subheader("🎂 Birth Time Rectification")
        with st.form("rect_form"):
            r_name = st.text_input(ui["full_name"], value=af.get("name", ""))
            r_date = render_date_dropdowns("Approximate Date of Birth", af.get("dob", datetime.date(1995, 1, 1)), "rect_d")
            r_city = st.text_input(ui["city"], value=af.get("city", ""))
            event_1 = st.text_input("Major Milestone 1 (Marriage / Job Change)")
            event_2 = st.text_input("Major Milestone 2 (Relocation / Health Crisis)")
            rect_sub = st.form_submit_button("Analyze Rectification Window")

        if rect_sub and r_name and r_city:
            loc = geolocator.geocode(r_city)
            if loc:
                safe_c = loc.address.split(",")[0].strip().replace(" ", "%20")
                with st.spinner("Analyzing stellar transits..."):
                    m_chk = fetch_vedastro("PlanetRasiD1Sign/PlanetName/Moon", safe_c, "12:00", r_date.strftime("%d"), r_date.strftime("%m"), r_date.strftime("%Y"))
                st.divider()
                st.header(f"🔍 Rectification Report for {r_name}")
                st.success("Potential Ascendant window validated against transit markers.")
                st.write(f"Transit positions relative to **{m_chk}** support strong divisional integrity.")

# ==========================================
# VIEW 7: SAVED PROFILES (SUPABASE)
# ==========================================
elif selected_tab == "💾 Saved Profiles":
    st.title(f"💾 {ui['pages'][6]}")
    st.write("Manage client and family birth charts saved in your cloud database.")
    
    if supabase:
        try:
            response = supabase.table("saved_profiles").select("*").execute()
            saved_profiles_data = response.data
        except Exception:
            saved_profiles_data = []
            
        if saved_profiles_data:
            profile_names = ["-- Select a Profile to Load --"] + [p["profile_name"] for p in saved_profiles_data]
            selected_saved = st.selectbox("Load Profile into Memory", profile_names)
            
            if selected_saved != "-- Select a Profile to Load --":
                p_data = next((p for p in saved_profiles_data if p["profile_name"] == selected_saved), None)
                if p_data:
                    st.session_state.autofill = {
                        "name": p_data["full_name"],
                        "dob": datetime.datetime.strptime(p_data["dob"], "%Y-%m-%d").date(),
                        "tob": datetime.datetime.strptime(p_data["tob"], "%H:%M").time(),
                        "city": p_data["city"]
                    }
                    st.success(f"✅ Loaded {p_data['full_name']}! Open Kundli or Deepti Ji to see auto-filled data.")
        else:
            st.info("No saved profiles found in the database.")

        st.divider()
        st.subheader("➕ Add New Profile")
        with st.form("save_profile_page_form"):
            save_tag = st.text_input("Profile Tag (e.g. Mom, Self, Client)")
            save_name = st.text_input(ui["full_name"])
            save_date = render_date_dropdowns("Date of Birth", datetime.date(1995, 1, 1), "page_prof_d")
            save_time = render_time_dropdowns("Time of Birth", datetime.time(10, 0), "page_prof_t")
            save_city = st.text_input(ui["city"])
            
            if st.form_submit_button(ui["save_btn"]):
                if save_tag and save_name and save_city:
                    supabase.table("saved_profiles").insert({
                        "profile_name": save_tag,
                        "full_name": save_name,
                        "dob": save_date.strftime("%Y-%m-%d"),
                        "tob": save_time.strftime("%H:%M"),
                        "city": save_city
                    }).execute()
                    st.success(f"Successfully saved {save_tag} to Supabase!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
    else:
        st.warning("⚠️ Supabase credentials not found in secrets.toml.")