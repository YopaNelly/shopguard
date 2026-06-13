import streamlit as st

ROADMAP_IMG = "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&q=80"
EDGE_IMG    = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80"
MOBILE_IMG  = "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600&q=80"
CLOUD_IMG   = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80"

def show():
    st.markdown(f"""
    <div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:2rem;height:170px;">
      <img src="{ROADMAP_IMG}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.25);">
      <div style="position:absolute;inset:0;padding:1.75rem 2.5rem;display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;text-transform:uppercase;
                    letter-spacing:0.14em;color:#0891B2;margin-bottom:0.35rem;">Development Roadmap</div>
        <div style="font-size:1.55rem;font-weight:700;color:#FFFFFF;">Roadmap and Future Improvements</div>
        <div style="color:#94A3B8;font-size:0.8rem;margin-top:0.3rem;">
          Planned enhancements to evolve ShopGuard AI into a full enterprise surveillance platform.
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Vision images
    col1, col2, col3 = st.columns(3)
    for col, img, title, desc in [
        (col1, EDGE_IMG,   "Edge AI Deployment",      "On-device inference on NVIDIA Jetson Nano at camera level - no cloud required."),
        (col2, MOBILE_IMG, "Mobile App Monitoring",   "Flutter cross-platform app for real-time remote monitoring and instant push alerts."),
        (col3, CLOUD_IMG,  "Cloud AI Infrastructure", "Auto-scaling inference with multi-tenant architecture for chain supermarket networks."),
    ]:
        with col:
            st.markdown(f"""
            <div style="border-radius:8px;overflow:hidden;border:1px solid #1E2D3D;margin-bottom:1.5rem;">
              <img src="{img}" style="width:100%;height:120px;object-fit:cover;filter:brightness(0.4);">
              <div style="padding:0.85rem 1rem;background:#0D1117;">
                <div style="color:#F1F5F9;font-weight:600;font-size:0.85rem;margin-bottom:0.3rem;">{title}</div>
                <div style="color:#64748B;font-size:0.78rem;line-height:1.5;">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Development Phases</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    phases = [
        ("Phase 1", "Current",   "Streamlit Prototype",      "CNN-BiLSTM video detection, dashboard, email alerts, PDF reports.",                          True),
        ("Phase 2", "Near-term", "Enterprise Backend",        "Django REST Framework with role-based access control, JWT authentication, and REST API.",    False),
        ("Phase 3", "Near-term", "Persistent Database",       "PostgreSQL with cloud object storage (AWS S3 or Backblaze) for scalable detection history.", False),
        ("Phase 4", "Mid-term",  "Real-time RTSP Streaming",  "Live CCTV feed integration via RTSP/WebRTC with per-frame CNN-BiLSTM inference.",           False),
        ("Phase 5", "Mid-term",  "WhatsApp and SMS Alerts",   "Instant WhatsApp notifications via the Meta API and SMS via Africa's Talking gateway.",     False),
        ("Phase 6", "Mid-term",  "Mobile Application",        "Flutter app for Android and iOS providing remote monitoring, alerts, and live feeds.",       False),
        ("Phase 7", "Long-term", "Edge AI on Jetson Nano",    "On-device inference at camera level using NVIDIA Jetson Nano for zero-latency detection.",  False),
        ("Phase 8", "Long-term", "Multi-Store Command Center","Centralised monitoring dashboard covering chain supermarket networks across Cameroon.",      False),
        ("Phase 9", "Long-term", "Federated Cloud Platform",  "Auto-scaling multi-tenant cloud inference with continuous model retraining from local data.",False),
    ]

    for phase, timeline, title, desc, current in phases:
        badge_col  = "#10B981" if current else "#0891B2"
        border_col = "rgba(16,185,129,0.25)" if current else "rgba(14,165,233,0.12)"
        badge_text = "Current Version" if current else timeline
        st.markdown(f"""
        <div style="border:1px solid {border_col};background:#0D1117;border-radius:8px;
                    padding:1rem 1.25rem;margin-bottom:0.65rem;display:flex;align-items:flex-start;gap:1rem;">
          <div style="flex-shrink:0;width:62px;text-align:center;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;text-transform:uppercase;
                        letter-spacing:0.08em;color:#475569;margin-bottom:0.25rem;">{phase}</div>
            <div style="background:rgba(0,0,0,0);border:1px solid {badge_col};border-radius:4px;
                        color:{badge_col};font-family:'IBM Plex Mono',monospace;font-size:0.55rem;
                        text-transform:uppercase;padding:0.15rem 0.3rem;letter-spacing:0.06em;">{badge_text}</div>
          </div>
          <div style="flex:1;">
            <div style="color:#F1F5F9;font-weight:600;font-size:0.88rem;margin-bottom:0.25rem;">{title}</div>
            <div style="color:#64748B;font-size:0.8rem;line-height:1.55;">{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="border:1px solid rgba(14,165,233,0.18);background:rgba(14,165,233,0.04);
                border-radius:8px;padding:1rem 1.5rem;margin-top:1rem;text-align:center;">
      <div style="color:#F1F5F9;font-weight:700;font-size:1.1rem;">Target Outcome</div>
      <div style="color:#10B981;font-size:1.5rem;font-weight:700;margin:0.25rem 0;">65% reduction in shoplifting losses</div>
      <div style="color:#64748B;font-size:0.82rem;">
        across Cameroonian retail environments by 2027 through progressive deployment of all nine phases.
      </div>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
