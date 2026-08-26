# Differentiation vs published Dianchi imputation (must be in Introduction)

**Neighbor paper (do not ignore):**  
Chen et al.–style tensor work, *Ecological Informatics* (2025)  
“Spatiotemporal water quality data reconstruction: A tensor factorization framework”  
doi:10.1016/j.ecoinf.2025.103283  

Same lake (Dianchi), missing reconstruction, strong numbers under **random 20–80% and 1–4 week gaps**.

| Axis | 2025 NTF ensemble | This protocol paper |
|------|-------------------|---------------------|
| Scientific object | A better reconstructor on Dianchi | Whether **evaluation missingness** changes method ranking |
| Missingness | Random rates + continuous week gaps | Operational bank: point / block_time / sensor / station / mixed (+ ocean Argo) |
| Second medium | No | East China Sea shelf oxygen, same bank |
| Claim | Lower RMSE/MAE/NSE vs SOTA | Linear wins short gaps; learned models recover sensor/station; MCAR misleads |
| Architecture | Biased nonnegative tensor factorization | MixHop ST as **one** learned imputer, not the sell |

If a reviewer says “Dianchi imputation is done,” the reply is: that paper optimized reconstruction error under random/gap missingness; we show **protocol-dependent ranking** on two aquatic media.
