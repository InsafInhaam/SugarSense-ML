import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

TESSERACT_PATH = "/opt/homebrew/bin/tesseract"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""
    
    for img in images:
        extracted_text += pytesseract.image_to_string(img)
        
    return extracted_text