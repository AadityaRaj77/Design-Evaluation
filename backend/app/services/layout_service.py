import cv2
import numpy as np


def compute_whitespace_ratio(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    _, threshold = cv2.threshold(
        gray,
        240,
        255,
        cv2.THRESH_BINARY
    )

    white_pixels = np.sum(threshold == 255)

    total_pixels = threshold.size

    whitespace_ratio = white_pixels / total_pixels

    return round(float(whitespace_ratio), 3)

def compute_edge_density(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_pixels = np.sum(edges > 0)

    total_pixels = edges.size

    density = edge_pixels / total_pixels

    return round(float(density), 3)

def compute_spacing_consistency(blocks):

    if len(blocks) < 2:
        return 1.0

    blocks = sorted(
        blocks,
        key=lambda b: b["y"]
    )

    gaps = []

    for i in range(len(blocks) - 1):

        current = blocks[i]

        next_block = blocks[i + 1]

        gap = next_block["y"] - (
            current["y"] + current["height"]
        )

        if gap > 0:
            gaps.append(gap)

    if not gaps:
        return 1.0

    mean_gap = sum(gaps) / len(gaps)

    variance = sum(
        (g - mean_gap) ** 2
        for g in gaps
    ) / len(gaps)

    consistency = 1 / (1 + variance)

    return round(float(consistency), 3)