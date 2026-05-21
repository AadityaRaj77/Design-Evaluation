from fastapi import APIRouter, UploadFile, File

from app.services.ai_service import analyze_ui_image

router = APIRouter()


@router.post("/analyze")
async def analyze_design(
    file: UploadFile = File(...)
):

    image_bytes = await file.read()

    result = await analyze_ui_image(image_bytes)

    return result