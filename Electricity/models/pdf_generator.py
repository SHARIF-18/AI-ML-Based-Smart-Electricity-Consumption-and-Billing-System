from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def generate_pdf_report(user_name, date, appliances, total_units, total_cost, electricity_rate, suggestions=None):
    """
    Generate PDF report for daily electricity usage
    
    Args:
        user_name: Name of the user
        date: Date string (YYYY-MM-DD)
        appliances: List of appliance dicts
        total_units: Total units consumed
        total_cost: Total cost
        electricity_rate: Rate per unit
        suggestions: List of AI suggestions (optional)
        
    Returns:
        Path to generated PDF file
    """
    # Create reports directory
    os.makedirs('data/reports', exist_ok=True)
    
    # Generate filename
    filename = f"data/reports/electricity_report_{date}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("Smart Electricity Consumption Report", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # User information
    user_info = [
        ['Report Generated For:', user_name],
        ['Date:', date],
        ['Generated On:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Electricity Rate:', f'₹{electricity_rate:.2f} per unit']
    ]
    
    user_table = Table(user_info, colWidths=[2.5*inch, 4*inch])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(user_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Appliance details heading
    appliance_heading = Paragraph("Appliance Usage Details", heading_style)
    story.append(appliance_heading)
    story.append(Spacer(1, 0.1*inch))
    
    # Appliance table
    appliance_data = [['#', 'Appliance Name', 'Power (W)', 'Hours', 'Units', 'Cost (₹)']]
    
    for i, app in enumerate(appliances, 1):
        appliance_data.append([
            str(i),
            app['name'],
            str(app['power']),
            f"{app['hours']:.2f}",
            f"{app['units']:.3f}",
            f"₹{app['cost']:.2f}"
        ])
    
    appliance_table = Table(appliance_data, colWidths=[0.5*inch, 2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    appliance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    
    story.append(appliance_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary section
    summary_heading = Paragraph("Daily Summary", heading_style)
    story.append(summary_heading)
    story.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Total Units Consumed:', f'{total_units:.3f} kWh'],
        ['Total Cost:', f'₹{total_cost:.2f}'],
        ['Average Cost per Unit:', f'₹{electricity_rate:.2f}'],
        ['Number of Appliances:', str(len(appliances))]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#fef3c7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # AI Suggestions (if provided)
    if suggestions and len(suggestions) > 0:
        ai_heading = Paragraph("AI-Powered Recommendations", heading_style)
        story.append(ai_heading)
        story.append(Spacer(1, 0.1*inch))
        
        for suggestion in suggestions[:5]:  # Top 5 suggestions
            icon_map = {
                'warning': '⚠',
                'info': 'ℹ',
                'tip': '💡',
                'alert': '🔔',
                'success': '✓'
            }
            icon = icon_map.get(suggestion.get('type', 'info'), '•')
            
            suggestion_text = f"{icon} <b>{suggestion.get('title', '')}</b>: {suggestion.get('message', '')}"
            if suggestion.get('potential_saving', 0) > 0:
                suggestion_text += f" <i>(Potential Monthly Savings: ₹{suggestion['potential_saving']:.2f})</i>"
            
            suggestion_para = Paragraph(suggestion_text, normal_style)
            story.append(suggestion_para)
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Energy saving tips
    tips_heading = Paragraph("General Energy Saving Tips", heading_style)
    story.append(tips_heading)
    story.append(Spacer(1, 0.1*inch))
    
    tips = [
        "• Use LED bulbs instead of incandescent bulbs to save up to 75% on lighting costs",
        "• Set air conditioners to 24-25°C for optimal comfort and efficiency",
        "• Unplug devices when not in use to avoid phantom power consumption",
        "• Use natural light during the day whenever possible",
        "• Regular maintenance of appliances ensures optimal energy efficiency",
        "• Consider using timer switches for water heaters and geysers"
    ]
    
    for tip in tips:
        tip_para = Paragraph(tip, normal_style)
        story.append(tip_para)
    
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER
    )
    
    footer = Paragraph(
        "This report was generated by Smart Electricity Consumption & Billing System<br/>Track, Analyze, and Optimize your electricity usage",
        footer_style
    )
    story.append(footer)
    
    # Build PDF
    doc.build(story)
    
    return filename