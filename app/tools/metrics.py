
from typing import Any


def query_metrics(
    metrics: dict[str, Any],
    metric_name: str | None = None,
) -> dict[str, Any]:
    """Retrieve all metrics or one named metric from an incident snapshot."""

    if metric_name is None:
        return metrics

    if metric_name not in metrics:
        return {
            "error": f"Metric '{metric_name}' was not found",
            "available_metrics": list(metrics.keys()),
        }

    return {metric_name: metrics[metric_name]}


def compare_metric_windows(
    current: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    """Compare current numeric metrics with their baseline values."""

    comparison = {}

    for name, current_value in current.items():
        baseline_value = baseline.get(name)

        if (
            isinstance(current_value, (int, float))
            and not isinstance(current_value, bool)
            and isinstance(baseline_value, (int, float))
            and not isinstance(baseline_value, bool)
        ):
            difference = current_value - baseline_value
            percentage_change = (
                (difference / abs(baseline_value)) * 100
                if baseline_value != 0
                else None
            )

            comparison[name] = {
                "current": current_value,
                "baseline": baseline_value,
                "difference": difference,
                "percentage_change": percentage_change,
            }

    return comparison
