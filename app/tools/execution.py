
from typing import Any


ALLOWED_ACTIONS = {
    "collect_diagnostics",
    "check_service_health",
}


def execute_remediation(
    action_id: str,
    approval_status: str,
    approved_action_id: str,
    incident_id: str,
) -> dict[str, Any]:
    """Execute an allowlisted simulated action after approval checks."""

    if approval_status != "approved":
        raise PermissionError("Remediation has not been approved.")

    if not approved_action_id or approved_action_id != incident_id:
        raise PermissionError(
            "Approved action does not match the current incident."
        )

    if action_id not in ALLOWED_ACTIONS:
        raise ValueError(f"Action '{action_id}' is not allowlisted.")

    # Synthetic phase: no real infrastructure operation occurs.
    if action_id == "collect_diagnostics":
        return {
            "action_id": action_id,
            "status": "simulated",
            "message": "Diagnostic collection simulated successfully.",
        }

    if action_id == "check_service_health":
        return {
            "action_id": action_id,
            "status": "simulated",
            "message": "Service health check simulated successfully.",
        }

    raise ValueError(f"Action '{action_id}' is not implemented.")
