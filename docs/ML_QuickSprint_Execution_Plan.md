# Emission-Trajectory Machine Learning Project
## Short-Sprint Execution Plan

**Dr. Khawar Naeem**  
Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University  
Prepared 6 July 2026

## 1. Decision and project position

This project temporarily moves ahead of the full SQL capstone. It will read the official Our World in Data (OWID) CO2 dataset directly with pandas. After the SQL Global Carbon Inventory is completed, an `extract.sql` stage can be added so the two projects demonstrate a connected SQL-to-ML workflow.

The required project is deliberately narrow: predict each country's annual production-based CO2 emissions one year ahead. The portfolio value comes from honest evaluation, time-aware validation, reproducibility, and error analysis, not from using the most complicated model.

Working repository name: `emission-trajectory-ml`

Core question:

> Using information available through year *t*, how accurately can we predict a country's production-based CO2 emissions in year *t + 1*, and does machine learning outperform simple historical baselines?

## 2. Definition of success

The core project is complete when all of the following are true:

1. The OWID dataset is loaded reproducibly from a documented source.
2. Country rows are separated from OWID aggregates.
3. Features use only information available at prediction time.
4. Training, validation, and test data are separated chronologically.
5. Persistence and linear-trend baselines are reported.
6. Ridge, a tree-based model, and XGBoost are compared on identical test data.
7. MAE and RMSE are reported overall and by selected countries.
8. The README explains at least one failure mode and avoids causal or policy-forecast claims.
9. A clean training script reproduces the final metrics.
10. The repository is public on GitHub.

The minimum defensible result is not “XGBoost wins.” It is a trustworthy comparison showing whether any model beats persistence and where it fails.

## 3. Scope

### Required core

- One-year-ahead regression target
- OWID country-year observations
- Lagged and rolling historical features
- Chronological validation
- Persistence baseline
- Linear-trend baseline
- Ridge regression
- `HistGradientBoostingRegressor` or random forest
- XGBoost
- MAE, RMSE, and country-level error analysis
- Reproducible scripts and public README

### Extension gates

Attempt these only after the core result is reproducible:

1. Five prediction horizons, *t + 1* through *t + 5*
2. Peaked, plateaued, or rising classification
3. Permutation importance or SHAP
4. Prediction intervals or empirical uncertainty bands
5. Streamlit application
6. SQL extraction from the future Global Carbon Inventory database

The classification task is not required for the first release. The deployed app is useful but must not delay a sound evaluation.

## 4. Data and analytical boundaries

Primary file: `data/raw/owid-co2-data.csv`

Codebook: `data/raw/owid-co2-codebook.csv`

Initial country filter:

- Keep rows with a three-letter ISO code.
- Exclude codes beginning with `OWID_`.
- Require at least 40 usable annual observations.
- Initially require population above 1 million in the prediction year.
- Record every exclusion rule in the README.

Initial target:

```text
target_co2_next_year = country CO2 value shifted backward by one year
```

The target represents annual territorial, production-based CO2 emissions. It is not a causal policy estimate, an energy-system scenario, or a complete greenhouse-gas forecast.

## 5. Initial feature set

Start with a small, explainable feature set:

- Current annual CO2
- CO2 lags of 1, 3, 5, and 10 years
- Five-year and ten-year rolling CO2 means
- Five-year CO2 slope or growth rate
- Population and population growth
- GDP per capita and recent GDP-per-capita growth, where coverage permits
- CO2 per capita
- Coal, oil, gas, cement, and flaring CO2 or their shares
- Share of global CO2

Every rolling statistic must be calculated within country and must not use observations after year *t*. A safe pattern is to shift before rolling whenever the current year's value should be excluded.

Do not add dozens of weak variables during the first pass. Add a feature only when its timing, meaning, and missing-data behavior are understood.

## 6. Validation design

Use chronological splits:

```text
Training:   all usable years through 2014
Validation: 2015–2018
Test:       2019 onward
```

If the latest OWID release changes the available endpoint, retain these boundaries for comparability unless the test set becomes too short.

Rules:

- Never randomly split country-year rows for forecasting.
- Fit imputers and scalers on training data only.
- Tune models using training and validation data only.
- Evaluate the final selected configuration once on the test period.
- Keep 2020 in the test set and discuss the COVID-era structural break.
- Compare all models on exactly the same eligible rows.

Primary metrics:

- MAE, for interpretable average absolute error
- RMSE, to expose large misses

Supporting diagnostics:

- Error by prediction year
- Error by country
- Error as a percentage of observed emissions, with caution near zero
- Performance for major emitters versus smaller economies

## 7. Model ladder

Run models in this order:

1. **Persistence:** next year equals the current year.
2. **Linear trend:** extrapolate each country's recent historical trend.
3. **Ridge regression:** regularized linear benchmark.
4. **Histogram gradient boosting or random forest:** nonlinear tabular benchmark.
5. **XGBoost:** industry-standard boosted-tree comparison.

Keep XGBoost tuning deliberately small:

- `max_depth`
- `n_estimators`
- `learning_rate`
- optionally `subsample` and `colsample_bytree`

Do not run a large hyperparameter search. The project question is whether the model generalizes through time, not whether hundreds of configurations can optimize one validation window.

## 8. Seven-session sprint

Each session should take approximately three to four focused hours and end with one committed artifact.

### Session 1: repository, data, and framing

