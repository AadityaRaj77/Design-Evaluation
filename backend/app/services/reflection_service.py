def should_refine(
    evaluation
):

    quality_score = evaluation.get(
        "quality_score",
        10
    )

    if quality_score < 7:
        return True

    return False