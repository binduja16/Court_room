from transformers import pipeline

summarizer = pipeline("summarization", model="google/pegasus-xsum")

def simplify_text(text: str) -> str:
    try:
        summary = summarizer(text[:1000], max_length=60, min_length=20, do_sample=False)
        return summary[0]['summary_text']
    except Exception:
        return "⚠️ Could not simplify document. Please read carefully."
