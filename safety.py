# safety.py
import re

# Regex for detecting legal advice
ADVICE = re.compile(r'\b(you should|file a case|hire a lawyer|legal advice)\b', re.I)

def advice_filter(text: str) -> bool:
    """
    Returns True if the text contains legal advice-like statements.
    """
    return bool(ADVICE.search(text))

def check_safety(text: str) -> bool:
    """
    Check if extracted text is safe to display.
    - Blocks banned words
    - Blocks explicit legal advice
    Returns True if safe, False if unsafe.
    """
    banned_words = ["terrorism", "violence", "hate speech", "fake notice"]

    for word in banned_words:
        if word.lower() in text.lower():
            return False
    
    if advice_filter(text):
        return False

    return True
