"""
Reporly UI — Custom CSS + HTML component helpers.
Injects modern dark theme on top of Streamlit's default styling.
Reference: Ops/UX-REFERENCE.md (color system, typography, spacing, animations).
"""
import streamlit as st


# ---------------------------------------------------------------------------
# CSS Injection
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
/* === FONTS === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* === BACKGROUND === */
.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: #111118;
    border-right: 1px solid #222;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label {
    color: #a0a0a0;
    font-size: 13px;
    font-weight: 500;
}

/* === HEADER AREA === */
h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.4rem !important;
    letter-spacing: -0.02em;
}
h2 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #f0f0f0 !important;
    font-size: 1.4rem !important;
}
h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    color: #e0e0e0 !important;
}

/* === METRIC CARDS === */
div[data-testid="stMetric"] {
    background: rgba(26, 26, 26, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 20px 16px;
    transition: all 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(6, 182, 212, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(6, 182, 212, 0.1);
}
div[data-testid="stMetric"] label {
    color: #888 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
    color: #f0f0f0 !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #141418;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #222;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    color: #888;
    transition: all 0.15s ease;
}
.stTabs [aria-selected="true"] {
    background: rgba(6, 182, 212, 0.15) !important;
    color: #06b6d4 !important;
    font-weight: 600;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #ccc;
    background: rgba(255, 255, 255, 0.05);
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #06b6d4 !important;
}

/* === BUTTONS === */
.stButton > button[kind="primary"],
.stDownloadButton > button {
    background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em;
}
.stButton > button[kind="primary"]:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(6, 182, 212, 0.4) !important;
}
.stButton > button[kind="primary"]:active,
.stDownloadButton > button:active {
    transform: scale(0.98) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #a0a0a0 !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #06b6d4 !important;
    color: #06b6d4 !important;
}

/* === FILE UPLOADER === */
section[data-testid="stFileUploader"] {
    border: 2px dashed #333 !important;
    border-radius: 16px !important;
    padding: 32px !important;
    transition: all 0.2s ease;
}
section[data-testid="stFileUploader"]:hover {
    border-color: #06b6d4 !important;
    background: rgba(6, 182, 212, 0.03);
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    background: #1a1a1a !important;
    border-radius: 8px !important;
    border: 1px solid #282828 !important;
}

/* === DATAFRAME === */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #282828;
}

/* === PROGRESS BAR === */
.stProgress > div > div {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
    border-radius: 8px;
}

/* === DIVIDER === */
hr {
    border-color: #222 !important;
}

/* === ANIMATIONS === */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.fade-in-up {
    animation: fadeInUp 0.4s ease forwards;
}

/* === CUSTOM COMPONENTS (via st.markdown) === */
.rp-hero-badge {
    display: inline-block;
    background: rgba(6, 182, 212, 0.1);
    color: #06b6d4;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.02em;
    border: 1px solid rgba(6, 182, 212, 0.2);
}
.rp-insight-card {
    background: rgba(26, 26, 26, 0.6);
    backdrop-filter: blur(8px);
    border: 1px solid #282828;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}
.rp-insight-card:hover {
    border-color: rgba(6, 182, 212, 0.2);
}
.rp-insight-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #f0f0f0;
    margin-bottom: 8px;
}
.rp-insight-desc {
    font-size: 13px;
    color: #a0a0a0;
    line-height: 1.6;
}
.rp-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.rp-badge-high   { background: rgba(239,68,68,0.15); color: #ef4444; }
.rp-badge-medium { background: rgba(234,179,8,0.15); color: #eab308; }
.rp-badge-low    { background: rgba(34,197,94,0.15); color: #22c55e; }
.rp-template-card {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.2s ease;
    cursor: default;
}
.rp-template-card:hover {
    border-color: #06b6d4;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.rp-template-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 16px;
    color: #f0f0f0;
    margin-top: 12px;
}
.rp-template-desc {
    font-size: 12px;
    color: #888;
    margin-top: 4px;
}
.rp-step-card {
    background: rgba(26, 26, 26, 0.6);
    border: 1px solid #282828;
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.2s ease;
}
.rp-step-card:hover {
    border-color: rgba(6, 182, 212, 0.2);
    transform: translateY(-2px);
}
.rp-step-icon {
    font-size: 28px;
    margin-bottom: 8px;
}
.rp-step-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #f0f0f0;
}
.rp-step-desc {
    font-size: 13px;
    color: #888;
    margin-top: 4px;
}
</style>
"""


def inject_custom_css():
    """Inject custom CSS into the Streamlit app. Call once at top of main()."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HTML Component Helpers
# ---------------------------------------------------------------------------

def insight_card(index: int, title: str, description: str, importance: str) -> None:
    """Render a styled insight card with importance badge."""
    badge_class = f"rp-badge-{importance}"
    st.markdown(f"""
    <div class="rp-insight-card">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <span style="color:#555; font-weight:700; font-size:14px;">#{index}</span>
            <span class="rp-insight-title" style="flex:1;">{title}</span>
            <span class="rp-badge {badge_class}">{importance}</span>
        </div>
        <div class="rp-insight-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def template_preview_card(name: str, primary: str, accent: str, desc: str) -> None:
    """Render a template preview card with color swatch."""
    st.markdown(f"""
    <div class="rp-template-card">
        <div style="display:flex; gap:6px; justify-content:center;">
            <div style="width:32px; height:32px; border-radius:8px; background:{primary};"></div>
            <div style="width:32px; height:32px; border-radius:8px; background:{accent};"></div>
        </div>
        <div class="rp-template-name">{name}</div>
        <div class="rp-template-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def welcome_step_card(icon: str, title: str, desc: str) -> None:
    """Render a step card for the welcome screen.
    NOTE: icon must be HTML-safe (SVG, emoji, or HTML entity). Streamlit
    :material/name: shortcodes do NOT render inside unsafe_allow_html blocks.
    """
    st.markdown(f"""
    <div class="rp-step-card">
        <div class="rp-step-icon">{icon}</div>
        <div class="rp-step-title">{title}</div>
        <div class="rp-step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
