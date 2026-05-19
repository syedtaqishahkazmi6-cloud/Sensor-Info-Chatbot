import streamlit as st
import os
import re
import time
import difflib
from PIL import Image

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="SensorLab HCI Pro",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FULL HCI STYLE ENGINE ---
def apply_hci_styles(theme, txt_color, accent_color):
    themes = {
        "Black & White": {"bg": "#000000", "surface": "#111111", "card": "#1a1a1a", "border": "#2a2a2a"},
        "Cyber Blue":    {"bg": "#000d1a", "surface": "#001426", "card": "#001e38", "border": "#003355"},
        "Carbon":        {"bg": "#0d0d0d", "surface": "#141414", "card": "#1c1c1c", "border": "#2c2c2c"},
        "Deep Purple":   {"bg": "#0a0010", "surface": "#120020", "card": "#1a0030", "border": "#2a0050"},
        "Forest Dark":   {"bg": "#050f05", "surface": "#0a180a", "card": "#101f10", "border": "#1a3020"},
    }
    t = themes.get(theme, themes["Black & White"])

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

        /* ── ROOT ── */
        :root {{
            --bg:       {t['bg']};
            --surface:  {t['surface']};
            --card:     {t['card']};
            --border:   {t['border']};
            --txt:      {txt_color};
            --accent:   {accent_color};
            --accent22: {accent_color}22;
            --accent55: {accent_color}55;
            --accent88: {accent_color}88;
        }}

        /* ── BASE ── */
        html, body, .stApp {{
            background-color: var(--bg) !important;
            color: var(--txt) !important;
            font-family: 'Exo 2', sans-serif !important;
        }}

        /* ── SCANLINE OVERLAY ── */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0,0,0,0.03) 2px,
                rgba(0,0,0,0.03) 4px
            );
            pointer-events: none;
            z-index: 9999;
        }}

        /* ── SIDEBAR ── */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%) !important;
            border-right: 1px solid var(--border) !important;
        }}
        [data-testid="stSidebar"] * {{
            color: var(--txt) !important;
        }}
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background: var(--card) !important;
            border: 1px solid var(--accent55) !important;
            border-radius: 8px !important;
            color: var(--txt) !important;
        }}
        [data-testid="stSidebar"] label {{
            color: var(--accent) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-size: 0.75rem !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
        }}

        /* ── HEADINGS ── */
        h1 {{
            font-family: 'Orbitron', monospace !important;
            font-weight: 900 !important;
            font-size: 2rem !important;
            color: var(--accent) !important;
            letter-spacing: 0.15em !important;
            text-shadow: 0 0 20px var(--accent55), 0 0 40px var(--accent22) !important;
            border-bottom: 1px solid var(--accent55) !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 1.5rem !important;
            animation: flickerIn 0.8s ease-out !important;
        }}
        h2, h3 {{
            font-family: 'Orbitron', monospace !important;
            color: var(--accent) !important;
            letter-spacing: 0.1em !important;
        }}

        /* ── CHAT MESSAGES ── */
        [data-testid="stChatMessage"] {{
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-left: 3px solid var(--accent) !important;
            border-radius: 0 12px 12px 0 !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 0.75rem !important;
            animation: slideInMsg 0.3s ease-out !important;
            transition: box-shadow 0.2s ease !important;
        }}
        [data-testid="stChatMessage"]:hover {{
            box-shadow: 0 0 15px var(--accent22) !important;
        }}
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div {{
            color: var(--txt) !important;
            font-family: 'Exo 2', sans-serif !important;
        }}

        /* User messages get a different style */
        [data-testid="stChatMessage"][data-testid*="user"] {{
            border-left-color: #888 !important;
        }}

        /* ── CHAT INPUT ── */
        [data-testid="stChatInput"] {{
            background: var(--surface) !important;
            border: 1px solid var(--accent55) !important;
            border-radius: 12px !important;
            color: var(--txt) !important;
            font-family: 'Share Tech Mono', monospace !important;
            box-shadow: 0 0 20px var(--accent22) !important;
            transition: box-shadow 0.3s ease !important;
        }}
        [data-testid="stChatInput"]:focus-within {{
            box-shadow: 0 0 30px var(--accent55) !important;
            border-color: var(--accent) !important;
        }}
        [data-testid="stChatInput"] textarea {{
            color: var(--txt) !important;
            background: transparent !important;
            font-family: 'Share Tech Mono', monospace !important;
        }}
        [data-testid="stChatInput"] textarea::placeholder {{
            color: var(--accent55) !important;
        }}

        /* ── BUTTONS ── */
        .stButton > button {{
            background: transparent !important;
            border: 1px solid var(--accent55) !important;
            color: var(--accent) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-size: 0.8rem !important;
            letter-spacing: 0.1em !important;
            border-radius: 6px !important;
            padding: 0.4rem 1rem !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            background: var(--accent22) !important;
            border-color: var(--accent) !important;
            box-shadow: 0 0 15px var(--accent55) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}

        /* ── DIVIDER ── */
        hr {{
            border-color: var(--border) !important;
        }}

        /* ── SPINNER ── */
        .stSpinner > div {{
            border-top-color: var(--accent) !important;
        }}

        /* ── ALERTS / WARNINGS ── */
        [data-testid="stAlert"] {{
            background: var(--card) !important;
            border: 1px solid var(--accent55) !important;
            border-radius: 8px !important;
            color: var(--txt) !important;
        }}

        /* ── COLOR PICKERS ── */
        [data-testid="stColorPicker"] {{
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }}

        /* ── SCROLLBAR ── */
        ::-webkit-scrollbar {{ width: 4px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg); }}
        ::-webkit-scrollbar-thumb {{
            background: var(--accent55);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

        /* ── TOAST ── */
        [data-testid="stToast"] {{
            background: var(--card) !important;
            border: 1px solid var(--accent55) !important;
            border-radius: 10px !important;
            color: var(--txt) !important;
            font-family: 'Share Tech Mono', monospace !important;
        }}

        /* ── MAIN CONTENT AREA ── */
        .main .block-container {{
            padding-top: 2rem !important;
            max-width: 900px !important;
        }}

        /* ── IMAGES ── */
        img {{
            border: 1px solid var(--accent55) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 20px var(--accent22) !important;
        }}

        /* ── STATUS BADGE ── */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--card);
            border: 1px solid var(--accent55);
            border-radius: 20px;
            padding: 4px 12px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.72rem;
            color: var(--accent);
            letter-spacing: 0.08em;
        }}
        .status-dot {{
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--accent);
            animation: pulse 1.5s infinite;
        }}

        /* ── STAT CARDS ── */
        .stat-row {{
            display: flex;
            gap: 12px;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}
        .stat-card {{
            flex: 1;
            min-width: 120px;
            background: var(--card);
            border: 1px solid var(--border);
            border-top: 2px solid var(--accent);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            text-align: center;
        }}
        .stat-num {{
            font-family: 'Orbitron', monospace;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--accent);
        }}
        .stat-lbl {{
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.68rem;
            color: var(--txt);
            opacity: 0.6;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-top: 2px;
        }}

        /* ── WELCOME BANNER ── */
        .welcome-banner {{
            background: linear-gradient(135deg, var(--card) 0%, var(--surface) 100%);
            border: 1px solid var(--accent55);
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.82rem;
            color: var(--accent88);
            line-height: 1.8;
            animation: flickerIn 0.6s ease-out;
        }}
        .welcome-banner strong {{
            color: var(--accent) !important;
        }}

        /* ── RESPONSIVE DESIGN ── */
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.4rem !important; margin-bottom: 1rem !important; }}
            .stat-card {{ flex: 1 1 40%; min-width: 40%; padding: 0.5rem; }}
            .stat-num {{ font-size: 1.2rem; }}
            .welcome-banner {{ padding: 1rem; font-size: 0.75rem; }}
            .main .block-container {{ padding-top: 1rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}
            [data-testid="stChatMessage"] {{ padding: 0.75rem !important; }}
        }}

        /* ── ANIMATIONS ── */
        @keyframes flickerIn {{
            0%   {{ opacity: 0; text-shadow: none; }}
            30%  {{ opacity: 0.6; }}
            60%  {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes slideInMsg {{
            from {{ opacity: 0; transform: translateX(-10px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50%       {{ opacity: 0.5; transform: scale(0.8); }}
        }}
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 10px var(--accent22); }}
            50%       {{ box-shadow: 0 0 25px var(--accent55); }}
        }}
        </style>
    """, unsafe_allow_html=True)


# --- 3.5. CONVERSATION STATE + SMARTER INTERACTION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_sensor" not in st.session_state:
    st.session_state.pending_sensor = None
if "show_sensor_list" not in st.session_state:
    st.session_state.show_sensor_list = False
if "theme" not in st.session_state:
    st.session_state.theme = "Black & White"
if "custom_text_color" not in st.session_state:
    st.session_state.custom_text_color = "#E8F4FD"
if "custom_accent_color" not in st.session_state:
    st.session_state.custom_accent_color = "#00D4FF"
if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = False
if "clear_history_confirm" not in st.session_state:
    st.session_state.clear_history_confirm = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(BASE_DIR, "database", "text_data")
IMAGE_DIR = os.path.join(BASE_DIR, "database", "image_data")


def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()


def sensor_key_to_name(file_key):
    return file_key.replace("_", " ")


def extract_field(content, label):
    for line in content.splitlines():
        if line.lower().startswith(label.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def find_sensor_image(file_key):
    for ext in [".jpg", ".png", ".jpeg"]:
        path = os.path.join(IMAGE_DIR, f"{file_key}{ext}")
        if os.path.exists(path):
            return path
    return None


def load_sensor_catalog():
    if not os.path.exists(TEXT_DIR):
        return []

    catalog = []
    for filename in sorted(os.listdir(TEXT_DIR)):
        if not filename.endswith(".txt"):
            continue

        file_key = filename[:-4]
        path = os.path.join(TEXT_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        display_name = extract_field(content, "Sensor Name") or sensor_key_to_name(file_key)
        category = extract_field(content, "Category")
        catalog.append({
            "key": file_key,
            "name": display_name,
            "search_name": sensor_key_to_name(file_key),
            "category": category,
            "content": content,
            "image": find_sensor_image(file_key),
        })

    return catalog


def format_sensor_list(sensors, limit=None):
    shown = sensors[:limit] if limit else sensors
    lines = [f"- `{sensor['name']}` (ID: `{sensor['key']}`)" for sensor in shown]
    if limit and len(sensors) > limit:
        lines.append(f"- ...and {len(sensors) - limit} more")
    return "\n".join(lines)


def is_full_info_request(text):
    lower = normalize_text(text)
    return any(phrase in lower for phrase in [
        "give me", "show me", "show details", "full details", "sensor info",
        "specs", "give me that sensor info", "more info", "details"
    ])


def is_affirmative(text):
    words = normalize_text(text).split()
    return any(word in words for word in ["yes", "sure", "ok", "okay", "yep", "yeah", "please", "goahead", "go", "doit"])


def is_negative(text):
    words = normalize_text(text).split()
    return any(word in words for word in ["no", "not", "dont", "dont", "nope", "nah", "later"])


def summarize_sensor_text(content, lines=3):
    clean_lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    return "\n".join(clean_lines[:lines])


def build_sensor_preview(name, content):
    return (
        f"### 🔎 Sensor found: `{name.upper()}`\n\n"
        f"{summarize_sensor_text(content)}\n\n"
        "I can share the full sensor specification. Reply with "
        "`yes`, `give me that sensor info`, or `show me details`."
    )


def show_full_sensor(sensor_info):
    response = f"### ✅ Full Sensor Information: `{sensor_info['name'].upper()}`\n\n{sensor_info['content']}"
    st.markdown(response)
    if sensor_info.get("image"):
        img = Image.open(sensor_info["image"])
        col1, _ = st.columns([1, 1])
        with col1:
            st.image(img, use_container_width=True)
    st.session_state.messages.append({"role": "assistant", "content": response, "image": sensor_info.get("image")})
    st.session_state.pending_sensor = None


# --- 3. SIDEBAR ---
if "theme" not in st.session_state:
    st.session_state.theme = "Black & White"

with st.sidebar:
    st.markdown("""
        <div style='font-family:"Orbitron",monospace;font-size:1.1rem;font-weight:900;
                    letter-spacing:0.15em;margin-bottom:1rem;'>
            📟 SENSORLAB
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.7rem;
                    opacity:0.5;letter-spacing:0.1em;margin-bottom:1.5rem;'>
            HCI INTERFACE v2.0
        </div>
    """, unsafe_allow_html=True)

    st.subheader("⚙️ Theme Engine")
    new_theme = st.selectbox(
        "Active Theme:",
        ["Black & White", "Cyber Blue", "Carbon", "Deep Purple", "Forest Dark"],
        index=["Black & White", "Cyber Blue", "Carbon", "Deep Purple", "Forest Dark"].index(st.session_state.theme)
    )
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.toast(f"⚡ Theme → {new_theme}", icon="🎨")
        st.rerun()

    st.subheader("🎨 Color Tweaks")
    custom_text_color   = st.color_picker("Text Color",         st.session_state.custom_text_color, key="custom_text_color")
    custom_accent_color = st.color_picker("Accent / Glow Color", st.session_state.custom_accent_color, key="custom_accent_color")

    st.divider()

    # Session stats
    msg_count = len(st.session_state.get("messages", []))
    st.markdown(f"""
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.72rem;
                    opacity:0.55;letter-spacing:0.08em;margin-bottom:0.5rem;'>
            SESSION STATS
        </div>
        <div style='display:flex;gap:8px;margin-bottom:1rem;'>
            <div style='flex:1;background:#1a1a1a;border:1px solid #2a2a2a;
                        border-radius:6px;padding:6px;text-align:center;'>
                <div style='font-family:"Orbitron",monospace;font-size:1.1rem;
                            font-weight:700;color:{custom_accent_color};'>{msg_count}</div>
                <div style='font-family:"Share Tech Mono",monospace;font-size:0.6rem;
                            opacity:0.5;text-transform:uppercase;'>MESSAGES</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Danger Zone with confirmation popup
    st.subheader("🗑️ Danger Zone")
    if "delete_confirm" not in st.session_state:
        st.session_state.delete_confirm = False

    if not st.session_state.delete_confirm:
        if st.button("Reset Session", use_container_width=True):
            st.session_state.delete_confirm = True
            st.rerun()
    else:
        st.warning("⚠️ This will erase all history.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", use_container_width=True):
                st.session_state.messages = []
                st.session_state.delete_confirm = False
                st.toast("Session cleared!", icon="🧹")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.delete_confirm = False
                st.rerun()

    st.divider()
    st.subheader("🔎 Quick Actions")
    if st.button("Show sensor list", use_container_width=True):
        st.session_state.show_sensor_list = not st.session_state.show_sensor_list

    if st.session_state.show_sensor_list:
        sensor_files = load_sensor_catalog()
        st.markdown("**Available sensors:**")
        for sensor in sensor_files:
            st.markdown(f"- `{sensor['name']}`")

    st.divider()
    st.markdown("""
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.65rem;
                    opacity:0.35;letter-spacing:0.06em;line-height:1.8;'>
            QUICK COMMANDS<br>
            › ultrasonic<br>
            › temperature<br>
            › infrared<br>
            › accelerometer<br>
            › hi / hello / salam
        </div>
    """, unsafe_allow_html=True)


# Apply styles
apply_hci_styles(st.session_state.theme, custom_text_color, custom_accent_color)


# --- 4. SENSOR LOGIC ---
def get_chat_response(text):
    lower = normalize_text(text)
    if any(key in lower for key in ["what sensors", "available sensors", "list sensors", "show sensors"]):
        sensors = load_sensor_catalog()
        if sensors:
            return f"I can give details for these {len(sensors)} sensors:\n" + format_sensor_list(sensors)
        return "I don't have sensor text data yet. Please add files under database/text_data."

    responses = {
        "hi":         "Hello! I'm your Sensor Assistant. Type a sensor name to look it up.",
        "hello":      "Hi there! Ready to explore sensors? Try typing 'ultrasonic' or 'temperature'.",
        "salam":      "Walaikum Assalam! How can I help you today?",
        "how are you":"Systems nominal. All databases online. Ready to assist!",
        "help":       "Available commands: type any sensor name, category, or keyword (e.g. 'ultrasonic', 'temperature', 'gas', 'accelerometer'). Use 'list sensors' to show everything.",
        "what can you do": "I can guide you through sensor data, answer general instructions, and give full sensor details when you ask for them.",
    }
    return responses.get(lower)

def get_sensor_matches(user_input):
    query = normalize_text(user_input)
    if not query:
        return []

    catalog = load_sensor_catalog()
    if not catalog:
        return []

    def searchable(sensor):
        return normalize_text(" ".join([
            sensor["name"],
            sensor["search_name"],
            sensor.get("category", ""),
            sensor["content"],
        ]))

    for sensor in catalog:
        if query == normalize_text(sensor["key"]):
            return [sensor]

    exact = [
        sensor for sensor in catalog
        if query in {
            normalize_text(sensor["name"]),
            normalize_text(sensor["search_name"]),
        }
    ]
    if exact:
        return exact

    name_matches = [
        sensor for sensor in catalog
        if query in normalize_text(sensor["name"])
        or query in normalize_text(sensor["search_name"])
        or query in normalize_text(sensor.get("category", ""))
    ]
    if name_matches:
        return name_matches

    content_matches = [sensor for sensor in catalog if query in searchable(sensor)]
    if content_matches:
        return content_matches

    names = [sensor["search_name"] for sensor in catalog]
    fuzzy_names = difflib.get_close_matches(query, names, n=8, cutoff=0.45)
    return [sensor for sensor in catalog if sensor["search_name"] in fuzzy_names]


def get_sensor_data(user_input):
    matches = get_sensor_matches(user_input)
    if len(matches) != 1:
        return None, None, None

    sensor = matches[0]
    return sensor["content"], sensor["image"], sensor["name"]


def build_multi_match_response(matches, user_input):
    return (
        f"### Multiple sensors matched `{user_input}`\n\n"
        f"I found {len(matches)} matching sensors. Type the exact **ID** to open one:\n\n"
        f"{format_sensor_list(matches, limit=25)}"
    )


# --- 5. MAIN UI ---

# Title + status bar
st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;'>
        <div>
            <h1 style='margin:0;'>🕹️ SENSORLAB TERMINAL</h1>
        </div>
        <div class='status-badge'>
            <div class='status-dot'></div>
            SYSTEM ONLINE
        </div>
    </div>
""", unsafe_allow_html=True)

# Stat bar
total_sensors = 0
if os.path.exists(TEXT_DIR):
    total_sensors = len([f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")])

st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-card'>
            <div class='stat-num'>{total_sensors}</div>
            <div class='stat-lbl'>Sensors DB</div>
        </div>
        <div class='stat-card'>
            <div class='stat-num'>{len(st.session_state.get("messages", []))}</div>
            <div class='stat-lbl'>Messages</div>
        </div>
        <div class='stat-card'>
            <div class='stat-num' style='font-size:0.95rem;'>✓</div>
            <div class='stat-lbl'>DB Status</div>
        </div>
        <div class='stat-card'>
            <div class='stat-num' style='font-size:0.95rem;'>v2.0</div>
            <div class='stat-lbl'>Version</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Welcome banner (only on first visit)
if "welcomed" not in st.session_state:
    st.markdown("""
        <div class='welcome-banner'>
            <strong>▸ SENSORLAB HCI TERMINAL INITIALIZED</strong><br>
            Type a sensor name (e.g. <strong>ultrasonic</strong>, <strong>infrared</strong>, <strong>temperature</strong>) to query the database.<br>
            Fuzzy matching enabled — approximate names are accepted.<br>
            Type <strong>help</strong> for a command overview.
        </div>
    """, unsafe_allow_html=True)
    st.session_state.welcomed = True

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

control_col1, control_col2 = st.columns([1, 1])
with control_col1:
    if not st.session_state.clear_history_confirm:
        if st.button("🧹 Clear chat history", use_container_width=True):
            st.session_state.clear_history_confirm = True
            st.experimental_rerun()
    else:
        st.warning("⚠️ This will erase all chat history.")
        confirm_col, cancel_col = st.columns([1, 1])
        with confirm_col:
            if st.button("✅ Confirm clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.pending_sensor = None
                st.session_state.clear_history_confirm = False
                st.toast("Chat history cleared.", icon="🧹")
                st.experimental_rerun()
        with cancel_col:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.clear_history_confirm = False
                st.experimental_rerun()
with control_col2:
    if st.button("🗑️ Delete last message", use_container_width=True):
        if st.session_state.messages:
            st.session_state.messages.pop()
            st.toast("Last message removed.", icon="🗑️")
            st.experimental_rerun()
        else:
            st.toast("No messages to remove.", icon="⚠️")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"):
            col1, _ = st.columns([1, 1])
            with col1:
                st.image(msg["image"], use_container_width=True)

# Input handler
if prompt := st.chat_input("⟩ Enter sensor name or command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        matches = get_sensor_matches(prompt)
        if len(matches) == 1:
            sensor_match = matches[0]
            text, img_path, match = sensor_match["content"], sensor_match["image"], sensor_match["name"]
        else:
            text, img_path, match = None, None, None
        if st.session_state.pending_sensor and (is_full_info_request(prompt) or is_affirmative(prompt)):
            show_full_sensor(st.session_state.pending_sensor)
        elif st.session_state.pending_sensor and is_negative(prompt):
            msg = "No problem — I am ready when you are. Ask me about another sensor or type a sensor name."
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state.pending_sensor = None
        elif greet := get_chat_response(prompt):
            st.markdown(greet)
            st.session_state.messages.append({"role": "assistant", "content": greet})
        elif text:
            sensor_info = {"name": match, "content": text, "image": img_path}
            if is_full_info_request(prompt):
                show_full_sensor(sensor_info)
            else:
                preview = build_sensor_preview(match, text)
                st.markdown(preview)
                if img_path:
                    img = Image.open(img_path)
                    col1, _ = st.columns([1, 1])
                    with col1:
                        st.image(img, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": preview, "image": img_path})
                st.session_state.pending_sensor = sensor_info
        elif len(matches) > 1:
            msg = build_multi_match_response(matches, prompt)
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            if st.session_state.pending_sensor and is_full_info_request(prompt):
                show_full_sensor(st.session_state.pending_sensor)
            else:
                sensor_files = load_sensor_catalog()
                suggestion = "Try a sensor name like `ultrasonic`, `temperature`, or `infrared`."
                if sensor_files:
                    suggestion += "\n\nAvailable sensors: " + ", ".join([f"`{sensor['name']}`" for sensor in sensor_files[:7]])
                err = f"""**⚠ NO MATCH FOUND**

`{prompt}` did not match any sensor in the database.

{suggestion}"""
                st.warning(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
