# CLAUDE.md — Emission-Trajectory ML Project

> Master context for this project. It outranks conversation memory and older planning text. Read `AGENTS.md` first. Update the status and session log at the end of every working session. Last updated: 8 July 2026.

## Identity and purpose

Dr. Khawar Naeem is building a public sustainability data-science portfolio project using the official Our World in Data CO2 dataset. The immediate objective is a credible one-year-ahead country emissions forecast evaluated against simple baselines.

External affiliation must always be written as:

> Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University

## Current project state

| Item | Status |
|---|---|
| Short-sprint plan | Complete |
| Learning-depth plan (`ML_Learning_Plan_KhawarNaeem.md`) | Complete |
| Project context files | Complete |
| OWID dataset | Downloaded locally |
| OWID codebook | Downloaded locally |
| Repository scaffold | Partial |
| Session 1 framing and EDA | Complete 8 Jul; notebook run end to end, all 5 check questions answered (see `notebooks/01_framing_eda_check_questions.md`) |
| Modeling table | Not started |
| Baselines | Not started |
| Ridge/tree models | Not started |
| XGBoost | Not started |
| Error analysis | Not started |
| Public GitHub repository | Created 8 Jul: https://github.com/khawar89/energy-carbon-forecast-ml (Session 1 pushed) |

## Current next action

Session 1 is complete. Next:

1. Decide the 2024 test-year question left open in the frozen problem statement (2024 may be a partially final OWID release year) before Session 2 starts.
2. Session 2: build the modeling table in `src/build_features.py` (target shift, lags, rolls, eligibility filter, now including `cement_co2` and `flaring_co2` in wave 1), verifying Qatar by hand against the values in `notebooks/01_framing_eda_check_questions.md`.
3. Public GitHub repository created and Session 1 pushed: https://github.com/khawar89/energy-carbon-forecast-ml. Push again at the end of each future session.
4. Add a visualization/story layer (distributions, outliers, scale concentration, persistence check) as its own notebook or folder, planned for the end of the project, to support the public portfolio version.

Do not train XGBoost until Session 5.

## Authoritative decisions

- One-year-ahead regression is the required first release.
- The model predicts territorial, production-based annual CO2.
- CSV-to-pandas is the current ingestion path.
- SQL integration is deferred until the SQL capstone resumes.
- Training ends in 2014; validation is 2015–2018; test begins in 2019.
- Persistence is the minimum benchmark.
- XGBoost is a comparison model, not the project goal.
- Evaluation honesty is the main differentiator.
- Five-year forecasting, classification, SHAP, and deployment are extensions.
- Every comparison table includes a persistence skill score: `skill = 1 - MAE_model / MAE_persistence` (8 Jul).
- Models may predict the year-over-year delta internally; all models are scored on the reconstructed level, on identical rows (8 Jul).
- Error reporting is scale-aware: overall MAE/RMSE plus median errors, percentage errors, and emitter-size tiers (8 Jul).
- First-wave features use near-complete columns (co2 lags/rolls, population, co2_per_capita, share_global_co2, cement_co2, flaring_co2); fuel-mix (coal, gas) and GDP/consumption_co2 features are a second wave with explicit missing-data handling (8 Jul; cement/flaring added to wave 1 same day after confirming 4.8%/8.1% missing, see `data/README.md`).

## File map

- `AGENTS.md`: behavioral and verification rules for coding agents.
- `CLAUDE.md`: authoritative state, decisions, and restart log.
- `ML_QuickSprint_Execution_Plan.md`: active seven-session plan (scope, gates, verification).
- `ML_Learning_Plan_KhawarNaeem.md`: learning-depth layer; plan amendments, per-session concepts and check questions, gradient-boosting learning path. Wins on schedule and teaching.
- `notebooks/01_framing_eda.ipynb`: Session 1 teaching notebook (drafted 8 Jul).
- `MLProject_Guide_KhawarNaeem.md`: earlier broad ten-day plan, retained for history.
- `.gitignore`: excludes raw data, model artifacts, caches, and local environments.
- `data/README.md`: data provenance and download locations.
- `data/raw/`: locally downloaded OWID CSV and codebook.
- `notebooks/`: exploration, baselines, and error analysis.
- `src/`: reusable feature, training, and evaluation code.
- `results/`: saved metric tables and reproducible outputs.

## Project story for employers

The intended story is:

> I built a country-year emissions forecasting pipeline, engineered time-aware features, prevented future leakage, compared boosted trees with persistence and linear baselines, and reported where the model failed.

Do not frame the result as a decision-grade national forecast. It is a statistical extrapolation portfolio project using historical public data.

## Working division

Codex handles engineering, debugging, execution, tests, and reproducibility. Claude supports first-principles teaching, leakage review, analytical framing, and prose review. Khawar makes and understands the modeling decisions.

Teaching mode (agreed 8 Jul 2026): the assistant implements and explains; Khawar's obligation is understanding, verified through the check questions in `ML_Learning_Plan_KhawarNaeem.md`. A session is not complete until its check questions are answered. Cadence: 2 hours minimum per day, 3-4 when possible; one sprint session may span two days.

## Writing rules

