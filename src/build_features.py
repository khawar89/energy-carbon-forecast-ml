"""Build the modeling table for energy-carbon-forecast-ml (Session 2).

Turns the raw OWID country-year panel into one flat table with:
  - the one-year-ahead target (and its delta parameterization),
  - wave-1 features that use only information available at year t,
  - chronological split labels keyed on the TARGET year.

Design principles (see ML_Learning_Plan_KhawarNaeem.md, Session 2):
  1. One table, built once, reused by every model. This is the ML analogue
     of a SQL staging table: models must differ in algorithm, never in data.
  2. All temporal operations happen per country (groupby) and on a
     gap-free yearly index, BEFORE any row filtering. Filtering first would
     leave holes in the series, and shift() is positional, not temporal:
     it grabs "the previous row," which is only "the previous year" when
     the rows are consecutive years.
  3. No feature for predicting year t+1 may use information after year t.

Usage:
    python src/build_features.py
Writes data/processed/modeling_table.csv (gitignored) and prints a
verification report. Exits with an error if any structural check fails.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Configuration: the frozen decisions from Session 1. Change these only by
# recording a new decision in CLAUDE.md first.
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "owid-co2-data.csv"
OUT_CSV = ROOT / "data" / "processed" / "modeling_table.csv"

MIN_HISTORY_YEARS = 40        # a country needs >= 40 non-missing co2 years
MIN_POPULATION = 1_000_000    # measured at feature year t (available at
                              # prediction time; the plan said "prediction
                              # year," but population at t+1 is not knowable
                              # at prediction time, so we use t and record
                              # the deviation)
TRAIN_END = 2014              # target years <= 2014 -> train
VAL_END = 2018                # target years 2015-2018 -> validation
TEST_END = 2023               # target years 2019-2023 -> headline test
                              # target year 2024 -> provisional appendix

# Wave-1 features: near-complete columns. Rows missing any of these are
# dropped (row-drop decision, 8 Jul 2026). Energy columns stay NULLABLE:
# they are feature candidates, and how to impute them is a per-model
# decision made in Session 4 (fitted on training years only).
CORE_FEATURES = [
    "co2", "co2_lag1", "co2_lag3", "co2_lag5", "co2_lag10",
    "co2_roll5_mean", "co2_roll10_mean", "co2_slope5",
    "co2_per_capita", "share_global_co2",
    "population", "pop_growth5_pct",
    "cement_co2", "flaring_co2",
]
NULLABLE_FEATURES = [
    "primary_energy_consumption", "energy_growth1_pct", "energy_per_capita",
]


def load_countries(path: Path = RAW_CSV) -> pd.DataFrame:
    """Load the raw CSV and keep genuine countries only.

    Real countries carry a 3-letter ISO code; aggregates (World, Asia,
    EU-27, ...) have no iso_code or one starting with OWID_. Sorting by
    (country, year) here is what makes every later groupby operation
    deterministic.
    """
    df = pd.read_csv(path)
    is_country = df["iso_code"].notna() & ~df["iso_code"].astype(str).str.startswith("OWID")
    cols = [
        "country", "iso_code", "year", "co2", "co2_per_capita",
        "share_global_co2", "population", "cement_co2", "flaring_co2",
        "primary_energy_consumption", "energy_per_capita",
    ]
    return df.loc[is_country, cols].sort_values(["country", "year"]).reset_index(drop=True)


def _one_country(g: pd.DataFrame) -> pd.DataFrame:
    """Add target and temporal features for a single country's series.

    The reindex step is the safety net: it inserts an explicit all-NaN row
    for any missing calendar year, so that shift(k) always means "k years
    ago," never "k rows ago." On a gap-free series it changes nothing; on
    a gapped one it prevents silently wrong lags.
    """
    g = g.set_index("year").reindex(range(int(g["year"].min()), int(g["year"].max()) + 1))
    g.index.name = "year"
    g["country"] = g["country"].ffill()          # restore keys on inserted rows
    g["iso_code"] = g["iso_code"].ffill()

    co2 = g["co2"]

    # ----- target: next year's co2, and its delta parameterization -------
    # shift(-1) pulls year t+1's value onto year t's row. This row's
    # features describe year t; its target lives in year t+1.
    g["target_co2_next"] = co2.shift(-1)
    g["target_delta"] = g["target_co2_next"] - co2

    # ----- lags: the value k years before t ------------------------------
    for k in (1, 3, 5, 10):
        g[f"co2_lag{k}"] = co2.shift(k)

    # ----- rolling means over windows ENDING at t ------------------------
    # rolling(5) at year t covers t-4..t inclusive: all information already
    # observed at prediction time, so this is legal. (Shift-before-roll is
    # only needed when year t itself must be excluded.)
    g["co2_roll5_mean"] = co2.rolling(5).mean()
    g["co2_roll10_mean"] = co2.rolling(10).mean()

    # ----- recent trend: average yearly change over the last 5 years -----
    g["co2_slope5"] = (co2 - co2.shift(5)) / 5.0

    # ----- context dynamics ----------------------------------------------
    # fill_method=None matters: pct_change's default forward-fills missing
    # values before differencing, which would FABRICATE a growth rate
    # across a data gap. With None, a gap yields NaN, which is the truth.
    g["pop_growth5_pct"] = g["population"].pct_change(5, fill_method=None) * 100.0
    g["energy_growth1_pct"] = g["primary_energy_consumption"].pct_change(1, fill_method=None) * 100.0

    return g.reset_index()


def add_target_and_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the per-country temporal logic to every country.

    group_keys=False keeps the output flat. Nothing here crosses a country
    boundary: the groupby is the wall between Zimbabwe's last year and
    Zambia's first.
    """
    parts = [_one_country(g) for _, g in df.groupby("country", sort=True)]
    return pd.concat(parts, ignore_index=True)


