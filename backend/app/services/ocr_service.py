from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en'
)


def extract_text_blocks(image_path):

    results = ocr.ocr(image_path)

    extracted = []

    for line in results[0]:

        bbox = line[0]

        text = line[1][0]

        confidence = line[1][1]

        extracted.append({
            "text": text,
            "confidence": confidence,
            "bbox": bbox
        })

    return extracted