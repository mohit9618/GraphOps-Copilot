
from langchain_groq import ChatGroq

from app.schemas.incident import RCAOutput
from app.state import State
from app.tools.rca import (
    combine_investigation_evidence,
    validate_rca_result,
)
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_llm = llm.with_structured_output(RCAOutput)



def rca_node(state: State) -> dict:
    log_analysis = state.get("log_analysis", "")
    metrics_analysis = state.get("metrics_analysis", "")

    log_evidence = state.get("log_evidence", [])
    metrics_evidence = state.get("metrics_evidence", [])

    # Backward compatibility with the current Log Analyst output.
    if not log_evidence:
        log_evidence = state.get("evidence", [])

    evidence_package = combine_investigation_evidence(
        log_analysis=log_analysis,
        metrics_analysis=metrics_analysis,
        log_evidence=log_evidence,
        metrics_evidence=metrics_evidence,
    )

    available_evidence = list(
        dict.fromkeys(log_evidence + metrics_evidence)
    )

    prompt = f"""
You are the Root Cause Analysis agent in GraphOps Copilot.

Analyze the incident using ONLY the investigation results below.
Do not invent logs, metrics, events, or dependencies.
Distinguish confirmed evidence from hypotheses.
If evidence is insufficient, state that clearly and use low confidence.

Incident ID: {state.get("incident_id", "unknown")}
Incident description: {state.get("incident_description", "")}
Affected service: {state.get("affected_service", "unknown")}
Severity: {state.get("severity", "unknown")}

Log analysis:
{evidence_package["log_analysis"]}

Metrics analysis:
{evidence_package["metrics_analysis"]}

Log evidence:
{evidence_package["log_evidence"]}

Metrics evidence:
{evidence_package["metrics_evidence"]}

Return:
- A concise root-cause hypothesis
- Confidence from 0.0 to 1.0
- Supporting evidence selected only from the supplied evidence
- Alternative hypotheses
- An explanation of the reasoning
"""

    result = structured_llm.invoke(prompt)

    validated = validate_rca_result(
        root_cause=result.root_cause,
        confidence=result.confidence,
        supporting_evidence=result.supporting_evidence,
        available_evidence=available_evidence,
    )

    errors = list(state.get("errors", []))

    if validated["unsupported_evidence"]:
        errors.append(
            "RCA returned evidence not present in the investigation results; "
            "unsupported items were excluded."
        )

    return {
        "root_cause": validated["root_cause"],
        "root_cause_confidence": validated["confidence"],
        "evidence": validated["supporting_evidence"],
        "errors": errors,
    }
