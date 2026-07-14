# CLAUDE.md — Emission-Trajectory ML Project

> Master context for this project. It outranks conversation memory and older planning text. Read `AGENTS.md` first. Update the status and session log at the end of every working session. Last updated: 13 July 2026.

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
| Modeling table | Built and verified 10 Jul (`src/build_features.py`); Session 2 CLOSED 13 Jul, five check questions answered (`notebooks/02_build_features_walkthrough_check_questions.md`) |
| Baselines | Session 3 CLOSED 13 Jul: executed end to end, `results/model_comparison.csv` saved (persistence MAE 6.757, linear_trend MAE 7.281, skill -0.078), three check questions answered (`notebooks/03_baselines_check_questions.md`) |
| Ridge/tree models | Session 4 CLOSED 13 Jul: `notebooks/04_models_ridge_tree.ipynb` executed; Ridge alphas frozen at 0.1/0.1; `results/model_comparison.csv` now has six validation rows; persistence remains best MAE, hgb_delta closest ML model |
| XGBoost | Session 5 CLOSED 14 Jul: validation grid run, configs frozen (xgb_level d6/lr0.10/125 trees; xgb_delta d3/lr0.10/173 trees), single test evaluation run, results frozen; `results/model_comparison.csv` has 8 val + 8 test rows; xgb_delta best test MAE 9.345 (skill +0.151, CI includes zero); check questions in `notebooks/05_xgboost_check_questions.md` |
| Error analysis | Session 6 CLOSED 14 Jul: by-year/by-country/by-tier decomposition executed; skill is giant-tier only (xgb_delta +0.325 there, -0.863 small tier); reversal SURVIVES on test (cleared for figures/post); figs 9-11 + four CSVs saved; check questions in `notebooks/06_error_analysis_check_questions.md` |
| Public GitHub repository | Created 8 Jul: https://github.com/khawar89/energy-carbon-forecast-ml (Session 1 pushed) |
| Math foundations doc | Extended 14 Jul (`math/main.pdf`, commit 6ab13da): 6 sections, 10 pages, 28 numbered equations, 10 verified references; now includes the full XGBoost second-order derivation (leaf weight, split gain, gamma pruning, early-stopping refit rule) and the level/delta parameterization, both verified against executed xgboost 3.3.0 |

## Current next action (handoff state, updated 14 Jul 2026)

**Sessions 5 AND 6 CLOSED 14 Jul.** Results are FROZEN (AGENTS.md "Post-test freeze"). Next exact action: **Session 7, reproducibility and publication pass**: (1) clean-clone dry run: fresh clone, pinned env, `python src/build_features.py` then `python src/train.py` must reproduce `results/model_comparison.csv` exactly; (2) README final pass against the verification gates (every claim traces to a saved artifact); (3) repo hygiene for portfolio use (description, topics, pinned repo); (4) the LinkedIn post from `linkedin_drafts/Session5_PreRegistered_Drafts_WinsAndLoses.md` (Version B framing: positive point skill, interval includes zero; the Session 6 tier/reversal findings may fold in, figures are cleared) plus the Session 6 angle if posted separately; (5) then the deferred future-sessions planning (extensions per gates, `docs/Research_Publication_Roadmap.md` timing, RAG flagship handoff).

Historical handoff state from 13 Jul (Sessions 1-4) follows.

## Previous handoff state (13 Jul 2026, historical)

Where things stand: Session 1 complete and pushed. **Session 2 CLOSED 13 Jul** — worked cell by cell with Claude (real code executed live against the actual raw CSV and `data/processed/modeling_table.csv`, since Jupyter is not installed in the shell used for teaching; every notebook claim verified against genuine output, not toy claims), all five check questions answered and recorded in `notebooks/02_build_features_walkthrough_check_questions.md`. **Session 3 CLOSED 13 Jul** — pre-registration written and committed before any cell ran (2 of 3 predictions correct, 1 close), notebook executed cell by cell (Khawar also ran it independently in his own local Jupyter/Anaconda environment and confirmed matching output throughout, including hitting and resolving a genuine notebook-state error on a rerun of the save cell), `results/model_comparison.csv` saved, reconcile-and-interpret plus all three check questions answered (with Claude's full guidance, at Khawar's request) and recorded in `notebooks/03_baselines_check_questions.md`. **Session 4 CLOSED 13 Jul** — pre-registration written before model execution, Ridge level and Ridge delta alphas both frozen at 0.1, notebook executed in Khawar's VS Code/Jupyter environment, `results/model_comparison.csv` saved with six validation rows, reconciliation and all four check questions recorded in `notebooks/04_models_ridge_tree_check_questions.md`. Result: persistence remains best on validation MAE (6.757); the best ML row is hgb_delta (MAE 6.874, skill -0.017), close but still worse than persistence; hgb_level fails badly on MAE/RMSE, likely from large-emitter threshold errors. A live finding from Session 3 (the MAE-vs-percentage-error ranking reversal: Russia/Pakistan/Vietnam) is carried forward to Session 6, not used yet — see the 13 Jul decisions-log entry below. `src/evaluate.py` is finished and self-tested; `requirements.txt` is now pinned to the Anaconda environment that reproduces Session 4 tree metrics (`pandas==2.2.2`, `numpy==1.26.4`, `scikit-learn==1.5.1`, `matplotlib==3.9.2`; XGBoost still to be installed/used in Session 5). Environment note: Khawar's Anaconda Python 3.12 / scikit-learn 1.5.1 reproduces the saved Session 4 table exactly; this machine's system Python 3.13 / scikit-learn 1.9.0 reproduces baselines and Ridge exactly but gives different HistGradientBoosting rows, so use the pinned environment for clean reproduction.

Khawar's queue, in strict order (do not skip ahead of him):

