import importlib
import sys
from pathlib import Path


def test_bulk_predictor_loads_models_from_repo_root(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    app_dir = repo_root / "app"

    monkeypatch.chdir(app_dir)
    sys.path.insert(0, str(app_dir))
    sys.modules.pop("services.bulk_predictor", None)

    import services.bulk_predictor as bulk_predictor

    model, preprocessor = bulk_predictor.load_model_artifacts()

    assert model is not None
    assert preprocessor is not None
