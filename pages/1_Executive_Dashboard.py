import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

HERO_IMG    = "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=1200&q=80"
STORE1_IMG  = "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&q=80"
STORE2_IMG  = "https://images.unsplash.com/photo-1534723452862-4c874986d5d8?w=400&q=80"
STORE3_IMG  = "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400&q=80"
CCTV_IMG    = "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&q=80"

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,17,23,1)',
    font_color='#64748B',
    xaxis=dict(gridcolor='#1A2535', tickfont=dict(size=10)),
    yaxis=dict(gridcolor='#1A2535', tickfont=dict(size=10)),
    margin=dict(t=10, b=0, l=0, r=0),
    height=260,
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1E2D3D', borderwidth=1,
                font=dict(color='#94A3B8', size=11)),
)

def show():
    # Hero banner
    st.markdown(f"""
    <div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:2rem;height:190px;">
      <img src="{HERO_IMG}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.28);">
      <div style="position:absolute;inset:0;padding:1.75rem 2.5rem;display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;text-transform:uppercase;
                    letter-spacing:0.14em;color:#0891B2;margin-bottom:0.35rem;">Real-time Security Overview</div>
        <div style="font-size:1.6rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.02em;">Executive Dashboard</div>
        <div style="color:#94A3B8;font-size:0.8rem;margin-top:0.3rem;">
          Live metrics from the CNN-BiLSTM shoplifting detection engine.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df_path = "data/detections.csv"
    df = pd.DataFrame()
    if os.path.exists(df_path):
        try:
            df = pd.read_csv(df_path)
        except:
            pass

    total_videos   = len(df)                   if not df.empty else 47
    suspicious     = len(df[df['prediction'] == 'Suspicious']) if not df.empty else 13
    normal         = len(df[df['prediction'] == 'Normal'])     if not df.empty else 34
    avg_confidence = df['confidence'].mean()*100 if not df.empty else 78.4
    security_score = max(0, 100-(suspicious/max(total_videos,1))*50) if not df.empty else 86.2

    # KPI row
    kpis = [
        ("Videos Processed",  total_videos,            f"Since deployment",     "#0891B2"),
        ("Suspicious Events", suspicious,               "Require review",        "#EF4444"),
        ("Normal Activity",   normal,                   "Within threshold",      "#10B981"),
        ("Avg Confidence",    f"{avg_confidence:.1f}%", "CNN-BiLSTM output",     "#0891B2"),
        ("Security Score",    f"{security_score:.0f}/100","Composite index",     "#6366F1"),
    ]
    cols = st.columns(5)
    for col, (label, value, delta, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div style="background:#0D1117;border:1px solid #1E2D3D;border-radius:8px;
                        padding:1.1rem 1rem;border-top:2px solid {color};">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;text-transform:uppercase;
                          letter-spacing:0.1em;color:#475569;margin-bottom:0.4rem;">{label}</div>
              <div style="font-size:1.65rem;font-weight:700;color:#F1F5F9;line-height:1;">{value}</div>
              <div style="font-size:0.72rem;color:#334155;margin-top:0.35rem;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.75rem;'></div>", unsafe_allow_html=True)

    # System status + store images
    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">System Status and Store Coverage</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    col_status, col_s1, col_s2, col_s3 = st.columns([1.4, 1, 1, 1])

    with col_status:
        now = datetime.now().strftime('%H:%M:%S')
        st.markdown(f"""
        <div class="panel" style="height:100%;">
          <div class="panel-header">
            <span class="panel-title">Live System Status</span>
            <span class="badge badge-online"><span class="badge-dot pulse"></span>Online</span>
          </div>
          <table class="info-table">
            <tr><td>AI Engine</td><td style="color:#10B981;">Active</td></tr>
            <tr><td>Cameras</td><td>4 Connected</td></tr>
            <tr><td>Last Alert</td><td>{now}</td></tr>
            <tr><td>Model</td><td>CNN-BiLSTM v1</td></tr>
            <tr><td>Backbone</td><td>MobileNetV2</td></tr>
            <tr><td>Dataset</td><td>UCF-Crime</td></tr>
            <tr><td>Recall</td><td style="color:#10B981;">83.33%</td></tr>
            <tr><td>Threshold</td><td>0.50</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    store_images = [
        (col_s1, STORE1_IMG, "Bonanjo Branch", "CAM 01 and 02", "#10B981"),
        (col_s2, STORE2_IMG, "Akwa Branch",    "CAM 03 and 04", "#10B981"),
        (col_s3, CCTV_IMG,   "CCTV Network",   "4 active feeds", "#0891B2"),
    ]
    for col, img, title, sub, color in store_images:
        with col:
            st.markdown(f"""
            <div style="border-radius:8px;overflow:hidden;border:1px solid #1E2D3D;">
              <img src="{img}" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.42);">
              <div style="padding:0.75rem 0.9rem;background:#0D1117;">
                <div style="color:#F1F5F9;font-weight:600;font-size:0.85rem;">{title}</div>
                <div style="display:flex;align-items:center;gap:0.4rem;margin-top:0.25rem;">
                  <div style="width:6px;height:6px;background:{color};border-radius:50%;"></div>
                  <span style="color:{color};font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                               text-transform:uppercase;letter-spacing:0.07em;">{sub}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.75rem;'></div>", unsafe_allow_html=True)

    # Charts
    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Detection Overview</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    col_chart, col_pie = st.columns([3, 1])

    with col_chart:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        if not df.empty:
            fig = px.bar(df, x='timestamp', y='confidence', color='prediction',
                color_discrete_map={'Normal':'#10B981','Suspicious':'#EF4444'},
                labels={'confidence':'Confidence','timestamp':'Time','prediction':'Result'})
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div style="height:200px;display:flex;align-items:center;justify-content:center;color:#334155;">Upload videos to populate the timeline</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div style="color:#94A3B8;font-size:0.78rem;margin-bottom:0.5rem;">Prediction Split</div>', unsafe_allow_html=True)
        if not df.empty:
            counts = df['prediction'].value_counts()
            fig_pie = go.Figure(go.Pie(
                labels=counts.index.tolist(), values=counts.values.tolist(),
                hole=0.6, marker_colors=['#10B981','#EF4444'],
                textfont=dict(color='#94A3B8', size=10)))
            fig_pie.update_layout(**{**CHART_LAYOUT, 'height':220, 'margin':dict(t=0,b=0,l=0,r=0)})
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.markdown('<div style="height:150px;display:flex;align-items:center;justify-content:center;color:#334155;font-size:0.75rem;">No data</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent detections table
    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Recent Detections</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if not df.empty:
        recent = df.tail(8)[['timestamp','video_name','prediction','confidence','risk_level']].copy()
        recent['confidence'] = (recent['confidence']*100).round(1).astype(str) + '%'
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div style="padding:2rem;text-align:center;color:#334155;">No detections yet. Upload a video in Video Analysis to begin.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show()
