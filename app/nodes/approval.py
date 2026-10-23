
from app.schemas.incident import ApprovalDecision
from app.state import State


def approval_node(state: State) -> dict:
    decision_data = state.get("approval_decision")

    if not decision_data:
        return {
            "approval_status": "pending",
            "errors": state.get("errors", []),
        }

    if isinstance(decision_data, ApprovalDecision):
        decision = decision_data
    else:
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
        errors.append("Approval rejected: approver identity is required.")
        return {
            "approval_status": "pending",
            "approved_action_id": "",
            "errors": errors,
        }

    return {
        "approval_status": "approved",
        "approved_action_id": state.get("incident_id", ""),
        "errors": errors,
    }
