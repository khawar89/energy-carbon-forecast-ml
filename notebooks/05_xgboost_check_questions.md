# Session 5 check questions and reconciliation record

Recorded 14 July 2026. The reconcile-and-interpret answers and the three check
answers below were prepared with Claude's full guidance at Khawar's request
(same attribution convention as the Session 3 record). The validation-phase
pre-registration in the notebook is Khawar's own, written before any model
cell ran; the test pre-registration was Claude-guided and is marked as such
in the notebook.

## Pre-registration scoring

Validation phase (Khawar's own, 3 questions): question 1 (XGBoost will not
beat persistence) was wrong; xgb_delta reached validation MAE 6.184 against
persistence's 6.757, skill +0.085, the first positive validation skill in the
project. Question 2 (delta over level) was correct, for the correct
structural reason: every delta configuration beat every level configuration.
Question 3 was recorded as honestly unsure and is resolved by check question 1
below and the grid itself (deep delta trees were cut off by early stopping at
35-43 trees; shallow ones earned 173-261).

Test phase (Claude-guided, 4 questions): the ranking prediction placed
persistence first and that was the largest miss; persistence fell to sixth of
eight. What the prediction misunderstood: a disrupted window (2020 collapse,
2021 rebound) is hostile to persistence most of all, since large year-over-year
changes are exactly what "predict no change" cannot see; persistence's test
RMSE (43.97, worst of the top six) shows its error budget concentrated in the
disruption. The no-distinguishable-positive-skill prediction was correct: all
five positive point skills have country-clustered 95 percent intervals that
include zero. Delta over level was correct. The 2020 attribution (level trees
worst overall) held; the trend baseline did far better than predicted (second,
skill +0.114), consistent with many countries being on sustained declines
across 2019-2023.

## Reconcile and interpret (notebook section 9)

1. Biggest miss: expecting persistence to stay first on test. It assumed the
   test window was hostile to tuned models, when it is most hostile to the
   no-change forecast itself.
2. Honest headline: "XGBoost predicting year-over-year changes beat
   persistence by 15 percent on test MAE (9.345 vs 11.004, skill +0.151), but
   the country-clustered bootstrap interval [-0.018, +0.271] cannot rule out
   sampling noise; no model achieved statistically distinguishable positive
   skill." Persistence also kept the best MedianAE (1.367) and MdAPE (5.06):
   for the typical country, no-change remained the best forecast; the ML
   gains live in the large, volatile rows. The only statistically
   distinguishable test result is xgb_level being WORSE than persistence
   (skill -1.834, p = 0.005).
3. Validation rankings partially survived: xgb_delta stayed best among ML
   models and level trees stayed last, but persistence dropped from second to
   sixth and linear_trend rose from fifth to second. Single-window rankings
   are fragile; this is why the interval sits beside every point estimate.
4. 2020: to be decomposed properly in Session 6 (per-year error tables from
   results/test_predictions.csv). The aggregate signature is already visible
   in persistence's outsized RMSE. A disruption no feature built from
   pre-2019 history could anticipate is an expected limit of extrapolation,
   not a bug; the provisional-2024 appendix (persistence best again, MAE
   4.96) shows the calm-year regime flipping back.

## Check questions

**1. Why do `n_estimators` and `learning_rate` trade off?**

The ensemble prediction is a running sum of tree corrections, each scaled by
the learning rate, so total correction is approximately learning_rate times
n_estimators; halving the rate needs roughly double the trees to reach the
same fit. Observed directly in the Session 5 grids: depth-3 level needed 535
trees at rate 0.05 versus 149 at rate 0.10; depth-3 delta needed 261 versus
173. Small steps generalize better because each tree corrects only the broad,
repeatable error before residuals are re-examined, at the price of compute.

**2. Difference between validation-based early stopping and test-set peeking?**

Both read held-out data; the difference is the data's assigned job. Validation
exists to make selection choices, and early stopping is a tree-count selection
made on validation, so validation scores are optimistic by construction. The
test set's only job is to measure the frozen model once; letting test numbers
influence any choice turns it into a second validation set and leaves no
honest data. Hence the Session 5 protocol: freeze hyperparameters and tree
counts from validation, refit on train plus validation with the count fixed
and early stopping disabled (information may flow from validation into the
model after its selection job is done, never from test), score once, never
retune.

**3. If XGBoost beats Ridge on validation but loses on test, what does that
suggest?**

That the validation edge was window-specific: patterns of the 2015-2018 regime
(or selection luck across the grid) that 2019-2023 did not repeat, i.e.
overfitting to the validation window through tuning. This project produced the
mirror image, xgb_delta's skill improving from +0.085 (calm window) to +0.151
(disrupted window), which teaches the same lesson from the other side: each
window favors different strategies, so a single window's ranking is weak
evidence either way, and the clustered bootstrap interval is the honest
companion to any point ranking.

## Frozen configuration record

XGB_LEVEL = max_depth 6, learning_rate 0.10, n_trees 125 (validation grid
winner). XGB_DELTA = max_depth 3, learning_rate 0.10, n_trees 173 (validation
grid winner). Both frozen by Khawar on 14 July 2026, taken as printed with no
post-hoc second-guessing; transcribed into `src/train.py`. After the single
test run, results are frozen: no retuning on any split. Session 6 interprets;
it does not re-fit.
