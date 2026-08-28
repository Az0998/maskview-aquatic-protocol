# JHI upload pack

IWA *Journal of Hydroinformatics* · Research paper  
Upload at the IWA online submission system. Do not mention prior rejections.

## Ready files (this folder)

Copy these into the journal portal:

| Portal field | File |
|--------------|------|
| Manuscript | `JHI_MaskView_protocol_manuscript.docx` |
| Cover letter | `cover_letter_jhi.docx` (text twin: `cover_letter_jhi.txt`) |
| Highlights (if asked) | `highlights.txt` |
| Figure 1 | `figures/fig_maskview_pattern_bank.png` |
| Figure 2 | `figures/fig_keep_ratio_tax.png` |
| Figure 3 | `figures/fig_rank_reversal_two_media.png` |

Figures are already embedded in the Word file. Upload the PNGs again only if the portal requires separate artwork.

## Portal metadata

- **Title:** Operational missingness reverses method rankings in aquatic monitoring networks: a Mask-View protocol on a lake station grid and a shelf oxygen cube
- **Article type:** Research paper
- **Author:** Senjie Zhang (corresponding)
- **Affiliation:** Lanzhou University, Lanzhou 730000, Gansu, China
- **Email:** 3079099853@qq.com (use an institutional address if you have one)
- **Keywords:** missing data; water quality; dissolved oxygen; graph neural network; hydroinformatics; Mask-View; automatic monitoring; East China Sea; Dianchi Lake
- **Data:** https://github.com/Az0998/maskview-aquatic-protocol · https://huggingface.co/datasets/anonymous-dianchi-2026/dianchi-water (CC BY 4.0, public)
- **Suggested reviewers:** hydroinformatics / missing-data / automatic monitoring. Avoid physical oceanography of ECS fronts.

## Checks already done

- Word rebuilt from frozen CSVs (6 tables, 3 figures). Stale claim “persist/clim invariant to the mask” is gone; remaining “invariant” is “invariant by construction.”
- Hugging Face Dianchi dataset is public under CC BY 4.0 (19.8% missing, 22 stations, 2022–2024).
- 105-grid sensor winner is BRITS; recipe 0.421 vs 0.430 is not claimed as a finding.
- Keep scan and paired bootstrap are in the Word Results.

## Do not upload

- `manuscript_draft.md` (working source, not IWA format)
- Engine checkpoints, WOA NetCDFs, or Paper B
- Any cover letter that mentions Water / HSJ / previous decisions
