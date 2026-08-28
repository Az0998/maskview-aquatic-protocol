# Operational missingness reverses method rankings in aquatic monitoring networks: a Mask-View protocol on a lake station grid and a shelf oxygen cube

**Journal:** *Journal of Hydroinformatics* (IWA)  
**Article type:** Research paper  
**Authors:** Senjie Zhang¹,*  
**Affiliation:** ¹ Lanzhou University, Lanzhou 730000, Gansu, China  
**Correspondence:** 3079099853@qq.com  
**Code:** https://github.com/Az0998/maskview-aquatic-protocol  
**Word manuscript (IWA/JHI):** `paper/JHI_MaskView_protocol_manuscript.docx`  
**Cover letter:** `paper/cover_letter_jhi.txt`  
**Highlights:** `paper/highlights.txt`  

---

## Abstract

Automatic water-quality stations and biogeochemical profiles rarely fail as scattered missing-completely-at-random (MCAR) holes. They fail as downtime slabs, dropped parameters, and station or Argo-column blackouts. Benchmarks that hide only random cells therefore overstate the value of local temporal interpolators and of models trained on dense history. We introduce a shared **Mask-View** pattern bank—point, block_time, sensor, station, mixed, and an Argo-column analog—and score **who wins**, not a universal error. On the Dianchi 22-station, 9-variable, 4-hourly panel (2022–2024), linear interpolation attains the lowest standardized MAE on point (0.161), block_time (0.254) and mixed (0.264) gaps, but collapses to ≈0.68–0.70 under sensor and station outages, where BRITS and a MixHop spatiotemporal imputer recover. On an East China Sea shelf dissolved-oxygen cube, a spatiotemporal Transformer is best at one-month lead under dense history (RMSE 3.88 µmol kg⁻¹ versus climatology 5.30). The same model remains first at lead-1 under operational masks, but RMSE rises 10–35% as effective voxel keep falls; the default station/section margin over climatology shrinks to ~0.06 mainly because those masks keep ~8–9% of voxels, not because column geometry uniquely inverts ranking (paired month-block 5–95% CI still excludes zero). Persistence scored on unmasked history is not a fair sparse baseline; last-observed persistence and temporal linear interpolation never beat climatology. Lead-2 skill reverts to climatology except for block_time. The transferable result is a protocol: MCAR rankings are not operational rankings. Hydroinformatics papers should report an operational pattern bank before claiming that a learned model replaces linear interpolation or climatology.

**Keywords:** missing data; water quality; dissolved oxygen; graph neural network; hydroinformatics; Mask-View; automatic monitoring; East China Sea; Dianchi Lake

---

## 1. Introduction

High-frequency aquatic monitoring is now limited less by sampling design than by **structured missingness**. Instruments go offline for hours to days; a single parameter channel dies; a whole station or profile column disappears. On the open Dianchi automatic-station release the natural missing rate on a regular 4 h grid is 19.8%. Of those missing cells, 96.9% occur while the entire station is silent; isolated one-step holes are 0.6%. Station-outage durations are heavy-tailed (cell-weighted median 3.5 days). Ocean oxygen products face the complementary problem: biogeochemical Argo profiles sample the interior as sparse columns, not as a dense cube.

Deep imputers such as BRITS (Cao et al. 2018) and SAITS (Du et al. 2023), graph models (Cini et al. 2022), and tensor reconstructions have improved generic completion. A 2025 *Ecological Informatics* study (Wu et al. 2025) reconstructed Dianchi water-quality fields with biased nonnegative tensor factorization under random 20–80% holes and 1–4 week gaps, reporting strong RMSE/MAE/NSE (doi:10.1016/j.ecoinf.2025.103283). That paper answers “which reconstructor is most accurate on Dianchi under random/gap missingness?” It does not ask whether **the ranking itself** depends on the missingness mechanism, nor whether the same protocol travels to a second aquatic medium. When we score our Linear / LOCF / MixHop imputers under that EcoInf bank, Linear wins all eight settings (random 20–80% MAE 0.160–0.242; 1–4 week gaps 0.285–0.402). The same Linear collapses on Mask-View sensor/station outages (MAE ≈ 0.68). The neighbor’s missingness therefore never left the interpolable regime.

Editors of international water journals routinely desk-reject single-site machine-learning applications that use standard architectures without a transferable question. The present paper is written against that failure mode. We do **not** claim a new universal sequence model. We claim that an **operational Mask-View bank** changes method ranking on (i) an inland automatic network and (ii) a coastal oxygen forecast cube, and that MCAR-only tables mislead operations.

