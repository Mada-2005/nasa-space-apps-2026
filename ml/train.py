"""Lane A: train a baseline model.

Order of work (do not skip steps):
1. Load features from data/processed/features.parquet (lane C produces it).
2. Split by TIME or by REGION, never randomly, so the metric is honest
   (random splits leak neighbouring pixels/days into validation).
3. Fit the simplest baseline first (persistence / climatology / logistic regression).
4. Fit one stronger model (gradient boosting). Keep it only if it beats the baseline on validation.
5. Save model + metrics to ml/artifacts/.

Judges score Validity: "is it scientifically sound, does it achieve its goal".
A baseline comparison table is the cheapest way to prove that.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "data" / "processed" / "features.parquet"
ARTIFACTS = ROOT / "ml" / "artifacts"


def main() -> None:
    import pandas as pd
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score, roc_auc_score

    if not FEATURES.exists():
        raise SystemExit(f"Missing {FEATURES}. Ask lane C (data) for it, or use MOCK=1 meanwhile.")

    df = pd.read_parquet(FEATURES)
    target = "target"           # TODO: set per challenge
    time_col = "time"           # TODO: set per challenge
    feature_cols = [c for c in df.columns if c not in {target, time_col, "id", "lat", "lon"}]

    df = df.sort_values(time_col)
    cut = int(len(df) * 0.8)
    train, val = df.iloc[:cut], df.iloc[cut:]

    results = {}
    models = {
        "baseline_logreg": LogisticRegression(max_iter=1000),
        "hgb": HistGradientBoostingClassifier(),
    }
    for name, model in models.items():
        model.fit(train[feature_cols], train[target])
        p = model.predict_proba(val[feature_cols])[:, 1]
        results[name] = {
            "val_auc": float(roc_auc_score(val[target], p)),
            "val_f1": float(f1_score(val[target], p > 0.5)),
        }
        print(name, results[name])

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "metrics.json").write_text(json.dumps(results, indent=2))
    best = max(results, key=lambda k: results[k]["val_auc"])
    import joblib

    joblib.dump({"model": models[best], "features": feature_cols, "name": best},
                ARTIFACTS / "model.joblib")
    print("best:", best)


if __name__ == "__main__":
    main()
