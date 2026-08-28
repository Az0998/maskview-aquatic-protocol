# Differentiation vs published Dianchi imputation (must be in Introduction)

**Neighbor:** Wu X., Shan K., Wang L., Wang J. & Shang M. (2025). *Ecological Informatics* 90, 103283.  
“Spatiotemporal water quality data reconstruction: A tensor factorization framework”  
doi:10.1016/j.ecoinf.2025.103283

Same lake (Dianchi), missing reconstruction, strong numbers under **random 20–80% and 1–4 week gaps**.

| Axis | Wu et al. 2025 NTF ensemble | This protocol paper |
|------|-----------------------------|---------------------|
| Scientific object | A better reconstructor on Dianchi | Whether **evaluation missingness** changes method ranking |
| Missingness | Random rates + continuous week gaps | Operational bank: point / block_time / sensor / station / mixed (+ ocean Argo analog) |
| Second medium | No | East China Sea shelf oxygen, same bank |
| Claim | Lower RMSE/MAE/NSE vs SOTA | Linear wins interpolable banks; learned models recover Mask-View sensor/station; MCAR misleads |
| Architecture | Biased nonnegative tensor factorization | MixHop ST as **one** learned imputer, not the sell |

If a reviewer says “Dianchi imputation is done,” the reply is: that paper optimized reconstruction error under random/gap missingness; we show **protocol-dependent ranking** on two aquatic media.

## Direct test (same models, two banks)

`data/frozen/lake/ecoinf_dual_protocol.csv` — Linear / LOCF / spatial_plus_l0 under EcoInf missingness vs frozen Mask-View averages.

| Bank | Settings | Winner |
|------|----------|--------|
| EcoInf random 20–80% | 4 rates | **Linear** at every rate (0.160 → 0.242) |
| EcoInf 1–4 week gaps | 4 lengths | **Linear** at every length (0.285–0.402) |
| Mask-View point / block_time | pattern avg | **Linear** |
| Mask-View sensor | 105-grid | **BRITS** (0.430); recipe 0.421 is a 0.009 sensitivity, not a second winner |
| Mask-View station | 105-grid | **BRITS** (0.435); Linear 0.679 |

The neighbor’s missingness bank never leaves the interpolable regime. We did not reimplement NTF; the scientific object is ranking under their protocol vs ours.
