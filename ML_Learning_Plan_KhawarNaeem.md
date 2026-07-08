# Emission-Trajectory ML Project: Learning-Depth Plan

**Dr. Khawar Naeem**
Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University
Prepared 8 July 2026. Companion to `ML_QuickSprint_Execution_Plan.md`; where the two conflict on schedule or teaching, this file wins. The quick-sprint plan remains authoritative for scope, gates, and verification.

## 1. Purpose and working mode

The quick-sprint plan defines what to build. This file defines how Khawar learns while it is built. Agreed mode (8 July 2026): the AI assistant implements and explains; Khawar's job is to understand the logic, the data structures, and why each step is the efficient way to solve the problem, deeply enough to explain every decision in an interview without notes. Each session therefore has three parts: a concept briefing before code, a walkthrough of the code that was written, and check questions Khawar must answer before the session is logged as complete. If he cannot answer a check question, that concept is re-taught before moving on.

Cadence amendment: sessions run at a 2-hour minimum, extending to 3-4 hours when energy permits. Each of the seven sprint sessions may therefore span one or two calendar days. The end-of-session protocol in `AGENTS.md` still applies at the end of every working day.

## 2. Review of the quick-sprint plan

Verdict: the plan is sound. Chronological validation, mandatory persistence baseline, leakage rules, gated extensions, and small XGBoost tuning are exactly right. Four amendments follow from an 8 July inspection of the downloaded data (50,411 rows, 79 columns, years 1750-2024, 218 ISO-coded countries, 36 aggregate entities).

**Amendment 1: report skill against persistence, not just raw error.** The median absolute year-over-year change in country CO2 since 2010 is about 4.4 percent of the level. Persistence is therefore a strong opponent and small-looking model errors can still be worse than doing nothing. Add a skill column to every comparison table: `skill = 1 - MAE_model / MAE_persistence`, computed on identical rows. A model with negative skill loses to persistence and must be reported as losing.

**Amendment 2: models may predict the change, evaluation stays on the level.** Because next-year emissions are close to this-year emissions, predicting the raw level lets a model look accurate by simply reproducing the input. Predicting the delta (`co2[t+1] - co2[t]`) forces the model to learn what actually moves emissions. Either parameterization is allowed; predictions are always converted back to the level before scoring, so all models remain comparable on the same MAE and RMSE. This does not change the locked task definition.

**Amendment 3: scale-aware error reporting.** The top five emitters (China, United States, India, Russia, Japan) account for roughly 62 percent of 2023 global CO2; 2023 country levels span 0 to about 12,172 Mt. A single overall MAE is dominated by giants. Report, in addition: median absolute error, median absolute percentage error (excluding near-zero emitters), and error tables split by emitter size tier. Discuss, but do not silently apply, log transformation.

**Amendment 4: plan for feature missingness before modeling.** In post-1990 country rows: coal_co2 is missing in about 38 percent, gas_co2 44 percent, gdp 29 percent, consumption_co2 47 percent; core co2 and population are nearly complete. Consequence: the first modeling table should lean on the near-complete columns (co2, its lags and rolls, population, co2_per_capita, share_global_co2) and treat fuel-mix and GDP features as a second wave with explicit missing-data handling fitted on training years only.

## 3. Session-by-session learning layer

Each entry lists the concepts to master, why the approach is efficient, and the check questions to pass. Resources are single links from the quick-sprint plan, consumed only when that session starts.

### Session 1: framing and EDA (active, started 8 July 2026)

Concepts: panel (country-year) data structure; why entity filtering matters (OWID aggregates would double-count the world); target timing (`t` features, `t+1` target); why random row splits are invalid for forecasting.
Why efficient: pandas groupby-per-country operations express per-country logic in one vectorized pass instead of a loop over 218 countries.
Check questions: (1) Why must Asia and European Union rows be excluded? (2) If a feature for year t used `co2_growth_prct` of year t+1, what error is that, and how would it inflate results? (3) Why is 2015-2018 validation rather than a random 20 percent?

