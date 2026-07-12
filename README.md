# energy-carbon-forecast-ml

One-year-ahead forecasting of country CO2 emissions from the official Our World in Data (OWID) dataset, benchmarked honestly against simple baselines.

**Status: in progress.** Session 1 (framing, EDA, problem statement) is complete. Feature engineering, baselines, and models land in the coming sessions. This README grows as results are produced; no metric is claimed here before it exists in `results/`.

## The question

Using information available through year *t*, how accurately can we predict a country's production-based CO2 emissions in year *t+1*, and does machine learning beat simple historical baselines?

The honest benchmark matters more than the model: country emissions change slowly (median absolute year-over-year change since 2010 is about 4.4 percent of the level), so persistence, predicting that next year equals this year, is a strong opponent. Every model here is reported with a skill score against persistence, computed on identical rows. A model that loses to persistence will be reported as losing.

## Scope

The current target is production-based annual CO2 (Mt) per country, one year ahead. Energy variables (primary energy consumption and related columns) are used as candidate features; forecasting energy as a second target is a planned extension, gated until the core CO2 result is reproducible. The name of the repository reflects the intended full arc, not the current deliverable.

This is a statistical extrapolation portfolio project using historical public data. It is not a causal model, a policy forecast, or an energy-system scenario.

## Data

Official OWID CO2 dataset: about 50,000 country-year rows, 79 columns, 1750-2024. The raw CSV is not committed; retrieval instructions and the codebook are in `data/`. Entity filtering (218 ISO-coded countries kept; aggregates such as World and Asia excluded, plus documented edge cases like Kosovo and the Kuwaiti Oil Fires record) is described in `data/README.md`.

## Method summary

- Chronological validation, never random row splits: train through 2014, validation 2015-2018, headline test 2019-2023. 2024 targets are reported separately as provisional, since the newest OWID release year is revisable.
- Features for predicting year *t+1* use data through year *t* only; all lags and rolling statistics are computed within country.
- Baselines: persistence and recent linear trend. Models: Ridge, histogram gradient boosting, XGBoost.
- Metrics: MAE, RMSE, persistence skill score, plus scale-aware breakdowns (the top five emitters account for roughly 62 percent of global CO2, so a single overall MAE would be dominated by giants).

## Findings so far (Session 1, EDA)

![Ranking reversal: top-10 total emitters versus top-10 per-capita emitters](results/figures/fig8_ranking_reversal.png)

Total and per-capita emissions produce almost disjoint top-10 lists; only Saudi Arabia and the United States appear on both. The same denominator choice will shape how model errors are judged across country sizes.

Full exploratory analysis: `notebooks/01_framing_eda.ipynb` and `notebooks/01b_visual_eda.ipynb`, with all figures in `results/figures/`.

## Repository notes

This project is built in a documented human-plus-AI workflow. The agent context files (`CLAUDE.md`, `AGENTS.md`, the execution and learning plans, and the recorded check questions) are committed deliberately as part of the method: they contain the locked modeling decisions, the leakage rules, and the session-by-session record of what was decided and why.

## Author

Dr. Khawar Naeem, Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University.

## References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data

OWID CO2 codebook: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv

Scikit-learn lagged-feature forecasting example: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/
