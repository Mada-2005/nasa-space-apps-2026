"""Generate contracts/fixtures/sample_predictions.json.

Lane A runs this after every schema change so lanes B and C always have valid fake data.
The numbers are random. Nothing here is science.
"""
from __future__ import annotations

import json
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "contracts" / "fixtures" / "sample_predictions.json"

FEATURES = ["feature_a", "feature_b", "feature_c", "feature_d"]
LABELS = ["high", "medium", "low"]


def make_item(i: int, rng: random.Random) -> dict:
    score = round(rng.random(), 3)
    label = "high" if score > 0.66 else "medium" if score > 0.33 else "low"
    start = date(2025, 1, 1)
    series = [
        {"t": (start + timedelta(days=30 * k)).isoformat(), "v": round(rng.gauss(score, 0.1), 3)}
        for k in range(12)
    ]
    contribs = [rng.uniform(-1, 1) for _ in FEATURES]
    return {
        "id": f"item-{i:03d}",
        "location": {
            "frame": "earth",
            "lat": round(rng.uniform(22, 31.5), 4),   # Egypt bounding box, change per challenge
            "lon": round(rng.uniform(25, 35), 4),
            "name": f"Site {i}",
        },
        "time": "2025-12-01",
        "score": score,
        "label": label,
        "explanation": [
            {"feature": f, "contribution": round(c, 3)} for f, c in zip(FEATURES, contribs)
        ],
        "series": series,
    }


def main(n: int = 40, seed: int = 7) -> None:
    rng = random.Random(seed)
    bundle = {
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "challenge": "TBD: set in docs/CHALLENGE.md",
        "model": {
            "name": "mock-model",
            "version": "0.0",
            "metrics": {"val_f1": 0.0, "val_auc": 0.0},
            "notes": "Fixture data, not a real model.",
        },
        "items": [make_item(i, rng) for i in range(n)],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(bundle, indent=2))
    print(f"wrote {OUT} with {n} items")


if __name__ == "__main__":
    main()
