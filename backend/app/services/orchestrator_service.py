from app.agents.layout_agent import analyze_layout
from app.agents.evaluator_agent import (
    evaluate_agent_outputs
)


async def run_design_agents(
    vision_metrics
):

    layout_result = await analyze_layout(
        vision_metrics
    )
    evaluation = await evaluate_agent_outputs(
    layout_result
    )

    return {
        "layout_analysis": layout_result,
        "evaluation": evaluation
    }