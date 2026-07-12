# AGENTS.md — Emission-Trajectory ML Project

> Tool-neutral instructions for Codex and other coding agents. This file outranks model recall about this project. Read it first, then `CLAUDE.md`, then `docs/ML_QuickSprint_Execution_Plan.md`. Last updated: 13 July 2026.

## Current objective

Build a reproducible public machine-learning project that predicts each country's production-based CO2 emissions one year ahead using the official OWID CO2 CSV.

The active sequence is:

```text
OWID CSV -> pandas modeling table -> chronological baselines -> Ridge/tree models -> XGBoost -> error analysis -> GitHub
```

The SQL Global Carbon Inventory is paused, not canceled. This ML project reads the CSV directly now. Add `extract.sql` only after the SQL capstone is completed.

## Required read order

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/ML_QuickSprint_Execution_Plan.md`, the authoritative execution plan for scope, gates, and verification
4. `docs/ML_Learning_Plan_KhawarNaeem.md`, the learning-depth layer; it wins on schedule, teaching mode, and the four 8 July amendments (skill score, delta parameterization, scale-aware metrics, two-wave features)
5. `data/README.md` when handling data
6. Only the notebook or source file required for the current session

`docs/MLProject_Guide_KhawarNaeem.md` is the earlier, broader plan. Where it conflicts with the quick-sprint plan, the quick-sprint plan wins.

## Folder layout and naming conventions

- Root: `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore` only. Planning documents live in `docs/`.
- `notebooks/`: numbered by pipeline stage, one stage per notebook, letters for supplements: `01_framing_eda`, `01b_visual_eda`, `02_build_features_walkthrough`; reserved next: `03_baselines`, `04_models_ridge_tree`, `05_xgboost`, `06_error_analysis`. Each session's check-question record sits beside its notebook as `NN_..._check_questions.md`.
- `src/`: reusable pipeline code (`build_features.py`, later `train.py`, `evaluate.py`).
- `results/`: saved metrics and `figures/`. `assets/`: static images (flags). `data/`: README plus `raw/` (gitignored CSV) and `processed/` (gitignored outputs).
- `reports/`: personal session reports, gitignored, local only.
- `learning_notes/` and `linkedin_drafts/`: gitignored, local only. The first holds the project mental model (read it early in a new session); the second holds post angles and the standing rules for public posts. Neither may ever be committed or quoted verbatim in public files.

## Locked decisions

- Required task: one-year-ahead country-level CO2 regression.
- Raw source: official OWID `owid-co2-data.csv` plus its codebook.
- Data access: pandas reads the CSV directly during this phase.
- Validation: chronological, never a random row split.
- Initial periods: training through 2014, validation 2015–2018, test 2019 onward.
- Required baselines: persistence and recent linear trend.
- Model ladder: Ridge, histogram gradient boosting or random forest, then XGBoost.
- Primary metrics: MAE and RMSE, plus a persistence skill score (`1 - MAE_model / MAE_persistence`) in every comparison table (8 Jul).
- Models may predict the year-over-year delta internally, but all models are scored on the reconstructed level, on identical rows (8 Jul).
- Error reporting is scale-aware: median errors, percentage errors, and emitter-size tiers beside overall MAE/RMSE (8 Jul).
- Required interpretation: errors by country and prediction year, including the 2020 disruption.
- Raw data stays out of Git. Publish source URLs and reproducible retrieval instructions.

## Extension gates

Do not start these until the one-year model reproduces from a clean run:

- horizons two through five;
- peaked/plateaued/rising classification;
- SHAP;
- uncertainty intervals;
- Streamlit deployment;
- SQL extraction.

## Coding rules

- Khawar owns the target, split, feature timing, baseline choice, model-selection rationale, and interpretation.
- Codex may scaffold, implement, debug, test, and refactor when asked.
- Teaching mode (8 Jul): whenever an agent implements a step, it must also explain the logic, the data structures used, and why the approach is efficient. A session closes only after Khawar answers that session's check questions in `docs/ML_Learning_Plan_KhawarNaeem.md`.
- Before writing model code, state the target year, feature year, and split boundaries.
- Group all lags and rolling calculations by country.
- Prevent leakage. No feature for year `t` may use data after `t`.
- Compute growth/percentage-change features with `pct_change(fill_method=None)`; never let a real data gap forward-fill into a fabricated growth rate (13 Jul 2026 finding: pandas' own default for this parameter has changed across versions, so state it explicitly rather than depend on whichever default a given installed pandas version ships).
- Fit preprocessing only on training years.
- Compare models on the same eligible rows.
- Set random seeds where applicable.
- Save metrics to a results file. Do not rely only on notebook output.
- Prefer small, readable functions over a long notebook-only pipeline.
- Do not tune XGBoost extensively. Generalization through time matters more than validation-window optimization.

## Figure rules

- Khawar is a data scientist and treats framing as part of the analysis: the same data can support opposite stories depending on the denominator (China leads totals; Qatar leads per capita). Figures should surface a framing insight where one exists, not only describe the data.
- Every figure's markdown cell states one modeling consequence.
- Save every figure to `results/figures/` as a PNG; README claims must cite saved figures, not notebook-only output.
- Label counterfactuals as illustrations. Never present them as scenarios or projections.
- The public repo is https://github.com/khawar89/energy-carbon-forecast-ml; work ships session by session, so figures must render correctly in executed notebooks on GitHub.
- National flag assets for highlight annotations live in `assets/flags/` (flagcdn PNGs).

## Verification gates

Before accepting a result, verify:

1. Country-year sorting is correct.
2. Targets and lags do not cross country boundaries.
3. Aggregates and `OWID_` entities are excluded from the country model.
4. Training-only preprocessing is enforced.
5. All models use the same evaluation rows.
6. Persistence metrics are beside ML metrics.
7. A clean run reproduces the reported table.
8. README claims match saved results.

## Local reports

`reports/` is gitignored and stays out of the public repo: it holds Khawar's personal session reports (Book Antiqua docx/pdf learning records), not portfolio content. The approved Session 1 report plan is in `CLAUDE.md` under "Approved plan: Session 1 report"; if a build is interrupted, resume from that plan.

## Data safety

- `data/raw/owid-co2-data.csv` is downloaded locally and ignored by Git.
- The codebook may be retained locally; publish a source link even if it is committed later.
- Do not mix the private QTTSC emission-factor practice data into this project.
- Do not describe statistical extrapolation as a causal, policy, or energy-system forecast.

## End-of-session protocol

At the end of each working session:

1. Save one visible artifact.
2. Run the relevant checks.
3. Update the status and session log in `CLAUDE.md`.
4. Commit and push when a project repository exists.
5. Record the exact next action, not a broad intention.

## References

OWID CO2 data repository: https://github.com/owid/co2-data

Scikit-learn user guide: https://scikit-learn.org/stable/user_guide.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/

