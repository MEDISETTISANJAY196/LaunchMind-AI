import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.core.config import settings

class PDFService:
    @staticmethod
    def generate_startup_report(
        startup_name: str,
        industry: str,
        stage: str,
        description: str,
        swot_data: dict,
        canvas_data: dict,
        market_data: dict,
        branding_data: dict,
        output_filename: str
    ) -> str:
        """Compiles startup indicators into a stylized, printable PDF report."""
        # Ensure target folder exists
        reports_dir = os.path.join(settings.UPLOADS_DIR, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, output_filename)
        
        # Init PDF document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#4B5563'),
            spaceAfter=25
        )
        
        h2_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#1E3A8A'),
            spaceBefore=15,
            spaceAfter=10,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=8
        )
        
        bold_body_style = ParagraphStyle(
            'ReportBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=11,
            textColor=colors.white
        )

        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#374151')
        )

        story = []
        
        # 1. Title Block
        story.append(Paragraph("LaunchMind-AI Business Blueprint", title_style))
        story.append(Paragraph(f"Analysis Report for <b>{startup_name}</b> | Industry: {industry or 'N/A'} | Stage: {stage or 'N/A'}", subtitle_style))
        story.append(Spacer(1, 10))
        
        # 2. Executive Summary
        story.append(Paragraph("Executive Summary", h2_style))
        story.append(Paragraph(description or "No business description provided yet.", body_style))
        story.append(Spacer(1, 12))
        
        # 3. Market Sizing (TAM/SAM/SOM)
        story.append(Paragraph("Market Research & Sizing", h2_style))
        tam_text = market_data.get('tam') or "N/A"
        sam_text = market_data.get('sam') or "N/A"
        som_text = market_data.get('som') or "N/A"
        
        market_table_data = [
            [Paragraph("Market Segment", table_header_style), Paragraph("Sizing & Description", table_header_style)],
            [Paragraph("<b>TAM (Total Addressable)</b>", table_cell_style), Paragraph(tam_text, table_cell_style)],
            [Paragraph("<b>SAM (Serviceable Addressable)</b>", table_cell_style), Paragraph(sam_text, table_cell_style)],
            [Paragraph("<b>SOM (Serviceable Obtainable)</b>", table_cell_style), Paragraph(som_text, table_cell_style)]
        ]
        
        # Table width fits letter page: width = 8.5" = 612pt. Margins are 40 + 40 = 80. Content area = 532pt
        market_table = Table(market_table_data, colWidths=[180, 352])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
        ]))
        story.append(market_table)
        
        if market_data.get('target_demographics'):
            story.append(Spacer(1, 10))
            story.append(Paragraph("<b>Target Demographics:</b>", bold_body_style))
            story.append(Paragraph(market_data.get('target_demographics'), body_style))
            
        if market_data.get('customer_personas'):
            story.append(Paragraph("<b>Ideal Customer Persona:</b>", bold_body_style))
            story.append(Paragraph(market_data.get('customer_personas'), body_style))
            
        story.append(Spacer(1, 15))
        
        # 4. SWOT Analysis Matrix
        story.append(Paragraph("SWOT Matrix Analysis", h2_style))
        s_list = swot_data.get('strengths') or "N/A"
        w_list = swot_data.get('weaknesses') or "N/A"
        o_list = swot_data.get('opportunities') or "N/A"
        t_list = swot_data.get('threats') or "N/A"
        
        swot_table_data = [
            [Paragraph("Strengths (S)", table_header_style), Paragraph("Weaknesses (W)", table_header_style)],
            [Paragraph(s_list, table_cell_style), Paragraph(w_list, table_cell_style)],
            [Paragraph("Opportunities (O)", table_header_style), Paragraph("Threats (T)", table_header_style)],
            [Paragraph(o_list, table_cell_style), Paragraph(t_list, table_cell_style)]
        ]
        
        swot_table = Table(swot_table_data, colWidths=[266, 266])
        swot_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1E3A8A')),
            ('BACKGROUND', (0,2), (1,2), colors.HexColor('#1E3A8A')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
            ('BACKGROUND', (0,1), (0,1), colors.HexColor('#EFF6FF')), # Light blue strength
            ('BACKGROUND', (1,1), (1,1), colors.HexColor('#FEF2F2')), # Light red weakness
            ('BACKGROUND', (0,3), (0,3), colors.HexColor('#ECFDF5')), # Light green opportunity
            ('BACKGROUND', (1,3), (1,3), colors.HexColor('#FFFBEB')), # Light amber threat
        ]))
        story.append(swot_table)
        
        if swot_data.get('ai_feedback'):
            story.append(Spacer(1, 10))
            story.append(Paragraph("<b>SWOT Strategic Analysis:</b>", bold_body_style))
            story.append(Paragraph(swot_data.get('ai_feedback'), body_style))
            
        story.append(Spacer(1, 15))
        
        # 5. Business Model Canvas
        story.append(Paragraph("Business Model Canvas", h2_style))
        
        # Canvas grid structure (9 boxes). Let's construct a simplified 3-column table
        canvas_table_data = [
            [
                Paragraph("<b>Key Partners</b><br/>" + (canvas_data.get('key_partners') or "N/A"), table_cell_style),
                Paragraph("<b>Key Activities</b><br/>" + (canvas_data.get('key_activities') or "N/A") + "<br/><br/><b>Key Resources</b><br/>" + (canvas_data.get('key_resources') or "N/A"), table_cell_style),
                Paragraph("<b>Value Propositions</b><br/>" + (canvas_data.get('value_propositions') or "N/A"), table_cell_style),
                Paragraph("<b>Customer Relationships</b><br/>" + (canvas_data.get('customer_relationships') or "N/A") + "<br/><br/><b>Channels</b><br/>" + (canvas_data.get('channels') or "N/A"), table_cell_style),
                Paragraph("<b>Customer Segments</b><br/>" + (canvas_data.get('customer_segments') or "N/A"), table_cell_style)
            ],
            [
                Paragraph("<b>Cost Structure</b><br/>" + (canvas_data.get('cost_structure') or "N/A"), table_cell_style),
                Paragraph("", table_cell_style), # empty spacer span
                Paragraph("<b>Revenue Streams</b><br/>" + (canvas_data.get('revenue_streams') or "N/A"), table_cell_style),
                Paragraph("", table_cell_style),
                Paragraph("", table_cell_style)
            ]
        ]
        
        # Col widths summing to 532:
        canvas_table = Table(canvas_table_data, colWidths=[106, 106, 108, 106, 106])
        canvas_table.setStyle(TableStyle([
            ('SPAN', (0,1), (1,1)), # Cost structure takes 2 cols span
            ('SPAN', (2,1), (4,1)), # Revenue streams takes 3 cols span
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#9CA3AF')),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB'))
        ]))
        story.append(canvas_table)
        story.append(Spacer(1, 15))
        
        # 6. Branding Blueprint
        story.append(Paragraph("Branding & Slogan Blueprint", h2_style))
        story.append(Paragraph(f"<b>Suggested Brand Names:</b> {branding_data.get('name_suggestions') or 'N/A'}", body_style))
        story.append(Paragraph(f"<b>Suggested Slogans:</b> {branding_data.get('slogans') or 'N/A'}", body_style))
        story.append(Paragraph(f"<b>Brand Colors Palette:</b> {branding_data.get('brand_colors') or 'N/A'}", body_style))
        story.append(Paragraph(f"<b>Suggested Logo Art Concept:</b> {branding_data.get('logo_description') or 'N/A'}", body_style))
        
        # Build PDF
        doc.build(story)
        return file_path
pdf_service = PDFService()
