"""Drift guard: train.py must model with the exact feature lists that
build_features.py used to build and verify the modeling table.

train.py imports the lists rather than keeping copies, and this test pins
the contract: if a local copy is ever reintroduced and edited on one side
only, the assertion fails instead of the models silently training on a
different feature set than the table was verified for.

Run directly (prints OK) or via pytest:

    python src/test_feature_lists.py
"""

import build_features
import train


def test_feature_lists_match() -> None:
    assert train.FEATURES == build_features.CORE_FEATURES + build_features.NULLABLE_FEATURES, \
        "train.FEATURES has drifted from the lists in build_features.py"
    assert len(train.FEATURES) == len(set(train.FEATURES)), \
        "train.FEATURES contains duplicate column names"


if __name__ == "__main__":
    test_feature_lists_match()
    print(f"OK: train.py uses build_features' lists unchanged "
          f"({len(build_features.CORE_FEATURES)} core + "
          f"{len(build_features.NULLABLE_FEATURES)} nullable = "
          f"{len(train.FEATURES)} features)")
