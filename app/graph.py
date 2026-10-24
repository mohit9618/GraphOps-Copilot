
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import State
from app.nodes.triage import triage_node
from app.nodes.log_analyst import log_analyst_node
from app.nodes.metrics_analyst import metrics_analyst_node
from app.nodes.rca import rca_node
from app.nodes.remediation import remediation_node
from app.nodes.approval import approval_node
from app.nodes.execution import execution_node
from app.nodes.verification import verification_node


def route_after_approval(state: State) -> str:
    if state.get("approval_status") == "approved":
        return "execution"

    return END


def route_after_execution(state: State) -> str:
    if state.get("execution_status") in ("simulated", "success"):
        return "verification"

    return END


builder = StateGraph(State)

builder.add_node("triage", triage_node)
builder.add_node("log_analyst", log_analyst_node)
builder.add_node("metrics_analyst", metrics_analyst_node)
builder.add_node("rca", rca_node)
builder.add_node("remediation", remediation_node)
builder.add_node("approval", approval_node)
builder.add_node("execution", execution_node)
builder.add_node("verification", verification_node)

builder.add_edge(START, "triage")

# Run the two independent analysts in parallel.
builder.add_edge("triage", "log_analyst")
builder.add_edge("triage", "metrics_analyst")

builder.add_edge("log_analyst", "rca")
builder.add_edge("metrics_analyst", "rca")

builder.add_edge("rca", "remediation")
builder.add_edge("remediation", "approval")

builder.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "execution": "execution",
        END: END,
    },
)

builder.add_conditional_edges(
    "execution",
    route_after_execution,
    {
        "verification": "verification",
        END: END,
    },
)

builder.add_edge("verification", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
