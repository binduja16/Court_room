from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import textwrap

def generate_pdf(summary, facts, petition, ipc_list, resources, filename="legal_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    def write_block(title, lines, font="Helvetica", bold=False):
        nonlocal y
        if y < 100:  # page break
            c.showPage()
            y = height - 50
        c.setFont("Helvetica-Bold" if bold else font, 12 if bold else 10)
        if title:
            c.drawString(50, y, title)
            y -= 20
        for line in lines:
            for wrapped in textwrap.wrap(line, width=90):
                if y < 50:  # page break
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, wrapped.strip())
                y -= 15
        y -= 10

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "⚖️ AI Courtroom Assistant Report")
    y -= 30

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    y -= 40

    # Sections
    write_block("📄 Simplified Summary", [summary], bold=True)

    # Clean Key Facts
    key_fact_lines = []
    for key, val in facts.items():
        if isinstance(val, list) and val:
            pretty_val = ", ".join(val)
        elif not val:
            pretty_val = "Not detected"
        else:
            pretty_val = str(val)
        key_fact_lines.append(f"- {key}: {pretty_val}")
    write_block("🔍 Key Facts", key_fact_lines, bold=True)

    # IPC Sections
    if ipc_list:
        ipc_lines = [f"Section {i['section']} - {i['description']}" for i in ipc_list]
        write_block("⚖️ Possible IPC Sections", ipc_lines, bold=True)

    # Draft Petition
    write_block("📝 Draft Petition", petition.split("\n"), bold=True)

    # Legal Aid Resources
    resource_lines = [f"- {r['Authority']}: {r['Helpline']}" for r in resources]
    write_block("📞 Free Legal Aid Resources", resource_lines, bold=True)

    c.save()
    return filename
