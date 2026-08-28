"""Lead-1 ST-climatology margin vs effective voxel keep (point vs station)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from config import FIGURES, OCEAN


def main() -> None:
    df = pd.read_csv(OCEAN / "keep_ratio_scan.csv")
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    pt = df[df.pattern == "point"].sort_values("keep_frac")
    st = df[df.pattern == "station"].sort_values("keep_frac")
    none = df[df.pattern == "none"].iloc[0]
    ax.axhline(0.0, color="#888", lw=0.8)
    ax.errorbar(
        pt.keep_frac,
        pt.point_delta_clim_minus_st,
        yerr=[
            pt.point_delta_clim_minus_st - pt.delta_clim_minus_st_p05,
            pt.delta_clim_minus_st_p95 - pt.point_delta_clim_minus_st,
        ],
        fmt="o-",
        color="#1f6f8b",
        label="point (random voxels)",
        capsize=3,
    )
    ax.errorbar(
        st.keep_frac,
        st.point_delta_clim_minus_st,
        yerr=[
            st.point_delta_clim_minus_st - st.delta_clim_minus_st_p05,
            st.delta_clim_minus_st_p95 - st.point_delta_clim_minus_st,
        ],
        fmt="s--",
        color="#b45309",
        label="station (columns)",
        capsize=3,
    )
    ax.scatter(
        [none.keep_frac],
        [none.point_delta_clim_minus_st],
        marker="D",
        color="#1f6f8b",
        zorder=5,
        label="dense history",
    )
    ax.set_xlabel("Effective voxel keep (water cells)")
    ax.set_ylabel(r"Lead-1 $\Delta$ = clim RMSE $-$ ST RMSE ($\mu$mol kg$^{-1}$)")
    ax.set_title("Tax is mostly how much history remains")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.05, 1.6)
    FIGURES.mkdir(parents=True, exist_ok=True)
    out = FIGURES / "fig_keep_ratio_tax.png"
    fig.tight_layout()
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("Wrote", out)


if __name__ == "__main__":
    main()
