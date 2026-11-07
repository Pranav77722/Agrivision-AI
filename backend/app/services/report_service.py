import io
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

from app.models.diagnosis import Diagnosis
from app.models.user import User
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self):
        self.storage = get_storage_service()

    async def generate_diagnostic_report(
        self,
        diagnosis: Diagnosis,
        user: Optional[User] = None,
        language: str = "en"
    ) -> str:
        """Generate a branded Agrivision AI+ diagnostic PDF report and return storage URL."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom branding styles
        brand_color = colors.HexColor("#1b5e20")  # Deep Forest Green
        secondary_color = colors.HexColor("#2e7d32")
        accent_color = colors.HexColor("#f1f8e9")
        dark_text = colors.HexColor("#212121")

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=brand_color,
            alignment=1,  # Center
        )

        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#555555"),
            alignment=1,
        )

        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=brand_color,
            spaceBefore=10,
            spaceAfter=4,
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=dark_text,
        )

        bold_style = ParagraphStyle(
            "BoldBody",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=dark_text,
        )

        story = []

        # Header Title
        story.append(Paragraph("AGRIVISION AI+", title_style))
        story.append(Paragraph("Comprehensive Plant Pathology & Crop Health Advisory Report", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=2, color=brand_color, spaceAfter=15))

        # Metadata Table
        report_id = f"AGRI-{str(diagnosis.id)[:8].upper()}"
        gen_time = datetime.now(timezone.utc).strftime("%d %B %Y, %H:%M UTC")
        farmer_name = user.full_name if user else "Registered Farmer"
        phone_num = user.phone if user else "N/A"

        meta_data = [
            [
                Paragraph("<b>Report ID:</b>", bold_style),
                Paragraph(report_id, body_style),
                Paragraph("<b>Date & Time:</b>", bold_style),
                Paragraph(gen_time, body_style),
            ],
            [
                Paragraph("<b>Farmer Name:</b>", bold_style),
                Paragraph(farmer_name, body_style),
                Paragraph("<b>Contact Phone:</b>", bold_style),
                Paragraph(phone_num, body_style),
            ],
            [
                Paragraph("<b>Target Crop:</b>", bold_style),
                Paragraph(diagnosis.crop_type, body_style),
                Paragraph("<b>Model Version:</b>", bold_style),
                Paragraph(diagnosis.model_version, body_style),
            ],
        ]

        meta_table = Table(meta_data, colWidths=[100, 170, 100, 170])
        meta_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), accent_color),
                ("BOX", (0, 0), (-1, -1), 1, brand_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c8e6c9")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ])
        )
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # Diagnosis Summary Section
        story.append(Paragraph("1. Diagnostic Analysis", section_heading))
        conf_percent = round(diagnosis.confidence * 100, 1)
        sev_percent = round(diagnosis.severity_percentage, 1)

        diag_data = [
            [Paragraph("<b>Parameter</b>", bold_style), Paragraph("<b>Observation / AI Assessment</b>", bold_style)],
            [Paragraph("Detected Condition / Disease:", body_style), Paragraph(f"<b>{diagnosis.predicted_disease}</b>", bold_style)],
            [Paragraph("Prediction Confidence:", body_style), Paragraph(f"{conf_percent}%", body_style)],
            [Paragraph("Severity Classification:", body_style), Paragraph(f"{diagnosis.severity} ({sev_percent}% area affected)", body_style)],
            [Paragraph("Status:", body_style), Paragraph(diagnosis.status.capitalize(), body_style)],
        ]

        diag_table = Table(diag_data, colWidths=[180, 360])
        diag_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f5e9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )
        story.append(diag_table)
        story.append(Spacer(1, 15))

        # Recommendations Section
        story.append(Paragraph("2. Integrated Treatment & Management Plan", section_heading))

        recs = diagnosis.recommendations or {}
        chem_controls = recs.get("chemical_control", [])
        org_controls = recs.get("organic_control", [])
        cult_practices = recs.get("cultural_practices", [])

        plan_data = [
            [Paragraph("<b>Strategy</b>", bold_style), Paragraph("<b>Actionable Recommendations</b>", bold_style)]
        ]

        if chem_controls:
            items_str = "<br/>".join([f"• {c}" for c in chem_controls[:3]])
            plan_data.append([Paragraph("<b>Chemical Control</b>", bold_style), Paragraph(items_str, body_style)])

        if org_controls:
            items_str = "<br/>".join([f"• {o}" for o in org_controls[:3]])
            plan_data.append([Paragraph("<b>Organic / Bio-Control</b>", bold_style), Paragraph(items_str, body_style)])

        if cult_practices:
            items_str = "<br/>".join([f"• {p}" for p in cult_practices[:3]])
            plan_data.append([Paragraph("<b>Cultural Practices</b>", bold_style), Paragraph(items_str, body_style)])

        if len(plan_data) == 1:
            plan_data.append([
                Paragraph("<b>Standard Care</b>", bold_style),
                Paragraph("Apply broad-spectrum copper fungicide, avoid waterlogging, and maintain balanced soil nutrition.", body_style)
            ])

        plan_table = Table(plan_data, colWidths=[140, 400])
        plan_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f5e9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        story.append(plan_table)
        story.append(Spacer(1, 20))

        # Safety Disclaimer & Helplines
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.gray, spaceAfter=10))
        disclaimer_text = (
            "<b>Disclaimer:</b> Agrivision AI+ recommendations are AI-assisted diagnostic guidance based on visual pattern recognition. "
            "Farmers are advised to adhere strictly to regional agrochemical label instructions and consult local Krishi Vigyan Kendra (KVK) "
            "or agricultural extension officers for localized conditions. Kisan Call Centre Toll-Free Helpline: 1800-180-1551."
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#777777"),
        )
        story.append(Paragraph(disclaimer_text, disclaimer_style))

        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Upload generated PDF
        pdf_filename = f"report_{diagnosis.id}_{language}.pdf"
        report_url = await self.storage.upload_file(
            file_bytes=pdf_bytes,
            filename=pdf_filename,
            content_type="application/pdf",
            folder="reports"
        )

        return report_url
