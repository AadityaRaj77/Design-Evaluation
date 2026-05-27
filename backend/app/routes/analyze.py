import os
import uuid
import cv2

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
from app.services.visualization_service import (
    draw_layout_blocks,
    draw_ocr_boxes
)
from app.services.region_service import (
    find_largest_blocks,
    label_layout_block
)
from app.services.issue_visualization_service import (
    highlight_problem_regions
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
    # image = cv2.imread(file_path)
    absolute_path = os.path.abspath(file_path)

    image = cv2.imread(absolute_path)

    if image is None:

      raise Exception(
        f"Failed to load image: {absolute_path}"
      )
    image_height, image_width = image.shape[:2]

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    colors = extract_dominant_colors(file_path)

    text_blocks = extract_text_blocks(file_path)
    layout_blocks = detect_layout_blocks(file_path)
    spacing_consistency = compute_spacing_consistency(
    layout_blocks
    )
    layout_overlay_path = (
    f"uploads/layout_{unique_filename}"
    )
    ocr_overlay_path = (
    f"uploads/ocr_{unique_filename}"
    )
    largest_blocks = find_largest_blocks(
    layout_blocks
    )

    labeled_regions = []

    for block in largest_blocks:

      label = label_layout_block(
         block,
         image_width,
         image_height
        )

      labeled_regions.append({
        "label": label,
        "block": block
      })

    draw_ocr_boxes(
      file_path,
      text_blocks,
      ocr_overlay_path
    )   

    draw_layout_blocks(
      file_path,
      layout_blocks,
      layout_overlay_path
    )

    issue_overlay_path = (
      f"uploads/issues_{unique_filename}"
    )

    highlight_problem_regions(
       file_path,
       labeled_regions,
       issue_overlay_path
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
    "regions": labeled_regions,
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
    result["visualizations"] = {
    "layout_overlay":
        layout_overlay_path,
    "ocr_overlay":
        ocr_overlay_path,
    "issue_overlay":
        issue_overlay_path,
}

    store_review_memory(
    result,
    vision_metrics
    )

    return result