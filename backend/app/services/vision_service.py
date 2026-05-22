from PIL import Image
import numpy as np
from collections import Counter


def extract_dominant_colors(image_path, num_colors=5):

    image = Image.open(image_path)

    image = image.resize((150, 150))

    pixels = np.array(image).reshape(-1, 3)

    pixels = [tuple(pixel) for pixel in pixels]

    most_common = Counter(pixels).most_common(num_colors)

    dominant_colors = [
        color[0] for color in most_common
    ]

    return dominant_colors