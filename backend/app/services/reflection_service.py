def should_refine(
    evaluation
):

    quality_score = evaluation.get(
        "quality_score",
        10
    )

    return quality_score < 7