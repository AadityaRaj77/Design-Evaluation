import cv2


def highlight_problem_regions(
    image_path,
    regions,
    output_path
):

    image = cv2.imread(image_path)

    for region in regions:

        block = region["block"]

        x = block["x"]
        y = block["y"]
        w = block["width"]
        h = block["height"]

        label = region["label"]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            3
        )

        cv2.putText(
            image,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imwrite(
        output_path,
        image
    )

    return output_path