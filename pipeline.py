from langdetect import detect

def preprocess(text: str):
    try:
        lang = detect(text)
    except:
        lang = "en"
    # For hackathon MVP, just return text (skip real translation)
    return text
