
from app.state import State
from app.tools.execution import execute_remediation


def execution_node(state: State) -> dict:
    incident_id = state.get("incident_id", "")
    action_id = state.get("remediation_action_id", "")

    try:
        result = execute_remediation(
            action_id=action_id,
            approval_status=state.get("approval_status", "pending"),
            approved_action_id=state.get("approved_action_id", ""),
            incident_id=incident_id,
        )

        return {
            "remediation_result": result["message"],
            "execution_status": result["status"],
            "errors": list(state.get("errors", [])),
        }

    except (PermissionError, ValueError) as exc:
        return {
            "remediation_result": "",
            "execution_status": "blocked",
            "errors": list(state.get("errors", [])) + [str(exc)],
        }
