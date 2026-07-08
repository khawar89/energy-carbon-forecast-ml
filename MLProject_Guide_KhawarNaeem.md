# Emission-Trajectory ML Model: Project 2 Guidebook

**Dr. Khawar Naeem** | Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University
Prepared 2 July 2026. Execution guide for Sprint Project 2 (weeks 4-5, roughly 27 July to 9 August 2026, 2-4 hrs/day). It assumes Project 1 shipped, because this project deliberately reuses its MySQL database. Links verified July 2026; re-verify before reuse.

---

## 1. What this project is and why it works

You build a model that answers two connected questions from the same OWID data you already know: which countries have structurally peaked in emissions, and what does a defensible 5-year forecast of national CO2 look like. The portfolio point is not model sophistication; it is **evaluation honesty**. Most portfolio ML projects fail the credibility test because they leak future information or never compare against a naive baseline. Yours will lead with baselines, time-based validation, and error analysis. That is the same rigor-as-differentiator theme that runs through your whole path.

Two deliverables: a public GitHub repository, and a small deployed app (Streamlit Community Cloud or Hugging Face Spaces) where a user picks a country and sees history, peak status, and the 5-year projection with uncertainty caveats.

Success definition: repo public, app live, README leads with findings, and every reported metric is against a time-based holdout with a naive baseline beside it.

---

## 2. Framing (decide once, Day 1, do not reopen)

**Task A, classification:** label each country as peaked (maximum annual CO2 more than 10 years ago and current level at least 15 percent below peak), plateaued, or rising. Simple rule-based labels from the data itself; the model then predicts the label from structural features (GDP per capita, fuel mix shares, growth rates). This yields interpretable feature-importance stories.

**Task B, forecasting:** predict CO2 for horizon t+1 to t+5 per country using lagged features. Train on data through 2014, validate 2015-2018, test 2019 onward. Report MAE and RMSE per horizon, always next to two baselines: naive persistence (next year equals this year) and linear extrapolation of the last 10 years.

Scope discipline: no deep learning, no exotic time-series packages. scikit-learn plus XGBoost (or LightGBM) is enough and is what the job market checks.

---

## 3. Repository structure

```
emission-trajectory-ml/
├── README.md
├── data/                     # extraction queries, not raw dumps
│   └── extract.sql
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_baselines.ipynb
│   └── 03_models.ipynb
├── src/
│   ├── features.py
│   ├── train.py
│   └── predict.py
├── models/                   # saved model artifacts (joblib)
├── app/
│   └── streamlit_app.py
├── insights/
│   └── INSIGHTS.md
└── requirements.txt
```

The `data/extract.sql` file pulls the modeling table from the Project 1 MySQL database. That one file quietly proves SQL-to-ML pipeline competence.

---

## 4. Feature set (engineer in SQL where possible)

Per country-year: CO2 lags 1, 3, 5, 10; rolling 5-year and 10-year mean and slope; per-capita CO2; GDP per capita and its 5-year growth; fuel mix shares (coal, oil, gas); share of global emissions; years since peak so far; population growth. Target: CO2 at horizons +1 to +5.

Leakage rules, written into the README: features for year t use only data through year t; scalers and imputers fit on training years only; country never appears in both train and test for the classification task (group split).

---

## 5. Day-by-day plan (10 working days)

**Days 1-2, frame and extract.** Write `extract.sql` against carbon_inventory; build the pandas modeling frame via SQLAlchemy; EDA notebook: missingness by decade, which countries have usable series (rule: at least 40 years of data, population over 1 million); freeze the country list. Commit.

**Days 3-4, baselines first.** Implement persistence and linear-trend baselines for Task B and a majority-class baseline for Task A. Produce the baseline metrics table. This table is the yardstick everything else must beat; put it in the README early. Commit.

**Days 5-6, models.** Task A: logistic regression, then random forest, then XGBoost; report accuracy, macro F1, confusion matrix; SHAP or permutation importance for the story. Task B: Ridge, then XGBoost with lag features, one model per horizon; time-series split validation. Keep a single `results.csv` accumulating every run. Commit.

**Day 7, error analysis.** Where does the model fail: oil states (Qatar, Saudi Arabia) with volatile series, small economies, post-Soviet structural breaks, COVID-era 2020 dips. Write these up honestly in INSIGHTS.md; a paragraph on why 2020 breaks naive models reads as senior judgment. Commit.

**Day 8, deploy.** Streamlit app: country selector, history chart, peak-status badge, 5-year projection with the baseline shown alongside, and a visible caveat box (production-based accounting, no policy information in features). Deploy to Streamlit Community Cloud (free, GitHub-linked) or Hugging Face Spaces. Commit.

**Day 9, README and insights.** Same README discipline as Project 1: findings first, then method, then limitations. State plainly that this is a statistical extrapolation, not an energy-system model, and name what a real forecast would add (policy variables, energy capacity pipelines). Commit.

**Day 10, buffer and announcement.** Fix the worst rough edge only; draft the LinkedIn post (hook: "I asked a simple question: which countries have actually peaked?"). Commit.

Cut lines if behind, in order: SHAP analysis, then Task B horizons +4/+5, then app polish. Never cut: baselines table, time-based split, deployed app in some form, README limitations.

---

## 6. How to use Claude Code on this project

Same division of labor as Project 1: you own the modeling decisions and the evaluation design; Claude owns scaffolding and review. Delegate freely: environment setup, requirements.txt, Streamlit boilerplate, plotting code, docstrings, deployment debugging. Do yourself, then ask for critique only: feature list (ask "what leakage risks do you see"), the validation split design, the metrics table, the README claims. Two high-value prompts: "act as an ML reviewer and list every way this notebook could be leaking future information," and on the final day, "read this README as a skeptical hiring manager; list the three weakest claims."

---

## 7. Learning resources (targeted, not a curriculum)

Use these to fill gaps as they appear, not as prerequisite courses. Kaggle Intermediate ML and the Kaggle Time Series course cover lag features and leakage in a few hours. The scikit-learn user guide sections on cross-validation (TimeSeriesSplit) and pipelines are the reference. StatQuest videos for any concept that feels shaky (gradient boosting, regularization). XGBoost and LightGBM official docs for parameters; do not tune more than max_depth, n_estimators, learning_rate. Chip Huyen's writing for how practitioners think about evaluation.

---

## 8. Definition of done

Public repo; `extract.sql` runs against the Project 1 database; baselines table present; all metrics from time-based holdouts; app deployed and linked from the README; INSIGHTS.md has at least 4 findings including one honest failure mode; at least one commit per working day.

---

## References

OWID CO2 dataset: https://github.com/owid/co2-data
scikit-learn user guide: https://scikit-learn.org/stable/user_guide.html
scikit-learn TimeSeriesSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
Kaggle Intermediate Machine Learning: https://www.kaggle.com/learn/intermediate-machine-learning
Kaggle Time Series course: https://www.kaggle.com/learn/time-series
XGBoost documentation: https://xgboost.readthedocs.io/en/stable/
LightGBM documentation: https://lightgbm.readthedocs.io/en/stable/
SHAP documentation: https://shap.readthedocs.io/en/latest/
Streamlit documentation: https://docs.streamlit.io
Streamlit Community Cloud: https://streamlit.io/cloud
Hugging Face Spaces: https://huggingface.co/spaces
StatQuest (Josh Starmer) YouTube: https://www.youtube.com/@statquest
Chip Huyen blog: https://huyenchip.com/blog/
Claude Code documentation: https://code.claude.com/docs
