# Operational missingness reverses method rankings in aquatic monitoring networks: a Mask-View protocol on a lake station grid and a shelf oxygen cube

**Journal:** *Journal of Hydroinformatics* (IWA)  
**Article type:** Research paper  
**Authors:** Senjie Zhang¹,*  
**Affiliation:** ¹ Lanzhou University, Lanzhou 730000, Gansu, China  
**Correspondence:** 3079099853@qq.com  
**Code:** https://github.com/Az0998/maskview-aquatic-protocol  

---

## Abstract

Automatic water-quality stations and biogeochemical profiles rarely fail as scattered missing-completely-at-random (MCAR) holes. They fail as downtime slabs, dropped parameters, and station or Argo-column blackouts. Benchmarks that hide only random cells therefore overstate the value of local temporal interpolators and of models trained on dense history. We introduce a shared **Mask-View** pattern bank—point, block_time, sensor, station, mixed, and an Argo-column analog—and score **who wins**, not a universal error. On the Dianchi 22-station, 9-variable, 4-hourly panel (2022–2024), linear interpolation attains the lowest standardized MAE on point (0.161), block_time (0.254) and mixed (0.264) gaps, but collapses to ≈0.68–0.70 under sensor and station outages, where BRITS and a MixHop spatiotemporal imputer recover. On an East China Sea shelf dissolved-oxygen cube, a spatiotemporal Transformer is best at one-month lead under dense history (RMSE 3.88 µmol kg⁻¹ versus climatology 5.30). The same model remains first at lead-1 under operational masks, but RMSE rises 10–35%; persistence (8.26) and climatology (5.30) are invariant to history sparsity, and lead-2 skill reverts to climatology except for block_time. The transferable result is a protocol: MCAR rankings are not operational rankings. Hydroinformatics papers should report an operational pattern bank before claiming that a learned model replaces linear interpolation or climatology.

**Keywords:** missing data; water quality; dissolved oxygen; graph neural network; hydroinformatics; Mask-View; automatic monitoring; East China Sea; Dianchi Lake

---

## 1. Introduction

High-frequency aquatic monitoring is now limited less by sampling design than by **structured missingness**. Instruments go offline for hours to days; a single parameter channel dies; a whole station or profile column disappears. On the open Dianchi automatic-station release the natural missing rate on a regular 4 h grid is about 19.8% and is predominantly block-structured. Ocean oxygen products face the complementary problem: biogeochemical Argo profiles sample the interior as sparse columns, not as a dense cube.

Deep imputers such as BRITS (Cao et al. 2018) and SAITS (Du et al. 2023), graph models (Cini et al. 2022), and tensor reconstructions have improved generic completion. A 2025 *Ecological Informatics* study reconstructed Dianchi water-quality fields with biased nonnegative tensor factorization under random 20–80% holes and 1–4 week gaps, reporting strong RMSE/MAE/NSE (doi:10.1016/j.ecoinf.2025.103283). That paper answers “which reconstructor is most accurate on Dianchi under random/gap missingness?” It does not ask whether **the ranking itself** depends on the missingness mechanism, nor whether the same protocol travels to a second aquatic medium.

Editors of international water journals routinely desk-reject single-site machine-learning applications that use standard architectures without a transferable question. The present paper is written against that failure mode. We do **not** claim a new universal sequence model. We claim that an **operational Mask-View bank** changes method ranking on (i) an inland automatic network and (ii) a coastal oxygen forecast cube, and that MCAR-only tables mislead operations.

The contributions are:

1. A shared pattern dictionary mapping lake station failures onto shelf-oxygen masks, including an Argo-column analog.  
2. A rank-reversal evaluation: lake standardized MAE versus ocean RMSE/F1, compared only through **winner identity**.  
3. Evidence that linear interpolation dominates short lake gaps while collapsing on sensor/station outages, and that a shelf oxygen Transformer is taxed by history sparsity toward climatology at lead-2.

---

## 2. Methods

### 2.1. Protocol

For each window we hide originally observed cells with one of: **point** (MCAR), **block_time** (contiguous downtime), **sensor** (parameter or depth-channel dropout), **station** (site or column outage), **mixed**, and for the ocean cube **argo** (profile-like columns) and **none** (dense-history upper bound). Training, where applicable, samples complementary views; evaluation uses fixed patterns. Details of mask construction differ by medium (Table 1 in `PROTOCOL.md`); the scientific question does not.

### 2.2. Lake testbed

Dianchi-Water: 22 stations, nine variables (TEM, pH, DO, CON, NTU, IMN, NH3-N, TP, TN), 4-hourly, 2022–2024. Windows of length 36 (6 days). Temporal split: train to 30 June 2023, validation 2023 H2, test 2024. Baselines: Mean, LOCF, Linear (per station–variable), SAITS, BRITS, StemGNN as GRIN*, and MaskView-ST (MixHop graph + temporal attention). The recommended recipe `spatial_plus_l0` uses denser k-NN (k = 8), mask-aware aggregation, station-pattern upsampling and consistency weight λ = 0. Metrics: standardized MAE on artificially hidden, originally observed cells.

