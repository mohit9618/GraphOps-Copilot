
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, START, END


def approval_test_node(state):
    decision = interrupt({
        "incident_id": state["incident_id"],
        "suggested_remediation": state["suggested_remediation"],
    })

    if decision["approved"]:
        return {"approval_status": "approved"}

    return {"approval_status": "rejected"}


def test_approval_interrupt_and_resume():
    builder = StateGraph(dict)
    builder.add_node("approval", approval_test_node)
    builder.add_edge(START, "approval")
    builder.add_edge("approval", END)

    test_graph = builder.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "INC-TEST-001"}}

    initial_result = test_graph.invoke(
        {
            "incident_id": "INC-TEST-001",
            "suggested_remediation": "Collect diagnostics",
        },
        config=config,
    )

    assert "__interrupt__" in initial_result

    final_result = test_graph.invoke(
        Command(resume={
            "approved": True,
            "approved_by": "test-operator",
            "reason": "Test approval",
        }),
        config=config,
    )

    assert final_result["approval_status"] == "approved"
