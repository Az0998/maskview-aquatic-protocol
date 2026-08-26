"""Paper A figure: lake recipe vs Linear, ocean ST vs dense history."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from config import FIGURES, TABLES


def main() -> None:
    lake = pd.read_csv(TABLES / "lake_pattern_winners.csv")
    ocean = pd.read_csv(TABLES / "ocean_pattern_winners.csv")
    shared = ["point", "block_time", "sensor", "station", "mixed"]
    L = lake.set_index("pattern").loc[shared]
    x = range(len(shared))
    w = 0.25

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    axes[0].bar([i - w for i in x], L["simple_Linear"], w, label="Linear", color="#6b7c85")
    axes[0].bar(list(x), L["learned_MaskViewST"], w, label="MaskView-ST", color="#7aa0ad")
    axes[0].bar([i + w for i in x], L["recipe_spatial_plus_l0"], w, label="spatial_plus_l0", color="#1f6f8b")
    axes[0].set_xticks(list(x), shared, rotation=20)
    axes[0].set_ylabel("Standardized MAE")
    axes[0].set_title("Lake Dianchi imputation")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set_ylim(0, 0.85)

    O = ocean.set_index("pattern")
    pats = [p for p in ["none", "point", "block_time", "sensor", "station", "argo"] if p in O.index]
    axes[1].bar(pats, O.loc[pats, "ST_RMSE"], color="#1f6f8b")
    axes[1].set_ylabel(r"Lead-1 RMSE ($\mu$mol kg$^{-1}$)")
    axes[1].set_title("ECS oxygen (ST Transformer)")
    axes[1].tick_params(axis="x", rotation=20)

    fig.suptitle("Mask-View protocol — ranking depends on missingness", fontsize=11)
    FIGURES.mkdir(parents=True, exist_ok=True)
    out = FIGURES / "fig_rank_reversal_two_media.png"
    fig.tight_layout()
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("Wrote", out)


if __name__ == "__main__":
    main()