1. ~~Session 2 study~~ DONE 13 Jul.
2. ~~Execute `notebooks/03_baselines.ipynb`~~ DONE 13 Jul.
3. ~~Execute `notebooks/04_models_ridge_tree.ipynb`~~ DONE 13 Jul.
4. ~~Run Session 5~~ DONE 14 Jul (closed; see the 14 Jul session log entry).

Standing agent behavior: teaching mode per AGENTS.md (implement AND explain; sessions close on check answers). Never reveal the withheld Session 3/4 numeric results before Khawar executes the notebooks with his pre-registrations written. Commit and push at the end of each session. Read `learning_notes/BigPicture_MentalModel_KhawarNaeem.md` early for the project's reasoning and named traps.

## Approved spec: Session 5 scaffold (build only after Sessions 3-4 results exist)

Deliberately NOT pre-built: its choices must react to the Sessions 3-4 validation table. When Khawar has committed Session 4 results, build `notebooks/05_xgboost.ipynb` plus `src/train.py` to this spec:

- Same table, same features, same referee (`evaluate.comparison_table`), same rows as all prior models.
- `XGBRegressor`, both parameterizations (level and delta) unless Session 4 showed one clearly dominant; small defensible grid only (max_depth, n_estimators, learning_rate, optionally subsample/colsample_bytree), selected on validation, with early stopping against validation years. Seeds set. No wide search.
- Freeze the chosen configuration in writing (a Khawar decision, like the alpha freezes), then run the SINGLE test evaluation: all six-plus models scored once on test targets 2019-2023, same-rows rule. The 2024 provisional appendix is a separate labeled table.
- `src/train.py` = the clean-run script reproducing the final metrics end to end (build features if missing, fit frozen configs, write `results/model_comparison.csv` with val and test rows).
- Pre-registration: Khawar ranks all models on test BEFORE the test run; per `linkedin_drafts/`, both the "wins" and "loses" post drafts are written before seeing test results.
- After the test run, results are frozen: no going back to tune anything on any split. Session 6 interprets; it does not re-fit.

## Forward track: research-publication roadmap (separate from the sprint; starts after Session 7)

Full detail, every claim search-verified: `docs/Research_Publication_Roadmap.md` (built 13 Jul 2026). Summary: three staged ideas -
(1) a near-free metric-reversal note (the MAE-vs-percentage-error reversal already found in Session 3, formalized against Hyndman & Koehler 2006);
(2) a methodology-audit paper (benchmark published 2024-2025 ML CO2-forecasting claims against this project's own honest persistence-skill standard - search confirmed most don't report one);
(3) an MRIO/SPA bridge paper (couple the ML forecast with structural-path-analysis for forward-looking CBAM trade-exposure risk, Qatar/LNG focal case - the biggest lift, the long-horizon target).
Preprint policy corrected via search: Elsevier and Nature Portfolio both explicitly allow preprints without penalty; plan uses preprints for ideas 1-2, direct submission for the flagship idea 3. Venue targets (hybrid, no forced fee, verified numbers): MethodsX for idea 1. For idea 3, framing decides the venue - this project is ENVIRONMENTAL first, so the environmental journals lead: **Resources, Conservation and Recycling** (best scope match for the MRIO/footprint methodology, IF ~13.7, hybrid), Ecological Economics, or Environmental Science & Policy (fast, ~15-day review); Applied Energy / Sustainable Production and Consumption apply only under a genuinely energy-systems framing; Global Environmental Change only under a political-economy reframing. Energy and Climate Change flagged as possibly gold-OA (forced fee) - confirm before targeting. This track does not start until Session 7 closes; do not let it compete with the sprint cadence.

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
- 2024 targets are excluded from the headline test set (test = predicting 2019-2023) because the newest OWID release year is provisional and subject to revision; 2024 predictions are reported separately in a clearly labeled provisional appendix table. Features from 2023 and earlier are settled, so only the target side is affected (8 Jul).
- Energy columns (`primary_energy_consumption`, `energy_per_capita`, `co2_per_unit_energy`; 7-8% missing 1990+) are feature candidates for the CO2 model; `energy_per_gdp` goes to wave 2. Predicting energy as a second target is a gated extension after the one-year CO2 model ships, not current scope (8 Jul).

## File map

- `AGENTS.md`: behavioral and verification rules for coding agents.
- `CLAUDE.md`: authoritative state, decisions, and restart log.
- `docs/ML_QuickSprint_Execution_Plan.md`: active seven-session plan (scope, gates, verification).
- `docs/ML_Learning_Plan_KhawarNaeem.md`: learning-depth layer; plan amendments, per-session concepts and check questions, gradient-boosting learning path. Wins on schedule and teaching.
- `docs/MLProject_Guide_KhawarNaeem.md`: earlier broad ten-day plan, retained for history.
- `docs/Research_Publication_Roadmap.md`: separate track (starts after Session 7), planning how to extend this project into a publishable research paper - three staged ideas, verified venue targeting, corrected preprint-policy notes. Built 13 Jul 2026.
- `notebooks/01_framing_eda.ipynb`: Session 1 teaching notebook (run and completed 8 Jul).
- `notebooks/01_framing_eda_check_questions.md`: Session 1 check-question answers with corrections.
- `notebooks/01b_visual_eda.ipynb`: Session 1b visual EDA; six executed figures saved to `results/figures/` (skew, concentration, persistence, missingness waves, energy-CO2 coupling, Qatar anchor).
- `notebooks/02_build_features_walkthrough.ipynb`: Session 2 classroom for the feature pipeline.
- `notebooks/02_build_features_walkthrough_check_questions.md`: Session 2 check-question answers with corrections (closed 13 Jul).
- `notebooks/03_baselines.ipynb`: Session 3 baselines notebook (executed 13 Jul); `notebooks/03_baselines_check_questions.md`: its check-question and reconcile answers (closed 13 Jul).
- `src/build_features.py`: builds and verifies `data/processed/modeling_table.csv` (10 Jul).
- `.gitignore`: excludes raw data, processed outputs, model artifacts, caches, reports, and local environments.
- `data/README.md`: data provenance, download locations, and entity exclusions.
- `data/raw/`: locally downloaded OWID CSV and codebook. `data/processed/`: pipeline outputs, gitignored.
- Naming conventions for `notebooks/` and folders: see AGENTS.md "Folder layout and naming conventions" (reserved next: 03 baselines, 04 Ridge/tree, 05 XGBoost, 06 error analysis).
- `results/`: saved metric tables and figures. `reports/`: personal session reports, gitignored.
- `learning_notes/` (gitignored): `BigPicture_MentalModel_KhawarNaeem.md` is the project's mental model, named traps, and standing facts; ANY NEW AI SESSION should read it right after AGENTS.md and this file to absorb the reasoning, not just the file list. Also holds the pipeline map SVG.
- `linkedin_drafts/` (gitignored): per-session post angles, standing post rules, and the posted/ record. Read before drafting any public post about this project.
- `math/` (committed, tracked in git): standalone LaTeX document formalizing the project's mathematical foundations (evaluation metrics, baselines, Ridge regularization, ensembles/boosting, and uncertainty/significance of skill scores - section 6, added 13 Jul 2026), numbered equations, verified academic references in `references.bib`. Built 13 Jul 2026 in parallel with the coding sessions (not a substitute for them); grows one new `sections/0N_*.tex` file per relevant future session. Compile with `tectonic main.tex` (from inside `math/`) to produce `main.pdf`, which is committed so it renders on GitHub without a LaTeX install. See `AGENTS.md`'s folder-layout entry for the full convention.

