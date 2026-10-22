
from app.tools.metrics import query_metrics, compare_metric_windows


def test_query_metrics():
    metrics = {
        "request_latency_ms": 4200,
        "error_rate_percent": 12.5,
    }

    assert query_metrics(metrics, "request_latency_ms") == {
        "request_latency_ms": 4200
    }


def test_compare_metric_windows():
    current = {"request_latency_ms": 4200}
    baseline = {"request_latency_ms": 250}

    result = compare_metric_windows(current, baseline)

    assert result["request_latency_ms"]["difference"] == 3950
    assert result["request_latency_ms"]["percentage_change"] == 1580.0