- Create the repository structure.
- Confirm the dataset and codebook load.
- Inspect columns, year range, entity counts, and missingness.
- Write the problem statement and prediction timing.
- Separate countries from aggregates.

Artifact: `notebooks/01_framing_eda.ipynb`

### Session 2: modeling table

- Freeze the initial country eligibility rules.
- Create the next-year target within each country.
- Create lagged and rolling features.
- Verify several countries manually, including Qatar.
- Save a compact processed table locally, not the full raw CSV in Git.

Artifact: `src/build_features.py`

### Session 3: baselines

- Implement persistence.
- Implement a recent linear-trend baseline.
- Calculate validation MAE and RMSE.
- Create the first `results/model_comparison.csv`.

Artifact: baseline results table and `notebooks/02_baselines.ipynb`

### Session 4: linear and tree benchmarks

- Build a preprocessing pipeline fitted on training years only.
- Fit Ridge regression.
- Fit histogram gradient boosting or random forest.
- Compare both against the same baseline rows.

Artifact: updated model-comparison table.

### Session 5: XGBoost

- Install and fit `XGBRegressor`.
- Tune only a few defensible parameters on the validation years.
- Freeze the selected configuration.
- Evaluate once on the test years.

Artifact: `src/train.py` and final test metrics.

### Session 6: error analysis and interpretation

- Analyze errors by country and year.
- Examine Qatar, Saudi Arabia, major emitters, and structural breaks.
- Compare 2020 errors with other years.
- Use permutation importance first; use SHAP only if time remains.
- Write four evidence-based findings and at least two limitations.

Artifact: `notebooks/03_error_analysis.ipynb` and `insights/INSIGHTS.md`.

### Session 7: reproducibility and publication

- Re-run the pipeline from a clean environment.
- Finalize `requirements.txt`.
- Add a data-download script or documented download command.
- Write the README with findings and metrics first.
- Publish the GitHub repository.
- Add Streamlit only if the core reproduces without manual notebook state.

Artifact: public repository with a reproducible final commit.

## 9. Repository structure

```text
emission-trajectory-ml/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── README.md
│   └── raw/                    # downloaded locally, excluded from Git
├── notebooks/
│   ├── 01_framing_eda.ipynb
│   ├── 02_baselines.ipynb
│   └── 03_error_analysis.ipynb
├── src/
│   ├── build_features.py
│   ├── train.py
│   └── evaluate.py
├── results/
│   └── model_comparison.csv
├── insights/
│   └── INSIGHTS.md
└── app/
    └── streamlit_app.py       # gated extension
```

The raw OWID CSV should not be committed. The repository should contain the source URL, retrieval date, codebook, and a reproducible download instruction.

## 10. Claims the project can support

If completed as specified, the project can support these claims:

- Built a country-year machine-learning pipeline using pandas and scikit-learn.
- Engineered lagged and rolling features without using future information.
- Evaluated forecasting models with chronological holdouts.
- Benchmarked XGBoost against persistence and linear alternatives.
- Conducted country- and year-level error analysis.
- Published a reproducible sustainability analytics project.

It should not claim that the model predicts policy outcomes, captures causal effects, or provides decision-grade national emission scenarios.

## 11. Focused free learning resources

Use resources only when the corresponding implementation step begins.

### Forecast framing, lagged features, and leakage

- Scikit-learn lagged-feature forecasting example: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html
- Scikit-learn cross-validation guide: https://scikit-learn.org/stable/modules/cross_validation.html
- Kaggle Time Series course: https://www.kaggle.com/learn/time-series
- Kaggle Intermediate Machine Learning: https://www.kaggle.com/learn/intermediate-machine-learning

### Regression, trees, and boosting

- StatQuest video channel: https://www.youtube.com/@statquest
- StatQuest machine-learning index: https://statquest.org/video_index.html
- Scikit-learn histogram gradient boosting documentation: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html
- XGBoost installation guide: https://xgboost.readthedocs.io/en/stable/install.html
- XGBoost Python introduction: https://xgboost.readthedocs.io/en/stable/python/python_intro.html

### Evaluation and interpretation

- Scikit-learn model evaluation guide: https://scikit-learn.org/stable/modules/model_evaluation.html
- Scikit-learn permutation importance: https://scikit-learn.org/stable/modules/permutation_importance.html
- SHAP documentation, optional extension: https://shap.readthedocs.io/en/latest/

Recommended learning rule: no course binge. Watch or read one concept, implement it immediately, and record the result in the repository.

## 12. Working agreement with AI assistants

Codex may scaffold files, debug code, build reusable functions, run models, and verify reproducibility. Khawar owns the target definition, time split, feature timing, baseline choice, model-selection rationale, and interpretation. Claude may tutor concepts and review leakage, claims, and README prose.

At each modeling stage, ask:

1. Would this feature exist when the prediction is made?
2. Is this model evaluated on later years than it trained on?
3. Is the comparison against the same rows and target?
4. Does the result beat a simple baseline?
5. Can the reported metric be reproduced from a clean run?

## References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data

OWID CO2 dataset CSV: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv

OWID CO2 codebook CSV: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv

Our World in Data CO2 and greenhouse-gas emissions explorer: https://ourworldindata.org/co2-and-greenhouse-gas-emissions

Scikit-learn documentation: https://scikit-learn.org/stable/user_guide.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/

