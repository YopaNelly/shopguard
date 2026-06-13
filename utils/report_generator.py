from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os

TEAL   = (8,  145, 178)
NAVY   = (13, 27,  42)
GREY   = (71, 85, 105)
WHITE  = (255,255,255)
RED    = (239, 68,  68)
GREEN  = (16, 185, 129)
AMBER  = (245,158, 11)

class SentinelReport(FPDF):
    def __init__(self, store_name="Sentinel AI Platform"):
        super().__init__()
        self.store_name = store_name
        self.set_margins(15, 15, 15)

    def header(self):
        # Navy top bar
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.set_y(5)
        self.cell(0, 8, "SENTINEL AI  |  Shoplifting Detection Security Report", align="C")
        self.set_y(18)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*GREY)
        self.cell(0, 5,
            f"Confidential  |  Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  ShopGuard AI, NHPI University of Bamenda  |  Page {self.page_no()}",
            align="C")

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(*TEAL)
        self.rect(15, self.get_y(), 180, 8, 'F')
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.cell(0, 8, f"  {title.upper()}", ln=True)
        self.set_text_color(30, 30, 30)
        self.ln(2)

    def kpi_row(self, kpis):
        """kpis = list of (label, value, color_rgb)"""
        box_w = 180 / len(kpis)
        x0 = 15
        y0 = self.get_y()
        for label, value, color in kpis:
            self.set_fill_color(*color)
            self.rect(x0, y0, box_w - 3, 22, 'F')
            self.set_xy(x0, y0 + 2)
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(*WHITE)
            self.cell(box_w - 3, 10, str(value), align="C")
            self.set_xy(x0, y0 + 13)
            self.set_font("Helvetica", "", 7)
            self.cell(box_w - 3, 6, label, align="C")
            x0 += box_w
        self.set_xy(15, y0 + 25)
        self.set_text_color(30, 30, 30)

    def row_pair(self, label, value):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GREY)
        self.cell(50, 6, label)
        self.set_text_color(20, 20, 20)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 6, str(value), ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)


