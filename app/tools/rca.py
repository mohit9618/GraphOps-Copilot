
from typing import Any


def combine_investigation_evidence(
    log_analysis: str,
    metrics_analysis: str,
    log_evidence: list[str] | None = None,
    metrics_evidence: list[str] | None = None,
) -> dict[str, Any]:
    """Combine log and metric findings into a single evidence package."""

    return {
        "log_analysis": log_analysis,
        "metrics_analysis": metrics_analysis,
        "log_evidence": log_evidence or [],
        "metrics_evidence": metrics_evidence or [],
    }


def validate_rca_result(
    root_cause: str,
    confidence: float,
    supporting_evidence: list[str],
    available_evidence: list[str],
) -> dict[str, Any]:
    """Validate confidence and ensure cited evidence came from the investigation."""

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be between 0.0 and 1.0")

    if not root_cause.strip():
        raise ValueError("Root cause cannot be empty")

    unsupported = [
        item for item in supporting_evidence
        if item not in available_evidence
    ]

    return {
        "root_cause": root_cause,
        "confidence": confidence,
        "supporting_evidence": [
            item for item in supporting_evidence
            if item in available_evidence
        ],
        "unsupported_evidence": unsupported,
    }
