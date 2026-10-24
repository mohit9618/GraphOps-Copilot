
from app.graph import graph


def test_graph_compiles():
    assert graph is not None


def test_graph_has_expected_nodes():
    expected_nodes = {
        "triage",
        "log_analyst",
        "metrics_analyst",
        "rca",
        "remediation",
        "approval",
        "execution",
        "verification",
    }

    assert expected_nodes.issubset(set(graph.nodes.keys()))
