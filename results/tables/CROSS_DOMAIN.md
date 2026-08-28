# Cross-domain Mask-View rank reversal

This repository is standalone. Numbers come from `data/frozen/`.

## Lake (standardized MAE)
| pattern | medium | metric | simple_Linear | learned_MaskViewST | recipe_spatial_plus_l0 | BRITS | winner_default_grid | learned_beats_Linear | recipe_beats_Linear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| point | lake_dianchi | std_MAE | 0.1611 | 0.2969 | 0.2946 | 0.4295 | Linear | False | False |
| block_time | lake_dianchi | std_MAE | 0.2538 | 0.3261 | 0.3131 | 0.4417 | Linear | False | False |
| sensor | lake_dianchi | std_MAE | 0.6957 | 0.4413 | 0.4209 | 0.4302 | BRITS | True | True |
| station | lake_dianchi | std_MAE | 0.6786 | 0.5386 | 0.5399 | 0.4345 | BRITS | True | True |
| mixed | lake_dianchi | std_MAE | 0.2636 | 0.3392 | 0.334 | 0.4332 | Linear | False | False |

## Ocean (lead-1 RMSE µmol kg⁻¹)
| pattern | medium | metric | keep_frac | persist_locf | spatial_linear | clim_RMSE | ST_RMSE | lead1_best | lead2_best | lead1_F1 | degradation_vs_dense | st_margin_vs_clim | lead2_falls_to_climatology |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | ocean_ecs | lead1_RMSE_umolkg | 1.0 | 8.265 | 8.265 | 5.298 | 3.876 | st_transformer | hybrid_clim_st | 0.741 | 0.0 | 1.422 | False |
| point | ocean_ecs | lead1_RMSE_umolkg | 0.249 | 6.176 | 12.697 | 5.298 | 5.016 | st_transformer | climatology | 0.692 | 0.294 | 0.282 | True |
| block | ocean_ecs | lead1_RMSE_umolkg | 0.267 | 6.105 | 13.728 | 5.298 | 4.994 | st_transformer | climatology | 0.683 | 0.289 | 0.304 | True |
| block_time | ocean_ecs | lead1_RMSE_umolkg | 0.45 | 10.049 | 10.049 | 5.298 | 4.273 | st_transformer | hybrid_clim_st | 0.72 | 0.102 | 1.025 | False |
| sensor | ocean_ecs | lead1_RMSE_umolkg | 0.2 | 5.99 | 5.99 | 5.298 | 5.075 | st_transformer | climatology | 0.693 | 0.309 | 0.223 | True |
| station | ocean_ecs | lead1_RMSE_umolkg | 0.089 | 5.599 | 14.168 | 5.298 | 5.232 | st_transformer | climatology | 0.674 | 0.35 | 0.066 | True |
| mixed | ocean_ecs | lead1_RMSE_umolkg | 0.205 | 6.006 | 12.773 | 5.298 | 5.071 | st_transformer | climatology | 0.68 | 0.308 | 0.227 | True |
| argo | ocean_ecs | lead1_RMSE_umolkg | 0.078 | 5.538 | 15.15 | 5.298 | 5.241 | st_transformer | climatology | 0.667 | 0.352 | 0.057 | True |

## Shared patterns
| pattern | lake_winner | lake_recipe_beats_Linear | ocean_lead1_best | ocean_lead2_best | ocean_lead1_degradation | ocean_persist_unmasked_RMSE | ocean_persist_locf_RMSE | ocean_clim_RMSE | ocean_ST_RMSE | ocean_ST_beats_clim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| point | Linear | False | st_transformer | climatology | 0.294 | 8.265 | 6.176 | 5.298 | 5.016 | True |
| block_time | Linear | False | st_transformer | hybrid_clim_st | 0.102 | 8.265 | 10.049 | 5.298 | 4.273 | True |
| sensor | BRITS | True | st_transformer | climatology | 0.309 | 8.265 | 5.99 | 5.298 | 5.075 | True |
| station | BRITS | True | st_transformer | climatology | 0.35 | 8.265 | 5.599 | 5.298 | 5.232 | True |
| mixed | Linear | False | st_transformer | climatology | 0.308 | 8.265 | 6.006 | 5.298 | 5.071 | True |

