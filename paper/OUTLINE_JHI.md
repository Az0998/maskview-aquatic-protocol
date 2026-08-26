# Paper A outline (Journal of Hydroinformatics)

**Working title:** Operational missingness reverses imputer rankings in aquatic monitoring networks: a Mask-View protocol on a lake station grid and a shelf oxygen cube

## Abstract skeleton

1. Automatic stations and Argo-like profiles fail as blocks, not MCAR.  
2. We define a shared pattern bank and score **ranking**, not a universal winner.  
3. Dianchi: Linear wins point/block/mixed; learned models recover sensor dropout.  
4. ECS oxygen: dense-history Transformer is best at lead-1; Argo/station columns raise RMSE ~35%; lead-2 often reverts to climatology.  
5. Implication: hydroinformatics benchmarks that only inject random holes mislead operations.

## Sections

1. Introduction — Water/HSJ-class “case study” failure; 2025 EcoInf NTF as reconstruction neighbor.  
2. Protocol — table in PROTOCOL.md.  
3. Testbed A — Dianchi (cite sibling methods; 105 settings).  
4. Testbed B — ECS Mask-View ablation (lead-1/2, F1).  
5. Rank reversal — one figure, two media.  
6. Discussion — when not to use GNN; station gap vs BRITS; WOA-informed cube limitation.  
7. Open code — two GitHub repos + this synthesis repo.

## Cover-letter sentence

We are not submitting a new sequence model. We submit a missingness protocol whose ranking conclusions hold on an inland automatic network and a coastal oxygen cube.
