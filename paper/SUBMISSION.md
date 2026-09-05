# Final EMS upload checklist (1 Sep 2026)

**Journal:** *Environmental Modelling & Software*  
**Portal:** https://www.editorialmanager.com/envsoft/  
**Article type:** Research Article  
**Rebuild:** `py -3.12 scripts/plot_pattern_bank.py` then `plot_rank_reversal.py`, `plot_keep_ratio_tax.py`, `plot_graphical_abstract.py`, `build_ems_docx.py`

## Files to upload

| Item | File |
|---|---|
| Manuscript | `paper/EMS_interpolability_certificate_manuscript.docx` |
| Cover letter | `paper/cover_letter_ems.docx` |
| Highlights (required, 3–5 × ≤85 chars) | `paper/highlights.docx` and `paper/highlights.txt` |
| Graphical abstract (encouraged, ≥531×1328 px) | `paper/figures/graphical_abstract.png` |
| Fig. 1 | `paper/figures/fig_maskview_pattern_bank.png` |
| Fig. 2 | `paper/figures/fig_keep_ratio_tax.png` |
| Fig. 3 | `paper/figures/fig_rank_reversal_two_media.png` |

Do **not** upload `ECOINF_MaskView_protocol_manuscript.docx`, `JHI_MaskView_protocol_manuscript.docx`, or any letter that mentions a prior rejection.

## Portal fields (typical)

- Title: An interpolability certificate for aquatic monitoring: when linear interpolation is admissible, and when the wrong mask changes hypoxia and nutrient warnings
- Short title: Interpolability certificate for aquatic missingness
- Authors: Senjie Zhang (corresponding), Lanzhou University, 3079099853@qq.com
- Abstract: paste from the Word Abstract (single paragraph OK)
- Keywords: interpolability; missing data; dissolved oxygen; early warning; aquatic monitoring; Mask-View
- Funding: none
- Competing interests: none
- Data availability: GitHub + Hugging Face CC BY 4.0 (see manuscript)
- Suggested reviewers: leave blank unless you have names

## Cover letter rule

Criterion + decision + software. No rejection history.

## Gate (passed)

ρ 15/15; warning CSI flip on sensor/station; ocean deploy table; claim is the certificate, not “we are not a new architecture.”
