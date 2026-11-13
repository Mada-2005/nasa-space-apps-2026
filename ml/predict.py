"""Lane A: turn the trained model into ml/outputs/predictions.json (must pass the contract)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "ml" / "artifacts"
OUT = ROOT / "ml" / "outputs" / "predictions.json"


def label_for(score: float) -> str:
    return "high" if score > 0.66 else "medium" if score > 0.33 else "low"


def main() -> None:
    import joblib
    import pandas as pd

    bundle_in = joblib.load(ARTIFACTS / "model.joblib")
    model, feats = bundle_in["model"], bundle_in["features"]
    metrics = json.loads((ARTIFACTS / "metrics.json").read_text())[bundle_in["name"]]

    df = pd.read_parquet(ROOT / "data" / "processed" / "features.parquet")
    scores = model.predict_proba(df[feats])[:, 1]

    items = []
    for (_, row), s in zip(df.iterrows(), scores):
        items.append({
            "id": str(row["id"]),
            "location": {"frame": "earth", "lat": float(row["lat"]), "lon": float(row["lon"])},
            "time": str(row["time"])[:10],
            "score": float(s),
            "label": label_for(float(s)),
        })

    bundle = {
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "challenge": (ROOT / "docs" / "CHALLENGE.md").read_text().splitlines()[0].lstrip("# "),
        "model": {"name": bundle_in["name"], "version": "1.0", "metrics": metrics},
        "items": items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(bundle, indent=2))
    print(f"wrote {len(items)} predictions to {OUT}")


if __name__ == "__main__":
    main()
