# Car Accident Analysis: Weather, Climate, and Population


## 1. Introduction
Driving is the default way Americans get around, and despite steady gains in vehicle safety technology, crashes remain a major source of death and economic loss — roughly 40,901 fatalities and an estimated $340 billion in economic costs in 2023. This project asks how much of crash risk is tied to *conditions* rather than driver behavior alone, focusing on weather and on regional/population differences. We combine accident records with population to test whether adverse weather and denser regions show elevated crash risk.

## 2. Data
- **US Accidents (2016–2023)** — 7,728,394 records of US traffic accidents, including timestamp, location, severity (1–4), and on-scene weather. This is our primary source.
- **State population** — used to convert raw accident counts into per-capita rates, so comparisons reflect risk rather than simply where more people (and cars) are.
- **NOAA nClimDiv (climate)** — identified as an exogenous monthly climate source (temperature, precipitation) for an extended model. Integrating it is described in Methods as an optional extension and left as future work.

**Important data caveat.** The US Accidents dataset is compiled from live traffic APIs, so reporting coverage varies across states and over time and some states are over-represented. We therefore treat absolute geographic counts cautiously and rely on per-capita rates and exposure-free comparisons.

## 3. Methods
- **EDA** — temporal patterns (by month/hour), severity distribution, and weather composition.
- **Statistical analysis** — because ~85% of driving (and accidents) occurs in clear/cloudy weather, raw accident counts by weather are misleading. We instead test the *severity* of crashes across weather types (an exposure-free comparison) using a chi-square test of independence (with Cramér's V for effect size) and a Kruskal–Wallis test.
- **Geospatial** — a per-capita state choropleth and a national hexbin density map of accident hotspots.
- **Predictive** — Poisson and Negative Binomial GLMs of monthly accident *counts* per state, with `log(population)` as an offset to handle exposure, plus month and Census-region terms; evaluated on a held-out final 6 months. A climate-augmented version using nClimDiv predictors is left as future work.

## 4. Results
**EDA.** The data spans 2016–2023 across 7,728,394 records. About 85% of accidents occurred in clear or cloudy conditions (Clear 3.04M, Cloudy 2.90M), with rain (467k), fog/low-visibility (183k), snow/ice (155k), and thunderstorms (78k) making up the rest. As anticipated, these raw counts reflect *exposure* — how often each condition occurs while driving — not risk. *(Insert `figs/eda_overview.png` and `figs/weather_counts.png`.)*

**Weather and severity.** Mean severity (1–4 scale) was highest in rain (2.27) and snow/ice (2.27), then cloudy (2.25) and thunderstorm (2.25), and lowest in clear (2.20) and fog/low-visibility (2.19). The association is statistically significant (chi-square = 32,916, df = 15, p < 0.001; Kruskal–Wallis H = 26,282, p < 0.001), **but the effect size is negligible: Cramér's V = 0.04**, and the full spread of mean severity is only ~0.08 points. With n = 6.8M, even trivial differences reach significance, so the practical takeaway is that adverse weather is associated with *very slightly* more severe crashes, not dramatically more. *(Insert `figs/severity_by_weather.png`.)*

**Geospatial.** Per-capita accident rates varied widely by state, led by South Carolina (an outlier at ~6,500 per 100k), then California (~4,000) and Oregon (~3,800). The hexbin map shows accidents concentrated along major metropolitan corridors. *(Insert `figs/choropleth.png` and `figs/density_hexbin.png`.)*

**Predictive.** A Poisson GLM of monthly state accident counts (month + region, with `log(population)` offset) showed strong overdispersion (dispersion ≈ 954), so a Negative Binomial model was fit to correct the inference. On the held-out final six months the two models predicted similarly (Poisson MAE 1,201 / RMSE 1,961; NB MAE 1,159 / RMSE 2,291). Accident counts peaked in **December (≈16% above the January baseline)**, confirming a winter seasonal pattern. *(Note: the deviance-based pseudo-R² values — 0.20 Poisson vs 0.085 NB — are not directly comparable across model families; the held-out errors are the meaningful comparison.)*

## 5. Discussion
Our hypothesis was that higher-population and harsher-weather regions would show elevated crash risk. The evidence is mixed and, importantly, constrained by data quality. Weather relates to crash severity in the expected direction — rain and snow crashes are marginally more severe than clear-weather crashes — but the effect is so small (V = 0.04) that weather is not a meaningful driver of *severity* in this dataset. Geographically, per-capita rates do not track population cleanly: South Carolina's extreme value and the South/West skew of the leaderboard most plausibly reflect uneven reporting coverage across the data's source APIs rather than true regional risk. The predictive model captured a sensible winter seasonality and regional baseline differences, but left most monthly variation unexplained — consistent with the dataset's known reporting inconsistencies, including the documented pandemic-era dip in 2020.

Two methodological lessons stand out. First, with millions of records, statistical significance is essentially automatic, so **effect size, not the p-value, is what should drive conclusions**. Second, **accident-reporting coverage is itself a confounder**, so per-capita and cross-state comparisons must be read cautiously.

## 6. Limitations
Reporting coverage in the accidents dataset is uneven across states and time, so geographic comparisons partly reflect data collection rather than true risk — South Carolina's outlier per-capita rate is the clearest example. The per-capita figures use approximate recent state populations and are a relative index (total accidents over the full window divided by a single-year population), not an annual rate. Weather is recorded categorically at the scene, the climate-augmented (nClimDiv) model was scoped but not included in the final run, and all results are associational, not causal.

## 7. Conclusion
Across 7.7 million accidents from 2016–2023, weather shows only a marginal association with crash severity (rain and snow slightly above clear), monthly accident counts follow a modest winter-peaking seasonal cycle, and per-capita rates vary by state in ways largely attributable to uneven reporting rather than population or climate. The clearest result is methodological: at this data scale, effect sizes and data-quality confounders matter far more than significance tests, and any conclusion about regional risk must account for how the data was collected. A natural next step is the climate-augmented count model using NOAA nClimDiv predictors, which could test directly whether month-to-month precipitation and temperature add explanatory power beyond seasonality.