## Project story for employers

The intended story is:

> I built a country-year emissions forecasting pipeline, engineered time-aware features, prevented future leakage, compared boosted trees with persistence and linear baselines, and reported where the model failed.

Do not frame the result as a decision-grade national forecast. It is a statistical extrapolation portfolio project using historical public data.

## Data storytelling (agreed 8 Jul 2026)

Khawar's stated professional identity for this project is data scientist, and he finds the framing layer of the work as compelling as the modeling: the same data supports opposite stories depending on how the question is posed (China leads totals; Qatar, where he lives and works, leads per capita at ~40 t/person). Figures should surface this kind of denominator-aware, question-framing insight, not just describe the data. Conventions: every figure states one modeling consequence in its markdown cell; figures are saved to `results/figures/` so README claims tie to saved artifacts; counterfactuals (e.g. "world at Qatar's rate would be ~9x current") are always labeled as illustrations, never scenarios. Public narrative anchor: he anchors sanity checks on the country he lives in, which happens to be the world's most carbon-intensive per person. LinkedIn profile for posts about this project: https://www.linkedin.com/in/khawar-naeem-203a6524/

## Working division

Codex handles engineering, debugging, execution, tests, and reproducibility. Claude supports first-principles teaching, leakage review, analytical framing, and prose review. Khawar makes and understands the modeling decisions.

Teaching mode (agreed 8 Jul 2026): the assistant implements and explains; Khawar's obligation is understanding, verified through the check questions in `ML_Learning_Plan_KhawarNaeem.md`. A session is not complete until its check questions are answered. Cadence: 2 hours minimum per day, 3-4 when possible; one sprint session may span two days.

## Writing rules

- US English.
- Plain, direct, cautious academic claims.
- No em dashes. Use commas, semicolons, or parentheses instead.
- Use human academic prose: varied sentence openings, concrete nouns, and logical paragraph flow. Avoid formulaic AI-sounding transitions and empty signposting.
- Avoid ornate or filler phrasing, including: delve into, it is worth noting, moreover, furthermore, in conclusion, plays a crucial role, comprehensive, holistic, paradigm shift, real-world impact, and unprecedented unless literature-verified.
- Structure academic paragraphs as one claim, then evidence, then cautious interpretation.
- Use "suggests," "indicates," "is consistent with," "points to," "reflects," "shows," or "appears to" when interpretation is uncertain.
- Do not claim causal effects.
- Tie every quantitative README claim to a saved result.
- Future methodology and manuscript sections should reuse `math/main.pdf` and the LaTeX source in `math/sections/` for equation forms, notation, and citation anchors rather than re-deriving formulas from memory.
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
| 8 Jul 2026 | 2024 targets out of headline test, reported in a provisional appendix | Newest OWID release year is provisional and revisable; scoring against it would tie README claims to numbers OWID may replace. Features (2023 and earlier) are settled, so a labeled side table is safe. |
| 13 Jul 2026 | Carry the MAE-vs-percentage-error reversal finding forward to Session 6, do not use it yet | Found live while teaching Session 3, on the persistence baseline's validation-year `error_by_country` table: Russia has the lowest percentage error (1.33%) despite a top-10 absolute-error miss, while Pakistan (11.05%) and Vietnam (8.22%) have far higher percentage errors despite smaller absolute misses - a ranking reversal parallel to figs 7-8 (totals vs per-capita), this time for model error. Numbers are validation-only; no figure or public post is built from them. Session 6 (error analysis) must re-run this same per-country MAE-vs-percentage breakdown on the final TEST-set predictions and confirm whether the reversal survives before it goes in any figure. Full detail in `linkedin_drafts/LinkedIn_Post_Points_BySession.md` (gitignored, local only). |
| 13 Jul 2026 | Pin the reproducibility environment after Session 4 | Session 4's baselines and Ridge rows reproduce across environments, but `HistGradientBoostingRegressor` rows differ between scikit-learn 1.5.1 and 1.9.0. `requirements.txt` is pinned to the Anaconda versions that reproduce the saved Session 4 table exactly. |
| 14 Jul 2026 | Freeze XGBoost configs as the validation-grid winners, as printed | Khawar's decision: xgb_level = max_depth 6, learning_rate 0.10, 125 trees (val MAE 8.528); xgb_delta = max_depth 3, learning_rate 0.10, 173 trees (val MAE 6.184). Taking the grid winners without second-guessing avoids hand-tuning past the frozen grid; the near-tie with d3/lr0.05 (6.194) was noted and rejected on that ground. |
| 14 Jul 2026 | Post-test freeze: results final, no retuning on any split | The single test evaluation ran 14 Jul after both pre-registrations and both LinkedIn drafts were written. Any post-test change to a model would make the test a second validation set. Session 6 interprets only. |
| 14 Jul 2026 | README headline carries the significance caveat, not just the point win | xgb_delta beat persistence on test (MAE 9.345 vs 11.004, skill +0.151) but the country-clustered 95% CI [-0.018, +0.271] includes zero (p=0.14), and persistence kept the best MedianAE/MdAPE. Claiming a clean ML win would overstate the evidence; the honest framing (point win, interval includes zero, typical country still favors persistence) is the project's thesis in action. |

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

