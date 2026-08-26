# Mask-View aquatic missingness protocol

Standalone repository for **Paper A**. Clone and run — frozen tables live in `data/frozen/`.

[![pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://az0998.github.io/maskview-aquatic-protocol/)

**Target journal:** *Journal of Hydroinformatics*  
**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

Operational block missingness changes which imputer/forecaster wins. This is a **protocol paper**, not a new architecture.

## Quick start

```bash
git clone https://github.com/Az0998/maskview-aquatic-protocol.git
cd maskview-aquatic-protocol
pip install -r requirements.txt
python scripts/build_cross_domain_tables.py
python scripts/plot_rank_reversal.py
```

## Layout

```
data/frozen/     locked lake + ocean result snapshots
scripts/         rank-reversal tables and figure
results/         generated tables/figures
paper/           JHI outline + EcoInf-2025 differentiation
docs/            GitHub Pages
```

Full training code remains in the experiment archives (`water-ai-do-forecast`, `ocean-do-forecast`) if you need to regenerate the frozen files. This repo is what you submit as the paper’s open synthesis.

## License

MIT
