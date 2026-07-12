# Session 2 check questions — answers and explanations

Dr. Khawar Naeem, emission-trajectory ML project. Answered after working through `02_build_features_walkthrough.ipynb` cell by cell with Claude (real code executed live against the actual raw CSV and `data/processed/modeling_table.csv`, since Jupyter is not installed on this machine), 13 July 2026. Khawar answered first; Claude reviewed, corrected, and extended each answer where needed (noted per question), matching the Session 1 protocol.

## 1. Write, from memory, the pandas expression for a 5-year rolling mean of co2 that uses only information available at year t. Why is shift-before-roll NOT needed here, and when would it be?

**Answer:** `df.groupby("country")["co2"].rolling(5).mean()`. At year t this window covers t-4 through t inclusive, and including year t's own value is legal because it is genuinely known at prediction time (you are standing in year t, about to predict t+1). Shift-before-roll is only needed when a window must deliberately exclude the current year; it is not needed here because the window is allowed to include it.

*Khawar's original answer wrote `shift(-1)` then `rolling(5).mean()`. This was corrected: `shift(-1)` is the target's formula (pulls a future row backward) and does not belong in this feature at all; using it here would leak a future value into a feature meant to predict the future, the exact trap the project is built to avoid. The correct expression has no shift of any kind, plus the `groupby("country")` was missing from the original recall. Khawar's stated reason for not needing shift-before-roll ("since t is known") was correct and needed no correction.*

## 2. What happens in each country's earliest rows when co2_lag10 is created, and what does the pipeline do with those rows? What does each country's FINAL row lack, and why?

**Answer:** A country's first 10 rows have no year 10 years earlier to pull from, so `co2_lag10` is `NaN` for each of them (verified live on Qatar: 1949-1958, its first 10 reported years, all show `co2_lag10 = NaN`; 1959 is the first row where it resolves, correctly pulling 1949's value). These rows get dropped by `df.dropna(subset=CORE_FEATURES)` in `filter_eligible`. Separately, each country's final row (e.g. Qatar 2024) lacks `target_co2_next`, because `shift(-1)` needs a following row to pull from and none exists yet; this is dropped by a separate line, `df.dropna(subset=["target_co2_next"])`. Two different features, two different directions (lag looks backward and runs out at the start of history; target looks forward and runs out at the end), same underlying principle: the pipeline cannot manufacture history or future that does not exist, so it honestly drops what it cannot compute rather than fabricating a value.

*Khawar indicated he was not clear on this question rather than attempting it independently. Claude explained the full mechanism, including live verification against Qatar's real data for both the early-row lag gap and the final-row target gap, and the two specific `dropna` lines in `src/build_features.py` responsible for removing each.*

## 3. Qatar's 2023 row: state its target value, and which split it belongs to and why (two separate decisions are involved).

**Answer:** Target value 125.812 (Qatar's real 2024 co2, pulled backward by `shift(-1)`). Split: `provisional_2024`, because splits are keyed on `target_year = year + 1`, not on the feature year itself. Feature year 2023 has target_year 2024, and 2024 sits in its own provisional bucket, outside the 2019-2023 headline test window, because the newest OWID release year is provisional and revisable.

*Khawar's original answer was correct and unaided on both parts, including correctly avoiding the plausible-looking trap of assuming "year 2023" belongs in the 2019-2023 test window (it does not, because the row's answer, not its feature year, decides the split).*

## 4. Why must features be built before eligibility filtering, and not after?

**Answer:** The eligibility rules (>=40 years of history, population >=1M) delete rows. If filtering ran first, the deletions would punch gaps into what was a complete per-country timeline, and any lag/rolling/slope computed afterward would silently recompute against a gappy series, reproducing the positional-vs-temporal bug (shift grabbing "the previous row" rather than "the previous year") except self-inflicted by the pipeline's own filtering step rather than by a genuine gap in the raw data. Critically, this failure is silent: a lag on a filtered series does not error, it just quietly returns a technically-real but wrong number. Deleting a finished, correctly-computed row after all features exist does no damage; deleting a row before something downstream needs to see it does.

*Khawar's original answer identified the core mechanism (filtering first creates gaps, corrupting later lags) correctly and unaided. Claude added the silent-failure framing and the "delete after computing, not before" summary rule.*

## 5. A colleague splits train/val/test on the feature year instead of the target year. Which specific rows are now mislabeled, and which direction does the resulting evaluation bias go?

**Answer:** Applying the same cutoff numbers (<=2014 / 2015-2018 / 2019-2023 / 2024) directly to the feature year instead of the target year mislabels exactly the three boundary years, per country: year 2014 (correctly `val`, since its answer is 2015) becomes `train`; year 2018 (correctly `test`, since its answer is 2019) becomes `val`; year 2023 (correctly `provisional_2024`, since its answer is 2024) becomes `test`. In every case a row is pulled backward into an earlier, less-protected split, so training secretly contains an early look at validation's answer pattern, validation secretly contains an early look at test's first year, and the headline test metric would even absorb the still-revisable 2024 answer. Because country emissions barely change year to year, this leak biases reported performance **optimistically**: each split looks better than genuine out-of-sample performance would actually be, since it has effectively been given a one-step-early preview of the next, more-protected split.

*Khawar indicated he was not clear on this question rather than attempting it independently. Claude worked it through against Qatar's real rows (2013-2023) to identify the exact three boundary years affected, then reasoned through the bias direction from the persistence property (median absolute year-over-year change ~4.4%) established in Session 1.*

## Session note

Two of five answers (3 and 4) were correct and unaided on the first attempt. One (1) needed a specific correction: conflating the target's `shift(-1)` formula with the rolling-mean feature's formula, which would have introduced exactly the kind of future-leakage the project is designed to prevent. Two (2 and 5) needed the full mechanism explained rather than being attempted independently. All five were grounded in real, live-executed code against the actual raw CSV and the actual `data/processed/modeling_table.csv`, not toy claims, including several concrete boundary-row checks (Qatar's 1949-1959 lag gap, the 2013-2023 split table) that surfaced during the walkthrough itself.

## References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data
