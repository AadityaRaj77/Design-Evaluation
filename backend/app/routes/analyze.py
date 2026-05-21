from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/analyze")
async def analyze_design(
    file: UploadFile = File(...)
):

    return {
        "message": "Pipeline working",
        "filename": file.filename
    }