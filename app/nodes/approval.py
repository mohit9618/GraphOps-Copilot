
from langgraph.types import interrupt

from app.schemas.incident import ApprovalDecision
from app.state import State


def approval_node(state: State) -> dict:
    approval_request = {
        "incident_id": state.get("incident_id", "unknown"),
        "incident_description": state.get("incident_description", ""),
        "affected_service": state.get("affected_service", "unknown"),
        "severity": state.get("severity", "unknown"),
        "root_cause": state.get("root_cause", ""),
        "suggested_remediation": state.get("suggested_remediation", ""),
        "remediation_risk": state.get("remediation_risk", "unknown"),
    }

    # The graph pauses here until an external caller resumes it.
    decision_data = interrupt(approval_request)

    decision = ApprovalDecision.model_validate(decision_data)
    errors = list(state.get("errors", []))

    if not decision.approved:
        return {
            "approval_status": "rejected",
            "approved_action_id": "",
            "remediation_result": "Remediation rejected by approver.",
            "errors": errors,
        }

    if not decision.approved_by.strip():
        return {
            "approval_status": "pending",
            "approved_action_id": "",
            "errors": errors + ["Approver identity is required."],
        }

    return {
        "approval_status": "approved",
        "approved_action_id": state.get("incident_id", ""),
        "errors": errors,
    }
