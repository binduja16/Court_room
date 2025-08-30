def generate_draft(parties, amounts, dates, summary_text):
    draft = f"""
📝 Draft Petition

To,
{parties[0] if parties else "The Authority"}

Respected Sir/Madam,

I kindly submit the following petition regarding the matter involving:
- Parties: {', '.join(parties) if parties else "Not detected"}
- Amount: {', '.join(amounts) if amounts else "Not detected"}
- Dates: {', '.join(dates) if dates else "Not detected"}

Summary of Issue:
{summary_text if summary_text else "Not available"}

I request your urgent intervention in this matter.

Sincerely,
[Your Name]
"""
    return draft.strip()
