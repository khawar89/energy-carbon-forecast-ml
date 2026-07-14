# Session 7 check questions and reproducibility record

Recorded 14 July 2026. Answers prepared with Claude's full guidance at
Khawar's request (same attribution convention as the Session 3, 5, and 6
records). Session 7 has no notebook; its artifact is the verified clean-clone
reproduction, the README reproduction section, and this record.

## Clean-clone reproduction (the session's core gate)

Performed 14 July 2026: fresh `git clone` of the public repository into an
empty directory, plus the one documented manual step (downloading the OWID
CSV into `data/raw/` per `data/README.md`), then, in the pinned environment
(Python 3.12, pandas 2.2.2, numpy 1.26.4, scikit-learn 1.5.1, xgboost 3.3.0):

1. `python src/build_features.py`: rebuilt `data/processed/modeling_table.csv`
   from raw; all built-in verification checks passed (Qatar answer key, 200
   random target/lag re-derivations, duplicates, split bounds).
2. `python src/train.py`: refit every model on the frozen configurations and
   rewrote `results/model_comparison.csv`.
3. The regenerated table was compared to the committed table with
   `pandas.testing.assert_frame_equal` (relative tolerance 1e-12): identical.

## Check questions

**1. What single command reproduces `results/model_comparison.csv`?**

`python src/train.py`, in the pinned environment, with the raw OWID CSV
present in `data/raw/` (the one manual, documented step, since raw data is
deliberately not committed). The script rebuilds the modeling table if it is
missing, running `build_features.py`'s verification checks that refuse to
save on any failure, then refits the frozen configurations and rewrites all
three results files. No notebook state is involved; this is why the Session 3
notebook-state bug (`table.insert` failing on a rerun) can never contaminate
the reported table.

**2. Which README claim would violate the honesty boundary, and how is it
rephrased?**

Any of these would violate it: "the model forecasts national emissions for
policy planning" (claims a causal, decision-grade forecast; the project is
statistical extrapolation of historical public data); "XGBoost significantly
outperforms all baselines" (the country-clustered 95 percent interval on its
skill includes zero, so "significantly" is false); or an unscoped "the model
beats persistence" (true only for the giant-emitter tier; every ML model
loses to persistence below 10 Mt). The compliant phrasings the README
actually carries: "statistical extrapolation ... not a causal model, a policy
forecast, or an energy-system scenario"; "beat persistence by about 15
percent on test MAE, but a country-clustered bootstrap ... cannot rule out
that the gap is sampling noise"; and "adds value for the largest emitters
only." The affiliation rule also applies: always "Qatar Transportation and
Traffic Safety Center (QTTSC), Qatar University," never any internal lab
name.

## Publication-side actions this session

- README: status set to complete; "Reproduce the result" section added with
  the exact commands and the documented OWID download URL (matching
  `data/README.md`).
- Repository metadata set for portfolio use: description ("One-year-ahead
  country CO2 forecasting with an evaluation designed to be un-foolable ...")
  and topics (machine-learning, forecasting, xgboost, co2-emissions,
  sustainability, time-series, reproducible-research, data-science).
- Final LinkedIn post text prepared in the gitignored `linkedin_drafts/`
  folder (Version B framing per the pre-registered drafts: positive point
  skill, interval includes zero), for Khawar to review and publish himself;
  after publishing, save the final text per the `posted/` convention.
