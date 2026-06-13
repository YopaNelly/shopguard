"""
Access control for ShopGuard AI.
Three roles as described in the project documentation:
  - admin       Full access including model info, architecture, reports, history
  - operator    Video analysis, dashboard, analytics, live feed, alerts
  - viewer      Dashboard and detection history read-only
Passwords are stored as bcrypt hashes. For the prototype they are hardcoded here;
in production replace with a database lookup.

To generate a new hash in a Python shell:
    import hashlib
    hashlib.sha256("your_password".encode()).hexdigest()
"""
import streamlit as st
import hashlib

# ── User database ─────────────────────────────────────────────────────────────
# Format: username → {"password_hash": sha256(password), "role": role, "name": display_name}
_USERS = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role":  "admin",
        "name":  "Administrator",
    },
    "ngadou": {
        "password_hash": hashlib.sha256("shopguard2024".encode()).hexdigest(),
        "role":  "admin",
        "name":  "Ngadou (Project Author)",
    },
    "security1": {
        "password_hash": hashlib.sha256("security123".encode()).hexdigest(),
        "role":  "operator",
        "name":  "Security Officer",
    },
    "viewer": {
        "password_hash": hashlib.sha256("view2024".encode()).hexdigest(),
        "role":  "viewer",
        "name":  "Store Manager (Read-Only)",
    },
}

# ── Role permissions ──────────────────────────────────────────────────────────
# Maps role → list of allowed page names (matching nav_items keys in app.py)
_ROLE_PAGES = {
    "admin": [
        "Dashboard", "Live Surveillance", "Video Analysis",
        "Detection Results", "Analytics", "AI Model Info",
        "Architecture", "Detection History", "Reports",
        "Roadmap", "About",
    ],
    "operator": [
        "Dashboard", "Live Surveillance", "Video Analysis",
        "Detection Results", "Analytics", "Detection History",
        "Reports", "About",
    ],
    "viewer": [
        "Dashboard", "Detection History", "About",
    ],
}


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login_page():
    """
    Render the login form. Stores authenticated user info in st.session_state.
    Call this at the top of app.py before rendering any other content.
    """
    st.markdown("""
    <style>
    .login-wrap {
        max-width: 420px;
        margin: 6vh auto 0;
        padding: 2.5rem 2.5rem 2rem;
        background: #0D1117;
        border: 1px solid #1E2D3D;
        border-radius: 14px;
    }
    .login-logo {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.75rem;
    }
    .login-logo-icon {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #0891B2, #0369A1);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
    }
    .login-title  { color: #F1F5F9; font-size: 1.3rem; font-weight: 700; line-height: 1; }
    .login-sub    { color: #475569; font-size: 0.68rem; font-family: 'IBM Plex Mono', monospace;
                    text-transform: uppercase; letter-spacing: 0.1em; }
    .login-hint   { background: rgba(8,145,178,0.07); border: 1px solid rgba(8,145,178,0.18);
                    border-radius: 7px; padding: 0.75rem 1rem; margin-bottom: 1.25rem;
                    color: #64748B; font-size: 0.78rem; line-height: 1.6; }
    .login-hint strong { color: #0891B2; }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div class="login-wrap">
          <div class="login-logo">
            <div class="login-logo-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                   stroke="white" stroke-width="2.2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div>
              <div class="login-title">ShopGuard AI</div>
              <div class="login-sub">Surveillance Platform</div>
            </div>
          </div>
          <div class="login-hint">
            <strong>Demo credentials:</strong><br>
            Admin &nbsp;&nbsp;: <strong>admin</strong> / <strong>admin123</strong><br>
            Operator: <strong>security1</strong> / <strong>security123</strong><br>
            Viewer &nbsp;: <strong>viewer</strong> / <strong>view2024</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

        if submitted:
            user = _USERS.get(username.strip().lower())
            if user and user["password_hash"] == _hash(password):
                st.session_state["authenticated"] = True
                st.session_state["username"]      = username.strip().lower()
                st.session_state["user_role"]     = user["role"]
                st.session_state["user_name"]     = user["name"]
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")


def logout():
    """Clear authentication state."""
    for key in ["authenticated", "username", "user_role", "user_name"]:
        st.session_state.pop(key, None)
    st.rerun()


def require_auth():
    """
    Call at top of app.py.
    If not authenticated, show login page and stop execution.
    Returns True if authenticated.
    """
    if not st.session_state.get("authenticated"):
        login_page()
        st.stop()
    return True


def get_allowed_pages() -> list:
    """Return the list of pages the current user may access."""
    role = st.session_state.get("user_role", "viewer")
    return _ROLE_PAGES.get(role, _ROLE_PAGES["viewer"])


def can_access(page_name: str) -> bool:
    """Check whether current user can access a given page."""
    return page_name in get_allowed_pages()


def role_badge() -> str:
    """Return an HTML badge for the current user's role (for sidebar display)."""
    role = st.session_state.get("user_role", "viewer")
    name = st.session_state.get("user_name", "User")
    colours = {
        "admin":    ("#0891B2", "rgba(8,145,178,0.12)"),
        "operator": ("#10B981", "rgba(16,185,129,0.12)"),
        "viewer":   ("#64748B", "rgba(100,116,139,0.12)"),
    }
    col, bg = colours.get(role, colours["viewer"])
    return (
        f'<div style="background:{bg};border:1px solid {col}22;border-radius:7px;'
        f'padding:0.55rem 0.85rem;margin-bottom:1.1rem;">'
        f'<div style="color:{col};font-family:\'IBM Plex Mono\',monospace;font-size:0.6rem;'
        f'text-transform:uppercase;letter-spacing:0.1em;">{role}</div>'
        f'<div style="color:#94A3B8;font-size:0.8rem;margin-top:0.15rem;">{name}</div>'
        f'</div>'
    )