The contributions are:

1. A shared pattern dictionary mapping lake station failures onto shelf-oxygen masks, including an Argo-column analog.  
2. A rank-reversal evaluation: lake standardized MAE versus ocean RMSE/F1, compared only through **winner identity**; plus a dual-protocol table showing Linear wins the EcoInf random/week bank and loses Mask-View sensor/station.  
3. Evidence that linear interpolation dominates short lake gaps while collapsing on sensor/station outages, and that a shelf oxygen Transformer is taxed by history sparsity toward climatology at lead-2, even after fair masked persistence and temporal interpolation are scored.

---

## 2. Methods

### 2.1. Protocol

For each window we hide originally observed cells with one of: **point** (MCAR), **block_time** (contiguous downtime), **sensor** (parameter or depth-channel dropout), **station** (site or column outage), **mixed**, and for the ocean cube **argo** (profile-like columns) and **none** (dense-history upper bound). Training, where applicable, samples complementary views; evaluation uses fixed patterns. Details of mask construction differ by medium (Table 1 in `PROTOCOL.md`); the scientific question does not.

### 2.2. Lake testbed

Dianchi-Water: 22 stations, nine variables (TEM, pH, DO, CON, NTU, IMN, NH3-N, TP, TN), 4-hourly, 2022–2024. Windows of length 36 (6 days). Temporal split: train to 30 June 2023, validation 2023 H2, test 2024. Baselines: Mean, LOCF, Linear (per station–variable), SAITS, BRITS, StemGNN as GRIN*, and MaskView-ST (MixHop graph + temporal attention). The recommended recipe `spatial_plus_l0` uses denser k-NN (k = 8), mask-aware aggregation, station-pattern upsampling and consistency weight λ = 0. Metrics: standardized MAE on artificially hidden, originally observed cells.

### 2.3. Ocean testbed

East China Sea shelf dissolved-oxygen cube with WOA-informed development oxygen and physical drivers (temperature, salinity, stratification, OISST, 10 m wind). Task: 12-month history → 1–3 month forecast. Models: persistence, month-of-year climatology, LSTM anomaly, spatiotemporal Transformer, hybrid climatology–Transformer. Masks are applied to **oxygen history**; physics channels remain visible. Spatial masks are constant across the 12-month window (except `block_time`), so a voxel is fully observed or never; lake 10/20/30% rates are not comparable (station keep ≈ 0.089, argo/section keep ≈ 0.078). Persistence and climatology in the original ablation did **not** ingest the masked cube; their RMSE was therefore invariant by construction. Fair counterparts scored here: last-observed persistence (LOCF) with climatology fill, per-voxel temporal linear interpolation, and horizontal interpolation of the LOCF field. Climatology remains a valid operational fallback because it does not need recent oxygen. The learned Transformer does. Uncertainty on the lead-1 ST–climatology gap uses a paired month-block bootstrap (n = 22 test months, 200 resamples) of Δ = RMSE_clim − RMSE_ST; we retrain ST with the ablation recipe (8 epochs) so the interval is internally consistent with the masked runs. The object of inference is the paired difference, not overlap of the two marginal RMSE intervals. Default `keep_ratio=0.25` is **not** lake 10/20/30%: we therefore scan point voxel keep at 0.10–0.50 and station column counts 4–24 (effective keep ≈ 0.044–0.267). Sensor is not scanned as a rate: with Z = 5, 10/20/25% all keep one depth layer.

### 2.4. What is comparable

Lake MAE and ocean RMSE are not on the same scale. We compare (i) which method wins inside each medium and (ii) whether operational masks flip that ranking relative to the easy-gap or dense-history case.

---

## 3. Results

### 3.1. Lake ranking is protocol-dependent

Pattern-averaged standardized MAE:

| Pattern | Linear | MaskView-ST | spatial_plus_l0 | BRITS | Winner (default grid) |
|---------|-------:|------------:|----------------:|------:|-----------------------|
| point | **0.161** | 0.297 | 0.295 | 0.430 | Linear |
| block_time | **0.254** | 0.326 | 0.313 | 0.442 | Linear |
| mixed | **0.264** | 0.339 | 0.334 | 0.433 | Linear |
| sensor | 0.696 | 0.441 | 0.421 | **0.430** | BRITS |
| station | 0.679 | 0.539 | 0.540 | **0.435** | BRITS |

