Frozen snapshots so this repository clones without sibling checkouts.

- `lake/` from `water-ai-do-forecast/results` (2026-08 Dianchi Mask-View grid + spatial_plus_l0 ablation)
  - `ecoinf_dual_protocol.csv` — same models under EcoInf random 20–80% and 1–4 week gaps vs operational bank
  - `natural_missing_taxonomy.csv` / `natural_missing_replay.csv` — 96.9% of holes are station-level; year-shift replay vs MCAR
- `ocean/` from `ocean-do-forecast/results/tables/`
  - `maskview_ablation.*` — ST/hybrid under 8 patterns (lead-1/2)
  - `ocean_simple_vs_learned.csv` — original persist/clim/ST (persist/clim **unmasked**)
  - `fair_sparse_baselines.csv` — persist_locf / linear_time / spatial_linear ingest the **same mask**
  - `maskview_keep_rates.csv` — effective voxel keep (station ~0.089, argo ~0.078, not lake 10/20/30%)
  - `st_clim_bootstrap.*` — paired month-block CI on lead-1 ST vs climatology (n=22, 200 boots)
  - `keep_ratio_scan.*` — point keep 10–50% vs station 4–24 columns; tax tracks voxel keep more than geometry
