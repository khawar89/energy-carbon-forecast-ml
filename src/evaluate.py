"""Shared evaluation utilities for energy-carbon-forecast-ml.

Every model in this project, from persistence to XGBoost, is scored through
these functions. That is the point: when Session 5 claims "XGBoost beats
persistence by X," the claim is credible only if both numbers came from the
identical code path on the identical rows.

Design rules (from AGENTS.md and the learning plan):
  - All models are scored on the LEVEL (target_co2_next), even if a model
    predicted the delta internally. Convert before calling these functions.
  - All models in one comparison are scored on exactly the same rows:
    `comparison_table` drops any row where ANY model's prediction is missing,
    so no model gets an easier subset.
  - Every table carries the persistence skill score:
        skill = 1 - MAE_model / MAE_persistence
    Positive skill beats doing nothing; negative skill loses to it.

Self-test: `python src/evaluate.py` runs assertions on tiny hand-checkable
examples and prints OK. If it prints anything else, do not trust results
produced with this module.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Scalar metrics. Each takes two aligned arrays and returns one float.
# ---------------------------------------------------------------------------

def mae(y_true, y_pred) -> float:
    """Mean absolute error: the average size of a miss, in Mt CO2.

    Interpretable and robust to a few large misses; dominated by large
    COUNTRIES, though, because errors are in absolute Mt.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true, y_pred) -> float:
    """Root mean squared error: like MAE but squares each miss first.

    Squaring punishes large misses quadratically, so RMSE >> MAE signals
    that a model's error budget is concentrated in a few disasters.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def median_ae(y_true, y_pred) -> float:
    """Median absolute error: the typical miss for the typical country.

    Immune to the giants; compare with MAE to see how much of the average
    error is China/US scale versus everyone else.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.median(np.abs(y_true - y_pred)))


def mdape(y_true, y_pred, min_level: float = 1.0) -> float:
    """Median absolute percentage error, excluding near-zero emitters.

    Percentage errors explode as the denominator approaches zero (a 0.1 Mt
    miss on a 0.2 Mt emitter is 50 percent), so rows with observed emissions
    below `min_level` Mt are excluded and the exclusion is part of the
    metric's definition. Reported in percent.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    keep = y_true >= min_level
    return float(np.median(np.abs(y_true[keep] - y_pred[keep]) / y_true[keep]) * 100.0)


def skill(mae_model: float, mae_persistence: float) -> float:
    """Persistence skill score: 1 - MAE_model / MAE_persistence.

    0 means exactly as good as predicting no change; 0.25 means one quarter
    of persistence's average error was removed; negative means the model is
    WORSE than doing nothing and must be reported as losing.
    """
    return 1.0 - mae_model / mae_persistence


# ---------------------------------------------------------------------------
# Table builders. These operate on the modeling-table DataFrame.
# ---------------------------------------------------------------------------

def comparison_table(df: pd.DataFrame, prediction_cols: dict,
                     target_col: str = "target_co2_next",
                     persistence_col: str = "pred_persistence") -> pd.DataFrame:
    """Score several models on identical rows and return one tidy table.

    prediction_cols maps display name -> column name, e.g.
        {"persistence": "pred_persistence", "linear_trend": "pred_trend"}

    Rows where the target or ANY prediction is missing are dropped for ALL
    models (same-rows rule). The skill column is computed against the model
    named by `persistence_col`, which must be one of the prediction columns.
    """
    cols = [target_col] + list(prediction_cols.values())
    eligible = df.dropna(subset=cols)
    y = eligible[target_col]

    mae_persist = mae(y, eligible[persistence_col])
    rows = []
    for name, col in prediction_cols.items():
        p = eligible[col]
        rows.append({
            "model": name,
            "n_rows": len(eligible),
            "MAE": mae(y, p),
            "RMSE": rmse(y, p),
            "MedianAE": median_ae(y, p),
            "MdAPE_pct": mdape(y, p),
            "skill_vs_persistence": skill(mae(y, p), mae_persist),
        })
    return pd.DataFrame(rows)


def error_by_country(df: pd.DataFrame, prediction_col: str,
                     target_col: str = "target_co2_next") -> pd.DataFrame:
    """Per-country MAE for one model, sorted worst first.

    The input should already be restricted to one split and to rows where
    the prediction exists. This is the starting table for Session 6's error
    analysis and for the 'where does the model fail' README paragraph.
    """
    eligible = df.dropna(subset=[target_col, prediction_col]).copy()
    eligible["abs_err"] = (eligible[target_col] - eligible[prediction_col]).abs()
    out = eligible.groupby("country").agg(
        n=("abs_err", "size"),
        MAE=("abs_err", "mean"),
        mean_level=(target_col, "mean"),
    )
    out["MAE_pct_of_level"] = out["MAE"] / out["mean_level"] * 100.0
    return out.sort_values("MAE", ascending=False)


# ---------------------------------------------------------------------------
# Self-test on hand-checkable numbers.
# ---------------------------------------------------------------------------

def _self_test() -> None:
    y_true = [10.0, 20.0, 30.0]
    y_pred = [12.0, 20.0, 26.0]          # misses: 2, 0, 4

    assert abs(mae(y_true, y_pred) - 2.0) < 1e-12          # (2+0+4)/3
    assert abs(median_ae(y_true, y_pred) - 2.0) < 1e-12    # median(0,2,4)
    assert abs(rmse(y_true, y_pred) - np.sqrt(20 / 3)) < 1e-12
    # percentage misses: 2/10=20%, 0/20=0%, 4/30=13.33% -> median 13.33%
    assert abs(mdape(y_true, y_pred) - 100 * (4 / 30)) < 1e-9

    assert abs(skill(1.0, 2.0) - 0.5) < 1e-12              # halved the error
    assert skill(3.0, 2.0) < 0                             # worse than nothing

    df = pd.DataFrame({
        "country": ["A", "A", "B", "B"],
        "target_co2_next": [10.0, 20.0, 100.0, np.nan],
        "pred_persistence": [11.0, 22.0, 90.0, 5.0],
        "pred_trend": [10.0, 20.0, np.nan, 5.0],
    })
    t = comparison_table(df, {"persistence": "pred_persistence", "linear_trend": "pred_trend"})
    # Same-rows rule: row with NaN target AND row where trend is NaN are
    # dropped for BOTH models -> n_rows == 2 for both.
    assert (t["n_rows"] == 2).all()
    assert abs(t.loc[t.model == "linear_trend", "MAE"].iloc[0] - 0.0) < 1e-12
    assert abs(t.loc[t.model == "persistence", "skill_vs_persistence"].iloc[0] - 0.0) < 1e-12

    print("evaluate.py self-test: OK")


if __name__ == "__main__":
    _self_test()
