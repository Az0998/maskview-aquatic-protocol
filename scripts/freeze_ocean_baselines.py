"""Compact ocean persist/clim/ST table from sibling experiment JSONs (optional refresh)."""
from __future__ import annotations

import json
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


def main() -> None:
    rows = []
    for pat, tag in TAG.items():
        path = SIBLING / f"multilead_{tag}.json"
        if not path.exists():
            print("missing", path)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for rec in payload.get("metrics", []):
            if rec.get("lead_months") != 1:
                continue
            if rec.get("model") not in MODELS:
                continue
            rows.append(
                {
                    "pattern": pat,
                    "model": rec["model"],
                    "lead": 1,
                    "RMSE": round(float(rec["rmse"]), 3),
                    "F1": round(float(rec["hypoxia_f1"]), 3),
                    "CSI": round(float(rec["hypoxia_csi"]), 3),
                }
            )
        # lead 2 climatology takeover
        for rec in payload.get("metrics", []):
            if rec.get("lead_months") != 2:
                continue
            if rec.get("model") not in MODELS:
                continue
            rows.append(
                {
                    "pattern": pat,
                    "model": rec["model"],
                    "lead": 2,
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


if __name__ == "__main__":
    main()
