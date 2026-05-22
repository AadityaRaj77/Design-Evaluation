def compute_text_density(text_blocks):

    total_chars = sum(
        len(block["text"])
        for block in text_blocks
    )

    return total_chars