- US English.
- Plain, direct, cautious claims.
- No em dashes.
- Use “suggests” or “indicates” when interpretation is uncertain.
- Do not claim causal effects.
- Tie every quantitative README claim to a saved result.
- End polished project documents with a References section containing full URLs.

## Decisions log

| Date | Decision | Rationale |
|---|---|---|
| 6 Jul 2026 | Move temporarily from SQL to ML | Build visible data-science evidence while retaining SQL for later expansion. |
| 6 Jul 2026 | Read OWID CSV directly | Avoid making the unfinished SQL capstone a blocker. |
| 6 Jul 2026 | Start with one-year forecasting | Narrow enough to finish and evaluate honestly. |
| 6 Jul 2026 | Gate classification and deployment | Core reproducibility must ship before optional scope. |
| 8 Jul 2026 | Add persistence skill score to all comparisons | Median year-over-year change is ~4.4% of level (2010+), so persistence is strong; raw MAE alone can flatter a losing model. |
| 8 Jul 2026 | Allow delta parameterization, score on level | Predicting the change forces the model to learn what moves emissions; level scoring keeps all models comparable. |
| 8 Jul 2026 | Scale-aware error reporting | Top-5 emitters are ~62% of 2023 global CO2; overall MAE alone is dominated by giants. |
| 8 Jul 2026 | Two-wave feature strategy | coal_co2 ~38%, gas_co2 ~44%, gdp ~29%, consumption_co2 ~47% missing in post-1990 country rows. |
| 8 Jul 2026 | Teaching mode: assistant implements, Khawar must pass check questions | Maximize learning depth at his 2-4 hr/day cadence. |

## Session log

### 6 July 2026, setup

- Created the short-sprint execution plan.
- Downloaded the official OWID dataset and codebook.
- Verified approximately 50,411 data records and 79 codebook variables.
- Added project-level Codex and Claude context.
- Next: Session 1 framing and EDA.

### 8 July 2026, plan review and Session 1 start (with Claude)

- Confirmed SQL runway complete and capstone paused; ML project is active.
- Inspected the downloaded data: 50,411 rows, 79 columns, 1750-2024, 218 ISO-coded countries, 36 aggregates; co2 coverage through 2024 for 215 countries; 202 countries have >= 40 years of co2 data.
- Key findings recorded: persistence strength (median |YoY| ~4.4% of level since 2010), scale concentration (top-5 = ~62% of 2023 total), missingness map for candidate features.
- Wrote `ML_Learning_Plan_KhawarNaeem.md` (four plan amendments, per-session learning layer, check questions, gradient-boosting path).
- Drafted `notebooks/01_framing_eda.ipynb` as a teaching notebook; cells not yet executed by Khawar.
- Next exact action: Khawar runs the Session 1 notebook end to end and answers its five check questions.

### 8 July 2026, Session 1 walkthrough (with Claude)

- Khawar running the Session 1 notebook cell by cell with Claude explaining pandas syntax and concepts as each cell executes.
- Confirmed the country/aggregate filter (cell 6) produces 218 countries and 36 aggregates as expected. Noted three of the 36 excluded entities are real places, not statistical aggregates: Kosovo (no ISO code, disputed recognition), Ryukyu Islands (historical/administrative, pre-1972), Kuwaiti Oil Fires (1991 Gulf War event record, not a country). Documented in `data/README.md` under a new "Entity filtering and exclusions" section; flagged for the eventual project README's data-limitations section too.
- Also found and documented: Monaco, San Marino, Vatican have an ISO code but zero non-missing `co2` values (microstates, no reliable OWID estimate); Antarctica and Christmas Island pass the country filter with near-zero `co2` despite not being real nations (removed downstream by the population > 1M eligibility rule). All in `data/README.md`.
- Decided `cement_co2` and `flaring_co2` (4.8%/8.1% missing 1990+) join wave 1 of the two-wave feature strategy, handled by row-drop rather than imputation. Recorded in `data/README.md` and the authoritative decisions list above.
- Confirmed by Khawar's own run: top-5 emitters (China, US, India, Russia, Japan) = 62% of 2023 global co2; median |YoY change| since 2010 = 4.40% of level, matching the 8 Jul figures exactly.
- Verified Qatar's 2015-2024 co2 rose every year 2020-2024 (101.3 to 125.8 Mt); this table is the manual answer key for Session 2's target-shift check.
- All five check questions answered; recorded with corrections in `notebooks/01_framing_eda_check_questions.md`. Two answers (double counting; persistence rationale) were correct unaided. Three (leakage vs. overfitting; why chronological split specifically prevents leakage; `World` as an OWID-constructed aggregate vs. row count) needed a concept explained before landing.
- Session 1 marked complete in the status table.
- Agreed with Khawar: this project will ship as a public GitHub repository, built up section by section (each session's work pushed as it completes), with an added data-visualization layer (distributions, outliers, scale concentration, persistence check) planned for the end of the project. Repository name and creation still pending Khawar's confirmation.
- Next exact action: decide the 2024 test-year question, choose and create the public repo, then start Session 2 (`src/build_features.py`).

## References

OWID CO2 data repository: https://github.com/owid/co2-data

Scikit-learn lagged-feature example: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/