Linear wins 9 of 15 individual rate settings; BRITS wins 5 (all sensor/station); MaskView-ST wins 1. A pooled mean MAE would have ranked MaskView-ST first (0.388 versus Linear 0.411) and hidden the reversal. The `spatial_plus_l0` recipe improves sensor MAE from the default MixHop 0.441 to 0.421, which is 0.009 below BRITS 0.430; we treat that as a sensitivity, not a second winner. The station gap to BRITS remains (~0.105). Point-only training (ablation) is excellent on MCAR and collapses on sensor/station—direct evidence that the pattern bank is necessary.

The EcoInf 2025 bank does not produce this reversal. On the same 2024 test windows, Linear remains first at random 20/40/60/80% (standardized MAE 0.160, 0.183, 0.209, 0.242) against LOCF and `spatial_plus_l0`. On full-panel 1–4 week contiguous gaps, Linear remains first (0.311, 0.285, 0.341, 0.402); the MixHop model, seeing only stitched 6-day windows, never overtakes it.

Naturally missing cells have no labels, so we replay another year’s outage calendar onto 2024 cells that were observed. Replaying 2022 (hide rate 10.5% of observed 2024 cells) yields Linear 0.383 versus MCAR at the same count 0.168; replaying 2023 (3.5%) yields 0.328 versus 0.147. Linear still wins both replays; `spatial_plus_l0` does not. Structure therefore **taxes** Linear relative to MCAR without flipping the winner. Ranking reversal appears only when the evaluation window itself has no temporal neighbors (Mask-View sensor/station). The calendar of real outages is interpolable along the year; the operational stress test is not a copy of median downtime, it is the case with no in-window support.

Ranking therefore depends on **which missingness bank is used**, not on swapping the lake.

### 3.2. Ocean: learned skill is taxed by history sparsity

Lead-1 RMSE (µmol kg⁻¹). Persistence (unmasked) is the original oracle last-month score and is **not** a sparse baseline. persist_locf uses only kept oxygen.

| Pattern | keep | persist_locf | clim | ST | ST vs dense | ST−clim |
|---------|-----:|-------------:|-----:|---:|------------:|--------:|
| none (dense) | 1.00 | 8.27 | 5.30 | **3.88** | — | −1.42 |
| block_time | 0.45 | 10.05 | 5.30 | **4.27** | +10% | −1.03 |
| point | 0.25 | 6.18 | 5.30 | **5.02** | +29% | −0.28 |
| sensor | 0.20 | 5.99 | 5.30 | **5.08** | +31% | −0.22 |
| station | 0.089 | 5.60 | 5.30 | **5.23** | +35% | −0.07 |
| argo (section) | 0.078 | 5.54 | 5.30 | **5.24** | +35% | −0.06 |

Temporal linear interpolation equals persist_locf under static spatial masks (last-month forecast only needs the endpoint). Horizontal interpolation of sparse columns is worse than persistence (RMSE 12–15). The competitive simple bar is therefore climatology, not persistence: persist_locf never beats 5.30. At lead-1 the Transformer still wins every pattern. At lead-2 the best model is climatology or a hybrid except for block_time. Low-oxygen F1 falls from 0.74 (dense) to 0.67 (argo). Argo and station differ by 0.009 µmol kg⁻¹ and share a column-limited geometry; argo here is a Yangtze-section proxy, not live Argovis.

The remaining station/section edge looks small enough to be noise if one only inspects overlapping marginal RMSE intervals (station ST 5.09–5.38 versus climatology 5.16–5.47). The paired difference is the right test: month-resampled Δ = clim − ST stays positive in all 200 replicates. Dense history Δ is 1.43 [1.34, 1.54]; point 0.30 [0.26, 0.34]; station 0.078 [0.064, 0.093]; argo/section 0.062 [0.051, 0.071]. Retrain RMSE tracks the locked ablation (station 5.220 vs 5.232; argo 5.235 vs 5.241).

That default table **confounds rate with geometry**: station keeps 0.089 of water voxels, point keeps 0.25. A keep scan (8-epoch recipe; `fig_keep_ratio_tax.png`) separates the two.

| Setting | keep | ST | Δ (clim−ST) | Δ 5–95% |
|---------|-----:|---:|------------:|---------|
| point 10% | 0.101 | 5.214 | 0.084 | [0.071, 0.098] |
| point 20% | 0.199 | 5.069 | 0.228 | [0.197, 0.267] |
| point 30% | 0.295 | 4.956 | 0.342 | [0.306, 0.394] |
| 4 columns | 0.044 | 5.284 | 0.013 | [0.006, 0.022] |
| 8 columns (default) | 0.089 | 5.233 | 0.064 | [0.054, 0.075] |
| 16 columns | 0.178 | 5.129 | 0.169 | [0.155, 0.184] |
| 24 columns | 0.267 | 4.963 | 0.335 | [0.304, 0.369] |

