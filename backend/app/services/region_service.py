def find_largest_blocks(
    layout_blocks,
    top_k=3
):

    sorted_blocks = sorted(
        layout_blocks,
        key=lambda b: b["area"],
        reverse=True
    )

    return sorted_blocks[:top_k]

# region labelling
def label_layout_block(
    block,
    image_width,
    image_height
):

    center_y = (
        block["y"]
        + block["height"] / 2
    )

    relative_y = (
        center_y / image_height
    )

    if relative_y < 0.25:
        return "top_section"

    elif relative_y < 0.65:
        return "middle_section"

    return "bottom_section"