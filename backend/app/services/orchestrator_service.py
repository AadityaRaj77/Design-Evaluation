from app.agents.layout_agent import analyze_layout
from app.agents.evaluator_agent import evaluate_agent_outputs
from app.agents.typography_agent import analyze_typography
from app.agents.color_agent import analyze_colors
from app.agents.ux_agent import analyze_ux
from app.agents.reflection_agent import refine_critique

from app.services.aggregator_service import aggregate_agent_results
from app.services.reflection_service import should_refine
from app.services.retrieval_service import retrieve_similar_reviews


async def run_design_agents(
    vision_metrics
):
    similar_reviews = retrieve_similar_reviews(
        vision_metrics
    )

    memory_context = []

    for review in similar_reviews:
        memory_context.append({
            "score": review.overall_score,
            "weakness": review.critique_summary,
            "density": review.text_density,
            "whitespace": review.whitespace_ratio
        })

    layout_result = await analyze_layout(
        vision_metrics,
        memory_context
    )

    typography_result = await analyze_typography(
        vision_metrics
    )

    color_result = await analyze_colors(
        vision_metrics
    )

    ux_result = await analyze_ux(
        vision_metrics
    )

    combined_outputs = {
        "layout": layout_result,
        "typography": typography_result,
        "color": color_result,
        "ux": ux_result
    }

    aggregated = aggregate_agent_results(
        combined_outputs
    )

    evaluation = await evaluate_agent_outputs(
        combined_outputs
    )

    refined_output = None

    if should_refine(evaluation):
        refined_output = await refine_critique(
            aggregated,
            evaluation
        )

    return {
        "agent_outputs": combined_outputs,
        "evaluation": evaluation,
        "aggregated_result": aggregated,
        "refined_output": refined_output
    }