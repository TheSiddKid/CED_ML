import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"


def test_model_artifacts_exist() -> None:
    required = [
        MODELS / "preprocessor.joblib",
        MODELS / "random_forest_model.joblib",
        MODELS / "metrics.json",
        MODELS / "metadata.json",
        MODELS / "feature_importance.csv",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"Missing artifacts: {missing}. Run training first."


def test_metrics_content() -> None:
    metrics_path = MODELS / "metrics.json"
    assert metrics_path.exists(), "metrics.json missing"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    for key in ["mae", "rmse", "r2", "unit", "train_rows", "test_rows"]:
        assert key in metrics

    assert metrics["train_rows"] > 0
    assert metrics["test_rows"] > 0
