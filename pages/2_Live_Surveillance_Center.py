import streamlit as st
from datetime import datetime

# Real supermarket / surveillance images
CAMS = [
    ("https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=640&q=80", "CAM-01","Main Entrance","Normal","1080p 30fps"),
    ("https://images.unsplash.com/photo-1534723452862-4c874986d5d8?w=640&q=80", "CAM-02","Aisle A - Electronics","Alert","1080p 30fps"),
    ("https://images.unsplash.com/photo-1551218808-94e220e084d2?w=640&q=80", "CAM-03","Checkout Zone","Normal","720p 25fps"),
    ("https://images.unsplash.com/photo-1582139329536-e7284fece509?w=640&q=80", "CAM-04","Storage Corridor","Normal","720p 25fps"),
]

def show():
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon" style="background:linear-gradient(135deg,#0EA5E9,#0284C7);">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
      </div>
      <div>
        <h1>Live Surveillance Center</h1>
        <p class="subtitle">Control room - 4 active camera feeds</p>
      </div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("Active Cameras","4","All feeds nominal","#10B981"),
        ("Current Alerts","2","Awaiting review","#EF4444"),
        ("System Uptime","12d 4h","99.8% availability","#0891B2"),
        ("Recording","LIVE","All cameras active","#F59E0B"),
    ]
    for col, (label, val, delta, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div style="background:#0D1117;border:1px solid #1E2D3D;border-radius:8px;
                        padding:1rem;border-top:2px solid {color};">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;text-transform:uppercase;
                          letter-spacing:0.1em;color:#475569;margin-bottom:0.3rem;">{label}</div>
              <div style="font-size:1.45rem;font-weight:700;color:#F1F5F9;">{val}</div>
              <div style="font-size:0.7rem;color:#334155;margin-top:0.25rem;">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.75rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Camera Feeds - Simulated Preview</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    for i, (img_url, cam_id, location, status, spec) in enumerate(CAMS):
        col = col_a if i % 2 == 0 else col_b
        is_alert   = status == "Alert"
        s_color    = "#EF4444" if is_alert else "#10B981"
        border_col = "rgba(239,68,68,0.4)" if is_alert else "rgba(16,185,129,0.18)"
        with col:
            st.markdown(f"""
            <div style="border-radius:8px;overflow:hidden;border:1px solid {border_col};margin-bottom:1rem;">
              <div style="position:relative;">
                <img src="{img_url}" style="width:100%;height:190px;object-fit:cover;filter:brightness(0.48);">
                <div style="position:absolute;top:0.5rem;left:0.6rem;display:flex;align-items:center;
                            gap:0.35rem;background:rgba(0,0,0,0.65);border-radius:4px;padding:0.2rem 0.5rem;">
                  <div style="width:6px;height:6px;background:#EF4444;border-radius:50%;animation:pulse-dot 1s infinite;"></div>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#EF4444;">REC</span>
                </div>
                {"<div style=\"position:absolute;top:0.5rem;right:0.6rem;background:rgba(239,68,68,0.85);border-radius:4px;padding:0.2rem 0.6rem;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#FFF;text-transform:uppercase;letter-spacing:0.06em;\">ALERT</div>" if is_alert else ""}
                <div style="position:absolute;bottom:0;left:0;right:0;
                            background:linear-gradient(to top,rgba(0,0,0,0.85),transparent);
                            padding:0.75rem 0.9rem;">
                  <div style="color:#F1F5F9;font-weight:600;font-size:0.85rem;">{cam_id} - {location}</div>
                  <div style="color:#64748B;font-family:'IBM Plex Mono',monospace;font-size:0.62rem;">{spec}</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;
                          background:#0D1117;padding:0.6rem 0.9rem;">
                <span style="color:#475569;font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                             text-transform:uppercase;">{cam_id}</span>
                <span style="display:flex;align-items:center;gap:0.3rem;">
                  <div style="width:6px;height:6px;background:{s_color};border-radius:50%;"></div>
                  <span style="color:{s_color};font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                               text-transform:uppercase;">{status}</span>
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">AI Alert Stream</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    now = datetime.now().strftime("%H:%M:%S")
    alerts = [
        (now,"CAM-02","High","Suspicious loitering detected near electronics shelf - probability 87%"),
        (now,"CAM-02","High","Bag concealment motion pattern identified - probability 79%"),
        (now,"CAM-01","Medium","Unattended item flagged at store entrance - probability 61%"),
        (now,"CAM-03","Low","Extended checkout dwell time detected - probability 38%"),
    ]
    colors = {"High":"#EF4444","Medium":"#F59E0B","Low":"#0891B2"}
    bg     = {"High":"rgba(239,68,68,0.05)","Medium":"rgba(245,158,11,0.05)","Low":"rgba(14,165,233,0.05)"}
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    for t, cam, level, msg in alerts:
        c = colors[level]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1rem;padding:0.75rem 0.9rem;
                    background:{bg[level]};border-bottom:1px solid #1A2535;">
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:#475569;flex-shrink:0;">{t}</span>
          <span style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:{c};
                       text-transform:uppercase;flex-shrink:0;">{cam}</span>
          <span style="color:#94A3B8;font-size:0.8rem;flex:1;">{msg}</span>
          <span style="background:rgba(0,0,0,0.3);color:{c};border:1px solid {c};border-radius:4px;
                       padding:0.1rem 0.5rem;font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                       text-transform:uppercase;flex-shrink:0;">{level}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#1E3A5F;font-size:0.72rem;font-family:'IBM Plex Mono',monospace;
                padding:0.75rem 0;text-align:center;text-transform:uppercase;letter-spacing:0.08em;">
      Production deployment streams live CCTV via RTSP with real-time CNN-BiLSTM inference per frame
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
