from langgraph.graph import StateGraph, END
from app.state import AgentState

from app.retrieval.retriever import retrieve
from app.generation.generator import generate

from app.grading.relevance import score_relevance
from app.grading.grounding import score_grounding
from app.grading.completeness import score_completeness

from app.confidence.scorer import compute_confidence
from app.memory.memory import rewrite_query


def evaluate(state):
    if state.confidence >= 0.75:
        return "accept"
    if state.failed_attempts >= 2:
        return "accept"
    return "retry"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.add_node("relevance", score_relevance)
    workflow.add_node("grounding", score_grounding)
    workflow.add_node("completeness", score_completeness)
    workflow.add_node("confidence", compute_confidence)

    workflow.add_node("rewrite", rewrite_query)

    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "relevance")
    workflow.add_edge("relevance", "grounding")
    workflow.add_edge("grounding", "completeness")
    workflow.add_edge("completeness", "confidence")

    workflow.add_conditional_edges(
        "confidence",
        evaluate,
        {
            "accept": END,
            "retry": "rewrite"
        }
    )

    workflow.add_edge("rewrite", "retrieve")

    return workflow.compile()
