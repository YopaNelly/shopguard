import streamlit as st

NHPI_IMG   = "https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80"
RETAIL_IMG = "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&q=80"
AI_IMG     = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80"

def show():
    # Hero
    st.markdown(f"""
    <div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:2rem;height:200px;">
      <img src="{NHPI_IMG}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.28);">
      <div style="position:absolute;inset:0;padding:1.75rem 2.5rem;display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;text-transform:uppercase;
                    letter-spacing:0.14em;color:#0891B2;margin-bottom:0.35rem;">Final Year Engineering Project - 2025/2026</div>
        <div style="font-size:1.65rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.02em;">About This Project</div>
        <div style="color:#94A3B8;font-size:0.82rem;margin-top:0.35rem;">
          ShopGuard AI - Intelligent Video Surveillance for Cameroonian Supermarkets
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        <div class="panel">
          <div class="panel-header"><span class="panel-title">Project Details</span></div>
          <table class="info-table">
            <tr><td>Full Title</td><td>Intelligent Video Surveillance System for Detecting Shoplifting in Supermarkets</td></tr>
            <tr><td>Student</td><td>Tatchou Yopa Gertrude Nelly</td></tr>
            <tr><td>Registration</td><td>UBa22E0314</td></tr>
            <tr><td>Department</td><td>Computer Engineering</td></tr>
            <tr><td>Institution</td><td>National Higher Polytechnic Institute, University of Bamenda</td></tr>
            <tr><td>Supervisor</td><td>Engr. Ayeah Milton</td></tr>
            <tr><td>Methodology</td><td>Spiral Model (4 Cycles)</td></tr>
            <tr><td>Dataset</td><td>UCF-Crime (79 videos: 50 normal, 29 shoplifting)</td></tr>
            <tr><td>Model Recall</td><td>83.33% on shoplifting class</td></tr>
            <tr><td>Year</td><td>2025/2026</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div style="border-radius:8px;overflow:hidden;margin-bottom:1rem;height:180px;border:1px solid #1E2D3D;">
          <img src="{RETAIL_IMG}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45);">
        </div>
        <div class="panel">
          <div style="color:#0891B2;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                      text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Target Social Impact</div>
          <div style="color:#94A3B8;font-size:0.82rem;line-height:1.65;">
            Cameroonian supermarkets lose an estimated
            <strong style="color:#F1F5F9;">2 billion FCFA</strong> annually to retail theft.
            ShopGuard AI provides an affordable, locally adapted AI surveillance layer
            that reduces manual monitoring workload and enables faster security response.
          </div>
          <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid #1A2535;">
            <div style="color:#10B981;font-size:1.35rem;font-weight:700;">65% theft reduction</div>
            <div style="color:#475569;font-size:0.78rem;">target across participating retail environments</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Abstract</span>
      <div class="section-divider-line"></div>
    </div>
    <div class="panel">
      <div style="color:#94A3B8;font-size:0.88rem;line-height:1.75;">
        This project develops a CNN-BiLSTM model to automatically detect suspicious behaviours -
        including loitering, item concealment, and abnormal movement patterns - from CCTV surveillance footage.
        The system is specifically tailored for Cameroonian retail environments, addressing local infrastructure
        constraints through a lightweight MobileNetV2 backbone paired with Bidirectional LSTM temporal modelling.
        Trained under a Spiral Model methodology across four iterative cycles, the platform delivers a complete,
        deployable AI security tool accessible to African retailers without enterprise-grade GPU infrastructure.
        The model achieves 83.33% recall on the shoplifting class across a 79-video UCF-Crime subset,
        demonstrating strong performance under significant data constraints.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-divider">
      <span class="section-divider-label">Technical Contributions</span>
      <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)

    items = [
        ("CNN-BiLSTM Architecture",  "MobileNetV2 spatial feature extractor combined with Bidirectional LSTM for temporal sequence modelling across 32-frame video clips."),
        ("Focal Loss Training",       "Focal Loss (gamma=2.0, alpha=0.25) addresses class imbalance and focuses model training on hard, ambiguous examples."),
        ("Sequence-Consistent Augmentation", "Identical spatial transforms applied to all 32 frames in a clip, preserving temporal coherence during data augmentation."),
        ("No-GPU Deployment",         "Streamlit platform runs on standard laptop hardware with no dedicated GPU, making it accessible to Cameroonian retailers."),
        ("Automated Email Alerts",    "Gmail SMTP integration sends instant HTML threat alerts with attached PDF reports when suspicious activity is detected."),
        ("PDF Security Reports",      "Professionally formatted multi-page PDF reports with KPI cards, risk charts, detection logs, and actionable recommendations."),
    ]
    col1, col2 = st.columns(2)
    for i, (title, desc) in enumerate(items):
        with (col1 if i%2==0 else col2):
            st.markdown(f"""
            <div class="panel" style="margin-bottom:0.75rem;">
              <div style="color:#0891B2;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                          text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem;">{title}</div>
              <div style="color:#94A3B8;font-size:0.8rem;line-height:1.55;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:1.5rem;padding:1rem;
                color:#1E3A5F;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                text-transform:uppercase;letter-spacing:0.1em;">
      ShopGuard AI - National Higher Polytechnic Institute, University of Bamenda - 2025/2026
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    show()