def filter_eligible(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the frozen eligibility rules AFTER features exist.

    Order matters: these rules delete rows. Had we filtered first, the
    deletions would punch holes in each country's series and corrupt the
    shifts. Rules (documented in the README):
      - >= 40 non-missing co2 years over the country's full history
        (a static, whole-series eligibility choice, not a feature);
      - population >= 1M at feature year t;
      - a target must exist (drops each country's final year);
      - all wave-1 core features present (row-drop decision, 8 Jul).
    """
    obs = df.dropna(subset=["co2"]).groupby("country")["co2"].size()
    df = df[df["country"].isin(obs[obs >= MIN_HISTORY_YEARS].index)]
    df = df[df["population"] >= MIN_POPULATION]
    df = df.dropna(subset=["target_co2_next"])
    df = df.dropna(subset=CORE_FEATURES)
    return df.reset_index(drop=True)


def add_splits(df: pd.DataFrame) -> pd.DataFrame:
    """Label chronological splits, keyed on the year being PREDICTED.

    A row with feature year 2014 predicts 2015, so it belongs to
    validation, not training: the split guards the target's vintage.
    """
    df["target_year"] = df["year"] + 1
    conditions = [
        df["target_year"] <= TRAIN_END,
        df["target_year"] <= VAL_END,
        df["target_year"] <= TEST_END,
        df["target_year"] == TEST_END + 1,
    ]
    df["split"] = np.select(conditions, ["train", "val", "test", "provisional_2024"], default="drop")
    return df[df["split"] != "drop"].reset_index(drop=True)


def verify(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    """Structural checks. Any failure raises: a wrong table must not ship."""
    # 1. One row per (country, feature-year).
    assert not df.duplicated(["country", "year"]).any(), "duplicate country-year rows"

    # 2. Qatar answer key from Session 1: the 2023 row predicts 2024.
    q = df.loc[(df["country"] == "Qatar") & (df["year"] == 2023), "target_co2_next"]
    assert len(q) == 1 and abs(q.iloc[0] - 125.812) < 0.01, f"Qatar 2023 target wrong: {q.values}"

    # 3. Targets do not cross country boundaries: for 200 random rows,
    #    target equals the raw csv's co2 at (same country, year + 1).
    raw_lookup = raw.set_index(["country", "year"])["co2"]
    sample = df.sample(min(200, len(df)), random_state=42)
    for _, r in sample.iterrows():
        expected = raw_lookup.get((r["country"], r["year"] + 1))
        assert expected is not None and abs(r["target_co2_next"] - expected) < 1e-9, \
            f"target mismatch for {r['country']} {r['year']}"

    # 4. Lags are temporal: lag5 equals the raw value 5 years earlier.
    for _, r in sample.iterrows():
        expected = raw_lookup.get((r["country"], r["year"] - 5))
        if expected is not None and not np.isnan(expected):
            assert abs(r["co2_lag5"] - expected) < 1e-9, \
                f"lag5 mismatch for {r['country']} {r['year']}"

    # 5. Split sanity: no target year beyond the provisional year.
    assert df["target_year"].max() <= TEST_END + 1, "target year beyond 2024"


def main() -> None:
    raw = load_countries()
    df = add_target_and_features(raw)
    df = filter_eligible(df)
    df = add_splits(df)
    verify(df, raw)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)

    print(f"modeling table: {df.shape[0]} rows, {df.shape[1]} columns, "
          f"{df['country'].nunique()} countries, feature years "
          f"{df['year'].min()}-{df['year'].max()}")
    print(df["split"].value_counts().reindex(["train", "val", "test", "provisional_2024"]).to_string())
    for col in NULLABLE_FEATURES:
        print(f"nullable feature {col}: {df[col].isna().mean() * 100:.1f}% missing")
    print(f"saved -> {OUT_CSV.relative_to(ROOT)}")
    print("all verification checks passed")


if __name__ == "__main__":
    main()
