# Research Publication Roadmap

Dr. Khawar Naeem, Qatar Transportation and Traffic Safety Center (QTTSC), Qatar University. Prepared 13 July 2026, with Claude, using the `research-idea-scout` method (capability x current situation x gap x data x outlet fit). Every current-situation and literature-gap claim below was verified by live web search, not recalled from memory. This is a separate track from the numbered ML sprint sessions in `CLAUDE.md` and `AGENTS.md`, and starts only after Session 7 closes the core sprint.

## 1. Purpose

The emission-trajectory ML project is currently a portfolio repository: an honest, leakage-safe, chronologically-validated forecasting pipeline. This document plans how to extend it into a genuinely novel, publishable research contribution, without derailing the active sprint.

## 2. Capability profile

The distinctive combination this project can draw on:

- A working, leakage-safe, chronologically-validated ML forecasting pipeline with honest persistence-skill benchmarking (already built, Sessions 1-4).
- Multi-regional input-output (MRIO) and structural path analysis (SPA) expertise, evidenced by existing personal skills (`mrio-io-spa-methodology`, `python-mrio-spa-pipeline`).
- Graph-learning and gradient-boosting ML expertise (`ml-graph-learning-networks`).
- Emission-factor and life-cycle-assessment data-sourcing expertise, tied to the QTTSC day job.
- A Qatar/GCC vantage point: the highest per-capita CO2 emitter in this project's own dataset, and a major LNG exporter, giving an authentic focal case not available to most researchers in this space.

## 3. Three staged ideas

### Idea 1: Metric-reversal note (near-free)

The MAE-vs-percentage-error rank reversal already found live in Session 3: on the persistence baseline's validation-year error table, Russia has the lowest percentage error (1.33%) despite a top-10 absolute-error miss, while Pakistan (11.05%) and Vietnam (8.22%) have far higher percentage errors despite smaller absolute misses. This mirrors the totals-vs-per-capita reversal already used in this project's figures 7-8. The underlying theory is well established (Hyndman and Koehler, 2006, already verified and cited in `math/references.bib`); search did not surface a recent country-panel emissions-forecasting paper that foregrounds this specific diagnostic for evaluation practice. Lowest effort of the three; already half-built. Can stand alone as a short methods note, or become a section of Idea 2.

Per `CLAUDE.md`'s 13 July 2026 decisions-log entry, before this idea is finalized: re-run the same per-country MAE-vs-percentage breakdown on Session 5's final TEST-set predictions (not the validation-only numbers found in Session 3) and confirm whether the same countries, or a similar reversal, still holds.

### Idea 2: Methodology-audit paper (moderate lift)

Search confirmed a real, citable gap: recent (2024-2025) published machine-learning national-CO2-forecasting papers do not appear to report a persistence-null-model skill score, despite persistence being a strong, trivial-to-compute baseline. One example found: a 2025 Scientific Reports paper forecasting the top eleven emitters through 2030, reporting 96.21 percent average "accuracy" across six ML models, with no visible comparison against a naive persistence forecast (Nazir, 2025, or the relevant lead author; see reference below; full author list to be confirmed when this idea is developed). This project's own Session 1 finding, median absolute year-over-year change of approximately 4.4 percent of level since 2010, indicates persistence is a materially strong baseline that a claimed-accurate model should be measured against.

Contribution: apply this project's own `src/evaluate.py` discipline (same-rows rule, persistence skill score, scale-aware metrics) to a comparable feature set drawn from public data, and report how much of a comparable model's claimed accuracy survives an honest null-model comparison. This reuses the existing pipeline almost entirely.

Rigor upgrade added 13 July 2026 (strengthens this idea in particular): `src/evaluate.py` now includes `cluster_bootstrap_skill`, a country-clustered bootstrap that puts a confidence interval and a bootstrap significance p-value on a skill score, formalized in `math/main.pdf` Section 6 (references Diebold and Mariano 1995, Efron and Tibshirani 1993, Cameron, Gelbach and Miller 2008). This closes the biggest rigor gap for a publishable version: reviewers at any target journal will ask whether a reported skill difference is statistically distinguishable from zero, and most published ML CO2-forecasting papers report neither a persistence baseline nor a significance statement on their comparisons. A concrete demonstration already exists: this project's own linear-trend baseline has point skill -0.078 against persistence on validation, but the clustered 95 percent interval is roughly [-0.34, +0.20] with a bootstrap p near 0.7, so the two are statistically indistinguishable, a conclusion the bare point estimate hides. NOTE on ownership: the tool is additive infrastructure and is deliberately not wired into the mandatory comparison table; which significance test to adopt and how to interpret it remain modeling decisions Khawar owns (per AGENTS.md), to be settled when this idea is actually developed.

