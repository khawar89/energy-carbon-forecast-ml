# Session 6 check questions and reconciliation record

Recorded 14 July 2026. The pre-registration, reconcile answers, and the three
check answers below were prepared with Claude's full guidance at Khawar's
request (same attribution convention as the Session 3 and Session 5 records).

## Pre-registration scoring (4 questions, Claude-guided)

Question 1 half missed: trend was predicted worse than persistence in 2020
but was slightly better (MAE 13.135 vs 13.950, within-year skill +0.058).
The misunderstanding: treating large emitters as uniformly rising pre-2020,
when enough (United States, Germany, Japan) were flat or declining that
trend's downward slopes absorbed part of the COVID drop. The mirrored-2021
half was correct: 2021 is trend's only losing year (skill -0.043), because
its five-year slope window then contained the collapse while emissions
rebounded. Question 2 correct: the reversal survived on test, including the
cast (Russia again the low-percentage case at 2.14 percent, against the
guided caveat that 2022 might displace it). Question 3 correct: skill is
concentrated in the giant tier and sharply negative for small emitters.
Question 4 correct on both halves: co2_slope5 first (2.889), the co2 level
family individually understated (co2_roll5_mean 0.098).

## Reconcile and interpret

Recorded in the notebook's section 6 (reconcile cell) with the numbers;
highlights: 2020 is every model's worst year; xgb_delta holds positive skill
in all five test years but earns most of it in the calm years 2019/2022 and
almost entirely in the giant tier (+0.325 there, -0.863 small tier);
ridge_delta is the giant tier's quiet winner (+0.329); the level trees'
giant-tier MAE (508 and 773 Mt vs persistence's 169) is the saturation
failure made visible; the Session 3 MAE-versus-percentage reversal survives
on test and is cleared for figures and the public post.

## Check questions

**1. Why is percentage error misleading for near-zero emitters?**

Percentage error divides by the actual value, so as emissions approach zero
the ratio explodes or is undefined: a 0.2 Mt miss on a 0.4 Mt emitter reads
as 50 percent while a 40 Mt miss on China reads as under 1 percent. A mean
percentage error over mixed sizes is therefore dominated by the smallest
denominators, the least consequential rows. That is why `evaluate.mdape`
excludes emitters below 1 Mt by definition and why this project reports
absolute and percentage views side by side rather than either alone
(Hyndman and Koehler 2006 formalize this caution).

**2. Were 2020 errors larger for persistence or for the trend baseline, and
why?**

Pre-registered: trend worse (persistence over-predicts by the fall; trend
adds its extrapolated pre-COVID rise on top). Actual: trend slightly BETTER
in 2020 (13.135 vs 13.950), because enough large emitters had flat or
declining pre-2020 slopes that trend's extrapolation absorbed part of the
drop. The mechanism the prediction got right arrived one year late: in 2021
trend's slope window contained the collapse and pointed down into the
rebound, making 2021 trend's only losing year (-0.043). Lesson: extrapolation
through a break fails on a delay equal to the break entering the window.

**3. Why can permutation importance understate a feature that is correlated
with another?**

Permutation importance measures how much error worsens when one column is
shuffled while the model and all other columns stay fixed. If a correlated
sibling carries nearly the same information, the model's trees can lean on
the sibling for most rows, so shuffling either column alone barely hurts,
and BOTH can rank low even when the shared signal is essential. Observed
directly: co2_roll5_mean scored 0.098 and co2_lag10 0.332 while the family's
directional summary co2_slope5 scored 2.889; the level family's low
individual scores reflect redundancy, not irrelevance. Importances over
correlated features are read as group structure, never as per-feature
rankings.

## Artifacts produced this session

`results/error_by_year.csv`, `results/error_by_country_persistence_top10.csv`,
`results/error_by_tier.csv`, `results/permutation_importance_xgb_delta.csv`;
figures `fig9_error_by_year.png`, `fig10_reversal_test.png` (the cleared
reversal figure), `fig11_skill_by_tier.png`, each with a modeling-consequence
markdown cell in the executed notebook. No model was re-fit or retuned; the
frozen xgb_delta configuration was reproduced unchanged for permutation
importance only.
