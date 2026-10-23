
from typing import TypedDict, Any


class State(TypedDict):
    incident_id: str
    incident_description: str
    severity: str
    affected_service: str
    investigation_priority: str

    logs: list[str]
    metrics: dict[str, Any]
    log_analysis: str
    metrics_analysis: str

    root_cause: str
    root_cause_confidence: float
    evidence: list[str]

    remediation_action_id: str
    execution_status: str
    suggested_remediation: str
    remediation_risk: str
    approval_status: str
    remediation_result: str
    approval_decision: dict | None

    verification_status: str
    verification_details: str
    verification_observations: list[str]

    errors: list[str]