Do not compare MAE to µmol kg⁻¹. Compare **who wins**.
Ocean `persist_unmasked` ignores the mask; use `persist_locf` as the fair persistence analog.

## Dual protocol vs EcoInf 2025

# Dual protocol: EcoInf 2025 missingness vs Mask-View operational bank

Same Dianchi panel. EcoInf: random 20-80% and 1-4 week gaps (doi:10.1016/j.ecoinf.2025.103283).
Learned EcoInf numbers are spatial_plus_l0 (current MixHop checkpoint). maskview_st.pt is an older graph block and was skipped.
Week-gap Linear/LOCF see the full series; spatial_plus_l0 is stitched 6-day windows.

| Protocol | Setting | Linear | LOCF | MaskView-ST | spatial_plus_l0 | Winner |
|---|---|---:|---:|---:|---:|---|
| ecoinf_random | random_20pct | 0.160 | 0.205 | - | 0.292 | Linear |
| ecoinf_random | random_40pct | 0.183 | 0.228 | - | 0.306 | Linear |
| ecoinf_random | random_60pct | 0.209 | 0.247 | - | 0.340 | Linear |
| ecoinf_random | random_80pct | 0.242 | 0.275 | - | 0.408 | Linear |
| ecoinf_week_gap | 1week | 0.311 | 0.357 | - | 0.349 | Linear |
| ecoinf_week_gap | 2week | 0.285 | 0.340 | - | 0.378 | Linear |
| ecoinf_week_gap | 3week | 0.341 | 0.416 | - | 0.401 | Linear |
| ecoinf_week_gap | 4week | 0.402 | 0.475 | - | 0.427 | Linear |
| maskview_operational | point | 0.161 | 0.206 | 0.297 | 0.295 | Linear |
| maskview_operational | block_time | 0.254 | 0.290 | 0.326 | 0.313 | Linear |
| maskview_operational | sensor | 0.696 | 0.696 | 0.441 | 0.421 | spatial_plus_l0 |
| maskview_operational | station | 0.679 | 0.679 | 0.539 | 0.540 | BRITS |

Linear wins all 8 EcoInf settings. Operational sensor/station flip the ranking.



## Natural missingness
# Natural missingness taxonomy and year-shift replay

Naturally missing cells have no ground truth. Replay copies another year's
missing calendar onto 2024 observed cells. MCAR control uses the same hide count.

Station-outage duration (all years): per-run p50=0.2 days, p90=0.8 days; cell-weighted p50=3.5 days, p90=630.5 days (n_runs=6263).

## Taxonomy (fraction of missing cells)

| split | missing_rate | frac_station | frac_sensor_ge1day | frac_block | frac_point | non_point |
|---|---:|---:|---:|---:|---:|---:|
| all | 0.198 | 0.969 | 0.019 | 0.006 | 0.006 | 0.994 |
| train | 0.257 | 0.962 | 0.027 | 0.006 | 0.006 | 0.994 |
| val | 0.130 | 0.978 | 0.003 | 0.010 | 0.010 | 0.990 |
| test | 0.143 | 0.985 | 0.007 | 0.004 | 0.004 | 0.996 |

## Replay vs MCAR (standardized MAE)

| Protocol | Setting | Linear | LOCF | spatial_plus_l0 | Winner | hide_rate |
|---|---|---:|---:|---:|---|---:|
| year_shift_replay | 2022_to_2024 | 0.383 | 0.495 | 0.494 | Linear | 0.105 |
| year_shift_replay | 2023_to_2024 | 0.328 | 0.403 | 0.474 | Linear | 0.035 |
| mcar_matched_rate | 2022_to_2024 | 0.168 | 0.217 | 0.297 | Linear | 0.105 |
| mcar_matched_rate | 2023_to_2024 | 0.147 | 0.198 | 0.291 | Linear | 0.035 |
