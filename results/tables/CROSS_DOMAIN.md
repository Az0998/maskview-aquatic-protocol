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
| pattern | medium | metric | ST_RMSE | lead1_best | lead2_best | lead1_F1 | degradation_vs_dense | lead2_falls_to_climatology |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | ocean_ecs | lead1_RMSE_umolkg | 3.876 | st_transformer | hybrid_clim_st | 0.741 | 0.0 | False |
| point | ocean_ecs | lead1_RMSE_umolkg | 5.016 | st_transformer | climatology | 0.692 | 0.294 | True |
| block | ocean_ecs | lead1_RMSE_umolkg | 4.994 | st_transformer | climatology | 0.683 | 0.289 | True |
| block_time | ocean_ecs | lead1_RMSE_umolkg | 4.273 | st_transformer | hybrid_clim_st | 0.72 | 0.102 | False |
| sensor | ocean_ecs | lead1_RMSE_umolkg | 5.075 | st_transformer | climatology | 0.693 | 0.309 | True |
| station | ocean_ecs | lead1_RMSE_umolkg | 5.232 | st_transformer | climatology | 0.674 | 0.35 | True |
| mixed | ocean_ecs | lead1_RMSE_umolkg | 5.071 | st_transformer | climatology | 0.68 | 0.308 | True |
| argo | ocean_ecs | lead1_RMSE_umolkg | 5.241 | st_transformer | climatology | 0.667 | 0.352 | True |

## Shared patterns
| pattern | lake_winner | lake_recipe_beats_Linear | ocean_lead1_best | ocean_lead2_best | ocean_lead1_degradation |
| --- | --- | --- | --- | --- | --- |
| point | Linear | False | st_transformer | climatology | 0.294 |
| block_time | Linear | False | st_transformer | hybrid_clim_st | 0.102 |
| sensor | BRITS | True | st_transformer | climatology | 0.309 |
| station | BRITS | True | st_transformer | climatology | 0.35 |
| mixed | Linear | False | st_transformer | climatology | 0.308 |

Do not compare MAE to µmol kg⁻¹. Compare **who wins**.