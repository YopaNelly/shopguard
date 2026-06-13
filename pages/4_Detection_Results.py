import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

THREAT_IMG  = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&q=80"
NORMAL_IMG  = "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&q=80"
SCAN_IMG    = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80"

def show():
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon" style="background:linear-gradient(135deg,#6366F1,#4F46E5);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      </div>
      <div><h1>Detection Results</h1><p class="subtitle">Most recent CNN-BiLSTM inference output</p></div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.get('last_analysis'):
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;border:1px solid #1E2D3D;">
          <img src="{SCAN_IMG}" style="width:100%;height:200px;object-fit:cover;filter:brightness(0.3);">
          <div style="padding:2.5rem;text-align:center;background:#0D1117;">
            <div style="color:#334155;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                        text-transform:uppercase;letter-spacing:0.08em;">No analysis available</div>
            <div style="color:#1E3A5F;font-size:0.85rem;margin-top:0.5rem;">
              Go to Video Analysis and upload footage to run inference.
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        return

    res      = st.session_state.last_analysis
    is_susp  = res['prediction'] == "Suspicious"
    prob     = res['avg_prob']
    conf     = res['confidence']
    v_color  = "#EF4444" if is_susp else "#10B981"
    v_bg     = "rgba(239,68,68,0.07)" if is_susp else "rgba(16,185,129,0.07)"
    v_border = "rgba(239,68,68,0.22)" if is_susp else "rgba(16,185,129,0.22)"
    v_text   = "THREAT DETECTED" if is_susp else "NO THREAT DETECTED"
    hero_img = THREAT_IMG if is_susp else NORMAL_IMG
    ts       = datetime.fromtimestamp(res['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

    # Hero image
    st.markdown(f"""
    <div style="position:relative;border-radius:10px;overflow:hidden;margin-bottom:1.5rem;height:160px;
                border:1px solid {v_border};">
      <img src="{hero_img}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.32);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;padding:0 2rem;">
        <div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;text-transform:uppercase;
                      letter-spacing:0.14em;color:{v_color};margin-bottom:0.3rem;">{v_text}</div>
          <div style="font-size:1.65rem;font-weight:700;color:#FFFFFF;">{res['prediction']} Activity</div>
          <div style="color:#94A3B8;font-size:0.82rem;margin-top:0.25rem;">{ts}</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        bar_col_prob = "#EF4444" if prob>=0.7 else ("#F59E0B" if prob>=0.4 else "#10B981")
        st.markdown(f"""
        <div style="border:1px solid {v_border};background:{v_bg};border-radius:10px;padding:1.5rem;">
          <table class="info-table">
            <tr><td>Video File</td><td>{res['video_name']}</td></tr>
            <tr><td>Timestamp</td><td>{ts}</td></tr>
            <tr><td>Anomaly Probability</td><td><strong style="color:{v_color};">{prob*100:.1f}%</strong></td></tr>
            <tr><td>Model Confidence</td><td>{conf*100:.1f}%</td></tr>
            <tr><td>Risk Level</td><td><strong style="color:{v_color};">{res['risk']}</strong></td></tr>
            <tr><td>Processing Time</td><td>{res['processing_time']:.2f} s</td></tr>
            <tr><td>Decision Threshold</td><td>0.50</td></tr>
            <tr><td>Model</td><td>CNN-BiLSTM (MobileNetV2)</td></tr>
          </table>
          <div style="margin-top:1.25rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#94A3B8;margin-bottom:0.3rem;">
              <span>Anomaly Probability</span>
              <span style="color:{bar_col_prob};font-weight:700;">{prob*100:.1f}%</span>
            </div>
            <div style="background:#1A2535;border-radius:4px;height:8px;overflow:hidden;">
              <div style="height:100%;width:{prob*100:.1f}%;background:{bar_col_prob};border-radius:4px;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#94A3B8;
                        margin:0.75rem 0 0.3rem;">
              <span>Model Confidence</span>
              <span style="color:#0891B2;font-weight:700;">{conf*100:.1f}%</span>
            </div>
            <div style="background:#1A2535;border-radius:4px;height:8px;overflow:hidden;">
              <div style="height:100%;width:{conf*100:.1f}%;background:#0891B2;border-radius:4px;"></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    with col_right:
        gauge_color = "#EF4444" if is_susp else "#10B981"
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob*100,
            number={'suffix':'%','font':{'color':'#F1F5F9','size':28}},
            domain={'x':[0,1],'y':[0,1]},
            gauge={
                'axis':{'range':[0,100],'tickcolor':'#334155','tickfont':{'color':'#475569','size':10}},
                'bar':{'color':gauge_color,'thickness':0.25},
                'bgcolor':'#1A2535','borderwidth':0,
                'steps':[
                    {'range':[0,40],'color':'#0A2818'},
                    {'range':[40,65],'color':'#1A1A0A'},
                    {'range':[65,100],'color':'#1A0808'},
                ],
                'threshold':{'line':{'color':'#F59E0B','width':2},'thickness':0.75,'value':50}
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',height=250,
                          margin=dict(t=20,b=0,l=20,r=20),font_color='#94A3B8')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div style="padding:1rem;background:{v_bg};border:1px solid {v_border};border-radius:8px;margin-top:0.5rem;">
          <div style="color:{v_color};font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                      text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">Model Interpretation</div>
          <div style="color:#94A3B8;font-size:0.8rem;line-height:1.6;">
            {"The CNN-BiLSTM model identified anomalous spatial and temporal patterns consistent with shoplifting behaviour in the UCF-Crime training distribution. MobileNetV2 extracted frame-level features; the BiLSTM captured forward and backward temporal dynamics across 32 frames."
             if is_susp else
             "Spatial features from MobileNetV2 and temporal patterns from the BiLSTM layer are consistent with normal retail activity. The output probability is below the 0.50 decision threshold."}
          </div>
        </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
