import streamlit as st
import pandas as pd
from utils.helpers import load_detection_history

def show():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🗃</div>
        <div>
            <h1>Detection History</h1>
            <p class="subtitle">All recorded inference events</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = load_detection_history()

    if df.empty:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:3rem;">
            <div style="font-size:2rem;margin-bottom:0.75rem;opacity:0.3;">🗃</div>
            <div style="color:#334155;font-family:'IBM Plex Mono',monospace;font-size:0.75rem;
                        text-transform:uppercase;letter-spacing:0.08em;">No Records</div>
            <div style="color:#1E3A5F;font-size:0.85rem;margin-top:0.5rem;">
                Detection history will appear here after video analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search by video name", placeholder="filename.mp4")
    with col2:
        pred_filter = st.multiselect("Prediction", options=df['prediction'].unique())
    with col3:
        risk_filter = st.multiselect("Risk Level", options=df['risk_level'].unique())

    if search:
        df = df[df['video_name'].str.contains(search, case=False)]
    if pred_filter:
        df = df[df['prediction'].isin(pred_filter)]
    if risk_filter:
        df = df[df['risk_level'].isin(risk_filter)]

    st.markdown(f"""
    <div style="color:#475569;font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.75rem;">
        {len(df)} records
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "confidence": st.column_config.ProgressColumn(
                "Confidence", format="%.0f%%", min_value=0, max_value=1
            ),
            "prediction": st.column_config.TextColumn("Prediction"),
        }
    )

    st.markdown("""
    <div class="section-divider">
        <span class="section-divider-label">Export</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, _ = st.columns([1, 1, 2])
    with col_a:
        st.download_button("Download CSV", df.to_csv(index=False), "detection_history.csv", "text/csv")

if __name__ == "__main__":
    show()
