"""
Video Analysis page - ShopGuard AI.
Uploads a CCTV video, runs CNN-BiLSTM inference, displays:
  - Video metadata
  - Resized preview frames (8 thumbnails visible on screen)
  - Probability bars and result verdict
  - PDF report download
  - Email alert (if credentials configured)
"""
import streamlit as st
import tempfile
import os
import time
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

from utils.helpers        import save_detection, get_risk_level, load_detection_history
from utils.model_loader   import load_surveillance_model, predict_single
from utils.video_processor import (
    process_video_for_inference,
    extract_preview_frames,
    get_video_metadata,
)
from utils.report_generator import generate_pdf_report
from utils.email_alerts     import send_alert_email, RECIPIENT_EMAIL


# ── Unsplash images ───────────────────────────────────────────────────────────
HEADER_IMG  = "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=1200&q=80"
CCTV_IMG    = "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=600&q=80"
STORE_IMG   = "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=600&q=80"
AI_IMG      = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80"
ALERT_IMG   = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&q=80"
RETAIL_IMG  = "https://images.unsplash.com/photo-1534723452862-4c874986d5d8?w=600&q=80"
CLEAR_IMG   = "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400&q=80"


def _divider(label):
    st.markdown(f"""
    <div class="section-divider">
        <span class="section-divider-label">{label}</span>
        <div class="section-divider-line"></div>
    </div>""", unsafe_allow_html=True)


def _info_panel(rows):
    cells = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)
    return f'<div class="panel"><table class="info-table">{cells}</table></div>'


