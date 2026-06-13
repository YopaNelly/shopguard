import streamlit as st
import graphviz

def show():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🏗</div>
        <div>
            <h1>System Architecture</h1>
            <p class="subtitle">End-to-end AI surveillance pipeline</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture diagram
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="margin-bottom:1rem;">Pipeline Diagram</div>', unsafe_allow_html=True)

    dot = graphviz.Digraph(graph_attr={'bgcolor': 'transparent', 'rankdir': 'LR'})
    dot.attr('node', shape='box', style='filled,rounded', fontname='IBM Plex Mono',
             fontsize='11', fontcolor='#E2E8F0', color='#1E2D3D', fillcolor='#0D1117',
             margin='0.2,0.1')
    dot.attr('edge', color='#334155', arrowsize='0.7')

    nodes = [
        ('A', 'Video Upload'),
        ('B', 'Frame Extraction'),
        ('C', 'Resize + Normalize'),
        ('D', 'MobileNetV2\n(Spatial Features)'),
        ('E', 'LSTM(128)\n(Temporal Modeling)'),
        ('F', 'Dense + Sigmoid'),
        ('G', 'Alert Engine'),
        ('H', 'Dashboard'),
    ]
    for nid, label in nodes:
        dot.node(nid, label)
    dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH'])
    st.graphviz_chart(dot)
    st.markdown("</div>", unsafe_allow_html=True)

    # Components
    st.markdown("""
    <div class="section-divider">
        <span class="section-divider-label">Component Overview</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="panel">
            <div class="panel-header"><span class="panel-title">Data Ingestion</span></div>
            <table class="info-table">
                <tr><td>Interface</td><td>Streamlit file uploader</td></tr>
                <tr><td>Formats</td><td>MP4, AVI, MOV, MKV</td></tr>
                <tr><td>Frame Sampling</td><td>Stride-based extraction</td></tr>
                <tr><td>Preprocessing</td><td>Resize 128×128, normalize</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <div class="panel-header"><span class="panel-title">AI Processing</span></div>
            <table class="info-table">
                <tr><td>CNN</td><td>MobileNetV2 (ImageNet)</td></tr>
                <tr><td>RNN</td><td>LSTM · 128 units</td></tr>
                <tr><td>Output</td><td>Sigmoid probability</td></tr>
                <tr><td>Framework</td><td>TensorFlow / Keras</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="panel">
            <div class="panel-header"><span class="panel-title">Output Services</span></div>
            <table class="info-table">
                <tr><td>Alerts</td><td>In-app, risk-classified</td></tr>
                <tr><td>Storage</td><td>CSV detection history</td></tr>
                <tr><td>Reports</td><td>PDF + CSV export</td></tr>
                <tr><td>Deployment</td><td>Local · Google Colab</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
