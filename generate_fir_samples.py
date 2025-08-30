# generate_fir_samples_bindu_jeevi_murthy.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_test_fir_pdf(filename="fir_bindu_jeevi_murthy.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1  # Center

    subtitle_style = styles['Heading2']
    subtitle_style.spaceAfter = 12

    body_style = ParagraphStyle(
        'body_style',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=10
    )

    story = []

    # Title
    story.append(Paragraph("Sample FIR Document", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Sub-header
    story.append(Paragraph("Multi-IPC Case Example", subtitle_style))
    story.append(Spacer(1, 0.1 * inch))

    # FIR content with Miss Bindu (complainant), Jeevi / Mr. Murthy (accused)
    lines = [
        "The police in Bengaluru have registered an FIR based on a complaint filed by <b>Miss Bindu</b>.",
        "The complainant alleges that <b>Jeevi</b>, also known as <b>Mr. Murthy</b>, cheated her of ₹3,00,000 by promising a rental property but never providing it.",
        "Furthermore, the accused <b>Jeevi alias Mr. Murthy</b> threatened the complainant with dire consequences if she reported the matter to the police.",
        "Additionally, it was discovered that the accused had stolen a gold chain worth ₹40,000 from Miss Bindu’s residence.",
        "In another incident, <b>Jeevi (Mr. Murthy)</b> has been arrested for allegedly assaulting his neighbor during a property dispute in Bengaluru on 22 August 2025.",
        "The cases involve multiple IPC sections including <b>cheating, theft, criminal intimidation, and assault</b>."
    ]

    for line in lines:
        story.append(Paragraph(line, body_style))

    doc.build(story)
    print(f"✅ FIR PDF generated: {filename}")

if __name__ == "__main__":
    generate_test_fir_pdf()
