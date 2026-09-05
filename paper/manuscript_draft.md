# An interpolability certificate for aquatic monitoring: when linear interpolation is admissible, and when the wrong mask changes hypoxia and nutrient warnings


**Journal:** *Environmental Modelling & Software* (backup: *Ecological Informatics*)  
**Article type:** Research Article  
**Authors:** Senjie Zhang¹,*  
**Affiliation:** ¹ Lanzhou University, Lanzhou 730000, Gansu, China  
**Correspondence:** 3079099853@qq.com  
**Code:** https://github.com/Az0998/maskview-aquatic-protocol  

Do not submit `ECOINF_MaskView_protocol_manuscript.docx` or `JHI_MaskView_protocol_manuscript.docx`. Rebuild with `python scripts/build_ems_docx.py`.

---

## Abstract

Automatic lake stations and column-limited oxygen products fail as blocks, not as scattered missing-completely-at-random (MCAR) holes. Reconstruction papers that hide only random cells or week-long gaps, including Wu et al. (2025) on Dianchi, therefore recommend linear interpolation in a regime that is interpolable by construction.

We compute an interpolability certificate ρ from the mask alone: a hidden cell is interpolable if the same station–variable still has an observed neighbour inside the evaluation window. On 15 Mask-View settings, ρ ≥ 0.5 matches a Linear win on the frozen 105-grid exactly (15/15). Point and block-time have ρ ≈ 1.0; sensor and station have ρ = 0. The Wu et al. random and week-gap banks have ρ ≥ 0.998, which is why Linear wins all eight of those settings.

The certificate is not only a ranking rule. If a manager deploys Linear because an MCAR or week-gap table said so, DO-drop and TN-exceedance warnings collapse on the cells that were actually hidden: CSI = 0 under sensor and station masks. BRITS recovers TN CSI to 0.72 (sensor) and 0.74 (station). On point holes, Linear remains the warning champion (DO CSI 0.80 versus BRITS 0.69). On a shelf oxygen cube, lead-1 still prefers a Transformer, but lead-2 hypoxia F1 prefers climatology except under block-time gaps.

The reusable product is the certificate and the warning test. Compute ρ before replacing Linear, and score the alarm on the cells the mask hid.

**Keywords:** interpolability; missing data; dissolved oxygen; early warning; aquatic monitoring; Mask-View

---

## 1. Introduction

Lake and coastal managers now rely on automatic sensors to watch eutrophication, hypoxia, and bloom-related chemistry at sub-daily resolution. The operational need is a usable dissolved-oxygen (DO) and nutrient series for reconstruction and warning, not a leaderboard mean absolute error (MAE). Dianchi Lake is a well-studied plateau eutrophic system in Yunnan, China [14,22,23]. Coastal oxygen decline is a parallel management problem [5,24]. Both problems fail as structured missingness [1,2].

Instruments go offline for hours to days. A single parameter channel dies. A whole station or a profile column disappears. On the open Dianchi automatic high-frequency monitoring (AHFM) release the natural missing rate on a regular 4 h grid is 19.8% [3]. Of those missing cells, 96.9% occur while the entire station is silent. Isolated one-step holes are 0.6%. Station-outage lengths are heavy-tailed (cell-weighted median 3.5 days). Coastal oxygen products face the complementary geometry: biogeochemical profiles sample the interior as sparse columns, not as a dense cube [4].

Published reconstruction banks do not match that geometry. Wu et al. [10] reconstructed Dianchi water-quality fields with biased nonnegative tensor factorization under random 20–80% holes and 1–4 week gaps, reporting strong RMSE, MAE and Nash–Sutcliffe scores. We score linear interpolation, last observation carried forward (LOCF), and a MixHop recipe [11] under that bank: Linear wins all eight settings. The same Linear model has standardised MAE ≈ 0.68–0.70 when a sensor or a station is dark for the whole 6-day window. That published bank never left the interpolable regime. A manager who trusts that bank will deploy Linear into the failure mode that already dominates the archive.

