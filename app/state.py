
from typing import TypedDict, Any


class State(TypedDict, total=False):
    incident_id: str
    incident_description: str
    severity: str
    affected_service: str

    logs: list[str]
    metrics: dict[str, Any]

    log_analysis: str
    metrics_analysis: str
    log_evidence: list[str]
    metrics_evidence: list[str]

    root_cause: str
    root_cause_confidence: float
    evidence: list[str]

    suggested_remediation: str
    remediation_risk: str

    approval_decision: dict | None
    approval_status: str
    approved_action_id: str

    remediation_action_id: str
    remediation_result: str
    execution_status: str

    verification_observations: list[str]
    verification_status: str
    verification_details: str

    investigation_priority: str
    errors: list[str]