### 8 July 2026, evening: repo shipped, 2024 decided, visual EDA added (with Claude)

- Public repository created and pushed: https://github.com/khawar89/energy-carbon-forecast-ml (name chosen by Khawar with Claude's casing cleanup; description: one-year-ahead country CO2 forecasting with honest baseline comparisons).
- 2024 test-year question decided (option 3): headline test = 2019-2023 targets; 2024 in a labeled provisional appendix. Frozen problem statement in the notebook updated to match.
- Khawar proposed adding visualization to Session 1 and expanding scope to energy prediction. Resolved: visual EDA built now (`notebooks/01b_visual_eda.ipynb`, six figures in `results/figures/`); energy columns adopted as feature candidates (7-8% missing); energy as a second prediction target deferred as a gated extension per the sprint cut rules.
- Next exact action: Session 2, `src/build_features.py` plus `notebooks/02_build_features_walkthrough.ipynb`.

### 10 July 2026, Session 2 prepared (with Claude)

- Built and verified `src/build_features.py`: one flat modeling table with target (`target_co2_next`, plus `target_delta`), wave-1 features (co2 lags 1/3/5/10, rolling means 5/10, 5-year slope, co2_per_capita, share_global_co2, population and 5-year growth, cement_co2, flaring_co2), nullable energy candidates (primary_energy_consumption, 1-year growth, energy_per_capita), and splits keyed on target year.
- Verified against the real data: 7,443 rows, 24 columns, 153 countries, feature years 1870-2023. Splits: train 5,917 / val 612 (exactly 4 per country) / test 762 / provisional_2024 152. Qatar 2023 row confirmed: target 125.812, split provisional_2024. Energy candidates ~24% missing in the final table.
- Built-in verification: Qatar answer key, 200 random targets and lags re-derived from the raw CSV, duplicate check, split bounds. Script refuses to save on any failure.
- Two implementation decisions recorded: population >= 1M measured at feature year t, not t+1 (t+1 population unknowable at prediction time; deviation from plan wording); `pct_change(fill_method=None)` so data gaps yield NaN instead of fabricated growth rates. Also: per-country calendar reindex before any shift, because shift is positional, not temporal.
- Wrote `notebooks/02_build_features_walkthrough.ipynb`: teaching notebook (shift target, positional-vs-temporal trap with toy gap demo, feature families, order of operations, split keying, exclusion accounting) plus five check questions.
- 65 of 218 countries excluded by eligibility rules; the walkthrough's section 6 produces the accounting for the README data-limitations section.
- Khawar's Session 2 work: run the walkthrough, run the script, read it top to bottom, answer the five check questions, commit and push.
- Next exact action after that: Session 3, baselines (`notebooks/02_baselines.ipynb` reading `data/processed/modeling_table.csv`), persistence and linear trend with the skill-score table.

### 10 July 2026, Session 3 scaffolded (with Claude)

- Built `src/evaluate.py`: shared metrics (MAE, RMSE, MedianAE, MdAPE with near-zero exclusion, persistence skill score), `comparison_table` enforcing the same-rows rule, `error_by_country`. Self-test on hand-checkable numbers passes (`python src/evaluate.py` prints OK). Every model in Sessions 3-6 must be scored through this module.
- Built `notebooks/03_baselines.ipynb` as an UNEXECUTED skeleton: pre-registration section (Khawar commits three predictions before running), persistence and trend cells, comparison table, per-country winner analysis, Qatar check, results/model_comparison.csv writer, reconciliation prompts, three check questions. All code paths smoke-tested against the real modeling table; numeric results deliberately withheld so they emerge first for Khawar.
- Session ordering agreed 10 Jul: Khawar studies Session 2 (walkthrough + check questions) tonight, THEN runs Session 3. Session 3 is not started until Session 2's check questions are answered.
- Next exact action: Khawar closes Session 2 (five check answers to Claude), then executes 03_baselines.ipynb top to bottom, filling the pre-registration first.

### 10 July 2026, Session 4 scaffolded (with Claude)

- Built `notebooks/04_models_ridge_tree.ipynb`, unexecuted skeleton: concepts block (Ridge vs OLS with correlated lags, scaling for linear vs tree models, bagging vs boosting, fit-on-train-only preprocessing), four pre-registration predictions, Ridge in level and delta parameterizations (small alpha grid chosen on validation, alpha cells left as `...` for Khawar to freeze), HistGradientBoostingRegressor in both parameterizations (modest fixed settings, no wide search), six-way comparison table via `evaluate.comparison_table` (2 baselines + 4 models, same-rows rule), full rewrite of `results/model_comparison.csv`, reconciliation prompts, four check questions.
- All six model paths smoke-tested against the real modeling table with sklearn 1.7; results withheld so they emerge for Khawar at run time.
- Added `requirements.txt` (pandas, numpy, scikit-learn, xgboost, matplotlib, jupyter).
- Feature set frozen for Session 4: 14 core + 3 nullable energy columns; `year` deliberately excluded (era memorization does not extrapolate).
- Boundary agreed: Session 5 (XGBoost) is NOT pre-built; its tuning choices must react to Sessions 3-4 validation results.
- Queue for Khawar, in order: (1) Session 2 study + five check answers, (2) execute 03_baselines with pre-registration, (3) execute 04_models_ridge_tree with pre-registration and alpha freezes. No new scaffolds until this queue clears.