The informatics advance is an interpolability certificate. For each artificially hidden cell we ask only whether the same station–variable still has an originally observed, still-visible neighbour in the window. The fraction of such cells is ρ. ρ is computed from the mask. It does not require training seven models. We show that ρ ≥ 0.5 recovers every Linear win on a 7 × 5 × 3 Dianchi grid, and that ρ = 0 on sensor and station is exactly where Linear’s warning CSI falls to zero.

A second medium tests whether the same named bank changes a forecast deployment. On an East China Sea shelf oxygen cube, a spatiotemporal Transformer [12] remains first at one-month lead after fair masked persistence is scored, but lead-2 hypoxia F1 prefers climatology under column-limited history.

Contributions: (1) a mask-only certificate that states when Linear is admissible; (2) a dual-protocol table that explains Wu et al. [10] as an interpolable bank; (3) a warning-decision table: deploying Linear versus BRITS [6] changes CSI on the hidden cells; (4) an ocean deploy rule at lead-1 versus lead-2.

Boundary: the ocean cube is World Ocean Atlas (WOA)–informed development oxygen, not GOBAI-O2 [4]. Transfer to another lake requires recomputing ρ, not copying MixHop weights. We do not invent a reconstructor that beats BRITS on station blackout.

---

## 2. Materials and methods

### 2.1 Scientific object

The object of inference is a decision rule under a named missingness bank: is Linear admissible, and does the wrong admission change a warning? Lake MAE and ocean RMSE are not on the same scale. We compare winner identity inside each medium, the interpolability scalar that predicts that identity, and warning skill on the cells the mask actually hid.

### 2.2 Pattern bank

For each evaluation window we hide originally observed cells with one named pattern (Table 1). Naturally missing cells are never hidden and never scored. Lake evaluation hide rates are r ∈ {0.10, 0.20, 0.30} with seed 42.

Lake hide algorithms. point: MCAR on observed cells. block_time: downtime slabs of 3–12 steps (12–48 h). sensor: drop 1 or 2 variables at all stations and times in the window. station: drop 1–3 whole stations for the entire window. mixed: half point and half block_time, with probability 0.5 also a lighter station drop.

Ocean hide algorithms apply to oxygen history only (H = 12 months). Physics channels stay visible. Default keep_ratio = 0.25; default n_stations = 8. point: Bernoulli keep per voxel, broadcast over H (keep ≈ 0.25). block_time: a spatial block hidden for a contiguous time slab (keep ≈ 0.45). sensor: keep one of five depth layers (keep 0.20). station: eight water columns (keep 0.089). argo: Yangtze-section proxy of 7 grid cells (keep 0.078); not live Argovis.

### 2.3 Lake study system

Lake Dianchi (Kunming, Yunnan) [14,22,23]. Dianchi-Water [3], CC BY 4.0, 22 automatic stations, 1 January 2022 – 30 December 2024. Nine variables: TEM (°C), pH, DO (mg L−1), CON (µS cm−1), NTU, IMN (mg L−1), NH3-N, TP, TN (mg L−1). Chlorophyll-a and phycocyanin excluded (>87% missing). Cadence 4-hourly. After reindex: T = 6,568 × 22 × 9 = 1,300,464 cells, 19.8% missing. GPS withheld; spatial models use the released Haversine matrix. Source: CNEMC [15]. Sentinel remap (−1/−2/−3 → NaN). Split-wise missing rates: 25.7% / 13.0% / 14.3%.

### 2.4 Lake windows and score

Windows L = 36 steps (6 days), stride 18. 180 / 60 / 120 train / validation / test windows. Chronological split: train ≤ 30 June 2023; validation July–December 2023; test 2024. Standardization fit on training observed cells. Evaluation mask E: originally observed then hidden. Primary score: pooled standardized MAE on E.

Simple baselines: Mean, LOCF, Linear (pandas interpolate, both directions, per station–variable). Learned: SAITS, BRITS, GRIN* (StemGNN stand-in), MaskView-ST (MixHop + temporal attention). Default grid: 7 models × 5 patterns × 3 rates = 105 settings. Recipe spatial_plus_l0 is a sensitivity, not a second official winner.

