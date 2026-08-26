"""Figure 1: shared Mask-View bank on lake (node×var×time) and ocean (z×y×x)."""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from config import FIGURES


def lake_mask(kind: str, rng: np.random.Generator) -> np.ndarray:
    # (time, node×var)
    m = np.ones((18, 12), dtype=float)
    if kind == "point":
        m.ravel()[rng.choice(m.size, 50, replace=False)] = 0
    elif kind == "block_time":
        m[6:13, 3:8] = 0
    elif kind == "sensor":
        m[:, 9:11] = 0
    elif kind == "station":
        m[:, 4:7] = 0
    elif kind == "mixed":
        m.ravel()[rng.choice(m.size, 25, replace=False)] = 0
        m[8:12, 2:5] = 0
    return m


def ocean_mask(kind: str, rng: np.random.Generator) -> np.ndarray:
    # plan view (y, x); white = hidden
    m = np.ones((14, 18), dtype=float)
    if kind == "point":
        m.ravel()[rng.choice(m.size, 70, replace=False)] = 0
    elif kind == "block_time":
        m[4:10, 6:13] = 0
    elif kind == "sensor":
        m[:, :] = 1
        m[::2, :] = 0.35  # every other depth-row proxy
    elif kind == "station":
        m[:, :] = 0.15
        for j in (2, 7, 12, 16):
            m[:, j] = 1
    elif kind == "argo":
        m[:, :] = 0.12
        for i, j in ((2, 3), (5, 8), (9, 14), (11, 5), (3, 16), (8, 11)):
            m[i : i + 2, j] = 1
    return m


def main() -> None:
    rng = np.random.default_rng(0)
    lake_pats = ["point", "block_time", "sensor", "station"]
    ocean_pats = ["point", "block_time", "station", "argo"]
    fig, axes = plt.subplots(2, 4, figsize=(11.2, 4.8))
    for j, p in enumerate(lake_pats):
        axes[0, j].imshow(lake_mask(p, rng).T, aspect="auto", cmap="gray_r", vmin=0, vmax=1)
        axes[0, j].set_title(p, fontsize=10)
        axes[0, j].set_xticks([])
        axes[0, j].set_yticks([])
        if j == 0:
            axes[0, j].set_ylabel("Lake · node×var")
        axes[0, j].set_xlabel("time")
    for j, p in enumerate(ocean_pats):
        axes[1, j].imshow(ocean_mask(p, rng), aspect="auto", cmap="gray_r", vmin=0, vmax=1)
        axes[1, j].set_title(p if p != "argo" else "argo (columns)", fontsize=10)
        axes[1, j].set_xticks([])
        axes[1, j].set_yticks([])
        if j == 0:
            axes[1, j].set_ylabel("Ocean · plan view")
        axes[1, j].set_xlabel("x")
    fig.suptitle("Mask-View pattern bank (white = hidden)", fontsize=12)
    FIGURES.mkdir(parents=True, exist_ok=True)
    out = FIGURES / "fig_maskview_pattern_bank.png"
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Wrote", out)


if __name__ == "__main__":
    main()
