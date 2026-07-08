# Session 1 check questions — answers and explanations

Dr. Khawar Naeem, emission-trajectory ML project. Answered after running `01_framing_eda.ipynb` end to end, 8 July 2026. Khawar answered first; Claude reviewed, corrected, and extended each answer where needed (noted per question).

## 1. Why must `Asia` and `European Union (27)` rows be excluded from training?

**Answer:** Aggregate entities like `Asia` and `European Union (27)` are pre-summed totals built from their member countries' emissions. Including them alongside the countries they contain would double-count the same underlying emissions at different scales (for example China's emissions counted once as `China` and again inside `Asia`), which would distort the model's sense of what a typical row looks like.

*Khawar's original answer identified this correctly on the first attempt (double counting). No correction needed.*

## 2. A feature for year *t* accidentally uses `co2_growth_prct` from year *t+1`. What is this error called, and why would it make validation results look great and real forecasts fail?

**Answer:** This is **leakage** (specifically future leakage or look-ahead leakage), not overfitting. The distinction: overfitting is a training-process problem where the model memorizes noise in the training data and fails to generalize; leakage is a data-construction problem where the model is given information, during training or feature-building, that would not actually exist yet at real prediction time. Here, `co2_growth_prct` for year t+1 directly encodes information about the very change being predicted, so it acts like an answer key. Validation looks excellent because the same illegitimate feature is present in validation too, but at real deployment time, standing in year t forecasting t+1, that number does not exist yet, so the model fails immediately in genuine use.

*Khawar's original answer said "overfitting." Claude corrected this to leakage and explained the distinction between the two failure modes.*

## 3. Why is the validation set 2015-2018 rather than a random 20% of rows?

**Answer:** A random split could place, for example, Qatar-2015 in training and Qatar-2012 in validation, meaning the model would train on data from later years than some of the rows it is validated against. That is leakage at the row-split level (as opposed to the feature level in question 2). It also would not simulate how the model is actually used: in reality you only ever have the past available to predict the future, never the reverse. A chronological split forces validation to behave like genuine forecasting, since every validation-year row sits strictly after every training-year row.

*Khawar's original answer noted the chronological pattern (using Qatar's steady growth as an example) but did not identify the leakage/deployment-simulation mechanism. Claude added the core reasoning.*

## 4. Why is persistence expected to be a strong baseline for this particular variable?

**Answer:** National emissions come from large, slow-moving physical infrastructure (power plants, vehicle fleets, factories) that does not change materially year to year absent a shock. The notebook confirmed this by hand: median absolute year-over-year change since 2010 is only 4.40% of the level. So "next year equals this year" is usually close to true, and only a real disruption (accident, natural disaster, war, a pandemic year like 2020) breaks the pattern.

*Khawar's original answer identified the incremental-change reasoning and gave correct examples of disruptions (accident, natural hazard, war) on the first attempt. No correction needed.*

## 5. Whose row count is bigger in this dataset, `World` or `China`, and why does it not matter for our model?

**Answer:** The two are not meaningfully different in row count. `World` is a single OWID-constructed aggregate entity with one row per year (the pre-summed global total, drawn from Our World in Data's own name), while `China` is a real country with its own row per year. Both likely span a similar number of years, so their raw row counts are close, regardless of `China` having far larger emissions values. It does not matter which has more rows, or how large its values are, because entity filtering is based on the `iso_code` field, not on row count or emissions size: `World` carries the `OWID_WRL` code, marked with the `OWID_` prefix that OWID uses for all of its own constructed aggregates, and is excluded on that basis alone.

*Khawar's original answer correctly noted China's emissions are largest, but had not connected "row count" to entity identity, and needed the OWID acronym and the concept of `World` as a constructed aggregate explained from scratch. Claude explained both before this final answer was written.*

## Session note

Two of five answers (1 and 4) were correct without correction. Three (2, 3, 5) needed a correction or a concept explained before landing on a solid answer, in each case around the same underlying idea: distinguishing genuine data problems (leakage, entity construction) from more familiar but incorrect labels (overfitting) or surface-level pattern observations. This is exactly the kind of first-principles gap the project's teaching-mode agreement (8 Jul 2026, `CLAUDE.md`) is meant to catch before Session 2 begins.

## References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data
