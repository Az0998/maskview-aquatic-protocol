# Unified Mask-View pattern bank

Shared names. Construction differs by medium; evaluation question is the same:
**does the ranking of simple vs learned methods flip when missingness is operational rather than MCAR?**

| Pattern | Lake automatic station | Shelf oxygen (history cube) |
|---------|------------------------|-----------------------------|
| `point` | MCAR on observed cells | Static random keep on O₂ grid (same voxels all 12 months) |
| `block_time` | Consecutive downtime slab | Time slab × spatial block |
| `block` | (covered by block_time) | Spatial patch, all depths |
| `sensor` | Drop 1–2 variables | Hide selected O₂ channels/depths; physics stays |
| `station` | Whole station blackout | Column-limited stations |
| `mixed` | Point + block (± station) | Compound of the above |
| `argo` | n/a | Section-column proxy (7 cells); not live Argovis |
| `none` | n/a (natural ~19.8% already) | Dense O₂ history (upper bound) |

## Metrics (do not mix units)

Lake metrics stay **standardized MAE**. Ocean metrics stay **RMSE (µmol kg⁻¹)** and hypoxia F1.  
The comparable scientific object is **winner identity** and **skill degradation vs the easy-gap winner**.

## Effective keep (ocean, default `keep_ratio=0.25`)

Ocean spatial masks are **constant in time** (except `block_time`). A voxel is therefore fully observed for all 12 history months or never. Temporal linear interpolation of the last month is then identical to LOCF. Lake rates 10/20/30% are **not** the same quantity as ocean `keep_ratio=0.25`. Compare lake hide rates with ocean **point** voxel keep. Station keep is `n_stations × Z / n_water` (8 columns → 0.089 on this 450-voxel mask), independent of `keep_ratio`. Sensor with Z = 5 cannot realize 10 vs 20 vs 25% as distinct rates (all keep one layer).

| Pattern | Voxel keep | Notes |
|---------|-----------:|-------|
| none | 1.00 | Dense-history upper bound |
| block_time | 0.45 | Time slab; every voxel seen at some month |
| block | 0.27 | Spatial patch |
| point | 0.25 | Static random voxels, not independent MCAR each month |
| mixed | 0.21 | Station columns + extra points |
| sensor | 0.20 | Whole depth layers dropped |
| station | 0.089 | 8 random columns |
| argo | 0.078 | Yangtze-section proxy (7 grid cells), **not** live Argovis; treat as station analog |

## Fair ocean simple baselines

`persist_unmasked` / climatology in the original ablation **do not read the mask**. Fair counterparts: `persist_locf` (last observed O₂, climatology fill), `linear_time` (per-voxel temporal interp → last month), `spatial_linear` (horizontal fill of the LOCF field). Competitive simple bar is **climatology**, not persistence.

## Natural missingness (Dianchi 4 h grid)

Missing cells are not MCAR. 96.9% occur while all nine variables at a station are silent; isolated one-step holes are 0.6%. Station-outage lengths are heavy-tailed (cell-weighted median 3.5 days). Year-shift replay of 2022/2023 calendars onto observed 2024 cells still ranks Linear first, but MAE is about twice MCAR at the same hide rate. Mask-View `station`/`sensor` remain **stress tests** (no in-window temporal neighbors), not a copy of median downtime.

## Rank-reversal hypothesis

1. Easy gaps (`point`, short `block_time`): Linear / LOCF (lake) or dense ST (ocean lead-1) win or stay close.  
2. Hard gaps (`sensor`, `station`, `argo`): temporal interpolators collapse (lake). On the shelf, fair persist/linear never beat climatology; lead-1 ST still wins. Default station Δ ≈ 0.06 is mostly **9% voxel keep**, not a unique column curse: at matched keep, point 10% Δ = 0.084 vs 8 columns 0.064. Point 10/20/30% never flips ranking. Four columns (keep 0.044) still have Δ = 0.013 [0.006, 0.022]. Lead-2 reverts to climatology.  
3. Therefore the paper reports **conditional ranking**, not “MaskView-ST beats Linear everywhere.” Fair ocean persist is **not** invariant to the mask; unmasked persist was an implementation artifact.
