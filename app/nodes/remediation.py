
from langchain_groq import ChatGroq

from app.schemas.incident import RemediationOutput
from app.state import State
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_llm = llm.with_structured_output(RemediationOutput)


def remediation_node(state: State) -> dict:
    prompt = f"""
You are the Remediation Planner agent in GraphOps Copilot.

Recommend a remediation for the incident using the supplied information.

Incident ID: {state.get("incident_id", "unknown")}
Incident description: {state.get("incident_description", "")}
Affected service: {state.get("affected_service", "unknown")}
Severity: {state.get("severity", "unknown")}

Root cause hypothesis:
{state.get("root_cause", "Not established")}

Root cause confidence:
{state.get("root_cause_confidence", 0.0)}

Supporting evidence:
{state.get("evidence", [])}

Log analysis:
{state.get("log_analysis", "")}

Metrics analysis:
{state.get("metrics_analysis", "")}

Requirements:
1. Propose one specific, actionable remediation.
2. Explain why it addresses the suspected root cause.
3. Describe the expected outcome and potential risk.
4. Set requires_approval to true.
5. Do not claim that any action has been executed.
6. If the root cause is uncertain, prefer a safe diagnostic or reversible action.
7. Do not invent infrastructure details or available tools.
"""

    result = structured_llm.invoke(prompt)

    return {
        "suggested_remediation": result.proposed_action,
        "remediation_risk": result.risk_level,
        "approval_status": "pending",
        "remediation_result": "",
    }
