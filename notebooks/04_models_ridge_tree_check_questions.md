# Session 4 Check Questions: Ridge and Tree Benchmark

Closed: 13 July 2026

## 1. Why does standardizing features change Ridge's predictions but not the tree's? Where exactly in each algorithm does the difference live?

Ridge uses coefficient sizes, and its penalty is applied to those coefficients. If one feature is measured in millions and another in percentages, the coefficient sizes are not comparable unless the features are standardized. Standardizing changes Ridge because it changes the scale on which the coefficient penalty operates.

Trees do not use linear coefficients. They split on ordered thresholds such as `feature < value`. A monotonic rescaling changes the threshold value but not the ordering of rows, so tree predictions do not depend on standardization in the same way.

## 2. Bagging and boosting both combine many trees. State, in one sentence each, HOW each one reduces error, and which of the two our HistGB model is.

Bagging reduces variance by training many trees independently on resampled data and averaging their predictions.

Boosting reduces error sequentially by training each new tree to correct the remaining errors of the current ensemble.

The Session 4 `HistGradientBoostingRegressor` is a boosting model.

## 3. The imputer in the Ridge pipeline: on which rows was it fitted, which rows did it transform, and what specific harm occurs if it is fitted on all rows before splitting?

The imputer was fitted only on the training rows, using training-set medians. It then transformed both training and validation rows using those same learned medians.

If the imputer were fitted on all rows before splitting, validation-year information would enter the preprocessing step. That would cause leakage and make validation performance look more honest than it really is.

## 4. Your Ridge-on-level model almost certainly assigned a coefficient near 1 to `co2` after unscaling. What does that tell you about what it learned, and how does the delta parameterization change the question the model must answer?

A coefficient near 1 on current CO2 would indicate that Ridge level learned a persistence-like rule: next-year emissions are usually close to current-year emissions.

The delta parameterization changes the task by asking the model to predict the change from current CO2 to next-year CO2. Instead of mostly learning scale, it must learn movement.

## Session 4 result summary

The best validation MAE remained the persistence baseline. The best machine-learning model was `hgb_delta`, which came close to persistence but did not beat it on validation MAE. Both model families showed better behavior under the delta parameterization than under the level parameterization, but the improvement was not enough to produce positive persistence skill.

References:

Project notebook: `notebooks/04_models_ridge_tree.ipynb`

Saved results: `results/model_comparison.csv`
