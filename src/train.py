"""Clean-run reproduction of the final model comparison (Session 5).

Reproduces the whole result from a cold start, with no notebook state:
builds the modeling table if missing, refits every model on the frozen
configuration, and writes the validation and test metrics plus the raw test
predictions (for Session 6's error analysis).

    python src/train.py

DELIBERATELY GATED. The frozen XGBoost configurations below start as None.
They must be transcribed from the Session 5 notebook AFTER Khawar has run the
validation grid and frozen his choices; the script refuses to run until then,
so it can never fabricate a test result from placeholder settings. Ridge alpha
(0.1) and the HistGB settings are the values already frozen in Session 4.

Run in the reproducible environment (Python 3.12, scikit-learn 1.5.1,
xgboost 3.3.0) per requirements.txt.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor

import evaluate

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "processed" / "modeling_table.csv"
OUT_METRICS = ROOT / "results" / "model_comparison.csv"
OUT_TEST_PRED = ROOT / "results" / "test_predictions.csv"
OUT_PROVISIONAL = ROOT / "results" / "provisional_2024.csv"

SEED = 42

CORE = ["co2", "co2_lag1", "co2_lag3", "co2_lag5", "co2_lag10",
        "co2_roll5_mean", "co2_roll10_mean", "co2_slope5",
        "co2_per_capita", "share_global_co2",
        "population", "pop_growth5_pct", "cement_co2", "flaring_co2"]
NULLABLE = ["primary_energy_consumption", "energy_growth1_pct", "energy_per_capita"]
FEATURES = CORE + NULLABLE

# ---- Frozen configuration -------------------------------------------------
RIDGE_ALPHA = 0.1                       # frozen in Session 4
HGB = dict(max_depth=None, max_iter=300, learning_rate=0.05,
           early_stopping=False, random_state=SEED)
XGB_FIXED = dict(subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
                 random_state=SEED, n_jobs=-1)

# Frozen by Khawar Naeem, 14 Jul 2026: both validation-grid winners, taken as
# printed (early stopping on val chose the tree counts; see the Session 5 notebook).
XGB_LEVEL = dict(max_depth=6, learning_rate=0.10, n_trees=125)
XGB_DELTA = dict(max_depth=3, learning_rate=0.10, n_trees=173)


def _ensure_table() -> pd.DataFrame:
    if not TABLE.exists():
        import build_features
        build_features.main()
    return pd.read_csv(TABLE)


def _level(pred, base_co2, target_col):
    """Reconstruct the level: delta models predict the change, add it to co2_t."""
    return pred if target_col == "target_co2_next" else base_co2 + pred


def _fit_predict(fit_df, eval_df, target_col, kind):
    """Fit one model family on fit_df, predict the LEVEL on eval_df."""
    base = eval_df["co2"].to_numpy()
    if kind == "ridge":
        pipe = Pipeline([("impute", SimpleImputer(strategy="median")),
                         ("scale", StandardScaler()),
                         ("model", Ridge(alpha=RIDGE_ALPHA))])
        pipe.fit(fit_df[FEATURES], fit_df[target_col])
        return _level(pipe.predict(eval_df[FEATURES]), base, target_col)
    if kind == "hgb":
        m = HistGradientBoostingRegressor(**HGB)
        m.fit(fit_df[FEATURES], fit_df[target_col])
        return _level(m.predict(eval_df[FEATURES]), base, target_col)
    if kind == "xgb":
        cfg = XGB_LEVEL if target_col == "target_co2_next" else XGB_DELTA
        m = xgb.XGBRegressor(n_estimators=cfg["n_trees"], learning_rate=cfg["learning_rate"],
                             max_depth=cfg["max_depth"], **XGB_FIXED)
        m.fit(fit_df[FEATURES], fit_df[target_col])
        return _level(m.predict(eval_df[FEATURES]), base, target_col)
    raise ValueError(kind)


def _all_predictions(fit_df, eval_df):
    """Return eval_df with all eight prediction columns attached."""
    out = eval_df.copy()
    out["pred_persistence"] = out["co2"]
    out["pred_linear_trend"] = out["co2"] + out["co2_slope5"]
    out["pred_ridge_level"] = _fit_predict(fit_df, eval_df, "target_co2_next", "ridge")
    out["pred_ridge_delta"] = _fit_predict(fit_df, eval_df, "target_delta", "ridge")
    out["pred_hgb_level"] = _fit_predict(fit_df, eval_df, "target_co2_next", "hgb")
    out["pred_hgb_delta"] = _fit_predict(fit_df, eval_df, "target_delta", "hgb")
    out["pred_xgb_level"] = _fit_predict(fit_df, eval_df, "target_co2_next", "xgb")
    out["pred_xgb_delta"] = _fit_predict(fit_df, eval_df, "target_delta", "xgb")
    return out


PRED_COLS = {
    "persistence": "pred_persistence", "linear_trend": "pred_linear_trend",
    "ridge_level": "pred_ridge_level", "ridge_delta": "pred_ridge_delta",
    "hgb_level": "pred_hgb_level", "hgb_delta": "pred_hgb_delta",
    "xgb_level": "pred_xgb_level", "xgb_delta": "pred_xgb_delta",
}


def main() -> None:
    if XGB_LEVEL is None or XGB_DELTA is None:
        raise SystemExit(
            "Frozen XGBoost configs are not set. Run the Session 5 notebook, "
            "freeze XGB_LEVEL and XGB_DELTA, transcribe them into src/train.py, "
            "then re-run. (This guard prevents fabricating a test result from "
            "placeholder settings.)")

    df = _ensure_table()
    train = df[df["split"] == "train"]
    val = df[df["split"] == "val"]
    test = df[df["split"] == "test"]
    prov = df[df["split"] == "provisional_2024"]

    # Validation: models fitted on train only (reproduces the selection phase).
    val_scored = _all_predictions(train, val)
    val_table = evaluate.comparison_table(val_scored, PRED_COLS)
    val_table.insert(1, "split", "val")

    # Test: models refitted on train + val (through target-year 2018), the
    # frozen tree counts fixed, then scored ONCE on the held-out test years.
    fit_df = pd.concat([train, val], ignore_index=True)
    test_scored = _all_predictions(fit_df, test)
    test_table = evaluate.comparison_table(test_scored, PRED_COLS)
    test_table.insert(1, "split", "test")

    prov_scored = _all_predictions(fit_df, prov)
    prov_table = evaluate.comparison_table(prov_scored, PRED_COLS)
    prov_table.insert(1, "split", "provisional_2024")

    OUT_METRICS.parent.mkdir(parents=True, exist_ok=True)
    pd.concat([val_table, test_table], ignore_index=True).to_csv(OUT_METRICS, index=False)
    keep = ["country", "year", "target_year", "target_co2_next"] + list(PRED_COLS.values())
    test_scored[keep].to_csv(OUT_TEST_PRED, index=False)
    prov_table.to_csv(OUT_PROVISIONAL, index=False)

    print(f"wrote {OUT_METRICS.relative_to(ROOT)} (val + test rows)")
    print(f"wrote {OUT_TEST_PRED.relative_to(ROOT)} (per-row test predictions for Session 6)")
    print(f"wrote {OUT_PROVISIONAL.relative_to(ROOT)} (labeled provisional 2024)")
    print("\nTEST (targets 2019-2023), sorted by MAE:")
    print(test_table.sort_values("MAE").round(3).to_string(index=False))


if __name__ == "__main__":
    main()