### 2.5 Interpolability certificate

Let E be originally observed cells that are hidden. Cell (t, n, d) ∈ E is interpolable if there exists t′ ≠ t in the same window with (t′, n, d) originally observed and still visible. ρ = |interpolable| / |E|. Linear is declared admissible if ρ ≥ 0.5. Both-sides interpolability (a visible time strictly before and after t) is reported as a diagnostic, not as the decision threshold. ρ is computed from masks only (`eval_interpolability_certificate.py`).

### 2.6 Dual-protocol and year-shift

Wu et al. [10] bank: random 20/40/60/80% of observed cells and independent contiguous 1–4 week gaps on the 2024 panel. Linear and LOCF see the full panel; MixHop sees stitched 6-day windows. Year-shift: copy another year’s missing calendar onto 2024 cells that were observed (2022→2024 hides 10.52%; 2023→2024 hides 3.46%), plus an MCAR control at the same count.

### 2.7 Warning decision

On 2024 test windows, hide at rate 0.20 under point, sensor, and station. Impute with Linear, LOCF, cross-site spatial mean, and BRITS (PyPOTS, 8 epochs, trained once on train windows). Labels from originally observed values: DO drop ≥ 2 mg L−1 within 24 h; TN ≥ 2 mg L−1. Score only times whose warning window overlaps an artificially hidden target cell (DO: 24 h window overlaps a hidden DO cell; TN: hidden TN cells only). CSI = TP / (TP+FP+FN). Frozen in `downstream_protocol_warning.csv`.

### 2.8 Ocean study system, task, and deploy rule

Domain 118–128°E, 26–35°N; depths {10, 50, 100, 200, 500} dbar; 9 × 10 × 5 grid, 450 water voxels; monthly 2004–2022. Oxygen is a WOA18-informed development field, not GOBAI-O2. Task: 12-month history → 1-, 2- and 3-month forecast. Split by target month: train ≤ 2018; validation 2019–2020; test ≥ 2021 (n = 22). Fair sparse baselines: persist_locf, linear_time, spatial_linear; climatology does not need recent oxygen. Low-oxygen F1 uses a tenth-percentile threshold on this cube (195.09 µmol kg−1). Uncertainty: paired month-block bootstrap, 200 resamples [17,18].

Deploy rule (frozen ablation, no retrain): deploy Transformer at lead-1 if ST RMSE < climatology. At lead-2, deploy climatology when its hypoxia F1 is at least that of the Transformer, except block_time (hybrid).

### 2.9 Reproducibility

Headline tables are frozen CSV snapshots. Reviewer path without GPU: clone the synthesis repository; `python scripts/build_cross_domain_tables.py`; `python scripts/build_ems_docx.py`. Seed 42. Lake source: Hugging Face `anonymous-dianchi-2026/dianchi-water`. Optional GPU: `eval_interpolability_certificate.py` (CPU); `eval_downstream_protocol.py` (BRITS, CUDA). Ocean engine: `ocean-do-forecast`.

---

## 3. Results

### 3.1 How sensors actually fail

On Dianchi, 96.9% of naturally missing cells occur during full-station silence. Isolated one-step holes are 0.6%. Sensor-length gaps (≥1 day on a subset of variables) are 1.9%. A benchmark that only injects point holes is testing a minority failure mode.

### 3.2 Interpolability certificate predicts the Linear win

Mask-View point and block-time have ρ ≈ 0.9999; mixed ρ ≈ 0.88; sensor and station ρ = 0. EcoInf random mean ρ = 0.999; week-gap ρ = 1.0. Linear-admissible (ρ ≥ 0.5) matches Linear wins on 15/15 Mask-View settings. Sensor@20% MAE winner is MaskView-ST, but Linear remains forbidden (ρ = 0), so the certificate still separates Linear-legal from Linear-illegal.

### 3.3 Supporting MAE ranking