### Idea 3: MRIO/SPA bridge paper (highest novelty, uses the full capability stack)

Couple an honestly-benchmarked ML national-emissions forecast (this project) as an input to a structural-path-analysis or multi-regional input-output model, to project forward-looking trade-embodied-carbon exposure. Framed around the EU Carbon Border Adjustment Mechanism (CBAM), whose definitive phase began 1 January 2026 (confirmed current via search), and for which the World Bank has explicitly called for tools that let developing and exporting countries measure their exposure.

Search confirmed existing ML-plus-MRIO work (for example, graph-neural-network approaches that jointly learn interindustry network structure and couple it with sectoral GHG intensity) models the input-output network's own structure. Feeding an independently-forecasted, honestly-benchmarked national emissions trajectory into an MRIO/SPA model specifically to project forward-looking exposure appears to be an open combination, not yet done in this configuration.

Qatar and the wider GCC LNG-export position is a strong, authentic focal case: the highest per-capita emitter in this project's own data, a major LNG exporter in the middle of a real capacity expansion (North Field East and South, targeting 2027) against analyst warnings of a possible LNG glut by 2030, and public carbon-intensity-reduction targets (15 percent upstream, 25 percent at LNG facilities, by 2030).

Feasibility note: OWID's `co2` series is national-aggregate, not sectoral. Coupling it to an MRIO model requires a defensible simplifying assumption (for example, combining the national forecast with EXIOBASE's existing sectoral emission-intensity shares, held fixed or trended, rather than forecasting each sector independently), stated explicitly, consistent with this project's "statistical extrapolation, not a causal or engineering forecast" honesty rule. This is the biggest lift of the three and the long-horizon target.

## 4. Preprint policy, corrected

An initial assumption, that posting a preprint early could jeopardize later consideration at Elsevier or Nature Portfolio journals, was checked against the publishers' own stated policies and does not hold up. Both Springer Nature and Elsevier have explicit, standing policies stating that posting of preprints (on arXiv or similar servers) is not considered prior publication and does not affect consideration by their journals. A preprint also establishes a timestamped, public priority claim, which is protective against being scooped, rather than exposing the underlying idea.

Given the preference to protect the highest-value idea, the plan uses a split strategy rather than "preprint everything" or "preprint nothing":

- Ideas 1 and 2 (lower stakes; benefit from early feedback and a timestamped priority claim): preprint on arXiv when ready, then submit to a named journal.
- Idea 3 (the flagship idea): skip the preprint step and submit directly to the target journal, to retain full control over the timing and first public framing of the biggest idea. This is a legitimate, common choice for a flagship contribution, independent of the corrected publisher-policy question.

## 5. Venue targeting

Constraint, per an explicit preference: target hybrid journals (subscription-based by default; open access only if the author opts in and pays an article processing charge, or APC) rather than gold-open-access journals that charge every author. Heliyon was considered and dropped on this basis (it is a gold open-access, Cell Press title; an APC applies to every published article).

| Journal | Scope fit | Turnaround (verified where noted) | Cost via subscription route | Recommended for |
|---|---|---|---|---|
| MethodsX | Methods and protocol papers specifically; requires "evidence of efficiency... comparison with pre-existing practices," matching a persistence-skill-scored evaluation protocol | About 7 weeks submission to publication | Diamond open access; free for everyone, not only hybrid | Idea 1; possibly Idea 2 if framed tightly as a methods comparison |
| Applied Energy | Energy systems, forecasting, trade and policy | 1 day to first decision, 54 days post-review, 127 days total to acceptance (fastest verified among options considered) | Hybrid; confirmed not a forced-APC journal; free via subscription, OA optional at approximately 4,210 USD | Idea 2; Idea 3 under an engineering framing. Q1, 2025 impact factor 12.2 |
| Sustainable Production and Consumption | Production and consumption systems, supply chains; a natural home for MRIO/structural-path-analysis work | Not confirmed by search | Hybrid; free via subscription, OA optional at approximately 3,200 USD (IChemE members 20 percent discount) | Idea 3, arguably the strongest scope match found for the MRIO/SPA/trade-embodied-carbon framing. Q1, 2025 impact factor 9.6 |
| Sustainable Cities and Society | Urban sustainability, transportation, climate adaptation, smart cities | About 3 weeks to first decision, 5.2 weeks peer review (fast, confirmed) | Hybrid; free via subscription, OA optional at approximately 3,590 USD; 24-month self-archiving embargo available | Idea 3 only if a transportation-sector angle is developed (ties to the QTTSC affiliation); weaker fit for a purely national-aggregate CO2 story as currently scoped. Q1, 2025 impact factor 13.3 |
| Renewable Energy; Energy for Sustainable Development; Sustainable Energy Technologies and Assessments | Broader energy/sustainability scope | Not confirmed by search | Hybrid, no forced fee | Backup options if the primary targets are a poor fit once a draft exists |
| Ecological Indicators | Metrics and indicator-development methodology, a strong scope match for Idea 1 specifically | Not confirmed; likely multi-month | Standard hybrid | Alternative to MethodsX for Idea 1 |
| Journal of Cleaner Production | Good life-cycle-assessment/sustainability fit | 6-10 weeks to first decision; 4-8 months total to acceptance (confirmed slow) | Standard hybrid | Not recommended given the speed priority |

