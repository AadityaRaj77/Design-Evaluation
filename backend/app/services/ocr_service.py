import easyocr

reader = easyocr.Reader(['en'])


def extract_text_blocks(image_path):

    results = reader.readtext(image_path)

    extracted = []

    for result in results:

        try:

            bbox = result[0]
            text = result[1]
            confidence = result[2]
            extracted.append({
                "text": text,
                "confidence": float(confidence),
                "bbox": [
                  [int(point[0]), int(point[1])]
                  for point in bbox
                ]
            })

        except Exception:
            continue

    return extracted