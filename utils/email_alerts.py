"""
Email alert system using Gmail SMTP (smtplib - fully free, no third-party service).
The sender account uses an App Password (not the Gmail login password).
Set these once in the sidebar Settings page or via environment variables.
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os


RECIPIENT_EMAIL = "yopatatchou@gmail.com"


def send_alert_email(
    video_name: str,
    probability: float,
    confidence: float,
    risk_level: str,
    processing_time: float,
    sender_email: str,
    sender_app_password: str,
    pdf_path: str = None,
) -> tuple[bool, str]:
    """
    Send a threat-detected alert email via Gmail SMTP.
    Returns (success: bool, message: str).
    """
    if not sender_email or not sender_app_password:
        return False, "Sender email or App Password not configured. Go to Settings page."

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = f"[SENTINEL AI] Shoplifting Alert - {risk_level} Risk Detected"

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7fa; margin: 0; padding: 0; }}
  .wrapper {{ max-width: 600px; margin: 30px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
  .header {{ background: #0D1B2A; padding: 28px 32px; }}
  .header h1 {{ color: #FFFFFF; margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }}
  .header p {{ color: #0891B2; margin: 4px 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; font-family: monospace; }}
  .alert-banner {{ background: #FEF2F2; border-left: 4px solid #EF4444; padding: 18px 32px; }}
  .alert-banner h2 {{ color: #991B1B; margin: 0 0 4px; font-size: 17px; }}
  .alert-banner p {{ color: #7F1D1D; margin: 0; font-size: 13px; }}
  .body {{ padding: 28px 32px; }}
  .kpi-row {{ display: flex; gap: 12px; margin-bottom: 24px; }}
  .kpi {{ flex: 1; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 14px 16px; text-align: center; }}
  .kpi .val {{ font-size: 22px; font-weight: 700; color: #0D1B2A; }}
  .kpi .lbl {{ font-size: 11px; color: #64748B; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.06em; }}
  .detail-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .detail-table td {{ padding: 9px 12px; border-bottom: 1px solid #F1F5F9; }}
  .detail-table td:first-child {{ color: #64748B; font-weight: 500; width: 44%; }}
  .detail-table td:last-child {{ color: #0D1B2A; font-weight: 600; }}
  .risk-high {{ color: #EF4444; }}
  .risk-medium {{ color: #F59E0B; }}
  .risk-low {{ color: #10B981; }}
  .action-box {{ background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 6px; padding: 16px 20px; margin-top: 20px; }}
  .action-box h3 {{ color: #0369A1; margin: 0 0 8px; font-size: 14px; }}
  .action-box ul {{ margin: 0; padding-left: 18px; color: #0C4A6E; font-size: 13px; line-height: 1.8; }}
  .footer {{ background: #F8FAFC; padding: 18px 32px; text-align: center; border-top: 1px solid #E2E8F0; }}
  .footer p {{ margin: 0; color: #94A3B8; font-size: 11px; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>SENTINEL AI</h1>
    <p>Shoplifting Detection Platform</p>
  </div>
  <div class="alert-banner">
    <h2>Shoplifting Threat Detected</h2>
    <p>The AI surveillance system has flagged a <strong>{risk_level} Risk</strong> event requiring immediate attention.</p>
  </div>
  <div class="body">
    <div class="kpi-row">
      <div class="kpi"><div class="val">{probability*100:.0f}%</div><div class="lbl">Threat Probability</div></div>
      <div class="kpi"><div class="val">{confidence*100:.0f}%</div><div class="lbl">Confidence</div></div>
      <div class="kpi"><div class="val class="risk-{risk_level.lower()}">{risk_level}</div><div class="lbl">Risk Level</div></div>
    </div>
    <table class="detail-table">
      <tr><td>Video File</td><td>{video_name}</td></tr>
      <tr><td>Detection Time</td><td>{timestamp}</td></tr>
      <tr><td>Anomaly Probability</td><td>{probability*100:.1f}%</td></tr>
      <tr><td>Model Confidence</td><td>{confidence*100:.1f}%</td></tr>
      <tr><td>Risk Classification</td><td><span class="risk-{risk_level.lower()}">{risk_level}</span></td></tr>
      <tr><td>Processing Duration</td><td>{processing_time:.2f} seconds</td></tr>
      <tr><td>AI Model</td><td>CNN-BiLSTM (MobileNetV2 backbone)</td></tr>
      <tr><td>Decision Threshold</td><td>0.50</td></tr>
    </table>
    <div class="action-box">
      <h3>Recommended Actions</h3>
      <ul>
        <li>Immediately review the flagged video footage</li>
        <li>Dispatch security personnel to the relevant aisle or zone</li>
        <li>Log the incident in the store security register</li>
        <li>Escalate to management if the event is confirmed</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <p>This alert was generated automatically by ShopGuard AI &mdash; NHPI, University of Bamenda</p>
    <p style="margin-top:4px;">Do not reply to this email. Contact your security team directly.</p>
  </div>
</div>
</body>
</html>
"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = sender_email
        msg["To"]      = RECIPIENT_EMAIL

        msg.attach(MIMEText(html_body, "html"))

        # Attach PDF report if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(pdf_path)}"',
            )
            msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, RECIPIENT_EMAIL, msg.as_string())

        return True, f"Alert sent to {RECIPIENT_EMAIL}"

    except smtplib.SMTPAuthenticationError:
        return False, (
            "Gmail authentication failed. Make sure you are using an App Password "
            "(not your Gmail login password). Enable 2-Step Verification, then go to "
            "Google Account > Security > App Passwords to generate one."
        )
    except Exception as e:
        return False, f"Email error: {str(e)}"