### Session 2: modeling table

Concepts: `shift` and `rolling` within `groupby` (shift-before-roll when the current year must be excluded); leakage across country boundaries; wide-versus-long table thinking carried over from SQL joins.
Why efficient: building one flat modeling table once, then reusing it for every model, beats recomputing features inside each model script; it is the ML analogue of a SQL staging table.
Check questions: (1) Write the pandas expression for a 5-year rolling mean of co2 that uses only years up to and including t. (2) What happens at each country's first rows when lag features are created, and what do we do with those rows? (3) Verify Qatar's 2023 target equals its 2024 co2 value.

### Session 3: baselines

Concepts: persistence and linear-trend as falsifiable null models; MAE versus RMSE (RMSE punishes large misses quadratically); the skill score from Amendment 1.
Why efficient: baselines cost minutes and define the bar every later model must clear; skipping them is the most common portfolio credibility failure.
Check questions: (1) For Qatar 2019-2024, is persistence biased up or down, and why (hint: Qatar grew every year)? (2) When do MAE and RMSE rank two models differently? (3) What does skill of -0.05 mean in words?

### Session 4: Ridge and tree benchmark

Concepts: regularization (why Ridge over OLS with correlated lag features); pipelines and fit-on-train-only preprocessing; decision trees, then ensembles: bagging (random forest) versus boosting (sequential error-correction); why tree models need no feature scaling.
Why efficient: `HistGradientBoostingRegressor` bins features into histograms, cutting split-search cost, and handles missing values natively, which matters given Amendment 4.
Check questions: (1) Why does scaling change Ridge but not tree predictions? (2) In one sentence each, how do bagging and boosting reduce error differently? (3) Where exactly may the imputer see data from 2015-2018?

### Session 5: XGBoost

Concepts: gradient boosting as gradient descent in function space (each tree fits the negative gradient of the loss); XGBoost specifics: regularized objective, shrinkage (learning_rate), subsampling, early stopping against the validation years; why heavy tuning on one validation window is disguised overfitting.
Why efficient: XGBoost is the industry-standard tabular benchmark; showing it beaten or barely winning against persistence is itself a publishable-quality portfolio finding.
Check questions: (1) Why do n_estimators and learning_rate trade off? (2) What is the difference between validation-based early stopping and test-set peeking? (3) If XGBoost beats Ridge on validation but loses on test, what does that suggest?

### Session 6: error analysis

Concepts: error decomposition by country, year, and size tier (Amendment 3); the 2020 COVID structural break as an honest failure case; permutation importance and its correlated-feature caveat.
Why efficient: error analysis converts one number into findings an employer can read; it is the highest-value-per-hour part of the project.
Check questions: (1) Why is percentage error misleading for near-zero emitters? (2) Predict before looking: will 2020 errors be larger for persistence or for the trend baseline, and why? (3) Why can permutation importance understate a feature that is correlated with another?

### Session 7: reproducibility and publication

Concepts: clean-run discipline; requirements pinning; README claims tied to saved results; the difference between a statistical extrapolation and a policy forecast.
Check questions: (1) What single command reproduces `results/model_comparison.csv`? (2) Which README claim would violate the honesty boundary, and how is it rephrased?

## 4. Gradient-boosting learning path

Khawar already knows Python, linear regression, and basic neural networks. The bridge to XGBoost, in order, one concept per sitting, implemented immediately: decision-tree regression (split criteria, depth, overfitting), bootstrap aggregation and random forests, boosting as sequential residual fitting, gradient boosting as functional gradient descent, then XGBoost's additions (second-order approximation, regularization terms, histogram binning, subsampling). StatQuest's gradient boosting and XGBoost series maps one video to each of these steps; watch only the step currently being implemented.

## 5. References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data

Scikit-learn lagged-feature forecasting example: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html

Scikit-learn HistGradientBoostingRegressor: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/

StatQuest video index: https://statquest.org/video_index.html
