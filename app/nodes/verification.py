
from langchain_groq import ChatGroq

from app.schemas.incident import VerificationOutput
from app.state import State

from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

structured_llm = llm.with_structured_output(VerificationOutput)


def verification_node(state: State) -> dict:
    execution_status = state.get("execution_status", "unknown")
    remediation_result = state.get("remediation_result", "")
    observations = state.get("verification_observations", [])
    
    if execution_status not in ("simulated", "success"):
        return {
            "verification_status": "unknown",
            "verification_details": (
                "Verification was not performed because remediation "
                "was not successfully executed."
            ),
        }

    if not observations:
        return {
            "verification_status": "unknown",
            "verification_details": (
                "Verification could not determine recovery because "
                "no post-execution observations were provided."
            ),
        }


    # Do not claim recovery if the action was blocked or never executed.
    if execution_status not in ("simulated", "success"):
        return {
            "verification_status": "unknown",
            "verification_details": (
                "Verification was not performed because remediation "
                "was not successfully executed."
            ),
        }

    prompt = f"""
You are the Verification agent in GraphOps Copilot.

Determine whether the incident appears resolved based only on the
provided post-execution observations.

Incident ID: {state.get("incident_id", "unknown")}
Incident description: {state.get("incident_description", "")}
Affected service: {state.get("affected_service", "unknown")}
Root cause hypothesis: {state.get("root_cause", "unknown")}

Execution status: {execution_status}
Execution result: {remediation_result}

Post-execution observations:
{observations}

Rules:
- Do not invent monitoring data or claim that a real service was checked.
- A simulated action alone is not proof of recovery.
- If observations are missing or insufficient, return unknown.
- Use resolved only when observations support recovery.
- Use partially_resolved when evidence shows improvement but not full recovery.
- Use unresolved when observations show that the problem persists.
"""

    result = structured_llm.invoke(prompt)

    return {
        "verification_status": result.status,
        "verification_details": result.summary,
    }
