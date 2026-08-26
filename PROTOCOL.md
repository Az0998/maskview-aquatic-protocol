# Unified Mask-View pattern bank

Shared names. Construction differs by medium; evaluation question is the same:
**does the ranking of simple vs learned methods flip when missingness is operational rather than MCAR?**

| Pattern | Lake automatic station | Shelf oxygen (history cube) |
|---------|------------------------|-----------------------------|
| `point` | MCAR on observed cells | Random keep on O₂ grid |
| `block_time` | Consecutive downtime slab | Time slab × spatial block |
| `block` | (covered by block_time) | Spatial patch, all depths |
| `sensor` | Drop 1–2 variables | Hide selected O₂ channels/depths; physics stays |
| `station` | Whole station blackout | Column-limited stations |
| `mixed` | Point + block (± station) | Compound of the above |
| `argo` | n/a | Profile-like columns (operational analog of station) |
| `none` | n/a (natural ~19.8% already) | Dense O₂ history (upper bound) |

## Metrics (do not mix units)

Lake metrics stay **standardized MAE**. Ocean metrics stay **RMSE (µmol kg⁻¹)** and hypoxia F1.  
The comparable scientific object is **winner identity** and **skill degradation vs the easy-gap winner**.

## Rank-reversal hypothesis

1. Easy gaps (`point`, short `block_time`): Linear / LOCF (lake) or dense ST (ocean lead-1) win or stay close.  
2. Hard gaps (`sensor`, `station`, `argo`): temporal interpolators collapse (lake); lead-1 ST degrades toward climatology at lead-2 (ocean).  
3. Therefore the paper reports **conditional ranking**, not “MaskView-ST beats Linear everywhere.”
