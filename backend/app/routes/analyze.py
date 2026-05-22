import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.services.ai_service import analyze_ui_image
from app.services.vision_service import extract_dominant_colors
from app.services.ocr_service import extract_text_blocks
from app.services.text_analysis_service import compute_text_density

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_design(
    file: UploadFile = File(...)
):

    unique_filename = f"{uuid.uuid4()}.png"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    colors = extract_dominant_colors(file_path)

    text_blocks = extract_text_blocks(file_path)

    density = compute_text_density(text_blocks)

    result = await analyze_ui_image(contents)

    result["dominant_colors"] = colors
    result["text_density"] = density
    result["detected_text"] = text_blocks[:5]

    return result