On point (the lake 10/20/30% analog) ST wins every rate. Matching voxel keep, columns are only modestly harsher (point 0.10 vs 8 columns: 0.084 vs 0.064; point 0.20 vs 16 columns: 0.228 vs 0.169). persist_locf never beats climatology. Operational sparsity therefore does not invert lead-1 ranking. It **taxes** the learned advantage mainly by how much oxygen history remains, secondarily by packing that history into columns, and it hands longer leads back to climatology. The residual ~0.06 µmol kg⁻¹ at the default 8-column mask is statistically signed on this window, not operationally large.

### 3.3. Cross-media protocol message

Easy lake gaps reward Linear; hard lake gaps reward cross-variable/spatial models. Real Dianchi outage calendars still rank Linear first but roughly double its MAE versus MCAR at the same hide rate. Dense ocean history rewards a Transformer; column-limited history does not let persist/linear steal the win—climatology is the simple bar. The published station vs point contrast (+35% vs +29% vs dense) is mostly that default station keeps ~9% of voxels versus point 25%; at matched keep, columns add only a small extra tax, and lake-like point 10/20/30% never flips lead-1 ranking. Lead-2 reverts to climatology. A benchmark that only injects point holes, or that scores persistence on unmasked history, would have missed both failure modes.

Figures: `results/figures/fig_maskview_pattern_bank.png` (pattern bank); `results/figures/fig_keep_ratio_tax.png` (ST–clim margin vs voxel keep); `results/figures/fig_rank_reversal_two_media.png` (rankings).

---

## 4. Discussion

The 2025 Dianchi tensor paper remains the reconstruction accuracy neighbor; we differ in **question** (ranking under operational masks; two media). MixHop capacity does not close the lake station-outage gap to BRITS, which mixes flattened cross-station channels more aggressively than a local graph—an informative limitation, not a result to hide.

Ocean oxygen here is a WOA-informed development cube, not GOBAI-O2 time-varying oxygen. Conclusions about ranking under masks still hold as a protocol demonstration; process-level frontal claims are out of scope. Unmasked persistence/climatology invariance must not be reported as a scientific finding; it follows from baselines that ignore the mask. After fair scoring, climatology remains the simple method to beat. The Transformer’s remaining lead-1 edge under the default 8-column mask is small (~0.06 µmol kg⁻¹) because that mask keeps ~9% of voxels, not because columns uniquely destroy skill. On n = 22 test months the paired bootstrap of Δ excludes zero down to 4 columns (Δ = 0.013 [0.006, 0.022]). That supports “still first” as a ranking statement on this window; it does not make 0.06 µmol kg⁻¹ an operationally large gain, and month exchangeability is an assumption of the block bootstrap. Lake 10/20/30% should be compared with ocean **point** keep, not with `keep_ratio=0.25` on station.

We recommend that hydroinformatics studies (i) publish the pattern bank, (ii) keep Linear/climatology as first-class baselines, and (iii) report winner identity by pattern rather than a single mean score.

---

## 5. Conclusions

Mask-View is an evaluation and training protocol for operational aquatic missingness. On Dianchi it shows when not to prefer a GNN over linear interpolation; on the ECS shelf it shows when a Transformer’s dense-history advantage is taxed back toward climatology. The paper’s general significance is that **missingness protocol is part of the scientific claim**.

---

## Data availability

Lake tables: frozen snapshots in this repository (`data/frozen/lake`), sourced from the Dianchi Mask-View benchmark. Ocean tables: `data/frozen/ocean`. Experiment engines: https://github.com/Az0998/dianchi-maskview-imputation and https://github.com/Az0998/ocean-do-forecast. Dianchi open data: https://huggingface.co/datasets/anonymous-dianchi-2026/dianchi-water (CC BY 4.0).

## Author contributions

S.Z. conceived the study, designed the Mask-View protocol, performed the analyses, and wrote the manuscript.

## References (core)

Cao et al. 2018. BRITS. NeurIPS.  
Du et al. 2023. SAITS. Expert Syst. Appl. 219, 119619.  
Cini et al. 2022. GRIN. ICLR.  
Wu X., Shan K., Wang L., Wang J. & Shang M. 2025. Ecol. Inform. 90, 103283.  
CNEMC automatic monitoring data release.  
IWA. Journal of Hydroinformatics instructions for authors.
