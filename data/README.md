# Data

The project uses the official Our World in Data CO2 dataset.

Download URLs:

- Dataset: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
- Codebook: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv

The files are downloaded locally into `data/raw/`. The large raw dataset should not be committed to GitHub. Record the retrieval date and retain the source URLs so the analysis is reproducible.

## Entity filtering and exclusions

The country filter keeps rows with a non-missing `iso_code` that does not start with `OWID_` (session 1 notebook, section 3). This yields 218 country entities and excludes 36 aggregate entities. Most exclusions are continent, income-group, or organization aggregates (`World`, `Asia`, `European Union (27)`, `OECD (GCP)`, etc.) that would double-count real countries.

Three exclusions are real, specific places, not statistical aggregates, and are worth documenting separately so they are not mistaken for an oversight:

- **Kosovo** — excluded because it lacks a standard ISO 3166-1 alpha-3 code in this dataset, reflecting its disputed international recognition status. A genuinely populated place is missing from the country-level model as a result.
- **Ryukyu Islands** — a historical/administrative entity (pre-1972 Okinawa-area reporting), not a current sovereign state.
- **Kuwaiti Oil Fires** — a one-off historical event record (1991 Gulf War oil fires), not a country.

These three should be named explicitly in the project README's data-limitations section rather than left implicit in the "36 aggregates" count.

Separately, of the 218 ISO-coded countries, three have an ISO code but zero non-missing `co2` values in the entire series: **Monaco, San Marino, Vatican**. All three are microstates too small for OWID's territorial CO2 methodology to publish an estimate. They fail the eligibility filter's population and history requirements anyway, but this is a distinct reason (no data at all, not just a short history) worth naming in the data-limitations section.

**Antarctica** also passes the country filter (it holds a real, non-`OWID_` ISO code, `ATA`) despite being an uninhabited continent with no state or permanent population; its 2023 `co2` value is 0. **Christmas Island** (Australian external territory, near-zero population) is a similar near-zero case. Both are removed downstream by the eligibility filter's `population > 1M` requirement, but are named here so the filter's behavior is documented rather than an unexplained side effect.

## Two-wave feature strategy (decided 8 Jul 2026, extended)

Wave 1 (near-complete, drop missing rows, no imputation): `co2` and its lags/rolls, `population`, `co2_per_capita`, `share_global_co2`, **plus `cement_co2` and `flaring_co2`** (4.8% and 8.1% missing 1990+, close enough to the Wave-1 threshold that row-dropping the missing fraction is cheap, and both carry industrial-process signal distinct from combustion `co2`).

Wave 2 (29-47% missing, needs explicit missing-data handling — imputation, drop, or a missingness-indicator feature, to be decided when this wave is built): `coal_co2`, `gas_co2`, `gdp`, `consumption_co2`.

## References

Our World in Data CO2 dataset repository: https://github.com/owid/co2-data

