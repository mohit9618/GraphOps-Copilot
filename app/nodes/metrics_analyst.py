

from langchain_groq import ChatGroq

from app.schemas.incident import MetricsAnalysisOutput
from app.state import State
from dotenv import load_dotenv
load_dotenv()
from app.schemas.incident import MetricsAnalysisOutput
from app.state import State
from app.tools.metrics import query_metrics, compare_metric_windows


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

structured_llm = llm.with_structured_output(MetricsAnalysisOutput)


def metrics_analyst_node(state: State) -> dict:
    metrics = state.get("metrics", {})

    current = metrics.get("current", {})
    baseline = metrics.get("baseline", {})

    current_metrics = query_metrics(current)
    comparison = compare_metric_windows(current, baseline)

    prompt = f"""
    You are the metrics analyst for GraphOps Copilot.

    Incident:
    {state.get("incident_description", "Not provided")}

    Affected service:
    {state.get("affected_service", "Unknown")}

    Current metric snapshot:
    {current_metrics}

    Comparison with baseline:
    {comparison}

    Instructions:
    1. Identify abnormal metric values and significant changes.
    2. Explain which metrics may be related to the incident.
    3. Use only the supplied metric evidence.
    4. Do not invent thresholds or claim causation from correlation alone.
    5. If evidence is insufficient, explicitly state that.
    """

    result = structured_llm.invoke(prompt)

    return {
        "metrics_analysis": result.conclusion,
        "errors": [],
    }
