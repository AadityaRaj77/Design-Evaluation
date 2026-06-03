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
    compute_edge_density,
    compute_spacing_consistency
)
from app.services.component_service import detect_layout_blocks
from app.services.orchestrator_service import run_design_agents
from app.services.memory_service import store_review_memory
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

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/analyze")
async def analyze_design(
    file: UploadFile = File(...)
):
    unique_filename = f"{uuid.uuid4()}.png"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save file first
    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Load image after saving
    absolute_path = os.path.abspath(
        file_path
    )

    image = cv2.imread(
        absolute_path
    )

    if image is None:
        raise Exception(
            f"Failed to load image: {absolute_path}"
        )

    image_height, image_width = image.shape[:2]

    # Basic analysis
    colors = extract_dominant_colors(
        file_path
    )

    text_blocks = extract_text_blocks(
        file_path
    )

    layout_blocks = detect_layout_blocks(
        file_path
    )

    spacing_consistency = compute_spacing_consistency(
        layout_blocks
    )

    density = compute_text_density(
        text_blocks
    )

    whitespace_ratio = compute_whitespace_ratio(
        file_path
    )

    edge_density = compute_edge_density(
        file_path
    )

    # Regions
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

    # Visualization paths
    layout_overlay_path = f"uploads/layout_{unique_filename}"
    ocr_overlay_path = f"uploads/ocr_{unique_filename}"
    issue_overlay_path = f"uploads/issues_{unique_filename}"

    # Generate overlays
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

    highlight_problem_regions(
        file_path,
        labeled_regions,
        issue_overlay_path
    )

    # Vision metrics
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
        "regions": labeled_regions
    }

    # Multi-agent analysis
    agent_results = await run_design_agents(
        vision_metrics
    )

    # Main AI vision review
    vision_review = await analyze_ui_image(
        contents,
        vision_metrics
    )

    final_response = {
        "vision_review": vision_review,
        "overall_score": agent_results["aggregated_result"].get(
            "overall_score",
            vision_review.get("overall_score", 0)
        ),
        "summary": vision_review.get("summary", {}),
        "metrics": vision_review.get("metrics", {}),
        "confidence": vision_review.get("confidence", 0.0),
        "agent_outputs": agent_results["agent_outputs"],
        "aggregated_result": agent_results["aggregated_result"],
        "evaluation": agent_results["evaluation"],
        "refined_output": agent_results["refined_output"],
        "dominant_colors": colors,
        "text_density": density,
        "whitespace_ratio": whitespace_ratio,
        "edge_density": edge_density,
        "detected_text": text_blocks[:5],
        "layout_blocks": layout_blocks[:10],
        "visualizations": {
            "layout_overlay": layout_overlay_path,
            "ocr_overlay": ocr_overlay_path,
            "issue_overlay": issue_overlay_path
        }
    }

    store_review_memory(
        final_response,
        vision_metrics
    )

    return final_response