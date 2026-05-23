def aggregate_agent_results(
    agent_results
):

    scores = []

    all_issues = []

    all_suggestions = []

    for agent_name, result in agent_results.items():

        if not isinstance(result, dict):
            continue

        score = result.get("score")

        if score is not None:
            scores.append(score)

        issues = result.get(
            "issues",
            []
        )

        suggestions = result.get(
            "suggestions",
            []
        )

        all_issues.extend(issues)

        all_suggestions.extend(suggestions)

    overall_score = (
        sum(scores) / len(scores)
        if scores else 0
    )

    unique_issues = []

    seen_titles = set()

    for issue in all_issues:

        title = issue.get(
            "title",
            ""
        )

        if title not in seen_titles:

            seen_titles.add(title)

            unique_issues.append(issue)

    sorted_suggestions = sorted(
        all_suggestions,
        key=lambda s: s.get(
            "priority",
            999
        )
    )

    strongest_issue = (
        unique_issues[0]
        if unique_issues
        else None
    )

    return {

        "overall_score": round(
            overall_score,
            2
        ),

        "issues": unique_issues,

        "suggestions": sorted_suggestions[:5],

        "strongest_issue": strongest_issue,

        "agent_scores": {
            agent: result.get("score")
            for agent, result
            in agent_results.items()
        }
    }