### 2.3. Ocean testbed

East China Sea shelf dissolved-oxygen cube with WOA-informed development oxygen and physical drivers (temperature, salinity, stratification, OISST, 10 m wind). Task: 12-month history → 1–3 month forecast. Models: persistence, month-of-year climatology, LSTM anomaly, spatiotemporal Transformer, hybrid climatology–Transformer. Masks are applied to **oxygen history**; physics channels remain visible. Because persistence and climatology do not ingest the masked history cube, their lead-1 RMSE is **invariant** to the Mask-View pattern (8.26 and 5.30 µmol kg⁻¹). That invariance is the ocean analog of a simple operational fallback: climatology does not need dense recent oxygen. The learned Transformer does.

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
| sensor | 0.696 | 0.441 | **0.421** | 0.430 | BRITS (recipe beats Linear) |
| station | 0.679 | 0.539 | 0.540 | **0.435** | BRITS |

Linear wins 9 of 15 individual rate settings; BRITS wins 5 (all sensor/station); MaskView-ST wins 1. The `spatial_plus_l0` recipe improves sensor MAE to 0.421 (ahead of BRITS 0.430) while the station gap to BRITS remains (~0.105). Point-only training (ablation) is excellent on MCAR and collapses on sensor/station—direct evidence that the pattern bank is necessary.

### 3.2. Ocean: learned skill is taxed by history sparsity

Lead-1 RMSE (µmol kg⁻¹):

| Pattern | Persistence | Climatology | ST Transformer | ST vs dense |
|---------|------------:|------------:|---------------:|------------:|
| none (dense) | 8.27 | 5.30 | **3.88** | — |
| block_time | 8.27 | 5.30 | **4.27** | +10% |
| point | 8.27 | 5.30 | **5.02** | +29% |
| sensor | 8.27 | 5.30 | **5.08** | +31% |
| station / argo | 8.27 | 5.30 | **5.23 / 5.24** | +35% |

At lead-1 the Transformer still beats climatology under every mask. At lead-2 the best model is climatology or a hybrid except for block_time. Low-oxygen F1 falls from 0.74 (dense) to 0.67 (argo). Operational sparsity therefore does not invert lead-1 ranking against climatology, but it **erodes the learned advantage** and hands longer leads back to climatology—the forecast analog of “do not replace the simple method everywhere.”

### 3.3. Cross-media protocol message

Easy lake gaps reward Linear; hard lake gaps reward cross-variable/spatial models. Dense ocean history rewards a Transformer; Argo-like history taxes it toward a climatology fallback at lead-2. A benchmark that only injects point holes would have declared Linear (lake) or dense ST (ocean) sufficient and would have missed the operational failure modes.

Figures: `results/figures/fig_maskview_pattern_bank.png` (pattern bank); `results/figures/fig_rank_reversal_two_media.png` (rankings).

---

## 4. Discussion

The 2025 Dianchi tensor paper remains the reconstruction accuracy neighbor; we differ in **question** (ranking under operational masks; two media). MixHop capacity does not close the lake station-outage gap to BRITS, which mixes flattened cross-station channels more aggressively than a local graph—an informative limitation, not a result to hide.

Ocean oxygen here is a WOA-informed development cube, not GOBAI-O2 time-varying oxygen. Conclusions about ranking under masks still hold as a protocol demonstration; process-level frontal claims are out of scope.

We recommend that hydroinformatics studies (i) publish the pattern bank, (ii) keep Linear/climatology as first-class baselines, and (iii) report winner identity by pattern rather than a single mean score.

---

## 5. Conclusions

Mask-View is an evaluation and training protocol for operational aquatic missingness. On Dianchi it shows when not to prefer a GNN over linear interpolation; on the ECS shelf it shows when a Transformer’s dense-history advantage is taxed back toward climatology. The paper’s general significance is that **missingness protocol is part of the scientific claim**.

---

## Data availability

Lake tables: frozen snapshots in this repository (`data/frozen/lake`), sourced from the Dianchi Mask-View benchmark. Ocean tables: `data/frozen/ocean`. Experiment engines: https://github.com/Az0998/dianchi-maskview-imputation and https://github.com/Az0998/ocean-do-forecast. Dianchi open data: https://huggingface.co/datasets/anonymous-dianchi-2026/dianchi-water.

## References (core)

Cao et al. 2018. BRITS. NeurIPS.  
Du et al. 2023. SAITS. Expert Syst. Appl. 219, 119619.  
Cini et al. 2022. GRIN. ICLR.  
Spatiotemporal water quality data reconstruction: A tensor factorization framework. Ecol. Inform. 2025, 103283.  
CNEMC automatic monitoring data release.  
IWA. Journal of Hydroinformatics instructions for authors.
