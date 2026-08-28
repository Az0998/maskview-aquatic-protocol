"""Refresh ocean frozen tables from sibling experiment outputs (optional)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SIBLING = ROOT.parent / "ocean-do-forecast" / "results" / "tables"
OUT = ROOT / "data" / "frozen" / "ocean"

TAG = {
    "none": "full_physics",
    "point": "point_physics",
    "block": "block_physics",
    "block_time": "block_time_physics",
    "sensor": "sensor_physics",
    "station": "station_physics",
    "mixed": "mixed_physics",
    "argo": "argo_physics",
}
MODELS = ("persistence", "climatology", "st_transformer", "hybrid_clim_st")
LEADS = (1, 2, 3)
FAIR_FILES = (
    "fair_sparse_baselines.csv",
    "fair_sparse_baselines.md",
    "maskview_keep_rates.csv",
    "st_clim_bootstrap.csv",
    "st_clim_bootstrap.json",
    "st_clim_bootstrap.md",
    "keep_ratio_scan.csv",
    "keep_ratio_scan.json",
    "keep_ratio_scan.md",
)


def main() -> None:
    rows = []
    for pat, tag in TAG.items():
        path = SIBLING / f"multilead_{tag}.json"
        if not path.exists():
            print("missing", path)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for rec in payload.get("metrics", []):
            if rec.get("lead_months") not in LEADS:
                continue
            if rec.get("model") not in MODELS:
                continue
            rows.append(
                {
                    "pattern": pat,
                    "model": rec["model"],
                    "lead": int(rec["lead_months"]),
                    "RMSE": round(float(rec["rmse"]), 3),
                    "F1": round(float(rec["hypoxia_f1"]), 3),
                    "CSI": round(float(rec["hypoxia_csi"]), 3),
                }
            )
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "ocean_simple_vs_learned.csv"
    df.to_csv(out, index=False)
    print("Wrote", out, "n=", len(df))
    for name in FAIR_FILES:
        src = SIBLING / name
        if src.exists():
            shutil.copy2(src, OUT / name)
            print("copied", name)


if __name__ == "__main__":
    main()
