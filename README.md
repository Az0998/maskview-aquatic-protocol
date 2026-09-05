# Mask-View 插值可行性证书（湖泊水质）

> **一句话：** 用指标 ρ 判断「线性插值能不能用」；错误插补会翻转低氧 / 总氮预警效果。个人兴趣自学项目，尚无导师指导；EMS 审稿中，**尚未录用**。

**仓库：** https://github.com/Az0998/maskview-aquatic-protocol  
**作者：** 张森捷（Senjie Zhang），兰州大学（`3079099853@qq.com`）

| 项目 | 说明 |
|------|------|
| 数据 | 滇池公开自动站水质（块状缺失为主） |
| 方法 | Mask-View 缺失模式库 + ρ 证书 + 下游 DO/TN 预警 CSI |
| 复现 | 冻结表在 `data/frozen/`，一键脚本见下方 |
| 手稿 | `paper/EMS_interpolability_certificate_manuscript.docx` |

---

# Mask-View interpolability certificate

Standalone repository for **Paper A**. Clone and run — frozen tables live in `data/frozen/`.

**Target journal:** *Environmental Modelling & Software*  
**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

A mask-only interpolability certificate ρ states when linear interpolation is admissible. Deploying Linear because an MCAR or week-gap table said so changes DO-drop and TN-exceedance warning CSI when a sensor or station is dark. Lead-2 hypoxia F1 on a shelf oxygen cube prefers climatology under column-limited keep.

## Quick start

```bash
git clone https://github.com/Az0998/maskview-aquatic-protocol.git
cd maskview-aquatic-protocol
pip install -r requirements.txt
python scripts/build_cross_domain_tables.py
python scripts/plot_pattern_bank.py
python scripts/plot_rank_reversal.py
python scripts/plot_keep_ratio_tax.py
python scripts/plot_graphical_abstract.py
python scripts/build_ems_docx.py
```

## Layout

```
data/frozen/     locked lake + ocean result snapshots (including ρ, warning CSI, ocean deploy)
scripts/         tables, figures, EMS Word builder
results/         generated tables/figures
paper/           EMS manuscript pack; EcoInf/JHI Word files are archive only
docs/            GitHub Pages
```

Full training code remains in the experiment archives (`water-ai-do-forecast`, `ocean-do-forecast`) if you need to regenerate the frozen files. This repo is what you submit as the paper’s open synthesis.

## Manuscript

- Draft: `paper/manuscript_draft.md`
- Word (Elsevier EMS): `paper/EMS_interpolability_certificate_manuscript.docx`
- Cover letter: `paper/cover_letter_ems.docx` (`cover_letter_ems.txt`)
- Highlights: `paper/highlights.txt` / `paper/highlights.docx`
- Graphical abstract: `paper/figures/graphical_abstract.png`
- Upload checklist: `paper/SUBMISSION.md`
- Figures: `paper/figures/` (same files as `results/figures/`)

```bash
python scripts/build_cross_domain_tables.py
python scripts/plot_pattern_bank.py
python scripts/plot_rank_reversal.py
python scripts/plot_keep_ratio_tax.py
python scripts/plot_graphical_abstract.py
python scripts/build_ems_docx.py
```

Certificate and warning (engine repo `water-ai-do-forecast`):

```bash
python eval_interpolability_certificate.py
python eval_downstream_protocol.py
```

Ocean deploy table (no retrain):

```bash
python scripts/build_ocean_deploy_table.py
```

## License

MIT
