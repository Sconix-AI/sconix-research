import json

from sconixlib import Run, gpu_info, set_seed


def test_set_seed_returns_seed():
    assert set_seed(123) == 123


def test_gpu_info_has_torch_key():
    assert "torch" in gpu_info()


def test_run_writes_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with Run("unit", config={"lr": 0.1}, batch=8) as run:
        run.log(step=0, loss=1.0)
        run.log(step=1, loss=0.5)
        run.summary(final_loss=0.5)

    assert (run.dir / "config.yaml").exists()
    assert (run.dir / "env.json").exists()
    summary = json.loads((run.dir / "summary.json").read_text())
    assert summary["status"] == "ok"
    assert summary["final_loss"] == 0.5
    assert summary["config"]["batch"] == 8
    lines = (run.dir / "metrics.jsonl").read_text().splitlines()
    assert len(lines) == 2


def test_run_records_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    try:
        with Run("boom") as run:
            raise ValueError("expected")
    except ValueError:
        pass
    summary = json.loads((run.dir / "summary.json").read_text())
    assert summary["status"] == "failed"
    assert "expected" in summary["error"]