Note on Nature-tier journals: Nature Portfolio journals (for example, Nature Climate Change, Nature Sustainability, Nature Machine Intelligence) do publish AI-and-climate work, confirmed via search, but at a maturity and empirical-depth bar well beyond a first paper from a project built as a learning sprint, and no fast-turnaround figures were found for them. The realistic path to a high-end journal here is Idea 3, once fully matured with real EXIOBASE-based empirical results and ideally after Applied Energy or a comparable venue establishes a track record, not skipping the applied-venue stage.

### Global Environmental Change (checked at Khawar's request)

Global Environmental Change (GEC) was checked directly against its own aims-and-scope text (ScienceDirect). It is a fundamentally different kind of journal from the others in this table: its scope requires "a significant social science contribution" through governance studies, political economy, political ecology, justice frameworks, or decision sciences. Quantitative modeling is welcomed only when it "interrogates assumptions, values, and societal implications," not as a standalone technical contribution.

- Impact factor 9.3, Q1 (2025-2026), a genuinely high-prestige outlet, confirmed by search.
- Review time was not found by search; do not assume it is fast. Confirm directly with the journal before treating it as a speed-competitive option.
- Fit: poor for Ideas 1 and 2 (both are technical evaluation-methodology contributions without a governance or political-economy framing). Potentially a good fit for Idea 3, but only if reframed as a political-economy or governance argument, for example how CBAM as a new global carbon-trade-governance institution reshapes economic exposure and agency for a Gulf hydrocarbon-exporting state, with the ML-plus-MRIO forecast-and-propagation model serving as the empirical evidence for that argument.
- Search surfaced closely related, recent work confirming this space is active: "The 'triple burden' effect and 'pressure-opportunity paradox' of net-zero transitions: exploring the political economy of Carbon Border Adjustment Mechanism (CBAM) implementation in the Global South" (ScienceDirect, 2025), plus a paper mapping political responses to CBAM across 32 countries (2019-2024). These appear to be qualitative and policy-analytic; whether they cover Gulf LNG-exporting states specifically has not yet been verified and must be checked directly (reading the "triple burden" paper's country set) before finalizing a GEC-aimed framing, not assumed.

Net effect: Idea 3 has two legitimate framings for two different audiences, to be decided once the empirical work is further along: an engineering and applied framing for Applied Energy or Sustainable Production and Consumption, or a political-economy and governance framing for Global Environmental Change.

### Environmental journals (added 13 July 2026, second pass)

The first venue table skewed toward energy journals; this project is environmental first, so the following environmental journals in Global Environmental Change's family were checked directly. All are Elsevier; hybrid status and cost noted per journal. Metrics are 2024-2026 figures from search and should be reconfirmed at submission time.

| Journal | Scope fit | Metrics / turnaround (verified where noted) | Cost via subscription route | Recommended for |
|---|---|---|---|---|
| Resources, Conservation and Recycling | Material flow analysis, life-cycle assessment, input-output, circular economy - arguably the single best scope match found for the MRIO/footprint methodology itself | Impact factor about 13.7 (very high); turnaround not confirmed | Hybrid; the gold-open-access companion is a separate journal (RCR Advances), so the main title's subscription route is free. OA APC applies only if chosen | Idea 3, strongest environmental scope match for the MRIO/footprint framing; possibly Idea 2 |
| Ecological Economics | Environmental economics, input-output, footprint, natural-resource economics - a natural home for a trade-embodied-carbon/MRIO argument | Impact factor 6.7, Q1; turnaround not confirmed | Long-standing Elsevier subscription (hybrid) journal; search reported an OA APC of about 4,100 USD, which is the opt-in OA figure, not a forced fee - confirm hybrid status at submission | Idea 3, economics-leaning framing |
| Environmental Science & Policy | Climate change, environmental resource management, sustainability, policy-society interface | Impact factor 6.55; reported review speed about 15 days (fast); acceptance about 12% | Hybrid; traditional subscription route free, OA APC about 3,410 USD, waivable in some cases | Idea 3, policy-leaning framing; a faster, environmental-science alternative to Global Environmental Change |
| Journal of Environmental Management | Environmental system modelling and optimization, environmental impact assessment, life-cycle analysis, material flow analysis, emission accounting - explicitly names the methods this project uses | High impact factor (about 8, reconfirm); turnaround not confirmed | Hybrid | Ideas 2 and 3, technical-environmental framing |
| Energy and Climate Change | Energy-climate intersection, emissions-reduction strategies, social and physical sciences | Impact factor 5.6 | CAUTION: search described it as "open access" with an APC of about 4,110 USD - it may be a gold-open-access (forced-fee) journal, which would violate the no-forced-fee constraint. DO NOT target until hybrid-vs-gold status is confirmed directly | Only if confirmed hybrid |

Revised environmental recommendation for Idea 3: **Resources, Conservation and Recycling** is now the leading target for the MRIO/footprint framing (best scope match, very high impact, hybrid), with **Ecological Economics** (economics framing) and **Environmental Science & Policy** (policy framing, and fast) as strong environmental alternatives. The energy journals (Applied Energy, Sustainable Production and Consumption) remain valid only if the paper's framing leans genuinely toward energy systems rather than environmental footprint accounting. Sustainable Cities and Society stays relevant only under a transportation-sector framing.

## 6. Sequencing

This is a separate track. It starts only after Session 7 closes the core ML sprint (Sessions 4 through 7: Ridge and tree models, XGBoost, error analysis, reproducibility). It does not compete with the sprint's 2-4 hour per day cadence; it is recorded now so none of this thinking is lost before then.

## 7. Next exact action for this track

Do not start until Session 7 is closed. When resumed: begin with Idea 1 (lowest effort, already half-built), re-verifying the metric-reversal finding against Session 5's final test-set predictions rather than the validation-only numbers found in Session 3, then decide between a standalone MethodsX submission or folding it into Idea 2.

## References

Hyndman, R.J. and Koehler, A.B. (2006). Another look at measures of forecast accuracy. International Journal of Forecasting, 22(4), 679-688. https://doi.org/10.1016/j.ijforecast.2006.03.001

Scientific Reports (2025). A machine learning approach to carbon emissions prediction of the top eleven emitters by 2030 and their prospects for meeting Paris agreement targets. https://www.nature.com/articles/s41598-025-04236-5

World Bank Blogs. How developing countries can measure exposure to the EU's carbon border adjustment mechanism. https://blogs.worldbank.org/en/trade/how-developing-countries-can-measure-exposure-to-the-eu-s-carbon

ScienceDirect (2025). The "triple burden" effect and "pressure-opportunity paradox" of net-zero transitions: exploring the political economy of Carbon Border Adjustment Mechanism (CBAM) implementation in the Global South. https://www.sciencedirect.com/science/article/pii/S2211467X25002767

MethodsX, guide for authors. https://www.sciencedirect.com/journal/methodsx/publish/guide-for-authors

Applied Energy, open access information. https://www.sciencedirect.com/journal/applied-energy/publish/open-access-options

Sustainable Production and Consumption, open access information. https://www.elsevier.com/journals/sustainable-production-and-consumption/2352-5509/open-access-options

Sustainable Cities and Society, open access information. https://www.sciencedirect.com/journal/sustainable-cities-and-society/publish/open-access-options

Global Environmental Change, aims and scope. https://www.sciencedirect.com/journal/global-environmental-change

Resources, Conservation and Recycling, journal home. https://www.sciencedirect.com/journal/resources-conservation-and-recycling

Ecological Economics, journal home. https://www.sciencedirect.com/journal/ecological-economics

Environmental Science & Policy, journal home. https://www.sciencedirect.com/journal/environmental-science-and-policy

Journal of Environmental Management, journal home. https://www.sciencedirect.com/journal/journal-of-environmental-management

Energy and Climate Change, journal home. https://www.sciencedirect.com/journal/energy-and-climate-change
