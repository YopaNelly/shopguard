import streamlit as st
import os
import importlib.util

st.set_page_config(
    page_title="ShopGuard AI - Surveillance Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth (must come before any other rendering) ───────────────────────────────
from utils.auth import require_auth, get_allowed_pages, role_badge, logout

require_auth()   # shows login page and stops if not authenticated


# ── CSS ───────────────────────────────────────────────────────────────────────
def load_css():
    css_file = "css/style.css"
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── Session defaults ──────────────────────────────────────────────────────────
for key, default in [
    ("last_analysis",   None),
    ("sender_email",    ""),
    ("sender_password", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── ALL pages (full list) ─────────────────────────────────────────────────────
ALL_PAGES = {
    "Dashboard":         "pages/1_Executive_Dashboard.py",
    "Live Surveillance": "pages/2_Live_Surveillance_Center.py",
    "Video Analysis":    "pages/3_Video_Analysis.py",
    "Detection Results": "pages/4_Detection_Results.py",
    "Analytics":         "pages/5_Analytics_Center.py",
    "AI Model Info":     "pages/6_AI_Model_Information.py",
    "Architecture":      "pages/7_System_Architecture.py",
    "Detection History": "pages/8_Detection_History.py",
    "Reports":           "pages/9_Reports_Center.py",
    "Roadmap":           "pages/10_Future_Improvements.py",
    "About":             "pages/11_About_Project.py",
}

# Filter pages by role
allowed = get_allowed_pages()
nav_items = {k: v for k, v in ALL_PAGES.items() if k in allowed}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.75rem 0 1.25rem;">
      <div style="display:flex;align-items:center;gap:0.75rem;">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,#0891B2,#0369A1);
                    border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </div>
        <div>
          <div style="color:#F1F5F9;font-weight:700;font-size:0.95rem;letter-spacing:-0.01em;line-height:1;">
            SHOPGUARD AI</div>
          <div style="color:#334155;font-size:0.6rem;font-family:'IBM Plex Mono',monospace;
                      text-transform:uppercase;letter-spacing:0.1em;">Surveillance Platform</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;padding:0.45rem 0.75rem;
                background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);
                border-radius:6px;margin-bottom:1rem;">
      <div style="width:7px;height:7px;background:#10B981;border-radius:50%;"></div>
      <span style="color:#10B981;font-family:'IBM Plex Mono',monospace;font-size:0.67rem;
                   text-transform:uppercase;letter-spacing:0.08em;">System Online</span>
    </div>""", unsafe_allow_html=True)

    # Role badge
    st.markdown(role_badge(), unsafe_allow_html=True)

    st.markdown(
        '<div style="color:#334155;font-size:0.62rem;font-family:\'IBM Plex Mono\',monospace;'
        'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Navigation</div>',
        unsafe_allow_html=True,
    )

    selected = st.radio(
        "nav",
        list(nav_items.keys()),
        label_visibility="collapsed",
        index=0,
        key="nav_radio",
    )

    st.markdown("<hr style='border-color:#1E2D3D;margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:0.5rem 0;">
      <div style="color:#334155;font-size:0.6rem;font-family:'IBM Plex Mono',monospace;
                  text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Model</div>
      <div style="color:#475569;font-size:0.73rem;line-height:1.6;">
        CNN-BiLSTM<br>
        <span style="color:#334155;">MobileNetV2 backbone</span><br>
        <span style="color:#334155;">UCF-Crime dataset</span><br>
        <span style="color:#10B981;font-weight:600;">83.33% recall</span>
      </div>
    </div>
    <div style="margin-top:0.75rem;color:#1E3A5F;font-size:0.6rem;font-family:'IBM Plex Mono',monospace;">
      NAHPI - University of Bamenda
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E2D3D;margin:1rem 0;'>", unsafe_allow_html=True)

    if st.button("Sign Out", use_container_width=True):
        logout()


# ── Main content ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

page_path = nav_items[selected]
try:
    if os.path.exists(page_path):
        spec = importlib.util.spec_from_file_location("page_module", page_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.show()
    else:
        st.error(f"Page file not found: {page_path}")
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

st.markdown('</div>', unsafe_allow_html=True)
