import cv2


def draw_layout_blocks(
    image_path,
    layout_blocks,
    output_path
):

    image = cv2.imread(image_path)

    for block in layout_blocks:

        x = block["x"]
        y = block["y"]
        w = block["width"]
        h = block["height"]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imwrite(
        output_path,
        image
    )

    return output_path

# ocr overlay
def draw_ocr_boxes(
    image_path,
    text_blocks,
    output_path
):

    image = cv2.imread(image_path)

    for block in text_blocks:

        try:

            bbox = block["bbox"]

            points = [
                tuple(point)
                for point in bbox
            ]

            for i in range(4):

                cv2.line(
                    image,
                    points[i],
                    points[
                        (i + 1) % 4
                    ],
                    (255, 0, 0),
                    2
                )

        except Exception:
            continue

    cv2.imwrite(
        output_path,
        image
    )

    return output_path