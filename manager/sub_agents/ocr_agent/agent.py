from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from PIL import Image
import easyocr
import numpy as np
import cv2

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

EXCLUDE_KEYWORDS = ["Mute", "Unmute", "Zoom", "Recording", "Live", "AM", "PM"]

def preprocess_image(image_pil):
    image_np = np.array(image_pil.convert("L"))  # grayscale
    _, thresh = cv2.threshold(image_np, 150, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

def extract_names_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image_np = preprocess_image(image)

    results = reader.readtext(image_np, detail=0)
    names = [
        line.strip()
        for line in results
        if line.strip()
        and 2 <= len(line.strip()) <= 30
        and 1 <= len(line.strip().split()) <= 5
    ]

    names = [name for name in names if any(c.isupper() for c in name)]
    names = [name for name in names if not any(excl.lower() in name.lower() for excl in EXCLUDE_KEYWORDS)]

    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)

    return unique_names

ocr_agent = LlmAgent(
    name="ocr_extractor_agent",
    instruction="Extract participant names from the uploaded Zoom screenshot using OCR.",
    model = Gemini(model_name="gemini-1.5-flash")
)