Linear wins point (0.161), block-time (0.254) and mixed (0.264). BRITS wins sensor (0.430) and station (0.435). A pooled mean MAE would have ranked MaskView-ST first (0.388 versus Linear 0.411) and hidden the reversal. The Wu et al. [10] bank does not produce this reversal: Linear remains first at random 20–80% and at 1–4 week gaps. Year-shift 2022→2024: Linear MAE 0.383 versus MCAR 0.168 at the same count; Linear still wins. Ranking reversal appears only when the evaluation window has no temporal neighbours.

### 3.4 Warning CSI flips when Linear is forbidden

At hide rate 0.20, scored only on imputation-dependent decisions:

| Pattern | Task | Linear CSI | BRITS CSI | Flip |
|---|---|---|---|---|
| point | DO drop | 0.798 | 0.687 | no |
| point | TN exceed | 0.948 | 0.733 | no |
| sensor | DO drop | 0.000 | 0.200 | yes |
| sensor | TN exceed | 0.000 | 0.720 | yes |
| station | DO drop | 0.000 | 0.208 | yes |
| station | TN exceed | 0.000 | 0.736 | yes |

On point holes Linear is the warning champion. On sensor/station Linear CSI is identically zero because no in-window neighbour exists. BRITS recovers TN exceedance; DO-drop recall under station blackout is still only 0.24 (CSI 0.21). Spatial mean can exceed BRITS on station DO CSI (0.337) as a transparent cross-site borrow; the official operational model on the 105-grid remains BRITS.

### 3.5 Ocean deploy rule

Lead-1: Transformer on every pattern, including station (keep 0.089; RMSE 5.23 versus climatology 5.30). Lead-2 hypoxia F1 prefers climatology on point, sensor, station, mixed and argo (F1 0.719 versus ST 0.68–0.69). block_time remains hybrid.

---

## 4. Discussion

The certificate is the transferable object. Another AHFM network can compute ρ on its own masks and decide whether Linear is legal before fitting BRITS. Wu et al. [10] remain the accuracy neighbour; their bank has ρ = 1 on week gaps, so Linear must win. That is not a criticism of tensor factorization. It is a statement about the hide design. The two papers are complementary: theirs reports reconstruction skill inside an interpolable bank; this paper states when that bank is the wrong one to trust for deployment.

Warning CSI is the management object. MAE ranking and warning ranking agree on the qualitative split (Linear on point; learned or cross-site on station), but recovering a 24 h DO drop when the whole site is dark is harder than recovering TN exceedance. We report BRITS DO CSI ≈ 0.21 under station blackout; we do not hide it.

Ocean lead-2 is a second decision flip: dense-history Transformer skill is not a licence to replace climatology at two-month lead under Argo-like keep.

Failed cases: year-shift calendars tax Linear but do not reverse ranking; MixHop does not close the station gap to BRITS; 0.06 µmol kg−1 is signed but small; the ocean cube is WOA-informed, not GOBAI; the ρ = 0.5 threshold was sufficient here and must be re-checked on another lake; BRITS warning is an 8-epoch reuse, not a tuned operational system. We did not add a second lake. Transfer copies the certificate, then re-scores local baselines.

---

## 5. Conclusions

Missingness protocol is part of the scientific claim because it changes who is allowed to interpolate and who should raise a hypoxia or nutrient alarm. Compute ρ before claiming that a learned model replaces Linear, and score the alarm on the cells the mask actually hid.

---

## Software availability

Name: Mask-View interpolability certificate. Developer: Senjie Zhang (`3079099853@qq.com`). Year: 2026. Language: Python. License: MIT. Cost: free. CPU for ρ and frozen tables; optional GPU for BRITS warning. https://github.com/Az0998/maskview-aquatic-protocol

---

## Data availability

Frozen tables: https://github.com/Az0998/maskview-aquatic-protocol  
Lake engine: https://github.com/Az0998/dianchi-maskview-imputation  
Ocean engine: https://github.com/Az0998/ocean-do-forecast  
Dianchi-Water: https://huggingface.co/datasets/anonymous-dianchi-2026/dianchi-water (CC BY 4.0)
