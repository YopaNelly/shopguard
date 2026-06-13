import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import load_detection_history

def show():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📈</div>
        <div>
            <h1>Analytics Center</h1>
            <p class="subtitle">Detection history · Trends · Distributions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = load_detection_history()

    if df.empty:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:3rem;">
            <div style="font-size:2rem;margin-bottom:0.75rem;opacity:0.3;">📊</div>
            <div style="color:#334155;font-family:'IBM Plex Mono',monospace;font-size:0.75rem;
                        text-transform:uppercase;letter-spacing:0.08em;">No Data Available</div>
            <div style="color:#1E3A5F;font-size:0.85rem;margin-top:0.5rem;">
                Process videos in the Video Analysis page to populate analytics.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        prediction_filter = st.selectbox("Prediction Filter", ["All", "Suspicious", "Normal"])
    with col2:
        risk_filter = st.selectbox("Risk Filter", ["All", "Low", "Medium", "High"])

    filtered = df.copy()
    if prediction_filter != "All":
        filtered = filtered[filtered['prediction'] == prediction_filter]
    if risk_filter != "All":
        filtered = filtered[filtered['risk_level'] == risk_filter]

    # KPIs
    suspicious_count = len(filtered[filtered['prediction'] == 'Suspicious'])
    total = max(len(filtered), 1)
    susp_pct = suspicious_count / total * 100
    avg_conf = filtered['confidence'].mean() * 100 if len(filtered) > 0 else 0

    kpi_cols = st.columns(3)
    kpi_data = [
        ("Total Detections", len(filtered), "Filtered records", "info"),
        ("Suspicious Rate", f"{susp_pct:.1f}%", f"{suspicious_count} events flagged", "alert"),
        ("Avg Confidence", f"{avg_conf:.1f}%", "CNN-LSTM output", "success"),
    ]
    for col, (label, val, delta, kind) in zip(kpi_cols, kpi_data):
        with col:
            st.markdown(f"""
            <div class="kpi-card {kind}">
                <div class="label">{label}</div>
                <div class="value">{val}</div>
                <div class="delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

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

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title" style="margin-bottom:0.75rem;">Prediction Split</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=filtered['prediction'].value_counts().index.tolist(),
            values=filtered['prediction'].value_counts().values.tolist(),
            hole=0.55,
            marker_colors=['#10B981', '#EF4444'],
            textfont=dict(color='#94A3B8', size=11),
        ))
        fig_pie.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title" style="margin-bottom:0.75rem;">Confidence Distribution</div>', unsafe_allow_html=True)
        fig_hist = go.Figure(go.Histogram(
            x=filtered['confidence'] * 100,
            nbinsx=20,
            marker_color='#0EA5E9',
            opacity=0.8,
        ))
        fig_hist.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Timeline
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="margin-bottom:0.75rem;">Detection Frequency</div>', unsafe_allow_html=True)
    filtered['date'] = pd.to_datetime(filtered['timestamp']).dt.date
    daily = filtered.groupby(['date', 'prediction']).size().reset_index(name='count')
    fig_line = px.line(
        daily, x='date', y='count', color='prediction', markers=True,
        color_discrete_map={'Normal': '#10B981', 'Suspicious': '#EF4444'},
    )
    fig_line.update_layout(**{**CHART_LAYOUT, 'height': 220})
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Export
    st.markdown("""
    <div class="section-divider">
        <span class="section-divider-label">Export</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)
    st.download_button(
        "Download Filtered Data (CSV)",
        filtered.to_csv(index=False),
        "sentinel_analytics_export.csv",
        "text/csv"
    )

if __name__ == "__main__":
    show()