def show():
    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="position:relative;border-radius:12px;overflow:hidden;
                margin-bottom:2rem;height:220px;">
      <img src="{HEADER_IMG}"
           style="width:100%;height:100%;object-fit:cover;filter:brightness(0.32);">
      <div style="position:absolute;inset:0;padding:2rem 2.5rem;
                  display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                    text-transform:uppercase;letter-spacing:0.14em;
                    color:#0891B2;margin-bottom:0.4rem;">CNN-BiLSTM Inference Engine</div>
        <div style="font-size:1.75rem;font-weight:700;color:#FFFFFF;
                    letter-spacing:-0.02em;line-height:1.1;">Video Analysis</div>
        <div style="color:#94A3B8;font-size:0.85rem;margin-top:0.4rem;">
          Upload CCTV footage and receive an instant AI threat assessment
          with automated email alert and PDF report.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────────
    _divider("How It Works")
    steps = [
        (CCTV_IMG,  "01", "Upload Footage",     "MP4, AVI, MOV or MKV from any CCTV source."),
        (STORE_IMG, "02", "Frame Extraction",   "32 frames uniformly sampled and resized to 64x64 for the model."),
        (AI_IMG,    "03", "CNN-BiLSTM Analysis","MobileNetV2 backbone feeds into Bidirectional LSTM."),
        (ALERT_IMG, "04", "Alert and Report",   "Instant email to security team plus downloadable PDF."),
    ]
    for col, (img, num, title, desc) in zip(st.columns(4), steps):
        with col:
            st.markdown(f"""
            <div style="border-radius:8px;overflow:hidden;border:1px solid #1E2D3D;">
              <img src="{img}"
                   style="width:100%;height:110px;object-fit:cover;filter:brightness(0.45);">
              <div style="padding:0.85rem 1rem;background:#0D1117;">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                            color:#0891B2;text-transform:uppercase;
                            letter-spacing:0.1em;margin-bottom:0.25rem;">{num}</div>
                <div style="color:#F1F5F9;font-weight:600;font-size:0.85rem;
                            margin-bottom:0.3rem;">{title}</div>
                <div style="color:#64748B;font-size:0.78rem;line-height:1.5;">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

    # ── Model status ──────────────────────────────────────────────────────────
    model = load_surveillance_model()
    is_demo = not hasattr(model, "input_shape") or "Demo" in type(model).__name__

    if not is_demo:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.65rem;padding:0.65rem 1.1rem;
                    background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.22);
                    border-radius:6px;margin-bottom:1.25rem;">
          <div style="width:8px;height:8px;background:#10B981;border-radius:50%;flex-shrink:0;
                      box-shadow:0 0 6px rgba(16,185,129,0.6);"></div>
          <span style="color:#10B981;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                       text-transform:uppercase;letter-spacing:0.07em;">
            CNN-BiLSTM Model Loaded and Ready for Inference
          </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.65rem;padding:0.65rem 1.1rem;
                    background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.22);
                    border-radius:6px;margin-bottom:1.25rem;">
          <div style="width:8px;height:8px;background:#F59E0B;border-radius:50%;flex-shrink:0;"></div>
          <span style="color:#F59E0B;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                       text-transform:uppercase;letter-spacing:0.07em;">
            Demo Mode - place model at /home/ngadou/Documents/best_cnn_bilstm_v2 and restart
          </span>
        </div>""", unsafe_allow_html=True)

    # ── Email config ──────────────────────────────────────────────────────────
    _divider("Email Alert Configuration")
    st.markdown(f"""
    <div class="panel" style="margin-bottom:1rem;">
      <div style="color:#94A3B8;font-size:0.82rem;line-height:1.65;">
        Alerts are automatically sent to
        <strong style="color:#0891B2;">{RECIPIENT_EMAIL}</strong>
        when a suspicious event is detected.
        Provide your Gmail address and a Gmail App Password below.
        Credentials are stored only in session memory and never saved to disk.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_mail, col_pass = st.columns(2)
    with col_mail:
        sender_email = st.text_input(
            "Your Gmail address (sender)",
            value=st.session_state.get("sender_email", ""),
            placeholder="yourname@gmail.com",
            key="sender_email_input",
        )
    with col_pass:
        sender_password = st.text_input(
            "Gmail App Password (16 characters)",
            value=st.session_state.get("sender_password", ""),
            type="password",
            placeholder="xxxx xxxx xxxx xxxx",
            key="sender_pass_input",
            help="Go to myaccount.google.com > Security > App Passwords.",
        )

    if sender_email:
        st.session_state["sender_email"] = sender_email
    if sender_password:
        st.session_state["sender_password"] = sender_password

    # ── Upload ────────────────────────────────────────────────────────────────
    _divider("Upload CCTV Footage")
    col_upload, col_img = st.columns([3, 2])
    with col_img:
        st.markdown(f"""
        <div style="border-radius:8px;overflow:hidden;height:180px;border:1px solid #1E2D3D;">
          <img src="{RETAIL_IMG}"
               style="width:100%;height:100%;object-fit:cover;filter:brightness(0.5);">
        </div>""", unsafe_allow_html=True)
    with col_upload:
        uploaded_file = st.file_uploader(
            "Drop CCTV footage here",
            type=["mp4", "avi", "mov", "mkv"],
            help="Supported: MP4, AVI, MOV, MKV. Minimum 32 frames required.",
        )

    if not uploaded_file:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:2rem;margin-top:1rem;
                                   border:1px dashed #1E2D3D;">
          <div style="color:#334155;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;
                      text-transform:uppercase;letter-spacing:0.08em;">No footage uploaded yet</div>
          <div style="color:#1E3A5F;font-size:0.82rem;margin-top:0.4rem;">
            Use the uploader above to begin.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    # Write to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.flush()
    video_path = tfile.name

    # ── Metadata ──────────────────────────────────────────────────────────────
    meta = get_video_metadata(video_path)
    fps         = meta.get("fps", 0)
    frame_count = meta.get("frame_count", 0)
    duration    = meta.get("duration", 0)
    width       = meta.get("width", 0)
    height_px   = meta.get("height", 0)

    _divider("Footage Preview and Frame Samples")
    col_vid, col_meta = st.columns([2, 1])

    with col_vid:
        st.video(video_path)

    with col_meta:
        st.markdown(_info_panel([
            ("Filename",   uploaded_file.name[:28]),
            ("Duration",   f"{duration:.2f} s"),
            ("Frame Rate", f"{fps:.1f} fps"),
            ("Resolution", f"{width} x {height_px}"),
            ("Frames",     f"{frame_count:,}"),
            ("File Size",  f"{uploaded_file.size / 1e6:.2f} MB"),
        ]), unsafe_allow_html=True)

        if frame_count < 32:
            st.warning("Video has fewer than 32 frames. Inference may be unreliable.")

    # ── Frame preview grid ────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:1.25rem;margin-bottom:0.5rem;">
      <div style="color:#475569;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                  text-transform:uppercase;letter-spacing:0.1em;">
        Sampled Frames Preview (resized for display)
      </div>
    </div>""", unsafe_allow_html=True)

    preview_frames, prev_err = extract_preview_frames(video_path, num_frames=8, display_size=160)
    if preview_frames and not prev_err:
        cols = st.columns(len(preview_frames))
        for col, (i, frame) in zip(cols, enumerate(preview_frames)):
            with col:
                pil_img = Image.fromarray(frame)
                st.image(
                    pil_img,
                    caption=f"Frame {i+1}",
                    use_container_width=True,
                )
    elif prev_err:
        st.caption(f"Preview unavailable: {prev_err}")

    # ── Run analysis ──────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("Run AI Analysis", type="primary", use_container_width=True)

    if not run:
        try:
            os.unlink(video_path)
        except Exception:
            pass
        return

    # ── Inference ─────────────────────────────────────────────────────────────
    with st.spinner("Running CNN-BiLSTM inference on 32-frame sequence..."):
        try:
            t0 = time.time()
            batch_tensor, err = process_video_for_inference(video_path)
            if err:
                st.error(f"Video processing error: {err}")
                return

            probability     = predict_single(model, batch_tensor)
            prediction      = "Suspicious" if probability >= 0.5 else "Normal"
            confidence      = max(probability, 1.0 - probability)
            risk            = get_risk_level(probability)
            processing_time = time.time() - t0

        except Exception as exc:
            st.error(f"Inference failed: {exc}")
            return

    save_detection(
        uploaded_file.name, prediction, confidence,
        risk, processing_time, probability,
    )

    analysis = {
        "video_name":      uploaded_file.name,
        "prediction":      prediction,
        "confidence":      confidence,
        "risk":            risk,
        "avg_prob":        probability,
        "timestamp":       time.time(),
        "processing_time": processing_time,
    }
    st.session_state["last_analysis"] = analysis

    # ── Result display ────────────────────────────────────────────────────────
    _divider("Analysis Result")
    is_susp     = prediction == "Suspicious"
    v_col       = "#EF4444" if is_susp else "#10B981"
    v_bg        = "rgba(239,68,68,0.07)"  if is_susp else "rgba(16,185,129,0.07)"
    v_bdr       = "rgba(239,68,68,0.22)"  if is_susp else "rgba(16,185,129,0.22)"
    v_icon      = ALERT_IMG if is_susp else CLEAR_IMG
    v_text      = "THREAT DETECTED" if is_susp else "NO THREAT DETECTED"
    ts_str      = datetime.fromtimestamp(analysis["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    interp_text = (
        "The CNN-BiLSTM model detected anomalous spatial and temporal patterns "
        "consistent with shoplifting behaviour."
        if is_susp else
        "Spatial features from MobileNetV2 and temporal patterns from the BiLSTM "
        "are consistent with normal retail activity (probability below 0.50 threshold)."
    )

    col_r1, col_r2 = st.columns([3, 2])

    with col_r1:
        st.markdown(f"""
        <div style="border:1px solid {v_bdr};background:{v_bg};border-radius:10px;
                    padding:1.5rem;margin-bottom:1rem;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                      text-transform:uppercase;letter-spacing:0.12em;
                      color:{v_col};margin-bottom:0.35rem;">{v_text}</div>
          <div style="font-size:1.5rem;font-weight:700;color:#F1F5F9;
                      margin-bottom:1rem;">{prediction} Activity</div>
          <table class="info-table">
            <tr><td>Video</td><td>{uploaded_file.name}</td></tr>
            <tr><td>Timestamp</td><td>{ts_str}</td></tr>
            <tr><td>Anomaly Probability</td>
                <td><strong style="color:{v_col};">{probability*100:.1f}%</strong></td></tr>
            <tr><td>Model Confidence</td><td>{confidence*100:.1f}%</td></tr>
            <tr><td>Risk Level</td>
                <td><strong style="color:{v_col};">{risk}</strong></td></tr>
            <tr><td>Processing Time</td><td>{processing_time:.2f} s</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        bar_col = (
            "#EF4444" if probability >= 0.7
            else "#F59E0B" if probability >= 0.4
            else "#10B981"
        )
        st.markdown(f"""
        <div style="margin-top:0.5rem;">
          <div style="display:flex;justify-content:space-between;font-size:0.78rem;
                      color:#94A3B8;margin-bottom:0.3rem;">
            <span>Anomaly Probability</span>
            <span style="color:{bar_col};font-weight:700;">{probability*100:.1f}%</span>
          </div>
          <div style="background:#1A2535;border-radius:4px;height:8px;overflow:hidden;">
            <div style="height:100%;width:{probability*100:.1f}%;background:{bar_col};
                        border-radius:4px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:0.78rem;
                      color:#94A3B8;margin:0.75rem 0 0.3rem;">
            <span>Model Confidence</span>
            <span style="color:#0891B2;font-weight:700;">{confidence*100:.1f}%</span>
          </div>
          <div style="background:#1A2535;border-radius:4px;height:8px;overflow:hidden;">
            <div style="height:100%;width:{confidence*100:.1f}%;
                        background:#0891B2;border-radius:4px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown(f"""
        <div style="border-radius:8px;overflow:hidden;border:1px solid {v_bdr};height:200px;">
          <img src="{v_icon}"
               style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45);">
        </div>
        <div style="margin-top:0.75rem;background:{v_bg};border:1px solid {v_bdr};
                    border-radius:6px;padding:0.9rem 1rem;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;
                      text-transform:uppercase;letter-spacing:0.1em;
                      color:{v_col};margin-bottom:0.35rem;">Model Interpretation</div>
          <div style="color:#94A3B8;font-size:0.8rem;line-height:1.6;">
            {interp_text}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── PDF + Email ───────────────────────────────────────────────────────────
    _divider("Automated Alert and Report")

    os.makedirs("reports", exist_ok=True)
    df_hist = load_detection_history()
    total_v = len(df_hist)
    susp_v  = len(df_hist[df_hist["prediction"] == "Suspicious"])
    stats   = {
        "total":           total_v,
        "suspicious":      susp_v,
        "normal":          total_v - susp_v,
        "avg_confidence":  df_hist["confidence"].mean() * 100 if total_v > 0 else 0,
        "security_score":  max(0, 100 - (susp_v / max(total_v, 1)) * 50),
        "risk_dist":       df_hist["risk_level"].value_counts().to_dict(),
    }
    tag          = "alert" if is_susp else "normal"
    pdf_filename = f"reports/sentinel_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_ok       = False

    try:
        generate_pdf_report(df_hist, stats, pdf_filename, last_analysis=analysis)
        pdf_ok = True
    except Exception as exc:
        st.warning(f"PDF generation issue: {exc}")

    if is_susp:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:0.65rem;padding:1rem 1.25rem;
                    background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2);
                    border-radius:8px;margin-bottom:1.25rem;">
          <img src="{ALERT_IMG}"
               style="width:52px;height:52px;object-fit:cover;border-radius:6px;flex-shrink:0;">
          <div>
            <div style="color:#EF4444;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;
                        text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.25rem;">
              Suspicious Activity Confirmed</div>
            <div style="color:#CBD5E1;font-size:0.82rem;line-height:1.6;">
              A PDF security report has been generated. If your email credentials are set above,
              the alert is dispatched immediately to
              <strong style="color:#0891B2;">{RECIPIENT_EMAIL}</strong>.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        s_email = st.session_state.get("sender_email", "")
        s_pass  = st.session_state.get("sender_password", "")

        col_em, col_dl = st.columns([2, 1])
        with col_em:
            if s_email and s_pass:
                with st.spinner("Sending alert email..."):
                    ok, msg = send_alert_email(
                        video_name=uploaded_file.name,
                        probability=probability,
                        confidence=confidence,
                        risk_level=risk,
                        processing_time=processing_time,
                        sender_email=s_email,
                        sender_app_password=s_pass,
                        pdf_path=pdf_filename if pdf_ok else None,
                    )
                if ok:
                    st.success(f"Alert email sent to {RECIPIENT_EMAIL}")
                else:
                    st.warning(f"Email not sent: {msg}")
            else:
                st.info(
                    "Enter Gmail credentials in the Email Alert Configuration section "
                    "above to enable automatic alerts."
                )

        with col_dl:
            if pdf_ok and os.path.exists(pdf_filename):
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        "Download PDF Report",
                        f,
                        file_name=os.path.basename(pdf_filename),
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                    )
    else:
        st.markdown("""
        <div style="padding:1rem 1.25rem;background:rgba(16,185,129,0.06);
                    border:1px solid rgba(16,185,129,0.2);border-radius:8px;margin-bottom:1rem;">
          <div style="color:#10B981;font-family:'IBM Plex Mono',monospace;font-size:0.7rem;
                      text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.25rem;">
            No threat detected - no email alert sent</div>
          <div style="color:#94A3B8;font-size:0.82rem;line-height:1.6;">
            Email alerts are only dispatched when suspicious activity is confirmed.
            You can still download the analysis report below.
          </div>
        </div>""", unsafe_allow_html=True)

        if pdf_ok and os.path.exists(pdf_filename):
            with open(pdf_filename, "rb") as f:
                st.download_button(
                    "Download Analysis Report",
                    f,
                    file_name=os.path.basename(pdf_filename),
                    mime="application/pdf",
                    type="secondary",
                )

    try:
        os.unlink(video_path)
    except Exception:
        pass


if __name__ == "__main__":
    show()
