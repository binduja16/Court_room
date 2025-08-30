from pdfminer.high_level import extract_text
from PIL import Image
import pytesseract, io

def from_pdf(file_bytes: bytes) -> str:
    return extract_text(io.BytesIO(file_bytes))

def from_image(file_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img)

