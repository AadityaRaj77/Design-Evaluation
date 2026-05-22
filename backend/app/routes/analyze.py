import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.services.ai_service import analyze_ui_image
from app.services.vision_service import extract_dominant_colors
from app.services.ocr_service import extract_text_blocks
from app.services.text_analysis_service import compute_text_density
from app.services.layout_service import (
    compute_whitespace_ratio,
    compute_edge_density
)
from app.services.component_service import detect_layout_blocks
from app.services.layout_service import compute_spacing_consistency
from app.services.orchestrator_service import run_design_agents
from app.services.memory_service import (
    store_review_memory
)

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
    layout_blocks = detect_layout_blocks(file_path)
    spacing_consistency = compute_spacing_consistency(
    layout_blocks
    )
    density = compute_text_density(text_blocks)
    whitespace_ratio = compute_whitespace_ratio(file_path)
    edge_density = compute_edge_density(file_path)
    vision_metrics = {
    "dominant_colors": colors,
    "text_density": density,
    "detected_text_count": len(text_blocks),
    "sample_text": [
        block["text"]
        for block in text_blocks[:10]
        ],
    "whitespace_ratio": whitespace_ratio,
    "edge_density": edge_density,
    "layout_block_count": len(layout_blocks),
    "spacing_consistency": spacing_consistency,
     }
    agent_results = await run_design_agents(
    vision_metrics
    )
    result = await analyze_ui_image(contents, vision_metrics)


    result["dominant_colors"] = colors
    result["text_density"] = density
    result["whitespace_ratio"] = whitespace_ratio
    result["edge_density"] = edge_density
    result["detected_text"] = text_blocks[:5]
    result["layout_blocks"] = layout_blocks[:10]
    result["agent_analysis"] = agent_results

    store_review_memory(
    result,
    vision_metrics
    )

    return result