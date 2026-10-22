from langchain_groq import ChatGroq

from app.schemas.incident import TriageOutput
from app.state import State
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
)

structured_llm = llm.with_structured_output(TriageOutput)


def triage_node(state: State) -> dict:
    """Classify an incident and determine its investigation priority."""

    prompt = f"""
    You are the incident triage agent in GrapgOps Copilot, an AI incident
    response copilot.

    Analyze the incident information and return a structured triage result.

    Incident ID: {state.get("incident_id", "unknown")}
    Description: {state.get("incident_description", "Not provided")}
    Affected service: {state.get("affected_service", "Unknown")}
    Initial severity: {state.get("severity", "unknown")}

    Instructions:
    1. Classify severity as low, medium, high, or critical.
    2. Assign investigation priority: low, medium, high, or urgent.
    3. Identify the affected service.
    4. Write a concise incident summary and explain your reasoning.
    5. Use only the supplied information. Do not invent logs, metrics,
       root causes, or evidence.
    """

    result = structured_llm.invoke(prompt)

    return {
        "severity": result.severity,
        "affected_service": result.affected_service,
        "incident_description": result.incident_summary,
        "investigation_priority": result.investigation_priority,
    }
