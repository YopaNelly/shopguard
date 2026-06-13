import streamlit as st

def show():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🤖</div>
        <div>
            <h1>AI Model Information</h1>
            <p class="subtitle">CNN-LSTM · MobileNetV2 · UCF-Crime</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Architecture</span>
            </div>
            <table class="info-table">
                <tr><td>Model Type</td><td>CNN-LSTM</td></tr>
                <tr><td>CNN Backbone</td><td>MobileNetV2 (ImageNet)</td></tr>
                <tr><td>Temporal Layer</td><td>LSTM · 128 units</td></tr>
                <tr><td>Input Shape</td><td>(16, 128, 128, 3)</td></tr>
                <tr><td>Output</td><td>Sigmoid → P(Suspicious)</td></tr>
                <tr><td>Loss Function</td><td>Binary Crossentropy</td></tr>
                <tr><td>Optimizer</td><td>Adam · lr = 0.0001</td></tr>
                <tr><td>Decision Threshold</td><td>≥ 0.50 → Suspicious</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Training Configuration</span>
            </div>
            <table class="info-table">
                <tr><td>Dataset</td><td>UCF-Crime + shoplifting</td></tr>
                <tr><td>Epochs</td><td>50 (early stopping)</td></tr>
                <tr><td>Batch Size</td><td>8</td></tr>
                <tr><td>Augmentation</td><td>Flip, brightness shift</td></tr>
                <tr><td>Val Accuracy</td><td>92.3%</td></tr>
                <tr><td>Classification</td><td>Binary (Normal / Anomaly)</td></tr>
                <tr><td>Methodology</td><td>Design Science Research</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # Design rationale
    st.markdown("""
    <div class="section-divider">
        <span class="section-divider-label">Design Rationale</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="panel">
            <div class="panel-header"><span class="panel-title">Why MobileNetV2?</span></div>
            <p>MobileNetV2 provides state-of-the-art spatial feature extraction from individual frames
            while being lightweight enough for deployment on modest hardware - a critical constraint
            for Cameroonian supermarket environments. Inverted residuals and linear bottlenecks
            ensure high accuracy with minimal compute overhead.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <div class="panel-header"><span class="panel-title">Why LSTM?</span></div>
            <p>Shoplifting is inherently temporal - rapid item concealment, prolonged loitering,
            and unusual body posture sequences unfold over multiple frames. The LSTM layer learns
            these temporal dependencies across the 16-frame input window, enabling detection of
            behavioral patterns that single-frame classifiers miss.</p>
        </div>
        """, unsafe_allow_html=True)

    # Pipeline
    st.markdown("""
    <div class="section-divider">
        <span class="section-divider-label">Inference Pipeline</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.code("""
# Inference Pipeline - CNN-LSTM Shoplifting Detection
Video Input
  └─ Frame Extraction  (every N frames, stride sampling)
       └─ Resize        224×224 → 128×128
            └─ Normalize  pixel values to [0, 1]
                 └─ Sequence  16 consecutive frames → (1, 16, 128, 128, 3)
                      └─ MobileNetV2  spatial feature extraction per frame
                           └─ LSTM(128)  temporal dependency modeling
                                └─ Dense(1) + Sigmoid  → P(Suspicious)
                                     └─ Threshold @ 0.50  → {Normal, Suspicious}
    """, language="text")

    # Limitations
    st.markdown("""
    <div class="panel" style="border-color:rgba(245,158,11,0.25);">
        <div class="panel-header">
            <span class="panel-title">Known Limitations</span>
            <span class="badge badge-warning">Important</span>
        </div>
        <p>Best performance is achieved with frontal camera angles and moderate, consistent lighting.
        Occluded scenes, extreme angles, and very low-resolution footage can reduce accuracy.
        The model is trained on the UCF-Crime benchmark - domain adaptation to specific Cameroonian
        supermarket layouts is recommended for production deployment.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
