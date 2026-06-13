import streamlit as st
import pandas as pd
from utils.helpers import load_detection_history
from utils.report_generator import generate_pdf_report
import os
from datetime import datetime

REPORT_IMG = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&q=80"

def show():
    st.markdown(f"""
    <div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:2rem;height:160px;">
      <img src="{REPORT_IMG}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.28);">
      <div style="position:absolute;inset:0;padding:1.5rem 2rem;display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;text-transform:uppercase;
                    letter-spacing:0.14em;color:#0891B2;margin-bottom:0.3rem;">Security Intelligence</div>
        <div style="font-size:1.55rem;font-weight:700;color:#FFFFFF;">Reports Center</div>
        <div style="color:#94A3B8;font-size:0.8rem;margin-top:0.25rem;">
          Generate professional PDF security reports from all detection data.
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    df = load_detection_history()

    if df.empty:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:3rem;">
          <div style="color:#334155;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                      text-transform:uppercase;letter-spacing:0.08em;">No data available</div>
          <div style="color:#1E3A5F;font-size:0.85rem;margin-top:0.5rem;">
            Process videos to generate report data.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    total         = len(df)
    suspicious    = len(df[df['prediction']=='Suspicious'])
    normal        = total - suspicious
    avg_conf      = df['confidence'].mean()*100
    risk_dist     = df['risk_level'].value_counts().to_dict()
    security_score= max(0, 100-(suspicious/max(total,1))*50)

    stats = {
        "total": total, "suspicious": suspicious, "normal": normal,
        "avg_confidence": avg_conf, "security_score": security_score, "risk_dist": risk_dist,
    }

    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Report Summary</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(5)
    kpis = [
        ("Total Events",    total,                  "#0891B2"),
        ("Suspicious",      suspicious,             "#EF4444"),
        ("Normal",          normal,                 "#10B981"),
        ("Avg Confidence",  f"{avg_conf:.1f}%",    "#0891B2"),
        ("Security Score",  f"{security_score:.0f}/100","#6366F1"),
    ]
    for col, (label, val, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div style="background:#0D1117;border:1px solid #1E2D3D;border-radius:8px;
                        padding:1rem;border-top:2px solid {color};text-align:center;">
              <div style="font-size:1.45rem;font-weight:700;color:#F1F5F9;">{val}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;text-transform:uppercase;
                          letter-spacing:0.08em;color:#475569;margin-top:0.3rem;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # What the report contains
    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Report Contents</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    items = [
        (col1, "Executive Summary", "Overall threat rate, confidence averages, and composite security index."),
        (col2, "Risk Distribution", "Colour-coded breakdown of High, Medium, and Low risk detections."),
        (col3, "Detection Log",     "Full table of up to 20 recent events with timestamp, prediction, and confidence."),
    ]
    items2 = [
        (col1, "Model Details",      "CNN-BiLSTM architecture, backbone, training parameters, and performance metrics."),
        (col2, "Recommendations",    "Actionable security recommendations based on detected threat patterns."),
        (col3, "Last Analysis",      "Detailed breakdown of the most recent video inference result."),
    ]
    for col, title, desc in items:
        with col:
            st.markdown(f"""
            <div class="panel" style="margin-bottom:0.75rem;">
              <div style="color:#0891B2;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                          text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem;">{title}</div>
              <div style="color:#94A3B8;font-size:0.8rem;line-height:1.55;">{desc}</div>
            </div>""", unsafe_allow_html=True)
    for col, title, desc in items2:
        with col:
            st.markdown(f"""
            <div class="panel">
              <div style="color:#0891B2;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                          text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem;">{title}</div>
              <div style="color:#94A3B8;font-size:0.8rem;line-height:1.55;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    col_gen, col_csv = st.columns([1, 1])
    with col_gen:
        if st.button("Generate PDF Security Report", type="primary", use_container_width=True):
            with st.spinner("Building report..."):
                try:
                    os.makedirs("reports", exist_ok=True)
                    filename = f"reports/sentinel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    last = st.session_state.get("last_analysis")
                    generate_pdf_report(df, stats, filename, last_analysis=last)
                    with open(filename,"rb") as f:
                        st.download_button(
                            "Download PDF",
                            f,
                            file_name=os.path.basename(filename),
                            mime="application/pdf",
                            type="secondary"
                        )
                    st.success("Report generated successfully.")
                except Exception as e:
                    st.error(f"Report generation failed: {e}")
    with col_csv:
        st.download_button(
            "Export Detection Log (CSV)",
            df.to_csv(index=False),
            "sentinel_detections.csv",
            "text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    show()