def generate_pdf_report(detection_df: pd.DataFrame, stats: dict, output_path: str,
                        last_analysis: dict = None):
    pdf = SentinelReport()
    pdf.add_page()

    # ── Cover info ──────────────────────────────────────
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Security Intelligence Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 5, f"Period: {datetime.now().strftime('%B %Y')}  |  Prepared by ShopGuard AI System", ln=True, align="C")
    pdf.ln(6)

    # ── KPI cards ───────────────────────────────────────
    pdf.kpi_row([
        ("Videos Analysed",   stats['total'],                   TEAL),
        ("Suspicious Events", stats['suspicious'],              RED),
        ("Normal Activity",   stats['normal'],                  GREEN),
        ("Avg Confidence",    f"{stats['avg_confidence']:.0f}%", (8,145,178)),
        ("Security Score",    f"{stats['security_score']:.0f}/100", (99,102,241)),
    ])

    # ── Executive summary ───────────────────────────────
    pdf.section_title("Executive Summary")
    threat_rate = (stats['suspicious'] / max(stats['total'], 1)) * 100
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5,
        f"The ShopGuard AI surveillance system has processed {stats['total']} video submissions "
        f"during this reporting period. The CNN-BiLSTM model (MobileNetV2 backbone, trained on UCF-Crime) "
        f"identified {stats['suspicious']} suspicious events, representing a {threat_rate:.1f}% threat rate. "
        f"Average model confidence across all analyses was {stats['avg_confidence']:.1f}%. "
        f"The composite security score stands at {stats['security_score']:.0f}/100, "
        f"{'indicating a secure environment.' if stats['security_score'] >= 70 else 'indicating elevated risk requiring review.'}"
    )
    pdf.ln(4)

    # ── Risk distribution ───────────────────────────────
    pdf.section_title("Risk Level Distribution")
    for risk_label, count in stats['risk_dist'].items():
        color = RED if risk_label == "High" else (AMBER if risk_label == "Medium" else GREEN)
        bar_w = min(130, int((count / max(stats['total'], 1)) * 130))
        y = pdf.get_y()
        pdf.set_fill_color(*color)
        pdf.rect(15, y, bar_w, 6, 'F')
        pdf.set_xy(15 + bar_w + 3, y)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(50, 6, f"{risk_label} Risk: {count} incidents")
        pdf.ln(8)

    # ── Last analysis detail ────────────────────────────
    if last_analysis:
        pdf.section_title("Most Recent Analysis")
        is_susp = last_analysis['prediction'] == 'Suspicious'
        status_color = RED if is_susp else GREEN
        pdf.set_fill_color(*status_color)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 9)
        verdict = "THREAT DETECTED" if is_susp else "NO THREAT DETECTED"
        pdf.cell(0, 8, f"  {verdict}  |  {last_analysis['prediction']} Activity", ln=True)
        pdf.set_text_color(30, 30, 30)
        pdf.ln(2)
        pdf.row_pair("Video File",       last_analysis['video_name'])
        pdf.row_pair("Anomaly Probability", f"{last_analysis['avg_prob']*100:.1f}%")
        pdf.row_pair("Model Confidence",  f"{last_analysis['confidence']*100:.1f}%")
        pdf.row_pair("Risk Level",        last_analysis['risk'])
        pdf.row_pair("Processing Time",   f"{last_analysis['processing_time']:.2f} seconds")
        pdf.row_pair("Timestamp",
            datetime.fromtimestamp(last_analysis['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))

    # ── Detections table (page 2) ───────────────────────
    pdf.add_page()
    pdf.section_title("Detection Log - Last 20 Events")

    cols  = ["Timestamp", "Video", "Prediction", "Confidence", "Risk"]
    widths = [40, 58, 28, 28, 26]

    # Header row
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 8)
    for col, w in zip(cols, widths):
        pdf.cell(w, 7, col, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    for i, (_, row) in enumerate(detection_df.tail(20).iterrows()):
        is_s = row['prediction'] == 'Suspicious'
        pdf.set_fill_color(245, 248, 255) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(widths[0], 6, str(row['timestamp'])[:16], border=1, fill=True)
        pdf.cell(widths[1], 6, str(row['video_name'])[:24], border=1, fill=True)
        pdf.set_text_color(*(RED if is_s else GREEN))
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(widths[2], 6, row['prediction'], border=1, fill=True, align="C")
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(widths[3], 6, f"{row['confidence']*100:.1f}%", border=1, fill=True, align="C")
        r_color = RED if row['risk_level'] == 'High' else (AMBER if row['risk_level'] == 'Medium' else GREEN)
        pdf.set_text_color(*r_color)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(widths[4], 6, row['risk_level'], border=1, fill=True, align="C")
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "", 8)
        pdf.ln()

    # ── Recommendations ─────────────────────────────────
    pdf.ln(6)
    pdf.section_title("Recommendations")
    recs = [
        ("Immediate Action",  "Review all High-risk flagged footage with security personnel within 24 hours."),
        ("Process Improvement", "Install additional cameras at blind spots identified in repeated suspicious zones."),
        ("Model Enhancement",   "Expand the training dataset with local footage for improved Cameroonian context accuracy."),
        ("Reporting Cadence",   "Generate weekly reports and share with store management and security supervisors."),
        ("Hardware Upgrade",    "Consider edge inference hardware for real-time per-frame processing capability."),
    ]
    for title, body in recs:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*TEAL)
        pdf.cell(0, 5, title, ln=True)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, body)
        pdf.ln(1)

    # ── Footer note ─────────────────────────────────────
    pdf.ln(4)
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(15, pdf.get_y(), 180, 14, 'F')
    pdf.set_xy(17, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(176, 5,
        "This report was automatically generated by ShopGuard AI. Results should be reviewed by "
        "a qualified security professional. The model achieves 83.33% recall on the UCF-Crime benchmark "
        "and is designed for deployment on standard hardware without GPU requirements.")

    pdf.output(output_path)