### 8 July 2026, night: figures 7-8, LinkedIn post, session report (with Claude)

- Beautified figure 7 (flags, styled diagonals, insight box) and built figure 8, the ranking reversal: top-10 totals beside top-10 per capita, only Saudi Arabia and the US on both lists. Flags for 19 countries committed to `assets/flags/`.
- Khawar published the LinkedIn post with figure 8; Claude prepared answers to four anticipated challenges (fairness framing, cumulative, per-GDP, production-vs-consumption for Qatar's LNG), recorded in the session report section 8.
- Built the approved Session 1 report: `reports/Session1_Report_EmissionTrajectory_KhawarNaeem.docx` and `.pdf`, Book Antiqua, 10 sections, all 8 figures, emissions and energy feature tables, check-question record. Local only (gitignored).
- Session 1 fully closed. Next exact action: Session 2, `src/build_features.py` plus `notebooks/02_build_features_walkthrough.ipynb`, verifying Qatar by hand.

### 13 July 2026, Session 2 closed (with Claude)

- Worked `notebooks/02_build_features_walkthrough.ipynb` cell by cell with Claude, in a plain chat session rather than a live Jupyter kernel (Jupyter is not installed on this machine). Every notebook claim was verified with real, live-executed code against the actual raw CSV and `data/processed/modeling_table.csv`, including several checks not in the original notebook: a live rerun of `python3 src/build_features.py` reproducing the exact 10 Jul numbers; a from-scratch reproduction of pandas' old `pct_change(fill_method="pad")` forward-fill behavior (not observable via the installed pandas 3.0.2, whose own default has since changed to `fill_method=None`) to show the fabricated-growth-rate trap concretely; a live demo of the "filter before lagging" self-inflicted-gap bug (order-of-operations cell had no code cell in the original notebook); Qatar's actual 1949-1959 rows showing the `co2_lag10` early-row gap in isolation from unrelated missing-data years; and the real Qatar 2013-2023 split table used to identify the exact three boundary years (2014, 2018, 2023) affected by a feature-year-vs-target-year split mixup.
- Two documentation fixes made mid-session, both prompted by the `pct_change(fill_method=None)` discussion: added a standing coding rule to `AGENTS.md` (compute growth features with `fill_method=None` explicitly, since pandas' own default for this has drifted across versions) and a tenth named trap to `learning_notes/BigPicture_MentalModel_KhawarNaeem.md` ("fabricated growth across a gap"), since that document's stated purpose is to list every trap a new agent should internalize before coding, and this one was missing despite the underlying decision already being logged elsewhere. Both apply directly to the not-yet-built wave-2 growth features (coal_co2, gas_co2, gdp, consumption_co2).
- All five check questions answered and recorded in `notebooks/02_build_features_walkthrough_check_questions.md`. Two (Qatar's 2023 target/split; why features precede filtering) were correct and unaided. One (the 5-year rolling-mean expression) needed a specific correction: the original attempt included `shift(-1)`, which is the target's formula (pulls a future value backward), not this feature's; using it here would have reintroduced the exact future-leakage trap the project is built to prevent. Two (the early/final row-drop mechanics; the feature-year-vs-target-year split bias) needed the full mechanism explained rather than being attempted independently.
- Environment note recorded: `pandas`/`numpy` are installed on this machine and sufficient for Session 2; `scikit-learn`/`xgboost`/`jupyter` are not yet installed and will be needed before Session 3/4 can run.
- Session 2 marked CLOSED in the status table and handoff-state section.
- Next exact action: Khawar installs `scikit-learn`/`xgboost`/`jupyter` (`pip3 install -r requirements.txt`) if not already done, then executes `notebooks/03_baselines.ipynb`: fill the pre-registration section first, run, reconcile against `src/evaluate.py`'s comparison table, answer the three check questions, commit results.

### 13 July 2026, Session 3 closed (with Claude)

- Pre-registered three predictions in writing before running any cell: persistence wins overall MAE (correct), ~35% of countries favor trend (close - real answer 39.2%, 60/153), persistence wins for Qatar (correct). No prediction was wrong.
- Worked `notebooks/03_baselines.ipynb` cell by cell, reading `src/evaluate.py`'s actual source alongside it (the `comparison_table` same-rows rule, the `mae`/`rmse`/`median_ae`/`mdape`/`skill` functions, and the module's own self-test) rather than treating the referee as a black box. Khawar separately ran the same cells in his own local Jupyter/Anaconda environment and confirmed matching output at every step.
- Result: persistence MAE 6.757 beats linear_trend MAE 7.281 (skill -0.078) overall, but trend actually wins on MedianAE (1.103 vs 1.134) and MdAPE (3.991% vs 4.178%) - persistence's advantage is concentrated in avoiding disasters among the largest emitters, confirmed by RMSE (24.930 vs 33.251). Per-country: trend wins in 39.2% of countries (e.g. United States, Germany); persistence wins in the rest (e.g. Qatar, China).
- Found live and flagged, not used yet: the MAE-vs-percentage-error ranking reversal in the persistence baseline's `error_by_country` table - Russia has the lowest percentage error (1.33%) despite a top-10 absolute miss, while Pakistan (11.05%) and Vietnam (8.22%) have far higher percentage errors despite smaller absolute misses. Validation-only, so carried forward to Session 6 rather than posted or visualized now (see the decisions-log entry below and `AGENTS.md`'s Figure rules); full narrative in `linkedin_drafts/LinkedIn_Post_Points_BySession.md` (gitignored).
- Real notebook-state bug hit and resolved: rerunning the save cell a second time raised `ValueError: cannot insert split, already exists`, because `table.insert(...)` mutates in place and Jupyter keeps `table` alive between cell runs. Fixed by rerunning the cell that rebuilds `table` first - a live example of why `AGENTS.md`'s "a clean run reproduces the reported table" gate exists, not a staged teaching example.
- `results/model_comparison.csv` saved (persistence and linear_trend rows, `split="val"`, full precision). Reconcile-and-interpret section plus all three check questions answered, with Claude's full guidance at Khawar's request; recorded in `notebooks/03_baselines_check_questions.md`.
- Environment note: Khawar has a working local Jupyter/Anaconda install (confirmed live via a real traceback during this session), separate from this machine's system Python used for teaching.
- Session 3 marked CLOSED in the status table and handoff-state section.
- Next exact action: install `scikit-learn` if not already available in whichever environment runs Session 4, then execute `notebooks/04_models_ridge_tree.ipynb`: pre-registration first, freeze the two Ridge alpha choices himself, run, reconcile, answer the four check questions, commit.

### 13 July 2026, math/ foundations document built (with Claude)

A new, standalone deliverable, in parallel with (not a replacement for) the numbered notebook
sessions: `math/main.tex` + `math/sections/{00_notation,01_evaluation_metrics,02_baselines,
03_ridge_regularization,04_ensembles_boosting}.tex` + `math/references.bib`, compiled to
`math/main.pdf` (committed, tracked in git).

- Formalizes, with numbered equations, exactly what the pipeline has built or is imminently
  building: MAE/RMSE/MedianAE/MdAPE/skill score (matching `src/evaluate.py` exactly), the
  persistence and linear-trend baselines, OLS vs Ridge and why correlated lag/rolling features
  favor Ridge, and regression trees through bagging/random forests/gradient boosting/XGBoost
  (Session 5's XGBoost math flagged for a fuller derivation once that session is built).
- Every reference independently verified by live web search before being entered in
  `references.bib`, not recalled from memory: Hyndman & Koehler (2006, IJF, forecast-accuracy
  metrics), Hyndman & Athanasopoulos (2021, free OTexts textbook, naive/drift methods), Hoerl &
  Kennard (1970, Technometrics, ridge regression), Breiman (1996 bagging, 2001 random forests,
  both Machine Learning), Friedman (2001, Annals of Statistics, gradient boosting), Chen &
  Guestrin (2016, KDD, XGBoost, free arXiv:1603.02754 version).
- Toolchain: `tectonic` installed via Homebrew (lightweight, ~100-150MB, self-contained; no
  LaTeX was previously installed on this machine). Two pre-existing, unrelated stale Homebrew
  `opt` symlinks (`freetype`, `fontconfig` - real leftover directories instead of proper
  symlinks, blocking `brew link`) were found and fixed during the install; not caused by this
  session's work.
- Compiled and verified: 7 pages, table of contents matches all 5 sections, 15 equations number
  sequentially, all 7 in-text citations resolve correctly against the bibliography (no undefined
  references). Bibliography via classic BibTeX (`\bibliographystyle{plain}`), which `tectonic`
  handles automatically in one invocation (no separate `biber` install needed).
- Also installed `scikit-learn`/`xgboost`/`jupyter` into this machine's system Python 3.13 (via
  `pip3 install -r requirements.txt`), separately fixing an unrelated xgboost/macOS issue
  (`libomp` missing; fixed with `brew install libomp`). This is additive only; Khawar's existing
  working Anaconda Python 3.12 environment (used throughout Session 3) is untouched.
- `AGENTS.md`'s folder-layout section and this file's File map both updated to register `math/`.
  `.gitignore` updated for LaTeX build artifacts (`main.pdf` itself stays tracked).
- Next exact action for this track: add `sections/05_xgboost.tex` (full second-order/split-gain
  derivation) once Session 5 is built; add `sections/06_forecast_accuracy_theory.tex` when
  Session 6 revisits the carried-forward MAE-vs-percentage-error reversal finding on real test
  data (see the 13 Jul decisions-log entry above), citing Hyndman & Koehler directly.

### 13 July 2026, research-rigor audit + uncertainty tooling (with Claude, Opus 4.8)

A deep-read audit of the whole technical stack (`src/build_features.py`, `src/evaluate.py`, the scaffolded Session 4 notebook) to find the highest-value weak area for turning this into a publishable paper. Finding: the code is clean and correct - no bug fix needed - but every metric is a bare POINT ESTIMATE with no uncertainty or significance. For a project whose whole thesis is "an evaluation that cannot fool its author," the missing piece is whether a skill difference is statistically distinguishable from zero. Closed that gap, additively:

- **`src/evaluate.py` gains `cluster_bootstrap_skill`** (plus two behavior-preserving guards: zero-division in `skill`, empty-sample in `mdape`). It resamples whole COUNTRIES with replacement (a cluster bootstrap - the panel-data-correct choice, since a country's own years are correlated and a naive row bootstrap would understate the interval) and returns a CI + a two-sided bootstrap p-value on the persistence skill score. **Deliberately NOT wired into `comparison_table`** - it is optional infrastructure, so nothing in Sessions 3-5 changes, no committed result moves, and no withheld Session 4/5 number is revealed. Self-test extended and passes (`python3 src/evaluate.py` -> OK).
- **Demonstration on the already-committed Session 3 validation baselines** (not a spoiler; Session 3 is closed): linear-trend point skill -0.078 vs persistence, but the country-clustered 95% CI is [-0.335, +0.199] with bootstrap p ~= 0.69 - so trend and persistence are STATISTICALLY INDISTINGUISHABLE on validation, a conclusion the bare point estimate hides. This is exactly the nuance a journal reviewer would demand.
- **`math/` gains section 6 (Uncertainty)** formalizing the loss differential, the clustered-bootstrap CI, and the bootstrap p-value with numbered equations; three references added, each independently search-verified: Diebold & Mariano (1995, JBES), Efron & Tibshirani (1993, bootstrap), Cameron, Gelbach & Miller (2008, cluster bootstrap). PDF recompiled and verified (8 pages, all citations resolve).
- **Ownership boundary kept explicit** (per AGENTS.md): the tool is added, but WHICH significance test to adopt and HOW to interpret it remain Khawar's modeling decisions, to be settled when the research-paper track (idea 2) is actually developed. Recorded in `docs/Research_Publication_Roadmap.md` under idea 2.
- No modeling decision was made for Khawar, no notebook was executed, and `results/model_comparison.csv` was not touched.

### 13 July 2026, Session 4 closed (with Codex)

- Worked through the Session 4 Ridge/tree notebook in teaching mode. Before running model-result cells, Khawar wrote a pre-registration: Ridge level expected close to persistence and maybe slightly better; Ridge delta uncertain; boosting expected to possibly beat Ridge; full ranking explicitly uncertain.
- Executed `notebooks/04_models_ridge_tree.ipynb` in Khawar's VS Code/Jupyter environment. Ridge level alpha candidates gave validation MAE 7.292, 7.530, 8.575, 9.946 for alpha 0.1, 1.0, 10.0, 100.0; Khawar froze `RIDGE_LEVEL_ALPHA = 0.1`. Ridge delta alpha candidates gave validation MAE 7.267, 7.318, 7.453, 7.385; Khawar froze `RIDGE_DELTA_ALPHA = 0.1`.
- Saved `results/model_comparison.csv` with six validation rows. Ranking by MAE: persistence 6.757; hgb_delta 6.874; ridge_delta 7.267; linear_trend 7.281; ridge_level 7.292; hgb_level 18.856. All ML rows have negative persistence skill; hgb_delta is closest at -0.017.
- Interpretation recorded in the notebook: persistence remains the best validation benchmark; delta parameterization helped both Ridge and HGB; hgb_level likely made large-emitter threshold errors, as indicated by RMSE 142.706; linear_trend still has the best MedianAE and MdAPE, reinforcing that typical-country and large-emitter metrics tell different stories.
- All four Session 4 check questions answered and recorded in `notebooks/04_models_ridge_tree_check_questions.md`. The key learning points were: Ridge needs scaling because the coefficient penalty depends on units; trees split by order/thresholds and do not need scaling; HGB is boosting, not bagging; the Ridge imputer is fitted only on training rows; level Ridge behaves partly like persistence, while delta Ridge must learn movement.
- Verification: `/opt/anaconda3/bin/python` (Python 3.12, pandas 2.2.2, numpy 1.26.4, scikit-learn 1.5.1, matplotlib 3.9.2) reproduces the saved Session 4 table exactly within tolerance. System Python 3.13 / scikit-learn 1.9.0 reproduces baselines and Ridge exactly but gives different HGB rows, so `requirements.txt` was pinned to the Anaconda versions for reproducibility. `python3 src/evaluate.py` self-test passes.
- Session 4 marked CLOSED. Next exact action: build Session 5, `notebooks/05_xgboost.ipynb` plus `src/train.py`, using the approved spec: small validation tuning, pre-registration before the single test-set evaluation, then freeze results with no post-test retuning.

### 14 July 2026, Session 5 closed (with Claude, Fable 5)

- Opened by extending `math/` first (Khawar's request, committed separately as `6ab13da` before any model ran): full XGBoost second-order derivation (gradient/Hessian, Taylor expansion, per-leaf decomposition, closed-form leaf weight, split gain with gamma pruning, squared-error specialization showing the n/(n+lambda) leaf shrinkage, shrinkage/subsampling, early-stopping-then-fixed-count refit rule) plus the previously unformalized level/delta parameterization (now eq. 6). Leaf-weight and split-gain formulas verified against executed xgboost 3.3.0, not recalled algebra; noted xgboost reports gain without the constant 1/2. Doc now 10 pages, 28 equations, zero undefined references.
- Khawar wrote the validation pre-registration himself before any model cell: (1) XGBoost will not beat persistence (wrong, instructively); (2) delta over level (correct, right mechanism); (3) honestly unsure on depth/learning-rate/early-stopping.
- Frozen validation grid run (8 fits, early stopping vs val): delta grid swept the level grid; best xgb_delta val MAE 6.184 vs persistence 6.757, the project's first positive validation skill (+0.085). Khawar reproduced the grid independently in his own environment, output identical to six decimals. He froze both grid winners as printed: xgb_level d6/lr0.10/125 trees, xgb_delta d3/lr0.10/173 trees; transcribed into `src/train.py`.
- Test pre-registration and both LinkedIn drafts (`linkedin_drafts/Session5_PreRegistered_Drafts_WinsAndLoses.md`) written BEFORE the unlock; test pre-registration prepared with Claude's full guidance at Khawar's request and marked as such (validation pre-registration is his own).
- Single test evaluation (targets 2019-2023, 762 rows, same-rows rule): FIVE models beat persistence on point MAE; persistence fell to sixth (MAE 11.004, worst-of-top-six RMSE 43.971, its errors concentrated in the 2020/2021 disruption). xgb_delta best: MAE 9.345, skill +0.151. Significance layer (country-clustered bootstrap, run once): every positive skill's 95% CI includes zero (xgb_delta [-0.018, +0.271], p=0.143); the only distinguishable result is xgb_level LOSING (skill -1.834, p=0.005). Persistence kept the best MedianAE (1.367) and MdAPE (5.055): the typical country still favors no-change; ML gains concentrate in large, volatile rows (Session 6's thread). Provisional 2024 appendix: persistence best again (calm-year regime flips back).
- `src/train.py` clean run reproduces the notebook test table exactly and wrote `results/model_comparison.csv` (8 val + 8 test rows), `results/test_predictions.csv` (for Session 6), `results/provisional_2024.csv`. `evaluate.py` self-test OK. Notebook committed EXECUTED, with outputs.
- Reconcile + check questions recorded in `notebooks/05_xgboost_check_questions.md` (Claude-guided at Khawar's request, marked). README updated with the headline table and the significance-caveated framing. AGENTS.md gains the post-test freeze section. `learning_notes/SESSION5_CODEX_HANDOFF.md` deleted and both pointers removed per its own instruction.
- Next exact action: Session 6, error analysis (`notebooks/06_error_analysis.ipynb` from `results/test_predictions.csv`): errors by country/year/size tier, the 2020 break, and the test-set re-verification of the Session 3 MAE-vs-percentage reversal before any figure uses it. Then Session 7 (reproducibility/publication), math/ error-analysis section, and the LinkedIn post (Version B framing).

### 14 July 2026, Session 6 closed (with Claude, Fable 5)

- Built `notebooks/06_error_analysis.ipynb` (19 cells) reading `results/test_predictions.csv`; smoke-tested with output suppressed, pre-registration (Claude-guided at Khawar's request, marked) recorded before execution. Interpretation only; the sole fit was reproducing the frozen xgb_delta config unchanged for permutation importance.
- By year: 2020 is every model's worst year (persistence MAE 13.95); xgb_delta holds positive skill in ALL five test years (+0.051 to +0.301) but earns most in calm 2019/2022, so the ML advantage reads post-shock and steady-state structure rather than anticipating disruptions. Trend's only losing year is 2021 (-0.043), the pre-registered mirror miss (slope window contaminated by the collapse into the rebound); the 2020 half of that prediction missed (trend slightly BEAT persistence in 2020, 13.135 vs 13.950, because enough large emitters had flat/declining pre-2020 slopes).
- By country: the Session 3 MAE-vs-percentage reversal SURVIVES on test with the same lead actors: Russia lowest percentage error (2.14%) in persistence's top-10 absolute list, China 3.19% on the largest absolute miss (365 Mt), Vietnam 11.26% opposite signature, Pakistan 13.20% in xgb_delta's list. Cleared for figures and the public post per the 13 Jul gate; `fig10_reversal_test.png` is the cleared figure.
- By tier: the headline +0.151 skill is giant-tier only (xgb_delta +0.325 on the 25 rows >= 1000 Mt; ridge_delta quietly best there at +0.329); ~zero in large/mid; every ML model loses to persistence in the small tier (xgb_delta -0.863). Level trees' giant-tier MAE 508/773 vs persistence 169 is the saturation failure made visible. Deployment claim must be tier-scoped.
- Permutation importance (frozen xgb_delta): co2_slope5 first (2.889), population second; the co2 level family individually low (roll5 0.098) from redundancy, read as group structure per the correlated-features caveat.
- Artifacts: figs 9-11 (each with a modeling-consequence cell; fig9 annotation bug found and fixed before commit), four CSVs in `results/`, notebook committed executed with outputs. Khawar's own run of fig9 matched exactly.
- `math/` gains section 7 (error decomposition: within-group MAE/skill, scale dependence per Hyndman-Koehler, permutation importance with the correlated-features caveat); 11 pages, 31 equations, no undefined references, no new bib entries needed.
- README gains the "Where the skill lives" section, every bullet tied to a saved CSV or figure. Check questions recorded in `notebooks/06_error_analysis_check_questions.md` (Claude-guided, marked).
- Next exact action: Session 7 (see handoff-state section above).

## Skills born in this project

Reusable skills live in `1_CV-khawar/0_Skills_Library_/` per the standing convention (never create or update skills inside projects). Born here so far, both in `4_Communication/`: `session-report-builder` (from the Session 1 report build) and `data-storytelling-figures` (from figures 1-8). A `panel-data-leakage-review` skill is planned after Session 2 exercises the AGENTS.md checklist for real. When this project teaches one of these skills something new, update the library copy, re-zip into `_installable/`, and log it in the library registry.

## Approved plan: Session 1 report (approved by Khawar 8 Jul 2026, evening; BUILT same evening)

STATUS: COMPLETE. Both `reports/Session1_Report_EmissionTrajectory_KhawarNaeem.docx` and `.pdf` built 8 Jul (PDF exported via Word automation). All 8 figures embedded, all 10 sections present. Local only, gitignored.

Deliverable: `reports/Session1_Report_EmissionTrajectory_KhawarNaeem.docx` (+ .pdf if a converter is available). LOCAL ONLY: `reports/` is gitignored; this is a personal learning record, not portfolio content. Book Antiqua 11pt, justified, US English, no em-dashes, References section with full URLs.

Ten sections: (1) project overview with repo link and honest-scope statement; (2) data foundation (OWID provenance, 50,411 rows, 79 cols, 1750-2024, what `co2` measures); (3) entity filtering and all exclusions (Kosovo, Ryukyu, Kuwaiti Oil Fires, Monaco/San Marino/Vatican, Antarctica, Christmas Island); (4) emissions analysis findings with figures (skew 172 vs 10.5, top-5 62%, persistence 4.40%, Qatar anchor table 2015-2024); (5) emissions feature columns table with % missing and wave assignment; (6) energy section (five columns, missingness, 1965+ coverage, coupling finding, feature-candidates-now / target-later decision); (7) frozen problem statement including the 2024 provisional-year decision; (8) framing insight (figs 7-8, denominator reversal, mapping to percentage and size-tier errors, four anticipated challenges including production-vs-consumption for Qatar); (9) the five check questions with Khawar's original answers, corrections, and final answers; (10) decisions log and Session 2 next steps, then References. All 8 figures embedded with captions stating modeling consequences.

Build: python-docx script; PDF via LibreOffice if installed, otherwise deliver docx and flag manual export. If a session is interrupted mid-build, resume from this plan; source content lives in this file's session log, `notebooks/01_framing_eda_check_questions.md`, `data/README.md`, and `results/figures/`.

## References

OWID CO2 data repository: https://github.com/owid/co2-data

Scikit-learn lagged-feature example: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html

XGBoost documentation: https://xgboost.readthedocs.io/en/stable/
